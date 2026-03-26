import json
import paho.mqtt.client as mqtt

from app.core.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        logger.info("Connected to MQTT Broker successfully.")
        client.subscribe("devices/#", qos=1)
    else:
        logger.error(f"Failed to connect, return code {reason_code}")

def on_message(client, userdata, msg):
    try:
        topic = msg.topic
        payload = msg.payload.decode()
        # logger.info(f"Received: {topic} -> {payload}")

        # data = json.loads(payload)
        # handle_device_data(topic, data)
    except json.JSONDecodeError:
        logger.warning(f"Invalid JSON format on topic {msg.topic}: {msg.payload}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")

def handle_device_data(topic, data):
    device_id = topic.split('/')[-1]
    logger.debug(f"Handling data for device {device_id}: {data}")

def start_mqtt():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    
    # if settings.MQTT_USER and settings.MQTT_PASSWORD:
        # client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)

    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(settings.MQTT_BROKER, settings.MQTT_PORT, keepalive=60)
        client.loop_start()
        return client
    except Exception as e:
        logger.critical(f"Could not connect to MQTT Broker: {e}")
        return None