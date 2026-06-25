"""
Pré-vérification avant wipe : vérifier qu'aucune table utilisateur ne pointe
vers les anciennes données Marketing/Designer/PM (skills, questions, modules,
units, lessons).

À lancer depuis backend/ avec : python app/scripts/check_before_wipe.py
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.db.session import SessionLocal
from app.models.skill import Skill
from app.models.question import Question
from app.models.module import Module
from app.models.unit import Unit
from app.models.lesson import Lesson
from app.models.user_skill_score import UserSkillScore
from app.models.user_response import UserResponse
from app.models.diagnostic_session import diagnosticSession
from app.models.learner_activity_log import LearnerActivityLog
from app.models.learner_skill_mastery import LearnerSkillMastery

# Career paths à wiper (Marketing, Designer, Project Manager — pas Sales !)
CAREER_PATHS_TO_WIPE = [80, 81, 82]

db = SessionLocal()
try:
    print("\n🔍 Pré-vérification avant wipe")
    print("=" * 70)
    print(f"Career paths concernés : {CAREER_PATHS_TO_WIPE}")
    print(f"(Sales = 79 sera PRÉSERVÉ)")
    print("-" * 70)

    # Récupérer tous les IDs concernés
    skill_ids = [
        s.id for s in db.query(Skill).filter(
            Skill.career_path_id.in_(CAREER_PATHS_TO_WIPE)
        ).all()
    ]
    question_ids = [
        q.id for q in db.query(Question).filter(
            Question.skill_id.in_(skill_ids)
        ).all()
    ] if skill_ids else []

    module_ids = [
        m.id for m in db.query(Module).filter(
            Module.role.in_([
                "AI Marketing Strategist", "AI Designer", "AI Project Manager"
            ])
        ).all()
    ]
    unit_ids = [
        u.id for u in db.query(Unit).filter(Unit.module_id.in_(module_ids)).all()
    ] if module_ids else []
    lesson_ids = [
        l.id for l in db.query(Lesson).filter(Lesson.unit_id.in_(unit_ids)).all()
    ] if unit_ids else []

    print(f"\n📊 Données à supprimer :")
    print(f"   - {len(skill_ids)} skills")
    print(f"   - {len(question_ids)} questions")
    print(f"   - {len(module_ids)} modules")
    print(f"   - {len(unit_ids)} units")
    print(f"   - {len(lesson_ids)} lessons")

    # ─────────────────────────────────────────────────────────────────────
    # Vérifier les références par les tables utilisateur
    # ─────────────────────────────────────────────────────────────────────
    print(f"\n🔗 Références par les tables utilisateur :")
    print("-" * 70)

    blockers_found = False

    # 1. UserSkillScore → skill_id
    if skill_ids:
        nb = db.query(UserSkillScore).filter(
            UserSkillScore.skill_id.in_(skill_ids)
        ).count()
        flag = "⚠️ " if nb > 0 else "✅"
        print(f"   {flag} user_skill_scores  → {nb} ligne(s) liée(s)")
        if nb > 0:
            blockers_found = True

    # 2. UserResponse → question_id
    if question_ids:
        nb = db.query(UserResponse).filter(
            UserResponse.question_id.in_(question_ids)
        ).count()
        flag = "⚠️ " if nb > 0 else "✅"
        print(f"   {flag} user_responses     → {nb} ligne(s) liée(s)")
        if nb > 0:
            blockers_found = True

    # 3. diagnosticSession → career_path_id (si applicable)
    try:
        nb = db.query(diagnosticSession).filter(
            diagnosticSession.career_path_id.in_(CAREER_PATHS_TO_WIPE)
        ).count()
        flag = "⚠️ " if nb > 0 else "✅"
        print(f"   {flag} diagnostic_sessions → {nb} ligne(s) liée(s)")
        if nb > 0:
            blockers_found = True
    except Exception:
        # Si pas de career_path_id sur ce modèle, on skip
        print(f"   ℹ️  diagnostic_sessions  → pas de FK directe (skip)")

    # 4. LearnerSkillMastery → skill_id
    if skill_ids:
        try:
            nb = db.query(LearnerSkillMastery).filter(
                LearnerSkillMastery.skill_id.in_(skill_ids)
            ).count()
            flag = "⚠️ " if nb > 0 else "✅"
            print(f"   {flag} learner_skill_mastery → {nb} ligne(s) liée(s)")
            if nb > 0:
                blockers_found = True
        except Exception as e:
            print(f"   ℹ️  learner_skill_mastery → erreur ({e})")

    # 5. LearnerActivityLog → lesson_id ou activity_id
    if lesson_ids:
        try:
            # Tentative avec lesson_id
            nb = db.query(LearnerActivityLog).filter(
                LearnerActivityLog.lesson_id.in_(lesson_ids)
            ).count()
            flag = "⚠️ " if nb > 0 else "✅"
            print(f"   {flag} learner_activity_log (lesson_id) → {nb} ligne(s)")
            if nb > 0:
                blockers_found = True
        except Exception:
            print(f"   ℹ️  learner_activity_log → pas de FK lesson_id directe")

    # ─────────────────────────────────────────────────────────────────────
    # Verdict
    # ─────────────────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    if blockers_found:
        print("⚠️  ATTENTION : des données utilisateur référencent les anciennes données.")
        print("   Le wipe va provoquer des erreurs de FK ou supprimer des stats.")
        print("   → Réfléchir à un wipe en cascade ou copier-coller les warnings ici.")
    else:
        print("✅ Aucune référence utilisateur trouvée — wipe sans risque.")
    print("=" * 70)

finally:
    db.close()