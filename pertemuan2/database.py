import sqlite3
import hashlib
import os
from datetime import datetime, date

DB_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "absensi.db")


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('dosen', 'mahasiswa')),
            nama TEXT NOT NULL,
            nim_nip TEXT,
            prodi TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS absensi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            tanggal DATE NOT NULL,
            jam_masuk TEXT,
            jam_pulang TEXT,
            status TEXT DEFAULT 'hadir' CHECK(status IN ('hadir','izin','sakit','alpha')),
            keterangan TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(user_id, tanggal)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mata_kuliah (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kode TEXT UNIQUE NOT NULL,
            nama TEXT NOT NULL,
            sks INTEGER DEFAULT 2,
            dosen_id INTEGER,
            FOREIGN KEY (dosen_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()


def insert_default_data():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            users = [
                ('dosen1', hash_password('123456'), 'dosen', 'M. Reza Fahlevi', 'NIP-198001012010011001', 'Teknik Informatika'),
                ('dosen2', hash_password('123456'), 'dosen', 'Sry Dhina Pohan, S.Kom.,M.Kom.', 'NIP-197505152005012002', 'Sistem Informasi'),
                ('mahasiswa1', hash_password('123456'), 'mahasiswa', 'Adilah Nazifah Salamah', '2023010001', 'Teknik Informatika'),
                ('mahasiswa2', hash_password('123456'), 'mahasiswa', 'Paramadina Mulya', '2023010002', 'Teknik Informatika'),
                ('mahasiswa3', hash_password('123456'), 'mahasiswa', 'Rahma Aulia', '2023010003', 'Sistem Informasi'),
                ('mahasiswa4', hash_password('123456'), 'mahasiswa', 'Setiawati', '2023010004', 'Sistem Informasi'),
            ]
            cursor.executemany(
                'INSERT INTO users (username, password, role, nama, nim_nip, prodi) VALUES (?,?,?,?,?,?)',
                users
            )

            # Sample mata kuliah
            mata_kuliah = [
                ('IF101', 'Algoritma & Pemrograman', 3, 1),
                ('IF202', 'Basis Data', 3, 1),
                ('SI101', 'Sistem Informasi Manajemen', 2, 2),
            ]
            cursor.executemany(
                'INSERT INTO mata_kuliah (kode, nama, sks, dosen_id) VALUES (?,?,?,?)',
                mata_kuliah
            )

            # Sample absensi data
            from datetime import timedelta
            today = date.today()
            statuses = ['hadir', 'hadir', 'hadir', 'izin', 'hadir', 'hadir', 'sakit', 'hadir']
            for mhs_id in [3, 4, 5, 6]:
                for i, status in enumerate(statuses):
                    d = today - timedelta(days=len(statuses) - i)
                    jam_masuk = '07:30' if status == 'hadir' else None
                    jam_pulang = '16:00' if status == 'hadir' else None
                    try:
                        cursor.execute(
                            'INSERT INTO absensi (user_id, tanggal, jam_masuk, jam_pulang, status) VALUES (?,?,?,?,?)',
                            (mhs_id, d.strftime('%Y-%m-%d'), jam_masuk, jam_pulang, status)
                        )
                    except:
                        pass

            conn.commit()
    except Exception as e:
        print(f"Seeding error: {e}")
    finally:
        conn.close()


# ──────────────────── AUTH ────────────────────
def authenticate(username: str, password: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hash_password(password))
    )
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None


# ──────────────────── ABSENSI ────────────────────
def absen_masuk(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    today = date.today().strftime('%Y-%m-%d')
    now = datetime.now().strftime('%H:%M')
    try:
        cursor.execute(
            "INSERT OR IGNORE INTO absensi (user_id, tanggal, jam_masuk, status) VALUES (?,?,?,?)",
            (user_id, today, now, 'hadir')
        )
        conn.commit()
        return True, "Absen masuk berhasil!"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()


def absen_pulang(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    today = date.today().strftime('%Y-%m-%d')
    now = datetime.now().strftime('%H:%M')
    try:
        cursor.execute(
            "UPDATE absensi SET jam_pulang=? WHERE user_id=? AND tanggal=? AND jam_pulang IS NULL",
            (now, user_id, today)
        )
        if cursor.rowcount == 0:
            conn.close()
            return False, "Belum absen masuk atau sudah absen pulang."
        conn.commit()
        return True, "Absen pulang berhasil!"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()


def get_absensi_mahasiswa(user_id: int, limit: int = 30):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM absensi WHERE user_id=? ORDER BY tanggal DESC LIMIT ?",
        (user_id, limit)
    )
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def get_absensi_today(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    today = date.today().strftime('%Y-%m-%d')
    cursor.execute("SELECT * FROM absensi WHERE user_id=? AND tanggal=?", (user_id, today))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_statistik_mahasiswa(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT status, COUNT(*) as total FROM absensi WHERE user_id=? GROUP BY status",
        (user_id,)
    )
    stats = {r['status']: r['total'] for r in cursor.fetchall()}
    conn.close()
    return stats


# ──────────────────── DOSEN ────────────────────
def get_all_mahasiswa():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE role='mahasiswa' ORDER BY nama")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def get_rekap_absensi_semua(limit: int = 50):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT a.*, u.nama, u.nim_nip, u.prodi
        FROM absensi a
        JOIN users u ON a.user_id = u.id
        WHERE u.role = 'mahasiswa'
        ORDER BY a.tanggal DESC, u.nama ASC
        LIMIT ?
    ''', (limit,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def get_statistik_kelas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT u.nama, u.nim_nip, u.prodi,
               SUM(CASE WHEN a.status='hadir' THEN 1 ELSE 0 END) as hadir,
               SUM(CASE WHEN a.status='izin' THEN 1 ELSE 0 END) as izin,
               SUM(CASE WHEN a.status='sakit' THEN 1 ELSE 0 END) as sakit,
               SUM(CASE WHEN a.status='alpha' THEN 1 ELSE 0 END) as alpha,
               COUNT(a.id) as total
        FROM users u
        LEFT JOIN absensi a ON u.id = a.user_id
        WHERE u.role = 'mahasiswa'
        GROUP BY u.id
        ORDER BY u.nama
    ''')
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def update_absensi_mahasiswa(user_id: int, tanggal: str, status: str, keterangan: str = ''):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            '''INSERT INTO absensi (user_id, tanggal, status, keterangan)
               VALUES (?,?,?,?)
               ON CONFLICT(user_id, tanggal) DO UPDATE SET status=excluded.status, keterangan=excluded.keterangan''',
            (user_id, tanggal, status, keterangan)
        )
        conn.commit()
        return True, "Data berhasil diperbarui"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()


if __name__ == "__main__":
    init_database()
    insert_default_data()
    print("Database siap!")
