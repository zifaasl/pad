"""
view_mahasiswa_dashboard.py – Dashboard mahasiswa
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import theme as T
import widgets as W
import database as DB
from datetime import datetime, date


class MahasiswaDashboard:
    def __init__(self, root, user, on_logout):
        self.root = root
        self.user = user
        self.on_logout = on_logout
        self.active_tab = None
        self._build()

    def _build(self):
        self.root.title(f"SiAbsen – {self.user['nama']}")
        self.root.configure(bg=T.PAGE_BG)
        self.root.geometry("1100x680")
        self.root.resizable(True, True)
        self._center(1100, 680)

        # ── Sidebar ──────────────────────────────────────────────
        self.sidebar = tk.Frame(self.root, bg=T.NAVY_MID, width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # ── Content area ─────────────────────────────────────────
        self.content = tk.Frame(self.root, bg=T.PAGE_BG)
        self.content.pack(side="left", fill="both", expand=True)

        self._build_sidebar()
        self._show_tab("beranda")

    def _build_sidebar(self):
        # Logo
        logo_frame = tk.Frame(self.sidebar, bg=T.INDIGO, pady=20)
        logo_frame.pack(fill="x")
        tk.Label(logo_frame, text="🎓 SiAbsen", font=(T.FONT_FAMILY, 16, "bold"),
                 bg=T.INDIGO, fg=T.WHITE).pack()
        tk.Label(logo_frame, text="Mahasiswa", font=T.FONT_SMALL,
                 bg=T.INDIGO, fg="#C7D2FE").pack()

        # Avatar
        avatar = tk.Frame(self.sidebar, bg=T.NAVY_MID, pady=20)
        avatar.pack(fill="x", padx=16, pady=(20, 10))
        tk.Label(avatar, text="👤", font=(T.FONT_FAMILY, 32),
                 bg=T.NAVY_MID, fg=T.INDIGO_LIGHT).pack()
        tk.Label(avatar, text=self.user['nama'], font=(T.FONT_FAMILY, 11, "bold"),
                 bg=T.NAVY_MID, fg=T.WHITE, wraplength=180).pack(pady=2)
        tk.Label(avatar, text=self.user.get('nim_nip', ''), font=T.FONT_SMALL,
                 bg=T.NAVY_MID, fg=T.GRAY_MID).pack()
        tk.Label(avatar, text=self.user.get('prodi', ''), font=T.FONT_SMALL,
                 bg=T.NAVY_MID, fg=T.GRAY_MID, wraplength=180).pack()

        W.make_separator(self.sidebar).pack(fill="x", padx=16, pady=8)

        # Menu items
        self.menu_btns = {}
        menus = [
            ("beranda",  "🏠  Beranda"),
            ("absen",    "📋  Absen Hari Ini"),
            ("riwayat",  "📅  Riwayat Absensi"),
            ("profil",   "👤  Profil Saya"),
        ]
        for key, label in menus:
            btn = tk.Button(
                self.sidebar, text=label, anchor="w",
                font=T.FONT_LABEL, relief="flat", bd=0,
                bg=T.NAVY_MID, fg=T.GRAY_LIGHT,
                activebackground=T.INDIGO, activeforeground=T.WHITE,
                cursor="hand2", padx=20, pady=10,
                command=lambda k=key: self._show_tab(k)
            )
            btn.pack(fill="x")
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=T.NAVY_LIGHT))
            btn.bind("<Leave>", lambda e, b=btn: self._restore_btn(b))
            self.menu_btns[key] = btn

        # Logout
        tk.Frame(self.sidebar, bg=T.NAVY_MID).pack(fill="both", expand=True)
        W.make_separator(self.sidebar).pack(fill="x", padx=16, pady=8)
        W.make_button(self.sidebar, "🚪  Keluar", self._logout,
                      bg=T.RED, hover_bg="#B91C1C",
                      font=T.FONT_LABEL).pack(fill="x", padx=16, pady=10, ipady=6)

    def _restore_btn(self, btn):
        key = [k for k, v in self.menu_btns.items() if v == btn]
        if key and self.active_tab == key[0]:
            btn.config(bg=T.INDIGO, fg=T.WHITE)
        else:
            btn.config(bg=T.NAVY_MID, fg=T.GRAY_LIGHT)

    def _show_tab(self, tab):
        self.active_tab = tab
        # Reset semua tombol
        for k, b in self.menu_btns.items():
            b.config(bg=T.INDIGO if k == tab else T.NAVY_MID,
                     fg=T.WHITE if k == tab else T.GRAY_LIGHT)
        # Bersihkan konten
        for w in self.content.winfo_children():
            w.destroy()

        if tab == "beranda":  self._tab_beranda()
        elif tab == "absen":  self._tab_absen()
        elif tab == "riwayat": self._tab_riwayat()
        elif tab == "profil": self._tab_profil()

    # ── Tab: Beranda ─────────────────────────────────────────────
    def _tab_beranda(self):
        self._make_header("🏠  Beranda", "Selamat datang kembali!")

        scroll = W.ScrollableFrame(self.content)
        scroll.pack(fill="both", expand=True, padx=0)
        inner = scroll.inner

        # Stat cards
        stats = DB.get_statistik_mahasiswa(self.user['id'])
        total = sum(stats.values())
        cards_data = [
            ("Total Pertemuan", total,       T.INDIGO,  "📊"),
            ("Hadir",           stats.get("hadir", 0), T.TEAL, "✅"),
            ("Izin",            stats.get("izin",  0), T.AMBER, "📋"),
            ("Sakit",           stats.get("sakit", 0), T.PURPLE, "🏥"),
            ("Alpha",           stats.get("alpha", 0), T.RED, "❌"),
        ]

        row = tk.Frame(inner, bg=T.PAGE_BG)
        row.pack(fill="x", padx=24, pady=20)
        for title, val, color, icon in cards_data:
            card = W.make_stat_card(row, title, val, color, icon)
            card.pack(side="left", padx=8, pady=4, ipadx=8, ipady=4, expand=True, fill="x")

        # Absen hari ini
        today_rec = DB.get_absensi_today(self.user['id'])
        sec = tk.Frame(inner, bg=T.CARD_BG, padx=24, pady=20)
        sec.pack(fill="x", padx=24, pady=(0, 16))
        tk.Label(sec, text="📍 Status Absensi Hari Ini",
                 font=T.FONT_SUB, bg=T.CARD_BG, fg=T.WHITE).pack(anchor="w")
        W.make_separator(sec, height=1).pack(fill="x", pady=8)

        if today_rec:
            info = tk.Frame(sec, bg=T.CARD_BG)
            info.pack(anchor="w")
            status = today_rec.get('status', '-')
            color = T.STATUS_COLOR.get(status, T.GRAY_MID)
            icon  = T.STATUS_ICON.get(status, "•")
            tk.Label(info, text=f"{icon}  {status.upper()}",
                     font=(T.FONT_FAMILY, 20, "bold"), bg=T.CARD_BG, fg=color).pack(anchor="w")
            masuk  = today_rec.get('jam_masuk', '-') or '-'
            pulang = today_rec.get('jam_pulang', '-') or '-'
            tk.Label(info, text=f"Masuk: {masuk}   |   Pulang: {pulang}",
                     font=T.FONT_LABEL, bg=T.CARD_BG, fg=T.GRAY_LIGHT).pack(anchor="w", pady=4)
        else:
            tk.Label(sec, text="Belum melakukan absensi hari ini",
                     font=T.FONT_LABEL, bg=T.CARD_BG, fg=T.GRAY_MID).pack(anchor="w", pady=6)
            W.make_button(sec, "  Absen Sekarang  →", lambda: self._show_tab("absen"),
                          font=T.FONT_LABEL).pack(anchor="w", pady=(4, 0), ipady=6)

        # Persentase kehadiran
        if total > 0:
            pct = round(stats.get('hadir', 0) / total * 100, 1)
            sec2 = tk.Frame(inner, bg=T.CARD_BG, padx=24, pady=20)
            sec2.pack(fill="x", padx=24, pady=(0, 24))
            tk.Label(sec2, text="📈 Persentase Kehadiran",
                     font=T.FONT_SUB, bg=T.CARD_BG, fg=T.WHITE).pack(anchor="w")
            W.make_separator(sec2, height=1).pack(fill="x", pady=8)

            bar_bg = tk.Frame(sec2, bg=T.NAVY_LIGHT, height=20)
            bar_bg.pack(fill="x", pady=4)
            bar_bg.update_idletasks()
            bar_w = bar_bg.winfo_width() or 600
            fill_w = max(4, int(bar_w * pct / 100))
            tk.Frame(bar_bg, bg=T.TEAL if pct >= 75 else T.AMBER, height=20, width=fill_w).place(x=0, y=0)
            color_pct = T.TEAL if pct >= 75 else T.AMBER if pct >= 50 else T.RED
            tk.Label(sec2, text=f"{pct}%  kehadiran",
                     font=(T.FONT_FAMILY, 14, "bold"), bg=T.CARD_BG, fg=color_pct).pack(anchor="w", pady=(6, 0))
            note = "✅ Kehadiran memenuhi syarat" if pct >= 75 else "⚠️ Kehadiran di bawah 75%!"
            tk.Label(sec2, text=note, font=T.FONT_SMALL,
                     bg=T.CARD_BG, fg=T.TEAL if pct >= 75 else T.AMBER).pack(anchor="w")

    # ── Tab: Absen ───────────────────────────────────────────────
    def _tab_absen(self):
        self._make_header("📋  Absen Hari Ini", datetime.now().strftime("%A, %d %B %Y"))

        frame = tk.Frame(self.content, bg=T.PAGE_BG)
        frame.pack(expand=True)

        card = W.make_card(frame, padx=48, pady=40)
        card.pack(padx=40, pady=20)

        # Status saat ini
        today = DB.get_absensi_today(self.user['id'])

        # Jam berjalan
        jam_label = tk.Label(card, text="", font=(T.FONT_FAMILY, 40, "bold"),
                              bg=T.CARD_BG, fg=T.WHITE)
        jam_label.pack()
        def update_jam():
            jam_label.config(text=datetime.now().strftime("%H:%M:%S"))
            self.root.after(1000, update_jam)
        update_jam()

        tanggal_label = tk.Label(card, text=datetime.now().strftime("%d %B %Y"),
                                  font=T.FONT_LABEL, bg=T.CARD_BG, fg=T.GRAY_MID)
        tanggal_label.pack(pady=(0, 24))

        W.make_separator(card).pack(fill="x", pady=8)

        # Status absen
        status_frame = tk.Frame(card, bg=T.CARD_BG)
        status_frame.pack(pady=16)

        self.lbl_masuk  = tk.Label(status_frame, text="Masuk: –",
                                    font=T.FONT_SUB, bg=T.CARD_BG, fg=T.GRAY_MID)
        self.lbl_masuk.grid(row=0, column=0, padx=20)
        self.lbl_pulang = tk.Label(status_frame, text="Pulang: –",
                                    font=T.FONT_SUB, bg=T.CARD_BG, fg=T.GRAY_MID)
        self.lbl_pulang.grid(row=0, column=1, padx=20)

        if today:
            masuk = today.get('jam_masuk') or '–'
            pulang = today.get('jam_pulang') or '–'
            self.lbl_masuk.config(text=f"Masuk: {masuk}", fg=T.TEAL)
            if pulang != '–':
                self.lbl_pulang.config(text=f"Pulang: {pulang}", fg=T.TEAL)

        self.lbl_result = tk.Label(card, text="", font=T.FONT_LABEL,
                                    bg=T.CARD_BG, fg=T.TEAL)
        self.lbl_result.pack(pady=4)

        W.make_separator(card).pack(fill="x", pady=8)

        # Tombol
        btn_row = tk.Frame(card, bg=T.CARD_BG)
        btn_row.pack(pady=16)

        masuk_done = bool(today and today.get('jam_masuk'))
        W.make_button(btn_row, "  ✅  Absen Masuk  ",
                      self._do_masuk, bg=T.TEAL, hover_bg="#0F9488",
                      font=(T.FONT_FAMILY, 13, "bold"),
                      state="disabled" if masuk_done else "normal").pack(side="left", padx=8, ipady=10)

        pulang_done = bool(today and today.get('jam_pulang'))
        W.make_button(btn_row, "  🏠  Absen Pulang  ",
                      self._do_pulang, bg=T.INDIGO, hover_bg=T.INDIGO_DARK,
                      font=(T.FONT_FAMILY, 13, "bold"),
                      state="disabled" if pulang_done else "normal").pack(side="left", padx=8, ipady=10)

    def _do_masuk(self):
        ok, msg = DB.absen_masuk(self.user['id'])
        if ok:
            self.lbl_result.config(text=f"✅ {msg}", fg=T.TEAL)
            self.lbl_masuk.config(text=f"Masuk: {datetime.now().strftime('%H:%M')}", fg=T.TEAL)
            W.ToastNotification(self.root, msg)
        else:
            self.lbl_result.config(text=f"❌ {msg}", fg=T.RED)

    def _do_pulang(self):
        ok, msg = DB.absen_pulang(self.user['id'])
        if ok:
            self.lbl_result.config(text=f"✅ {msg}", fg=T.TEAL)
            self.lbl_pulang.config(text=f"Pulang: {datetime.now().strftime('%H:%M')}", fg=T.TEAL)
            W.ToastNotification(self.root, msg)
        else:
            self.lbl_result.config(text=f"❌ {msg}", fg=T.RED)

    # ── Tab: Riwayat ─────────────────────────────────────────────
    def _tab_riwayat(self):
        self._make_header("📅  Riwayat Absensi", "30 Hari Terakhir")

        frame = tk.Frame(self.content, bg=T.PAGE_BG)
        frame.pack(fill="both", expand=True, padx=24, pady=16)

        # Tabel
        cols = ("Tanggal", "Jam Masuk", "Jam Pulang", "Status", "Keterangan")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Dark.Treeview",
                        background=T.CARD_BG, foreground=T.WHITE,
                        fieldbackground=T.CARD_BG, rowheight=32,
                        borderwidth=0, font=T.FONT_LABEL)
        style.configure("Dark.Treeview.Heading",
                        background=T.NAVY_LIGHT, foreground=T.GRAY_LIGHT,
                        font=(T.FONT_FAMILY, 11, "bold"), relief="flat")
        style.map("Dark.Treeview", background=[("selected", T.INDIGO)])

        tree = ttk.Treeview(frame, columns=cols, show="headings",
                             style="Dark.Treeview", height=16)
        widths = [150, 110, 110, 100, 200]
        for col, w in zip(cols, widths):
            tree.heading(col, text=col)
            tree.column(col, width=w, anchor="center")

        rows = DB.get_absensi_mahasiswa(self.user['id'], 30)
        for r in rows:
            status = r.get('status', '-')
            icon = T.STATUS_ICON.get(status, '•')
            tree.insert("", "end", values=(
                r.get('tanggal', '-'),
                r.get('jam_masuk', '-') or '-',
                r.get('jam_pulang', '-') or '-',
                f"{icon} {status}",
                r.get('keterangan', '-') or '-',
            ))

        sb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

    # ── Tab: Profil ──────────────────────────────────────────────
    def _tab_profil(self):
        self._make_header("👤  Profil Saya", "Informasi akun Anda")

        frame = tk.Frame(self.content, bg=T.PAGE_BG)
        frame.pack(expand=True)

        card = W.make_card(frame, padx=48, pady=36)
        card.pack(padx=40, pady=20)

        tk.Label(card, text="👤", font=(T.FONT_FAMILY, 52),
                 bg=T.CARD_BG, fg=T.INDIGO).pack()

        fields = [
            ("Nama Lengkap",  self.user.get('nama', '-')),
            ("Username",      self.user.get('username', '-')),
            ("NIM",           self.user.get('nim_nip', '-')),
            ("Program Studi", self.user.get('prodi', '-')),
            ("Role",          self.user.get('role', '-').capitalize()),
            ("Bergabung",     self.user.get('created_at', '-')[:10] if self.user.get('created_at') else '-'),
        ]
        for label, value in fields:
            row = tk.Frame(card, bg=T.CARD_BG)
            row.pack(fill="x", pady=6)
            tk.Label(row, text=f"{label}:", font=T.FONT_LABEL,
                     bg=T.CARD_BG, fg=T.GRAY_MID, width=18, anchor="w").pack(side="left")
            tk.Label(row, text=value, font=(T.FONT_FAMILY, 12, "bold"),
                     bg=T.CARD_BG, fg=T.WHITE).pack(side="left")

    # ── Helpers ──────────────────────────────────────────────────
    def _make_header(self, title, subtitle=""):
        hdr = tk.Frame(self.content, bg=T.NAVY_MID, padx=28, pady=16)
        hdr.pack(fill="x")
        tk.Label(hdr, text=title, font=T.FONT_HEADING,
                 bg=T.NAVY_MID, fg=T.WHITE).pack(anchor="w")
        if subtitle:
            tk.Label(hdr, text=subtitle, font=T.FONT_SMALL,
                     bg=T.NAVY_MID, fg=T.GRAY_MID).pack(anchor="w")

    def _logout(self):
        if messagebox.askyesno("Konfirmasi", "Yakin ingin keluar?"):
            self.on_logout()

    def _center(self, w, h):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
