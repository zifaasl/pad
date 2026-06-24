"""
view_login.py – Halaman login dengan tampilan modern dark
"""
import tkinter as tk
from tkinter import messagebox
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import theme as T
import widgets as W
import database as DB
from datetime import datetime


class LoginView:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        self._build()

    def _build(self):
        self.root.title("SiAbsen – Sistem Informasi Absensi")
        self.root.configure(bg=T.PAGE_BG)
        self.root.geometry("920x600")
        self.root.resizable(False, False)
        self._center_window(920, 600)

        # ── Layout: kiri (branding) + kanan (form) ──────────────────
        left = tk.Frame(self.root, bg=T.NAVY_MID, width=420)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        right = tk.Frame(self.root, bg=T.PAGE_BG)
        right.pack(side="right", fill="both", expand=True)

        self._build_left(left)
        self._build_right(right)

    def _build_left(self, parent):
        """Panel branding kiri."""
        inner = tk.Frame(parent, bg=T.NAVY_MID)
        inner.place(relx=0.5, rely=0.5, anchor="center")

        # Logo / Ikon
        tk.Label(inner, text="🎓", font=(T.FONT_FAMILY, 60),
                 bg=T.NAVY_MID, fg=T.INDIGO).pack(pady=(0, 20))

        tk.Label(inner, text="SiAbsen",
                 font=(T.FONT_FAMILY, 32, "bold"),
                 bg=T.NAVY_MID, fg=T.WHITE).pack()

        tk.Label(inner, text="Sistem Informasi Absensi\nAkademik Digital",
                 font=T.FONT_LABEL, bg=T.NAVY_MID, fg=T.GRAY_MID,
                 justify="center").pack(pady=(8, 40))

        # Feature badges
        features = [
            ("📊", "Rekap Otomatis"),
            ("🔐", "Multi Role Login"),
            ("📅", "Absensi Real-time"),
        ]
        for icon, label in features:
            row = tk.Frame(inner, bg=T.NAVY_MID)
            row.pack(anchor="w", pady=4)
            tk.Label(row, text=icon, bg=T.NAVY_MID, font=(T.FONT_FAMILY, 14)).pack(side="left", padx=(0, 10))
            tk.Label(row, text=label, bg=T.NAVY_MID, fg=T.GRAY_LIGHT,
                     font=T.FONT_LABEL).pack(side="left")

        # Garis waktu
        time_label = tk.Label(inner, text="", font=T.FONT_SMALL,
                               bg=T.NAVY_MID, fg=T.GRAY_MID)
        time_label.pack(pady=(30, 0))
        self._update_clock(time_label)

    def _build_right(self, parent):
        """Panel form kanan."""
        inner = tk.Frame(parent, bg=T.PAGE_BG)
        inner.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(inner, text="Selamat Datang 👋",
                 font=T.FONT_TITLE, bg=T.PAGE_BG, fg=T.WHITE).pack(pady=(0, 6))
        tk.Label(inner, text="Masuk ke akun Anda untuk melanjutkan",
                 font=T.FONT_LABEL, bg=T.PAGE_BG, fg=T.GRAY_MID).pack(pady=(0, 30))

        # Form card
        card = tk.Frame(inner, bg=T.CARD_BG, padx=36, pady=32)
        card.pack()

        # Username
        tk.Label(card, text="USERNAME", font=(T.FONT_FAMILY, 9, "bold"),
                 bg=T.CARD_BG, fg=T.GRAY_MID).pack(anchor="w")
        self.entry_user = W.make_entry(card, width=34)
        self.entry_user.pack(pady=(4, 16), ipady=10, padx=2)

        # Password
        tk.Label(card, text="PASSWORD", font=(T.FONT_FAMILY, 9, "bold"),
                 bg=T.CARD_BG, fg=T.GRAY_MID).pack(anchor="w")
        self.entry_pass = W.make_entry(card, show="●", width=34)
        self.entry_pass.pack(pady=(4, 8), ipady=10, padx=2)

        # Show password toggle
        self.show_pass = tk.BooleanVar(value=False)
        def toggle_show():
            self.entry_pass.config(show="" if self.show_pass.get() else "●")
        chk = tk.Checkbutton(card, text="Tampilkan Password",
                              variable=self.show_pass, command=toggle_show,
                              bg=T.CARD_BG, fg=T.GRAY_MID, selectcolor=T.NAVY_LIGHT,
                              activebackground=T.CARD_BG, font=T.FONT_SMALL,
                              cursor="hand2")
        chk.pack(anchor="w", pady=(0, 20))

        # Login button
        btn = W.make_button(card, "  Masuk  →", self._login,
                            bg=T.INDIGO, width=32,
                            font=(T.FONT_FAMILY, 12, "bold"))
        btn.pack(ipady=8)

        # Status label
        self.lbl_status = tk.Label(card, text="", font=T.FONT_SMALL,
                                   bg=T.CARD_BG, fg=T.RED)
        self.lbl_status.pack(pady=(10, 0))

        # Hint akun demo
        hint = tk.Frame(inner, bg=T.PAGE_BG)
        hint.pack(pady=(20, 0))
        tk.Label(hint, text="Akun Demo →  dosen1 / 123456  |  mahasiswa1 / 123456",
                 font=T.FONT_SMALL, bg=T.PAGE_BG, fg=T.GRAY_MID).pack()

        # Enter key binding
        self.root.bind("<Return>", lambda e: self._login())
        self.entry_user.focus()

    def _login(self):
        username = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()

        if not username or not password:
            self.lbl_status.config(text="❌  Harap isi semua kolom", fg=T.RED)
            return

        self.lbl_status.config(text="⏳  Memverifikasi...", fg=T.AMBER)
        self.root.update()

        user = DB.authenticate(username, password)
        if user:
            self.lbl_status.config(text="✅  Login berhasil!", fg=T.TEAL)
            self.root.after(400, lambda: self.on_success(user))
        else:
            self.lbl_status.config(text="❌  Username atau password salah", fg=T.RED)
            self.entry_pass.delete(0, tk.END)
            self.entry_pass.focus()

    def _update_clock(self, label):
        now = datetime.now().strftime("%A, %d %B %Y  –  %H:%M:%S")
        label.config(text=now)
        self.root.after(1000, lambda: self._update_clock(label))

    def _center_window(self, w, h):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")
