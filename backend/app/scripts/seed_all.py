import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# ✅ Forcer l'import de tous les modèles avant tout
import app.models.user
import app.models.role
import app.models.skill
import app.models.question
import app.models.career_path
import app.models.diagnostic_session
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
import app.models.module
import app.models.module_skill

from app.db.session import SessionLocal

# ── Career Paths (ids 79-82) ─────────────────────────────────────────────────
from app.scripts.seed_career_paths import seed_career_paths

# ── diagnostics (skills + questions) — diagnostics uniquement ────────────────
from app.scripts.seed_ai_sales_specialist_diagnostic import seed_ai_sales_specialist_diagnostic
from app.scripts.seed_ai_marketing_strategist_diagnostic import seed_ai_marketing_strategist_diagnostic
from app.scripts.seed_ai_designer_diagnostic import seed_ai_designer_diagnostic
from app.scripts.seed_ai_project_manager_diagnostic import seed_ai_project_manager_diagnostic

# ── Modules pédagogiques (modules + units + lessons + module_skills) ─────────
from app.scripts.seed_ai_sales_specialist_modules import seed_ai_sales_specialist_modules
from app.scripts.seed_ai_marketing_strategist_modules import seed_ai_marketing_strategist_modules
from app.scripts.seed_ai_designer_modules import seed_ai_designer_modules
from app.scripts.seed_ai_project_manager_modules import seed_ai_project_manager_modules


def main():
    db = SessionLocal()
    try:
        print("\n🚀 Démarrage du seed — Euklydia Academy")
        print("=" * 50)

        # ── Étape 0 — Career Paths ────────────────────────────────────────────
        print("\n🎯 Étape 0 — Career Paths (79-82)")
        seed_career_paths(db)

        # ── Étape 1 — diagnostics (diagnostics) ───────────────────────────────
        print("\n📋 Étape 1 — diagnostics (skills + questions)")
        seed_ai_sales_specialist_diagnostic(db)
        seed_ai_marketing_strategist_diagnostic(db)
        seed_ai_designer_diagnostic(db)
        seed_ai_project_manager_diagnostic(db)

        # ── Étape 2 — Modules pédagogiques ────────────────────────────────────
        # Pré-requis : les diagnostics doivent être seedés AVANT les modules
        # (les modules référencent les skills créées par les diagnostics).
        print("\n📚 Étape 2 — Modules pédagogiques (modules + units + lessons)")
        seed_ai_sales_specialist_modules(db)
        seed_ai_marketing_strategist_modules(db)
        seed_ai_designer_modules(db)
        seed_ai_project_manager_modules(db)

        db.commit()
        print("\n" + "=" * 50)
        print("✅ Seed terminé avec succès")
        print("\n   Diagnostics seedés :")
        print("   • AI Sales Specialist      (career_path_id=79)")
        print("   • AI Marketing Strategist  (career_path_id=80)")
        print("   • AI Designer              (career_path_id=81)")
        print("   • AI Project Manager       (career_path_id=82)")
        print("\n   Modules pédagogiques seedés :")
        print("   • AI Sales Specialist      (3 modules + 15 units + 45 lessons)")
        print("   • AI Marketing Strategist  (3 modules + 15 units + 45 lessons)")
        print("   • AI Designer              (3 modules + 15 units + 45 lessons)")
        print("   • AI Project Manager       (3 modules + 15 units + 45 lessons)")
        print("=" * 50)

    except Exception as e:
        db.rollback()
        print(f"\n❌ Erreur durant le seed : {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()