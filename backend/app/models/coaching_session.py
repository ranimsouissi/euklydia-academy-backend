# app/models/coaching_session.py
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.base import Base


class CoachingSession(Base):
    __tablename__ = "coaching_sessions"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)

    module_id    = Column(Integer, ForeignKey("modules.id"), nullable=True)
    section_type = Column(String(50), nullable=True)

    kpi_baseline     = Column(String(500), nullable=True)
    diagnostic_score = Column(Integer,     nullable=True)

    messages      = Column(JSON,    default=list)
    status        = Column(String,  default="active")
    mastery_score = Column(Numeric(4, 2), nullable=True)
    ended_at      = Column(DateTime(timezone=True), nullable=True)
    started_at    = Column(DateTime(timezone=True), server_default=func.now())


class Event(Base):
    __tablename__ = "events"

    id         = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("coaching_sessions.id",
                                             ondelete="CASCADE"))
    user_id    = Column(Integer, ForeignKey("users.id"))

    module_id    = Column(Integer, ForeignKey("modules.id"), nullable=True)
    section_type = Column(String(50), nullable=True)

    type       = Column(String,  nullable=False)
    payload    = Column(JSON,    nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())