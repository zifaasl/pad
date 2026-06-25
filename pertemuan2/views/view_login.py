import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from controller.controller_auth import AuthController


class LoginView:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.auth = AuthController()

        self.root.title("Login - Sistem Absensi")
        self.root.geometry("430x430")
        self.root.resizable(False, False)

        main_frame = ttk.Frame(self.root, padding=28)
        main_frame.pack(fill=BOTH, expand=True)

        card = ttk.Frame(main_frame, padding=24, bootstyle="light")
        card.pack(fill=BOTH, expand=True)

        ttk.Label(card, text="SISTEM ABSENSI", font=("Segoe UI", 18, "bold"),
                  bootstyle=PRIMARY).pack(pady=(0, 6))
        ttk.Label(card, text="Masuk untuk mengelola absensi",
                  font=("Segoe UI", 10), bootstyle=SECONDARY).pack(pady=(0, 14))
        ttk.Separator(card, bootstyle=SECONDARY).pack(fill=X, pady=(0, 14))

        ttk.Label(card, text="Username", font=("Segoe UI", 10)).pack(anchor=W)
        self.entry_username = ttk.Entry(card, font=("Segoe UI", 11))
        self.entry_username.pack(fill=X, pady=(4, 10))
        self.entry_username.focus()

        ttk.Label(card, text="Password", font=("Segoe UI", 10)).pack(anchor=W)
        self.entry_password = ttk.Entry(card, show="*", font=("Segoe UI", 11))
        self.entry_password.pack(fill=X, pady=(4, 6))

        self.label_error = ttk.Label(card, text="", font=("Segoe UI", 9),
                                     bootstyle=DANGER)
        self.label_error.pack(fill=X, pady=(8, 0))

        self.btn_login = ttk.Button(card, text="Masuk", bootstyle=SUCCESS,
                                    width=20, command=self._handle_login)
        self.btn_login.pack(pady=(12, 0))

        ttk.Label(card, text="Gunakan akun dosen atau mahasiswa",
                  font=("Segoe UI", 9), bootstyle=SECONDARY).pack(pady=(12, 0))

        self.root.bind("<Return>", lambda e: self._handle_login())

    def _handle_login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get()
        result = self.auth.login(username, password)
        if result['success']:
            self.on_login_success(result['user'])
        else:
            self.label_error.config(text=result['message'])
