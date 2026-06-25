"""
Script de validation des fichiers JSON Marketing Strategist (Round 3 — FINAL).

Vérifie :
1. La structure du diagnostic Marketing
2. La structure des Modules 1, 2 et 3
3. La présence des 8 ajouts v1.1 (2 sur M1 + 3 sur M2 + 3 sur M3)

Usage (depuis la racine du backend) :
    python validate_marketing_content.py

Aucune dépendance externe (uniquement la stdlib Python).
"""
from __future__ import annotations
import json
from pathlib import Path

# =============================================================================
# Configuration
# =============================================================================
CONTENT_DIR = Path("content")
DIAGNOSTIC_FILE = CONTENT_DIR / "diagnostics" / "ai_marketing_strategist.json"
ROLES_DIR = CONTENT_DIR / "roles" / "ai_marketing_strategist"

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"


def check(label: str, condition: bool, detail: str = "") -> bool:
    icon = f"{GREEN}✅{RESET}" if condition else f"{RED}❌{RESET}"
    suffix = f" — {detail}" if detail else ""
    print(f"  {icon} {label}{suffix}")
    return condition


def section(title: str):
    print(f"\n{BOLD}{BLUE}{'=' * 70}{RESET}")
    print(f"{BOLD}{BLUE}{title}{RESET}")
    print(f"{BOLD}{BLUE}{'=' * 70}{RESET}")


# =============================================================================
# Validation 1 — Diagnostic
# =============================================================================
def validate_diagnostic():
    section("📋 VALIDATION DU DIAGNOSTIC MARKETING")

    if not DIAGNOSTIC_FILE.exists():
        print(f"{RED}❌ Fichier introuvable : {DIAGNOSTIC_FILE}{RESET}")
        return False

    with DIAGNOSTIC_FILE.open(encoding="utf-8") as f:
        data = json.load(f)

    all_ok = True

    print(f"\n{BOLD}Métadonnées :{RESET}")
    all_ok &= check("role correct", data.get("role") == "AI Marketing Strategist", data.get("role"))
    all_ok &= check("career_path_id correct", data.get("career_path_id") == 80, str(data.get("career_path_id")))
    all_ok &= check("source v1.1 référencée", "v1.1" in data.get("source", ""), data.get("source", ""))

    print(f"\n{BOLD}Skills :{RESET}")
    skills = data.get("skills", [])
    all_ok &= check("3 skills présentes", len(skills) == 3, f"trouvé : {len(skills)}")

    expected_skills = [
        "AI Content Strategy & Creation",
        "AI Campaign & Growth Optimization",
        "AI Audience Intelligence",
    ]
    for i, expected in enumerate(expected_skills):
        if i < len(skills):
            actual = skills[i].get("name", "")
            all_ok &= check(f"Skill {i+1}: {expected}", actual == expected, f"trouvé : '{actual}'")

    print(f"\n{BOLD}Questions :{RESET}")
    questions = data.get("questions", [])
    all_ok &= check("9 questions présentes", len(questions) == 9, f"trouvé : {len(questions)}")

    by_skill = {}
    for q in questions:
        idx = q.get("skill_index")
        by_skill.setdefault(idx, []).append(q)

    for skill_idx in range(3):
        count = len(by_skill.get(skill_idx, []))
        all_ok &= check(f"Skill {skill_idx+1} : 3 questions", count == 3, f"trouvé : {count}")

    return all_ok


# =============================================================================
# Validation générique d'un module
# =============================================================================
def validate_module(module_num, file_name, expected_title, expected_level,
                     expected_duration, expected_skill, expected_persona):
    section(f"📚 VALIDATION DU MODULE {module_num} — {expected_title}")

    module_file = ROLES_DIR / file_name
    if not module_file.exists():
        print(f"{RED}❌ Fichier introuvable : {module_file}{RESET}")
        return False, None

    with module_file.open(encoding="utf-8") as f:
        data = json.load(f)

    all_ok = True

    all_ok &= check(f"display_order = {module_num}", data.get("display_order") == module_num, str(data.get("display_order")))
    all_ok &= check("title correct", data.get("title") == expected_title, data.get("title", ""))
    all_ok &= check(f"level = {expected_level}", data.get("level") == expected_level, data.get("level", ""))
    all_ok &= check(f"durée = {expected_duration} min", data.get("estimated_duration_min") == expected_duration, str(data.get("estimated_duration_min")))
    all_ok &= check(f"skill = {expected_skill}", data.get("skill_name") == expected_skill, data.get("skill_name", ""))

    critical_fields = [
        "description", "learning_objective", "expected_outcome",
        "role_based_example", "key_concepts", "prompt_examples",
        "practical_exercise", "comparison_tables", "section_content",
    ]
    for field in critical_fields:
        value = data.get(field)
        present = value is not None and (
            (isinstance(value, str) and len(value) > 20) or
            (isinstance(value, (list, dict)) and len(value) > 0)
        )
        all_ok &= check(f"champ '{field}' présent et non-vide", present)

    prompts = data.get("prompt_examples", [])
    all_ok &= check("3 prompts dans prompt_examples", len(prompts) == 3, f"trouvé : {len(prompts)}")

    persona_present = expected_persona in data.get("role_based_example", "")
    all_ok &= check(f"Persona '{expected_persona}' présent dans role_based_example", persona_present)

    kpi = data.get("expected_outcome", "")
    has_kpi = "%" in kpi
    all_ok &= check("expected_outcome contient des KPI chiffrés", has_kpi)

    return all_ok, data


# =============================================================================
# Validations des ajouts v1.1
# =============================================================================
def validate_v1_1_module_1(module_data):
    section("🆕 VALIDATION DES 2 AJOUTS v1.1 — Module 1")
    if module_data is None:
        return False
    all_ok = True
    sc = module_data.get("section_content", {})

    print(f"\n{BOLD}Module 1 — Ajout 1 : Engagement Optimization Playbook{RESET}")
    playbook = sc.get("engagement_optimization_playbook", {})
    all_ok &= check("engagement_optimization_playbook présent", bool(playbook))
    if playbook:
        levers = playbook.get("levers", [])
        all_ok &= check("4 leviers présents", len(levers) == 4, f"trouvé : {len(levers)}")
        for exp_id in ["lever_1_hook", "lever_2_format", "lever_3_timing", "lever_4_interaction"]:
            present = any(l.get("id") == exp_id for l in levers)
            all_ok &= check(f"levier '{exp_id}'", present)
        total_techniques = sum(len(l.get("techniques", [])) for l in levers)
        all_ok &= check(f"15+ techniques au total", total_techniques >= 15, f"trouvé : {total_techniques}")
        all_ok &= check("golden_rule présente", bool(playbook.get("golden_rule")))

    print(f"\n{BOLD}Module 1 — Ajout 2 : References & sources de veille{RESET}")
    refs = sc.get("references", {})
    all_ok &= check("references présent", bool(refs))
    if refs:
        sources = refs.get("sources", [])
        all_ok &= check("5 sources de référence", len(sources) == 5, f"trouvé : {len(sources)}")
        all_sources_text = " | ".join(s.get("name", "") for s in sources)
        for exp in ["HubSpot", "Notion AI", "LinkedIn", "Meta Business", "Buffer"]:
            all_ok &= check(f"source '{exp}'", exp in all_sources_text)

    return all_ok


def validate_v1_1_module_2(module_data):
    section("🆕 VALIDATION DES 3 AJOUTS v1.1 — Module 2")
    if module_data is None:
        return False
    all_ok = True
    sc = module_data.get("section_content", {})

    print(f"\n{BOLD}Module 2 — Ajout 1 : KPI Tracking Templates{RESET}")
    kpi_t = sc.get("kpi_tracking_templates", {})
    all_ok &= check("kpi_tracking_templates présent", bool(kpi_t))
    if kpi_t:
        templates = kpi_t.get("templates", [])
        all_ok &= check("3 templates présents", len(templates) == 3, f"trouvé : {len(templates)}")
        for exp_id in ["template_1_top_kpis", "template_2_weekly_dashboard", "template_3_ab_test_tracking"]:
            present = any(t.get("id") == exp_id for t in templates)
            all_ok &= check(f"template '{exp_id}'", present)
        t1 = next((t for t in templates if t.get("id") == "template_1_top_kpis"), None)
        if t1:
            kpis = t1.get("kpis", [])
            kpi_names = [k.get("kpi", "") for k in kpis]
            for exp_kpi in ["CTR", "CPC", "CVR", "CAC", "ROAS", "Frequency"]:
                all_ok &= check(f"KPI '{exp_kpi}' dans Template 1", exp_kpi in kpi_names)

    print(f"\n{BOLD}Module 2 — Ajout 2 : CAC Optimization Decision Tree{RESET}")
    dt = sc.get("cac_optimization_decision_tree", {})
    all_ok &= check("cac_optimization_decision_tree présent", bool(dt))
    if dt:
        branches = dt.get("diagnostic_step_1", {}).get("branches", [])
        all_ok &= check("4 branches diagnostiques", len(branches) == 4, f"trouvé : {len(branches)}")
        actions = dt.get("corrective_actions", [])
        all_ok &= check("4 actions correctives (2A/2B/2C/2D)", len(actions) == 4, f"trouvé : {len(actions)}")
        for exp_id in ["step_2A", "step_2B", "step_2C", "step_2D"]:
            present = any(a.get("id") == exp_id for a in actions)
            all_ok &= check(f"action '{exp_id}'", present)
        all_ok &= check("golden_rule présente", bool(dt.get("golden_rule")))

    print(f"\n{BOLD}Module 2 — Ajout 3 : References & sources de veille{RESET}")
    refs = sc.get("references", {})
    all_ok &= check("references présent", bool(refs))
    if refs:
        sources = refs.get("sources", [])
        all_ok &= check("5 sources de référence", len(sources) == 5, f"trouvé : {len(sources)}")
        all_sources_text = " | ".join(s.get("name", "") for s in sources)
        for exp in ["Meta Ads", "Google Ads", "AdCreative", "TikTok", "Hubspot"]:
            all_ok &= check(f"source '{exp}'", exp in all_sources_text)

    return all_ok


def validate_v1_1_module_3(module_data):
    section("🆕 VALIDATION DES 3 AJOUTS v1.1 — Module 3")
    if module_data is None:
        return False
    all_ok = True
    sc = module_data.get("section_content", {})

    print(f"\n{BOLD}Module 3 — Ajout 1 : Data-to-Insight Translation Framework{RESET}")
    framework = sc.get("data_to_insight_framework", {})
    all_ok &= check("data_to_insight_framework présent", bool(framework))
    if framework:
        steps = framework.get("steps", [])
        all_ok &= check("5 étapes présentes", len(steps) == 5, f"trouvé : {len(steps)}")
        expected_step_names = ["COLLECT", "CLEAN", "CLUSTER", "CHARACTERIZE", "CONVERT"]
        step_names = [s.get("name", "") for s in steps]
        for exp in expected_step_names:
            all_ok &= check(f"étape '{exp}'", exp in step_names)
        all_ok &= check("applied_example (Lina) présent", bool(framework.get("applied_example")))
        all_ok &= check("golden_rule présente", bool(framework.get("golden_rule")))

    print(f"\n{BOLD}Module 3 — Ajout 2 : From data → strategy Workflows{RESET}")
    workflows = sc.get("from_data_to_strategy_workflows", {})
    all_ok &= check("from_data_to_strategy_workflows présent", bool(workflows))
    if workflows:
        wfs = workflows.get("workflows", [])
        all_ok &= check("2 workflows présents", len(wfs) == 2, f"trouvé : {len(wfs)}")
        for exp_id in ["workflow_A_audit_trimestriel", "workflow_B_detection_continue"]:
            present = any(w.get("id") == exp_id for w in wfs)
            all_ok &= check(f"workflow '{exp_id}'", present)

    print(f"\n{BOLD}Module 3 — Ajout 3 : References & sources de veille{RESET}")
    refs = sc.get("references", {})
    all_ok &= check("references présent", bool(refs))
    if refs:
        sources = refs.get("sources", [])
        all_ok &= check("5 sources de référence", len(sources) == 5, f"trouvé : {len(sources)}")
        all_sources_text = " | ".join(s.get("name", "") for s in sources)
        for exp in ["Segment", "Mixpanel", "Amplitude", "Google Analytics", "Meta"]:
            all_ok &= check(f"source '{exp}'", exp in all_sources_text)

    # Vérifier l'ajout de Segment CDP dans tools
    print(f"\n{BOLD}Module 3 — Ajout bonus (§4.4.5) : Segment CDP dans Tools{RESET}")
    tools = module_data.get("comparison_tables", {}).get("tools", {})
    if tools:
        rows = tools.get("rows", [])
        segment_present = any("Segment" in str(row) for row in rows)
        all_ok &= check("Segment CDP présent dans comparison_tables.tools", segment_present)

    return all_ok


# =============================================================================
# Main
# =============================================================================
def main():
    print(f"\n{BOLD}🔍 VALIDATION DU CONTENU MARKETING v1.1 (Round 3 — FINAL){RESET}")
    print(f"{BOLD}Dossier scanné : {CONTENT_DIR.resolve()}{RESET}")
    print(f"{BOLD}Périmètre : Diagnostic + 3 Modules + 8 ajouts v1.1{RESET}")

    diag_ok = validate_diagnostic()

    mod1_ok, mod1_data = validate_module(
        module_num=1, file_name="module_1_content_strategy.json",
        expected_title="Content Strategy Optimization", expected_level="Fondation",
        expected_duration=240, expected_skill="AI Content Strategy & Creation",
        expected_persona="Sarah")

    mod2_ok, mod2_data = validate_module(
        module_num=2, file_name="module_2_campaign_performance.json",
        expected_title="Campaign Performance Optimization", expected_level="Pratique",
        expected_duration=300, expected_skill="AI Campaign & Growth Optimization",
        expected_persona="Yacine")

    mod3_ok, mod3_data = validate_module(
        module_num=3, file_name="module_3_audience_insights.json",
        expected_title="Audience Insights & Segmentation", expected_level="Expert",
        expected_duration=180, expected_skill="AI Audience Intelligence",
        expected_persona="Lina")

    v1_1_m1_ok = validate_v1_1_module_1(mod1_data)
    v1_1_m2_ok = validate_v1_1_module_2(mod2_data)
    v1_1_m3_ok = validate_v1_1_module_3(mod3_data)

    section("📊 RÉSUMÉ FINAL (Round 3 — FINAL)")
    print()
    check(f"{BOLD}Diagnostic Marketing{RESET}", diag_ok)
    check(f"{BOLD}Module 1 (Content Strategy){RESET}", mod1_ok)
    check(f"{BOLD}Module 2 (Campaign Performance){RESET}", mod2_ok)
    check(f"{BOLD}Module 3 (Audience Insights){RESET}", mod3_ok)
    check(f"{BOLD}Ajouts v1.1 Module 1 (2 nouveautés){RESET}", v1_1_m1_ok)
    check(f"{BOLD}Ajouts v1.1 Module 2 (3 nouveautés){RESET}", v1_1_m2_ok)
    check(f"{BOLD}Ajouts v1.1 Module 3 (3 nouveautés){RESET}", v1_1_m3_ok)

    if all([diag_ok, mod1_ok, mod2_ok, mod3_ok, v1_1_m1_ok, v1_1_m2_ok, v1_1_m3_ok]):
        print(f"\n{GREEN}{BOLD}🎉 TOUT EST VALIDE — Tu peux passer aux seeds Python et au wipe BDD !{RESET}\n")
        return 0
    else:
        print(f"\n{RED}{BOLD}⚠️  Des points sont à corriger avant la suite.{RESET}\n")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
