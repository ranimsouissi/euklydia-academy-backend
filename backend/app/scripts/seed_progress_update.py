"""
seed_progress_update.py
========================
Ajoute progress_update_fr aux 12 modules depuis les PDFs.

Usage :
    cd backend
    python app/scripts/seed_progress_update.py
"""

import os
import sys
import json
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("❌ DATABASE_URL manquante dans .env")
    sys.exit(1)

try:
    from sqlalchemy import create_engine, text
except ImportError:
    print("❌ sqlalchemy non installé")
    sys.exit(1)

engine = create_engine(DATABASE_URL)

# ─────────────────────────────────────────────────────────────────────────────
# DONNÉES — Progress Update des 12 modules (source : PDFs v1.1)
# ─────────────────────────────────────────────────────────────────────────────

PROGRESS_UPDATES = [

    # ══════════════════════════════════════════════════════════════════════════
    # AI MARKETING STRATEGIST
    # ══════════════════════════════════════════════════════════════════════════
    {
        "title_fr": "Content Strategy Optimization",
        "role": "AI Marketing Strategist",
        "progress_update_fr": {
            "kpi_label": "Taux d'engagement",
            "kpi_target": "+30 à +50 %",
            "skill_label": "AI Content Strategy & Creation",
            "skill_number": 1,
            "deliverables": [
                "Comparatif KPI avant / après (graphique)",
                "Mise à jour du score skill 1 (Content Strategy)",
                "Bibliothèque personnelle des prompts utilisés et des contenus produits"
            ],
            "next_step": "Module 2 ou 3 selon priorités"
        }
    },
    {
        "title_fr": "Campaign Performance Optimization",
        "role": "AI Marketing Strategist",
        "progress_update_fr": {
            "kpi_label": "CAC (Coût d'Acquisition Client)",
            "kpi_target": "-20 à -30 %",
            "skill_label": "AI Campaign & Growth Optimization",
            "skill_number": 2,
            "deliverables": [
                "Comparatif CAC avant / après",
                "Bibliothèque personnelle des créas testées (top 5 par performance)",
                "Mise à jour du score skill 2 (Campaign Performance)",
                "Recommandation pour le Module 3 (Audience Insights)"
            ],
            "next_step": "Module 3 — Audience Insights & Segmentation"
        }
    },
    {
        "title_fr": "Audience Insights & Segmentation",
        "role": "AI Marketing Strategist",
        "progress_update_fr": {
            "kpi_label": "Taux de conversion (campagnes ciblées)",
            "kpi_target": "+25 %",
            "skill_label": "AI Audience Intelligence",
            "skill_number": 3,
            "deliverables": [
                "Comparatif taux de conversion ciblé vs large",
                "Bibliothèque personnelle de personas avec messaging associé",
                "Mise à jour du score skill 3 (Audience Insights)",
                "Vue consolidée des 3 modules : parcours complet AI Marketing Strategist terminé"
            ],
            "next_step": "Parcours AI Marketing Strategist complété ✅"
        }
    },

    # ══════════════════════════════════════════════════════════════════════════
    # AI PROJECT MANAGER
    # ══════════════════════════════════════════════════════════════════════════
    {
        "title_fr": "Project Planning Automation",
        "role": "AI Project Manager",
        "progress_update_fr": {
            "kpi_label": "Temps de planification",
            "kpi_target": "Gain mesuré (graphique temps gagné)",
            "skill_label": "AI Project Planning",
            "skill_number": 1,
            "deliverables": [
                "Comparatif KPI avant / après (graphique temps gagné)",
                "Mise à jour du score skill 1 (Project Planning)",
                "Bibliothèque personnelle des prompts utilisés et plans produits",
                "Execution Timeline Model personnalisé prêt à réutiliser sur futurs projets"
            ],
            "next_step": "Module 2 ou 3 selon priorités"
        }
    },
    {
        "title_fr": "Risk Identification",
        "role": "AI Project Manager",
        "progress_update_fr": {
            "kpi_label": "Anticipation des risques",
            "kpi_target": "Risques identifiés avant / après",
            "skill_label": "AI Risk Intelligence",
            "skill_number": 2,
            "deliverables": [
                "Comparatif anticipation des risques avant / après",
                "Bibliothèque personnelle de playbooks de mitigation par type de risque",
                "Risk register complet avec les 8 risques Maghreb intégrés",
                "Mise à jour du score skill 2 (Risk Intelligence)",
                "Recommandation pour le Module 3 (Team Productivity Optimization)"
            ],
            "next_step": "Module 3 — Team Productivity Optimization"
        }
    },
    {
        "title_fr": "Team Productivity Optimization",
        "role": "AI Project Manager",
        "progress_update_fr": {
            "kpi_label": "Productivité d'équipe",
            "kpi_target": "Avant / après mesurable",
            "skill_label": "AI Execution & Productivity",
            "skill_number": 3,
            "deliverables": [
                "Comparatif productivité d'équipe avant / après",
                "Bibliothèque personnelle de prompts et templates de sprint",
                "Mise à jour du score skill 3 (Execution & Productivity)",
                "Vue consolidée des 3 modules : parcours complet AI Project Manager"
            ],
            "next_step": "Parcours AI Project Manager complété ✅"
        }
    },

    # ══════════════════════════════════════════════════════════════════════════
    # AI DESIGNER
    # ══════════════════════════════════════════════════════════════════════════
    {
        "title_fr": "Rapid Concept Generation",
        "role": "AI Designer",
        "progress_update_fr": {
            "kpi_label": "Vitesse d'idéation visuelle",
            "kpi_target": "KPI avant / après (graphique)",
            "skill_label": "AI Visual Ideation & Concept",
            "skill_number": 1,
            "deliverables": [
                "Comparatif KPI avant / après (graphique)",
                "Mise à jour du score skill 1 (Visual Ideation)",
                "Bibliothèque personnelle des prompts Midjourney testés et des concepts produits",
                "Recommandation pour la suite (Module 2 ou 3 selon priorités)"
            ],
            "next_step": "Module 2 ou 3 selon priorités"
        }
    },
    {
        "title_fr": "UX Optimization",
        "role": "AI Designer",
        "progress_update_fr": {
            "kpi_label": "Engagement (frictions résolues)",
            "kpi_target": "Avant / après les corrections",
            "skill_label": "AI UX Intelligence",
            "skill_number": 2,
            "deliverables": [
                "Comparatif engagement avant / après les corrections",
                "Bibliothèque personnelle de playbooks UX (top frictions résolues)",
                "Bibliothèque personnelle de mappings Insight → Action documentés",
                "Mise à jour du score skill 2 (UX Intelligence)",
                "Recommandation pour le Module 3 (Design System Automation)"
            ],
            "next_step": "Module 3 — Design System Automation"
        }
    },
    {
        "title_fr": "Design System Automation",
        "role": "AI Designer",
        "progress_update_fr": {
            "kpi_label": "Cohérence visuelle",
            "kpi_target": "Avant / après",
            "skill_label": "AI Design System & Ops",
            "skill_number": 3,
            "deliverables": [
                "Comparatif cohérence visuelle avant / après",
                "Bibliothèque personnelle de composants Figma versionnée",
                "Template Scalable Design Ops Framework adapté à son entreprise",
                "Mise à jour du score skill 3 (Design System)",
                "Vue consolidée des 3 modules : parcours complet AI Designer"
            ],
            "next_step": "Parcours AI Designer complété ✅"
        }
    },

    # ══════════════════════════════════════════════════════════════════════════
    # AI SALES SPECIALIST
    # ══════════════════════════════════════════════════════════════════════════
    {
        "title_fr": "Lead Qualification Automation",
        "role": "AI Sales Specialist",
        "progress_update_fr": {
            "kpi_label": "Taux de conversion leads",
            "kpi_target": "KPI avant / après (graphique)",
            "skill_label": "AI Lead Scoring & Qualification",
            "skill_number": 1,
            "deliverables": [
                "Comparatif KPI avant / après (graphique)",
                "Mise à jour du score skill 1 (Lead Scoring)",
                "Bibliothèque personnelle des prompts utilisés et des résultats obtenus",
                "Recommandation pour la suite (Module 2 ou approfondissement)"
            ],
            "next_step": "Module 2 ou approfondissement"
        }
    },
    {
        "title_fr": "Personalized Outreach at Scale",
        "role": "AI Sales Specialist",
        "progress_update_fr": {
            "kpi_label": "Reply rate",
            "kpi_target": "Avant / après",
            "skill_label": "AI Outreach & Personalization",
            "skill_number": 2,
            "deliverables": [
                "Comparatif reply rate avant / après",
                "Bibliothèque personnelle des templates testés (top 3 par reply rate)",
                "Mise à jour du score skill 2 (Outreach)",
                "Recommandation pour le Module 3 (Sales Call Preparation)"
            ],
            "next_step": "Module 3 — Sales Call Preparation"
        }
    },
    {
        "title_fr": "Sales Call Preparation",
        "role": "AI Sales Specialist",
        "progress_update_fr": {
            "kpi_label": "Close rate",
            "kpi_target": "Avant / après",
            "skill_label": "AI Sales Conversations",
            "skill_number": 3,
            "deliverables": [
                "Comparatif close rate avant / après",
                "Bibliothèque personnelle d'objection handling (les meilleures réponses)",
                "Mise à jour du score skill 3 (Sales Conversations)",
                "Vue consolidée des 3 modules : parcours complet AI Sales Specialist terminé"
            ],
            "next_step": "Parcours AI Sales Specialist complété ✅"
        }
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# PIPELINE UPDATE
# ─────────────────────────────────────────────────────────────────────────────

def run():
    print("=" * 60)
    print("  SEED PROGRESS UPDATE — 12 modules / 4 rôles")
    print("=" * 60)

    updated = 0
    errors = 0

    with engine.connect() as conn:
        for module_data in PROGRESS_UPDATES:
            try:
                result = conn.execute(text("""
                    UPDATE modules
                    SET progress_update_fr = cast(:progress_update_fr as jsonb)
                    WHERE title_fr = :title_fr
                      AND role     = :role
                    RETURNING id, title_fr, role
                """), {
                    "title_fr":           module_data["title_fr"],
                    "role":               module_data["role"],
                    "progress_update_fr": json.dumps(
                        module_data["progress_update_fr"],
                        ensure_ascii=False
                    ),
                })

                row = result.fetchone()
                if row:
                    print(f"  ✅ [{row.id}] {row.title_fr} ({row.role})")
                    updated += 1
                else:
                    print(f"  ⚠️  Non trouvé : '{module_data['title_fr']}' ({module_data['role']})")

            except Exception as e:
                print(f"  ❌ Erreur sur {module_data['title_fr']} : {e}")
                errors += 1

        conn.commit()

    print("\n" + "=" * 60)
    print(f"  ✅ {updated}/12 modules mis à jour")
    if errors:
        print(f"  ❌ {errors} erreurs")
    print("=" * 60)


if __name__ == "__main__":
    run()
