# backend/app/reportlab/theme.py
from __future__ import annotations

import os
from reportlab.lib import colors

# ============================================================
# Euklydia — SaaS Premium Theme (Official palette)
# ============================================================
EU_INK     = colors.HexColor("#0B3C3B")
EU_DARK    = colors.HexColor("#004E4C")
EU_PRIMARY = colors.HexColor("#006355")
EU_SECONDARY = colors.HexColor("#39A193")
EU_ACCENT  = colors.HexColor("#00B3A0")

BG_SOFT = colors.HexColor("#DDE7E7")
SURFACE = colors.HexColor("#F8FAFC")
BORDER  = colors.HexColor("#E5E7EB")
MUTED   = colors.HexColor("#64748B")
TEXT    = EU_INK
WHITE   = colors.white

# ============================================================
# Priority colors
# ============================================================
PRIORITY_HIGH          = colors.HexColor("#DC2626")
PRIORITY_MEDIUM        = colors.HexColor("#D97706")
PRIORITY_LOW           = colors.HexColor("#16A34A")
PRIORITY_HIGH_BG       = colors.HexColor("#FEF2F2")
PRIORITY_MEDIUM_BG     = colors.HexColor("#FFFBEB")
PRIORITY_LOW_BG        = colors.HexColor("#F0FDF4")
PRIORITY_HIGH_BORDER   = colors.HexColor("#FCA5A5")
PRIORITY_MEDIUM_BORDER = colors.HexColor("#FCD34D")
PRIORITY_LOW_BORDER    = colors.HexColor("#86EFAC")

# ============================================================
# Maturity level colors
# ============================================================
MATURITY_COLORS = {
    "Emerging":   colors.HexColor("#DC2626"),
    "Developing": colors.HexColor("#D97706"),
    "Advanced":   colors.HexColor("#2563EB"),
    "Strategic":  colors.HexColor("#16A34A"),
}

MATURITY_BG = {
    "Emerging":   colors.HexColor("#FEF2F2"),
    "Developing": colors.HexColor("#FFFBEB"),
    "Advanced":   colors.HexColor("#EFF6FF"),
    "Strategic":  colors.HexColor("#F0FDF4"),
}

# ============================================================
# Phase colors
# ============================================================
PHASE_COLORS = [
    colors.HexColor("#004E4C"),
    colors.HexColor("#006355"),
    colors.HexColor("#39A193"),
]

# ============================================================
# Layout tokens
# ============================================================
RADIUS   = 14
CARD_PAD = 14
CARD_GAP = 18
SECTION_GAP = 16
LINE = 12


def asset_path(filename: str) -> str:
    base_dir = os.path.dirname(__file__)
    return os.path.normpath(os.path.join(base_dir, "..", "assets", filename))