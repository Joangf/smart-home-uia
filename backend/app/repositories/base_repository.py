from typing import Any
from app.core.exceptions import DatabaseException
class BaseRepository:
    def __init__(self, db, table_name: str):
        self.db = db
        self.table_name = table_name
        self.pk = f"{table_name[:-1]}_id"

    def _table(self) -> Any:
        return self.db.table(self.table_name)
    
    def _execute(self, query) -> Any:
        try:
            return query.execute()
        except Exception as e:
            raise DatabaseException(str(e))

    def get_all(self) -> list:
        res = self._execute(self._table().select("*"))
        return res.data

    def get_by_id(self, id: int) -> dict | None:
        res = self._execute(self._table().select("*").eq(self.pk, id))
        return res.data[0] if res.data and len(res.data) > 0 else None

    def create(self, data: dict) -> dict:
        res = self._execute(self._table().insert(data))
        return res.data[0]

    def update(self, id: int, data: dict) -> dict | None:
        res = self._execute(self._table().update(data).eq(self.pk, id))
        return res.data[0] if res.data else None

    def delete(self, id: int) -> bool:
        res = self._execute(self._table().delete().eq(self.pk, id))
        return bool(res.data)