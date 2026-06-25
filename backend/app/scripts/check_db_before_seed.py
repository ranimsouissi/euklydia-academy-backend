"""
Script de vérification pré-seed.

À lancer AVANT de lancer les seeds Designer et PM pour s'assurer que :
1. Les career_paths nécessaires existent (Sales=79, Designer=81, PM=82)
2. Le schéma de la table modules contient bien toutes les colonnes
   référencées par les seeds

Usage :
    python -m scripts.check_db_before_seed
"""
from sqlalchemy import inspect, text
from app.db.session import SessionLocal  # adapter si chemin différent


# Liste des colonnes que les seeds Designer/PM essaient de remplir.
# Source : seed_ai_designer_modules.py + seed_ai_project_manager_modules.py
EXPECTED_MODULE_COLUMNS = {
    # Identité
    "title_fr", "title_en",
    "description_fr", "description_en",
    "level", "estimated_duration_min", "format",
    "role", "journey_stage", "display_order", "is_active",

    # Pédagogie textuelle
    "learning_objective_fr", "learning_objective_en",
    "expected_outcome_fr", "expected_outcome_en",
    "role_based_example_fr", "role_based_example_en",
    "takeaway_fr", "takeaway_en",
    "action_point_fr", "action_point_en",
    "practical_application_fr", "practical_application_en",
    "recommended_when_fr", "recommended_when_en",
    "why_this_module_fr", "why_this_module_en",
    "next_recommended_module_fr", "next_recommended_module_en",

    # JSON (contenu riche)
    "key_concepts_fr", "key_concepts_en",
    "comparison_tables_fr", "comparison_tables_en",
    "prompt_examples_fr", "prompt_examples_en",
    "section_content_fr", "section_content_en",
    "practical_exercise_fr", "practical_exercise_en",
}


def main():
    db = SessionLocal()
    try:
        print("=" * 60)
        print("CHECK 1 — career_paths (Sales=79, Designer=81, PM=82)")
        print("=" * 60)
        result = db.execute(text(
            "SELECT id, name FROM career_paths "
            "WHERE id IN (79, 81, 82) ORDER BY id"
        ))
        rows = result.fetchall()
        found_ids = {r[0] for r in rows}
        for row in rows:
            print(f"  ✅ id={row[0]:3d}  name={row[1]}")
        for expected_id, label in [(79, "Sales"), (81, "Designer"), (82, "PM")]:
            if expected_id not in found_ids:
                print(f"  ❌ MANQUANT : id={expected_id} ({label})")

        print()
        print("=" * 60)
        print("CHECK 2 — colonnes de la table 'modules'")
        print("=" * 60)
        inspector = inspect(db.bind)
        actual_columns = {col["name"] for col in inspector.get_columns("modules")}

        missing = EXPECTED_MODULE_COLUMNS - actual_columns
        extra_info = actual_columns - EXPECTED_MODULE_COLUMNS

        if not missing:
            print(f"  ✅ Toutes les {len(EXPECTED_MODULE_COLUMNS)} colonnes attendues sont présentes.")
        else:
            print(f"  ❌ COLONNES MANQUANTES ({len(missing)}) :")
            for col in sorted(missing):
                print(f"     • {col}")

        if extra_info:
            print(f"\n  ℹ️  Colonnes existantes mais non utilisées par le seed ({len(extra_info)}) :")
            for col in sorted(extra_info):
                print(f"     • {col}")

        print()
        print("=" * 60)
        print("CHECK 3 — types des colonnes JSON critiques")
        print("=" * 60)
        json_columns = [
            "key_concepts_fr", "comparison_tables_fr", "prompt_examples_fr",
            "section_content_fr", "practical_exercise_fr",
        ]
        cols_info = {c["name"]: c for c in inspector.get_columns("modules")}
        for col_name in json_columns:
            if col_name in cols_info:
                col_type = str(cols_info[col_name]["type"])
                if "JSON" in col_type.upper():
                    print(f"  ✅ {col_name:30s} → {col_type}")
                else:
                    print(f"  ⚠️  {col_name:30s} → {col_type} (attendu : JSON ou JSONB)")
            else:
                print(f"  ❌ {col_name:30s} → COLONNE MANQUANTE")

        print()
        print("=" * 60)
        print("CHECK 4 — autres tables critiques existent")
        print("=" * 60)
        for table in ["skills", "questions", "units", "lessons", "module_skills"]:
            if inspector.has_table(table):
                col_count = len(inspector.get_columns(table))
                print(f"  ✅ {table:20s} ({col_count} colonnes)")
            else:
                print(f"  ❌ {table:20s} TABLE MANQUANTE")

        print()
        print("=" * 60)
        print("CHECK 5 — données déjà seedées (pour anticiper l'idempotence)")
        print("=" * 60)
        for cp_id, label in [(79, "Sales"), (81, "Designer"), (82, "PM")]:
            skill_count = db.execute(text(
                "SELECT COUNT(*) FROM skills WHERE career_path_id = :id"
            ), {"id": cp_id}).scalar()
            module_count = db.execute(text(
                "SELECT COUNT(*) FROM modules WHERE role = :role"
            ), {"role": {"79": "AI Sales Specialist",
                         "81": "AI Designer",
                         "82": "AI Project Manager"}[str(cp_id)]}).scalar()
            status = "déjà seedé" if skill_count >= 3 else "à seeder"
            print(f"  • {label:10s} (cp={cp_id}) : skills={skill_count}, modules={module_count}  → {status}")

    finally:
        db.close()


if __name__ == "__main__":
    main()