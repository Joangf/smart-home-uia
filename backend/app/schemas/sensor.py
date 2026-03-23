from pydantic import BaseModel
from typing import Optional

class SensorCreate(BaseModel):
    pass

class SensorUpdate(BaseModel):
    pass

class SensorResponse(BaseModel):
    sensor_id: int
    device_id: int
    sensor_type: str
    unit: str
    min_valid: Optional[float]
    max_valid: Optional[float]
    
    