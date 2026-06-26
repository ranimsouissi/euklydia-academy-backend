"""
patch_resources_all_roles.py
=============================
Patch ciblé : met à jour uniquement la colonne section_content_fr
pour TOUS les rôles — lit les JSON de chaque rôle et update en base.

Usage :
    cd backend
    python -m app.scripts.patch_resources_all_roles

Pré-requis :
    - Les fichiers JSON ont été mis à jour avec la clé "resources"
    - Les modules sont déjà seedés en base
"""
from __future__ import annotations

import sys
import os
import json
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("❌ DATABASE_URL manquante dans .env")
    sys.exit(1)

from app.scripts.content_loader import load_role_modules

# Mapping role_slug → role (valeur stockée en base)
ROLES = {
    "ai_sales_specialist":       "AI Sales Specialist",
    "ai_marketing_strategist":   "AI Marketing Strategist",
    "ai_designer":               "AI Designer",
    "ai_project_manager":        "AI Project Manager",
}


def patch_role(session, role_slug: str, role_name: str):
    print(f"\n📂 Rôle : {role_name}")
    print(f"   Chargement depuis content/roles/{role_slug}/...")

    try:
        modules_data = load_role_modules(role_slug)
    except Exception as e:
        print(f"   ❌ Erreur chargement JSON : {e}")
        return 0, 1

    updated = 0
    errors = 0

    for module_data in modules_data:
        title = module_data["title"]
        section_content = module_data["section_content"]

        if "resources" not in section_content:
            print(f"   ⚠️  '{title}' : clé 'resources' absente — skip")
            errors += 1
            continue

        nb_resources = len(section_content["resources"])

        resources = section_content.get("resources", [])
        result = session.execute(text("""
            UPDATE modules
            SET
                section_content_fr = CAST(:section_content AS jsonb),
                section_content_en = CAST(:section_content AS jsonb),
                references_fr      = CAST(:references AS jsonb)
            WHERE
                role = :role
                AND title_fr = :title
        """), {
            "section_content": json.dumps(section_content, ensure_ascii=False),
            "references":      json.dumps(resources, ensure_ascii=False),
            "role": role_name,
            "title": title,
        })

        if result.rowcount == 0:
            print(f"   ❌ '{title}' : introuvable en base")
            errors += 1
        else:
            print(f"   ✅ '{title}' : {nb_resources} resources ajoutées")
            updated += 1

    return updated, errors


def run():
    print("=" * 60)
    print("  PATCH — resources[] dans section_content_fr")
    print("  Tous les rôles")
    print("=" * 60)

    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    total_updated = 0
    total_errors = 0

    try:
        for role_slug, role_name in ROLES.items():
            updated, errors = patch_role(session, role_slug, role_name)
            total_updated += updated
            total_errors += errors

        session.commit()

        print("\n" + "=" * 60)
        print(f"  ✅ Patch terminé !")
        print(f"  → {total_updated} modules mis à jour")
        if total_errors:
            print(f"  ⚠️  {total_errors} erreurs — vérifiez les messages ci-dessus")
        print("=" * 60)

    except Exception as e:
        session.rollback()
        print(f"\n❌ Erreur fatale : {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    run()