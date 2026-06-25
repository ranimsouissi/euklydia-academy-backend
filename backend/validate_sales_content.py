"""
Script de validation des fichiers JSON Sales Specialist.

Vérifie :
1. La structure attendue de chaque JSON
2. La présence des champs critiques (KPI, prompts, persona Karim, ajouts v1.1)
3. Le décompte des éléments (3 skills, 9 questions, 3 modules, etc.)

Usage (depuis la racine du backend) :
    python validate_sales_content.py

Aucune dépendance externe (uniquement la stdlib Python).
"""
from __future__ import annotations
import json
from pathlib import Path

# =============================================================================
# Configuration
# =============================================================================
CONTENT_DIR = Path("content")
DIAGNOSTIC_FILE = CONTENT_DIR / "diagnostics" / "ai_sales_specialist.json"
ROLES_DIR = CONTENT_DIR / "roles" / "ai_sales_specialist"

# Codes couleur ANSI (compatibles PowerShell récent)
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"


# =============================================================================
# Utilitaires
# =============================================================================
def check(label: str, condition: bool, detail: str = "") -> bool:
    """Affiche un check coloré et retourne le booléen."""
    icon = f"{GREEN}✅{RESET}" if condition else f"{RED}❌{RESET}"
    suffix = f" — {detail}" if detail else ""
    print(f"  {icon} {label}{suffix}")
    return condition


def warn(label: str, detail: str = ""):
    """Affiche un warning."""
    suffix = f" — {detail}" if detail else ""
    print(f"  {YELLOW}⚠️  {label}{suffix}{RESET}")


def section(title: str):
    """Affiche un titre de section."""
    print(f"\n{BOLD}{BLUE}{'=' * 70}{RESET}")
    print(f"{BOLD}{BLUE}{title}{RESET}")
    print(f"{BOLD}{BLUE}{'=' * 70}{RESET}")


# =============================================================================
# Validation 1 — Diagnostic (3 skills + 9 questions)
# =============================================================================
def validate_diagnostic():
    section("📋 VALIDATION DU DIAGNOSTIC")

    if not DIAGNOSTIC_FILE.exists():
        print(f"{RED}❌ Fichier introuvable : {DIAGNOSTIC_FILE}{RESET}")
        return False

    with DIAGNOSTIC_FILE.open(encoding="utf-8") as f:
        data = json.load(f)

    all_ok = True

    # Métadonnées
    print(f"\n{BOLD}Métadonnées :{RESET}")
    all_ok &= check("role correct", data.get("role") == "AI Sales Specialist", data.get("role"))
    all_ok &= check("career_path_id correct", data.get("career_path_id") == 79, str(data.get("career_path_id")))
    all_ok &= check("source v1.1 référencée", "v1.1" in data.get("source", ""), data.get("source", ""))

    # Skills
    print(f"\n{BOLD}Skills :{RESET}")
    skills = data.get("skills", [])
    all_ok &= check(f"3 skills présentes", len(skills) == 3, f"trouvé : {len(skills)}")

    expected_skills = [
        "Qualification IA des leads",
        "Prospection hyper-personnalisée",
        "Conversations commerciales assistées par IA",
    ]
    for i, expected in enumerate(expected_skills):
        if i < len(skills):
            actual = skills[i].get("name", "")
            all_ok &= check(f"Skill {i+1}: {expected}", actual == expected, f"trouvé : '{actual}'")

    # Questions
    print(f"\n{BOLD}Questions :{RESET}")
    questions = data.get("questions", [])
    all_ok &= check(f"9 questions présentes", len(questions) == 9, f"trouvé : {len(questions)}")

    # Distribution par skill
    by_skill = {}
    for q in questions:
        idx = q.get("skill_index")
        by_skill.setdefault(idx, []).append(q)

    for skill_idx in range(3):
        count = len(by_skill.get(skill_idx, []))
        all_ok &= check(f"Skill {skill_idx+1} : 3 questions", count == 3, f"trouvé : {count}")

    # Réponses correctes (test : doit être A, B, C ou D)
    valid_answers = all(q.get("correct_answer") in ["A", "B", "C", "D"] for q in questions)
    all_ok &= check("Toutes les correct_answer sont valides (A/B/C/D)", valid_answers)

    # Présence des 4 options
    all_4_options = all(
        all(q.get(f"option_{letter}") for letter in ["a", "b", "c", "d"])
        for q in questions
    )
    all_ok &= check("Toutes les questions ont 4 options", all_4_options)

    # Présence des explications
    all_explained = all(q.get("explanation") for q in questions)
    all_ok &= check("Toutes les questions ont une explication", all_explained)

    return all_ok


# =============================================================================
# Validation 2 — Modules (3 modules complets)
# =============================================================================
def validate_modules():
    section("📚 VALIDATION DES 3 MODULES")

    if not ROLES_DIR.exists():
        print(f"{RED}❌ Dossier introuvable : {ROLES_DIR}{RESET}")
        return False

    module_files = sorted(ROLES_DIR.glob("module_*.json"))
    print(f"\n{BOLD}Fichiers trouvés : {len(module_files)}{RESET}")
    for f in module_files:
        print(f"  • {f.name}")

    all_ok = check(f"3 fichiers modules", len(module_files) == 3, f"trouvé : {len(module_files)}")
    if len(module_files) != 3:
        return False

    expected_modules = [
        ("Lead Qualification Automation", "Fondation", 240, "Qualification IA des leads"),
        ("Personalized Outreach at Scale", "Pratique", 300, "Prospection hyper-personnalisée"),
        ("Sales Call Preparation", "Expert", 180, "Conversations commerciales assistées par IA"),
    ]

    modules = []
    for f in module_files:
        with f.open(encoding="utf-8") as fp:
            modules.append(json.load(fp))
    modules.sort(key=lambda m: m.get("display_order", 0))

    for i, (m, expected) in enumerate(zip(modules, expected_modules)):
        title_expected, level_expected, duration_expected, skill_expected = expected
        print(f"\n{BOLD}═══ Module {i+1} : {title_expected} ═══{RESET}")

        all_ok &= check(f"display_order = {i+1}", m.get("display_order") == i+1, str(m.get("display_order")))
        all_ok &= check(f"title correct", m.get("title") == title_expected, m.get("title", ""))
        all_ok &= check(f"level = {level_expected}", m.get("level") == level_expected, m.get("level", ""))
        all_ok &= check(f"durée = {duration_expected} min", m.get("estimated_duration_min") == duration_expected, str(m.get("estimated_duration_min")))
        all_ok &= check(f"skill = {skill_expected}", m.get("skill_name") == skill_expected, m.get("skill_name", ""))

        # Champs critiques
        critical_fields = [
            "description", "learning_objective", "expected_outcome",
            "role_based_example", "key_concepts", "prompt_examples",
            "practical_exercise", "comparison_tables", "section_content",
        ]
        for field in critical_fields:
            value = m.get(field)
            present = value is not None and (
                (isinstance(value, str) and len(value) > 20) or
                (isinstance(value, (list, dict)) and len(value) > 0)
            )
            all_ok &= check(f"champ '{field}' présent et non-vide", present)

        # Compte des prompts (doit être 3 par module)
        prompts = m.get("prompt_examples", [])
        all_ok &= check(f"3 prompts dans prompt_examples", len(prompts) == 3, f"trouvé : {len(prompts)}")

        # Persona Karim (présent dans Maghreb)
        karim_present = "Karim" in m.get("role_based_example", "")
        all_ok &= check(f"Persona 'Karim' présent dans role_based_example", karim_present)

        # KPI before/after (doit contenir des chiffres)
        kpi = m.get("expected_outcome", "")
        has_kpi = "%" in kpi
        all_ok &= check(f"expected_outcome contient des KPI chiffrés", has_kpi)

    return all_ok, modules


# =============================================================================
# Validation 3 — Ajouts v1.1 (4 nouveautés du PDF)
# =============================================================================
def validate_v1_1_additions(modules):
    section("🆕 VALIDATION DES 4 AJOUTS v1.1 (changelog PDF page 27)")

    if len(modules) < 2:
        print(f"{RED}❌ Pas assez de modules pour valider{RESET}")
        return False

    all_ok = True
    m1 = modules[0]  # Lead Qualification
    m2 = modules[1]  # Personalized Outreach

    # ─── Module 1 — Ajout 1 : Scoring logic templates ───
    print(f"\n{BOLD}Module 1 — Ajout 1 : Scoring logic templates (B2B/SaaS/Enterprise){RESET}")
    section_1 = m1.get("section_content", {})
    sl_templates = section_1.get("scoring_logic_templates", {})
    all_ok &= check("scoring_logic_templates présent", bool(sl_templates))
    if sl_templates:
        templates = sl_templates.get("templates", [])
        all_ok &= check(f"3 templates sectoriels", len(templates) == 3, f"trouvé : {len(templates)}")
        expected_ids = ["b2b_classique", "saas", "enterprise"]
        for exp_id in expected_ids:
            present = any(t.get("id") == exp_id for t in templates)
            all_ok &= check(f"template '{exp_id}'", present)

    # ─── Module 1 — Ajout 2 : What good scoring looks like ───
    print(f"\n{BOLD}Module 1 — Ajout 2 : What good scoring looks like (exemples comparatifs){RESET}")
    calibration = section_1.get("scoring_calibration_examples", {})
    all_ok &= check("scoring_calibration_examples présent", bool(calibration))
    if calibration:
        examples = calibration.get("examples", [])
        all_ok &= check(f"2 exemples (lead chaud + tiède)", len(examples) >= 2, f"trouvé : {len(examples)}")
        # Vérifier la présence du lead chaud 85/100 et lead tiède 52/100
        scores = [e.get("total_score", "") for e in examples]
        all_ok &= check("Exemple Lead chaud 85/100", any("85" in s for s in scores))
        all_ok &= check("Exemple Lead tiède 52/100", any("52" in s for s in scores))
        # Anti-exemple
        anti = calibration.get("anti_examples")
        all_ok &= check("anti_examples présent", bool(anti))

    # ─── Module 2 — Ajout 3 : Blueprint 10 personas ───
    print(f"\n{BOLD}Module 2 — Ajout 3 : Blueprint 10 personas{RESET}")
    section_2 = m2.get("section_content", {})
    blueprint = section_2.get("persona_blueprint", {})
    all_ok &= check("persona_blueprint présent", bool(blueprint))
    if blueprint:
        personas = blueprint.get("personas", [])
        all_ok &= check(f"10 personas", len(personas) == 10, f"trouvé : {len(personas)}")
        expected_personas = ["CEO", "Directeur Commercial", "CTO", "CFO", "COO", "DRH", "Founder", "Directeur Innovation"]
        all_personas_text = " | ".join(p.get("persona", "") for p in personas)
        for exp in expected_personas:
            present = exp in all_personas_text
            all_ok &= check(f"persona '{exp}'", present)

    # ─── Module 2 — Ajout 4 : Bad vs Good outreach library ───
    print(f"\n{BOLD}Module 2 — Ajout 4 : Bad vs Good outreach library{RESET}")
    library = section_2.get("bad_vs_good_outreach_library", {})
    all_ok &= check("bad_vs_good_outreach_library présent", bool(library))
    if library:
        cases = library.get("cases", [])
        all_ok &= check(f"3 cas comparatifs", len(cases) == 3, f"trouvé : {len(cases)}")
        # Vérifier les 3 canaux
        channels = [c.get("channel", "") for c in cases]
        for exp_channel in ["Cold Email", "LinkedIn", "WhatsApp"]:
            present = exp_channel in channels
            all_ok &= check(f"canal '{exp_channel}'", present)

    return all_ok


# =============================================================================
# Main
# =============================================================================
def main():
    print(f"\n{BOLD}🔍 VALIDATION DU CONTENU SALES SPECIALIST v1.1{RESET}")
    print(f"{BOLD}Dossier scanné : {CONTENT_DIR.resolve()}{RESET}")

    diag_ok = validate_diagnostic()
    modules_result = validate_modules()

    if isinstance(modules_result, tuple):
        modules_ok, modules_data = modules_result
        v1_1_ok = validate_v1_1_additions(modules_data)
    else:
        modules_ok = modules_result
        v1_1_ok = False

    # ─── Résumé final ───
    section("📊 RÉSUMÉ FINAL")
    print()
    check(f"{BOLD}Diagnostic (3 skills + 9 questions){RESET}", diag_ok)
    check(f"{BOLD}Modules (3 modules complets){RESET}", modules_ok)
    check(f"{BOLD}Ajouts v1.1 (4 nouveautés du PDF){RESET}", v1_1_ok)

    if diag_ok and modules_ok and v1_1_ok:
        print(f"\n{GREEN}{BOLD}🎉 TOUT EST VALIDE — Tu peux passer à la suite !{RESET}\n")
        return 0
    else:
        print(f"\n{RED}{BOLD}⚠️  Des points sont à corriger avant de continuer.{RESET}\n")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
