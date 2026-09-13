"""
fix_json_encoding.py
────────────────────
Corrige l'encodage cassé (Latin-1 interprété comme UTF-8) dans les fichiers
JSON des modules Euklydia.

Symptôme : "GÃ©nÃ¨re" au lieu de "Génère", "Ã " au lieu de "à", etc.
Cause    : le fichier JSON a été écrit en Latin-1 mais lu comme UTF-8.
Fix      : encoder chaque chaîne en Latin-1 puis décoder en UTF-8.

Usage :
    cd C:\\Users\\Ranim\\euklydia\\backend
    python app/scripts/fix_json_encoding.py
"""

import json
import os

# ── Liste des fichiers JSON à corriger ───────────────────────────────────
JSON_FILES = [
    "content/roles/ai_sales_specialist/module_1_lead_qualification.json",
    "content/roles/ai_sales_specialist/module_2_personalized_outreach.json",
    "content/roles/ai_sales_specialist/module_3_sales_call.json",
    "content/roles/ai_marketing_strategist/module_1_content_strategy.json",
    "content/roles/ai_marketing_strategist/module_2_campaign_performance.json",
    "content/roles/ai_marketing_strategist/module_3_audience_insights.json",
    "content/roles/ai_designer/module_1.json",
    "content/roles/ai_designer/module_2.json",
    "content/roles/ai_designer/module_3.json",
    "content/roles/ai_project_manager/module_1_project_planning_automation.json",
    "content/roles/ai_project_manager/module_2_risk_identification.json",
    "content/roles/ai_project_manager/module_3_team_productivity_optimization.json",
]


def fix_encoding(obj):
    """
    Parcourt récursivement un objet JSON et corrige les chaînes
    mal encodées (Latin-1 → UTF-8).
    """
    if isinstance(obj, str):
        try:
            # Tente de corriger : encode en Latin-1 puis décode en UTF-8
            fixed = obj.encode("latin-1").decode("utf-8")
            return fixed
        except (UnicodeEncodeError, UnicodeDecodeError):
            # La chaîne est déjà propre ou ne peut pas être corrigée
            return obj
    elif isinstance(obj, list):
        return [fix_encoding(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: fix_encoding(value) for key, value in obj.items()}
    else:
        return obj


def fix_file(json_path: str) -> bool:
    """
    Corrige l'encodage d'un fichier JSON.
    Retourne True si le fichier a été modifié, False sinon.
    """
    if not os.path.exists(json_path):
        print(f"  ❌ Fichier introuvable : {json_path}")
        return False

    with open(json_path, "r", encoding="utf-8") as f:
        original_content = f.read()
        data = json.loads(original_content)

    # Applique la correction récursive
    fixed_data = fix_encoding(data)

    # Sérialise en UTF-8 propre
    fixed_content = json.dumps(fixed_data, ensure_ascii=False, indent=2)

    # Compare pour savoir si quelque chose a changé
    if fixed_content == original_content:
        print(f"  ✅ Déjà propre : {json_path}")
        return False

    # Écrit le fichier corrigé
    with open(json_path, "w", encoding="utf-8") as f:
        f.write(fixed_content)

    print(f"  🔧 Corrigé : {json_path}")
    return True


def main():
    print("=== Correction encodage JSON (Latin-1 → UTF-8) ===\n")

    fixed_count   = 0
    already_clean = 0
    error_count   = 0

    for json_path in JSON_FILES:
        try:
            was_fixed = fix_file(json_path)
            if was_fixed:
                fixed_count += 1
            else:
                already_clean += 1
        except Exception as e:
            print(f"  ❌ Erreur sur {json_path} : {e}")
            error_count += 1

    print(f"\n=== Résultat ===")
    print(f"  🔧 Fichiers corrigés  : {fixed_count}")
    print(f"  ✅ Déjà propres       : {already_clean}")
    print(f"  ❌ Erreurs            : {error_count}")

    if fixed_count > 0:
        print(f"\n💡 N'oublie pas de committer les changements :")
        print(f"   git add content/roles/")
        print(f'   git commit -m "fix: correction encodage UTF-8 dans les JSON des modules"')


if __name__ == "__main__":
    main()