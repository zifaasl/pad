"""
view_dosen_dashboard.py – Dashboard Dosen
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import theme as T
import widgets as W
import database as DB
from datetime import datetime, date


class DosenDashboard:
    def __init__(self, root, user, on_logout):
        self.root = root
        self.user = user
        self.on_logout = on_logout
        self.active_tab = None
        self._build()

    def _build(self):
        self.root.title(f"SiAbsen – {self.user['nama']}")
        self.root.configure(bg=T.PAGE_BG)
        self.root.geometry("1200x720")
        self.root.resizable(True, True)
        self._center(1200, 720)

        # Sidebar
        self.sidebar = tk.Frame(self.root, bg=T.NAVY_MID, width=230)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Content
        self.content = tk.Frame(self.root, bg=T.PAGE_BG)
        self.content.pack(side="left", fill="both", expand=True)

        self._build_sidebar()
        self._show_tab("beranda")

    def _build_sidebar(self):
        # Logo
        logo_frame = tk.Frame(self.sidebar, bg="#4F46E5", pady=20)
        logo_frame.pack(fill="x")
        tk.Label(logo_frame, text="🎓 SiAbsen", font=(T.FONT_FAMILY, 16, "bold"),
                 bg="#4F46E5", fg=T.WHITE).pack()
        tk.Label(logo_frame, text="Dosen / Admin", font=T.FONT_SMALL,
                 bg="#4F46E5", fg="#C7D2FE").pack()

        # Avatar
        avatar = tk.Frame(self.sidebar, bg=T.NAVY_MID, pady=16)
        avatar.pack(fill="x", padx=16, pady=(20, 10))
        tk.Label(avatar, text="👨‍🏫", font=(T.FONT_FAMILY, 32),
                 bg=T.NAVY_MID, fg=T.INDIGO_LIGHT).pack()
        tk.Label(avatar, text=self.user['nama'], font=(T.FONT_FAMILY, 10, "bold"),
                 bg=T.NAVY_MID, fg=T.WHITE, wraplength=190).pack(pady=2)
        nip = self.user.get('nim_nip', '')
        if nip:
            tk.Label(avatar, text=nip, font=T.FONT_SMALL,
                     bg=T.NAVY_MID, fg=T.GRAY_MID).pack()
        W.make_badge(avatar, "  Dosen  ", T.INDIGO).pack(pady=4)

        W.make_separator(self.sidebar).pack(fill="x", padx=16, pady=8)

        self.menu_btns = {}
        menus = [
            ("beranda",  "🏠  Beranda"),
            ("rekap",    "📋  Rekap Absensi"),
            ("mahasiswa","👥  Data Mahasiswa"),
            ("input",    "✏️   Input Manual"),
            ("profil",   "👤  Profil"),
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

        tk.Frame(self.sidebar, bg=T.NAVY_MID).pack(fill="both", expand=True)
        W.make_separator(self.sidebar).pack(fill="x", padx=16, pady=4)

        # Waktu
        self.clock = tk.Label(self.sidebar, text="", font=T.FONT_SMALL,
                               bg=T.NAVY_MID, fg=T.GRAY_MID)
        self.clock.pack(pady=4)
        self._tick()

        W.make_button(self.sidebar, "🚪  Keluar", self._logout,
                      bg=T.RED, hover_bg="#B91C1C", font=T.FONT_LABEL).pack(
            fill="x", padx=16, pady=(4, 14), ipady=6)

    def _tick(self):
        self.clock.config(text=datetime.now().strftime("%H:%M  •  %d %b %Y"))
        self.root.after(1000, self._tick)

    def _restore_btn(self, btn):
        key = [k for k, v in self.menu_btns.items() if v == btn]
        if key and self.active_tab == key[0]:
            btn.config(bg=T.INDIGO, fg=T.WHITE)
        else:
            btn.config(bg=T.NAVY_MID, fg=T.GRAY_LIGHT)

    def _show_tab(self, tab):
        self.active_tab = tab
        for k, b in self.menu_btns.items():
            b.config(bg=T.INDIGO if k == tab else T.NAVY_MID,
                     fg=T.WHITE if k == tab else T.GRAY_LIGHT)
        for w in self.content.winfo_children():
            w.destroy()

        if tab == "beranda":    self._tab_beranda()
        elif tab == "rekap":    self._tab_rekap()
        elif tab == "mahasiswa": self._tab_mahasiswa()
        elif tab == "input":    self._tab_input()
        elif tab == "profil":   self._tab_profil()

    # ── Tab Beranda ──────────────────────────────────────────────
    def _tab_beranda(self):
        self._make_header("🏠  Beranda Dosen",
                          f"Halo, {self.user['nama']}! Berikut ringkasan hari ini.")

        scroll = W.ScrollableFrame(self.content)
        scroll.pack(fill="both", expand=True)
        inner = scroll.inner

        # Statistik kelas
        stats_all = DB.get_statistik_kelas()
        total_mhs = len(stats_all)
        total_hadir = sum(r.get('hadir', 0) or 0 for r in stats_all)
        total_alpha = sum(r.get('alpha', 0) or 0 for r in stats_all)
        total_izin  = sum(r.get('izin',  0) or 0 for r in stats_all)
        total_sakit = sum(r.get('sakit', 0) or 0 for r in stats_all)

        row = tk.Frame(inner, bg=T.PAGE_BG)
        row.pack(fill="x", padx=24, pady=20)
        for title, val, color, icon in [
            ("Total Mahasiswa", total_mhs,    T.INDIGO,  "👥"),
            ("Total Hadir",     total_hadir,  T.TEAL,    "✅"),
            ("Total Izin",      total_izin,   T.AMBER,   "📋"),
            ("Total Sakit",     total_sakit,  T.PURPLE,  "🏥"),
            ("Total Alpha",     total_alpha,  T.RED,     "❌"),
        ]:
            card = W.make_stat_card(row, title, val, color, icon)
            card.pack(side="left", padx=8, expand=True, fill="x")

        # Ringkasan per mahasiswa
        sec = tk.Frame(inner, bg=T.CARD_BG, padx=24, pady=20)
        sec.pack(fill="x", padx=24, pady=(0, 24))
        tk.Label(sec, text="📊 Rekap Kehadiran per Mahasiswa",
                 font=T.FONT_SUB, bg=T.CARD_BG, fg=T.WHITE).pack(anchor="w")
        W.make_separator(sec, height=1).pack(fill="x", pady=8)

        cols = ("Nama", "NIM", "Prodi", "Hadir", "Izin", "Sakit", "Alpha", "% Hadir")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("DarkD.Treeview",
                        background=T.CARD_BG, foreground=T.WHITE,
                        fieldbackground=T.CARD_BG, rowheight=30,
                        borderwidth=0, font=T.FONT_LABEL)
        style.configure("DarkD.Treeview.Heading",
                        background=T.NAVY_LIGHT, foreground=T.GRAY_LIGHT,
                        font=(T.FONT_FAMILY, 10, "bold"), relief="flat")
        style.map("DarkD.Treeview", background=[("selected", T.INDIGO)])

        tree = ttk.Treeview(sec, columns=cols, show="headings",
                             style="DarkD.Treeview", height=8)
        w = [160, 110, 140, 60, 60, 60, 60, 80]
        for col, cw in zip(cols, w):
            tree.heading(col, text=col)
            tree.column(col, width=cw, anchor="center")

        for r in stats_all:
            tot = r.get('total', 0) or 0
            hadir = r.get('hadir', 0) or 0
            pct = f"{round(hadir/tot*100)}%" if tot > 0 else "–"
            tree.insert("", "end", values=(
                r.get('nama','-'),
                r.get('nim_nip','-'),
                r.get('prodi','-'),
                hadir,
                r.get('izin',0) or 0,
                r.get('sakit',0) or 0,
                r.get('alpha',0) or 0,
                pct,
            ))
        tree.pack(fill="both", expand=True)

    # ── Tab Rekap ────────────────────────────────────────────────
    def _tab_rekap(self):
        self._make_header("📋  Rekap Absensi", "Data 50 pertemuan terakhir")

        frame = tk.Frame(self.content, bg=T.PAGE_BG, padx=24, pady=16)
        frame.pack(fill="both", expand=True)

        cols = ("Tanggal", "Nama", "NIM", "Prodi", "Masuk", "Pulang", "Status")
        tree = ttk.Treeview(frame, columns=cols, show="headings",
                             style="DarkD.Treeview", height=18)
        ws = [110, 180, 110, 140, 80, 80, 100]
        for col, cw in zip(cols, ws):
            tree.heading(col, text=col)
            tree.column(col, width=cw, anchor="center")

        rows = DB.get_rekap_absensi_semua(50)
        for r in rows:
            status = r.get('status','-')
            icon = T.STATUS_ICON.get(status,'•')
            tree.insert("", "end", values=(
                r.get('tanggal','-'),
                r.get('nama','-'),
                r.get('nim_nip','-'),
                r.get('prodi','-'),
                r.get('jam_masuk','-') or '-',
                r.get('jam_pulang','-') or '-',
                f"{icon} {status}",
            ))

        sb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

    # ── Tab Mahasiswa ─────────────────────────────────────────────
    def _tab_mahasiswa(self):
        self._make_header("👥  Data Mahasiswa", "Daftar mahasiswa terdaftar")

        frame = tk.Frame(self.content, bg=T.PAGE_BG, padx=24, pady=16)
        frame.pack(fill="both", expand=True)

        mhs_list = DB.get_all_mahasiswa()
        cols = ("No", "Nama", "Username", "NIM", "Program Studi", "Bergabung")
        tree = ttk.Treeview(frame, columns=cols, show="headings",
                             style="DarkD.Treeview", height=16)
        for col, w in zip(cols, [40, 200, 120, 120, 160, 120]):
            tree.heading(col, text=col)
            tree.column(col, width=w, anchor="center")

        for i, m in enumerate(mhs_list, 1):
            joined = (m.get('created_at') or '')[:10]
            tree.insert("", "end", values=(
                i, m.get('nama','-'), m.get('username','-'),
                m.get('nim_nip','-'), m.get('prodi','-'), joined,
            ))

        sb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

    # ── Tab Input Manual ──────────────────────────────────────────
    def _tab_input(self):
        self._make_header("✏️   Input Absensi Manual", "Ubah data absensi mahasiswa")

        scroll = W.ScrollableFrame(self.content)
        scroll.pack(fill="both", expand=True)
        inner = scroll.inner

        card = W.make_card(inner, padx=36, pady=28)
        card.pack(fill="x", padx=24, pady=20)

        tk.Label(card, text="Form Input Absensi", font=T.FONT_SUB,
                 bg=T.CARD_BG, fg=T.WHITE).pack(anchor="w", pady=(0, 12))
        W.make_separator(card, height=1).pack(fill="x", pady=(0, 16))

        form = tk.Frame(card, bg=T.CARD_BG)
        form.pack(fill="x")

        # Mahasiswa dropdown
        mhs_list = DB.get_all_mahasiswa()
        mhs_names = [f"{m['nama']} ({m.get('nim_nip','')})" for m in mhs_list]
        mhs_ids = [m['id'] for m in mhs_list]

        tk.Label(form, text="Mahasiswa:", font=T.FONT_LABEL,
                 bg=T.CARD_BG, fg=T.GRAY_MID).grid(row=0, col=0, sticky="w", pady=8, padx=(0,12))
        self.var_mhs = tk.StringVar(value=mhs_names[0] if mhs_names else "")
        cb_mhs = ttk.Combobox(form, textvariable=self.var_mhs,
                               values=mhs_names, state="readonly", width=36,
                               font=T.FONT_LABEL)
        cb_mhs.grid(row=0, column=1, pady=8, sticky="w")

        # Tanggal
        tk.Label(form, text="Tanggal:", font=T.FONT_LABEL,
                 bg=T.CARD_BG, fg=T.GRAY_MID).grid(row=1, column=0, sticky="w", pady=8, padx=(0,12))
        self.entry_tgl = W.make_entry(form, width=20)
        self.entry_tgl.insert(0, date.today().strftime("%Y-%m-%d"))
        self.entry_tgl.grid(row=1, column=1, pady=8, ipady=6, sticky="w")
        tk.Label(form, text="(YYYY-MM-DD)", font=T.FONT_SMALL,
                 bg=T.CARD_BG, fg=T.GRAY_MID).grid(row=1, column=2, padx=8, sticky="w")

        # Status
        tk.Label(form, text="Status:", font=T.FONT_LABEL,
                 bg=T.CARD_BG, fg=T.GRAY_MID).grid(row=2, column=0, sticky="w", pady=8, padx=(0,12))
        self.var_status = tk.StringVar(value="hadir")
        status_opts = ["hadir", "izin", "sakit", "alpha"]
        cb_status = ttk.Combobox(form, textvariable=self.var_status,
                                  values=status_opts, state="readonly", width=20,
                                  font=T.FONT_LABEL)
        cb_status.grid(row=2, column=1, pady=8, sticky="w")

        # Keterangan
        tk.Label(form, text="Keterangan:", font=T.FONT_LABEL,
                 bg=T.CARD_BG, fg=T.GRAY_MID).grid(row=3, column=0, sticky="w", pady=8, padx=(0,12))
        self.entry_ket = W.make_entry(form, width=36)
        self.entry_ket.grid(row=3, column=1, pady=8, ipady=6, sticky="w")

        # Tombol
        self.lbl_input_result = tk.Label(card, text="", font=T.FONT_LABEL,
                                          bg=T.CARD_BG, fg=T.TEAL)

        def do_save():
            idx = mhs_names.index(self.var_mhs.get()) if self.var_mhs.get() in mhs_names else -1
            if idx < 0:
                self.lbl_input_result.config(text="❌ Pilih mahasiswa!", fg=T.RED)
                return
            uid = mhs_ids[idx]
            tgl = self.entry_tgl.get().strip()
            status = self.var_status.get()
            ket = self.entry_ket.get().strip()
            ok, msg = DB.update_absensi_mahasiswa(uid, tgl, status, ket)
            self.lbl_input_result.config(
                text=f"{'✅' if ok else '❌'} {msg}",
                fg=T.TEAL if ok else T.RED
            )
            if ok:
                W.ToastNotification(self.root, msg)

        W.make_button(card, "  💾  Simpan Absensi  ", do_save,
                      font=(T.FONT_FAMILY, 12, "bold")).pack(anchor="w", pady=16, ipady=8)
        self.lbl_input_result.pack(anchor="w")

    # ── Tab Profil ───────────────────────────────────────────────
    def _tab_profil(self):
        self._make_header("👤  Profil Dosen", "Informasi akun Anda")

        frame = tk.Frame(self.content, bg=T.PAGE_BG)
        frame.pack(expand=True)

        card = W.make_card(frame, padx=48, pady=36)
        card.pack(padx=40, pady=20)

        tk.Label(card, text="👨‍🏫", font=(T.FONT_FAMILY, 52),
                 bg=T.CARD_BG, fg=T.INDIGO).pack()

        for label, key in [
            ("Nama Lengkap", "nama"), ("Username", "username"),
            ("NIP", "nim_nip"), ("Program Studi", "prodi"),
            ("Role", "role"),
        ]:
            val = self.user.get(key, '-')
            if key == "role": val = val.capitalize()
            row = tk.Frame(card, bg=T.CARD_BG)
            row.pack(fill="x", pady=6)
            tk.Label(row, text=f"{label}:", font=T.FONT_LABEL,
                     bg=T.CARD_BG, fg=T.GRAY_MID, width=18, anchor="w").pack(side="left")
            tk.Label(row, text=val, font=(T.FONT_FAMILY, 12, "bold"),
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
