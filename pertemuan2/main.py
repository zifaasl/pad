"""
main.py – Entry point Aplikasi SiAbsen
"""
import tkinter as tk
import sys
import os

# Tambah path agar import relatif berjalan
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

from database import init_database, insert_default_data
from view.view_login import LoginView
from view.view_mahasiswa_dashboard import MahasiswaDashboard
from view.view_dosen_dashboard import DosenDashboard


class AbsensiApp:
    """Main Application Controller"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(True, True)

        # Inisialisasi database
        init_database()
        insert_default_data()

        # Mulai dari login
        self.show_login()

    def show_login(self):
        self._clear()
        LoginView(self.root, self.on_login_success)

    def on_login_success(self, user):
        self._clear()
        if user['role'] == 'mahasiswa':
            MahasiswaDashboard(self.root, user, self.show_login)
        elif user['role'] == 'dosen':
            DosenDashboard(self.root, user, self.show_login)

    def _clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AbsensiApp()
    app.run()
