"""
Seed AI Marketing Strategist — Diagnostic (refactoré v1.1)

Charge le contenu depuis content/diagnostics/ai_marketing_strategist.json
(architecture Option 3 — JSON externe comme source de vérité).

Contenu pédagogique du diagnostic AI Marketing Strategist :
- 3 skills (logique 1 skill = 1 module)
- 9 questions QCM (3 par skill : Connaissance / Application / Maîtrise)

Source de vérité : PDF Parcours AI Marketing Strategist v1.1 — Mai 2026.

Career path : AI Marketing Strategist (id=80).

Idempotent : skip si déjà seedé.

Refactor : le contenu pédagogique (SKILLS, QUESTIONS) est externalisé dans
le fichier JSON content/diagnostics/ai_marketing_strategist.json. Ce script
ne contient plus que la logique d'insertion BDD.
"""
from app.models.skill import Skill
from app.models.question import Question
from app.scripts.content_loader import load_diagnostic


# Slug du rôle dans content/ (correspond au nom de fichier JSON)
ROLE_SLUG = "ai_marketing_strategist"


def seed_ai_marketing_strategist_diagnostic(db):
    """
    Seed les 3 skills + 9 questions du diagnostic AI Marketing Strategist.

    Lit le contenu depuis content/diagnostics/ai_marketing_strategist.json.
    Idempotent : skip si déjà seedé.
    """
    # =========================================================================
    # 0. Chargement du contenu depuis le JSON
    # =========================================================================
    diagnostic = load_diagnostic(ROLE_SLUG)
    career_path_id = diagnostic["career_path_id"]
    skills_data = diagnostic["skills"]
    questions_data = diagnostic["questions"]

    # =========================================================================
    # 1. Anti-doublon — skip si déjà seedé
    # =========================================================================
    existing_skills = (
        db.query(Skill)
        .filter(Skill.career_path_id == career_path_id)
        .count()
    )
    if existing_skills >= len(skills_data):
        print(
            f"⚠️  AI Marketing Strategist déjà seedé "
            f"({existing_skills} skills sur career_path {career_path_id}), skip."
        )
        return

    # =========================================================================
    # 2. Insérer les 3 skills
    # =========================================================================
    skill_objects = []
    for skill_data in skills_data:
        existing_skill = (
            db.query(Skill)
            .filter(
                Skill.name == skill_data["name"],
                Skill.career_path_id == career_path_id,
            )
            .first()
        )
        if existing_skill:
            skill_objects.append(existing_skill)
            continue

        skill = Skill(
            name=skill_data["name"],
            description=skill_data["description"],
            career_path_id=career_path_id,
        )
        db.add(skill)
        skill_objects.append(skill)

    db.flush()

    # =========================================================================
    # 3. Insérer les 9 questions (3 par skill)
    # =========================================================================
    for question_data in questions_data:
        skill = skill_objects[question_data["skill_index"]]

        existing_question = (
            db.query(Question)
            .filter(
                Question.text == question_data["text"],
                Question.skill_id == skill.id,
            )
            .first()
        )
        if existing_question:
            continue

        question = Question(
            text=question_data["text"],
            option_a=question_data["option_a"],
            option_b=question_data["option_b"],
            option_c=question_data["option_c"],
            option_d=question_data["option_d"],
            correct_answer=question_data["correct_answer"],
            explanation=question_data["explanation"],
            order=question_data["order"],
            skill_id=skill.id,
        )
        db.add(question)

    db.flush()

    print(
        f"✅ AI Marketing Strategist seedé (depuis JSON) : "
        f"{len(skills_data)} skills + {len(questions_data)} questions "
        f"(career_path {career_path_id})"
    )
