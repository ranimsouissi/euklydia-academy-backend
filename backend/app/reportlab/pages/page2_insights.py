# backend/app/reportlab/pages/page2_insights.py
from __future__ import annotations
from typing import Dict, Any, List
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

from app.reportlab.theme import BORDER, MUTED, CARD_PAD, RADIUS, CARD_GAP
from app.reportlab.translations import get_t
from app.reportlab.components import (
    topbar, section_title, rounded_rect, text, wrap, insight_card, footer,
)


def draw(c: canvas.Canvas, payload: Dict[str, Any], page: int, mx: float, top: float):
    W, _ = A4
    topbar(c)
    t = get_t(payload.get("language", "en"))

    assessment = payload["assessment"]
    breakdown: List[Dict[str, Any]] = assessment.get("skill_breakdown", [])
    llm = payload.get("llm_narrative") or {}
    insights = llm.get("capability_insights") or []

    y = section_title(c, mx, top,
                      t["capability_insights"],
                      t["capability_insights_sub"])

    if not insights:
        rounded_rect(c, mx, y - 74, W - 2 * mx, 74, r=RADIUS, fill=colors.white, stroke=BORDER)
        text(c, mx + CARD_PAD, y - 24, t["no_insights"], size=11, bold=True)
        wrap(c, mx + CARD_PAD, y - 42,
             t["no_insights_sub"],
             max_w=W - 2 * mx - 2 * CARD_PAD, size=10, color=MUTED)
        footer(c, page, mx)
        return

    score_map = {str(r.get("skill", "")): float(r.get("score_percent", 0.0))
                 for r in breakdown}
    card_w = W - 2 * mx

    for i, it in enumerate(insights[:2]):
        title    = str(it.get("skill", f"Gap {i+1}"))
        why      = str(it.get("why_it_matters", ""))
        risk     = str(it.get("risk", ""))
        leverage = str(it.get("business_leverage", ""))
        quick    = str(it.get("quick_win", ""))

        h_used = insight_card(
            c, mx, y, card_w, title,
            score_map.get(title),
            why, risk, leverage, quick,
            t=t,          # ← pass translations
        )
        y -= (h_used + CARD_GAP)

    footer(c, page, mx)