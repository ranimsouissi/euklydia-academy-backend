"""
run_seed_ai_sales.py — Script de lancement standalone

Lance le seed complet pour le rôle AI Sales Specialist (rôle pilote v2.0) :
  1. Career paths (s'assure que career_path 79 existe)
  2. Diagnostic   (3 skills + 9 questions)
  3. Modules      (3 modules + 15 units + 42 lessons + 3 mappings module_skills)

Pourquoi un script standalone ?
  Le fichier scripts/seed_all.py importe actuellement 10 fichiers seed qui
  n'existent pas encore (modules et units_lessons des 3 autres rôles).
  Ce script évite ce problème en n'important QUE les fichiers réellement
  présents pour le rôle pilote AI Sales Specialist.

Quand tous les rôles seront seedés, on pourra basculer sur seed_all.py.

Lancement (depuis le dossier backend, avec venv activée) :
    python -m app.scripts.run_seed_ai_sales

Idempotent : peut être relancé sans risque (chaque seed skip si déjà fait).
"""
import sys
import os

# Permet l'exécution depuis n'importe quel dossier en remontant à la racine du projet
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
)

# ─── Forcer l'import de tous les modèles avant tout ───────────────────────────
# Indispensable pour que SQLAlchemy résolve les relations (ex. Module.units →
# Unit.lessons → Lesson.activities). Si un modèle manque, les FK ne sont pas
# enregistrées et les inserts plantent avec des erreurs cryptiques.
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
import app.models.module
import app.models.module_skill
import app.models.unit
import app.models.lesson
import app.models.activity
import app.models.learner_activity_log
import app.models.learner_skill_mastery
import app.models.learner_path_log
import app.models.user_module_progress

from app.db.session import SessionLocal

# ─── Imports des seeds existants ──────────────────────────────────────────────
from app.scripts.seed_career_paths import seed_career_paths
from app.scripts.seed_ai_sales_specialist_diagnostic import (
    seed_ai_sales_specialist_diagnostic,
)
from app.scripts.seed_ai_sales_specialist_modules import (
    seed_ai_sales_specialist_modules,
)


def main():
    db = SessionLocal()
    try:
        print("\n🚀 Seed AI Sales Specialist — Euklydia Academy v2.0")
        print("=" * 60)

        # ── Étape 0 — Career Paths ────────────────────────────────────────────
        # S'assure que career_path 79 (AI Sales Specialist) existe.
        print("\n🎯 Étape 0 — Career Paths (79-82)")
        seed_career_paths(db)

        # ── Étape 1 — Diagnostic (skills + questions) ─────────────────────────
        # Crée les 3 skills (763, 764, 765) et leurs 9 questions QCM.
        print("\n📋 Étape 1 — Diagnostic AI Sales Specialist")
        print("   (3 skills + 9 questions)")
        seed_ai_sales_specialist_diagnostic(db)

        # ── Étape 2 — Modules pédagogiques ────────────────────────────────────
        # Crée les 3 modules + 15 units + 42 lessons + jointures module_skills.
        # Pré-requis : les skills doivent exister (étape 1).
        print("\n📦 Étape 2 — Modules AI Sales Specialist")
        print("   (3 modules + 15 units + 42 lessons + 3 jointures module_skills)")
        seed_ai_sales_specialist_modules(db)

        # ── Commit final ──────────────────────────────────────────────────────
        # Les seeds font db.flush() en interne mais pas db.commit().
        # Le commit est centralisé ici pour garantir l'atomicité :
        # si une étape plante, db.rollback() annule TOUT.
        db.commit()

        print("\n" + "=" * 60)
        print("✅ Seed AI Sales Specialist complet")
        print("   • career_path 79 — AI Sales Specialist")
        print("   • 3 skills (Qualification IA, Outreach, Sales Call)")
        print("   • 9 questions QCM diagnostic")
        print("   • 3 modules (Lead Qual / Outreach / Sales Call)")
        print("   • 15 units + 42 lessons")
        print("   • Contenu PDF v2.0 — 105 corrections appliquées")
        print("=" * 60)

    except Exception as e:
        db.rollback()
        print(f"\n❌ Erreur durant le seed : {e}")
        print("   Tous les changements de cette session ont été annulés.")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()