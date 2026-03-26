from app.repositories import BaseRepository


class SensorLogRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, "sensor_logs")

    def get_by_sensor_id(self, sensor_id: int) -> list:
        res = self._execute(self._table().select("*").eq("sensor_id", sensor_id))
        return res.data if res.data else []