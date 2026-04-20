from sqlalchemy import select, desc
from sqlalchemy.orm import Session

from app.models.assessment_session import AssessmentSession
from app.models.user_skill_score import UserSkillScore
from app.models.skill import Skill
from app.models.module import Module
from app.models.module_skill import ModuleSkill
from app.models.career_path import CareerPath
from app.models.user_module_progress import UserModuleProgress
from app.schemas.learning_path import LearningPathItemOut, LearningPathOut, RoadmapSummaryOut
from app.services.assessment_rules import (
    get_level,
    get_priority,
    get_recommended_module_level,
    get_profile_summary,
    sort_skill_results,
)

JOURNEY_STAGE_TO_LEVEL = {
    "foundation": "Beginner",
    "practice":   "Intermediate",
    "expert":     "Advanced",
}


def build_learning_path(db: Session, user_id: int, career_path_id: int) -> LearningPathOut:
    # =============================
    # 1. Récupérer la dernière session assessment
    # =============================
    last_session = db.execute(
        select(AssessmentSession)
        .where(AssessmentSession.user_id == user_id)
        .where(AssessmentSession.career_path_id == career_path_id)
        .order_by(desc(AssessmentSession.created_at))
        .limit(1)
    ).scalar_one_or_none()

    if not last_session:
        return LearningPathOut(
            items=[],
            modules_completed=0,
            modules_total=0,
            roadmap_progress=0,
            summary=None,
        )

    # =============================
    # 2. Récupérer les scores par skill
    # =============================
    rows = db.execute(
        select(UserSkillScore, Skill)
        .join(Skill, Skill.id == UserSkillScore.skill_id)
        .where(UserSkillScore.assessment_session_id == last_session.id)
    ).all()

    # Map skill_id → score réel de l'apprenant
    real_scores: dict[int, int] = {skill.id: uss.score for uss, skill in rows}

    skill_results = []
    for uss, skill in rows:
        skill_results.append(
            LearningPathItemOut(
                module_id=0,
                module_title="",
                module_title_fr=None,
                module_description=None,
                module_description_fr=None,
                module_level="",
                estimated_duration_min=None,
                format=None,
                skill_id=skill.id,
                skill_name=skill.name,
                score=uss.score,
                level=get_level(uss.score),
                priority=get_priority(uss.score),
                status="not_started",
            )
        )

    # =============================
    # 3. Trier les skills par priorité puis score croissant
    # =============================
    sorted_skills = sort_skill_results(skill_results)

    # =============================
    # 4. Récupérer la progression des modules de l'utilisateur
    # =============================
    progress_rows = db.execute(
        select(UserModuleProgress)
        .where(UserModuleProgress.user_id == user_id)
    ).scalars().all()

    progress_by_module_id = {row.module_id: row for row in progress_rows}

    # =============================
    # 5. Construire les items — avec agrégation des skills par module
    # =============================
    items_by_module_id: dict[int, LearningPathItemOut] = {}
    skills_by_module_id: dict[int, list[dict]] = {}

    for skill_item in sorted_skills:
        recommended_level = get_recommended_module_level(skill_item.score)

        module_row = db.execute(
            select(Module, ModuleSkill)
            .join(ModuleSkill, Module.id == ModuleSkill.module_id)
            .where(ModuleSkill.skill_id == skill_item.skill_id)
            .where(Module.is_active.is_(True))
            .where(Module.level == recommended_level)
            .order_by(Module.display_order.asc(), Module.id.asc())
            .limit(1)
        ).first()

        if not module_row:
            continue

        module, _ = module_row
        module_progress = progress_by_module_id.get(module.id)
        module_status = module_progress.status if module_progress else "not_started"

        if module.id not in items_by_module_id:
            items_by_module_id[module.id] = LearningPathItemOut(
                module_id=module.id,
                module_title=module.title_en,
                module_title_fr=module.title_fr,
                module_description=module.description_en,
                module_description_fr=module.description_fr,
                module_level=module.level,
                estimated_duration_min=module.estimated_duration_min,
                format=module.format,
                key_concepts_en=module.key_concepts_en,
                key_concepts_fr=module.key_concepts_fr,
                why_this_module_en=module.why_this_module_en,
                why_this_module_fr=module.why_this_module_fr,
                takeaway_en=module.takeaway_en,
                takeaway_fr=module.takeaway_fr,
                next_recommended_module_en=module.next_recommended_module_en,
                next_recommended_module_fr=module.next_recommended_module_fr,
                skill_id=skill_item.skill_id,
                skill_name=skill_item.skill_name,
                score=skill_item.score,
                level=skill_item.level,
                priority=skill_item.priority,
                status=module_status,
            )
            skills_by_module_id[module.id] = []

        skills_by_module_id[module.id].append({
            "skill_id": skill_item.skill_id,
            "skill_name": skill_item.skill_name,
            "score": skill_item.score,
            "level": skill_item.level,
            "priority": skill_item.priority,
        })

    for module_id, item in items_by_module_id.items():
        item.covered_skills = skills_by_module_id.get(module_id, [])

    # =============================
    # 5b. Toujours afficher les 3 modules (Fondations / Pratique / Expert)
    # Règles :
    # - Module déjà présent (High/Medium) → garder ses vrais covered_skills
    # - Module absent → l'ajouter avec priority="Low" + vrais scores si disponibles
    # =============================
    career_path = db.execute(
        select(CareerPath).where(CareerPath.id == career_path_id)
    ).scalar_one_or_none()

    if career_path:
        for stage in ["foundation", "practice", "expert"]:
            stage_modules = db.execute(
                select(Module)
                .where(Module.role == career_path.name)
                .where(Module.journey_stage == stage)
                .where(Module.is_active.is_(True))
                .order_by(Module.display_order.asc(), Module.id.asc())
            ).scalars().all()

            for module in stage_modules:
                # Récupérer tous les skills liés à ce module
                all_skill_rows = db.execute(
                    select(ModuleSkill, Skill)
                    .join(Skill, Skill.id == ModuleSkill.skill_id)
                    .where(ModuleSkill.module_id == module.id)
                ).all()

                if module.id in items_by_module_id:
                    # ✅ Module déjà présent (High ou Medium) — NE PAS toucher ses covered_skills
                    # Ils contiennent déjà les vrais scores de l'apprenant
                    continue

                # ✅ Module absent → l'ajouter comme Optionnel (Low)
                # Utiliser les vrais scores si disponibles, sinon 0
                optional_covered_skills = []
                for _, s in all_skill_rows:
                    real_score = real_scores.get(s.id, 0)
                    optional_covered_skills.append({
                        "skill_id": s.id,
                        "skill_name": s.name,
                        "score": real_score,
                        "level": get_level(real_score),
                        "priority": "Low",
                    })

                first_skill_row = all_skill_rows[0][1] if all_skill_rows else None
                module_progress = progress_by_module_id.get(module.id)
                module_status = module_progress.status if module_progress else "not_started"

                items_by_module_id[module.id] = LearningPathItemOut(
                    module_id=module.id,
                    module_title=module.title_en,
                    module_title_fr=module.title_fr,
                    module_description=module.description_en,
                    module_description_fr=module.description_fr,
                    module_level=module.level,
                    estimated_duration_min=module.estimated_duration_min,
                    format=module.format,
                    key_concepts_en=module.key_concepts_en,
                    key_concepts_fr=module.key_concepts_fr,
                    why_this_module_en=module.why_this_module_en,
                    why_this_module_fr=module.why_this_module_fr,
                    takeaway_en=module.takeaway_en,
                    takeaway_fr=module.takeaway_fr,
                    next_recommended_module_en=module.next_recommended_module_en,
                    next_recommended_module_fr=module.next_recommended_module_fr,
                    skill_id=first_skill_row.id if first_skill_row else 0,
                    skill_name=first_skill_row.name if first_skill_row else "",
                    score=real_scores.get(first_skill_row.id, 0) if first_skill_row else 0,
                    level=JOURNEY_STAGE_TO_LEVEL.get(stage, "Beginner"),
                    priority="Low",
                    status=module_status,
                    covered_skills=optional_covered_skills,
                )

    items = list(items_by_module_id.values())

    # =============================
    # 6. Calculer la progression globale (High + Medium uniquement)
    # =============================
    main_items = [item for item in items if item.priority in ("High", "Medium")]
    modules_total = len(main_items)
    modules_completed = sum(1 for item in main_items if item.status == "completed")

    roadmap_progress = 0
    if modules_total > 0:
        roadmap_progress = round((modules_completed / modules_total) * 100)

    total_duration_min = sum(
        item.estimated_duration_min or 0
        for item in main_items
        if item.estimated_duration_min is not None
    )

    # =============================
    # 7. Calculer le profil global et le résumé
    # =============================
    global_score = 0.0
    if skill_results:
        global_score = round(sum(s.score for s in skill_results) / len(skill_results), 1)

    role_key_map = {
        79: "ai_sales_specialist",
        80: "ai_marketing_strategist",
        81: "ai_designer",
        82: "ai_project_manager",
    }
    role_key = role_key_map.get(career_path_id, "ai_marketing_strategist")
    profile_data = get_profile_summary(global_score, role_key)

    summary = RoadmapSummaryOut(
        profile=profile_data["profile"],
        profile_fr=profile_data["profile_fr"],
        role_fr=profile_data.get("role_fr"),
        role_en=profile_data.get("role_en"),
        description_en=profile_data["description_en"],
        description_fr=profile_data["description_fr"],
        cta_en=profile_data.get("cta_en"),
        cta_fr=profile_data.get("cta_fr"),
        recommended_focus_en=profile_data.get("cta_en"),
        recommended_focus_fr=profile_data.get("cta_fr"),
        global_score=global_score,
        high_count=sum(1 for i in items if i.priority == "High"),
        medium_count=sum(1 for i in items if i.priority == "Medium"),
        low_count=sum(1 for i in items if i.priority == "Low"),
    )

    return LearningPathOut(
        items=items,
        modules_completed=modules_completed,
        modules_total=modules_total,
        roadmap_progress=roadmap_progress,
        total_duration_min=total_duration_min,
        summary=summary,
    )