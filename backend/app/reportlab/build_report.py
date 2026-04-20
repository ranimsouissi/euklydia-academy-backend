# backend/app/reportlab/build_report.py
from __future__ import annotations

from io import BytesIO
from typing import Dict, Any

from reportlab.pdfgen import canvas

from app.reportlab.layout import PAGE_SIZE, W, H, MARGIN_X, TOP_Y
from app.reportlab.pages.page1_summary import draw as draw_page1
from app.reportlab.pages.page2_insights import draw as draw_page2
from app.reportlab.pages.page3_breakdown import draw as draw_page3
from app.reportlab.pages.page4_roadmap import draw as draw_page4
from app.reportlab.pages.page5_cycle import draw as draw_page5


def generate_pdf(payload: Dict[str, Any]) -> bytes:
    print("✅ NEW REPORTLAB PIPELINE: app.reportlab.build_report.generate_pdf")
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=PAGE_SIZE)

    mx  = MARGIN_X
    top = TOP_Y

    draw_page1(c, payload, page=1, mx=mx, top=top)
    c.showPage()

    draw_page2(c, payload, page=2, mx=mx, top=top)
    c.showPage()

    draw_page3(c, payload, page=3, mx=mx, top=top)
    c.showPage()

    draw_page4(c, payload, page=4, mx=mx, top=top)
    c.showPage()                                    # ← ajouter
    draw_page5(c, payload, page=5, mx=mx, top=top)  # ← ajouter

    c.save()
    pdf_bytes = buf.getvalue()
    buf.close()
    return pdf_bytes