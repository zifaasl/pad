import logging
from typing import Any, Optional
from database import get_connection

logger = logging.getLogger(__name__)


class BaseModel:
    TABLE: str = ''
    PK: str = 'id'

    def _fetchone(self, query: str, params: tuple = ()) -> Optional[dict]:
        try:
            with get_connection() as conn:
                row = conn.execute(query, params).fetchone()
                return dict(row) if row else None
        except Exception as e:
            logger.error("Query error [%s]: %s | params=%s", self.TABLE, e, params)
            raise

    def _fetchall(self, query: str, params: tuple = ()) -> list[dict]:
        try:
            with get_connection() as conn:
                rows = conn.execute(query, params).fetchall()
                return [dict(r) for r in rows]
        except Exception as e:
            logger.error("Query error [%s]: %s | params=%s", self.TABLE, e, params)
            raise

    def _execute(self, query: str, params: tuple = ()) -> int:
        try:
            with get_connection() as conn:
                cursor = conn.execute(query, params)
                return cursor.lastrowid
        except Exception as e:
            logger.error("Execute error [%s]: %s | params=%s", self.TABLE, e, params)
            raise

    def _execute_update(self, query: str, params: tuple = ()) -> bool:
        try:
            with get_connection() as conn:
                cursor = conn.execute(query, params)
                return cursor.rowcount > 0
        except Exception as e:
            logger.error("Update error [%s]: %s | params=%s", self.TABLE, e, params)
            raise

    def create(self, **kwargs: Any) -> int:
        columns = ", ".join(kwargs.keys())
        placeholders = ", ".join("?" for _ in kwargs)
        values = tuple(kwargs.values())
        query = f"INSERT INTO {self.TABLE} ({columns}) VALUES ({placeholders})"
        return self._execute(query, values)

    def read(self, pk: Any) -> Optional[dict]:
        return self._fetchone(
            f"SELECT * FROM {self.TABLE} WHERE {self.PK} = ?", (pk,)
        )

    def update(self, pk: Any, **kwargs: Any) -> bool:
        allowed = getattr(self, 'ALLOWED_FIELDS', set(kwargs.keys()))
        fields = {k: v for k, v in kwargs.items() if k in allowed and v is not None}
        if not fields:
            return False
        set_clause = ", ".join(f"{k} = ?" for k in fields)
        values = list(fields.values()) + [pk]
        query = f"UPDATE {self.TABLE} SET {set_clause} WHERE {self.PK} = ?"
        return self._execute_update(query, values)

    def delete(self, pk: Any) -> bool:
        return self._execute_update(
            f"DELETE FROM {self.TABLE} WHERE {self.PK} = ?", (pk,)
        )

    def search(self, keyword: str, fields: list[str]) -> list[dict]:
        pattern = f"%{keyword}%"
        conditions = " OR ".join(f"{f} LIKE ?" for f in fields)
        params = tuple(pattern for _ in fields)
        return self._fetchall(
            f"SELECT * FROM {self.TABLE} WHERE {conditions}", params
        )
