from app.repositories import BaseRepository

class DeviceRepository(BaseRepository):

    def __init__(self, db):
        super().__init__(db, "devices")

    def get_by_name(self, name: str) -> dict | None:
        res = self._table().select("*").eq("device_name", name).execute()
        return res.data[0] if res.data else None

    # def get_by_type(self, device_type: str):
    #     return self.db.table(self.table)\
    #         .select("*")\
    #         .eq("device_type", device_type)\
    #         .execute()

    # def get_active_devices(self):
    #     return self.db.table(self.table)\
    #         .select("*")\
    #         .eq("is_active", True)\
    #         .execute()

    # def update_status(self, device_id: int, status: str):
    #     return self.db.table(self.table)\
    #         .update({"status": status})\
    #         .eq("id", device_id)\
    #         .execute()