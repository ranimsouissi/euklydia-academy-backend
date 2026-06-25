"""
Seed AI Sales Specialist — Modules pédagogiques (refactoré v1.1)

Charge le contenu depuis content/roles/ai_sales_specialist/module_*.json
(architecture Option 3 — JSON externe comme source de vérité).

Contenu pédagogique des 3 modules du parcours AI Sales Specialist :
- Module 1 : Lead Qualification Automation
- Module 2 : Personalized Outreach at Scale
- Module 3 : Sales Call Preparation

Source : PDF Parcours AI Sales Specialist v1.1 — Mai 2026.

Architecture pédagogique : chaque module est structuré en 5 unités logiques
qui regroupent les 7 sections du PDF (Use Case, KPI, Skills, Execution Content,
Execution Task, KPI Measurement, Progress Update) :

    Module
      ├── Unit 1 : Comprendre le problème business (Use Case + KPI Before/After)
      ├── Unit 2 : Compétences activées (Skills mapped)
      ├── Unit 3 : Execution Content (Templates + Workflows + Tools + Tutorials)
      ├── Unit 4 : Mission terrain (Execution Task)
      └── Unit 5 : Mesure d'impact & Progression (KPI Measurement + Progress)

Le contenu détaillé (prompts, workflows, exercices, tableaux comparatifs)
est stocké dans les colonnes JSON de la table modules :
- prompt_examples_fr    → les 3 prompts ChatGPT par module
- practical_exercise_fr → l'Execution Task chronométrée
- comparison_tables_fr  → les tableaux de tools, KPIs, workflows
- section_content_fr    → le Use Case détaillé + sections complémentaires
                          + ajouts v1.1 (scoring templates, persona blueprint,
                            bad vs good library, etc.)

Bilingue : V1 = FR uniquement. EN dupliqué de FR temporairement pour respecter
les contraintes NOT NULL (title_en, etc.) — sera retraduit en V2.

Refactor : le contenu pédagogique (MODULE_1/2/3) est externalisé dans des
fichiers JSON content/roles/ai_sales_specialist/module_*.json. Ce script ne
contient plus que la structure pédagogique (UNITS_TEMPLATE, LESSONS_BY_MODULE)
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
ROLE = "AI Sales Specialist"
CAREER_PATH_ID = 79  # cohérent avec seed_ai_sales_specialist_diagnostic.py
ROLE_SLUG = "ai_sales_specialist"  # nom du dossier dans content/roles/


# =============================================================================
# UNITS — 5 unités par module (total : 15)
# Structure pédagogique fixe — identique pour les 3 modules (réplicabilité).
# Reste dans le code Python car c'est un pattern technique, pas du contenu
# éditorial (la structure des Units ne change pas entre versions du PDF).
# =============================================================================
UNITS_TEMPLATE = [
    {
        "order": 1,
        "title_fr": "Comprendre le problème business",
        "description_fr": (
            "Le contexte commercial spécifique en Afrique du Nord, les pain "
            "points typiques que tu rencontres dans ton quotidien, et les "
            "KPIs que tu vas mesurer avant/après pour valider ton progrès."
        ),
        "estimated_duration_min": 30,
    },
    {
        "order": 2,
        "title_fr": "Compétences activées",
        "description_fr": (
            "Les 8 compétences précises que ce module développe, du niveau "
            "Connaissance au niveau Maîtrise. Auto-évaluation initiale et "
            "alignement avec ton score diagnostic."
        ),
        "estimated_duration_min": 20,
    },
    {
        "order": 3,
        "title_fr": "Execution Content",
        "description_fr": (
            "Le cœur opérationnel du module : 3 prompts ChatGPT validés, "
            "2 workflows (no-code + low-code), comparatif d'outils avec "
            "alternatives Afrique du Nord, et tutoriels vidéo."
        ),
        "estimated_duration_min": 90,
    },
    {
        "order": 4,
        "title_fr": "Mission terrain",
        "description_fr": (
            "L'Execution Task chronométrée : tu appliques les prompts sur "
            "tes vraies données, tu mesures le temps gagné, et tu valides "
            "3 critères de réussite chiffrés."
        ),
        "estimated_duration_min": 60,
    },
    {
        "order": 5,
        "title_fr": "Mesure d'impact & Progression",
        "description_fr": (
            "Comment collecter ta baseline à J0, mesurer l'impact à J+14, "
            "et lire les KPIs observatoires à J+30/J+60. Mise à jour de ton "
            "score skill et recommandation du module suivant."
        ),
        "estimated_duration_min": 30,
    },
]


# =============================================================================
# LESSONS — Détail des leçons par module et unité
# Structure : LESSONS_BY_MODULE[module_display_order][unit_order] = [list of lessons]
# Format des leçons : video, exercise, tutorial, case_study, quiz
# Difficulty 1-5 : 1=très facile (intro) → 5=très difficile (maîtrise)
#
# Reste dans le code Python car c'est une structure technique liée à l'UI
# (formats vidéo/exercice/etc.), pas du contenu pédagogique éditorial.
# =============================================================================
LESSONS_BY_MODULE = {
    # =========================================================================
    # MODULE 1 — Lead Qualification Automation
    # =========================================================================
    1: {
        # Unit 1 — Comprendre le problème business
        1: [
            {
                "title_fr": "Le quotidien de Karim : 5h/semaine perdues en qualification",
                "description_fr": (
                    "Étude de cas concrète : Karim, responsable commercial à Tunis, "
                    "et son problème de qualification manuelle de 30-50 leads/semaine."
                ),
                "format": "case_study",
                "difficulty_level": 1,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Pain points des équipes sales B2B en Afrique du Nord",
                "description_fr": (
                    "Les 5 pain points typiques : conversion faible, méthode non "
                    "formalisée, fiches incomplètes, désalignement Sales/Marketing, "
                    "forecasting imprévisible."
                ),
                "format": "video",
                "difficulty_level": 1,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Pattern temporel des KPIs : court / moyen / long terme",
                "description_fr": (
                    "Comprendre pourquoi on distingue KPIs de productivité (J+14), "
                    "qualité (J+14), et impact business (J+30/J+60 observatoire)."
                ),
                "format": "video",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
        ],
        # Unit 2 — Compétences activées
        2: [
            {
                "title_fr": "Les 8 compétences de la qualification IA",
                "description_fr": (
                    "Tour d'horizon des 8 compétences : frameworks, prompts, signaux "
                    "LinkedIn, classification A/B/C/D, scoring CRM, workflows, mesure, "
                    "adaptation Maghreb."
                ),
                "format": "video",
                "difficulty_level": 2,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Auto-évaluation initiale",
                "description_fr": (
                    "Compare ton score diagnostic au niveau attendu et identifie tes "
                    "compétences faibles à prioriser dans ce module."
                ),
                "format": "quiz",
                "difficulty_level": 2,
                "estimated_duration_min": 5,
            },
        ],
        # Unit 3 — Execution Content
        3: [
            {
                "title_fr": "Prompt 1 — BANT Scoring (anatomie d'un bon prompt)",
                "description_fr": (
                    "Décortique le Prompt 1 : variables BUDGET, ROLE_DECISION, devise "
                    "cadrée, grille de seuils. Pourquoi chaque ligne compte."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Prompt 2 — Buying Signals Detection",
                "description_fr": (
                    "Détecter les 3-5 signaux d'achat à partir d'infos LinkedIn. "
                    "Cadrage de la variable INFOS_LINKEDIN_COPIEES (pourquoi ChatGPT "
                    "ne navigue pas LinkedIn) et choix du canal."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Prompt 3 — Classification A/B/C/D batch",
                "description_fr": (
                    "Trier 10-20 leads en 4 catégories alignées sur la grille BANT. "
                    "Format de sortie tableau + synthèse."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Workflow 1 — HubSpot AI Lead Scoring (no-code)",
                "description_fr": (
                    "Activer le scoring prédictif HubSpot, paramétrer un score manuel "
                    "complémentaire, et utiliser le Prompt 1 BANT pour les cas ambigus. "
                    "Setup 15-20 min."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 20,
            },
            {
                "title_fr": "Workflow 2 — Scoring auto via Zapier (low-code)",
                "description_fr": (
                    "Pipeline complet : HubSpot trigger → Apollo enrichissement → "
                    "OpenAI scoring BANT → mise à jour HubSpot → notification Slack. "
                    "Version low-cost Maghreb avec n8n."
                ),
                "format": "tutorial",
                "difficulty_level": 4,
                "estimated_duration_min": 25,
            },
        ],
        # Unit 4 — Mission terrain
        4: [
            {
                "title_fr": "Mission : Score tes 10 derniers leads avec BANT",
                "description_fr": (
                    "60 minutes chronométrées sur tes vraies données. Critères de "
                    "réussite : 10 leads en < 30 min, 3+ écarts intuition vs IA ≥ 25 "
                    "points, plan d'action concret."
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
                    "Comment mesurer honnêtement ton temps de qualification actuel et "
                    "ton taux d'enrichissement avant tout changement. Formulaire intégré."
                ),
                "format": "exercise",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Mécanisme de relance J+7 / J+14 / J+30",
                "description_fr": (
                    "Comprendre pourquoi on mesure plusieurs fois : isoler l'effet du "
                    "module, distinguer effet ponctuel vs durable, attendre l'observatoire "
                    "pour le close rate."
                ),
                "format": "video",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Lecture du dashboard et recommandation suivante",
                "description_fr": (
                    "Lire ton comparatif baseline vs J+14, mettre à jour ton score "
                    "skill 'Qualification IA des leads', et choisir ton prochain module."
                ),
                "format": "tutorial",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
        ],
    },

    # =========================================================================
    # MODULE 2 — Personalized Outreach at Scale
    # =========================================================================
    2: {
        1: [
            {
                "title_fr": "Le quotidien de Karim : reply rate 3% sur 200 prospects",
                "description_fr": (
                    "Étude de cas : Karim contacte 50 prospects/semaine en email "
                    "générique, obtient 1-2 RDV, et n'utilise pas WhatsApp."
                ),
                "format": "case_study",
                "difficulty_level": 1,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Pain points de l'outreach B2B en Afrique du Nord",
                "description_fr": (
                    "Les 6 pain points : reply rate bas, personnalisation prénom-only, "
                    "pas de segmentation, mono-canal, peu de RDV, WhatsApp ignoré."
                ),
                "format": "video",
                "difficulty_level": 1,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Pourquoi WhatsApp est l'avantage régional clé",
                "description_fr": (
                    "Données et patterns culturels qui font de WhatsApp Business un "
                    "canal sous-exploité en Afrique du Nord. Pourquoi 80 % des "
                    "concurrents l'ignorent encore."
                ),
                "format": "video",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
        ],
        2: [
            {
                "title_fr": "Les 8 compétences de la prospection hyper-personnalisée",
                "description_fr": (
                    "Personnalisation à l'échelle, génération d'emails, séquences "
                    "multi-touch, segmentation, A/B test, contextualisation, mesure, "
                    "multi-langue."
                ),
                "format": "video",
                "difficulty_level": 2,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Personnalisation à l'échelle : nuance importante",
                "description_fr": (
                    "Différence entre segmentation manuelle (3-4 templates), "
                    "personnalisation prénom-only, et vraie personnalisation à "
                    "l'échelle pilotée par l'IA."
                ),
                "format": "video",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
        ],
        3: [
            {
                "title_fr": "Prompt 1 — Cold email personnalisé (variable Langue)",
                "description_fr": (
                    "Décortique le Prompt 1 : intégration de la variable Langue "
                    "[FR/AR/EN/mix], signature cadrée, génération objet + variante A/B."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Prompt 2 — Séquence multi-touch 4 messages",
                "description_fr": (
                    "Construire une séquence J1 (email) → J4 (LinkedIn) → J8 (email) "
                    "→ J12 (WhatsApp). Cadence flexible STANDARD/SERREE/ESPACEE."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Prompt 3 — Adaptation WhatsApp Maghreb",
                "description_fr": (
                    "Adapter un cold email pour WhatsApp : ton chaleureux, salutation "
                    "régionale (Tunisie/Algérie/Maroc/Égypte/Libye), longueur 3-4 lignes."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Workflow 1 — Cold email manuel assisté ChatGPT",
                "description_fr": (
                    "Pipeline no-code : Apollo identification → ChatGPT génération → "
                    "Brevo envoi → WhatsApp adaptation manuelle. Free tier compatible."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 20,
            },
            {
                "title_fr": "Workflow 2 — Séquence multi-canal automatisée",
                "description_fr": (
                    "Pipeline low-code : Apollo enrichissement → OpenAI génération → "
                    "Lemlist séquence → PhantomBuster LinkedIn. Avec A/B testing intégré."
                ),
                "format": "tutorial",
                "difficulty_level": 4,
                "estimated_duration_min": 25,
            },
        ],
        4: [
            {
                "title_fr": "Mission : Lance ta séquence multi-canal sur 30 prospects",
                "description_fr": (
                    "90 minutes chronométrées. Critères : reply rate ≥ 1.5× baseline, "
                    "≥ 50% prospects sur 2+ canaux, ≥ 1 RDV qualifié obtenu/agendé."
                ),
                "format": "exercise",
                "difficulty_level": 4,
                "estimated_duration_min": 90,
            },
        ],
        5: [
            {
                "title_fr": "Collecte baseline reply rate et RDV/semaine",
                "description_fr": (
                    "Mesurer honnêtement ton reply rate actuel et ton nombre de RDV "
                    "qualifiés/semaine avant le module."
                ),
                "format": "exercise",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Bibliothèque personnelle des templates testés",
                "description_fr": (
                    "Conservation de tes 3 meilleurs templates par reply rate. "
                    "Réutilisation et amélioration continue."
                ),
                "format": "tutorial",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Mise à jour du score skill et recommandation suivante",
                "description_fr": (
                    "Si skill 3 < 67/100, recommandation Module 3 (Sales Call). "
                    "Sinon : certificat AI Sales Specialist."
                ),
                "format": "tutorial",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
        ],
    },

    # =========================================================================
    # MODULE 3 — Sales Call Preparation
    # =========================================================================
    3: {
        1: [
            {
                "title_fr": "Le quotidien de Karim : 5 appels improvisés et CRM négligé",
                "description_fr": (
                    "Étude de cas : préparation 5 min, improvisation sur les objections "
                    "prix, notes papier oubliées, sentiment d'impréparation."
                ),
                "format": "case_study",
                "difficulty_level": 1,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Pain points des appels commerciaux en Afrique du Nord",
                "description_fr": (
                    "Préparation insuffisante, gestion d'objections improvisée, CRM "
                    "incomplet, multilinguisme mal géré, calendrier culturel ignoré."
                ),
                "format": "video",
                "difficulty_level": 1,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Spécificités Maghreb : multilinguisme, relationnel, Ramadan",
                "description_fr": (
                    "Pourquoi ces 3 dimensions changent la préparation et le suivi "
                    "des appels en Afrique du Nord — et comment les intégrer dans "
                    "ton briefing IA."
                ),
                "format": "video",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
        ],
        2: [
            {
                "title_fr": "Les 8 compétences des conversations commerciales IA",
                "description_fr": (
                    "Pre-call briefing, génération 3 min, gestion temps réel objections, "
                    "copilots, transcription, CRM auto, mesure qualité, adaptation Maghreb."
                ),
                "format": "video",
                "difficulty_level": 2,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Du briefing-seul à l'agent multi-fonction",
                "description_fr": (
                    "Pourquoi un agent multi-fonction (briefing + temps réel + post-call "
                    "+ CRM) surpasse les solutions partielles."
                ),
                "format": "video",
                "difficulty_level": 3,
                "estimated_duration_min": 10,
            },
        ],
        3: [
            {
                "title_fr": "Prompt 1 — Pre-call briefing 8 sections",
                "description_fr": (
                    "Briefing complet en 3 minutes : résumé, objectifs, questions, "
                    "objections, angle, signaux, next steps, contexte relationnel Maghreb."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Prompt 2 — Bibliothèque d'objection handling",
                "description_fr": (
                    "Construire 3-10 objections récurrentes avec réponse en 4 étapes "
                    "(reformulation, approfondissement, argument, re-engagement)."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Prompt 3 — Post-call : Deal Health + next steps",
                "description_fr": (
                    "Score Deal Health 0-100, pain points, champion interne, decision "
                    "process, brouillon de message de suivi adapté au canal."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Workflow 1 — Préparation manuelle assistée IA",
                "description_fr": (
                    "Pipeline no-code : LinkedIn + CRM → Prompt 1 briefing → "
                    "Otter/Notta transcription → Prompt 3 post-call → CRM update."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 20,
            },
            {
                "title_fr": "Workflow 2 — Briefing automatique 24h avant l'appel",
                "description_fr": (
                    "Pipeline low-code : Google Calendar trigger → HubSpot fetch → "
                    "OpenAI briefing → email automatique → activation Fireflies/Notta."
                ),
                "format": "tutorial",
                "difficulty_level": 4,
                "estimated_duration_min": 25,
            },
        ],
        4: [
            {
                "title_fr": "Mission : 5 appels avec briefing IA + transcription",
                "description_fr": (
                    "60 minutes étalées sur la semaine. Critères : 100 % CRM, "
                    "préparation ≤ 10 min/appel, ≥ 2 next steps précis par appel."
                ),
                "format": "exercise",
                "difficulty_level": 4,
                "estimated_duration_min": 60,
            },
        ],
        5: [
            {
                "title_fr": "Collecte baseline temps de prep et % CRM",
                "description_fr": (
                    "Mesurer ton temps de préparation actuel et ton taux de "
                    "documentation CRM avant le module."
                ),
                "format": "exercise",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Bibliothèque personnelle d'objection handling",
                "description_fr": (
                    "Conservation et amélioration continue de ta bibliothèque "
                    "d'objections issue de tes appels réels."
                ),
                "format": "tutorial",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Vue consolidée des 3 modules : parcours complet",
                "description_fr": (
                    "Synthèse de ton parcours AI Sales Specialist : scores des 3 skills, "
                    "KPIs avant/après, certificat, et bridge commercial Sales Copilot."
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
def seed_ai_sales_specialist_modules(db):
    """
    Seed les 3 modules + 15 units + ~45 lessons + jointures module_skills
    pour le rôle AI Sales Specialist.

    Charge le contenu des modules depuis content/roles/ai_sales_specialist/
    (architecture Option 3 — JSON externe).

    Source de vérité : PDF v1.1 — Mai 2026.

    Idempotent : skip si déjà seedé (vérifie l'existence d'un module
    avec role='AI Sales Specialist' avant de continuer).

    Pré-requis : seed_ai_sales_specialist_diagnostic.py doit avoir été
    exécuté avant (il crée les 3 skills référencées par skill_name dans
    chaque module JSON).
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
            f"⚠️  AI Sales Specialist modules déjà seedés "
            f"({existing_modules} modules pour role='{ROLE}'), skip."
        )
        return

    # =========================================================================
    # 2. Récupérer les skills (seedées par seed_ai_sales_specialist_diagnostic.py)
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
                f"Lance d'abord seed_ai_sales_specialist_diagnostic.py."
            )
        skills_by_name[skill_name] = skill

    # =========================================================================
    # 3. Insérer les 3 modules + units + lessons + jointures module_skills
    # =========================================================================
    total_units_created = 0
    total_lessons_created = 0
    total_module_skill_links = 0

    for module_data in modules_data:
        # Skip individuel si module déjà existant (par title + role)
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
        # Note : title_en, level sont NOT NULL → on duplique le FR dans EN
        # temporairement pour respecter le schéma. V2 : traduction EN propre.
        # Mapping JSON (clés sans _fr) → BDD (colonnes _fr et _en) :
        module = Module(
            title_fr=module_data["title"],
            title_en=module_data["title"],  # FR temporaire dans EN
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
        db.flush()  # pour récupérer module.id

        # ─── 3.2 Créer la jointure module_skills ─────────────────────────
        skill = skills_by_name[module_data["skill_name"]]
        module_skill_link = ModuleSkill(
            module_id=module.id,
            skill_id=skill.id,
        )
        db.add(module_skill_link)
        total_module_skill_links += 1

        # ─── 3.3 Créer les 5 units du module ─────────────────────────────
        units_created = {}  # order → Unit
        for unit_template in UNITS_TEMPLATE:
            unit = Unit(
                module_id=module.id,
                title_fr=unit_template["title_fr"],
                title_en=unit_template["title_fr"],  # FR temporaire dans EN
                description_fr=unit_template["description_fr"],
                description_en=unit_template["description_fr"],
                order=unit_template["order"],
                estimated_duration_min=unit_template["estimated_duration_min"],
                is_active=True,
            )
            db.add(unit)
            db.flush()  # pour récupérer unit.id
            units_created[unit_template["order"]] = unit
            total_units_created += 1

        # ─── 3.4 Créer les lessons par unit ──────────────────────────────
        module_order = module_data["display_order"]
        lessons_for_module = LESSONS_BY_MODULE.get(module_order, {})

        for unit_order, lessons_list in lessons_for_module.items():
            unit = units_created[unit_order]
            for idx, lesson_data in enumerate(lessons_list, start=1):
                lesson = Lesson(
                    unit_id=unit.id,
                    title_fr=lesson_data["title_fr"],
                    title_en=lesson_data["title_fr"],  # FR temporaire dans EN
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
        f"✅ AI Sales Specialist modules seedés (depuis JSON) :\n"
        f"   • {len(modules_data)} modules (role='{ROLE}')\n"
        f"   • {total_units_created} units (5 par module)\n"
        f"   • {total_lessons_created} lessons\n"
        f"   • {total_module_skill_links} jointures module_skills"
    )