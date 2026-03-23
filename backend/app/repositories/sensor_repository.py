from app.repositories.base_repository import BaseRepository

class SensorRepository(BaseRepository):

    def __init__(self, db):
        super().__init__(db, "sensors")

    # def get_by_type(self, sensor_type: str):
    #     return self.db.table(self.table)\
    #         .select("*")\
    #         .eq("sensor_type", sensor_type)\
    #         .execute()
