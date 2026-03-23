from fastapi import APIRouter, Depends, status
from app.schemas.sensor import SensorResponse
from app.services.sensor_service import SensorService
from app.core.dependencies import *

router = APIRouter(
    tags=["Sensors"],
    dependencies=[Depends(get_current_user)]
)


@router.get("/", response_model=list[SensorResponse])
def list_sensors(
    service: SensorService = Depends(get_sensor_service),
):
    return service.get_all()


@router.get("/{sensor_id}", response_model=SensorResponse)
def get_sensor(
    sensor_id: int,
    service: SensorService = Depends(get_sensor_service),
):
    return service.get_by_id(sensor_id)
