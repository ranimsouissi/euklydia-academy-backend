"""
Script utilitaire — Re-seed des questions du diagnostic AI Project Manager.

Contexte : les questions actuellement en BDD pour le career_path AI Project Manager
(id=82) ne correspondent pas à la spec PDF v1.0 validée par le CEO. Elles ont été
insérées par un seed antérieur (probablement une version provisoire), et l'idempotence
de seed_ai_project_manager_diagnostic.py les a fait skipper.

Ce script :
  1. Identifie les 3 skills PM existantes (on ne les touche pas — elles sont OK)
  2. Supprime les user_responses liées aux questions PM (cascade nécessaire pour FK)
  3. Supprime les 9 questions PM actuelles
  4. Réinsère les 9 questions du PDF v1.0 depuis seed_ai_project_manager_diagnostic.py

Idempotent : si les questions PDF sont déjà présentes, ne fait rien.
Sécurité : print l'état avant/après et demande une confirmation explicite.

Usage :
    python -m app.scripts.reseed_ai_project_manager_questions
"""
from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Forcer l'import des modèles pour SQLAlchemy
import app.models.user
import app.models.skill
import app.models.question
import app.models.user_response

from app.db.session import SessionLocal
from app.models.skill import Skill
from app.models.question import Question
from app.models.user_response import UserResponse

# Import du seed officiel (source de vérité = PDF v1.0)
from app.scripts.seed_ai_project_manager_diagnostic import (
    QUESTIONS as PDF_QUESTIONS,
    CAREER_PATH_ID,
)


def main():
    db = SessionLocal()
    try:
        print("=" * 70)
        print("RE-SEED — Questions AI Project Manager (career_path_id=82)")
        print("=" * 70)

        # =====================================================================
        # 1. Récupérer les skills PM existantes (ordre par id)
        # =====================================================================
        skills = (
            db.query(Skill)
            .filter(Skill.career_path_id == CAREER_PATH_ID)
            .order_by(Skill.id)
            .all()
        )
        if len(skills) != 3:
            print(
                f"❌ Erreur : {len(skills)} skills trouvées pour career_path_id="
                f"{CAREER_PATH_ID}, attendu 3. Abandon."
            )
            return

        print(f"\n✅ {len(skills)} skills PM trouvées :")
        for s in skills:
            print(f"   • id={s.id:3d}  name={s.name}")

        skill_ids = [s.id for s in skills]

        # =====================================================================
        # 2. Inventaire des questions actuelles
        # =====================================================================
        current_questions = (
            db.query(Question)
            .filter(Question.skill_id.in_(skill_ids))
            .order_by(Question.skill_id, Question.order)
            .all()
        )
        print(f"\n📋 {len(current_questions)} questions actuellement en BDD :")
        for q in current_questions:
            print(f"   • id={q.id} | skill_id={q.skill_id} | order={q.order} | "
                  f"{q.text[:80]}...")

        # =====================================================================
        # 3. Détection : sont-elles déjà conformes au PDF ?
        # =====================================================================
        pdf_first_texts = [PDF_QUESTIONS[i]["text"] for i in [0, 3, 6]]  # Q1.1 de chaque skill
        bdd_first_texts = [q.text for q in current_questions if q.order == 1]

        if set(pdf_first_texts) == set(bdd_first_texts):
            print("\n✅ Les questions actuelles correspondent déjà au PDF — rien à faire.")
            return

        print("\n⚠️  Les questions actuelles NE correspondent PAS au PDF v1.0.")
        print("    Action : suppression + réinsertion des 9 questions PDF.")

        # =====================================================================
        # 4. Compter les user_responses qui seront supprimées
        # =====================================================================
        question_ids = [q.id for q in current_questions]
        response_count = (
            db.query(UserResponse)
            .filter(UserResponse.question_id.in_(question_ids))
            .count()
        )
        print(f"\n🗑️  Cela supprimera également {response_count} user_responses liées.")

        # =====================================================================
        # 5. Confirmation explicite
        # =====================================================================
        print("\n" + "=" * 70)
        confirm = input(
            "Tape 'YES' pour confirmer la suppression et réinsertion : "
        ).strip()
        if confirm != "YES":
            print("❌ Abandon — aucune modification effectuée.")
            return

        # =====================================================================
        # 6. Suppression : d'abord user_responses (FK), puis questions
        # =====================================================================
        print("\n🗑️  Suppression des user_responses liées...")
        deleted_responses = (
            db.query(UserResponse)
            .filter(UserResponse.question_id.in_(question_ids))
            .delete(synchronize_session=False)
        )
        print(f"   • {deleted_responses} user_responses supprimées")

        print("🗑️  Suppression des 9 questions actuelles...")
        deleted_questions = (
            db.query(Question)
            .filter(Question.id.in_(question_ids))
            .delete(synchronize_session=False)
        )
        print(f"   • {deleted_questions} questions supprimées")

        # =====================================================================
        # 7. Réinsertion des questions du PDF
        # =====================================================================
        print("\n✏️  Insertion des 9 questions du PDF v1.0...")
        for question_data in PDF_QUESTIONS:
            skill = skills[question_data["skill_index"]]
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
            print(f"   • skill={skill.name[:30]:30s} | order={question_data['order']} | "
                  f"{question_data['text'][:60]}...")

        db.commit()

        # =====================================================================
        # 8. Vérification finale
        # =====================================================================
        new_questions = (
            db.query(Question)
            .filter(Question.skill_id.in_(skill_ids))
            .order_by(Question.skill_id, Question.order)
            .all()
        )

        print("\n" + "=" * 70)
        print(f"✅ Re-seed terminé : {len(new_questions)} questions PDF insérées")
        print("=" * 70)
        for q in new_questions:
            skill_name = next(s.name for s in skills if s.id == q.skill_id)
            print(f"   • id={q.id} | skill={skill_name[:30]:30s} | "
                  f"order={q.order} | {q.text[:60]}...")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Erreur durant le re-seed : {type(e).__name__}: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()