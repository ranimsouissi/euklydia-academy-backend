from pydantic import BaseModel


class SkillCovered(BaseModel):
    skill_id: int
    skill_name: str
    score: int
    level: str
    priority: str


class LearningPathItemOut(BaseModel):
    # ── Module ──────────────────────────────────────────────
    module_id: int
    module_title: str
    module_title_fr: str | None = None
    module_description: str | None = None
    module_description_fr: str | None = None
    module_level: str
    estimated_duration_min: int | None = None
    format: str | None = None

    # Champs enrichis pour le frontend
    key_concepts_en: list[str] | None = None
    key_concepts_fr: list[str] | None = None
    why_this_module_en: str | None = None
    why_this_module_fr: str | None = None
    takeaway_en: str | None = None
    takeaway_fr: str | None = None
    next_recommended_module_en: str | None = None
    next_recommended_module_fr: str | None = None

    # ── Skill principal (le plus prioritaire du module) ─────
    skill_id: int
    skill_name: str
    score: int
    level: str
    priority: str
    status: str = "not_started"

    # ✅ Tous les skills couverts par ce module
    covered_skills: list[SkillCovered] = []


class RoadmapSummaryOut(BaseModel):
    profile: str
    profile_fr: str
    role_fr: str | None = None
    role_en: str | None = None
    description_en: str
    description_fr: str
    cta_en: str | None = None
    cta_fr: str | None = None
    # Anciens champs gardés pour compatibilité frontend
    recommended_focus_en: str | None = None
    recommended_focus_fr: str | None = None
    global_score: float

    # Répartition des items par priorité
    high_count: int = 0
    medium_count: int = 0
    low_count: int = 0


class LearningPathOut(BaseModel):
    items: list[LearningPathItemOut]
    modules_completed: int = 0
    modules_total: int = 0
    roadmap_progress: int = 0
    total_duration_min: int = 0  # ✅ temps total High + Medium uniquement
    summary: RoadmapSummaryOut | None = None