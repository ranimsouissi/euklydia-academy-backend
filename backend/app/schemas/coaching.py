# app/schemas/coaching.py
from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime


class SessionCreateRequest(BaseModel):
    user_id:          int
    module_id:        int                    # remplace lesson_id
    section_type:     Literal[
                        "use_case",
                        "kpi",
                        "execution_content",
                        "execution_task",
                        "kpi_measurement"
                      ]                      # section en cours
    kpi_baseline:     Optional[str] = None   # KPI before déclaré
    diagnostic_score: Optional[int] = None  # score diagnostic apprenant


class SessionCreateResponse(BaseModel):
    session_id:  int
    status:      str
    started_at:  Optional[datetime] = None


class ChatRequest(BaseModel):
    session_id:   int            # lier le message à la session
    user_id:      int
    module_id:    int            # remplace lesson_id
    section_type: Literal[
                    "use_case",
                    "kpi",
                    "execution_content",
                    "execution_task",
                    "kpi_measurement"
                  ]              # contexte précis pour le RAG
    message:      str


class ChatResponse(BaseModel):
    answer:               str
    citations:            list[str]
    pain_point_detected:  bool         = False  # collecte anonymisée
    off_topic:            bool         = False  # scope guard
    redirect_module:      Optional[str] = None  # si off_topic = True