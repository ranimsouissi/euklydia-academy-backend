# backend/app/reportlab/pages/page1_summary.py
from __future__ import annotations

from datetime import datetime
from typing import Dict, Any
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

from app.reportlab.theme import BORDER, MUTED, TEXT, EU_DARK, CARD_PAD, RADIUS, EU_PRIMARY
from app.reportlab.translations import get_t
from app.reportlab.components import (
    rounded_rect, text, wrap, topbar, chips_wrap, footer,
    draw_paragraph, measure_paragraph,
    draw_scale_bar, SCALE_BLOCK_H,
)

_WHITE       = colors.white
_COVER_BG    = EU_DARK
_COVER_MUTED = colors.HexColor("#9EE5D8")
_TEAL_BG     = colors.HexColor("#E1F5EE")
_TEAL_FG     = colors.HexColor("#0F6E56")
_SCORE_COLOR = colors.HexColor("#0F6E56")


def _person_icon(c, x, y):
    c.setFillColor(_TEAL_BG)
    c.roundRect(x, y, 14, 14, 3, fill=1, stroke=0)
    c.setFillColor(_TEAL_FG)
    c.circle(x + 7, y + 9.5, 2.5, fill=1, stroke=0)
    c.roundRect(x + 3.5, y + 2, 7, 5, 2, fill=1, stroke=0)


def _email_icon(c, x, y):
    c.setFillColor(_TEAL_BG)
    c.roundRect(x, y, 14, 14, 3, fill=1, stroke=0)
    c.setFillColor(_TEAL_FG)
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(x + 7, y + 4, "@")


def _card(c, x, y, w, h, title):
    """White card. y = top of card."""
    rounded_rect(c, x, y - h, w, h, r=RADIUS, fill=_WHITE, stroke=BORDER)
    text(c, x + CARD_PAD, y - 20, title, size=11, bold=True)


def draw(c: canvas.Canvas, payload: Dict[str, Any], page: int, mx: float, top: float):
    W, _ = A4
    topbar(c)
    t = get_t(payload.get("language", "en"))

    leader     = payload["leader"]
    assessment = payload["assessment"]
    llm        = payload.get("llm_narrative") or {}

    # ── Header ────────────────────────────────────────────────────────────
    header_h = 100
    header_y = top - header_h
    rounded_rect(c, mx, header_y, W - 2 * mx, header_h,
                 r=RADIUS, fill=_COVER_BG, stroke=_COVER_BG)

    c.setFillColor(_COVER_MUTED)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(mx + 16, top - 22, t["academy_name"])

    c.setFillColor(_WHITE)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(mx + 16, top - 48, t["report_title"])

    now_str = datetime.now().strftime("%d/%m/%Y  %H:%M")
    c.setFillColor(_COVER_MUTED)
    c.setFont("Helvetica", 9)
    c.drawString(mx + 16, header_y + 14, now_str)

    # ── Leader card ───────────────────────────────────────────────────────
    y           = header_y - 14
    leader_h    = 88
    card_w_full = W - 2 * mx

    _card(c, mx, y, card_w_full, leader_h, t["leader"])

    raw_name  = leader.get("full_name") or leader.get("name", "-")
    full_name = raw_name.title()

    _person_icon(c, mx + CARD_PAD, y - 46)
    text(c, mx + CARD_PAD + 18, y - 40, full_name, size=13, bold=True)

    _email_icon(c, mx + CARD_PAD, y - 66)
    text(c, mx + CARD_PAD + 18, y - 60, leader.get("email", "-"), size=10, color=MUTED)

    text(c, mx + CARD_PAD, y - 80, t["role_label"], size=9, color=MUTED)
    wrap(c, mx + CARD_PAD + 34, y - 80, leader.get("role", "-"),
         max_w=card_w_full - 2 * CARD_PAD - 34, size=10, color=TEXT, leading=12)

    y -= (leader_h + 14)

    # ── KPI row ───────────────────────────────────────────────────────────
    card_w3    = (W - 2 * mx - 24) / 3
    ky         = y
    inner_pad  = 14

    score_x    = mx
    gap_x      = mx + card_w3 + 12
    strength_x = mx + 2 * (card_w3 + 12)

    # ★ Définir les données EN PREMIER
    all_breakdown = assessment.get("skill_breakdown", [])
    high_gaps = [
        r["skill"] for r in all_breakdown
        if float(r.get("priority", 0)) > 50
    ][:3]
    strengths = (assessment.get("strengths") or [])[:3]
    score_val = float(assessment.get("global_score_percent", 0.0))

    # ★ Puis calculer kpi_h qui dépend de high_gaps et strengths
    max_chips    = max(len(high_gaps), len(strengths), 1)
    chips_area_h = max_chips * 18 + (max_chips - 1) * 6 + 20
    kpi_h        = max(110, 20 + 14 + chips_area_h + SCALE_BLOCK_H + 10)
    chips_zone_y = ky - 44
    kpi_h              = max(110, 20 + 14 + chips_area_h + SCALE_BLOCK_H + 10)
    ky           = y
    inner_pad    = 14
    chips_zone_y = ky - 44   # ← single Y for both chip cards = guaranteed alignment

    score_x    = mx
    gap_x      = mx + card_w3 + 12
    strength_x = mx + 2 * (card_w3 + 12)

    # HIGH-only gaps (priority > 50 means score <= 49)
    all_breakdown = assessment.get("skill_breakdown", [])
    high_gaps = [
        r["skill"] for r in all_breakdown
        if float(r.get("priority", 0)) > 50
    ][:3]

    strengths = (assessment.get("strengths") or [])[:3]
    score_val = float(assessment.get("global_score_percent", 0.0))

    # — Global Score card —
    _card(c, score_x, ky, card_w3, kpi_h, t["global_score"])
    c.setFillColor(_SCORE_COLOR)
    c.setFont("Helvetica-Bold", 28)
    score_text_y = ky - 52
    c.drawString(score_x + CARD_PAD, score_text_y, f"{score_val:.0f}%")
    bar_top = max(score_text_y - 14, (ky - kpi_h) + SCALE_BLOCK_H + 6)
    draw_scale_bar(c, score_x + CARD_PAD, bar_top,
                   card_w3 - 2 * CARD_PAD, score_val,
                   fill_color=_SCORE_COLOR, show_ticks=True)

    # — High Priority Gaps card —
    _card(c, gap_x, ky, card_w3, kpi_h, t["high_priority_gaps"])
    if high_gaps:
        chips_wrap(c, gap_x + inner_pad, chips_zone_y,
                   card_w3 - 2 * inner_pad, high_gaps,
                   variant="gap", max_lines=3)
    else:
        text(c, gap_x + inner_pad, chips_zone_y, "-", size=10, color=MUTED)

    # — Strengths card —
    _card(c, strength_x, ky, card_w3, kpi_h, t["strengths"])
    if strengths:
        chips_wrap(c, strength_x + inner_pad, chips_zone_y,
                   card_w3 - 2 * inner_pad, strengths,
                   variant="strength", max_lines=3)
    else:
        text(c, strength_x + inner_pad, chips_zone_y, "-", size=10, color=MUTED)

    y -= (kpi_h + 18)

    # ── Narrative cards ───────────────────────────────────────────────────
    pad = CARD_PAD
    summary = llm.get("executive_summary") or (
        f"The {leader.get('role', 'role')} currently holds a global score of "
        f"{assessment.get('global_score_percent', 0)}%, reflecting a "
        f"{assessment.get('maturity_level', 'Unknown')} maturity level."
    )
    risk_txt = llm.get("strategic_risk_overview") or \
        "Strategic risks will be refined as more context becomes available."

    sum_h      = measure_paragraph(summary, card_w_full - 2 * pad, font_size=10, leading=12)
    sum_card_h = 16 + 20 + 8 + sum_h + 16
    rounded_rect(c, mx, y - sum_card_h, card_w_full, sum_card_h,
                 r=RADIUS, fill=_WHITE, stroke=BORDER)
    text(c, mx + pad, y - 22, t["executive_summary"], size=11, bold=True)
    draw_paragraph(c, mx + pad, y - 40, summary,
                   width=card_w_full - 2 * pad, font_size=10, leading=12, color=TEXT)
    y -= (sum_card_h + 14)

    risk_h      = measure_paragraph(risk_txt, card_w_full - 2 * pad, font_size=10, leading=12)
    risk_card_h = 16 + 20 + 8 + risk_h + 16
    rounded_rect(c, mx, y - risk_card_h, card_w_full, risk_card_h,
                 r=RADIUS,
                 fill=colors.Color(0.0, 0.39, 0.33, alpha=0.06),
                 stroke=BORDER)
    text(c, mx + pad, y - 22, t["strategic_risk_overview"], size=11, bold=True)
    draw_paragraph(c, mx + pad, y - 40, risk_txt,
                   width=card_w_full - 2 * pad, font_size=10, leading=12, color=MUTED)

    footer(c, page, mx)