import tkinter as tk

from database import init_database, insert_default_data
from views.view_dosen_dashboard import DosenDashboard
from views.view_login import LoginView
from views.view_mahasiswa_dashboard import MahasiswaDashboard


class AbsensiApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.current_view = None
        self.show_login()

    def show_login(self) -> None:
        self._clear_view()
        self.current_view = LoginView(self.root, on_login_success=self.handle_login_success)

    def handle_login_success(self, user: dict) -> None:
        self._clear_view()
        if user.get("role") == "dosen":
            self.current_view = DosenDashboard(self.root, user, on_logout=self.show_login)
        else:
            self.current_view = MahasiswaDashboard(self.root, user, on_logout=self.show_login)

    def _clear_view(self) -> None:
        for widget in self.root.winfo_children():
            widget.destroy()


def main() -> int:
    init_database()
    insert_default_data()

    root = tk.Tk()
    root.title("Sistem Absensi")
    root.geometry("450x380")
    AbsensiApp(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
