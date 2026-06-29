# app/api/v1/endpoints/modules.py
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy import text

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.module import Module
from app.models.user import User
from app.models.user_module_progress import UserModuleProgress
from app.schemas.module import ModuleRead
from app.services import mastery_service

router = APIRouter()

VALID_SECTIONS = {
    "use_case", "kpi", "execution_content",
    "execution_task", "kpi_measurement", "progress_update"
}

INITIAL_SECTION_PROGRESS = {
    "use_case":          "not_started",
    "kpi":               "not_started",
    "execution_content": "not_started",
    "execution_task":    "not_started",
    "kpi_measurement":   "not_started",
    "progress_update":   "not_started",
}

ALL_COMPLETED = {k: "completed" for k in VALID_SECTIONS}


# ----------------------------------------------------------------
# GET /modules/ — Liste des modules actifs
# ----------------------------------------------------------------

@router.get("/", response_model=list[ModuleRead])
def read_modules(
    db:    Session = Depends(get_db),
    skip:  int     = Query(default=0, ge=0),
    limit: int     = Query(default=100, ge=1, le=200),
) -> list[Module]:
    return (
        db.query(Module)
        .filter(Module.is_active.is_(True))
        .order_by(Module.display_order.asc(), Module.id.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )


# ----------------------------------------------------------------
# GET /modules/{module_id} — Détail d'un module
# ----------------------------------------------------------------

@router.get("/{module_id}", response_model=ModuleRead)
def read_module(
    module_id:    int,
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user),
) -> Module:
    module = (
        db.query(Module)
        .filter(Module.id == module_id, Module.is_active.is_(True))
        .first()
    )
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    progress = (
        db.query(UserModuleProgress)
        .filter(
            UserModuleProgress.user_id == current_user.id,
            UserModuleProgress.module_id == module_id,
        )
        .first()
    )

    # ── Statut + progression ─────────────────────────────────
    status_value     = progress.status           if progress else "not_started"
    progress_value   = progress.progress_percent if progress else 0
    module.status           = status_value
    module.progress_percent = progress_value
    module.module_status    = status_value          # alias frontend

    # ── Section progress ─────────────────────────────────────
    if progress and progress.section_progress:
        module.section_progress = progress.section_progress

    # ── Skill mastery du skill principal du module ───────────
    mastery_row = db.execute(text(
        "SELECT s.name AS skill_name, "
        "lsm.mastery_score, lsm.mastery_level, "
        "lsm.last_update_reason "
        "FROM module_skills ms "
        "JOIN skills s ON s.id = ms.skill_id "
        "LEFT JOIN learner_skill_mastery lsm "
        "  ON lsm.skill_id = ms.skill_id "
        "  AND lsm.user_id = :user_id "
        "WHERE ms.module_id = :module_id "
        "LIMIT 1"
    ), {"user_id": current_user.id, "module_id": module_id}).fetchone()

    if mastery_row:
        module.skill_mastery = {
            "skill_name":         mastery_row.skill_name,
            "mastery_score":      float(mastery_row.mastery_score) if mastery_row.mastery_score is not None else 0.0,
            "mastery_level":      mastery_row.mastery_level or "novice",
            "last_update_reason": mastery_row.last_update_reason,
        }

    return module


# ----------------------------------------------------------------
# POST /modules/{module_id}/start — Démarrer un module
# ----------------------------------------------------------------

@router.post("/{module_id}/start")
def start_module(
    module_id:    int,
    current_user: User    = Depends(get_current_user),
    db:           Session = Depends(get_db),
):
    module = (
        db.query(Module)
        .filter(Module.id == module_id, Module.is_active.is_(True))
        .first()
    )
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    progress = (
        db.query(UserModuleProgress)
        .filter(
            UserModuleProgress.user_id == current_user.id,
            UserModuleProgress.module_id == module_id,
        )
        .first()
    )

    now = datetime.utcnow()

    if not progress:
        progress = UserModuleProgress(
            user_id=current_user.id,
            module_id=module_id,
            status="in_progress",
            started_at=now,
            progress_percent=0,
            section_progress=dict(INITIAL_SECTION_PROGRESS),
        )
        db.add(progress)
    else:
        if progress.status != "completed":
            progress.status = "in_progress"
            if not progress.started_at:
                progress.started_at = now
            if not progress.section_progress:
                progress.section_progress = dict(INITIAL_SECTION_PROGRESS)
                flag_modified(progress, "section_progress")
            progress.updated_at = now

    db.commit()
    db.refresh(progress)

    return {
        "message":          "Module started",
        "module_id":        module_id,
        "status":           progress.status,
        "progress_percent": progress.progress_percent,
        "section_progress": progress.section_progress,
        "started_at":       progress.started_at,
        "completed_at":     progress.completed_at,
    }


# ----------------------------------------------------------------
# POST /modules/{module_id}/section/{section_type} — Avancer dans une section
# ----------------------------------------------------------------

@router.post("/{module_id}/section/{section_type}")
def update_section_progress(
    module_id:    int,
    section_type: str,
    payload:      dict,
    current_user: User    = Depends(get_current_user),
    db:           Session = Depends(get_db),
):
    """
    Met à jour la progression d'une section spécifique.
    payload: { "status": "in_progress" | "completed" }
    """
    if section_type not in VALID_SECTIONS:
        raise HTTPException(
            status_code=400,
            detail=f"section_type invalide. Valeurs acceptées : {VALID_SECTIONS}"
        )

    status = payload.get("status", "in_progress")
    if status not in ("in_progress", "completed"):
        raise HTTPException(
            status_code=400,
            detail="status doit être 'in_progress' ou 'completed'"
        )

    progress = (
        db.query(UserModuleProgress)
        .filter(
            UserModuleProgress.user_id == current_user.id,
            UserModuleProgress.module_id == module_id,
        )
        .first()
    )

    if not progress:
        raise HTTPException(
            status_code=404,
            detail="Module non démarré — appelez /start d'abord"
        )

    # ── Mettre à jour section_progress ───────────────────────
    current_sections = dict(progress.section_progress or {})
    current_sections[section_type] = status
    progress.section_progress = current_sections
    flag_modified(progress, "section_progress")

    # ── Enregistrer le timestamp d'ouverture de la section ───
    now = datetime.utcnow()
    current_opened = dict(progress.section_opened_at or {})
    if section_type not in current_opened:
        current_opened[section_type] = now.isoformat()
        progress.section_opened_at = current_opened
        flag_modified(progress, "section_opened_at")

    # ── Recalculer progress_percent ──────────────────────────
    total     = len(VALID_SECTIONS)
    completed = sum(1 for s in current_sections.values() if s == "completed")
    progress.progress_percent = round((completed / total) * 100)
    progress.updated_at = now

    db.commit()
    db.refresh(progress)

    return {
        "module_id":        module_id,
        "section_type":     section_type,
        "status":           status,
        "section_progress": progress.section_progress,
        "progress_percent": progress.progress_percent,
        "section_opened_at": progress.section_opened_at,
    }

# ----------------------------------------------------------------
# POST /modules/{module_id}/execution-task/submit
# ----------------------------------------------------------------

@router.post("/{module_id}/execution-task/submit")
def submit_execution_task(
    module_id:    int,
    payload:      dict,
    current_user: User    = Depends(get_current_user),
    db:           Session = Depends(get_db),
):
    """
    Soumet l'Execution Task d'un module.
    payload: { "url": str, "kpi_after": str, "difficulty": str (optionnel) }
    """
    url        = payload.get("url")
    kpi_after  = payload.get("kpi_after")
    difficulty = payload.get("difficulty")

    if not url:
        raise HTTPException(status_code=400, detail="url du livrable obligatoire")
    if not kpi_after:
        raise HTTPException(
            status_code=400,
            detail="kpi_after obligatoire pour valider la soumission"
        )

    progress = (
        db.query(UserModuleProgress)
        .filter(
            UserModuleProgress.user_id == current_user.id,
            UserModuleProgress.module_id == module_id,
        )
        .first()
    )

    if not progress:
        raise HTTPException(
            status_code=404,
            detail="Module non démarré — appelez /start d'abord"
        )

    now = datetime.utcnow()

    # ── Mettre à jour la soumission ──────────────────────────
    progress.execution_task_submitted    = True
    progress.execution_task_url          = url
    progress.kpi_after                   = kpi_after
    progress.execution_task_difficulty   = difficulty
    progress.execution_task_submitted_at = now
    progress.updated_at                  = now

    # ── Marquer execution_task comme completed ───────────────
    current_sections = dict(progress.section_progress or {})
    current_sections["execution_task"] = "completed"
    progress.section_progress = current_sections
    flag_modified(progress, "section_progress")

    # ── Recalculer progress_percent ──────────────────────────
    total     = len(VALID_SECTIONS)
    completed = sum(1 for s in current_sections.values() if s == "completed")
    progress.progress_percent = round((completed / total) * 100)

    db.commit()
    db.refresh(progress)

    # ── Mettre à jour la mastery ─────────────────────────────
    mastery_result = None
    try:
        module = db.query(Module).filter(Module.id == module_id).first()
        kpi_before = module.kpi_before_fr if module else None

        mastery_result = mastery_service.update_mastery_from_execution_task(
            db=db,
            user_id=current_user.id,
            module_id=module_id,
            kpi_before=kpi_before,
            kpi_after=kpi_after,
            execution_task_submitted=True,
            difficulty=difficulty,
            reason=f"execution_task_submitted module_id={module_id}"
        )
    except Exception:
        pass
    return {
        "message":          "Execution Task soumise avec succès",
        "module_id":        module_id,
        "execution_task":   {
            "submitted":    True,
            "url":          url,
            "kpi_after":    kpi_after,
            "difficulty":   difficulty,
            "submitted_at": now,
        },
        "progress_percent": progress.progress_percent,
        "section_progress": progress.section_progress,
        "mastery_update":   mastery_result,
    }


# ----------------------------------------------------------------
# POST /modules/{module_id}/complete — Compléter un module
# ----------------------------------------------------------------

@router.post("/{module_id}/complete")
def complete_module(
    module_id:    int,
    current_user: User    = Depends(get_current_user),
    db:           Session = Depends(get_db),
):
    module = (
        db.query(Module)
        .filter(Module.id == module_id, Module.is_active.is_(True))
        .first()
    )
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    progress = (
        db.query(UserModuleProgress)
        .filter(
            UserModuleProgress.user_id == current_user.id,
            UserModuleProgress.module_id == module_id,
        )
        .first()
    )

    now = datetime.utcnow()

    if not progress:
        progress = UserModuleProgress(
            user_id=current_user.id,
            module_id=module_id,
            status="completed",
            started_at=now,
            completed_at=now,
            progress_percent=100,
            section_progress=dict(ALL_COMPLETED),
        )
        db.add(progress)
    else:
        progress.status           = "completed"
        progress.progress_percent = 100
        progress.completed_at     = now
        progress.updated_at       = now
        if not progress.started_at:
            progress.started_at = now
        progress.section_progress = dict(ALL_COMPLETED)
        flag_modified(progress, "section_progress")

    db.commit()
    db.refresh(progress)

    # ── Mastery update post-complétion ───────────────────────
    mastery_result = None
    try:
        kpi_before = module.kpi_before_fr if module else None

        mastery_result = mastery_service.update_mastery_from_execution_task(
            db=db,
            user_id=current_user.id,
            module_id=module_id,
            kpi_before=kpi_before,
            kpi_after=progress.kpi_after,
            execution_task_submitted=progress.execution_task_submitted or False,
            difficulty=progress.execution_task_difficulty,
            reason=f"module_completed module_id={module_id}"
        )
    except Exception:
        pass

    return {
        "message":          "Module completed",
        "module_id":        module_id,
        "status":           progress.status,
        "progress_percent": progress.progress_percent,
        "section_progress": progress.section_progress,
        "started_at":       progress.started_at,
        "completed_at":     progress.completed_at,
        "mastery_update":   mastery_result,
    }