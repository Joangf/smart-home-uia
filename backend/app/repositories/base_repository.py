from typing import Any

class BaseRepository:
    def __init__(self, db, table_name: str):
        self.db = db
        self.table_name = table_name
        self.pk = f"{table_name[:-1]}_id"

    def _table(self) -> Any:
        return self.db.table(self.table_name)
    
    def get_all(self) -> list:
        res = self._table().select("*").execute()
        return res.data

    def get_by_id(self, id: int) -> dict | None:
        res = self._table().select("*").eq(self.pk, id).execute()
        return res.data[0] if res.data and len(res.data) > 0 else None

    def create(self, data: dict) -> dict:
        res = self._table().insert(data).execute()
        return res.data[0]

    def update(self, id: int, data: dict) -> dict | None:
        res = self._table().update(data).eq(self.pk, id).execute()
        return res.data[0] if res.data else None

    def delete(self, id: int) -> bool:
        res = self._table().delete().eq(self.pk, id).execute()
        return bool(res.data)