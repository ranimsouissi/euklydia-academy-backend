"""
Wipe ciblé des anciennes données v1 : Marketing, Designer, Project Manager.
Sales (career_path_id=79) est PRÉSERVÉ.

Ordre de suppression (respect des FK PostgreSQL) :
1. Lessons (référencent units)
2. Units (référencent modules)
3. ModuleSkills (référencent modules + skills)
4. Modules
5. Questions (référencent skills)
6. UserSkillScore (référencent skills) -- si présent
7. Skills

À lancer depuis backend/ avec : python app/scripts/wipe_old_seeds.py
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
from app.models.module_skill import ModuleSkill

# Career paths à wiper — Sales (79) est PRÉSERVÉ
CAREER_PATHS_TO_WIPE = [80, 81, 82]
ROLES_TO_WIPE = ["AI Marketing Strategist", "AI Designer", "AI Project Manager"]


def wipe_old_seeds(db):
    """
    Supprime les anciennes données v1 pour les career_paths 80, 81, 82
    en respectant l'ordre des contraintes FK.
    """
    print("\n🧹 Wipe des anciennes données v1")
    print("=" * 70)
    print(f"Career paths ciblés : {CAREER_PATHS_TO_WIPE}")
    print(f"Roles ciblés        : {ROLES_TO_WIPE}")
    print(f"⚠️  Sales (CP=79) sera PRÉSERVÉ")
    print("-" * 70)

    # ─────────────────────────────────────────────────────────────────────
    # 1. Récupérer les IDs à supprimer
    # ─────────────────────────────────────────────────────────────────────
    skill_ids = [
        s.id for s in db.query(Skill).filter(
            Skill.career_path_id.in_(CAREER_PATHS_TO_WIPE)
        ).all()
    ]
    module_ids = [
        m.id for m in db.query(Module).filter(
            Module.role.in_(ROLES_TO_WIPE)
        ).all()
    ]
    unit_ids = [
        u.id for u in db.query(Unit).filter(
            Unit.module_id.in_(module_ids)
        ).all()
    ] if module_ids else []

    print(f"\n📊 À supprimer :")
    print(f"   - {len(skill_ids)} skills")
    print(f"   - {len(module_ids)} modules")
    print(f"   - {len(unit_ids)} units")

    # ─────────────────────────────────────────────────────────────────────
    # 2. Suppression dans le bon ordre
    # ─────────────────────────────────────────────────────────────────────

    # 2.1 Lessons (référencent units)
    if unit_ids:
        nb = db.query(Lesson).filter(Lesson.unit_id.in_(unit_ids)).delete(
            synchronize_session=False
        )
        print(f"\n   🗑️  Lessons supprimées : {nb}")

    # 2.2 Units (référencent modules)
    if module_ids:
        nb = db.query(Unit).filter(Unit.module_id.in_(module_ids)).delete(
            synchronize_session=False
        )
        print(f"   🗑️  Units supprimées : {nb}")

    # 2.3 ModuleSkills (référencent modules ET skills)
    if module_ids:
        nb = db.query(ModuleSkill).filter(
            ModuleSkill.module_id.in_(module_ids)
        ).delete(synchronize_session=False)
        print(f"   🗑️  ModuleSkills supprimés : {nb}")

    # 2.4 Modules
    if module_ids:
        nb = db.query(Module).filter(Module.id.in_(module_ids)).delete(
            synchronize_session=False
        )
        print(f"   🗑️  Modules supprimés : {nb}")

    # 2.5 Questions (référencent skills)
    if skill_ids:
        nb = db.query(Question).filter(Question.skill_id.in_(skill_ids)).delete(
            synchronize_session=False
        )
        print(f"   🗑️  Questions supprimées : {nb}")

    # 2.6 UserSkillScore (si présent — peut bloquer la suppression des skills)
    try:
        from app.models.user_skill_score import UserSkillScore
        if skill_ids:
            nb = db.query(UserSkillScore).filter(
                UserSkillScore.skill_id.in_(skill_ids)
            ).delete(synchronize_session=False)
            print(f"   🗑️  UserSkillScores supprimés : {nb}")
    except Exception as e:
        print(f"   ℹ️  UserSkillScore : skip ({e})")

    # 2.7 Skills (en dernier)
    if skill_ids:
        nb = db.query(Skill).filter(Skill.id.in_(skill_ids)).delete(
            synchronize_session=False
        )
        print(f"   🗑️  Skills supprimées : {nb}")

    db.flush()
    print("\n" + "=" * 70)
    print("✅ Wipe terminé. Tu peux maintenant relancer seed_all.py")
    print("=" * 70)


if __name__ == "__main__":
    db = SessionLocal()
    try:
        # Confirmation interactive avant de tout supprimer
        print("\n⚠️  ATTENTION — SUPPRESSION DE DONNÉES")
        print(f"Ce script va supprimer toutes les données v1 pour :")
        print(f"  - career_paths {CAREER_PATHS_TO_WIPE}")
        print(f"  - roles {ROLES_TO_WIPE}")
        print(f"\nSales (career_path_id=79) sera PRÉSERVÉ.")
        confirm = input("\nTaper 'OUI' pour confirmer : ").strip()
        if confirm != "OUI":
            print("❌ Annulé.")
            sys.exit(0)

        wipe_old_seeds(db)
        db.commit()
        print("\n✅ Commit réussi.")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Erreur durant le wipe : {e}")
        print("→ Rollback appliqué, aucune donnée supprimée.")
        raise
    finally:
        db.close()