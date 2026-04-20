# backend/app/reportlab/components.py
from __future__ import annotations

from typing import Dict, Any, List, Optional
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT

from app.reportlab.theme import (
    EU_INK, EU_DARK, EU_PRIMARY, EU_SECONDARY, EU_ACCENT,
    BG_SOFT, SURFACE, BORDER, MUTED, TEXT, WHITE,
    RADIUS, CARD_PAD, CARD_GAP, SECTION_GAP, LINE,
    PRIORITY_HIGH, PRIORITY_MEDIUM, PRIORITY_LOW,
    PRIORITY_HIGH_BG, PRIORITY_MEDIUM_BG, PRIORITY_LOW_BG,
    PRIORITY_HIGH_BORDER, PRIORITY_MEDIUM_BORDER, PRIORITY_LOW_BORDER,
    MATURITY_COLORS, MATURITY_BG, PHASE_COLORS,
)

# ============================================================
# Layout constants
# ============================================================
_BAR_H        = 8    # unified bar height — all pages
_TICK_AREA_H  = 14   # space below bar for tick marks + labels
SCALE_BLOCK_H = _BAR_H + _TICK_AREA_H   # = 22 pts total


# ============================================================
# Default translation fallback (English)
# Used when t=None is passed to components
# ============================================================
_DEFAULT_T: Dict[str, str] = {
    "why_it_matters":    "Why it matters",
    "risk":              "Risk",
    "business_leverage": "Business leverage",
    "quick_win":         "Quick win (max. 2 weeks)",
    "objective":         "Objective",
    "key_actions":       "Key actions",
    "success_metrics":   "Success metrics",
    "expected_impact":   "Expected impact",
}


def _t(translations: Optional[Dict], key: str) -> str:
    """Safe translation lookup with English fallback."""
    if translations:
        return translations.get(key, _DEFAULT_T.get(key, key))
    return _DEFAULT_T.get(key, key)


# ============================================================
# Color helpers
# ============================================================

def score_color(score: float) -> colors.Color:
    if score < 40:
        return PRIORITY_HIGH
    if score < 60:
        return PRIORITY_MEDIUM
    if score < 80:
        return colors.HexColor("#2563EB")
    return PRIORITY_LOW


def maturity_color(level: str) -> colors.Color:
    return MATURITY_COLORS.get(level, EU_PRIMARY)


def priority_colors(label: str):
    if label == "High":
        return PRIORITY_HIGH_BG, PRIORITY_HIGH_BORDER, PRIORITY_HIGH
    if label == "Medium":
        return PRIORITY_MEDIUM_BG, PRIORITY_MEDIUM_BORDER, PRIORITY_MEDIUM
    return PRIORITY_LOW_BG, PRIORITY_LOW_BORDER, PRIORITY_LOW


# ============================================================
# ★ UNIFIED SCALE BAR — single implementation for all pages
# ============================================================

def draw_scale_bar(
    c: canvas.Canvas,
    x: float,
    y_top: float,
    w: float,
    score: float,
    fill_color=None,
    show_ticks: bool = True,
) -> float:
    """
    Draws a unified score bar identical on every page.

    Parameters
    ----------
    x, y_top  : top-left anchor (bar fills downward from y_top)
    w         : bar width
    score     : 0–100
    fill_color: override fill (default = score_color(score))
    show_ticks: draw 40/60/80 tick marks below bar

    Returns
    -------
    Height consumed: SCALE_BLOCK_H (22) with ticks, _BAR_H (8) without.
    """
    fc    = fill_color if fill_color is not None else score_color(float(score))
    bar_y = y_top - _BAR_H

    # Background track
    c.setFillColor(colors.HexColor("#F1F5F9"))
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.5)
    c.roundRect(x, bar_y, w, _BAR_H, 4, fill=1, stroke=1)
    c.setLineWidth(1)

    # Filled portion
    p = max(0.0, min(100.0, float(score)))
    if p > 0:
        vw = max(6.0, (p / 100.0) * w)
        c.setFillColor(fc)
        c.setStrokeColor(fc)
        c.roundRect(x, bar_y, vw, _BAR_H, 4, fill=1, stroke=0)

    if not show_ticks:
        return float(_BAR_H)

    # Tick marks at 40 / 60 / 80
    c.setLineWidth(0.6)
    for mark in [40, 60, 80]:
        tx = x + (mark / 100.0) * w
        c.setStrokeColor(colors.HexColor("#CBD5E1"))
        c.line(tx, bar_y - 1, tx, bar_y + _BAR_H + 1)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 6.5)
        c.drawCentredString(tx, bar_y - 10, str(mark))
    c.setLineWidth(1)

    return float(SCALE_BLOCK_H)


# ============================================================
# Backward-compat wrapper
# ============================================================

def progress_bar(
    c: canvas.Canvas, x: float, y: float, w: float, h: float,
    percent: float, fill_color=None,
):
    """Backward-compatible shim — bar only, no ticks."""
    draw_scale_bar(c, x, y + _BAR_H, w, percent,
                   fill_color=fill_color, show_ticks=False)


# ============================================================
# Lightning icon (drawn — replaces ⚡ emoji)
# ============================================================

def draw_lightning_icon(
    c: canvas.Canvas, x: float, y: float,
    size: float = 10, color=None,
):
    """Draws a lightning bolt as a ReportLab path (no unicode)."""
    if color is None:
        color = colors.HexColor("#D97706")
    c.setFillColor(color)
    c.setLineWidth(0)
    sw = size * 0.55
    p = c.beginPath()
    p.moveTo(x + sw * 0.5, y + size)
    p.lineTo(x + sw,        y + size * 0.55)
    p.lineTo(x + sw * 0.55, y + size * 0.55)
    p.lineTo(x + sw * 0.9,  y)
    p.lineTo(x,              y + size * 0.48)
    p.lineTo(x + sw * 0.45, y + size * 0.48)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.setLineWidth(1)


# ============================================================
# Primitives
# ============================================================

def topbar(c: canvas.Canvas):
    W, H = A4
    c.setFillColor(EU_DARK)
    c.rect(0, H - 12, W, 12, fill=1, stroke=0)


def rounded_rect(
    c: canvas.Canvas,
    x: float, y: float, w: float, h: float,
    r: float = RADIUS,
    fill=WHITE, stroke=BORDER,
    stroke_width: float = 1,
):
    c.setLineWidth(stroke_width)
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.roundRect(x, y, w, h, r, fill=1, stroke=1)
    c.setLineWidth(1)


def left_accent_bar(
    c: canvas.Canvas, x: float, y: float, h: float,
    color=EU_PRIMARY, width: float = 4, radius: float = 4,
):
    c.setFillColor(color)
    c.setStrokeColor(color)
    c.roundRect(x, y, width, h, radius, fill=1, stroke=0)


def hr(c: canvas.Canvas, x: float, y: float, w: float):
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.8)
    c.line(x, y, x + w, y)
    c.setLineWidth(1)


def text(
    c: canvas.Canvas, x: float, y: float, s: str,
    size: int = 10, color=TEXT, bold: bool = False,
):
    c.setFillColor(color)
    c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
    c.drawString(x, y, str(s or ""))


def wrap(
    c: canvas.Canvas, x: float, y: float, s: str,
    max_w: float, size: int = 10, color=TEXT,
    leading: float = LINE, bold: bool = False,
) -> float:
    c.setFillColor(color)
    font = "Helvetica-Bold" if bold else "Helvetica"
    c.setFont(font, size)
    words = (str(s or "")).split()
    if not words:
        return y - leading
    line = ""
    for w in words:
        test = (line + " " + w).strip()
        if c.stringWidth(test, font, size) <= max_w:
            line = test
        else:
            if line:
                c.drawString(x, y, line)
                y -= leading
            line = w
    if line:
        c.drawString(x, y, line)
        y -= leading
    return y


# ============================================================
# Paragraph helpers
# ============================================================

def _pstyle(
    font: str, size: int, leading: int, color, bold: bool = False,
) -> ParagraphStyle:
    return ParagraphStyle(
        name="eu_p",
        fontName="Helvetica-Bold" if bold else font,
        fontSize=size,
        leading=leading,
        textColor=color,
        alignment=TA_LEFT,
    )


def measure_paragraph(
    text_html: str, width: float,
    font_name: str = "Helvetica", font_size: int = 10,
    leading: int = 12, color=TEXT, bold: bool = False,
) -> float:
    p = Paragraph(
        (text_html or "").replace("\n", "<br/>"),
        _pstyle(font_name, font_size, leading, color, bold=bold),
    )
    _, h = p.wrap(width, 10000)
    return h


def draw_paragraph(
    c: canvas.Canvas, x: float, y_top: float,
    text_html: str, width: float,
    font_name: str = "Helvetica", font_size: int = 10,
    leading: int = 12, color=TEXT, bold: bool = False,
) -> float:
    p = Paragraph(
        (text_html or "").replace("\n", "<br/>"),
        _pstyle(font_name, font_size, leading, color, bold=bold),
    )
    _, h = p.wrap(width, 10000)
    p.drawOn(c, x, y_top - h)
    return h


def draw_bullets(
    c: canvas.Canvas, x: float, y_top: float, w: float,
    items: List[str], font_size: int = 10, leading: int = 12,
    max_items: int = 4, color=TEXT,
) -> float:
    used = 0.0
    y = y_top
    for it in [str(i).strip() for i in (items or []) if str(i).strip()][:max_items]:
        h = draw_paragraph(c, x, y, f"- {it}", w,
                           font_size=font_size, leading=leading, color=color)
        y    -= h
        used += h
    return used


# ============================================================
# UI components
# ============================================================

def footer(c: canvas.Canvas, page: int, mx: float):
    W, _ = A4
    c.setFont("Helvetica", 8)
    c.setFillColor(MUTED)
    c.drawRightString(W - mx, 12 * 2.8346457, f"Page {page}")


def section_title(
    c: canvas.Canvas, x: float, y: float,
    title_s: str, subtitle: str = "",
) -> float:
    text(c, x, y, title_s, size=16, color=TEXT, bold=True)
    if subtitle:
        text(c, x, y - 16, subtitle, size=9, color=MUTED)
        return y - 40
    return y - 30


def badge(
    c: canvas.Canvas, x: float, y: float, label: str,
    fill=colors.HexColor("#F8FAFC"), stroke=BORDER, text_color=EU_DARK,
):
    label = str(label or "").strip()
    w = max(56, c.stringWidth(label, "Helvetica-Bold", 9) + 18)
    rounded_rect(c, x, y, w, 18, r=9, fill=fill, stroke=stroke)
    text(c, x + 9, y + 5, label, size=9, color=text_color, bold=True)


def priority_badge(c: canvas.Canvas, x: float, y: float, label: str):
    bg, border, tc = priority_colors(label)
    badge(c, x, y, label, fill=bg, stroke=border, text_color=tc)


def chip(c: canvas.Canvas, x: float, y: float, label: str, variant: str = "neutral"):
    label = str(label or "").strip()
    if not label:
        return
    if variant == "strength":
        stroke, textc = EU_SECONDARY, EU_DARK
        fill = colors.Color(0.22, 0.63, 0.58, alpha=0.08)
    elif variant == "gap":
        stroke, textc = EU_ACCENT, EU_DARK
        fill = colors.Color(0.0, 0.70, 0.63, alpha=0.10)
    else:
        stroke, textc = BORDER, MUTED
        fill = colors.HexColor("#F8FAFC")
    w = max(44, c.stringWidth(label, "Helvetica", 9) + 18)
    rounded_rect(c, x, y, w, 18, r=9, fill=fill, stroke=stroke)
    text(c, x + 9, y + 5, label, size=9, color=textc)


def chips_wrap(
    c: canvas.Canvas, x: float, y: float, max_w: float,
    labels: List[str], variant: str = "gap",
    max_lines: int = 3, gap: float = 6, line_gap: float = 6,
) -> float:
    cx, cy, lines = x, y, 1
    for lab in (labels or []):
        label = str(lab or "").strip()
        if not label:
            continue
        w = max(44, c.stringWidth(label, "Helvetica", 9) + 18)
        if cx + w > x + max_w:
            lines += 1
            if lines > max_lines:
                break
            cx, cy = x, cy - (18 + line_gap)
        chip(c, cx, cy, label, variant=variant)
        cx += w + gap
    return cy - 18


def gap_priority_label(priority_value: float) -> str:
    """
    ★ FIXED thresholds (aligned with assessment_rules.py HIGH_MAX=49):
      priority = (100 - score) * weight  (weight=1 by default)
      score <= 49  →  priority >= 51  →  High
      score <= 74  →  priority >= 26  →  Medium
      score >= 75  →  priority <= 25  →  Low
    """
    p = float(priority_value or 0.0)
    if p > 50:
        return "High"
    if p > 25:
        return "Medium"
    return "Low"


# ============================================================
# insight_card  — page 2
# ★ Accepts optional `t` dict for bilingual labels
# ============================================================

def insight_card(
    c: canvas.Canvas, x: float, y_top: float, w: float,
    title_s: str, score: Optional[float],
    why: str, risk: str, leverage: str, quick: str,
    t: Optional[Dict] = None,
) -> float:
    pad      = CARD_PAD
    accent_w = 5
    inner_x  = x + accent_w + pad
    inner_w  = w - accent_w - 2 * pad

    sc           = float(score) if score is not None else 0.0
    accent_color = score_color(sc)

    # Labels (translated)
    lbl_why  = _t(t, "why_it_matters")
    lbl_risk = _t(t, "risk")
    lbl_lev  = _t(t, "business_leverage")
    lbl_qw   = _t(t, "quick_win")

    # Measure content
    why_h   = measure_paragraph(why or "-",      inner_w, font_size=10, leading=12)
    risk_h  = measure_paragraph(risk or "-",     inner_w, font_size=10, leading=12)
    lev_h   = measure_paragraph(leverage or "-", inner_w, font_size=10, leading=12)
    quick_h = measure_paragraph(quick or "-",    inner_w - 28, font_size=9, leading=11)

    SEP          = 8
    header_block = pad + 14 + 4
    score_row    = 22
    bar_block    = SCALE_BLOCK_H + 6
    text_blocks  = (11 + why_h + SEP) + (11 + risk_h + SEP) + (11 + lev_h + SEP)
    qw_block     = max(42, pad + 14 + 4 + quick_h + pad)

    h = max(260, header_block + score_row + bar_block + text_blocks + qw_block + pad)

    # Card shell
    rounded_rect(c, x, y_top - h, w, h, r=RADIUS, fill=WHITE, stroke=BORDER)
    left_accent_bar(c, x, y_top - h, h, color=accent_color,
                    width=accent_w, radius=RADIUS)

    yy = y_top - pad - 14

    # Title + score badge
    text(c, inner_x, yy, title_s, size=11, bold=True)
    if score is not None:
        sc_bg = (MATURITY_BG.get("Emerging", colors.HexColor("#FEF2F2"))
                 if sc < 40 else colors.HexColor("#F8FAFC"))
        badge(c, x + w - 80, yy - 4,
              f"{sc:.0f}%",
              fill=sc_bg, stroke=accent_color, text_color=accent_color)
    yy -= (header_block - pad + 4)

    # Unified scale bar
    draw_scale_bar(c, inner_x, yy, inner_w, sc,
                   fill_color=accent_color, show_ticks=True)
    yy -= bar_block

    # Text sections (translated labels)
    yy -= draw_paragraph(c, inner_x, yy, f"<b>{lbl_why}</b>",
                         inner_w, font_size=9, leading=11, color=MUTED)
    yy -= 2
    yy -= draw_paragraph(c, inner_x, yy, why or "-",
                         inner_w, font_size=10, leading=12)
    yy -= SEP

    yy -= draw_paragraph(c, inner_x, yy, f"<b>{lbl_risk}</b>",
                         inner_w, font_size=9, leading=11, color=MUTED)
    yy -= 2
    yy -= draw_paragraph(c, inner_x, yy, risk or "-",
                         inner_w, font_size=10, leading=12)
    yy -= SEP

    yy -= draw_paragraph(c, inner_x, yy, f"<b>{lbl_lev}</b>",
                         inner_w, font_size=9, leading=11, color=MUTED)
    yy -= 2
    yy -= draw_paragraph(c, inner_x, yy, leverage or "-",
                         inner_w, font_size=10, leading=12)

    # Quick win callout — anchored to card bottom
    qw_y = (y_top - h) + pad
    rounded_rect(c, inner_x, qw_y, inner_w, qw_block,
                 r=10, fill=BG_SOFT, stroke=EU_ACCENT, stroke_width=1)

    icon_y = qw_y + qw_block - pad - 8
    draw_lightning_icon(c, inner_x + pad, icon_y - 2, size=10,
                        color=colors.HexColor("#D97706"))
    c.setFillColor(EU_DARK)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(inner_x + pad + 14, icon_y, lbl_qw)

    draw_paragraph(c, inner_x + pad, icon_y - 8,
                   quick or "-",
                   inner_w - 2 * pad,
                   font_size=9, leading=11, color=EU_DARK)

    return h


# ============================================================
# phase_card  — page 4
# ★ Accepts optional `t` dict for bilingual labels
# ============================================================

def phase_card(
    c: canvas.Canvas, x: float, y_top: float, w: float,
    phase_label: str, focus: str, objective: str,
    actions: List[str], metrics: List[str], impact: str,
    phase_index: int = 0,
    t: Optional[Dict] = None,
) -> float:
    pad     = CARD_PAD
    inner_w = w - 2 * pad
    hdr_h   = 38

    ph_color = PHASE_COLORS[min(phase_index, len(PHASE_COLORS) - 1)]

    # Labels (translated)
    lbl_obj     = _t(t, "objective")
    lbl_actions = _t(t, "key_actions")
    lbl_metrics = _t(t, "success_metrics")
    lbl_impact  = _t(t, "expected_impact")

    # Measure variable blocks
    obj_h = measure_paragraph(objective or "-", inner_w, font_size=10, leading=12)
    act_h = sum(
        measure_paragraph(f"- {a}", inner_w - 4, font_size=10, leading=12)
        for a in [str(a).strip() for a in (actions or []) if str(a).strip()][:3]
    )
    met_h = sum(
        measure_paragraph(f"- {m}", inner_w - 4, font_size=10, leading=12)
        for m in [str(m).strip() for m in (metrics or []) if str(m).strip()][:2]
    )

    impact_pill_h = 32
    h = max(180,
            hdr_h + 18
            + (11 + obj_h) + 12
            + (11 + act_h) + 10
            + (11 + met_h) + 16
            + impact_pill_h + 14)

    y = y_top - h
    rounded_rect(c, x, y, w, h, r=RADIUS, fill=WHITE, stroke=BORDER)
    left_accent_bar(c, x, y, h, color=ph_color, width=5, radius=RADIUS)

    # Header band
    c.setFillColor(ph_color)
    c.roundRect(x, y_top - hdr_h, w, hdr_h, 12, fill=1, stroke=0)

    cx_ = x + pad + 12
    cy_ = y_top - hdr_h / 2
    c.setFillColor(colors.Color(1, 1, 1, alpha=0.2))
    c.circle(cx_, cy_, 12, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(cx_, cy_ - 4, str(phase_index + 1))

    safe_label = (phase_label
                  .replace("\u2013", "-")
                  .replace("\u2014", "-"))
    text(c, x + pad + 30, y_top - 24, safe_label, size=10, color=WHITE, bold=True)

    if focus:
        f = str(focus).strip()
        if len(f) > 38:
            f = f[:35].rsplit(" ", 1)[0] + "..."
        badge(c, x + w - 210, y_top - hdr_h + 10, f,
              fill=colors.Color(1, 1, 1, alpha=0.18),
              stroke=colors.Color(1, 1, 1, alpha=0.30),
              text_color=WHITE)

    yy = y_top - hdr_h - 14

    # Content blocks (translated labels)
    yy -= draw_paragraph(c, x + pad, yy, f"<b>{lbl_obj}</b>",
                         inner_w, font_size=9, leading=11, color=MUTED)
    yy -= 2
    yy -= draw_paragraph(c, x + pad, yy, objective or "-",
                         inner_w, font_size=10, leading=12)
    yy -= 10

    hr(c, x + pad, yy, inner_w)
    yy -= 12

    yy -= draw_paragraph(c, x + pad, yy, f"<b>{lbl_actions}</b>",
                         inner_w, font_size=9, leading=11, color=MUTED)
    yy -= 4
    yy -= draw_bullets(c, x + pad + 4, yy, inner_w - 4,
                       actions, max_items=3, color=TEXT)
    yy -= 8

    yy -= draw_paragraph(c, x + pad, yy, f"<b>{lbl_metrics}</b>",
                         inner_w, font_size=9, leading=11, color=MUTED)
    yy -= 4
    yy -= draw_bullets(c, x + pad + 4, yy, inner_w - 4,
                       metrics, max_items=2, color=TEXT)

    # Impact pill anchored to bottom
    imp   = (impact or "").strip().replace("\u2013", "-").replace("\u2014", "-")
    box_y = y + 10
    rounded_rect(c, x + pad, box_y, inner_w, impact_pill_h,
                 r=10, fill=ph_color, stroke=ph_color, stroke_width=1)
    text(c, x + pad + 10, box_y + 20, lbl_impact,
         size=9, color=WHITE, bold=True)
    draw_paragraph(c, x + pad + 120, box_y + 22, imp or "-",
                   inner_w - 130, font_size=9, leading=10, color=WHITE)

    return h