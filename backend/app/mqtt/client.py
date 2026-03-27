import json
import asyncio
import paho.mqtt.client as mqtt
import threading
from typing import Optional

from app.core.config import settings
from app.utils.logger import get_logger
from app.websocket.manager import ws_manager

logger = get_logger(__name__)


class MQTTClientManager:
    """Thread-safe MQTT client with proper event loop handling."""
    
    _lock = threading.Lock()
    _loop: Optional[asyncio.AbstractEventLoop] = None
    _client: Optional[mqtt.Client] = None
    
    @classmethod
    def set_event_loop(cls, loop: asyncio.AbstractEventLoop) -> None:
        """Set the event loop (thread-safe)."""
        with cls._lock:
            cls._loop = loop
            logger.debug(f"Event loop set to {loop}")
    
    @classmethod
    def get_event_loop(cls) -> Optional[asyncio.AbstractEventLoop]:
        """Get the event loop (thread-safe)."""
        with cls._lock:
            return cls._loop
    
    @classmethod
    def push_to_ws(
        cls, 
        device_id: str, 
        data: dict,
        timeout: float = 5.0
    ) -> bool:
        """
        Thread-safe bridge: MQTT thread -> async WebSocket.
        
        Args:
            device_id: Device identifier
            data: Message data
            timeout: Timeout in seconds
            
        Returns:
            True if successfully queued, False otherwise
        """
        loop = cls.get_event_loop()
        
        if loop is None:
            logger.warning(
                f"Event loop not initialized when pushing to WS for {device_id}. "
                "Make sure set_event_loop() was called."
            )
            return False
        
        try:
            future = asyncio.run_coroutine_threadsafe(
                ws_manager.broadcast_to_device(device_id, data),
                loop
            )
            # Wait for the coroutine to complete with timeout
            future.result(timeout=timeout)
            return True
            
        except asyncio.TimeoutError:
            logger.error(
                f"Timeout pushing message to {device_id} after {timeout}s. "
                "WebSocket broadcast may be overloaded."
            )
            return False
            
        except Exception as e:
            logger.error(
                f"Failed to push message to {device_id}: {type(e).__name__}: {e}",
                exc_info=True
            )
            return False
    
    @classmethod
    def set_client(cls, client: mqtt.Client) -> None:
        """Store the MQTT client reference."""
        with cls._lock:
            cls._client = client


# Module-level interface (backward compatible)
def set_event_loop(loop: asyncio.AbstractEventLoop) -> None:
    """Set the event loop."""
    MQTTClientManager.set_event_loop(loop)


def _push_to_ws(device_id: str, data: dict) -> bool:
    """Thread-safe bridge: MQTT thread -> async WebSocket."""
    return MQTTClientManager.push_to_ws(device_id, data)


def on_connect(client, userdata, flags, reason_code, properties=None):
    """Handle MQTT connection."""
    if reason_code == 0:
        logger.info("Connected to MQTT Broker successfully.")
        client.subscribe("devices/#", qos=1)
        logger.info("Subscribed to 'devices/#' topic")
    else:
        logger.error(
            f"Failed to connect to MQTT Broker, return code: {reason_code}. "
            "Check broker address and credentials."
        )


def on_disconnect(client, userdata, disconnect_flags, reason_code, properties=None):
    """Handle MQTT disconnection."""
    if reason_code != 0:
        logger.warning(
            f"Unexpected disconnect (code={reason_code}). "
            "Auto-reconnect in progress..."
        )
    else:
        logger.info("MQTT client disconnected cleanly")


def on_message(client, userdata, msg):
    """Handle incoming MQTT message."""
    try:
        topic = msg.topic
        payload = json.loads(msg.payload.decode())
        
        parts = topic.split("/")  # ["devices", "esp32_001", "sensors", "light"]
        if len(parts) < 3:
            logger.warning(f"Invalid topic format: {topic}")
            return
        
        device_id = parts[1]              # "esp32_001"
        sub_path = "/".join(parts[2:])    # "sensors/light"
        
        route_message(device_id, sub_path, payload)
        
    except json.JSONDecodeError:
        logger.warning(f"Invalid JSON on topic {msg.topic}: {msg.payload}")
    except Exception as e:
        logger.error(f"Error processing message from {msg.topic}: {e}", exc_info=True)


def route_message(device_id: str, sub_path: str, data: dict) -> None:
    """Route message to appropriate handler."""
    handlers = {
        "sensors/light": handle_light_data,
        "sensors/dht20": handle_dht20_data,
        "status": handle_status_data,
    }
    
    handler = handlers.get(sub_path)
    if handler:
        try:
            handler(device_id, data)
        except Exception as e:
            logger.error(
                f"Error in handler for {device_id}/{sub_path}: {e}",
                exc_info=True
            )
    else:
        logger.debug(f"No handler for topic: {sub_path}")


def handle_light_data(device_id: str, data: dict) -> None:
    """Handle light sensor data."""
    lux = data.get('lux', 'N/A')
    condition = data.get('condition', 'N/A')
    logger.info(f"[{device_id}]Light -> lux={lux}, condition={condition}")
    
    success = _push_to_ws(device_id, {"type": "light", **data})
    if not success:
        logger.warning(f"Failed to broadcast light data to {device_id}")


def handle_dht20_data(device_id: str, data: dict) -> None:
    """Handle DHT20 sensor data."""
    temp = data.get('temperature_c', 'N/A')
    humidity = data.get('humidity_pct', 'N/A')
    logger.info(f"[{device_id}]DHT20 -> temp={temp}°C, humidity={humidity}%")
    
    success = _push_to_ws(device_id, {"type": "dht20", **data})
    if not success:
        logger.warning(f"Failed to broadcast DHT20 data to {device_id}")


def handle_status_data(device_id: str, data: dict) -> None:
    """Handle device status."""
    status = data.get('status', 'UNKNOWN')
    logger.info(f"[{device_id}]Status -> {status}")
    
    success = _push_to_ws(device_id, {"type": "status", **data})
    if not success:
        logger.warning(f"Failed to broadcast status to {device_id}")


def start_mqtt() -> Optional[mqtt.Client]:
    """
    Start MQTT client and connect to broker.
    
    Returns:
        mqtt.Client instance if successful, None otherwise
    """
    try:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        
        # Set callbacks
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.on_message = on_message
        
        # Configure auto-reconnect
        client.reconnect_delay_set(min_delay=2, max_delay=30)
        
        # Optional: Set authentication
        # if settings.MQTT_USER and settings.MQTT_PASSWORD:
        #     client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
        
        # Connect to broker
        logger.info(
            f"Connecting to MQTT Broker at {settings.MQTT_BROKER}:"
            f"{settings.MQTT_PORT}..."
        )
        client.connect(settings.MQTT_BROKER, settings.MQTT_PORT, keepalive=60)
        
        # Start background thread
        client.loop_start()
        logger.info("MQTT client started (background thread)")
        
        # Store client reference
        MQTTClientManager.set_client(client)
        
        return client
        
    except ConnectionRefusedError:
        logger.critical(
            f"Connection refused by MQTT Broker at "
            f"{settings.MQTT_BROKER}:{settings.MQTT_PORT}. "
            "Check if broker is running."
        )
        return None
        
    except OSError as e:
        logger.critical(
            f"Network error connecting to MQTT Broker: {e}. "
            "Check broker address and network connectivity."
        )
        return None
        
    except Exception as e:
        logger.critical(
            f"Unexpected error starting MQTT client: {type(e).__name__}: {e}",
            exc_info=True
        )
        return None


def stop_mqtt(client: Optional[mqtt.Client]) -> None:
    """Gracefully stop MQTT client."""
    if client is not None:
        try:
            client.loop_stop()
            logger.info("MQTT client stopped")
        except Exception as e:
            logger.error(f"Error stopping MQTT client: {e}")