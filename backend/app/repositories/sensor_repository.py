from app.repositories import BaseRepository

class SensorRepository(BaseRepository):

    def __init__(self, db):
        super().__init__(db, "sensors")
