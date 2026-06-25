import logging
from typing import Optional
from datetime import date, datetime
from model.base import BaseModel

logger = logging.getLogger(__name__)


class AbsensiModel(BaseModel):
    TABLE = 'absensi'
    PK = 'id'
    ALLOWED_FIELDS = {'jam_masuk', 'jam_pulang', 'status', 'keterangan'}

    def create(self, user_id: int, tanggal: str, jam_masuk: Optional[str] = None,
               jam_pulang: Optional[str] = None, status: str = 'hadir',
               keterangan: Optional[str] = None) -> int:
        return super().create(
            user_id=user_id, tanggal=tanggal, jam_masuk=jam_masuk,
            jam_pulang=jam_pulang, status=status, keterangan=keterangan
        )

    def get_by_user(self, user_id: int) -> list[dict]:
        return self._fetchall(
            "SELECT * FROM absensi WHERE user_id = ? ORDER BY tanggal DESC",
            (user_id,)
        )

    def get_by_user_and_date(self, user_id: int, tanggal: str) -> Optional[dict]:
        return self._fetchone(
            "SELECT * FROM absensi WHERE user_id = ? AND tanggal = ?",
            (user_id, tanggal)
        )

    def get_today_by_user(self, user_id: int) -> Optional[dict]:
        return self._fetchone(
            """SELECT * FROM absensi
               WHERE user_id = ? AND tanggal = date('now', 'localtime')""",
            (user_id,)
        )

    def absen_masuk(self, user_id: int) -> int:
        today = date.today().isoformat()
        now = datetime.now().strftime('%H:%M:%S')
        return self.create(user_id=user_id, tanggal=today,
                           jam_masuk=now, status='hadir')

    def absen_pulang(self, user_id: int) -> bool:
        today = date.today().isoformat()
        now = datetime.now().strftime('%H:%M:%S')
        return self._execute_update(
            """UPDATE absensi
               SET jam_pulang = ?
               WHERE user_id = ? AND tanggal = ?""",
            (now, user_id, today)
        )

    def get_rekap_by_user(self, user_id: int, tahun: int) -> list[dict]:
        return self._fetchall(
            """SELECT strftime('%m', tanggal) AS bulan,
                      COUNT(*) AS total_hari,
                      SUM(CASE WHEN status = 'hadir' THEN 1 ELSE 0 END) AS hadir,
                      SUM(CASE WHEN status = 'izin' THEN 1 ELSE 0 END) AS izin,
                      SUM(CASE WHEN status = 'sakit' THEN 1 ELSE 0 END) AS sakit,
                      SUM(CASE WHEN status = 'alpha' THEN 1 ELSE 0 END) AS alpha
               FROM absensi
               WHERE user_id = ? AND strftime('%Y', tanggal) = ?
               GROUP BY strftime('%Y-%m', tanggal)
               ORDER BY bulan DESC""",
            (user_id, str(tahun))
        )

    def get_all_with_user(self) -> list[dict]:
        return self._fetchall(
            """SELECT a.*, u.nama AS user_nama, u.username
               FROM absensi a
               JOIN users u ON a.user_id = u.id
               ORDER BY a.tanggal DESC, a.jam_masuk DESC"""
        )

    def get_rekap_all_mahasiswa(self) -> list[dict]:
        return self._fetchall(
            """SELECT u.id, u.nama, u.username,
                      COUNT(a.id) AS total_absen,
                      SUM(CASE WHEN a.status = 'hadir' THEN 1 ELSE 0 END) AS hadir,
                      SUM(CASE WHEN a.status = 'izin' THEN 1 ELSE 0 END) AS izin,
                      SUM(CASE WHEN a.status = 'sakit' THEN 1 ELSE 0 END) AS sakit,
                      SUM(CASE WHEN a.status = 'alpha' THEN 1 ELSE 0 END) AS alpha
               FROM users u
               LEFT JOIN absensi a ON u.id = a.user_id
               WHERE u.role = 'mahasiswa'
               GROUP BY u.id, u.nama, u.username
               ORDER BY u.nama ASC"""
        )

    def get_by_tanggal(self, tanggal: str) -> list[dict]:
        return self._fetchall(
            """SELECT a.*, u.nama AS user_nama, u.username
               FROM absensi a
               JOIN users u ON a.user_id = u.id
               WHERE a.tanggal = ?
               ORDER BY u.nama ASC""",
            (tanggal,)
        )
