from pydantic import BaseModel
# from typing import Optional
from app.core.enums import SensorTypeEnum
# class SensorCreate(BaseModel):
#     pass

# class SensorUpdate(BaseModel):
#     pass
class SensorResponse(BaseModel):
    sensor_id: int
    device_id: int
    sensor_type: SensorTypeEnum
    unit: str
    min_valid: float
    max_valid: float
    
    