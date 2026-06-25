"""
seed_checkpoints.py
====================
Crée les activités checkpoints pour chaque module.
5 checkpoints par module, un par section :
  CP1 — Use Case + KPI     → quiz 3 questions compréhension
  CP2 — Skills mapped      → quiz auto-évaluation 3 questions
  CP3 — Execution Content  → exercise pratique prompt
  CP4 — Mission terrain    → exercise soumission mission
  CP5 — KPI Measurement    → quiz bilan 2 questions

Idempotent : skip les leçons qui ont déjà des activités.

Usage :
    cd backend
    python seed_checkpoints.py
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

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

engine  = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


# =============================================================================
# CHECKPOINTS PAR MODULE
# Structure : CHECKPOINTS[module_id][unit_order] = activity_data
# =============================================================================

CHECKPOINTS = {

    # =========================================================================
    # MODULE 403 — Lead Qualification Automation
    # =========================================================================
    403: {
        # CP1 — Use Case + KPI (Unit 1)
        1: {
            "type": "quiz",
            "title_fr": "Checkpoint 1 — Comprendre le problème business",
            "is_assessed": True,
            "passing_score": 70,
            "has_hints": True,
            "content_fr": {
                "questions": [
                    {
                        "id": "q1",
                        "question": "Quel est le taux de conversion lead → opportunité typique pour une équipe sales B2B en Afrique du Nord sans IA ?",
                        "options": ["5-8%", "10-15%", "25-30%", "40-50%"],
                        "correct": "B",
                        "explanation": "Sans méthode structurée, le taux de conversion est typiquement de 10-15% — trop faible et imprévisible."
                    },
                    {
                        "id": "q2",
                        "question": "Que signifie BANT dans la qualification des leads ?",
                        "options": [
                            "Business, Authority, Need, Timing",
                            "Budget, Authority, Need, Timing",
                            "Budget, Audience, Network, Timing",
                            "Business, Audience, Need, Target"
                        ],
                        "correct": "B",
                        "explanation": "BANT = Budget, Authority, Need, Timing — les 4 critères fondamentaux de qualification."
                    },
                    {
                        "id": "q3",
                        "question": "Selon la grille BANT v2.0, un lead avec un score de 55/100 doit être traité comment ?",
                        "options": [
                            "Appel dans les 24h",
                            "Email cette semaine",
                            "Nurturing (lead froid)",
                            "Disqualifier"
                        ],
                        "correct": "B",
                        "explanation": "Score 50-69 → Email cette semaine (lead tiède). Score ≥ 70 = appel 24h, 30-49 = nurturing, <30 = disqualifier."
                    }
                ]
            },
            "hints_fr": [
                {"level": 1, "text": "Relisez la section Use Case — les chiffres clés sont mentionnés."},
                {"level": 2, "text": "BANT est un acronyme dont chaque lettre représente un critère de qualification."},
                {"level": 3, "text": "La grille de décision BANT v2.0 divise les scores en 4 zones : ≥70, 50-69, 30-49, <30."}
            ],
            "rubric_fr": None
        },

        # CP2 — Skills mapped (Unit 2)
        2: {
            "type": "quiz",
            "title_fr": "Checkpoint 2 — Auto-évaluation compétences",
            "is_assessed": True,
            "passing_score": 60,
            "has_hints": True,
            "content_fr": {
                "questions": [
                    {
                        "id": "q1",
                        "question": "Parmi ces compétences, laquelle est la plus importante pour qualifier des leads B2B au Maghreb ?",
                        "options": [
                            "Maîtriser Excel avancé",
                            "Construire des prompts ChatGPT structurés pour évaluation de leads",
                            "Connaître parfaitement le code Python",
                            "Utiliser uniquement LinkedIn Sales Navigator"
                        ],
                        "correct": "B",
                        "explanation": "Les prompts ChatGPT structurés sont au cœur de la qualification IA — ils permettent d'évaluer objectivement chaque lead."
                    },
                    {
                        "id": "q2",
                        "question": "Comment classe-t-on les leads selon la méthode enseignée dans ce module ?",
                        "options": [
                            "1, 2, 3, 4 par ordre d'importance",
                            "Chaud, tiède, froid, mort",
                            "A, B, C, D selon priorité",
                            "High, Medium, Low"
                        ],
                        "correct": "C",
                        "explanation": "La classification A/B/C/D alignée sur la grille BANT v2.0 permet une priorisation claire et actionnable."
                    },
                    {
                        "id": "q3",
                        "question": "Quel outil CRM intègre nativement un scoring IA des leads ?",
                        "options": [
                            "Trello",
                            "HubSpot AI",
                            "Notion",
                            "Google Sheets"
                        ],
                        "correct": "B",
                        "explanation": "HubSpot AI, Salesforce Einstein et Zoho Zia intègrent du scoring natif — HubSpot étant le plus accessible en Afrique du Nord."
                    }
                ]
            },
            "hints_fr": [
                {"level": 1, "text": "Regardez la liste des 8 compétences clés du module."},
                {"level": 2, "text": "La classification utilise des lettres de l'alphabet."}
            ],
            "rubric_fr": None
        },

        # CP3 — Execution Content (Unit 3)
        3: {
            "type": "exercise",
            "title_fr": "Checkpoint 3 — Appliquer le Prompt 1 BANT",
            "is_assessed": True,
            "passing_score": 0,
            "has_hints": True,
            "content_fr": {
                "consigne": (
                    "Choisissez un lead réel de votre pipeline (ou inventez-en un fictif réaliste).\n\n"
                    "Appliquez le Prompt 1 — BANT Scoring en remplissant toutes les variables :\n"
                    "• NOM_DU_CONTACT, POSTE, ENTREPRISE, SECTEUR, PAYS\n"
                    "• BUDGET, ROLE_DECISION (si connu)\n"
                    "• DESCRIPTION_OFFRE, PROFIL_CLIENT_IDEAL, PRIX_MOYEN\n\n"
                    "Collez le résultat obtenu de ChatGPT avec :\n"
                    "1. Le SCORE /100\n"
                    "2. Le DÉTAIL BANT (Budget XX/25 | Authority XX/25 | Need XX/25 | Timeline XX/25)\n"
                    "3. L'ACTION recommandée\n"
                    "4. Les POINTS DE VIGILANCE"
                ),
                "livrable": "Résultat complet du Prompt 1 BANT avec score, détail et action recommandée.",
                "example": "SCORE : 72/100\nDÉTAIL : Budget 18/25 | Authority 20/25 | Need 22/25 | Timeline 12/25\nACTION : Appel dans les 24h\nPOINTS DE VIGILANCE : Budget non confirmé, Timeline courte à vérifier"
            },
            "hints_fr": [
                {"level": 1, "text": "Copiez le Prompt 1 BANT depuis la section Templates, remplacez toutes les variables entre crochets."},
                {"level": 2, "text": "Si vous n'avez pas de vrai lead, inventez : Karim Ben Ali, Directeur Commercial, PME tech à Tunis, 50 employés, besoin CRM."},
                {"level": 3, "text": "Le format de sortie doit inclure SCORE, DÉTAIL, ACTION et POINTS DE VIGILANCE — si ChatGPT ne les donne pas, relancez avec 'Respecte exactement le format demandé'."}
            ],
            "rubric_fr": {
                "criteres": [
                    {"nom": "Score BANT fourni avec décomposition", "poids": 0.4},
                    {"nom": "Action recommandée cohérente avec le score", "poids": 0.3},
                    {"nom": "Points de vigilance pertinents", "poids": 0.3}
                ]
            }
        },

        # CP4 — Mission terrain (Unit 4)
        4: {
            "type": "exercise",
            "title_fr": "Checkpoint 4 — Mission : Score tes 10 derniers leads",
            "is_assessed": True,
            "passing_score": 0,
            "has_hints": True,
            "content_fr": {
                "consigne": (
                    "Mission complète (60 minutes) — Appliquez BANT sur vos vrais leads :\n\n"
                    "1. Sélectionnez vos 10 derniers leads non qualifiés\n"
                    "2. Chronométrez la qualification manuelle sur 3 premiers (baseline)\n"
                    "3. Appliquez le Prompt 1 BANT sur les 7 suivants\n"
                    "4. Comparez : intuition vs IA pour chaque lead\n"
                    "5. Construisez votre plan d'action 14 jours\n\n"
                    "Soumettez un tableau récapitulatif avec :\n"
                    "• Lead | Score intuition | Score BANT IA | Écart | Action"
                ),
                "livrable": "Tableau de 10 leads avec scores, écarts et plan d'action 14 jours.",
                "success_criteria": [
                    "10 leads scorés en moins de 30 minutes total",
                    "≥ 3 leads avec écart ≥ 25 points entre intuition et IA",
                    "Plan d'action concret défini pour les 10 leads"
                ]
            },
            "hints_fr": [
                {"level": 1, "text": "Commencez par préparer votre bloc 'MON OFFRE' réutilisable — vous ne l'écrirez qu'une fois."},
                {"level": 2, "text": "Pour les leads en arabe, traduisez les infos clés en français avant de les coller dans le prompt."},
                {"level": 3, "text": "Si vous n'avez pas 10 leads réels, utilisez 5 leads réels + 5 leads fictifs réalistes."}
            ],
            "rubric_fr": {
                "criteres": [
                    {"nom": "Tableau complet avec 10 leads scorés", "poids": 0.4},
                    {"nom": "Comparaison intuition vs IA documentée", "poids": 0.3},
                    {"nom": "Plan d'action 14 jours concret", "poids": 0.3}
                ]
            }
        },

        # CP5 — KPI Measurement (Unit 5)
        5: {
            "type": "quiz",
            "title_fr": "Checkpoint 5 — Bilan et mesure d'impact",
            "is_assessed": True,
            "passing_score": 60,
            "has_hints": False,
            "content_fr": {
                "questions": [
                    {
                        "id": "q1",
                        "question": "À quel horizon temporel mesure-t-on l'impact sur le close rate après ce module ?",
                        "options": [
                            "J+3 (3 jours)",
                            "J+14 (2 semaines)",
                            "J+30/J+60 (observatoire)",
                            "J+180 (6 mois)"
                        ],
                        "correct": "C",
                        "explanation": "Le close rate est un KPI long terme — il faut J+30/J+60 pour observer l'impact réel sur la conversion."
                    },
                    {
                        "id": "q2",
                        "question": "Quelle réduction du temps de qualification par lead est attendue après avoir maîtrisé ce module ?",
                        "options": [
                            "10-20%",
                            "30-40%",
                            "70-80%",
                            "95-100%"
                        ],
                        "correct": "C",
                        "explanation": "Le module vise une réduction de 70-80% du temps de qualification — de 10 min/lead à 2-3 min/lead avec BANT IA."
                    }
                ]
            },
            "hints_fr": [],
            "rubric_fr": None
        }
    }
}


# =============================================================================
# Génération automatique pour les autres modules
# (structure identique, questions génériques)
# =============================================================================

def make_generic_checkpoints(module_id: int, module_title: str) -> dict:
    """Génère des checkpoints génériques pour les modules sans contenu spécifique."""
    return {
        1: {
            "type": "quiz",
            "title_fr": f"Checkpoint 1 — Comprendre le problème business",
            "is_assessed": True,
            "passing_score": 70,
            "has_hints": True,
            "content_fr": {
                "questions": [
                    {
                        "id": "q1",
                        "question": f"Quel est l'objectif principal du module '{module_title}' ?",
                        "options": [
                            "Apprendre à coder en Python",
                            "Automatiser et optimiser un processus métier avec l'IA",
                            "Gérer les ressources humaines",
                            "Créer des sites web"
                        ],
                        "correct": "B",
                        "explanation": "Ce module vise à automatiser et optimiser un processus métier clé grâce à l'IA."
                    },
                    {
                        "id": "q2",
                        "question": "Quel niveau de réduction du temps de travail manuel est typiquement attendu après ce module ?",
                        "options": ["10-20%", "30-40%", "50-80%", "100%"],
                        "correct": "C",
                        "explanation": "Les modules Euklydia visent une réduction de 50-80% du temps sur les tâches manuelles répétitives."
                    },
                    {
                        "id": "q3",
                        "question": "À quelle fréquence doit-on mesurer l'impact d'un module sur les KPIs business ?",
                        "options": [
                            "Une seule fois à la fin",
                            "Jamais — les résultats parlent d'eux-mêmes",
                            "J+14 et J+30/J+60 (court + moyen terme)",
                            "Uniquement J+7"
                        ],
                        "correct": "C",
                        "explanation": "Le pattern temporel Euklydia mesure à J+14 (productivité) et J+30/J+60 (impact business)."
                    }
                ]
            },
            "hints_fr": [
                {"level": 1, "text": "Relisez la section Use Case pour comprendre le problème business adressé."},
                {"level": 2, "text": "Les KPIs du module donnent des chiffres précis sur les résultats attendus."}
            ],
            "rubric_fr": None
        },
        2: {
            "type": "quiz",
            "title_fr": "Checkpoint 2 — Compétences clés",
            "is_assessed": True,
            "passing_score": 60,
            "has_hints": True,
            "content_fr": {
                "questions": [
                    {
                        "id": "q1",
                        "question": "Combien de compétences clés ce module développe-t-il ?",
                        "options": ["3", "5", "7-8", "10+"],
                        "correct": "C",
                        "explanation": "Chaque module Euklydia développe 7-8 compétences précises, du niveau Connaissance au niveau Maîtrise."
                    },
                    {
                        "id": "q2",
                        "question": "Quel est le but principal de l'auto-évaluation initiale ?",
                        "options": [
                            "Obtenir une note",
                            "Identifier ses compétences faibles à prioriser",
                            "Comparer avec les autres apprenants",
                            "Valider le module"
                        ],
                        "correct": "B",
                        "explanation": "L'auto-évaluation permet d'identifier les gaps spécifiques et de personnaliser le parcours."
                    }
                ]
            },
            "hints_fr": [
                {"level": 1, "text": "Regardez la section Compétences clés pour compter les compétences développées."}
            ],
            "rubric_fr": None
        },
        3: {
            "type": "exercise",
            "title_fr": "Checkpoint 3 — Appliquer un prompt du module",
            "is_assessed": True,
            "passing_score": 0,
            "has_hints": True,
            "content_fr": {
                "consigne": (
                    f"Choisissez l'un des prompts de la section Execution Content.\n\n"
                    "Appliquez-le sur un cas réel de votre travail (ou un cas fictif réaliste).\n\n"
                    "Soumettez :\n"
                    "1. Le prompt utilisé avec vos variables remplies\n"
                    "2. Le résultat obtenu de ChatGPT\n"
                    "3. Votre analyse : est-ce que le résultat est utilisable directement ?"
                ),
                "livrable": "Prompt rempli + résultat ChatGPT + analyse d'utilisabilité."
            },
            "hints_fr": [
                {"level": 1, "text": "Commencez par le Prompt 1 — c'est le plus simple et le plus fondamental."},
                {"level": 2, "text": "Remplacez toutes les variables entre crochets [VARIABLE] par vos vraies données."},
                {"level": 3, "text": "Si le résultat n'est pas satisfaisant, ajoutez 'Réponds en français et respecte exactement le format demandé'."}
            ],
            "rubric_fr": {
                "criteres": [
                    {"nom": "Prompt correctement rempli avec vraies données", "poids": 0.4},
                    {"nom": "Résultat ChatGPT fourni", "poids": 0.3},
                    {"nom": "Analyse pertinente de l'utilisabilité", "poids": 0.3}
                ]
            }
        },
        4: {
            "type": "exercise",
            "title_fr": "Checkpoint 4 — Mission terrain",
            "is_assessed": True,
            "passing_score": 0,
            "has_hints": True,
            "content_fr": {
                "consigne": (
                    "Réalisez la mission terrain complète décrite dans la section Mission.\n\n"
                    "Soumettez un compte-rendu avec :\n"
                    "1. Ce que vous avez fait concrètement\n"
                    "2. Le temps que ça vous a pris\n"
                    "3. Les résultats obtenus vs les critères de réussite\n"
                    "4. Ce que vous feriez différemment la prochaine fois"
                ),
                "livrable": "Compte-rendu de mission avec résultats mesurés."
            },
            "hints_fr": [
                {"level": 1, "text": "Relisez les critères de réussite de la mission avant de commencer."},
                {"level": 2, "text": "Chronométrez-vous — le temps gagné est un KPI important."}
            ],
            "rubric_fr": {
                "criteres": [
                    {"nom": "Mission réalisée sur données réelles", "poids": 0.5},
                    {"nom": "Résultats mesurés vs critères de réussite", "poids": 0.3},
                    {"nom": "Réflexion sur l'amélioration", "poids": 0.2}
                ]
            }
        },
        5: {
            "type": "quiz",
            "title_fr": "Checkpoint 5 — Bilan et KPIs",
            "is_assessed": True,
            "passing_score": 60,
            "has_hints": False,
            "content_fr": {
                "questions": [
                    {
                        "id": "q1",
                        "question": "Quels sont les deux niveaux temporels de mesure des KPIs dans ce module ?",
                        "options": [
                            "J+1 et J+7",
                            "J+14 (court terme) et J+30/J+60 (observatoire)",
                            "J+30 et J+90",
                            "J+60 et J+180"
                        ],
                        "correct": "B",
                        "explanation": "Le pattern Euklydia : J+14 pour les KPIs de productivité, J+30/J+60 pour l'impact business."
                    },
                    {
                        "id": "q2",
                        "question": "Que faire si vous n'atteignez pas les KPIs cibles après J+14 ?",
                        "options": [
                            "Abandonner le module",
                            "Attendre que ça s'améliore seul",
                            "Revoir les sections difficiles et relancer les prompts sur de nouveaux cas",
                            "Changer d'outil"
                        ],
                        "correct": "C",
                        "explanation": "Si les KPIs ne sont pas atteints à J+14, il faut revoir les sections difficiles et s'exercer davantage."
                    }
                ]
            },
            "hints_fr": [],
            "rubric_fr": None
        }
    }


# =============================================================================
# Seed principal
# =============================================================================

def run():
    print("=" * 60)
    print("  SEED_CHECKPOINTS.PY — Euklydia")
    print("=" * 60)

    session = Session()
    try:
        # 1. Récupérer tous les modules avec leur mapping unit → first lesson
        modules = session.execute(text(
            "SELECT id, title_fr FROM modules WHERE is_active = true ORDER BY id"
        )).fetchall()

        print(f"\n📦 {len(modules)} modules trouvés")

        unit_lesson_map = {}
        rows = session.execute(text(
            "SELECT m.id as module_id, u.order as unit_order, MIN(l.id) as lesson_id "
            "FROM modules m "
            "JOIN units u ON u.module_id = m.id "
            "JOIN lessons l ON l.unit_id = u.id "
            "WHERE m.is_active = true "
            "GROUP BY m.id, u.order ORDER BY m.id, u.order"
        )).fetchall()

        for row in rows:
            mid = row.module_id
            if mid not in unit_lesson_map:
                unit_lesson_map[mid] = {}
            unit_lesson_map[mid][row.unit_order] = row.lesson_id

        created = 0
        skipped = 0

        for module_row in modules:
            module_id = module_row.id
            module_title = module_row.title_fr

            # Utiliser les checkpoints spécifiques ou génériques
            checkpoints = CHECKPOINTS.get(module_id) or make_generic_checkpoints(module_id, module_title)

            for unit_order, cp_data in checkpoints.items():
                lesson_id = unit_lesson_map.get(module_id, {}).get(unit_order)
                if not lesson_id:
                    print(f"  ⚠️ Module {module_id} Unit {unit_order} — pas de lesson_id trouvé")
                    continue

                # Vérifier si déjà seedé
                existing = session.execute(text(
                    "SELECT id FROM activities WHERE lesson_id = :lesson_id LIMIT 1"
                ), {"lesson_id": lesson_id}).fetchone()

                if existing:
                    skipped += 1
                    continue

                # Insérer l'activité checkpoint
                session.execute(text(
                    "INSERT INTO activities "
                    "(lesson_id, type, title_fr, title_en, content_fr, content_en, "
                    "\"order\", passing_score, is_required, is_assessed, has_hints, "
                    "hints_fr, hints_en, rubric_fr, rubric_en, is_active, created_at) "
                    "VALUES "
                    "(:lesson_id, :type, :title_fr, :title_fr, "
                    "CAST(:content_fr AS jsonb), CAST(:content_fr AS jsonb), "
                    "1, :passing_score, true, :is_assessed, :has_hints, "
                    "CAST(:hints_fr AS jsonb), CAST(:hints_fr AS jsonb), "
                    "CAST(:rubric_fr AS jsonb), CAST(:rubric_fr AS jsonb), "
                    "true, NOW())"
                ), {
                    "lesson_id":     lesson_id,
                    "type":          cp_data["type"],
                    "title_fr":      cp_data["title_fr"],
                    "content_fr":    json.dumps(cp_data["content_fr"], ensure_ascii=False),
                    "passing_score": cp_data["passing_score"],
                    "is_assessed":   cp_data["is_assessed"],
                    "has_hints":     cp_data["has_hints"],
                    "hints_fr":      json.dumps(cp_data.get("hints_fr") or [], ensure_ascii=False),
                    "rubric_fr":     json.dumps(cp_data.get("rubric_fr"), ensure_ascii=False) if cp_data.get("rubric_fr") else None,
                })
                created += 1

            session.commit()
            print(f"  ✅ Module {module_id} — {module_title[:40]} : checkpoints créés")

        print(f"\n{'=' * 60}")
        print(f"  ✅ Seed checkpoints terminé !")
        print(f"  → {created} activités créées")
        print(f"  → {skipped} déjà existantes (skip)")
        print(f"{'=' * 60}")

    except Exception as e:
        session.rollback()
        print(f"\n❌ Erreur : {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    run()