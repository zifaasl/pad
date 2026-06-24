### SiAbsen – Sistem Informasi Absensi Akademik

Aplikasi desktop absensi akademik berbasis Python dengan **multi-role login** (Dosen & Mahasiswa) dan tampilan modern dark-theme.
---

### Struktur Proyek

```
absensi_app/
├── main.py                          ← Entry point
├── database.py                      ← Fungsi database SQLite
├── theme.py                         ← Konstanta warna & font
├── widgets.py                       ← Komponen UI reusable
├── absensi.db                       ← Database SQLite (auto-dibuat)
└── view/
    ├── view_login.py                ← Halaman login
    ├── view_mahasiswa_dashboard.py  ← Dashboard mahasiswa
    └── view_dosen_dashboard.py      ← Dashboard dosen
```

### Akun Default

| Role       | Username     | Password |
|------------|-------------|----------|
| Dosen      | dosen1      | 123456   |
| Dosen      | dosen2      | 123456   |
| Mahasiswa  | mahasiswa1  | 123456   |
| Mahasiswa  | mahasiswa2  | 123456   |
| Mahasiswa  | mahasiswa3  | 123456   |
| Mahasiswa  | mahasiswa4  | 123456   |
---

### Fitur

## Mahasiswa
- Login aman dengan hash password (SHA-256)
- **Beranda** – ringkasan statistik kehadiran & bar persentase
- **Absen Hari Ini** – absen masuk & pulang dengan jam real-time
- **Riwayat Absensi** – tabel 30 hari terakhir
- **Profil** – informasi akun

## Dosen
- **Beranda** – ringkasan total kehadiran kelas
- **Rekap Absensi** – seluruh data absensi mahasiswa
- **Data Mahasiswa** – tabel daftar mahasiswa
- **Input Manual** – ubah/tambah absensi mahasiswa
- **Profil** – informasi akun dosen
---

### Skema Database

## Tabel `users`
| Kolom       | Tipe    | Keterangan               |
|-------------|---------|--------------------------|
| id          | INTEGER | Primary key autoincrement |
| username    | TEXT    | Unique login name        |
| password    | TEXT    | SHA-256 hash             |
| role        | TEXT    | 'dosen' atau 'mahasiswa' |
| nama        | TEXT    | Nama lengkap             |
| nim_nip     | TEXT    | NIM/NIP                  |
| prodi       | TEXT    | Program studi            |
| created_at  | TIMESTAMP | Waktu dibuat            |

## Tabel `absensi`
| Kolom       | Tipe    | Keterangan               |
|-------------|---------|--------------------------|
| id          | INTEGER | Primary key              |
| user_id     | INTEGER | FK → users.id            |
| tanggal     | DATE    | Tanggal absensi          |
| jam_masuk   | TEXT    | Jam masuk (HH:MM)        |
| jam_pulang  | TEXT    | Jam pulang (HH:MM)       |
| status      | TEXT    | hadir/izin/sakit/alpha   |
| keterangan  | TEXT    | Catatan tambahan         |

## Tabel `mata_kuliah`
| Kolom    | Tipe    | Keterangan     |
|----------|---------|----------------|
| id       | INTEGER | Primary key    |
| kode     | TEXT    | Kode MK        |
| nama     | TEXT    | Nama MK        |
| sks      | INTEGER | Jumlah SKS     |
| dosen_id | INTEGER | FK → users.id  |

---

## Keamanan
- Password di-hash menggunakan **SHA-256** sebelum disimpan
- Tidak ada password plaintext di database
- Role check dilakukan di layer controller

---

## Tech Stack
- **Python 3.8+**
- **Tkinter** – GUI bawaan Python
- **SQLite3** – Database lokal bawaan Python
- **hashlib** – Hashing password
