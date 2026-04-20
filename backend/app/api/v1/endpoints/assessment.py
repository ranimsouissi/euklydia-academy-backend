import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select, desc
from sqlalchemy.orm import Session, selectinload
from datetime import datetime, timedelta

from app.core.deps import get_current_user
from app.core.limiter import limiter
from app.db.session import get_db
from app.core.config import settings
from app.services.assessment_rules import (
    get_level, get_priority, sort_skill_results,
    get_recommended_module_level, get_profile_summary
)

from app.models.user import User
from app.models.question import Question
from app.models.skill import Skill
from app.models.user_response import UserResponse
from app.models.user_skill_score import UserSkillScore
from app.models.assessment_session import AssessmentSession

from app.schemas.assessment_submit import SubmitAnswersIn
from app.schemas.assessment_results import SkillResultOut, AssessmentResultsOut
from app.schemas.assessment_questionnaire import QuestionnaireOut

router = APIRouter()
logger = logging.getLogger(__name__)


def _dt_iso(dt: datetime | None) -> str | None:
    return dt.isoformat() if dt else None


def _cooldown_check(db: Session, user_id: int, career_path_id: int):
    last_session = db.execute(
        select(AssessmentSession)
        .where(AssessmentSession.user_id == user_id)
        .where(AssessmentSession.career_path_id == career_path_id)
        .order_by(desc(AssessmentSession.created_at))
        .limit(1)
    ).scalar_one_or_none()

    if not last_session:
        return {"has_scores": False, "eligible": True, "last": None, "next": None}

    next_allowed_at = last_session.created_at + timedelta(days=settings.ASSESSMENT_COOLDOWN_DAYS)
    eligible = datetime.utcnow() >= next_allowed_at

    return {
        "has_scores": True,
        "eligible": eligible,
        "last": last_session.created_at,
        "next": next_allowed_at,
    }


# =========================
# GET /questionnaire
# =========================

@router.get("/questionnaire", response_model=QuestionnaireOut)
def get_questionnaire(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user.career_path_id:
        raise HTTPException(status_code=400, detail="Select career path first")

    skills = db.execute(
        select(Skill)
        .where(Skill.career_path_id == current_user.career_path_id)
        .order_by(Skill.id)
    ).scalars().all()

    if not skills:
        raise HTTPException(
            status_code=404,
            detail=f"No assessment found for career_path_id={current_user.career_path_id}"
        )

    skill_ids = [s.id for s in skills]

    questions = db.execute(
        select(Question)
        .where(Question.skill_id.in_(skill_ids))
        .order_by(Question.skill_id, Question.order)
    ).scalars().all()

    questions_by_skill: dict[int, list] = {s.id: [] for s in skills}
    for q in questions:
        questions_by_skill[q.skill_id].append(q)

    return {
        "career_path_id": current_user.career_path_id,
        "skills": [
            {
                "id": s.id,
                "name": s.name,
                "description": s.description,
                "questions": [
                    {
                        "id": q.id,
                        "text": q.text,
                        "order": q.order,
                        "option_a": q.option_a,
                        "option_b": q.option_b,
                        "option_c": q.option_c,
                        "option_d": q.option_d,
                    }
                    for q in questions_by_skill[s.id]
                ],
            }
            for s in skills
        ],
    }


# =========================
# POST /submit
# =========================

@router.post("/submit", response_model=list[SkillResultOut])
@limiter.limit("3/minute")
def submit_answers(
    request: Request,
    payload: SubmitAnswersIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user.career_path_id:
        raise HTTPException(status_code=400, detail="Select career path first")

    cooldown = _cooldown_check(db, current_user.id, current_user.career_path_id)
    if cooldown["has_scores"] and not cooldown["eligible"]:
        raise HTTPException(
            status_code=403,
            detail={
                "message": f"You can retake the assessment every {settings.ASSESSMENT_COOLDOWN_DAYS} days.",
                "last_assessment_at": _dt_iso(cooldown["last"]),
                "next_allowed_at": _dt_iso(cooldown["next"]),
            },
        )

    if not payload.answers:
        raise HTTPException(status_code=400, detail="answers is empty")

    q_ids = [a.question_id for a in payload.answers]

    stmt = (
        select(Question)
        .options(selectinload(Question.skill))
        .join(Question.skill)
        .where(Question.id.in_(q_ids))
        .where(Skill.career_path_id == current_user.career_path_id)
    )
    questions = db.execute(stmt).scalars().all()
    found_ids = {q.id for q in questions}

    missing_or_forbidden = [qid for qid in q_ids if qid not in found_ids]
    if missing_or_forbidden:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid or forbidden question_ids: {missing_or_forbidden}",
        )

    # ✅ Transaction atomique : si quelque chose plante, tout est rollback
    try:
        # 1. Créer la session
        session = AssessmentSession(
            user_id=current_user.id,
            career_path_id=current_user.career_path_id,
            global_score_percent=0.0,
        )
        db.add(session)
        db.flush()

        answers_map = {a.question_id: a.selected_option for a in payload.answers}
        now = datetime.utcnow()

        correct_per_skill: dict[int, int] = {}
        questions_per_skill: dict[int, int] = {}
        skill_names: dict[int, str] = {}

        # 2. Insérer les réponses
        for q in questions:
            sid = q.skill_id
            skill_names[sid] = q.skill.name
            questions_per_skill[sid] = questions_per_skill.get(sid, 0) + 1

            selected = answers_map[q.id]
            is_correct = selected == q.correct_answer
            correct_per_skill[sid] = correct_per_skill.get(sid, 0) + (1 if is_correct else 0)

            db.add(UserResponse(
                user_id=current_user.id,
                assessment_session_id=session.id,
                question_id=q.id,
                selected_option=selected,
                is_correct=is_correct,
                created_at=now,
            ))

        db.flush()

        # 3. Calculer et insérer les scores par skill
        results: list[SkillResultOut] = []
        computed_scores: list[int] = []

        for sid, correct in correct_per_skill.items():
            total_q = questions_per_skill.get(sid, 2)

            if correct == 0:
                score = 0
            elif correct == total_q:
                score = 100
            else:
                score = 50

            computed_scores.append(score)

            db.add(UserSkillScore(
                user_id=current_user.id,
                skill_id=sid,
                score=score,
                assessment_session_id=session.id,
            ))

            results.append(SkillResultOut(
                skill_id=sid,
                skill_name=skill_names[sid],
                score=score,
                level=get_level(score),
                priority=get_priority(score),
                recommended_module=get_recommended_module_level(score),
            ))

        # 4. Garde-fou anti-orphelin : refuser de committer une session sans scores
        if not results:
            raise RuntimeError(
                "No skill scores were computed — refusing to commit orphan session"
            )

        # 5. Score global
        global_score = round(sum(computed_scores) / max(len(computed_scores), 1), 1)
        session.global_score_percent = float(global_score)

        # 6. Commit atomique final
        db.commit()

        logger.info(
            f"Assessment submitted: user_id={current_user.id}, "
            f"session_id={session.id}, skills={len(results)}, global={global_score}%"
        )

        return sort_skill_results(results)

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.error(
            f"Assessment submit failed for user_id={current_user.id}: {e}",
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail="Failed to save assessment results. Please try again."
        )


# =========================
# GET /results
# =========================

@router.get("/results", response_model=list[SkillResultOut])
def get_results(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user.career_path_id:
        raise HTTPException(status_code=400, detail="Select career path first")

    last_session = db.execute(
        select(AssessmentSession)
        .where(AssessmentSession.user_id == current_user.id)
        .where(AssessmentSession.career_path_id == current_user.career_path_id)
        .order_by(desc(AssessmentSession.created_at))
        .limit(1)
    ).scalar_one_or_none()

    if not last_session:
        return []

    rows = db.execute(
        select(UserSkillScore, Skill)
        .join(Skill, Skill.id == UserSkillScore.skill_id)
        .where(UserSkillScore.assessment_session_id == last_session.id)
        .order_by(Skill.id)
    ).all()

    return [
        SkillResultOut(
            skill_id=skill.id,
            skill_name=skill.name,
            score=uss.score,
            level=get_level(uss.score),
            priority=get_priority(uss.score),
            recommended_module=get_recommended_module_level(uss.score),
        )
        for (uss, skill) in rows
    ]


# =========================
# GET /status
# =========================

@router.get("/status")
def assessment_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user.career_path_id:
        return {
            "has_scores": False,
            "required": True,
            "recommended": False,
            "eligible": True,
            "last_assessment_at": None,
            "next_allowed_at": None,
            "expires_at": None,
            "global_score_percent": None,
        }

    cooldown = _cooldown_check(db, current_user.id, current_user.career_path_id)

    last_session = db.execute(
        select(AssessmentSession)
        .where(AssessmentSession.user_id == current_user.id)
        .where(AssessmentSession.career_path_id == current_user.career_path_id)
        .order_by(desc(AssessmentSession.created_at))
        .limit(1)
    ).scalar_one_or_none()

    required = not cooldown["has_scores"]

    NINETY_DAYS = 90
    expired_90d = False
    days_since_last = None

    if last_session:
        delta = datetime.utcnow() - last_session.created_at
        days_since_last = delta.days
        expired_90d = delta.days >= NINETY_DAYS

    recommended = bool(expired_90d)

    expires_at = None
    global_score = None
    if last_session:
        expires_at = last_session.created_at + timedelta(days=settings.ASSESSMENT_COOLDOWN_DAYS)
        global_score = float(last_session.global_score_percent)

    return {
        "has_scores": cooldown["has_scores"],
        "required": required,
        "recommended": recommended,
        "eligible": cooldown["eligible"],
        "last_assessment_at": _dt_iso(cooldown["last"]),
        "next_allowed_at": _dt_iso(cooldown["next"]),
        "expires_at": _dt_iso(expires_at),
        "global_score_percent": global_score,
        "days_since_last": days_since_last,
    }