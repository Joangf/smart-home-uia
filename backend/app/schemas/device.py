from pydantic import BaseModel
from typing import Optional
from app.core.enums import DeviceTypeEnum, DeviceModeEnum

class DeviceCreate(BaseModel):
    device_name: str
    device_type: DeviceTypeEnum
    pin_number: int
    location: Optional[str] = "Unknown"
    status: Optional[str] = "online"
    is_active: Optional[bool] = True

class DeviceUpdate(BaseModel):
    device_name: Optional[str]
    device_type: Optional[DeviceTypeEnum]
    pin_number: Optional[int]
    location: Optional[str]
    device_mode: Optional[DeviceModeEnum]
    status: Optional[str]
    is_active: Optional[bool]

class DeviceResponse(BaseModel):
    device_id: int
    device_name: str
    device_type: DeviceTypeEnum
    pin_number: int
    location: str
    device_mode: DeviceModeEnum
    status: str
    is_active: bool
    