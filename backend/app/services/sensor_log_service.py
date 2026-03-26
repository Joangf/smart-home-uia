from app.repositories import SensorLogRepository

from app.utils.logger import get_logger

logger = get_logger(__name__)


class SensorLogService:
    def __init__(self, repo: SensorLogRepository):
        self.repo = repo
        logger.info("SensorLogService initialized with SensorLogRepository")

    def get_all(self) -> list:
        return self.repo.get_all()

    def get_by_sensor_id(self, sensor_id: int) -> list:
        return self.repo.get_by_sensor_id(sensor_id)