from pydantic import BaseModel
from typing import Optional

# class AlertThresholdCreate(BaseModel):
#     pass

class AlertThresholdUpdate(BaseModel):
    min_threshold: Optional[float]
    max_threshold: Optional[float]
    is_active: Optional[bool]

class AlertThresholdResponse(BaseModel):
    alert_threshold_id: int
    sensor_id: int
    min_threshold: Optional[float]
    max_threshold: Optional[float]
    is_active: Optional[bool]