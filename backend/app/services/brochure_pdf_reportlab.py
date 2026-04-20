# backend/app/services/brochure_pdf_reportlab.py
from __future__ import annotations

from typing import Dict, Any
from app.reportlab.build_report import generate_pdf


def generate_brochure_pdf_bytes_reportlab(payload: Dict[str, Any]) -> bytes:
    return generate_pdf(payload)