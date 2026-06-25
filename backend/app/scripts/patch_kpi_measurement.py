"""
patch_kpi_measurement.py — Ajoute kpi_measurement_method dans les 8 modules manquants

Pour chaque module sans kpi_measurement_method dans section_content_fr :
  1. Ajoute le champ dans le JSON source (content/roles/...)
  2. Met à jour la colonne section_content_fr en BD

Idempotent : skip si le champ existe déjà.

Lancement :
    python -m app.scripts.patch_kpi_measurement
"""
from __future__ import annotations
import sys, os, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.db.session import SessionLocal
from app.models.module import Module

# =============================================================================
# Jalons par défaut (communs à tous les modules)
# =============================================================================
DEFAULT_MILESTONES = [
    {"when": "J0",   "what": "Formulaire de baseline auto-affiché en début de module (obligatoire pour valider le module)"},
    {"when": "J+7",  "what": "Rappel par email + notification in-app"},
    {"when": "J+14", "what": "Formulaire de mesure d'impact auto-affiché + rappel"},
    {"when": "J+30", "what": "Rappel facultatif pour le KPI observatoire"},
    {"when": "J+60", "what": "Rappel facultatif final + consolidation dashboard"},
]

# =============================================================================
# Jalons spécifiques par module (titre du module → jalons personnalisés)
# =============================================================================
CUSTOM_MILESTONES = {
    "Personalized Outreach at Scale": [
        {"when": "J0",   "what": "Mesure ton reply rate actuel et nombre de RDV qualifiés/semaine (baseline)"},
        {"when": "J+7",  "what": "Rappel par email + notification in-app"},
        {"when": "J+14", "what": "Mesure reply rate et RDV/semaine après la séquence — compare à ta baseline"},
        {"when": "J+30", "what": "Rappel facultatif — impact durable sur le pipeline (RDV → opportunités)"},
        {"when": "J+60", "what": "Consolidation finale — impact long terme sur la conversion"},
    ],
    "Sales Call Preparation": [
        {"when": "J0",   "what": "Mesure ton temps de préparation par appel et ton taux de documentation CRM (baseline)"},
        {"when": "J+7",  "what": "Rappel par email + notification in-app"},
        {"when": "J+14", "what": "Mesure temps de prep et % appels documentés — compare à ta baseline"},
        {"when": "J+30", "what": "Rappel facultatif — close rate observatoire (cycles longs)"},
        {"when": "J+60", "what": "Consolidation finale — impact sur le close rate et la qualité pipeline"},
    ],
    "Campaign Performance Optimization": [
        {"when": "J0",   "what": "Mesure tes KPIs campagne actuels : CPA, ROAS, CTR (baseline)"},
        {"when": "J+7",  "what": "Rappel par email + notification in-app"},
        {"when": "J+14", "what": "Compare tes KPIs campagne avant/après optimisation IA"},
        {"when": "J+30", "what": "Rappel facultatif — impact sur le ROI campagne (moyen terme)"},
        {"when": "J+60", "what": "Consolidation finale — impact long terme sur le budget optimisé"},
    ],
    "Audience Insights & Segmentation": [
        {"when": "J0",   "what": "Mesure ton taux de segmentation actuel et la précision de tes personas (baseline)"},
        {"when": "J+7",  "what": "Rappel par email + notification in-app"},
        {"when": "J+14", "what": "Compare l'engagement par segment avant/après segmentation IA"},
        {"when": "J+30", "what": "Rappel facultatif — impact sur la conversion par persona"},
        {"when": "J+60", "what": "Consolidation finale — ROI de la segmentation sur les campagnes"},
    ],
    "UX Optimization": [
        {"when": "J0",   "what": "Mesure tes métriques UX actuels : taux de conversion, bounce rate, time-on-page (baseline)"},
        {"when": "J+7",  "what": "Rappel par email + notification in-app"},
        {"when": "J+14", "what": "Compare les métriques UX avant/après optimisation IA"},
        {"when": "J+30", "what": "Rappel facultatif — impact sur la conversion (observatoire)"},
        {"when": "J+60", "what": "Consolidation finale — impact long terme sur les conversions"},
    ],
    "Design System Automation": [
        {"when": "J0",   "what": "Mesure ton temps de production design actuel et ton taux de réutilisation composants (baseline)"},
        {"when": "J+7",  "what": "Rappel par email + notification in-app"},
        {"when": "J+14", "what": "Compare temps de production et cohérence design avant/après automation"},
        {"when": "J+30", "what": "Rappel facultatif — impact sur la vélocité de l'équipe design"},
        {"when": "J+60", "what": "Consolidation finale — ROI du design system automatisé"},
    ],
    "Risk Identification": [
        {"when": "J0",   "what": "Mesure ton taux de détection des risques actuel et ton délai moyen d'identification (baseline)"},
        {"when": "J+7",  "what": "Rappel par email + notification in-app"},
        {"when": "J+14", "what": "Compare le nombre de risques détectés avant/après IA"},
        {"when": "J+30", "what": "Rappel facultatif — impact sur la mitigation des risques projet"},
        {"when": "J+60", "what": "Consolidation finale — réduction des incidents non anticipés"},
    ],
    "Team Productivity Optimization": [
        {"when": "J0",   "what": "Mesure la productivité actuelle de ton équipe : tâches complétées, délais, blockers (baseline)"},
        {"when": "J+7",  "what": "Rappel par email + notification in-app"},
        {"when": "J+14", "what": "Compare la productivité équipe avant/après optimisation IA"},
        {"when": "J+30", "what": "Rappel facultatif — impact sur la vélocité des sprints"},
        {"when": "J+60", "what": "Consolidation finale — ROI de l'optimisation sur les livrables"},
    ],
}

# =============================================================================
# Mapping titre_module → chemin JSON
# =============================================================================
BASE_CONTENT = os.path.join(
    os.path.dirname(__file__), '..', '..', 'content', 'roles'
)

JSON_FILES = {
    "Personalized Outreach at Scale":    "ai_sales_specialist/module_2_personalized_outreach.json",
    "Sales Call Preparation":            "ai_sales_specialist/module_3_sales_call.json",
    "Campaign Performance Optimization": "ai_marketing_strategist/module_2_campaign_performance.json",
    "Audience Insights & Segmentation":  "ai_marketing_strategist/module_3_audience_insights.json",
    "UX Optimization":                   "ai_designer/module_2.json",
    "Design System Automation":          "ai_designer/module_3.json",
    "Risk Identification":               "ai_project_manager/module_2_risk_identification.json",
    "Team Productivity Optimization":    "ai_project_manager/module_3_team_productivity_optimization.json",
}


def patch_module(db, title_en: str, json_rel_path: str) -> bool:
    """
    Ajoute kpi_measurement_method dans section_content_fr du module.
    Retourne True si modifié, False si déjà présent (skip).
    """
    # ── 1. Charger le module depuis la BD ─────────────────────────────────────
    module = db.query(Module).filter(Module.title_en == title_en).first()
    if not module:
        print(f"  ⚠️  Module '{title_en}' introuvable en BD — skip")
        return False

    # ── 2. Vérifier si déjà présent ───────────────────────────────────────────
    section = module.section_content_fr or {}
    if isinstance(section, str):
        section = json.loads(section)

    if "kpi_measurement_method" in section:
        print(f"  ⏭️  '{title_en}' — kpi_measurement_method déjà présent, skip")
        return False

    # ── 3. Construire le bloc kpi_measurement_method ──────────────────────────
    milestones = CUSTOM_MILESTONES.get(title_en, DEFAULT_MILESTONES)
    kpi_block = {
        "title": "Méthode de collecte des KPIs",
        "milestones": milestones,
    }

    # ── 4. Mettre à jour la BD ────────────────────────────────────────────────
    section["kpi_measurement_method"] = kpi_block
    module.section_content_fr = section
    # Forcer SQLAlchemy à détecter le changement sur colonne JSON
    from sqlalchemy.orm.attributes import flag_modified
    flag_modified(module, "section_content_fr")
    db.flush()

    # ── 5. Mettre à jour le JSON source ───────────────────────────────────────
    json_path = os.path.join(BASE_CONTENT, json_rel_path.replace('/', os.sep))
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        if "section_content" in json_data:
            json_data["section_content"]["kpi_measurement_method"] = kpi_block
        else:
            json_data["section_content"] = {"kpi_measurement_method": kpi_block}

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        print(f"  ✅ JSON mis à jour : {json_rel_path}")
    else:
        print(f"  ⚠️  JSON non trouvé : {json_path} — BD mise à jour uniquement")

    return True


def main():
    db = SessionLocal()
    try:
        print("\n🔧 Patch kpi_measurement_method — Euklydia Academy")
        print("=" * 60)

        modified = 0
        skipped  = 0

        for title, json_path in JSON_FILES.items():
            print(f"\n📦 {title}")
            result = patch_module(db, title, json_path)
            if result:
                modified += 1
            else:
                skipped += 1

        db.commit()

        print("\n" + "=" * 60)
        print(f"✅ Patch terminé")
        print(f"   • Modules mis à jour : {modified}")
        print(f"   • Modules skippés    : {skipped}")
        print("=" * 60)

    except Exception as e:
        db.rollback()
        print(f"\n❌ Erreur : {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()