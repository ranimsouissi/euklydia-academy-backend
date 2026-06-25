"""
seed_tutorials_references.py
============================
Ajoute tutorials_fr, references_fr et progress_update_fr
aux modules existants via UPDATE (ne touche pas aux autres données).

Usage :
    cd backend
    python app/scripts/seed_tutorials_references.py
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
# DONNÉES — AI Marketing Strategist
# Source : Parcours_AI_Marketing_Strategist_v1_1.pdf
# ─────────────────────────────────────────────────────────────────────────────

MODULES_DATA = [

    # ── Module 406 — Content Strategy Optimization ───────────────────────────
    {
        "title_fr": "Content Strategy Optimization",
        "role": "AI Marketing Strategist",
        "tutorials_fr": [
            {
                "id": 1,
                "title": "Encode ta brand voice en 30 minutes",
                "duration_min": 15,
                "format": "screencast",
                "description": "Guide pas-à-pas pour encoder ta voix de marque dans un prompt maître réutilisable.",
                "template_url": None,
                "url": None
            },
            {
                "id": 2,
                "title": "Bâtis ton calendrier éditorial trimestriel",
                "duration_min": 20,
                "format": "screencast",
                "description": "Construis un calendrier 3 mois multi-canal aligné sur les saisonnalités Maghreb.",
                "template_url": None,
                "url": None
            }
        ],
        "references_fr": [
            {
                "source": "HubSpot Content Strategy Blog",
                "usage": "Frameworks de stratégie éditoriale B2B, benchmarks engagement",
                "url": "https://blog.hubspot.com/marketing"
            },
            {
                "source": "Notion AI Content Templates",
                "usage": "Templates de calendrier éditorial et structures d'articles",
                "url": "https://www.notion.so/templates"
            },
            {
                "source": "LinkedIn Marketing Solutions Blog",
                "usage": "Bonnes pratiques natives LinkedIn (formats, timing)",
                "url": "https://business.linkedin.com/marketing-solutions/blog"
            },
            {
                "source": "Meta Business Resources",
                "usage": "Best practices content social (Facebook, Instagram)",
                "url": "https://www.facebook.com/business/learn"
            },
            {
                "source": "Buffer & Hootsuite blogs",
                "usage": "Études de cas multi-canal et data engagement Maghreb/MENA",
                "url": "https://buffer.com/resources"
            }
        ],
        "progress_update_fr": {
            "kpi_label": "Taux d'engagement",
            "kpi_target": "+30 à +50 %",
            "skill_label": "AI Content Strategy & Creation",
            "deliverables": [
                "Comparatif KPI avant / après (taux d'engagement)",
                "Mise à jour du score skill 1 (Content Strategy)",
                "Bibliothèque personnelle des prompts utilisés et des contenus produits"
            ],
            "next_step": "Module 2 — Campaign Performance Optimization"
        }
    },

    # ── Module 407 — Campaign Performance Optimization ───────────────────────
    {
        "title_fr": "Campaign Performance Optimization",
        "role": "AI Marketing Strategist",
        "tutorials_fr": [
            {
                "id": 1,
                "title": "Génère 10 ad copies en 5 minutes",
                "duration_min": 10,
                "format": "screencast",
                "description": "Applique le Prompt 1 en live et génère 10 variantes d'ad copy testables.",
                "template_url": None,
                "url": None
            },
            {
                "id": 2,
                "title": "Lance ton premier A/B test rigoureux",
                "duration_min": 20,
                "format": "screencast",
                "description": "Configure un A/B test structuré sur Meta Ads avec hypothèse, variables et règle de décision.",
                "template_url": None,
                "url": None
            }
        ],
        "references_fr": [
            {
                "source": "Meta Ads AI Documentation",
                "usage": "Best practices Advantage+, Automated Rules, Dynamic Creative",
                "url": "https://www.facebook.com/business/ads"
            },
            {
                "source": "Google Ads Optimization Guides",
                "usage": "Smart Bidding, Responsive Search Ads, Performance Max",
                "url": "https://support.google.com/google-ads"
            },
            {
                "source": "AdCreative.ai blog",
                "usage": "Benchmarks créatifs par secteur et région",
                "url": "https://adcreative.ai/blog"
            },
            {
                "source": "TikTok Ads Maghreb insights",
                "usage": "Spécificités locales et formats UGC performants",
                "url": "https://ads.tiktok.com/business/creativecenter"
            },
            {
                "source": "HubSpot Marketing Blog",
                "usage": "Frameworks AIDA, PAS, growth marketing",
                "url": "https://blog.hubspot.com/marketing"
            }
        ],
        "progress_update_fr": {
            "kpi_label": "CAC (Coût d'Acquisition Client)",
            "kpi_target": "-20 à -30 %",
            "skill_label": "AI Campaign & Growth Optimization",
            "deliverables": [
                "Comparatif CAC avant / après",
                "Bibliothèque personnelle des créas testées (top 5 par performance)",
                "Mise à jour du score skill 2 (Campaign Performance)"
            ],
            "next_step": "Module 3 — Audience Insights & Segmentation"
        }
    },

    # ── Module 408 — Audience Insights & Segmentation ────────────────────────
    {
        "title_fr": "Audience Insights & Segmentation",
        "role": "AI Marketing Strategist",
        "tutorials_fr": [
            {
                "id": 1,
                "title": "Génère 4 personas data-driven en 30 minutes",
                "duration_min": 15,
                "format": "screencast",
                "description": "Applique le framework Data-to-Insight pour construire des personas actionnables depuis tes données.",
                "template_url": None,
                "url": None
            },
            {
                "id": 2,
                "title": "Configure une audience custom Meta basée sur tes personas",
                "duration_min": 20,
                "format": "screencast",
                "description": "Sync tes personas vers Meta Ads et configure des audiences personnalisées.",
                "template_url": None,
                "url": None
            }
        ],
        "references_fr": [
            {
                "source": "Segment Segmentation Resources",
                "usage": "Frameworks officiels de segmentation et CDP best practices",
                "url": "https://segment.com/academy"
            },
            {
                "source": "Mixpanel User Insights blog",
                "usage": "Cas d'usage analyse comportementale produit",
                "url": "https://mixpanel.com/blog"
            },
            {
                "source": "Amplitude Behavioral Analytics Playbook",
                "usage": "Méthodologies RFM et cohortes",
                "url": "https://amplitude.com/blog"
            },
            {
                "source": "Google Analytics 4 Help Center",
                "usage": "Audiences prédictives et machine learning natif",
                "url": "https://support.google.com/analytics"
            },
            {
                "source": "Meta Audience Insights documentation",
                "usage": "Custom Audiences et Lookalike best practices",
                "url": "https://www.facebook.com/business/help"
            }
        ],
        "progress_update_fr": {
            "kpi_label": "Taux de conversion (campagnes ciblées)",
            "kpi_target": "+25 %",
            "skill_label": "AI Audience Intelligence",
            "deliverables": [
                "Comparatif taux de conversion ciblé vs large",
                "Bibliothèque personnelle de personas avec messaging associé",
                "Mise à jour du score skill 3 (Audience Insights)",
                "Vue consolidée des 3 modules : parcours AI Marketing Strategist terminé"
            ],
            "next_step": "Parcours AI Marketing Strategist complété ✅"
        }
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# PIPELINE UPDATE
# ─────────────────────────────────────────────────────────────────────────────

def run():
    print("=" * 60)
    print("  SEED TUTORIALS & REFERENCES — AI Marketing Strategist")
    print("=" * 60)

    with engine.connect() as conn:
        updated = 0
        errors = 0

        for module_data in MODULES_DATA:
            try:
                result = conn.execute(text("""
                    UPDATE modules
                    SET
                        tutorials_fr      = cast(:tutorials_fr as jsonb),
                        references_fr     = cast(:references_fr as jsonb),
                        progress_update_fr = cast(:progress_update_fr as jsonb)
                    WHERE title_fr = :title_fr
                      AND role = :role
                    RETURNING id, title_fr
                """), {
                    "title_fr":          module_data["title_fr"],
                    "role":              module_data["role"],
                    "tutorials_fr":      json.dumps(module_data["tutorials_fr"], ensure_ascii=False),
                    "references_fr":     json.dumps(module_data["references_fr"], ensure_ascii=False),
                    "progress_update_fr": json.dumps(module_data["progress_update_fr"], ensure_ascii=False),
                })

                row = result.fetchone()
                if row:
                    print(f"  ✅ Module {row.id} — {row.title_fr}")
                    updated += 1
                else:
                    print(f"  ⚠️  Module non trouvé : {module_data['title_fr']}")

            except Exception as e:
                print(f"  ❌ Erreur sur {module_data['title_fr']} : {e}")
                errors += 1

        conn.commit()

    print("\n" + "=" * 60)
    print(f"  ✅ {updated} modules mis à jour")
    if errors:
        print(f"  ❌ {errors} erreurs")
    print("=" * 60)
    print("\n⏭  Prochaine étape : partagez les PDFs AI Designer,")
    print("   AI Project Manager et AI Sales Specialist")
    print("   pour compléter les 9 modules restants.")


if __name__ == "__main__":
    run()