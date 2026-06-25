"""
Script idempotent qui enrichit les 12 skills existantes avec leurs métadonnées
business de use case (use_case_name, kpi_before, kpi_after, blueprint_name,
display_order), en français.

Contenu issu des tables fournies par le métier (images 1-4) :
  - AI Sales Specialist (3 use cases)
  - AI Marketing Strategist (3 use cases)
  - AI Designer (3 use cases)
  - AI Project Manager (3 use cases)

Le script repose sur le matching par skill_name pour identifier la skill à mettre
à jour. Il est sûr de le relancer plusieurs fois (UPDATE only, jamais d'INSERT).

USAGE :
  python -m scripts.seed_use_cases
"""
from __future__ import annotations

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.skill import Skill


# ═══════════════════════════════════════════════════════════════════════════
# Mapping skill_name (tel que présent dans la DB, cf. data CSV) → métadonnées
# du use case correspondant.
#
# Champs :
#   - use_case_name : nom marketing court (en français)
#   - kpi_before    : KPI business AVANT adoption IA
#   - kpi_after     : KPI business APRÈS adoption IA
#   - blueprint_name: nom du Blueprint Euklydia
#   - display_order : ordre d'affichage du use case dans le rôle (1, 2, 3)
# ═══════════════════════════════════════════════════════════════════════════
USE_CASE_DATA: dict[str, dict] = {
    # ────────────────────────────────────────────────────────────────────
    # AI Sales Specialist
    # ────────────────────────────────────────────────────────────────────
    "Qualification IA des leads": {
        "use_case_name": "Qualification automatisée des leads",
        "kpi_before": "Faible taux de conversion (~10–15%)",
        "kpi_after": "+25–40% de leads qualifiés",
        "blueprint_name": "AI Lead Scoring Agent Blueprint",
        "display_order": 1,
    },
    "Prospection hyper-personnalisée": {
        "use_case_name": "Prospection hyper-personnalisée à grande échelle",
        "kpi_before": "Faible taux de réponse (~5–10%)",
        "kpi_after": "Taux de réponse multiplié par 2–3",
        "blueprint_name": "Hyper-Personalization Engine",
        "display_order": 2,
    },
    "Conversations commerciales assistées par IA": {
        "use_case_name": "Préparation des entretiens commerciaux",
        "kpi_before": "Faible taux de closing",
        "kpi_after": "+15–25% de taux de closing",
        "blueprint_name": "AI Sales Copilot System",
        "display_order": 3,
    },

    # ────────────────────────────────────────────────────────────────────
    # AI Marketing Strategist
    # ────────────────────────────────────────────────────────────────────
    "Stratégie et création de contenu IA": {
        "use_case_name": "Optimisation de la stratégie de contenu",
        "kpi_before": "Faible engagement",
        "kpi_after": "+30–50% d'engagement",
        "blueprint_name": "AI Content Engine System",
        "display_order": 1,
    },
    "Optimisation de campagnes et growth IA": {
        "use_case_name": "Optimisation de la performance des campagnes",
        "kpi_before": "CAC élevé",
        "kpi_after": "-20–30% de CAC",
        "blueprint_name": "AI Growth Loop Framework",
        "display_order": 2,
    },
    "Audience intelligence et segmentation IA": {
        "use_case_name": "Insights et segmentation d'audience",
        "kpi_before": "Ciblage imprécis",
        "kpi_after": "+25% de conversion",
        "blueprint_name": "AI Persona Intelligence System",
        "display_order": 3,
    },

    # ────────────────────────────────────────────────────────────────────
    # AI Designer
    # ────────────────────────────────────────────────────────────────────
    "AI Visual Ideation & Concept": {
        "use_case_name": "Génération rapide de concepts",
        "kpi_before": "Idéation lente",
        "kpi_after": "Idéation 5x plus rapide",
        "blueprint_name": "AI Design Ideation System",
        "display_order": 1,
    },
    "AI UX Intelligence": {
        "use_case_name": "Optimisation de l'UX",
        "kpi_before": "Faible engagement",
        "kpi_after": "+20–30% d'engagement",
        "blueprint_name": "AI UX Intelligence Framework",
        "display_order": 2,
    },
    "AI Design System & Ops": {
        "use_case_name": "Automatisation du design system",
        "kpi_before": "Incohérence",
        "kpi_after": "+40% de cohérence",
        "blueprint_name": "AI Design System Builder",
        "display_order": 3,
    },

    # ────────────────────────────────────────────────────────────────────
    # AI Project Manager
    # ────────────────────────────────────────────────────────────────────
    "AI Project Planning": {
        "use_case_name": "Automatisation de la planification projet",
        "kpi_before": "Planification lente",
        "kpi_after": "50–70% de temps gagné",
        "blueprint_name": "AI Planning Engine",
        "display_order": 1,
    },
    "AI Risk Intelligence": {
        "use_case_name": "Identification proactive des risques",
        "kpi_before": "Gestion réactive des problèmes",
        "kpi_after": "-30% de retards",
        "blueprint_name": "AI Risk Intelligence System",
        "display_order": 2,
    },
    "AI Execution & Productivity": {
        "use_case_name": "Optimisation de la productivité d'équipe",
        "kpi_before": "Faible efficacité",
        "kpi_after": "+25% de productivité",
        "blueprint_name": "AI Execution Optimization System",
        "display_order": 3,
    },
}


def seed_use_cases() -> None:
    """
    UPDATE idempotent : pour chaque skill_name présent dans USE_CASE_DATA,
    met à jour les 5 colonnes use case.

    Aucune création/suppression. Les skills inconnues sont signalées mais
    ne bloquent pas l'exécution.
    """
    db = SessionLocal()
    try:
        updated_count = 0
        skipped_count = 0
        not_found = []

        for skill_name, meta in USE_CASE_DATA.items():
            skill = db.execute(
                select(Skill).where(Skill.name == skill_name)
            ).scalar_one_or_none()

            if skill is None:
                not_found.append(skill_name)
                continue

            # Détection des changements pour ne pas marquer modifiée une ligne identique
            needs_update = (
                skill.use_case_name != meta["use_case_name"]
                or skill.kpi_before != meta["kpi_before"]
                or skill.kpi_after != meta["kpi_after"]
                or skill.blueprint_name != meta["blueprint_name"]
                or skill.display_order != meta["display_order"]
            )

            if not needs_update:
                skipped_count += 1
                continue

            skill.use_case_name = meta["use_case_name"]
            skill.kpi_before = meta["kpi_before"]
            skill.kpi_after = meta["kpi_after"]
            skill.blueprint_name = meta["blueprint_name"]
            skill.display_order = meta["display_order"]
            updated_count += 1

        db.commit()

        # Récap console
        print(f"✅ Use cases mis à jour : {updated_count}")
        print(f"⏭  Use cases déjà à jour (skip) : {skipped_count}")
        if not_found:
            print(f"⚠️  Skills introuvables ({len(not_found)}) :")
            for n in not_found:
                print(f"    - {n!r}")

    except Exception as e:
        db.rollback()
        print(f"❌ Erreur durant le seed : {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_use_cases()