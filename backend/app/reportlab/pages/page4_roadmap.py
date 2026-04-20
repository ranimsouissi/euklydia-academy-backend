# backend/app/reportlab/pages/page4_roadmap.py
from __future__ import annotations
from typing import Dict, Any, List
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors

from app.reportlab.theme import MUTED, CARD_GAP, EU_DARK, BORDER
from app.reportlab.translations import get_t
from app.reportlab.components import (
    topbar, text, rounded_rect, phase_card, footer,
)

_PHASE_COLORS = [
    colors.HexColor("#0F6E56"),
    colors.HexColor("#1D9E75"),
    colors.HexColor("#5DCAA5"),
]
_PHASE_LIGHT = [colors.HexColor("#E1F5EE")] * 3
_LINE_COLOR  = colors.HexColor("#CBD5E1")
_WHITE       = colors.white
_MARGIN_BOTTOM = 18 * mm


def _estimate_phase_card_h(objective, actions, metrics, w):
    from app.reportlab.components import measure_paragraph
    pad = 14
    inner_w = w - 2 * pad
    obj_h = measure_paragraph(objective or "-", inner_w, font_size=10, leading=12)
    act_h = sum(
        measure_paragraph(f"- {a}", inner_w - 4, font_size=10, leading=12)
        for a in [str(a).strip() for a in (actions or []) if str(a).strip()][:3]
    )
    met_h = sum(
        measure_paragraph(f"- {m}", inner_w - 4, font_size=10, leading=12)
        for m in [str(m).strip() for m in (metrics or []) if str(m).strip()][:2]
    )
    return max(180, 38 + 18 + (11 + obj_h) + 12 + (11 + act_h) + 10 + (11 + met_h) + 16 + 32 + 14)


def _draw_timeline(c, mx, y_top, page_w, phases, phase_labels):
    TL_H = 72
    R    = 14
    content_w = page_w - 2 * mx
    n = min(len(phases), 3)
    if n == 0:
        return 0

    if n == 1:
        positions = [mx + content_w / 2]
    elif n == 2:
        positions = [mx + content_w * 0.25, mx + content_w * 0.75]
    else:
        positions = [mx + content_w * 0.17,
                     mx + content_w * 0.50,
                     mx + content_w * 0.83]

    cy = y_top - TL_H / 2 + 10

    if n > 1:
        c.setStrokeColor(_LINE_COLOR)
        c.setLineWidth(2)
        c.line(positions[0] + R, cy, positions[-1] - R, cy)

    for i, ph in enumerate(phases[:n]):
        px    = positions[i]
        col   = _PHASE_COLORS[i]
        label = phase_labels[i] if i < len(phase_labels) else ""
        skill = str(ph.get("focus_skill", ""))

        c.setFillColor(_PHASE_LIGHT[i])
        c.circle(px, cy, R + 4, fill=1, stroke=0)
        c.setFillColor(col)
        c.circle(px, cy, R, fill=1, stroke=0)
        c.setFillColor(_WHITE)
        c.setFont("Helvetica-Bold", 11)
        nw = c.stringWidth(str(i + 1), "Helvetica-Bold", 11)
        c.drawString(px - nw / 2, cy - 4, str(i + 1))

        c.setFillColor(col)
        c.setFont("Helvetica-Bold", 8)
        lw = c.stringWidth(label, "Helvetica-Bold", 8)
        c.drawString(px - lw / 2, cy - R - 16, label)

        max_chars = 28
        sd = skill if len(skill) <= max_chars else skill[:max_chars - 1] + "..."
        c.setFillColor(colors.HexColor("#64748B"))
        c.setFont("Helvetica", 7)
        sw = c.stringWidth(sd, "Helvetica", 7)
        c.drawString(px - sw / 2, cy - R - 28, sd)

    return TL_H + 8


def draw(c: canvas.Canvas, payload: Dict[str, Any], page: int, mx: float, top: float):
    W, _ = A4
    topbar(c)
    t = get_t(payload.get("language", "en"))

    roadmap: List[Dict[str, Any]] = payload.get("roadmap_90_days", [])
    phase_labels = t["phase_labels"]

    y = top
    text(c, mx, y, t["roadmap_title"], size=16, bold=True)
    text(c, mx, y - 16, t["roadmap_sub"], size=9, color=MUTED)
    y -= 36

    if roadmap:
        tl_h = 80
        rounded_rect(c, mx, y - tl_h, W - 2 * mx, tl_h,
                     r=8, fill=colors.HexColor("#F8FAFC"),
                     stroke=colors.HexColor("#E2E8F0"))
        _draw_timeline(c, mx, y - 4, W, roadmap, phase_labels)
        y -= (tl_h + 14)

    llm    = payload.get("llm_narrative") or {}
    llm_rm = llm.get("roadmap") or {}
    current_page = page
    card_w = W - 2 * mx

    for idx, ph in enumerate(roadmap):
        phase_label_raw = str(ph.get("phase", ""))

        if "0-30" in phase_label_raw or "\u201330" in phase_label_raw:
            key = "phase_1"
            display_label = phase_labels[0] if phase_labels else phase_label_raw
        elif "30-60" in phase_label_raw or "30\u201360" in phase_label_raw:
            key = "phase_2"
            display_label = phase_labels[1] if len(phase_labels) > 1 else phase_label_raw
        else:
            key = "phase_3"
            display_label = phase_labels[2] if len(phase_labels) > 2 else phase_label_raw

        llm_phase = llm_rm.get(key) or {}
        focus     = llm_phase.get("focus")          or ph.get("focus_skill", "")
        objective = llm_phase.get("objective")       or ph.get("objective", "")
        impact    = llm_phase.get("expected_impact") or ph.get("expected_impact", "")
        actions   = llm_phase.get("key_actions")     or []
        metrics   = llm_phase.get("success_metrics") or []

        # Build translated phase label e.g. "Phase 1 (0-30 days)"
        translated_label = f"Phase {idx + 1} ({display_label})"

        estimated_h = _estimate_phase_card_h(objective, actions, metrics, card_w)

        if y - estimated_h < _MARGIN_BOTTOM + 10:
            footer(c, current_page, mx)
            c.showPage()
            current_page += 1
            topbar(c)
            y = top

        h_used = phase_card(
            c, mx, y, card_w,
            translated_label,
            str(focus), str(objective),
            [str(a) for a in actions],
            [str(m) for m in metrics],
            str(impact),
            phase_index=idx,
            t=t,    # ← translations
        )
        y -= (h_used + CARD_GAP)

    footer(c, current_page, mx)