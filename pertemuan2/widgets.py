"""
widgets.py – Komponen UI yang dapat digunakan ulang
"""
import tkinter as tk
from tkinter import ttk
import theme as T


def make_card(parent, **kwargs):
    """Frame bergaya card dengan latar navy-mid."""
    defaults = dict(bg=T.CARD_BG, relief="flat", bd=0)
    defaults.update(kwargs)
    frame = tk.Frame(parent, **defaults)
    return frame


def make_label(parent, text, font=T.FONT_BODY, fg=T.WHITE, bg=None, **kwargs):
    bg = bg or parent.cget("bg")
    return tk.Label(parent, text=text, font=font, fg=fg, bg=bg, **kwargs)


def make_entry(parent, show=None, width=30):
    """Entry field dengan tampilan dark."""
    entry = tk.Entry(
        parent,
        font=T.FONT_BODY,
        bg=T.NAVY_LIGHT,
        fg=T.WHITE,
        insertbackground=T.WHITE,
        relief="flat",
        bd=0,
        width=width,
        show=show or "",
        highlightthickness=2,
        highlightbackground=T.NAVY_LIGHT,
        highlightcolor=T.INDIGO,
    )
    return entry


def make_button(parent, text, command, bg=T.INDIGO, fg=T.WHITE,
                hover_bg=T.INDIGO_DARK, font=T.FONT_BODY, width=None, **kwargs):
    """Tombol interaktif dengan efek hover."""
    btn_kwargs = dict(
        text=text,
        command=command,
        bg=bg,
        fg=fg,
        font=font,
        relief="flat",
        bd=0,
        cursor="hand2",
        activebackground=hover_bg,
        activeforeground=fg,
        padx=T.BTN_PADDING[1],
        pady=T.BTN_PADDING[0],
    )
    if width:
        btn_kwargs["width"] = width
    btn_kwargs.update(kwargs)
    btn = tk.Button(parent, **btn_kwargs)

    def on_enter(e):
        btn.config(bg=hover_bg)
    def on_leave(e):
        btn.config(bg=bg)

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn


def make_badge(parent, text, color):
    """Label kecil berbentuk badge berwarna."""
    return tk.Label(
        parent, text=f"  {text}  ",
        bg=color, fg=T.WHITE,
        font=T.FONT_SMALL,
        relief="flat", bd=0,
        padx=4, pady=2
    )


def make_separator(parent, bg=T.NAVY_LIGHT, height=1):
    return tk.Frame(parent, bg=bg, height=height)


def make_stat_card(parent, title, value, color=T.INDIGO, icon="📊"):
    """Card statistik dengan ikon dan nilai besar."""
    card = make_card(parent, padx=20, pady=16)
    # Ikon
    tk.Label(card, text=icon, font=(T.FONT_FAMILY, 22), bg=T.CARD_BG, fg=color).pack(anchor="w")
    # Nilai
    tk.Label(card, text=str(value), font=(T.FONT_FAMILY, 28, "bold"),
             bg=T.CARD_BG, fg=color).pack(anchor="w")
    # Judul
    tk.Label(card, text=title, font=T.FONT_SMALL,
             bg=T.CARD_BG, fg=T.GRAY_MID).pack(anchor="w")
    return card


class ScrollableFrame(tk.Frame):
    """Frame dengan scrollbar vertikal."""
    def __init__(self, parent, bg=T.PAGE_BG, **kwargs):
        super().__init__(parent, bg=bg, **kwargs)

        canvas = tk.Canvas(self, bg=bg, highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)

        self.inner = tk.Frame(canvas, bg=bg)
        self.inner.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mouse wheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)


class ToastNotification:
    """Notifikasi sementara yang muncul di pojok kanan bawah."""
    def __init__(self, root, message, color=T.TEAL, duration=3000):
        self.root = root
        self.toast = tk.Toplevel(root)
        self.toast.overrideredirect(True)
        self.toast.attributes("-topmost", True)

        frame = tk.Frame(self.toast, bg=color, padx=20, pady=12)
        frame.pack()
        tk.Label(frame, text=message, bg=color, fg="white",
                 font=T.FONT_BODY).pack()

        # Posisi
        self.toast.update_idletasks()
        w = self.toast.winfo_width()
        h = self.toast.winfo_height()
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        self.toast.geometry(f"+{sw - w - 30}+{sh - h - 80}")

        self.toast.after(duration, self.toast.destroy)
