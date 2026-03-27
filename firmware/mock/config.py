from dataclasses import dataclass

@dataclass
class MQTTConfig:
    host: str = "localhost"
    port: int = 1883
    keepalive: int = 60

@dataclass
class DeviceConfig:
    light_id: str = "3"
    light_location: str = "Living Room"

    dht20_id: str = "5"
    dht20_location: str = "Bedroom"

    device_id: str = "yolobits"

TOPIC_LIGHT = "devices/{light_id}/sensors/light"
TOPIC_DHT20 = "devices/{dht20_id}/sensors/dht20"
TOPIC_STATUS = "devices/{device_id}/status"

# Tần suất gửi (giây)
PUBLISH_INTERVAL_LIGHT = 3   # ánh sáng cập nhật nhanh hơn
PUBLISH_INTERVAL_DHT20 = 10  # nhiệt độ/độ ẩm cập nhật chậm hơn