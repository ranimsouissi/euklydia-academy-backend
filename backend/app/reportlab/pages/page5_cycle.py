# backend/app/reportlab/pages/page5_cycle.py
from __future__ import annotations

from datetime import datetime
from typing import Dict, Any
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

from app.reportlab.theme import MUTED, BORDER, RADIUS, CARD_PAD, EU_PRIMARY
from app.reportlab.translations import get_t
from app.reportlab.components import (
    topbar, section_title, rounded_rect, draw_paragraph,
    left_accent_bar, footer, text, measure_paragraph,
)

_BANNER_BG     = colors.HexColor("#E1F5EE")
_BANNER_BORDER = colors.HexColor("#39A193")
_BANNER_TEXT   = colors.HexColor("#004E4C")
_CTA_BG        = colors.HexColor("#FFF8E1")
_CTA_BORDER    = colors.HexColor("#D97706")
_CTA_TEXT      = colors.HexColor("#92400E")


def draw(c: canvas.Canvas, payload: Dict[str, Any], page: int, mx: float, top: float):
    W, H = A4
    topbar(c)
    t = get_t(payload.get("language", "en"))

    card_w = W - 2 * mx

    # ── Page title ────────────────────────────────────────────────────────
    y = section_title(c, mx, top, t["page5_title"], t["page5_sub"])

    # ── Validity banner ───────────────────────────────────────────────────
    banner_h = 52
    rounded_rect(c, mx, y - banner_h, card_w, banner_h,
                 r=RADIUS, fill=_BANNER_BG, stroke=_BANNER_BORDER, stroke_width=1.5)
    left_accent_bar(c, mx, y - banner_h, banner_h,
                    color=_BANNER_BORDER, width=5, radius=RADIUS)

    # Left: "Valid for / 90 days"
    text(c, mx + 20, y - 16, t["validity_label"], size=9,  color=_BANNER_TEXT)
    text(c, mx + 20, y - 36, t["validity_value"], size=18, color=_BANNER_TEXT, bold=True)

    # Right: "Next assessment: DD/MM/YYYY"
    meta     = payload.get("meta", {})
    next_raw = meta.get("next_assessment_recommended", "")
    if next_raw:
        try:
            next_date_str = datetime.fromisoformat(next_raw).strftime("%d/%m/%Y")
        except Exception:
            next_date_str = next_raw[:10]
        text(c, mx + 220, y - 16, t["next_assessment"], size=9,  color=_BANNER_TEXT)
        text(c, mx + 220, y - 36, next_date_str,         size=18, color=_BANNER_TEXT, bold=True)

    y -= (banner_h + 18)

    # ── Note card ─────────────────────────────────────────────────────────
    note_txt = t["note_body"].replace("\n\n", "<br/><br/>")
    cta_txt  = t["cta_label"]

    body_h  = measure_paragraph(note_txt, card_w - 2 * CARD_PAD - 6,
                                font_size=10, leading=13)
    cta_h   = measure_paragraph(cta_txt, card_w - 2 * CARD_PAD - 32,
                                font_size=9, leading=11)
    cta_box = max(32, cta_h + 20)
    note_h  = CARD_PAD + 20 + 8 + body_h + 14 + cta_box + CARD_PAD

    rounded_rect(c, mx, y - note_h, card_w, note_h,
                 r=RADIUS, fill=colors.white, stroke=BORDER)
    left_accent_bar(c, mx, y - note_h, note_h,
                    color=EU_PRIMARY, width=5, radius=RADIUS)

    text(c, mx + CARD_PAD + 6, y - CARD_PAD - 14,
         t["note_title"], size=11, bold=True)

    draw_paragraph(c, mx + CARD_PAD + 6, y - CARD_PAD - 34,
                   note_txt,
                   width=card_w - 2 * CARD_PAD - 6,
                   font_size=10, leading=13, color=MUTED)

    # CTA pill anchored to card bottom
    cta_y = (y - note_h) + CARD_PAD
    rounded_rect(c, mx + CARD_PAD + 6, cta_y,
                 card_w - 2 * CARD_PAD - 12, cta_box,
                 r=10, fill=_CTA_BG, stroke=_CTA_BORDER, stroke_width=1)
    draw_paragraph(c, mx + CARD_PAD + 16, cta_y + cta_box - 8,
                   cta_txt,
                   width=card_w - 2 * CARD_PAD - 32,
                   font_size=9, leading=11, color=_CTA_TEXT)

    footer(c, page, mx)