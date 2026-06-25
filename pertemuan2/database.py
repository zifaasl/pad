import sqlite3
import os
import logging
from contextlib import contextmanager
from typing import Generator

logger = logging.getLogger(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), 'absensi.db')


@contextmanager
def get_connection() -> Generator[sqlite3.Connection, None, None]:
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        yield conn
        conn.commit()
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        logger.error("Database error: %s", e)
        raise
    finally:
        if conn:
            conn.close()


def init_database():
    ddl = [
        """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            nama TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""",
        """CREATE TABLE IF NOT EXISTS absensi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            tanggal DATE NOT NULL,
            jam_masuk TIME,
            jam_pulang TIME,
            status TEXT DEFAULT 'hadir',
            keterangan TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(user_id, tanggal)
        )""",
    ]
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            for stmt in ddl:
                cursor.execute(stmt)
        logger.info("Database initialized successfully")
    except sqlite3.Error as e:
        logger.critical("Failed to initialize database: %s", e)
        raise


def insert_default_data():
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            if cursor.fetchone()[0] == 0:
                data = [
                    ('dosen1', '123456', 'dosen', 'Dr. Saeful'),
                    ('mahasiswa1', '123456', 'mahasiswa', 'Andi Pratama'),
                    ('mahasiswa2', '123456', 'mahasiswa', 'Siti Nurhaliza'),
                ]
                cursor.executemany(
                    "INSERT INTO users (username, password, role, nama) VALUES (?, ?, ?, ?)",
                    data
                )
                logger.info("Default data inserted: %d users", len(data))
    except sqlite3.Error as e:
        logger.error("Failed to insert default data: %s", e)
        raise
