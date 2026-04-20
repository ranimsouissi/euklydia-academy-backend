from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import FileResponse
from pathlib import Path

from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.services.executive_report import generate_executive_report_payload
from app.services.report_storage import save_type_a_report
from app.models.report import Report
from fastapi import Query

router = APIRouter(prefix="/brochure", tags=["Brochure"])


@router.post("/executive-report/{user_id}/generate-and-store")
def generate_and_store_report(
    user_id: int,
    lang: str = Query("en"), # ← ajouter
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # ✅ user can only generate their own report (recommended)
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    try:
        language = lang if lang in ("en", "fr") else "en"
        payload = generate_executive_report_payload(db, user_id, language=language)
        report = save_type_a_report(db, payload)
        return {
            "report_id": report.id,
            "user_id": report.user_id,
            "report_type": report.report_type,
            "version": report.version,
            "global_score_percent": report.global_score_percent,
            "maturity_level": report.maturity_level,
            "created_at": report.created_at,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {e}")


@router.get("/reports/{user_id}")
def list_reports(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    reports = (
        db.query(Report)
        .filter(Report.user_id == user_id)
        .order_by(Report.created_at.desc())
        .all()
    )

    return [
        {
            "report_id": r.id,
            "report_type": r.report_type,
            "version": r.version,
            "global_score_percent": r.global_score_percent,
            "maturity_level": r.maturity_level,
            "created_at": r.created_at,
        }
        for r in reports
    ]


@router.get("/reports/download/{report_id}")
def download_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    r = db.query(Report).filter(Report.id == report_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Report not found")

    # ✅ ownership check
    if r.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    # ✅ file exists check
    p = Path(r.file_path)
    if not p.exists():
        raise HTTPException(status_code=404, detail="Report file missing on storage")

    return FileResponse(
        path=str(p),
        media_type="application/pdf",
        filename=f"euklydia_report_{report_id}.pdf",
    )


@router.get("/executive-report/{user_id}")
def preview_report_json(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    try:
        payload = generate_executive_report_payload(db, user_id)
        return payload
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))