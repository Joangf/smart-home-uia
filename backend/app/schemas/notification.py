from pydantic import BaseModel
from typing import Optional
from app.core.enums import NotificationTypeEnum, SeverityEnum

class NotificationCreate(BaseModel):
    device_id: Optional[int] = None
    title: str
    description: str
    notification_type: NotificationTypeEnum
    severity: SeverityEnum
    is_read: Optional[bool] = False


class NotificationUpdate(BaseModel):
    is_read: bool


class NotificationResponse(BaseModel):
    notification_id: int
    device_id: Optional[int] = None
    title: str
    description: str
    notification_type: NotificationTypeEnum
    severity: SeverityEnum
    is_read: bool
    created_at: str