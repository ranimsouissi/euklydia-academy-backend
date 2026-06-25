"""
Seed AI Designer — Modules pédagogiques (refactoré v1.1)

Charge le contenu depuis content/roles/ai_designer/module_*.json
(architecture Option 3 — JSON externe comme source de vérité).

Contenu pédagogique des 3 modules du parcours AI Designer :
- Module 1 : Rapid Concept Generation
- Module 2 : UX Optimization
- Module 3 : Design System Automation

Source : PDF Parcours AI Designer v1.1 — Mai 2026.

Architecture pédagogique : chaque module est structuré en 5 unités logiques
qui regroupent les 7 sections du PDF (Use Case, KPI, Skills, Execution Content,
Execution Task, KPI Measurement, Progress Update).

Refactor : le contenu pédagogique (MODULE_1/2/3) est externalisé dans des
fichiers JSON content/roles/ai_designer/module_*.json. Ce script
ne contient plus que la structure pédagogique (UNITS_TEMPLATE, LESSONS_BY_MODULE)
et la logique d'insertion BDD.

Idempotent : skip si déjà seedé.
"""
from __future__ import annotations

from app.models.module import Module
from app.models.unit import Unit
from app.models.lesson import Lesson
from app.models.module_skill import ModuleSkill
from app.models.skill import Skill
from app.scripts.content_loader import load_role_modules


# =============================================================================
# Constantes
# =============================================================================
ROLE = "AI Designer"
CAREER_PATH_ID = 81
ROLE_SLUG = "ai_designer"


# =============================================================================
# UNITS — 5 unités par module (total : 15)
# =============================================================================
UNITS_TEMPLATE = [
    {
        "order": 1,
        "title_fr": "Comprendre le problème business",
        "description_fr": (
            "Le contexte design spécifique en Afrique du Nord, les pain points "
            "typiques que tu rencontres dans ton quotidien, et les KPIs que tu "
            "vas mesurer avant/après pour valider ton progrès."
        ),
        "estimated_duration_min": 30,
    },
    {
        "order": 2,
        "title_fr": "Compétences activées",
        "description_fr": (
            "Les 7 compétences précises que ce module développe, du niveau "
            "Connaissance au niveau Maîtrise. Auto-évaluation initiale et "
            "alignement avec ton score diagnostic."
        ),
        "estimated_duration_min": 20,
    },
    {
        "order": 3,
        "title_fr": "Execution Content",
        "description_fr": (
            "Le cœur opérationnel du module : 3 prompts validés, 2 workflows "
            "(no-code + low-code), comparatif d'outils avec alternatives "
            "Maghreb, et tutoriels vidéo."
        ),
        "estimated_duration_min": 90,
    },
    {
        "order": 4,
        "title_fr": "Mission terrain",
        "description_fr": (
            "L'Execution Task chronométrée : tu appliques les prompts sur tes "
            "vrais projets, tu mesures le temps gagné, et tu valides 3 "
            "critères de réussite chiffrés."
        ),
        "estimated_duration_min": 60,
    },
    {
        "order": 5,
        "title_fr": "Mesure d'impact & Progression",
        "description_fr": (
            "Comment collecter ta baseline à J0, mesurer l'impact à J+14, et "
            "lire les KPIs moyen terme à J+30. Mise à jour de ton score skill "
            "et recommandation du module suivant."
        ),
        "estimated_duration_min": 30,
    },
]


# =============================================================================
# LESSONS — Préservé tel quel depuis le seed original AI Designer v1.0
# Structure : LESSONS_BY_MODULE[module_display_order][unit_order] = [list of lessons]
# Format des leçons : video, exercise, tutorial, case_study, quiz
# Difficulty 1-5 : 1=très facile (intro) → 5=très difficile (maîtrise)
# =============================================================================
LESSONS_BY_MODULE = {
    # =========================================================================
    # MODULE 1 — Rapid Concept Generation
    # =========================================================================
    1: {
        # Unit 1 — Comprendre le problème business
        1: [
            {
                "title_fr": "Le quotidien de Yasmine : 5 demandes urgentes le lundi matin",
                "description_fr": (
                    "Étude de cas concrète : Yasmine, designer e-commerce à "
                    "Casablanca, et son problème de production visuelle "
                    "chronophage face à un volume de demandes élevé."
                ),
                "format": "case_study",
                "difficulty_level": 1,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Pain points des designers in-house en Afrique du Nord",
                "description_fr": (
                    "Les 6 pain points typiques : idéation lente, piste unique, "
                    "aller-retours infinis, burn-out créatif, retard pipeline, "
                    "sentiment de production."
                ),
                "format": "video",
                "difficulty_level": 1,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Pattern temporel des KPIs : court / moyen / long terme",
                "description_fr": (
                    "Comprendre pourquoi on distingue KPIs de productivité (J+14), "
                    "qualité (J+30), et impact business (volumes mensuels)."
                ),
                "format": "video",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
        ],
        # Unit 2 — Compétences activées
        2: [
            {
                "title_fr": "Les 7 compétences de l'idéation visuelle IA",
                "description_fr": (
                    "Tour d'horizon des 7 compétences : anatomie d'un prompt, "
                    "paramètres avancés Midjourney, bibliothèque de prompts, "
                    "workflow d'itération, critères d'évaluation, présentation, "
                    "adaptation Maghreb."
                ),
                "format": "video",
                "difficulty_level": 2,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Auto-évaluation initiale",
                "description_fr": (
                    "Compare ton score diagnostic au niveau attendu et identifie "
                    "tes compétences faibles à prioriser dans ce module."
                ),
                "format": "quiz",
                "difficulty_level": 2,
                "estimated_duration_min": 5,
            },
        ],
        # Unit 3 — Execution Content
        3: [
            {
                "title_fr": "Prompt 1 — Brief créatif structuré (anatomie)",
                "description_fr": (
                    "Décortique le Prompt 1 : transformation d'un brief vague en "
                    "7 sections exploitables avec 3 directions distinctes. Pourquoi "
                    "chaque section compte."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Prompt 2 — Bibliothèque de prompts Midjourney par style",
                "description_fr": (
                    "Les 5 styles visuels de référence (minimaliste éditorial, "
                    "lifestyle authentique, product hero premium, illustration "
                    "éditoriale, UGC) avec paramètres avancés (--ar, --style, --chaos)."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Prompt 3 — Workflow d'itération v1 → v10",
                "description_fr": (
                    "Workflow chronométré 30 min en 4 phases : diverger (5 min) → "
                    "sélectionner (3 min) → raffiner (15 min) → finaliser (5 min)."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Workflow 1 — Sprint d'idéation 30 minutes (no-code)",
                "description_fr": (
                    "Pipeline complet : ChatGPT (brief) → Midjourney (génération 3 "
                    "directions × 4 variations) → sélection critères → raffinement → "
                    "planche Figma. Setup 30 min."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 20,
            },
            {
                "title_fr": "Workflow 2 — Pipeline d'idéation industriel (low-code)",
                "description_fr": (
                    "Pipeline industriel : Notion/Airtable trigger → ChatGPT API "
                    "(brief auto) → Midjourney API → Drive sauvegarde → Slack "
                    "validation humaine. Pour studios et agences."
                ),
                "format": "tutorial",
                "difficulty_level": 4,
                "estimated_duration_min": 25,
            },
        ],
        # Unit 4 — Mission terrain
        4: [
            {
                "title_fr": "Mission : Génère 10 concepts visuels en 30 minutes",
                "description_fr": (
                    "60 minutes chronométrées sur un brief réel. Critères de "
                    "réussite : 10 concepts variés en 30 min, 2+ « surprise "
                    "positive » par le client, bibliothèque enrichie de 3+ "
                    "prompts gagnants."
                ),
                "format": "exercise",
                "difficulty_level": 4,
                "estimated_duration_min": 60,
            },
        ],
        # Unit 5 — Mesure d'impact & Progression
        5: [
            {
                "title_fr": "Collecte de la baseline à J0",
                "description_fr": (
                    "Comment mesurer honnêtement ton temps actuel d'idéation et "
                    "ta diversité créative avant tout changement. Formulaire intégré."
                ),
                "format": "exercise",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Mécanisme de relance J+7 / J+14 / J+30",
                "description_fr": (
                    "Comprendre pourquoi on mesure plusieurs fois : isoler l'effet "
                    "du module, distinguer effet ponctuel vs durable, observer le "
                    "moyen terme sur le temps jusqu'au final validé."
                ),
                "format": "video",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Lecture du dashboard et recommandation suivante",
                "description_fr": (
                    "Lire ton comparatif baseline vs J+14, mettre à jour ton score "
                    "skill « AI Visual Ideation & Concept », et choisir ton "
                    "prochain module."
                ),
                "format": "tutorial",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
        ],
    },

    # =========================================================================
    # MODULE 2 — UX Optimization
    # =========================================================================
    2: {
        1: [
            {
                "title_fr": "Le quotidien de Yasmine : taux de conversion stagnant",
                "description_fr": (
                    "Étude de cas : Yasmine fait des changements UX au pifomètre "
                    "sur le site e-commerce, sans budget pour des tests labo, "
                    "sans diagnostic data-driven."
                ),
                "format": "case_study",
                "difficulty_level": 1,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Pain points UX en Afrique du Nord",
                "description_fr": (
                    "Les 6 pain points : engagement faible, audit subjectif, pas "
                    "d'analyse data-driven, recommandations non priorisées, "
                    "impact business non démontré, dev qui priorise les features."
                ),
                "format": "video",
                "difficulty_level": 1,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Pourquoi tester sur les appareils Maghreb dominants",
                "description_fr": (
                    "Frictions liées au tactile imprécis sur Android entry-level, "
                    "temps de chargement sur 3G/4G fluctuantes, accessibilité "
                    "souvent oubliée."
                ),
                "format": "video",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
        ],
        2: [
            {
                "title_fr": "Les 7 compétences de l'UX Intelligence",
                "description_fr": (
                    "Heuristiques de Nielsen, Hotjar/Clarity, analyse verbatims, "
                    "audit IA, priorisation par ROI, playbooks réutilisables, "
                    "mesure de l'engagement."
                ),
                "format": "video",
                "difficulty_level": 2,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Triangulation : heatmaps + heuristiques + verbatims",
                "description_fr": (
                    "Pourquoi croiser 3 sources de données (comportementale, "
                    "expert, qualitative) révèle les vraies frictions vs ressenti "
                    "subjectif."
                ),
                "format": "video",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
        ],
        3: [
            {
                "title_fr": "Prompt 1 — Audit heuristique automatisé Nielsen",
                "description_fr": (
                    "Évaluer un écran sur les 10 heuristiques de Nielsen : "
                    "score, constat, friction, recommandation, effort, impact "
                    "business par heuristique."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Prompt 2 — Analyse de 50-200 verbatims utilisateurs",
                "description_fr": (
                    "Classification, pain points avec citations, jobs-to-be-done, "
                    "recommandations priorisées (quick wins / mid-term / strategic), "
                    "citations représentatives."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Prompt 3 — UX improvement playbook par friction",
                "description_fr": (
                    "Bibliothèque de réponses standard : anatomie de la friction, "
                    "3 patterns de résolution, recommandation, specs design, "
                    "checklist mise en prod, KPIs, benchmark."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Workflow 1 — Audit UX express d'une page critique (no-code, 2h)",
                "description_fr": (
                    "Pipeline 2h : Hotjar (7 jours) → Prompt 1 (audit heuristique) → "
                    "triangulation Hotjar+IA → Prompt 3 (playbooks Top 3) → "
                    "mockups Figma."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 20,
            },
            {
                "title_fr": "Workflow 2 — UX intelligence en continu (low-code)",
                "description_fr": (
                    "Pipeline continu : Hotjar API + GA4 + Avis Google + Support → "
                    "détection anomalies → rapport UX hebdo IA → tickets Jira auto → "
                    "mockups Figma AI."
                ),
                "format": "tutorial",
                "difficulty_level": 4,
                "estimated_duration_min": 25,
            },
        ],
        4: [
            {
                "title_fr": "Mission : Audit UX d'une page critique + 3 corrections mockupées",
                "description_fr": (
                    "120 minutes étalées sur la semaine. Critères : 3 corrections "
                    "validées par l'équipe, mise en prod planifiée dans 2 semaines, "
                    "audit complet en moins de 2 jours."
                ),
                "format": "exercise",
                "difficulty_level": 4,
                "estimated_duration_min": 120,
            },
        ],
        5: [
            {
                "title_fr": "Collecte baseline taux d'engagement et durée d'audit",
                "description_fr": (
                    "Mesurer honnêtement ton taux d'engagement actuel et le temps "
                    "passé sur tes audits UX avant le module."
                ),
                "format": "exercise",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Bibliothèque personnelle de playbooks UX",
                "description_fr": (
                    "Conservation et amélioration continue de ta bibliothèque de "
                    "playbooks par type de friction (checkout, navigation, formulaires, "
                    "errors, search)."
                ),
                "format": "tutorial",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Mise à jour du score skill et recommandation suivante",
                "description_fr": (
                    "Si skill 3 < 67/100, recommandation Module 3 (Design System "
                    "Automation). Sinon : certificat AI Designer."
                ),
                "format": "tutorial",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
        ],
    },

    # =========================================================================
    # MODULE 3 — Design System Automation
    # =========================================================================
    3: {
        1: [
            {
                "title_fr": "Le quotidien de Yasmine : 3 produits, 3 chartes différentes",
                "description_fr": (
                    "Étude de cas : Yasmine recrée un bouton « Acheter » à chaque "
                    "produit, et les développeurs ont leurs propres versions des "
                    "composants en code."
                ),
                "format": "case_study",
                "difficulty_level": 1,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Pain points du design ops en Afrique du Nord",
                "description_fr": (
                    "Les 6 pain points : incohérence visuelle, perte de temps, "
                    "pas de fichier source unique, désynchronisation Figma↔code, "
                    "non-scalabilité, marque non reconnaissable."
                ),
                "format": "video",
                "difficulty_level": 1,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Spécificités Maghreb : équipes hybrides et RTL",
                "description_fr": (
                    "Pourquoi un design system devient stratégique pour les équipes "
                    "Tunis-Casablanca-Alger ou avec freelances distribués, et "
                    "comment intégrer le RTL (right-to-left) dès la conception."
                ),
                "format": "video",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
        ],
        2: [
            {
                "title_fr": "Les 7 compétences du Design System & Ops",
                "description_fr": (
                    "Architecture (foundations/components/patterns), design tokens, "
                    "audit cohérence, Figma AI, Tokens Studio, sync Figma↔code, "
                    "gouvernance."
                ),
                "format": "video",
                "difficulty_level": 2,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Du fichier Figma figé à la plateforme vivante",
                "description_fr": (
                    "Pourquoi un design system industrialisé (tokens centralisés + "
                    "composants générés + validation IA + sync code) surpasse les "
                    "approches statiques (PDF charte, fichier Figma partagé)."
                ),
                "format": "video",
                "difficulty_level": 3,
                "estimated_duration_min": 10,
            },
        ],
        3: [
            {
                "title_fr": "Prompt 1 — Audit de cohérence visuelle multi-produits",
                "description_fr": (
                    "Audit en 6 sections : inventaire foundations, écarts de "
                    "cohérence (tableau comparatif), design tokens recommandés, "
                    "composants prioritaires, roadmap migration, risques + quick wins."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Prompt 2 — Génération de composants Figma (spec)",
                "description_fr": (
                    "Spec complète d'un composant en 7 sections : anatomie, props, "
                    "variants, spécifications visuelles, accessibilité (WCAG 2.1 AA), "
                    "do/don't, spec dev (CSS/Tailwind/React)."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Prompt 3 — Documentation auto en Markdown",
                "description_fr": (
                    "Génération d'une documentation Markdown complète : description, "
                    "use cases, anti-patterns, props, variants, accessibilité, "
                    "exemples, code React+Tailwind, changelog."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Workflow 1 — Bootstrap d'un design system en 1 semaine",
                "description_fr": (
                    "Pipeline 7 jours : J1 audit cohérence → J2 design tokens → "
                    "J3 variables Figma → J4-J5 composants atomiques + variants → "
                    "J6 documentation auto → J7 training équipe."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 20,
            },
            {
                "title_fr": "Workflow 2 — Sync Figma ↔ Code (low-code)",
                "description_fr": (
                    "Pipeline industriel : Tokens Studio → GitHub Actions → "
                    "Style Dictionary (build CSS/Tailwind/iOS/Android) → PR auto vers "
                    "repos produit → validation IA + notification Slack."
                ),
                "format": "tutorial",
                "difficulty_level": 4,
                "estimated_duration_min": 25,
            },
        ],
        4: [
            {
                "title_fr": "Mission : Bootstrap un mini design system sur tes produits réels",
                "description_fr": (
                    "180 minutes étalées sur la semaine. Critères : 1+ produit "
                    "utilise les nouveaux composants dans 2 semaines, 15+ tokens "
                    "centralisés, 5 composants atomiques documentés et publiés."
                ),
                "format": "exercise",
                "difficulty_level": 4,
                "estimated_duration_min": 180,
            },
        ],
        5: [
            {
                "title_fr": "Collecte baseline cohérence et temps de création composant",
                "description_fr": (
                    "Mesurer honnêtement ton temps de création d'un nouveau composant "
                    "et la cohérence visuelle inter-produits avant le module."
                ),
                "format": "exercise",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Bibliothèque personnelle de composants Figma versionnée",
                "description_fr": (
                    "Conservation, versioning et amélioration continue de ta "
                    "bibliothèque de composants par type (atomiques, composites, "
                    "patterns)."
                ),
                "format": "tutorial",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Vue consolidée des 3 modules : parcours complet AI Designer",
                "description_fr": (
                    "Synthèse de ton parcours AI Designer : scores des 3 skills, "
                    "KPIs avant/après, certificat, et bridge commercial BrandStudio "
                    "(AI Design Ideation + AI UX Intelligence + AI Design System "
                    "Builder)."
                ),
                "format": "tutorial",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
        ],
    },
}


# =============================================================================
# Fonction de seed principale (idempotente)
# =============================================================================
def seed_ai_designer_modules(db):
    """
    Seed les 3 modules + 15 units + lessons + jointures module_skills
    pour le rôle AI Designer.

    Charge le contenu des modules depuis
    content/roles/ai_designer/ (architecture Option 3).

    Source de vérité : PDF v1.1 — Mai 2026.
    """
    # =========================================================================
    # 0. Chargement des modules depuis les JSON
    # =========================================================================
    modules_data = load_role_modules(ROLE_SLUG)

    # =========================================================================
    # 1. Anti-doublon — skip si déjà seedé
    # =========================================================================
    existing_modules = (
        db.query(Module)
        .filter(Module.role == ROLE)
        .count()
    )
    if existing_modules >= len(modules_data):
        print(
            f"⚠️  AI Designer modules déjà seedés "
            f"({existing_modules} modules pour role='{ROLE}'), skip."
        )
        return

    # =========================================================================
    # 2. Récupérer les skills
    # =========================================================================
    skills_by_name = {}
    for module_data in modules_data:
        skill_name = module_data["skill_name"]
        if skill_name in skills_by_name:
            continue
        skill = (
            db.query(Skill)
            .filter(
                Skill.name == skill_name,
                Skill.career_path_id == CAREER_PATH_ID,
            )
            .first()
        )
        if skill is None:
            raise RuntimeError(
                f"Skill '{skill_name}' introuvable pour career_path_id={CAREER_PATH_ID}. "
                f"Lance d'abord seed_ai_designer_diagnostic.py."
            )
        skills_by_name[skill_name] = skill

    # =========================================================================
    # 3. Insérer les 3 modules + units + lessons + jointures module_skills
    # =========================================================================
    total_units_created = 0
    total_lessons_created = 0
    total_module_skill_links = 0

    for module_data in modules_data:
        # Skip individuel
        existing_module = (
            db.query(Module)
            .filter(
                Module.title_fr == module_data["title"],
                Module.role == ROLE,
            )
            .first()
        )
        if existing_module:
            continue

        # ─── 3.1 Créer le module ──────────────────────────────────────────
        module = Module(
            title_fr=module_data["title"],
            title_en=module_data["title"],
            description_fr=module_data["description"],
            description_en=module_data["description"],
            learning_objective_fr=module_data["learning_objective"],
            learning_objective_en=module_data["learning_objective"],
            level=module_data["level"],
            estimated_duration_min=module_data["estimated_duration_min"],
            format=module_data["format"],
            role=ROLE,
            journey_stage=module_data["journey_stage"],
            display_order=module_data["display_order"],
            expected_outcome_fr=module_data["expected_outcome"],
            expected_outcome_en=module_data["expected_outcome"],
            key_concepts_fr=module_data["key_concepts"],
            key_concepts_en=module_data["key_concepts"],
            role_based_example_fr=module_data["role_based_example"],
            role_based_example_en=module_data["role_based_example"],
            takeaway_fr=module_data["takeaway"],
            takeaway_en=module_data["takeaway"],
            action_point_fr=module_data["action_point"],
            action_point_en=module_data["action_point"],
            practical_application_fr=module_data["practical_application"],
            practical_application_en=module_data["practical_application"],
            recommended_when_fr=module_data["recommended_when"],
            recommended_when_en=module_data["recommended_when"],
            why_this_module_fr=module_data["why_this_module"],
            why_this_module_en=module_data["why_this_module"],
            next_recommended_module_fr=module_data["next_recommended_module"],
            next_recommended_module_en=module_data["next_recommended_module"],
            comparison_tables_fr=module_data["comparison_tables"],
            comparison_tables_en=module_data["comparison_tables"],
            prompt_examples_fr=module_data["prompt_examples"],
            prompt_examples_en=module_data["prompt_examples"],
            section_content_fr=module_data["section_content"],
            section_content_en=module_data["section_content"],
            practical_exercise_fr=module_data["practical_exercise"],
            practical_exercise_en=module_data["practical_exercise"],
            is_active=module_data["is_active"],
        )
        db.add(module)
        db.flush()

        # ─── 3.2 Jointure module_skills ──────────────────────────────────
        skill = skills_by_name[module_data["skill_name"]]
        link = ModuleSkill(module_id=module.id, skill_id=skill.id)
        db.add(link)
        total_module_skill_links += 1

        # ─── 3.3 Créer les 5 units ───────────────────────────────────────
        units_created = {}
        for unit_template in UNITS_TEMPLATE:
            unit = Unit(
                module_id=module.id,
                title_fr=unit_template["title_fr"],
                title_en=unit_template["title_fr"],
                description_fr=unit_template["description_fr"],
                description_en=unit_template["description_fr"],
                order=unit_template["order"],
                estimated_duration_min=unit_template["estimated_duration_min"],
                is_active=True,
            )
            db.add(unit)
            db.flush()
            units_created[unit_template["order"]] = unit
            total_units_created += 1

        # ─── 3.4 Créer les lessons ───────────────────────────────────────
        module_order = module_data["display_order"]
        lessons_for_module = LESSONS_BY_MODULE.get(module_order, {})

        for unit_order, lessons_list in lessons_for_module.items():
            unit = units_created[unit_order]
            for idx, lesson_data in enumerate(lessons_list, start=1):
                lesson = Lesson(
                    unit_id=unit.id,
                    title_fr=lesson_data["title_fr"],
                    title_en=lesson_data["title_fr"],
                    description_fr=lesson_data["description_fr"],
                    description_en=lesson_data["description_fr"],
                    format=lesson_data["format"],
                    difficulty_level=lesson_data["difficulty_level"],
                    order=idx,
                    estimated_duration_min=lesson_data["estimated_duration_min"],
                    is_active=True,
                )
                db.add(lesson)
                total_lessons_created += 1

    db.flush()

    print(
        f"✅ AI Designer modules seedés (depuis JSON) :\n"
        f"   • {len(modules_data)} modules (role='{ROLE}')\n"
        f"   • {total_units_created} units (5 par module)\n"
        f"   • {total_lessons_created} lessons\n"
        f"   • {total_module_skill_links} jointures module_skills"
    )
