"""
content_loader.py — Utilitaire de chargement du contenu pédagogique JSON.

Charge le contenu depuis `backend/content/` pour les seeds.
Source de vérité : les fichiers JSON dans content/diagnostics/ et content/roles/.

Architecture (Option 3) :
    backend/
    ├── content/
    │   ├── diagnostics/
    │   │   └── ai_sales_specialist.json
    │   └── roles/
    │       └── ai_sales_specialist/
    │           ├── module_1_lead_qualification.json
    │           ├── module_2_personalized_outreach.json
    │           └── module_3_sales_call.json
    └── app/
        └── scripts/
            ├── content_loader.py         ← CE FICHIER
            ├── seed_ai_sales_specialist_diagnostic.py
            └── seed_ai_sales_specialist_modules.py

Usage dans un seed :
    from app.scripts.content_loader import load_diagnostic, load_role_modules

    diagnostic = load_diagnostic("ai_sales_specialist")
    modules = load_role_modules("ai_sales_specialist")
"""
from __future__ import annotations

import json
from pathlib import Path


# =============================================================================
# Localisation de la racine du backend
# =============================================================================
# Ce fichier est dans : backend/app/scripts/content_loader.py
# La racine du backend est donc à 3 niveaux au-dessus.
BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent
CONTENT_DIR = BACKEND_ROOT / "content"
DIAGNOSTICS_DIR = CONTENT_DIR / "diagnostics"
ROLES_DIR = CONTENT_DIR / "roles"


# =============================================================================
# Exceptions custom (pour des erreurs claires)
# =============================================================================
class ContentLoaderError(Exception):
    """Erreur générique de chargement du contenu."""
    pass


class ContentFileNotFound(ContentLoaderError):
    """Fichier JSON introuvable."""
    pass


class InvalidContentStructure(ContentLoaderError):
    """Structure JSON invalide (champs manquants, format incorrect)."""
    pass


# =============================================================================
# Utilitaires internes
# =============================================================================
def _load_json_file(path: Path) -> dict:
    """Charge un fichier JSON avec gestion d'erreurs claire."""
    if not path.exists():
        raise ContentFileNotFound(
            f"Fichier de contenu introuvable : {path}\n"
            f"Vérifie que le dossier backend/content/ est bien en place."
        )
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise InvalidContentStructure(
            f"JSON invalide dans {path.name} (ligne {e.lineno}, col {e.colno}) : {e.msg}"
        ) from e


# =============================================================================
# API publique
# =============================================================================
def load_diagnostic(role_slug: str) -> dict:
    """
    Charge le diagnostic d'un rôle (skills + questions).

    Args:
        role_slug: identifiant snake_case du rôle (ex: 'ai_sales_specialist')

    Returns:
        dict avec les clés : role, career_path_id, source, skills, questions, scoring_logic

    Raises:
        ContentFileNotFound: si le fichier n'existe pas
        InvalidContentStructure: si le JSON est invalide ou des champs requis manquent
    """
    path = DIAGNOSTICS_DIR / f"{role_slug}.json"
    data = _load_json_file(path)

    # Validation minimale de structure
    required_keys = ["role", "career_path_id", "skills", "questions"]
    missing = [k for k in required_keys if k not in data]
    if missing:
        raise InvalidContentStructure(
            f"{path.name} : clés manquantes au niveau racine : {missing}"
        )

    if not isinstance(data["skills"], list) or len(data["skills"]) == 0:
        raise InvalidContentStructure(
            f"{path.name} : 'skills' doit être une liste non vide"
        )

    if not isinstance(data["questions"], list) or len(data["questions"]) == 0:
        raise InvalidContentStructure(
            f"{path.name} : 'questions' doit être une liste non vide"
        )

    return data


def load_role_modules(role_slug: str) -> list[dict]:
    """
    Charge tous les modules d'un rôle, triés par display_order.

    Args:
        role_slug: identifiant snake_case du rôle (ex: 'ai_sales_specialist')

    Returns:
        Liste de dicts modules, triés par display_order (1, 2, 3, ...)

    Raises:
        ContentFileNotFound: si le dossier du rôle n'existe pas
        InvalidContentStructure: si un module a une structure invalide
    """
    role_dir = ROLES_DIR / role_slug
    if not role_dir.exists():
        raise ContentFileNotFound(
            f"Dossier du rôle introuvable : {role_dir}\n"
            f"Vérifie que les modules JSON sont bien dans backend/content/roles/{role_slug}/"
        )

    module_files = sorted(role_dir.glob("module_*.json"))
    if not module_files:
        raise ContentFileNotFound(
            f"Aucun fichier module_*.json trouvé dans {role_dir}"
        )

    modules = []
    for file_path in module_files:
        data = _load_json_file(file_path)

        # Validation minimale par module
        required_keys = [
            "display_order", "title", "skill_name", "level",
            "estimated_duration_min", "description", "learning_objective",
            "expected_outcome", "key_concepts", "prompt_examples",
            "practical_exercise", "comparison_tables", "section_content",
        ]
        missing = [k for k in required_keys if k not in data]
        if missing:
            raise InvalidContentStructure(
                f"{file_path.name} : clés manquantes : {missing}"
            )

        modules.append(data)

    # Tri par display_order pour garantir l'ordre logique (M1 → M2 → M3)
    modules.sort(key=lambda m: m["display_order"])

    return modules


def get_content_dir() -> Path:
    """Retourne le chemin absolu du dossier content/ (utile pour debug)."""
    return CONTENT_DIR


# =============================================================================
# Test d'intégrité (lancer ce fichier directement pour vérifier)
# =============================================================================
if __name__ == "__main__":
    """
    Permet de tester le module en standalone :
        python -m app.scripts.content_loader

    Vérifie que le contenu de AI Sales Specialist se charge correctement.
    """
    print(f"📂 CONTENT_DIR : {CONTENT_DIR}")
    print(f"📂 Existe : {CONTENT_DIR.exists()}")
    print()

    try:
        print("🔍 Chargement du diagnostic AI Sales Specialist...")
        diag = load_diagnostic("ai_sales_specialist")
        print(f"   ✅ Rôle : {diag['role']}")
        print(f"   ✅ Skills : {len(diag['skills'])}")
        print(f"   ✅ Questions : {len(diag['questions'])}")
        print()

        print("🔍 Chargement des modules AI Sales Specialist...")
        modules = load_role_modules("ai_sales_specialist")
        print(f"   ✅ Modules chargés : {len(modules)}")
        for m in modules:
            print(f"      • Module {m['display_order']} : {m['title']} ({m['level']}, {m['estimated_duration_min']} min)")

        print()
        print("🎉 content_loader fonctionne correctement !")

    except ContentLoaderError as e:
        print(f"❌ Erreur : {e}")
        import sys
        sys.exit(1)
