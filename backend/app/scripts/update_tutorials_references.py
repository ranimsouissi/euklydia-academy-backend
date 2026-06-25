"""
update_tutorials_references.py
================================
Lit les JSON depuis content/roles/ et met à jour les colonnes
tutorials_fr, references_fr, progress_update_fr dans la DB.

Les données sont extraites de section_content.tutorials et
section_content.references qui existent déjà dans les JSON.

Usage :
    cd backend
    python app/scripts/update_tutorials_references.py
"""

import os
import sys
import json
from pathlib import Path
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
# Chemin vers les JSON
# ─────────────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONTENT_DIR = BASE_DIR / "content" / "roles"

ROLES = [
    "ai_marketing_strategist",
    "ai_designer",
    "ai_project_manager",
    "ai_sales_specialist",
]

ROLE_LABELS = {
    "ai_marketing_strategist": "AI Marketing Strategist",
    "ai_designer": "AI Designer",
    "ai_project_manager": "AI Project Manager",
    "ai_sales_specialist": "AI Sales Specialist",
}


def extract_tutorials(section_content: dict) -> list | None:
    """Extrait tutorials depuis section_content."""
    if not section_content:
        return None
    tutorials = section_content.get("tutorials")
    if tutorials and isinstance(tutorials, list):
        return tutorials
    return None


def extract_references(section_content: dict) -> list | None:
    """Extrait references depuis section_content.references.sources."""
    if not section_content:
        return None
    refs = section_content.get("references")
    if not refs:
        return None
    sources = refs.get("sources")
    if sources and isinstance(sources, list):
        return sources
    return None


def extract_progress_update(section_content: dict) -> dict | None:
    """Extrait progress_update depuis section_content si présent."""
    if not section_content:
        return None
    return section_content.get("progress_update")


def run():
    print("=" * 60)
    print("  UPDATE TUTORIALS & REFERENCES — Tous les rôles")
    print("=" * 60)

    total_updated = 0
    total_errors = 0
    total_skipped = 0

    with engine.connect() as conn:
        for role_slug in ROLES:
            role_label = ROLE_LABELS[role_slug]
            role_dir = CONTENT_DIR / role_slug

            if not role_dir.exists():
                print(f"\n⚠️  Dossier introuvable : {role_dir}")
                continue

            json_files = sorted(role_dir.glob("module_*.json"))
            if not json_files:
                print(f"\n⚠️  Aucun JSON dans : {role_dir}")
                continue

            print(f"\n📦 {role_label} ({len(json_files)} modules)")

            for json_file in json_files:
                try:
                    with open(json_file, encoding="utf-8") as f:
                        data = json.load(f)

                    title_fr = data.get("title")
                    section_content = data.get("section_content", {})

                    if not title_fr:
                        print(f"  ⚠️  Pas de title dans {json_file.name}")
                        total_skipped += 1
                        continue

                    tutorials = extract_tutorials(section_content)
                    references = extract_references(section_content)
                    progress_update = extract_progress_update(section_content)

                    if not tutorials and not references and not progress_update:
                        print(f"  ⚠️  {title_fr} — aucune donnée à migrer dans section_content")
                        total_skipped += 1
                        continue

                    result = conn.execute(text("""
                        UPDATE modules
                        SET
                            tutorials_fr       = cast(:tutorials_fr as jsonb),
                            references_fr      = cast(:references_fr as jsonb),
                            progress_update_fr = cast(:progress_update_fr as jsonb)
                        WHERE title_fr = :title_fr
                          AND role     = :role
                        RETURNING id, title_fr
                    """), {
                        "title_fr":          title_fr,
                        "role":              role_label,
                        "tutorials_fr":      json.dumps(tutorials, ensure_ascii=False) if tutorials else "null",
                        "references_fr":     json.dumps(references, ensure_ascii=False) if references else "null",
                        "progress_update_fr": json.dumps(progress_update, ensure_ascii=False) if progress_update else "null",
                    })

                    row = result.fetchone()
                    if row:
                        t = "✓" if tutorials else "—"
                        r = "✓" if references else "—"
                        p = "✓" if progress_update else "—"
                        print(f"  ✅ [{row.id}] {row.title_fr} | tutorials:{t} references:{r} progress:{p}")
                        total_updated += 1
                    else:
                        print(f"  ⚠️  Module non trouvé en DB : '{title_fr}' (role={role_label})")
                        total_skipped += 1

                except Exception as e:
                    print(f"  ❌ Erreur sur {json_file.name} : {e}")
                    total_errors += 1

        conn.commit()

    print("\n" + "=" * 60)
    print(f"  ✅ {total_updated} modules mis à jour")
    if total_skipped:
        print(f"  ⚠️  {total_skipped} ignorés (données manquantes ou module introuvable)")
    if total_errors:
        print(f"  ❌ {total_errors} erreurs")
    print("=" * 60)


if __name__ == "__main__":
    run()
