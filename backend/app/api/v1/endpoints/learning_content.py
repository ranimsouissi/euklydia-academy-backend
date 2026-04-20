from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.activity import Activity
from app.models.learner_activity_log import LearnerActivityLog
from app.models.lesson import Lesson
from app.models.module import Module
from app.models.unit import Unit
from app.models.user import User
from app.models.user_module_progress import UserModuleProgress
from app.schemas.learning_content import (
    ActivityRead,
    LessonRead,
    UnitRead,
    UnitReadWithLessons,
)

router = APIRouter()


# ─────────────────────────────────────────────────────────────────────────────
# UNITS
# ─────────────────────────────────────────────────────────────────────────────

@router.get(
    "/modules/{module_id}/units",
    response_model=list[UnitRead],
    summary="Lister les unités d'un module",
)
def read_units(
    module_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Unit]:
    module = db.query(Module).filter(
        Module.id == module_id,
        Module.is_active.is_(True),
    ).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    units = (
        db.query(Unit)
        .filter(Unit.module_id == module_id, Unit.is_active.is_(True))
        .options(joinedload(Unit.lessons))
        .order_by(Unit.order.asc())
        .all()
    )
    return units


@router.get(
    "/units/{unit_id}",
    response_model=UnitReadWithLessons,
    summary="Détail d'une unité avec ses leçons et activités",
)
def read_unit(
    unit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Unit:
    unit = (
        db.query(Unit)
        .filter(Unit.id == unit_id, Unit.is_active.is_(True))
        .options(
            joinedload(Unit.lessons).joinedload(Lesson.activities)
        )
        .first()
    )
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    return unit


# ─────────────────────────────────────────────────────────────────────────────
# LESSONS
# ─────────────────────────────────────────────────────────────────────────────

@router.get(
    "/units/{unit_id}/lessons",
    response_model=list[LessonRead],
    summary="Lister les leçons d'une unité",
)
def read_lessons(
    unit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Lesson]:
    unit = db.query(Unit).filter(
        Unit.id == unit_id,
        Unit.is_active.is_(True),
    ).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    lessons = (
        db.query(Lesson)
        .filter(Lesson.unit_id == unit_id, Lesson.is_active.is_(True))
        .options(joinedload(Lesson.activities))
        .order_by(Lesson.order.asc())
        .all()
    )
    return lessons


@router.get(
    "/lessons/{lesson_id}",
    response_model=LessonRead,
    summary="Détail d'une leçon avec ses activités",
)
def read_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Lesson:
    lesson = (
        db.query(Lesson)
        .filter(Lesson.id == lesson_id, Lesson.is_active.is_(True))
        .options(joinedload(Lesson.activities))
        .first()
    )
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


# ─────────────────────────────────────────────────────────────────────────────
# ACTIVITIES
# ─────────────────────────────────────────────────────────────────────────────

@router.get(
    "/lessons/{lesson_id}/activities",
    response_model=list[ActivityRead],
    summary="Lister les activités d'une leçon",
)
def read_activities(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Activity]:
    lesson = db.query(Lesson).filter(
        Lesson.id == lesson_id,
        Lesson.is_active.is_(True),
    ).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    activities = (
        db.query(Activity)
        .filter(Activity.lesson_id == lesson_id, Activity.is_active.is_(True))
        .order_by(Activity.order.asc())
        .all()
    )
    return activities


@router.get(
    "/activities/{activity_id}",
    response_model=ActivityRead,
    summary="Détail d'une activité",
)
def read_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Activity:
    activity = (
        db.query(Activity)
        .filter(Activity.id == activity_id, Activity.is_active.is_(True))
        .first()
    )
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


# ─────────────────────────────────────────────────────────────────────────────
# ✅ POST /api/v1/activities/{activity_id}/submit
# ─────────────────────────────────────────────────────────────────────────────

@router.post(
    "/activities/{activity_id}/submit",
    summary="Soumettre une réponse à une activité",
)
def submit_activity(
    activity_id: int,
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    activity = (
        db.query(Activity)
        .filter(Activity.id == activity_id, Activity.is_active.is_(True))
        .first()
    )
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    now = datetime.utcnow()

    log = (
        db.query(LearnerActivityLog)
        .filter(
            LearnerActivityLog.user_id == current_user.id,
            LearnerActivityLog.activity_id == activity_id,
        )
        .first()
    )

    score = payload.get("score")
    learner_response = payload.get("learner_response", "")
    status = payload.get("status", "submitted")
    time_on_task = payload.get("time_on_task_seconds")
    hints_used = payload.get("hints_used", 0)

    if not log:
        log = LearnerActivityLog(
            user_id=current_user.id,
            activity_id=activity_id,
            lesson_id=activity.lesson_id,
            score=score,
            attempts=1,
            time_on_task_seconds=time_on_task,
            hints_used=hints_used,
            status=status,
            learner_response=str(learner_response)[:5000] if learner_response else None,
            started_at=now,
            completed_at=now if status in ("passed", "failed", "submitted", "completed") else None,
            created_at=now,
        )
        db.add(log)
    else:
        log.attempts += 1
        log.score = score if score is not None else log.score
        log.status = status
        log.hints_used += hints_used
        log.learner_response = str(learner_response)[:5000] if learner_response else log.learner_response
        if time_on_task:
            log.time_on_task_seconds = (log.time_on_task_seconds or 0) + time_on_task
        if status in ("passed", "failed", "submitted", "completed"):
            log.completed_at = now

    db.commit()
    db.refresh(log)

    return {
        "activity_id": activity_id,
        "status": log.status,
        "score": log.score,
        "attempts": log.attempts,
        "completed_at": log.completed_at,
        "feedback": None,
        "llm_feedback_fr": None,
        "llm_feedback_en": None,
    }


# ─────────────────────────────────────────────────────────────────────────────
# ✅ VUE COMPLÈTE — Module avec progression apprenant
# ─────────────────────────────────────────────────────────────────────────────

@router.get(
    "/modules/{module_id}/full",
    summary="Module complet avec unités, leçons, activités et progression",
)
def read_module_full(
    module_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    module = db.query(Module).filter(
        Module.id == module_id,
        Module.is_active.is_(True),
    ).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    units = (
        db.query(Unit)
        .filter(Unit.module_id == module_id, Unit.is_active.is_(True))
        .options(
            joinedload(Unit.lessons).joinedload(Lesson.activities)
        )
        .order_by(Unit.order.asc())
        .all()
    )

    # ✅ Progression du module pour cet apprenant
    module_progress = db.query(UserModuleProgress).filter(
        UserModuleProgress.user_id == current_user.id,
        UserModuleProgress.module_id == module_id,
    ).first()

    # ✅ IDs des leçons complétées par l'apprenant
    completed_lesson_ids = set(
        db.execute(
            select(LearnerActivityLog.lesson_id)
            .where(LearnerActivityLog.user_id == current_user.id)
            .where(LearnerActivityLog.status == "completed")
            .distinct()
        ).scalars().all()
    )

    return {
        "module_id": module.id,
        "title_fr": module.title_fr,
        "title_en": module.title_en,
        "level": module.level,
        "role": module.role,
        "journey_stage": module.journey_stage,
        # ✅ Progression globale du module
        "progress_percent": module_progress.progress_percent if module_progress else 0,
        "module_status": module_progress.status if module_progress else "not_started",
        "units": [
            {
                "id": u.id,
                "order": u.order,
                "title_fr": u.title_fr,
                "title_en": u.title_en,
                "estimated_duration_min": u.estimated_duration_min,
                "lessons": [
                    {
                        "id": l.id,
                        "order": l.order,
                        "title_fr": l.title_fr,
                        "title_en": l.title_en,
                        "format": l.format,
                        "difficulty_level": l.difficulty_level,
                        "estimated_duration_min": l.estimated_duration_min,
                        "prerequisite_lesson_id": l.prerequisite_lesson_id,
                        # ✅ Leçon complétée ou non
                        "is_completed": l.id in completed_lesson_ids,
                        "activities": [
                            {
                                "id": a.id,
                                "order": a.order,
                                "type": a.type,
                                "title_fr": a.title_fr,
                                "is_assessed": a.is_assessed,
                                "passing_score": a.passing_score,
                                "has_hints": a.has_hints,
                            }
                            for a in sorted(l.activities, key=lambda x: x.order)
                        ],
                    }
                    for l in sorted(u.lessons, key=lambda x: x.order)
                ],
            }
            for u in units
        ],
    }