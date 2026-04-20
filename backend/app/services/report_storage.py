from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from sqlalchemy.orm import Session

from app.models.report import Report
from app.services.brochure_pdf_reportlab import generate_brochure_pdf_bytes_reportlab


def save_type_a_report(db: Session, payload: Dict[str, Any]) -> Report:
    """
    Generate Type A PDF, save to storage, create Report row.
    """

    user_id = payload["leader"]["id"]
    version = payload.get("meta", {}).get("version", "type_a_v1")

    # 1️⃣ Generate PDF bytes
    pdf_bytes = generate_brochure_pdf_bytes_reportlab(payload)

    # 2️⃣ Prepare storage folder
    base_dir = Path(__file__).resolve().parents[2]
    storage_dir = base_dir / "storage" / "reports"
    storage_dir.mkdir(parents=True, exist_ok=True)

    # 3️⃣ Create filename
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"type_a_user_{user_id}_{timestamp}.pdf"
    file_path = storage_dir / filename

    # 4️⃣ Save file
    file_path.write_bytes(pdf_bytes)

    # 5️⃣ Create DB record
    assessment = payload["assessment"]

    report = Report(
        user_id=user_id,
        report_type="type_a",
        version=version,
        global_score_percent=float(assessment.get("global_score_percent", 0.0)),
        maturity_level=str(assessment.get("maturity_level", "Unknown")),
        file_path=str(file_path),
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    return report