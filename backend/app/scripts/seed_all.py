import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# ✅ Forcer l'import de tous les modèles avant tout
import app.models.user
import app.models.role
import app.models.skill
import app.models.question
import app.models.career_path
import app.models.assessment_session
import app.models.user_skill_score
import app.models.user_response
import app.models.oauth_account
import app.models.oauth_state
import app.models.user_profile
import app.models.password_reset_token
import app.models.unit
import app.models.lesson
import app.models.activity
import app.models.learner_activity_log
import app.models.learner_skill_mastery
import app.models.learner_path_log

from app.db.session import SessionLocal

# ── Career Paths (ids 79-82) ─────────────────────────────────────────────────
from app.scripts.seed_career_paths import seed_career_paths

# ── Assessments (skills + questions) ─────────────────────────────────────────
from app.scripts.seed_ai_sales_specialist import seed_ai_sales_specialist
from app.scripts.seed_ai_marketing_strategist import seed_ai_marketing_strategist
from app.scripts.seed_ai_designer import seed_ai_designer
from app.scripts.seed_ai_project_manager import seed_ai_project_manager

# ── Modules ───────────────────────────────────────────────────────────────────
from app.scripts.seed_ai_sales_specialist_modules import seed_ai_sales_specialist_modules
from app.scripts.seed_ai_marketing_strategist_modules import seed_ai_marketing_strategist_modules
from app.scripts.seed_ai_designer_modules import seed_ai_designer_modules
from app.scripts.seed_ai_project_manager_modules import seed_ai_project_manager_modules

# ── Units / Lessons / Activities ──────────────────────────────────────────────
from app.scripts.seed_ai_sales_units_lessons import seed_ai_sales_units_lessons
from app.scripts.seed_ai_marketing_units_lessons import seed_ai_marketing_units_lessons
from app.scripts.seed_ai_designer_units_lessons import seed_ai_designer_units_lessons
from app.scripts.seed_ai_project_manager_units_lessons import seed_ai_project_manager_units_lessons


def main():
    db = SessionLocal()
    try:
        print("\n🚀 Démarrage du seed — Euklydia Academy")
        print("=" * 50)

        # ── Étape 0 — Career Paths ────────────────────────────────────────────
        print("\n🎯 Étape 0 — Career Paths (79-82)")
        seed_career_paths(db)

        # ── Étape 1 — Assessments ─────────────────────────────────────────────
        print("\n📋 Étape 1 — Assessments (skills + questions)")
        seed_ai_sales_specialist(db)
        seed_ai_marketing_strategist(db)
        seed_ai_designer(db)
        seed_ai_project_manager(db)

        # ── Étape 2 — Modules ─────────────────────────────────────────────────
        print("\n📦 Étape 2 — Modules (Fondations / Pratique / Expert)")
        seed_ai_sales_specialist_modules(db)
        seed_ai_marketing_strategist_modules(db)
        seed_ai_designer_modules(db)
        seed_ai_project_manager_modules(db)

        # ── Étape 3 — Units / Lessons / Activities ────────────────────────────
        print("\n📚 Étape 3 — Units, Lessons, Activities")
        seed_ai_sales_units_lessons(db)
        seed_ai_marketing_units_lessons(db)
        seed_ai_designer_units_lessons(db)
        seed_ai_project_manager_units_lessons(db)

        db.commit()
        print("\n" + "=" * 50)
        print("✅ Seed complet — 4 rôles seedés avec succès")
        print("   AI Sales Specialist      (role_id=79)")
        print("   AI Marketing Strategist  (role_id=80)")
        print("   AI Designer              (role_id=81)")
        print("   AI Project Manager       (role_id=82)")
        print("=" * 50)

    except Exception as e:
        db.rollback()
        print(f"\n❌ Erreur durant le seed : {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()