# backend/app/reportlab/layout.py
from __future__ import annotations

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

PAGE_SIZE = A4
W, H = A4

MARGIN_X = 18 * mm
MARGIN_TOP = 18 * mm
MARGIN_BOTTOM = 18 * mm

TOP_Y = H - MARGIN_TOP
CONTENT_W = W - 2 * MARGIN_X