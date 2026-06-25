import logging
from typing import Optional
from datetime import date, datetime
from model.model_user import UserModel
from model.model_absensi import AbsensiModel

logger = logging.getLogger(__name__)


class AbsensiController:
    def __init__(self):
        self._absensi_model = AbsensiModel()
        self._user_model = UserModel()

    def tambah_absensi(self, user_id: int, tanggal: Optional[str] = None,
                       jam_masuk: Optional[str] = None,
                       jam_pulang: Optional[str] = None,
                       status: str = 'hadir',
                       keterangan: Optional[str] = None) -> dict:
        try:
            user = self._user_model.read(user_id)
            if not user:
                return {'success': False, 'message': 'User tidak ditemukan'}
            if user['role'] != 'mahasiswa':
                return {'success': False, 'message': 'Hanya mahasiswa yang bisa diabsensi'}

            if not tanggal:
                tanggal = date.today().isoformat()
            if not jam_masuk:
                jam_masuk = datetime.now().strftime('%H:%M:%S')

            existing = self._absensi_model.get_by_user_and_date(user_id, tanggal)
            if existing:
                return {'success': False,
                        'message': f'Mahasiswa sudah diabsen pada tanggal {tanggal}'}

            absensi_id = self._absensi_model.create(
                user_id=user_id, tanggal=tanggal, jam_masuk=jam_masuk,
                jam_pulang=jam_pulang, status=status, keterangan=keterangan
            )
            logger.info("Absensi dibuat: id=%d, user=%d, tgl=%s", absensi_id, user_id, tanggal)
            return {'success': True, 'message': 'Absensi berhasil ditambahkan', 'id': absensi_id}
        except Exception as e:
            logger.error("Gagal tambah absensi: %s", e, exc_info=True)
            return {'success': False, 'message': 'Terjadi kesalahan sistem'}

    def edit_absensi(self, absensi_id: int, **kwargs) -> dict:
        try:
            absensi = self._absensi_model.read(absensi_id)
            if not absensi:
                return {'success': False, 'message': 'Data absensi tidak ditemukan'}

            updated = self._absensi_model.update(absensi_id, **kwargs)
            if updated:
                logger.info("Absensi diupdate: id=%d, data=%s", absensi_id, kwargs)
                return {'success': True, 'message': 'Absensi berhasil diperbarui'}
            return {'success': False, 'message': 'Tidak ada data yang diubah'}
        except Exception as e:
            logger.error("Gagal edit absensi: %s", e, exc_info=True)
            return {'success': False, 'message': 'Terjadi kesalahan sistem'}

    def hapus_absensi(self, absensi_id: int) -> dict:
        try:
            absensi = self._absensi_model.read(absensi_id)
            if not absensi:
                return {'success': False, 'message': 'Data absensi tidak ditemukan'}

            deleted = self._absensi_model.delete(absensi_id)
            if deleted:
                logger.info("Absensi dihapus: id=%d", absensi_id)
                return {'success': True, 'message': 'Absensi berhasil dihapus'}
            return {'success': False, 'message': 'Gagal menghapus absensi'}
        except Exception as e:
            logger.error("Gagal hapus absensi: %s", e, exc_info=True)
            return {'success': False, 'message': 'Terjadi kesalahan sistem'}

    def absen_masuk(self, user_id: int) -> dict:
        try:
            existing = self._absensi_model.get_today_by_user(user_id)
            if existing:
                return {'success': False, 'message': 'Sudah absen masuk hari ini'}

            absensi_id = self._absensi_model.absen_masuk(user_id)
            logger.info("Absen masuk: user=%d, id=%d", user_id, absensi_id)
            return {'success': True, 'message': 'Absen masuk berhasil', 'id': absensi_id}
        except Exception as e:
            logger.error("Gagal absen masuk: %s", e, exc_info=True)
            return {'success': False, 'message': 'Terjadi kesalahan sistem'}

    def absen_pulang(self, user_id: int) -> dict:
        try:
            today = self._absensi_model.get_today_by_user(user_id)
            if not today:
                return {'success': False, 'message': 'Belum absen masuk hari ini'}
            if today.get('jam_pulang'):
                return {'success': False, 'message': 'Sudah absen pulang hari ini'}

            updated = self._absensi_model.absen_pulang(user_id)
            if updated:
                logger.info("Absen pulang: user=%d", user_id)
                return {'success': True, 'message': 'Absen pulang berhasil'}
            return {'success': False, 'message': 'Gagal absen pulang'}
        except Exception as e:
            logger.error("Gagal absen pulang: %s", e, exc_info=True)
            return {'success': False, 'message': 'Terjadi kesalahan sistem'}

    def cek_absen_hari_ini(self, user_id: int) -> dict:
        try:
            absensi = self._absensi_model.get_today_by_user(user_id)
            return {'success': True, 'sudah_absen': absensi is not None, 'data': absensi}
        except Exception as e:
            logger.error("Gagal cek absen: %s", e, exc_info=True)
            return {'success': False, 'message': 'Terjadi kesalahan sistem'}

    def rekap_semua_mahasiswa(self) -> dict:
        try:
            rows = self._absensi_model.get_rekap_all_mahasiswa()
            logger.info("Rekap semua mahasiswa: %d rows", len(rows))
            return {'success': True, 'data': rows}
        except Exception as e:
            logger.error("Gagal ambil rekap: %s", e, exc_info=True)
            return {'success': False, 'message': 'Terjadi kesalahan sistem'}

    def riwayat_absensi(self, user_id: Optional[int] = None,
                        tanggal: Optional[str] = None,
                        bulan: Optional[int] = None,
                        tahun: Optional[int] = None) -> dict:
        try:
            if user_id:
                user = self._user_model.read(user_id)
                if not user:
                    return {'success': False, 'message': 'User tidak ditemukan'}
                if tanggal:
                    rows = self._absensi_model.get_by_user_and_date(user_id, tanggal)
                    rows = [rows] if rows else []
                elif bulan and tahun:
                    rows = self._absensi_model.get_rekap_by_user(user_id, tahun)
                    rows = [r for r in rows if int(r['bulan']) == bulan]
                else:
                    rows = self._absensi_model.get_by_user(user_id)
                return {'success': True, 'data': rows}

            if tanggal:
                rows = self._absensi_model.get_by_tanggal(tanggal)
                return {'success': True, 'data': rows}

            rows = self._absensi_model.get_all_with_user()
            return {'success': True, 'data': rows}
        except Exception as e:
            logger.error("Gagal ambil riwayat: %s", e, exc_info=True)
            return {'success': False, 'message': 'Terjadi kesalahan sistem'}
