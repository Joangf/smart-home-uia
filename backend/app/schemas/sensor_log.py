from pydantic import BaseModel

class SensorLogResponse(BaseModel):
    sensor_log_id: int
    sensor_id: int
    value: float
    is_valid: bool
    recorded_at: str