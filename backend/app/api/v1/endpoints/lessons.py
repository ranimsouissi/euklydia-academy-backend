from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.activity import Activity
from app.models.learner_activity_log import LearnerActivityLog
from app.models.lesson import Lesson
from app.models.unit import Unit
from app.models.user import User
from app.models.user_module_progress import UserModuleProgress

router = APIRouter()


# ─────────────────────────────────────────────────────────────────────────────
# GET /api/v1/lessons/{lesson_id}
# Retourne une leçon avec ses activités
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/{lesson_id}")
def read_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    lesson = (
        db.query(Lesson)
        .filter(Lesson.id == lesson_id, Lesson.is_active.is_(True))
        .first()
    )
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    activities = (
        db.query(Activity)
        .filter(Activity.lesson_id == lesson_id, Activity.is_active.is_(True))
        .order_by(Activity.order.asc())
        .all()
    )

    logs = (
        db.query(LearnerActivityLog)
        .filter(
            LearnerActivityLog.user_id == current_user.id,
            LearnerActivityLog.lesson_id == lesson_id,
        )
        .all()
    )
    logs_by_activity = {log.activity_id: log for log in logs}

    return {
        "id": lesson.id,
        "unit_id": lesson.unit_id,
        "title_fr": lesson.title_fr,
        "title_en": lesson.title_en,
        "description_fr": lesson.description_fr,
        "description_en": lesson.description_en,
        "format": lesson.format,
        "difficulty_level": lesson.difficulty_level,
        "estimated_duration_min": lesson.estimated_duration_min,
        "prerequisite_lesson_id": lesson.prerequisite_lesson_id,
        "video_url_fr": lesson.video_url_fr,
        "video_url_en": lesson.video_url_en,
        "activities": [
            {
                "id": act.id,
                "order": act.order,
                "type": act.type,
                "title_fr": act.title_fr,
                "title_en": act.title_en,
                "content_fr": act.content_fr,
                "content_en": act.content_en,
                "is_assessed": act.is_assessed,
                "is_required": act.is_required,
                "has_hints": act.has_hints,
                "hints_fr": act.hints_fr,
                "hints_en": act.hints_en,
                "rubric_fr": act.rubric_fr,
                "rubric_en": act.rubric_en,
                "passing_score": act.passing_score,
                "learner_status": logs_by_activity.get(act.id, None) and logs_by_activity[act.id].status,
                "learner_score": logs_by_activity.get(act.id, None) and logs_by_activity[act.id].score,
                "attempts": logs_by_activity[act.id].attempts if act.id in logs_by_activity else 0,
            }
            for act in activities
        ],
    }


# ─────────────────────────────────────────────────────────────────────────────
# POST /api/v1/lessons/{lesson_id}/complete
# Marque une leçon comme complétée et met à jour la progression du module
# ─────────────────────────────────────────────────────────────────────────────

@router.post("/{lesson_id}/complete")
def complete_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    lesson = db.query(Lesson).filter(
        Lesson.id == lesson_id,
        Lesson.is_active.is_(True),
    ).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    now = datetime.utcnow()

    # ── 1. Marquer toutes les activités de la leçon comme complétées ─────────
    activities = db.query(Activity).filter(
        Activity.lesson_id == lesson_id,
        Activity.is_active.is_(True),
    ).all()

    for act in activities:
        log = db.query(LearnerActivityLog).filter(
            LearnerActivityLog.user_id == current_user.id,
            LearnerActivityLog.activity_id == act.id,
        ).first()
        if not log:
            log = LearnerActivityLog(
                user_id=current_user.id,
                activity_id=act.id,
                lesson_id=lesson_id,
                status="completed",
                attempts=1,
                started_at=now,
                completed_at=now,
                created_at=now,
            )
            db.add(log)
        elif log.status != "completed":
            log.status = "completed"
            log.completed_at = now

    db.commit()

    # ── 2. Vérifier si toutes les leçons de l'unité sont complétées ──────────
    unit_lessons = db.query(Lesson).filter(
        Lesson.unit_id == lesson.unit_id,
        Lesson.is_active.is_(True),
    ).all()
    unit_lesson_ids = [l.id for l in unit_lessons]

    completed_unit_lesson_ids = db.execute(
        select(LearnerActivityLog.lesson_id)
        .where(LearnerActivityLog.user_id == current_user.id)
        .where(LearnerActivityLog.lesson_id.in_(unit_lesson_ids))
        .where(LearnerActivityLog.status == "completed")
        .distinct()
    ).scalars().all()

    unit_completed = len(set(completed_unit_lesson_ids)) >= len(unit_lesson_ids)

    # ── 3. Mettre à jour la progression du module ─────────────────────────────
    unit = db.query(Unit).filter(Unit.id == lesson.unit_id).first()
    if unit:
        # Toutes les leçons de toutes les unités du module
        all_units = db.query(Unit).filter(
            Unit.module_id == unit.module_id,
            Unit.is_active.is_(True),
        ).all()

        all_module_lesson_ids = []
        for u in all_units:
            u_lessons = db.query(Lesson).filter(
                Lesson.unit_id == u.id,
                Lesson.is_active.is_(True),
            ).all()
            all_module_lesson_ids.extend([l.id for l in u_lessons])

        # Leçons complétées du module
        completed_module_lesson_ids = db.execute(
            select(LearnerActivityLog.lesson_id)
            .where(LearnerActivityLog.user_id == current_user.id)
            .where(LearnerActivityLog.lesson_id.in_(all_module_lesson_ids))
            .where(LearnerActivityLog.status == "completed")
            .distinct()
        ).scalars().all()

        total = len(all_module_lesson_ids)
        completed = len(set(completed_module_lesson_ids))
        progress_percent = round((completed / total) * 100) if total > 0 else 0

        # Créer ou mettre à jour user_module_progress
        module_progress = db.query(UserModuleProgress).filter(
            UserModuleProgress.user_id == current_user.id,
            UserModuleProgress.module_id == unit.module_id,
        ).first()

        if not module_progress:
            module_progress = UserModuleProgress(
                user_id=current_user.id,
                module_id=unit.module_id,
                status="in_progress",
                progress_percent=progress_percent,
                started_at=now,
                created_at=now,
                updated_at=now,
            )
            db.add(module_progress)
        else:
            module_progress.progress_percent = progress_percent
            module_progress.updated_at = now
            if progress_percent == 100:
                module_progress.status = "completed"
                module_progress.completed_at = now
            elif module_progress.status == "not_started":
                module_progress.status = "in_progress"
                module_progress.started_at = now

        db.commit()

    return {
        "lesson_id": lesson_id,
        "status": "completed",
        "unit_id": lesson.unit_id,
        "unit_completed": unit_completed,
        "progress_percent": progress_percent if unit else 0,
    }