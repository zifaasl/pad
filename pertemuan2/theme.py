# ──────────────────────────────────────────────────────────────────
#  TEMA VISUAL – Aplikasi Absensi Akademik
#  Palet: Deep Navy  ×  Electric Indigo  ×  Warm White  ×  Accent Teal
# ──────────────────────────────────────────────────────────────────

# ── WARNA UTAMA ──────────────────────────────────────────────────
NAVY         = "#0F172A"   # latar sidebar / header
NAVY_MID     = "#1E293B"   # card gelap
NAVY_LIGHT   = "#334155"   # border / hover

INDIGO       = "#6366F1"   # aksen utama (tombol, highlight)
INDIGO_LIGHT = "#818CF8"   # hover state
INDIGO_DARK  = "#4F46E5"   # active state

TEAL         = "#14B8A6"   # success / hadir
AMBER        = "#F59E0B"   # warning / izin
RED          = "#EF4444"   # error / alpha
PURPLE       = "#A855F7"   # sakit / info

WHITE        = "#F8FAFC"   # teks utama
GRAY_LIGHT   = "#CBD5E1"   # teks sekunder
GRAY_MID     = "#94A3B8"   # placeholder
CARD_BG      = "#1E293B"   # background card
PAGE_BG      = "#0F172A"   # background halaman

# ── FONT ─────────────────────────────────────────────────────────
FONT_FAMILY  = "Segoe UI"
FONT_TITLE   = (FONT_FAMILY, 26, "bold")
FONT_HEADING = (FONT_FAMILY, 18, "bold")
FONT_SUB     = (FONT_FAMILY, 14, "bold")
FONT_BODY    = (FONT_FAMILY, 12)
FONT_SMALL   = (FONT_FAMILY, 10)
FONT_LABEL   = (FONT_FAMILY, 11)
FONT_CODE    = ("Consolas", 11)

# ── UKURAN ───────────────────────────────────────────────────────
RADIUS       = 10
PADDING_LG   = 30
PADDING_MD   = 20
PADDING_SM   = 12
PADDING_XS   = 8

BTN_PADDING  = (12, 30)
BTN_RADIUS   = 8

# ── STATUS WARNA ─────────────────────────────────────────────────
STATUS_COLOR = {
    "hadir" : TEAL,
    "izin"  : AMBER,
    "sakit" : PURPLE,
    "alpha" : RED,
}

STATUS_ICON = {
    "hadir" : "✅",
    "izin"  : "📋",
    "sakit" : "🏥",
    "alpha" : "❌",
}

# ── HELPER ───────────────────────────────────────────────────────
def apply_dark_style(widget, bg=PAGE_BG, fg=WHITE):
    """Apply dark theme to a widget recursively."""
    try:
        widget.configure(bg=bg, fg=fg)
    except Exception:
        pass
    for child in widget.winfo_children():
        apply_dark_style(child, bg, fg)
