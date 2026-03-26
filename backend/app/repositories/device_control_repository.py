from app.repositories import BaseRepository

class DeviceControlRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, "device_controls")

    def get_by_device_id(self, device_id: int) -> list:
        res = self._execute(self._table().select("*").eq("device_id", device_id))
        return res.data if res.data else []