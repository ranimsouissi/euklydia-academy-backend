"""
sync_db_to_json.py
──────────────────
Synchronise tutorials_fr et references_fr depuis la base de données
vers les fichiers JSON des modules (Direction : Base → JSON).

Pourquoi : la base contient la version enrichie et correctement encodée
(UTF-8) de ces deux champs, alors que les JSON ont divergé (encodage cassé
pour tutorials, structure incomplète pour references).

Usage :
    cd C:\\Users\\Ranim\\euklydia\\backend
    python app/scripts/sync_db_to_json.py
"""

import json
import os
import psycopg2
from dotenv import load_dotenv

# ── Chargement de l'environnement ─────────────────────────────────────────
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL manquant dans .env")

# Convertit le format SQLAlchemy → format psycopg2
# postgresql+psycopg2://user:pass@host:port/db → postgresql://user:pass@host:port/db
DATABASE_URL = DATABASE_URL.replace("postgresql+psycopg2://", "postgresql://")
# ── Correspondance module_id → chemin JSON ────────────────────────────────
# Adapté à la structure content/roles/ de ton projet
MODULE_JSON_MAP = {
    403: "content/roles/ai_sales_specialist/module_1_lead_qualification.json",
    404: "content/roles/ai_sales_specialist/module_2_personalized_outreach.json",
    405: "content/roles/ai_sales_specialist/module_3_sales_call.json",
    406: "content/roles/ai_marketing_strategist/module_1_content_strategy.json",
    407: "content/roles/ai_marketing_strategist/module_2_campaign_performance.json",
    408: "content/roles/ai_marketing_strategist/module_3_audience_insights.json",
    409: "content/roles/ai_designer/module_1.json",
    410: "content/roles/ai_designer/module_2.json",
    411: "content/roles/ai_designer/module_3.json",
    412: "content/roles/ai_project_manager/module_1_project_planning_automation.json",
    413: "content/roles/ai_project_manager/module_2_risk_identification.json",
    414: "content/roles/ai_project_manager/module_3_team_productivity_optimization.json",
}

def sync():
    print("=== Synchronisation Base → JSON ===\n")

    conn = psycopg2.connect(DATABASE_URL)
    cur  = conn.cursor()

    cur.execute("""
        SELECT id, title_fr, tutorials_fr, references_fr
        FROM modules
        WHERE id = ANY(%s)
        ORDER BY id
    """, (list(MODULE_JSON_MAP.keys()),))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    updated = 0
    errors  = 0

    for module_id, title_fr, tutorials_fr, references_fr in rows:
        json_path = MODULE_JSON_MAP.get(module_id)
        if not json_path:
            print(f"  ⚠️  Module {module_id} — aucun JSON mappé, ignoré")
            continue

        if not os.path.exists(json_path):
            print(f"  ❌ Module {module_id} ({title_fr}) — fichier introuvable : {json_path}")
            errors += 1
            continue

        try:
            # Lecture du JSON existant
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Mise à jour des deux champs depuis la base
            if tutorials_fr:
                data["tutorials_fr"] = tutorials_fr
                print(f"  ✅ Module {module_id} ({title_fr}) — tutorials_fr mis à jour ({len(tutorials_fr)} tutoriels)")
            else:
                print(f"  ⚠️  Module {module_id} ({title_fr}) — tutorials_fr vide en base, ignoré")

            if references_fr:
                data["references_fr"] = references_fr
                print(f"  ✅ Module {module_id} ({title_fr}) — references_fr mis à jour ({len(references_fr)} références)")
            else:
                print(f"  ⚠️  Module {module_id} ({title_fr}) — references_fr vide en base, ignoré")

            # Sauvegarde du JSON (UTF-8, indenté, sans encodage ascii)
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            updated += 1

        except Exception as e:
            print(f"  ❌ Module {module_id} ({title_fr}) — erreur : {e}")
            errors += 1

    print(f"\n=== Résultat : {updated} modules mis à jour, {errors} erreurs ===")

if __name__ == "__main__":
    sync()