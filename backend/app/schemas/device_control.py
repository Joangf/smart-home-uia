from pydantic import BaseModel
from typing import Optional
from app.core.enums import ActionEnum, SourceEnum
class DeviceControlCreate(BaseModel):
    device_id: int
    action: ActionEnum
    value: Optional[str]
    source: SourceEnum

# class DeviceControlUpdate(BaseModel):
#     pass

class DeviceControlResponse(BaseModel):
    device_control_id: int
    device_id: int
    action: ActionEnum
    value: Optional[str]
    source: SourceEnum
    executed_at: str