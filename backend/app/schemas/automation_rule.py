from pydantic import BaseModel
from typing import Optional
from app.core.enums import TriggerTypeEnum, ConditionOperatorEnum, ActionEnum

class AutomationRuleCreate(BaseModel):
    device_id: int
    sensor_id: Optional[int] 
    automation_rule_name: str
    trigger_type: TriggerTypeEnum
    condition_operator: Optional[ConditionOperatorEnum]
    condition_value: Optional[float] 
    schedule_time: Optional[str] 
    repeat_days: Optional[str] 
    action: ActionEnum
    is_active: Optional[bool] = True


class AutomationRuleUpdate(BaseModel):
    device_id: Optional[int]
    sensor_id: Optional[int] 
    automation_rule_name: Optional[str] 
    trigger_type: Optional[TriggerTypeEnum]
    condition_operator: Optional[ConditionOperatorEnum] 
    condition_value: Optional[float] 
    schedule_time: Optional[str] 
    repeat_days: Optional[str] 
    action: Optional[ActionEnum] 
    is_active: Optional[bool]


class AutomationRuleResponse(BaseModel):
    automation_rule_id: int
    device_id: int
    sensor_id: Optional[int] 
    automation_rule_name: str
    trigger_type: TriggerTypeEnum
    condition_operator: Optional[ConditionOperatorEnum] 
    condition_value: Optional[float] 
    schedule_time: Optional[str] 
    repeat_days: Optional[str] 
    action: ActionEnum
    is_active: bool