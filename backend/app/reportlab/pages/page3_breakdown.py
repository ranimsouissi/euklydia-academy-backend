# backend/app/reportlab/pages/page3_breakdown.py
from __future__ import annotations

from typing import Dict, Any, List
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors

from app.reportlab.theme import BORDER, MUTED, TEXT, CARD_PAD, RADIUS
from app.reportlab.translations import get_t
from app.reportlab.components import (
    topbar, rounded_rect, text, wrap, priority_badge,
    gap_priority_label, footer,
    draw_paragraph, measure_paragraph, score_color,
    draw_scale_bar,
)

_MARGIN_BOTTOM = 18 * mm

# ── Column layout (relative to mx) ──────────────────────────────────────────
# Content width ≈ 493pt (A4=595, mx≈51)
# skill: 0→200 | score%: 200→230 | bar: 200→330 | priority: 340→410 | risk: 415→end
_COL_SKILL_OFF  = 12    # skill name x offset from mx
_COL_SCORE_OFF  = 200   # score % text
_COL_BAR_OFF    = 200   # bar starts at same x as score (bar is below score text)
_BAR_W          = 120   # bar width → ends at mx+320
_COL_PRIO_OFF   = 340   # gap priority badge
_COL_RISK_OFF   = 418   # business risk text


def draw(c: canvas.Canvas, payload: Dict[str, Any], page: int, mx: float, top: float):
    W, H = A4
    topbar(c)
    t = get_t(payload.get("language", "en"))

    content_w = W - 2 * mx

    col_skill = mx + _COL_SKILL_OFF
    col_score = mx + _COL_SCORE_OFF
    col_bar   = mx + _COL_BAR_OFF
    col_prio  = mx + _COL_PRIO_OFF
    col_risk  = mx + _COL_RISK_OFF
    risk_w    = (W - mx - 4) - col_risk

    assessment = payload["assessment"]
    breakdown: List[Dict[str, Any]] = assessment.get("skill_breakdown", [])

    y = top
    text(c, mx, y, t["ai_maturity_breakdown"], size=16, bold=True)
    text(c, mx, y - 16, t["ai_maturity_breakdown_sub"], size=9, color=MUTED)
    y -= 40

    # ── Top 4 summary block ──────────────────────────────────────────────
    top4 = breakdown[:4]
    if top4:
        top4_h = 22 + len(top4) * 26 + 16
        rounded_rect(c, mx, y - top4_h, W - 2 * mx, top4_h,
                     r=RADIUS, fill=colors.white, stroke=BORDER)
        text(c, mx + CARD_PAD, y - 22, t["capability_maturity_top4"],
             size=11, bold=True)

        yy = y - 48
        for i, r in enumerate(top4, start=1):
            skill = str(r.get("skill", "-"))
            score = float(r.get("score_percent", 0.0))
            sc    = score_color(score)

            wrap(c, mx + CARD_PAD, yy, f"{i}. {skill}",
                 max_w=content_w * 0.45, size=10, color=TEXT, leading=11)

            # Score % right-aligned
            c.setFillColor(sc)
            c.setFont("Helvetica-Bold", 9)
            c.drawRightString(W - mx - CARD_PAD, yy, f"{score:.0f}%")

            # Bar spanning middle of the card
            bar_left  = mx + content_w * 0.50
            bar_right = W - mx - CARD_PAD - 36
            draw_scale_bar(c, bar_left, yy + 2, bar_right - bar_left,
                           score, fill_color=sc, show_ticks=False)
            yy -= 26

        y -= (top4_h + 18)

    # ── Table header ──────────────────────────────────────────────────────
    header_h = 30
    rounded_rect(c, mx, y - header_h, W - 2 * mx, header_h,
                 r=10, fill=colors.HexColor("#F8FAFC"), stroke=BORDER)
    text(c, col_skill, y - 18, t["col_capability"],    size=9, color=MUTED, bold=True)
    text(c, col_score, y - 18, t["col_score"],         size=9, color=MUTED, bold=True)
    text(c, col_prio,  y - 18, t["col_gap_priority"],  size=9, color=MUTED, bold=True)
    text(c, col_risk,  y - 18, t["col_business_risk"], size=9, color=MUTED, bold=True)
    y -= 42

    # ── Table rows ────────────────────────────────────────────────────────
    min_row_h  = 56   # enough for score text + bar (8pt) + gap + badge
    row_pad_y  = 10
    row_gap    = 6
    current_pg = page

    for r in breakdown[:9]:
        skill    = str(r.get("skill", "-"))
        score    = float(r.get("score_percent", 0.0))
        prio_val = float(r.get("priority", 0.0))
        risk     = str(r.get("risk", "")).strip()
        if len(risk) > 220:
            risk = risk[:217].rstrip() + "..."

        sc         = score_color(score)
        prio_label = gap_priority_label(prio_val)

        # Measure heights
        skill_h = min(
            measure_paragraph(skill, col_score - col_skill - 8,
                               font_size=10, leading=11),
            22,
        )
        risk_h = measure_paragraph(risk, risk_w, font_size=9, leading=10)

        # Row height: must fit score text (12) + bar (8) + ticks space (4) + badge (18)
        content_h = max(skill_h, risk_h, 12 + 8 + 4 + 4 + 18)
        row_h     = max(min_row_h, content_h + 2 * row_pad_y)

        # ── Page break if needed ──────────────────────────────────────────
        if y - row_h < _MARGIN_BOTTOM + 10:
            footer(c, current_pg, mx)
            c.showPage()
            current_pg += 1
            topbar(c)
            y = top

        rounded_rect(c, mx, y - row_h, W - 2 * mx, row_h,
                     r=10, fill=colors.white, stroke=BORDER)

        text_top = y - row_pad_y

        # ── Skill name ───────────────────────────────────────────────────
        draw_paragraph(c, col_skill, text_top, skill,
                       width=col_score - col_skill - 8,
                       font_size=10, leading=11, color=TEXT)

        # ── Score % ──────────────────────────────────────────────────────
        c.setFillColor(sc)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(col_score, text_top - 2, f"{score:.0f}%")

        # ── Progress bar — directly below score text, same x ─────────────
        # bar_y_top = top-of-bar = just below score text
        bar_y_top = text_top - 18   # 16pt below score baseline
        draw_scale_bar(c, col_bar, bar_y_top, _BAR_W,
                       score, fill_color=sc, show_ticks=False)

        # ── Gap priority badge — vertically centered in row ───────────────
        badge_y = (y - row_h) + (row_h - 18) / 2
        priority_badge(c, col_prio, badge_y, prio_label)

        # ── Business risk — top-aligned with skill name ───────────────────
        draw_paragraph(c, col_risk, text_top, risk,
                       width=risk_w, font_size=9, leading=10, color=MUTED)

        y -= (row_h + row_gap)

    footer(c, current_pg, mx)