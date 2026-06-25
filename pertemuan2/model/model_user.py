import logging
from typing import Optional
from model.base import BaseModel

logger = logging.getLogger(__name__)


class UserModel(BaseModel):
    TABLE = 'users'
    PK = 'id'
    ALLOWED_FIELDS = {'username', 'password', 'role', 'nama'}

    def create(self, username: str, password: str, role: str, nama: str) -> int:
        return super().create(username=username, password=password,
                              role=role, nama=nama)

    def login(self, username: str, password: str) -> Optional[dict]:
        return self._fetchone(
            """SELECT id, username, role, nama FROM users
               WHERE username = ? AND password = ?""",
            (username, password)
        )

    def get_by_role(self, role: str) -> list[dict]:
        return self._fetchall(
            "SELECT * FROM users WHERE role = ? ORDER BY nama ASC", (role,)
        )
