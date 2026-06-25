from pydantic import BaseModel
from typing import Optional

class SkillResultOut(BaseModel):
    skill_id: int
    skill_name: str
    score: int
    level: str
    priority: str
    recommended_module: Optional[str] = None

class DiagnosticResultsOut(BaseModel):
    global_score: float
    profile: str
    profile_fr: str
    description_en: str
    description_fr: str
    recommended_focus_en: str
    recommended_focus_fr: str
    skills: list[SkillResultOut]