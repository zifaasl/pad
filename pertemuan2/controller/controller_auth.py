import logging
from typing import Optional
from model.model_user import UserModel

logger = logging.getLogger(__name__)


class AuthController:
    def __init__(self):
        self._user_model = UserModel()
        self._logged_in_user: Optional[dict] = None

    def login(self, username: str, password: str) -> dict:
        try:
            if not username or not password:
                return {'success': False, 'message': 'Username dan password harus diisi'}

            user = self._user_model.login(username, password)
            if not user:
                logger.warning("Login gagal untuk username: %s", username)
                return {'success': False, 'message': 'Username atau password salah'}

            self._logged_in_user = user
            logger.info("Login berhasil: %s (%s)", user['nama'], user['role'])
            return {'success': True, 'message': 'Login berhasil', 'user': user}
        except Exception as e:
            logger.error("Error saat login: %s", e, exc_info=True)
            return {'success': False, 'message': 'Terjadi kesalahan sistem'}

    def logout(self) -> dict:
        if self._logged_in_user:
            logger.info("Logout: %s", self._logged_in_user['nama'])
        self._logged_in_user = None
        return {'success': True, 'message': 'Logout berhasil'}

    def validasi_role(self, required_role: str) -> dict:
        if not self._logged_in_user:
            return {'success': False, 'message': 'Belum login'}
        if self._logged_in_user['role'] != required_role:
            return {'success': False,
                    'message': f'Akses ditolak. Dibutuhkan role: {required_role}'}
        return {'success': True, 'message': 'Role valid'}

    def get_current_user(self) -> Optional[dict]:
        return dict(self._logged_in_user) if self._logged_in_user else None

    def is_authenticated(self) -> bool:
        return self._logged_in_user is not None

    def set_user(self, user: dict) -> None:
        self._logged_in_user = user
