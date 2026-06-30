# app/api/v1/endpoints/coaching.py
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.deps import get_db
from app.schemas.coaching import (
    SessionCreateRequest, SessionCreateResponse,
    ChatRequest, ChatResponse
)
from app.models.coaching_session import CoachingSession, Event
from app.services import rag_service

router = APIRouter()


# ----------------------------------------------------------------
# POST /coaching/sessions — Créer une session tuteur
# ----------------------------------------------------------------

@router.post("/sessions", response_model=SessionCreateResponse)
def create_session(
    req: SessionCreateRequest,
    db:  Session = Depends(get_db)
):
    session = CoachingSession(
        user_id=req.user_id,
        module_id=req.module_id,
        section_type=req.section_type,
        kpi_baseline=req.kpi_baseline,
        diagnostic_score=req.diagnostic_score,
        status="active",
        messages=[]
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    return SessionCreateResponse(
        session_id=session.id,
        status=session.status,
        started_at=session.started_at
    )


# ----------------------------------------------------------------
# POST /coaching/sessions/{session_id}/chat — Chat avec le tuteur
# ----------------------------------------------------------------

@router.post("/sessions/{session_id}/chat", response_model=ChatResponse)
def chat(
    session_id: int,
    req:        ChatRequest,
    db:         Session = Depends(get_db)
):
    session = db.query(CoachingSession).filter(
        CoachingSession.id == session_id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session introuvable")

    if session.status == "abandoned":
        raise HTTPException(
            status_code=400,
            detail="Session expirée — créez une nouvelle session"
        )

    embedding = rag_service.embed_text(req.message)
    chunks    = rag_service.search_chunks(
        db,
        module_id=req.module_id,
        section_type=req.section_type,
        embedding=embedding
    )

    # ── Task 5 — Scope guard : trouver le module concerné si hors-scope ──
    redirect_module_title = None
    if not chunks:
        redirect_module_title = rag_service.find_best_module_match(
            db,
            embedding=embedding,
            exclude_module_id=req.module_id
        )

    history         = rag_service.get_session_history(db, session_id)
    learner_profile = rag_service.get_learner_profile(db, req.user_id)

    answer = rag_service.call_llm(
        message=req.message,
        chunks=chunks,
        history=history,
        learner_profile=learner_profile,
        section_type=req.section_type,
        kpi_baseline=session.kpi_baseline,
        redirect_module_title=redirect_module_title
    )

    rag_service.save_chat(
        db=db,
        session_id=session_id,
        user_id=req.user_id,
        module_id=req.module_id,
        section_type=req.section_type,
        user_message=req.message,
        assistant_answer=answer,
        history=history
    )

    try:
        rag_service.detect_pain_point(
            db=db,
            session_id=session_id,
            user_id=req.user_id,
            module_id=req.module_id,
            section_type=req.section_type,
            user_message=req.message
        )
    except Exception:
        pass

    off_topic = len(chunks) == 0
    citations = [
        c["citation_ref"] if c.get("citation_ref") else f"chunk-{c['chunk_id']}"
        for c in chunks
    ]

    return ChatResponse(
        answer=answer,
        citations=citations,
        pain_point_detected=False,
        off_topic=off_topic,
        redirect_module=redirect_module_title
    )


# ----------------------------------------------------------------
# PATCH /coaching/sessions/{session_id}/close — Fermer une session
# ----------------------------------------------------------------

@router.patch("/sessions/{session_id}/close")
def close_session(
    session_id: int,
    db:         Session = Depends(get_db)
):
    session = db.query(CoachingSession).filter(
        CoachingSession.id == session_id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session introuvable")

    from datetime import datetime, timezone
    session.status   = "completed"
    session.ended_at = datetime.now(timezone.utc)
    db.commit()
    return {"session_id": session_id, "status": "completed"}


# ----------------------------------------------------------------
# POST /coaching/execution-task/feedback — Feedback post-soumission
# ----------------------------------------------------------------

@router.post("/execution-task/feedback")
def get_execution_task_feedback(
    payload: dict,
    db:      Session = Depends(get_db)
):
    """
    Génère un feedback post-soumission de l'Execution Task.
    Remplace /hint — l'Agent 1 couvre les hints pendant l'apprentissage.

    payload: {
      "module_id":    int,
      "module_title": str,
      "kpi_before":   str | null,
      "kpi_after":    str,
      "difficulty":   str | null,
      "section_type": str
    }
    """
    from app.services import feedback_service

    # Récupérer les tutoriels du module
    module_id = payload.get("module_id", 0)
    tuto_row = db.execute(text("""
        SELECT tutorials_fr FROM modules WHERE id = :mid
    """), {"mid": module_id}).fetchone()
    tutorials = tuto_row.tutorials_fr if tuto_row and tuto_row.tutorials_fr else []
    tutorial_titles = [t.get("title") for t in tutorials if t.get("title")]

    feedback = feedback_service.generate_execution_task_feedback(
        module_id=module_id,
        module_title=payload.get("module_title", "Module"),
        kpi_before=payload.get("kpi_before"),
        kpi_after=payload.get("kpi_after"),
        difficulty=payload.get("difficulty"),
        section_type=payload.get("section_type", "execution_task"),
        tutorial_titles=tutorial_titles
    )
    return feedback


# ----------------------------------------------------------------
# POST /coaching/events — Enregistrer un événement
# ----------------------------------------------------------------

@router.post("/events")
async def record_event(
    request: Request,
    db:      Session = Depends(get_db)
):
    try:
        body = await request.json()
    except Exception:
        return {"status": "ignored"}

    user_id      = body.get("user_id")
    module_id    = body.get("module_id")
    section_type = body.get("section_type")
    event_type   = body.get("type", "drop_off")
    payload      = body.get("payload", {})

    if not user_id or not module_id:
        return {"status": "ignored"}

    try:
        session = db.execute(
            text(
                "SELECT id FROM coaching_sessions "
                "WHERE user_id  = :user_id "
                "AND module_id  = :module_id "
                "AND status     = 'active' "
                "ORDER BY started_at DESC LIMIT 1"
            ),
            {"user_id": user_id, "module_id": module_id}
        ).fetchone()

        session_id = session[0] if session else None

        event = Event(
            session_id=session_id,
            module_id=module_id,
            section_type=section_type,
            user_id=user_id,
            type=event_type,
            payload=payload or {}
        )
        db.add(event)
        db.commit()
        return {"status": "ok", "type": event_type}

    except Exception:
        db.rollback()
        return {"status": "error"}