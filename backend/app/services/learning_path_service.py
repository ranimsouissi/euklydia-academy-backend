from sqlalchemy import select, desc
from sqlalchemy.orm import Session

from app.models.diagnostic_session import DiagnosticSession
from app.models.user_skill_score import UserSkillScore
from app.models.skill import Skill
from app.models.module import Module
from app.models.module_skill import ModuleSkill
from app.models.career_path import CareerPath
from app.models.user_module_progress import UserModuleProgress
from app.models.user_profile import UserProfile
from app.schemas.learning_path import (
    LearningPathItemOut,
    LearningPathOut,
    RoadmapSummaryOut,
    SectionProgressItem,
    ExecutionTaskSubmissionOut,
)
from app.services.diagnostic_rules import (
    get_level,
    get_priority,
    get_recommended_module_level,
    get_profile_summary,
    sort_skill_results,
)

STAGE_TO_LEVEL = {
    "foundation": "Fondation",
    "practice":   "Pratique",
    "expert":     "Expert",
}


def build_learning_path(
    db:             Session,
    user_id:        int,
    career_path_id: int
) -> LearningPathOut:

    # 1. Récupérer la dernière session diagnostic
    last_session = db.execute(
        select(DiagnosticSession)
        .where(DiagnosticSession.user_id == user_id)
        .where(DiagnosticSession.career_path_id == career_path_id)
        .order_by(desc(DiagnosticSession.created_at))
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

    # 2. Récupérer les scores par skill + objets Skill complets
    rows = db.execute(
        select(UserSkillScore, Skill)
        .join(Skill, Skill.id == UserSkillScore.skill_id)
        .where(UserSkillScore.diagnostic_session_id == last_session.id)
    ).all()

    real_scores:  dict[int, int]   = {skill.id: uss.score for uss, skill in rows}
    skills_by_id: dict[int, Skill] = {skill.id: skill for uss, skill in rows}

    skill_results = []
    for uss, skill in rows:
        skill_results.append(
            LearningPathItemOut(
                module_id=0,
                module_title="",
                module_level="",
                skill_id=skill.id,
                skill_name=skill.name,
                score=uss.score,
                level=get_level(uss.score),
                priority=get_priority(uss.score),
                status="not_started",
            )
        )

    # 3. Trier les skills par priorité puis score croissant
    sorted_skills = sort_skill_results(skill_results)

    # 4. Récupérer la progression des modules
    progress_rows = db.execute(
        select(UserModuleProgress)
        .where(UserModuleProgress.user_id == user_id)
    ).scalars().all()

    progress_by_module_id = {row.module_id: row for row in progress_rows}

    # 5. Récupérer le profil apprenant — temps disponible
    profile_row = db.execute(
        select(UserProfile)
        .where(UserProfile.user_id == user_id)
    ).scalar_one_or_none()

    time_available = (
        int(profile_row.time_available_per_week)
        if profile_row and hasattr(profile_row, 'time_available_per_week')
        and profile_row.time_available_per_week
        else None
    )

    # 6. Construire les items
    items_by_module_id:  dict[int, LearningPathItemOut] = {}
    skills_by_module_id: dict[int, list[dict]]          = {}

    for skill_item in sorted_skills:
        module_row = db.execute(
            select(Module, ModuleSkill)
            .join(ModuleSkill, Module.id == ModuleSkill.module_id)
            .where(ModuleSkill.skill_id == skill_item.skill_id)
            .where(Module.is_active.is_(True))
            .order_by(Module.display_order.asc(), Module.id.asc())
            .limit(1)
        ).first()

        if not module_row:
            continue

        module, _      = module_row
        module_progress = progress_by_module_id.get(module.id)
        module_status   = module_progress.status if module_progress else "not_started"
        primary_skill   = skills_by_id.get(skill_item.skill_id)

        if module.id not in items_by_module_id:

            # ── Section progress ─────────────────────────────
            section_progress = []
            if module_progress and module_progress.section_progress:
                for section_type, status in module_progress.section_progress.items():
                    section_progress.append(SectionProgressItem(
                        section_type=section_type,
                        status=status
                    ))

            # ── Execution Task soumission ────────────────────
            execution_task = None
            if module_progress:
                execution_task = ExecutionTaskSubmissionOut(
                    submitted=module_progress.execution_task_submitted or False,
                    url=module_progress.execution_task_url,
                    kpi_after=module_progress.kpi_after,
                    difficulty=module_progress.execution_task_difficulty,
                    submitted_at=module_progress.execution_task_submitted_at
                )

            # ── KPI after réel vs KPI cible ──────────────────
            # kpi_after réel = ce que l'apprenant a mesuré
            # kpi_after cible = ce que le module promet
            kpi_after_value = (
                module_progress.kpi_after
                if module_progress and module_progress.kpi_after
                else (primary_skill.kpi_after if primary_skill else None)
            )

            items_by_module_id[module.id] = LearningPathItemOut(
                module_id=module.id,
                module_title=module.title_en,
                module_title_fr=module.title_fr,
                module_description=module.description_en,
                module_description_fr=module.description_fr,
                module_level=module.level,
                journey_stage=module.journey_stage,
                estimated_duration_min=module.estimated_duration_min,
                format=module.format,
                key_concepts_en=module.key_concepts_en,
                key_concepts_fr=module.key_concepts_fr,
                why_this_module_en=module.why_this_module_en,
                why_this_module_fr=module.why_this_module_fr,
                takeaway_en=module.takeaway_en,
                takeaway_fr=module.takeaway_fr,
                next_recommended_module_en=None,
                next_recommended_module_fr=None,
                skill_id=skill_item.skill_id,
                skill_name=skill_item.skill_name,
                score=skill_item.score,
                level=skill_item.level,
                priority=skill_item.priority,
                status=module_status,
                progress_percent=float(
                    module_progress.progress_percent
                ) if module_progress and module_progress.progress_percent else 0.0,
                use_case_name=primary_skill.use_case_name if primary_skill else None,
                kpi_before=primary_skill.kpi_before if primary_skill else None,
                kpi_after=kpi_after_value,
                blueprint_name=primary_skill.blueprint_name if primary_skill else None,
                use_case_display_order=primary_skill.display_order if primary_skill else None,
                # ── Nouveaux champs ──────────────────────────
                section_progress=section_progress,
                execution_task=execution_task,
                mastery_last_updated=str(module_progress.updated_at)
                                     if module_progress else None,
            )
            skills_by_module_id[module.id] = []

        skills_by_module_id[module.id].append({
            "skill_id":   skill_item.skill_id,
            "skill_name": skill_item.skill_name,
            "score":      skill_item.score,
            "level":      skill_item.level,
            "priority":   skill_item.priority,
        })

    for module_id, item in items_by_module_id.items():
        item.covered_skills = skills_by_module_id.get(module_id, [])

    # 7. Compléter avec les modules additionnels du career path
    career_path = db.execute(
        select(CareerPath).where(CareerPath.id == career_path_id)
    ).scalar_one_or_none()

    if career_path:
        for stage_key, level_fr in STAGE_TO_LEVEL.items():
            stage_modules = db.execute(
                select(Module)
                .where(Module.role == career_path.name)
                .where(Module.level == level_fr)
                .where(Module.is_active.is_(True))
                .order_by(Module.display_order.asc(), Module.id.asc())
            ).scalars().all()

            for module in stage_modules:
                if module.id in items_by_module_id:
                    continue

                all_skill_rows = db.execute(
                    select(ModuleSkill, Skill)
                    .join(Skill, Skill.id == ModuleSkill.skill_id)
                    .where(ModuleSkill.module_id == module.id)
                ).all()

                optional_covered_skills = []
                for _, s in all_skill_rows:
                    real_score = real_scores.get(s.id, 0)
                    optional_covered_skills.append({
                        "skill_id":   s.id,
                        "skill_name": s.name,
                        "score":      real_score,
                        "level":      get_level(real_score),
                        "priority":   "Low",
                    })

                first_skill_row = all_skill_rows[0][1] if all_skill_rows else None
                module_progress = progress_by_module_id.get(module.id)
                module_status   = module_progress.status if module_progress else "not_started"
                primary_skill   = first_skill_row

                # ── Section progress ─────────────────────────
                section_progress = []
                if module_progress and module_progress.section_progress:
                    for section_type, status in module_progress.section_progress.items():
                        section_progress.append(SectionProgressItem(
                            section_type=section_type,
                            status=status
                        ))

                # ── Execution Task soumission ────────────────
                execution_task = None
                if module_progress:
                    execution_task = ExecutionTaskSubmissionOut(
                        submitted=module_progress.execution_task_submitted or False,
                        url=module_progress.execution_task_url,
                        kpi_after=module_progress.kpi_after,
                        difficulty=module_progress.execution_task_difficulty,
                        submitted_at=module_progress.execution_task_submitted_at
                    )

                kpi_after_value = (
                    module_progress.kpi_after
                    if module_progress and module_progress.kpi_after
                    else (primary_skill.kpi_after if primary_skill else None)
                )

                items_by_module_id[module.id] = LearningPathItemOut(
                    module_id=module.id,
                    module_title=module.title_en,
                    module_title_fr=module.title_fr,
                    module_description=module.description_en,
                    module_description_fr=module.description_fr,
                    module_level=module.level,
                    journey_stage=module.journey_stage,
                    estimated_duration_min=module.estimated_duration_min,
                    format=module.format,
                    key_concepts_en=module.key_concepts_en,
                    key_concepts_fr=module.key_concepts_fr,
                    why_this_module_en=module.why_this_module_en,
                    why_this_module_fr=module.why_this_module_fr,
                    takeaway_en=module.takeaway_en,
                    takeaway_fr=module.takeaway_fr,
                    next_recommended_module_en=None,
                    next_recommended_module_fr=None,
                    skill_id=primary_skill.id   if primary_skill else 0,
                    skill_name=primary_skill.name if primary_skill else "",
                    score=real_scores.get(primary_skill.id, 0) if primary_skill else 0,
                    level=module.level,
                    priority="Low",
                    status=module_status,
                    progress_percent=float(
                        module_progress.progress_percent
                    ) if module_progress and module_progress.progress_percent else 0.0,
                    covered_skills=optional_covered_skills,
                    use_case_name=primary_skill.use_case_name if primary_skill else None,
                    kpi_before=primary_skill.kpi_before if primary_skill else None,
                    kpi_after=kpi_after_value,
                    blueprint_name=primary_skill.blueprint_name if primary_skill else None,
                    use_case_display_order=primary_skill.display_order if primary_skill else None,
                    # ── Nouveaux champs ──────────────────────
                    section_progress=section_progress,
                    execution_task=execution_task,
                    mastery_last_updated=str(module_progress.updated_at)
                                         if module_progress else None,
                )

    items = list(items_by_module_id.values())

    # 8. Calculer la progression globale
    main_items        = [i for i in items if i.priority in ("High", "Medium")]
    modules_total     = len(main_items)
    modules_completed = sum(1 for i in main_items if i.status == "completed")

    roadmap_progress = (
        round((modules_completed / modules_total) * 100)
        if modules_total > 0 else 0
    )

    total_duration_min = sum(
        item.estimated_duration_min or 0
        for item in main_items
        if item.estimated_duration_min is not None
    )

    # 9. Détecter la stagnation
    modules_without_improvement = sum(
        1 for item in main_items
        if item.execution_task
        and item.execution_task.submitted
        and not item.execution_task.kpi_after
    )
    stagnation_detected = modules_without_improvement >= 2

    # 10. Prochain module recommandé
    next_module = next(
        (item for item in items
         if item.status == "not_started"
         and item.priority in ("High", "Medium")),
        None
    )

    # 11. Calculer le profil global
    global_score = 0.0
    if skill_results:
        global_score = round(
            sum(s.score for s in skill_results) / len(skill_results), 1
        )

    role_key_map = {
        79: "ai_sales_specialist",
        80: "ai_marketing_strategist",
        81: "ai_designer",
        82: "ai_project_manager",
    }
    role_key     = role_key_map.get(career_path_id, "ai_marketing_strategist")
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
        # ── Nouveaux champs ──────────────────────────────────
        next_recommended_module_id=next_module.module_id if next_module else None,
        stagnation_detected=stagnation_detected,
        time_available_per_week=time_available,
    )

    return LearningPathOut(
        items=items,
        modules_completed=modules_completed,
        modules_total=modules_total,
        roadmap_progress=roadmap_progress,
        total_duration_min=total_duration_min,
        summary=summary,
    )