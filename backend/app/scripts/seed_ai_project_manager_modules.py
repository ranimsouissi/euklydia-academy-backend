"""
Seed AI Project Manager — Modules pédagogiques (refactoré v1.1)

Charge le contenu depuis content/roles/ai_project_manager/module_*.json
(architecture Option 3 — JSON externe comme source de vérité).

Contenu pédagogique des 3 modules du parcours AI Project Manager :
- Module 1 : Project Planning Automation
- Module 2 : Risk Identification
- Module 3 : Team Productivity Optimization

Source : PDF Parcours AI Project Manager v1.1 — Mai 2026 — Ranim Souissi.

Architecture pédagogique : chaque module est structuré en 5 unités logiques
qui regroupent les 7 sections du PDF (Use Case, KPI, Skills, Execution Content,
Execution Task, KPI Measurement, Progress Update).

Refactor : le contenu pédagogique (MODULE_1/2/3) est externalisé dans des
fichiers JSON content/roles/ai_project_manager/module_*.json. Ce script
ne contient plus que la structure pédagogique (UNITS_TEMPLATE, LESSONS_BY_MODULE)
et la logique d'insertion BDD.

Idempotent : skip si déjà seedé.

DIFFÉRENCE IMPORTANTE vs AI Sales / AI Designer / AI Marketing : le bridge
commercial du parcours AI Project Manager s'appuie sur des SYSTÈMES Euklydia
internes (AI Planning Engine, AI Risk Intelligence System, AI Execution
Optimization System) et NON sur un produit phare intégré nouveau. Cette
spécificité est documentée dans le section_content.commercial_bridge du
Module 3 JSON.
"""
from app.models.module import Module
from app.models.unit import Unit
from app.models.lesson import Lesson
from app.models.module_skill import ModuleSkill
from app.models.skill import Skill
from app.scripts.content_loader import load_role_modules


# =============================================================================
# Constantes
# =============================================================================
ROLE = "AI Project Manager"
CAREER_PATH_ID = 82
ROLE_SLUG = "ai_project_manager"


# =============================================================================
# UNITS — 5 unités par module (total : 15)
# Les 7 sections du PDF se regroupent en 5 unités logiques.
# Le mapping est identique pour les 3 modules (réplicabilité du modèle pédagogique).
# =============================================================================
UNITS_TEMPLATE = [
    {
        "order": 1,
        "title_fr": "Comprendre le problème business",
        "description_fr": (
            "Le contexte de gestion de projet spécifique en Afrique du Nord, "
            "les pain points typiques que tu rencontres dans ton quotidien, "
            "et les KPIs que tu vas mesurer avant/après pour valider ton "
            "progrès."
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
            "L'Execution Task chronométrée : tu appliques les prompts sur "
            "tes vrais projets, tu mesures le temps gagné, et tu valides "
            "3 critères de réussite chiffrés."
        ),
        "estimated_duration_min": 60,
    },
    {
        "order": 5,
        "title_fr": "Mesure d'impact & Progression",
        "description_fr": (
            "Comment collecter ta baseline à J0, mesurer l'impact à J+14, "
            "et lire les KPIs moyen terme à J+30 / fin de projet. Mise à "
            "jour de ton score skill et recommandation du module suivant."
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
# PRÉSERVATION INTÉGRALE du LESSONS_BY_MODULE du seed v1.0 (Ranim Souissi)
# 42 leçons réparties sur 3 modules × 5 units (14 leçons par module).
# =============================================================================
LESSONS_BY_MODULE = {
    # =========================================================================
    # MODULE 1 — Project Planning Automation
    # =========================================================================
    1: {
        # Unit 1 — Comprendre le problème business
        1: [
            {
                "title_fr": "Le quotidien de Karim : 2 jours pour un planning incomplet",
                "description_fr": (
                    "Étude de cas concrète : Karim, project manager à Tunis, "
                    "et son problème de planification chronophage qui le coupe "
                    "de ses autres responsabilités (coaching, stakeholders)."
                ),
                "format": "case_study",
                "difficulty_level": 1,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Pain points des PM en Afrique du Nord",
                "description_fr": (
                    "Les 6 pain points typiques : planification lente, tâches "
                    "oubliées, dépendances non identifiées, pas de réutilisation, "
                    "PM en retard sur le coaching, plans peu engageants."
                ),
                "format": "video",
                "difficulty_level": 1,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Pattern temporel des KPIs : court / moyen / long terme",
                "description_fr": (
                    "Comprendre pourquoi on distingue KPIs de productivité "
                    "(J+14), qualité estimations (J+30), et impact business "
                    "livraison (fin de projet)."
                ),
                "format": "video",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
        ],
        # Unit 2 — Compétences activées
        2: [
            {
                "title_fr": "Les 7 compétences de la planification IA",
                "description_fr": (
                    "Tour d'horizon des 7 compétences : structure d'un plan, "
                    "brief structuré, ChatGPT pour roadmap, Notion AI, Asana/"
                    "ClickUp templates IA, bibliothèque templates, boucle de "
                    "revue."
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
                "title_fr": "Prompt 1 — Roadmap projet complète (anatomie)",
                "description_fr": (
                    "Décortique le Prompt 1 : transformation d'un brief en "
                    "roadmap 6 sections (phases, tâches, jalons, dépendances, "
                    "risques, suivi). Pourquoi chaque section compte."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Prompt 2 — Estimation comparative par historique",
                "description_fr": (
                    "Recalibrer les estimations à partir de l'historique : 3 "
                    "fourchettes (optimiste/réaliste/pessimiste) + zones à "
                    "risque + apprentissages + niveau de confiance."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Prompt 3 — Mise à jour du plan en continu",
                "description_fr": (
                    "Maintenir le plan à jour à chaque sprint review : statut "
                    "global Vert/Jaune/Rouge, impacts, plan révisé, actions "
                    "recommandées, communication suggérée."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Workflow 1 — Bootstrap d'un plan projet en 1h (no-code)",
                "description_fr": (
                    "Pipeline complet : brief 15 min → Prompt 1 roadmap → "
                    "Prompt 2 recalibrage → import Notion/Asana → revue équipe "
                    "30 min → communication stakeholders. Setup 20-30 min."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 20,
            },
            {
                "title_fr": "Workflow 2 — Mise à jour continue du plan (low-code)",
                "description_fr": (
                    "Pipeline industriel : sync Asana/Jira API → trigger hebdo → "
                    "ChatGPT API + Prompt 3 → versioning Notion → notification "
                    "Slack avec diff → validation équipe en sprint planning."
                ),
                "format": "tutorial",
                "difficulty_level": 4,
                "estimated_duration_min": 25,
            },
        ],
        # Unit 4 — Mission terrain
        4: [
            {
                "title_fr": "Mission : Génère un plan projet complet en 1h",
                "description_fr": (
                    "90 minutes chronométrées sur un projet réel. Critères de "
                    "réussite : plan complet en moins de 90 min, validé par "
                    "l'équipe ou le sponsor, 5+ dépendances critiques au J0."
                ),
                "format": "exercise",
                "difficulty_level": 4,
                "estimated_duration_min": 90,
            },
        ],
        # Unit 5 — Mesure d'impact & Progression
        5: [
            {
                "title_fr": "Collecte de la baseline à J0",
                "description_fr": (
                    "Comment mesurer honnêtement ton temps actuel de "
                    "planification et ta précision d'estimation avant tout "
                    "changement. Formulaire intégré."
                ),
                "format": "exercise",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Mécanisme de relance J+7 / J+14 / J+30",
                "description_fr": (
                    "Comprendre pourquoi on mesure plusieurs fois : isoler "
                    "l'effet du module, distinguer effet ponctuel vs durable, "
                    "observer le moyen terme sur la précision des estimations."
                ),
                "format": "video",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Lecture du dashboard et recommandation suivante",
                "description_fr": (
                    "Lire ton comparatif baseline vs J+14, mettre à jour ton "
                    "score skill « AI Project Planning », et choisir ton "
                    "prochain module."
                ),
                "format": "tutorial",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
        ],
    },

    # =========================================================================
    # MODULE 2 — Risk Identification
    # =========================================================================
    2: {
        1: [
            {
                "title_fr": "Le quotidien de Karim : 6 semaines de retard sur la migration cloud",
                "description_fr": (
                    "Étude de cas : Karim avait fait une « petite analyse » de "
                    "30 min au démarrage. Trois mois plus tard, 4 risques "
                    "non-anticipés ont décalé le projet de 6 semaines."
                ),
                "format": "case_study",
                "difficulty_level": 1,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Pain points de la gestion des risques en Afrique du Nord",
                "description_fr": (
                    "Les 6 pain points : issues réactives, registre minimaliste, "
                    "signaux faibles non capturés, pas de playbooks, communication "
                    "tardive, apprentissage post-projet limité."
                ),
                "format": "video",
                "difficulty_level": 1,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Risques externes Maghreb-spécifiques",
                "description_fr": (
                    "Calendrier régional (Ramadan, Aïd, fêtes nationales), "
                    "pannes électriques, disponibilité talents tech, contraintes "
                    "réglementaires locales : ces risques sont souvent ignorés "
                    "des checklists internationales."
                ),
                "format": "video",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
        ],
        2: [
            {
                "title_fr": "Les 7 compétences du Risk Intelligence",
                "description_fr": (
                    "Framework PMI, atelier risk discovery, risk register "
                    "structuré, signaux faibles, playbooks par type, veille "
                    "continue, communication stakeholders."
                ),
                "format": "video",
                "difficulty_level": 2,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Du mode réactif au mode proactif",
                "description_fr": (
                    "Pourquoi 70 % des retards sont des risques non-anticipés "
                    "et comment passer d'une posture réactive à une posture "
                    "proactive structurée."
                ),
                "format": "video",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
        ],
        3: [
            {
                "title_fr": "Prompt 1 — Atelier risk discovery (6 catégories)",
                "description_fr": (
                    "Identifier 15-25 risques structurés sur 6 catégories : "
                    "technique, humain, fournisseur, scope, financier, externe. "
                    "Pour chaque risque : description, proba, impact, signal "
                    "d'alerte, mitigation, contingence, owner."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Prompt 2 — Détection de signaux faibles",
                "description_fr": (
                    "Analyser comptes-rendus, Slack, tickets, emails pour "
                    "détecter les signaux faibles, changements de sentiment, "
                    "sujets récurrents non résolus, contradictions."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Prompt 3 — Playbook de mitigation par type",
                "description_fr": (
                    "Construire des playbooks 7 sections : signaux d'activation, "
                    "évaluation rapide, actions 24h, parties prenantes à "
                    "informer, plan de contingence, suivi post-incident, "
                    "apprentissages."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Workflow 1 — Risk discovery au démarrage projet (no-code, 2h)",
                "description_fr": (
                    "Pipeline 2h : brief enrichi → Prompt 1 (15-25 risques) → "
                    "atelier équipe 45 min → Prompt 3 sur Top 5 → import risk "
                    "register Notion/Asana → owner + cadence."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 20,
            },
            {
                "title_fr": "Workflow 2 — Veille continue des signaux faibles (low-code)",
                "description_fr": (
                    "Pipeline continu : sync Slack + Asana/Jira → trigger hebdo → "
                    "ChatGPT API + Prompt 2 → ajout au risk register → "
                    "notification PM → déclenchement automatique playbook si "
                    "signal critique."
                ),
                "format": "tutorial",
                "difficulty_level": 4,
                "estimated_duration_min": 25,
            },
        ],
        4: [
            {
                "title_fr": "Mission : Conduis un atelier risk discovery sur ton projet en cours",
                "description_fr": (
                    "120 minutes étalées sur la semaine. Critères : 15+ risques "
                    "validés par l'équipe, owner désigné par risque, playbook "
                    "construit pour les 3 risques majeurs."
                ),
                "format": "exercise",
                "difficulty_level": 4,
                "estimated_duration_min": 120,
            },
        ],
        5: [
            {
                "title_fr": "Collecte baseline retards et risques identifiés",
                "description_fr": (
                    "Mesurer honnêtement le % de tes projets en retard et le "
                    "nombre de risques que tu identifies au démarrage avant le "
                    "module."
                ),
                "format": "exercise",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Bibliothèque personnelle de playbooks de mitigation",
                "description_fr": (
                    "Conservation et amélioration continue de ta bibliothèque "
                    "de playbooks par type de risque (technique, humain, "
                    "fournisseur, scope, financier, externe)."
                ),
                "format": "tutorial",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Mise à jour du score skill et recommandation suivante",
                "description_fr": (
                    "Si skill 3 < 67/100, recommandation Module 3 (Team "
                    "Productivity Optimization). Sinon : certificat AI Project "
                    "Manager."
                ),
                "format": "tutorial",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
        ],
    },

    # =========================================================================
    # MODULE 3 — Team Productivity Optimization
    # =========================================================================
    3: {
        1: [
            {
                "title_fr": "Le quotidien de Karim : 80 tickets, 60 % de completion rate",
                "description_fr": (
                    "Étude de cas : Karim improvise une priorisation au feeling, "
                    "certains devs sont surchargés, d'autres en sous-charge, et "
                    "personne n'a une vision claire de qui fait quoi."
                ),
                "format": "case_study",
                "difficulty_level": 1,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Pain points de la productivité d'équipe en Afrique du Nord",
                "description_fr": (
                    "Les 6 pain points : 60 % completion rate, priorisation au "
                    "feeling, charge mal équilibrée, backlog inflationniste, "
                    "sprint planning chronophage, pas de visibilité performance."
                ),
                "format": "video",
                "difficulty_level": 1,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Spécificités Maghreb : Ramadan, calendriers décalés, équipes distribuées",
                "description_fr": (
                    "Pourquoi ces 3 dimensions changent la planification de "
                    "sprint et l'équilibrage de charge — et comment les "
                    "intégrer dans tes prompts IA dès le départ."
                ),
                "format": "video",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
        ],
        2: [
            {
                "title_fr": "Les 7 compétences de l'Execution & Productivity",
                "description_fr": (
                    "Eisenhower + RICE, sprint planning IA-augmenté, équilibrage "
                    "charge, dashboard performance, signaux burn-out, Jira/"
                    "ClickUp AI, rétrospectives data-driven."
                ),
                "format": "video",
                "difficulty_level": 2,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Du PM courailleur de tâches à l'architecte de performance",
                "description_fr": (
                    "Comment l'IA transforme le rôle du PM : moins de "
                    "micro-management, plus d'optimisation systémique. La "
                    "productivité d'équipe ne se décrète pas, elle s'optimise."
                ),
                "format": "video",
                "difficulty_level": 3,
                "estimated_duration_min": 10,
            },
        ],
        3: [
            {
                "title_fr": "Prompt 1 — Priorisation backlog Eisenhower + RICE",
                "description_fr": (
                    "Trier 50-200 tickets en 4 quadrants Eisenhower puis "
                    "scoring RICE (Reach × Impact × Confidence / Effort) pour "
                    "Q1 et Q2. Top 10 sprint + tickets à éliminer + alertes."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Prompt 2 — Équilibrage de la charge d'équipe",
                "description_fr": (
                    "Affecter intelligemment les tickets en équilibrant "
                    "capacité, compétences, et préférences. Détection des "
                    "surcharges (>110 %) et sous-charges (<70 %), risques "
                    "burn-out, script de communication équipe."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Prompt 3 — Rétrospective IA-augmentée",
                "description_fr": (
                    "Animer une rétro 30 min data-driven : synthèse "
                    "quantitative, ce qui a marché, points d'amélioration "
                    "(causes racines), actions concrètes avec owner, signaux "
                    "faibles, script d'animation."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Workflow 1 — Sprint planning éclair en 30 min (no-code)",
                "description_fr": (
                    "Pipeline 30 min : export backlog J-1 → Prompt 1 priorisation "
                    "→ Prompt 2 équilibrage → sprint planning 30 min → import "
                    "Jira/ClickUp → annonce Slack."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 20,
            },
            {
                "title_fr": "Workflow 2 — Dashboard performance hebdo + rétro auto (low-code)",
                "description_fr": (
                    "Pipeline continu : sync Jira/ClickUp API → calcul completion "
                    "rate + charge + blocages → dashboard Looker Studio → fin "
                    "de sprint : Prompt 3 rétro pré-rédigée → animation 30 min."
                ),
                "format": "tutorial",
                "difficulty_level": 4,
                "estimated_duration_min": 25,
            },
        ],
        4: [
            {
                "title_fr": "Mission : Sprint planning IA-augmenté + rétrospective",
                "description_fr": (
                    "180 minutes étalées sur le sprint. Critères : completion "
                    "rate +10 %, satisfaction équipe ≥ 4/5, 3+ actions "
                    "concrètes avec owner et critère de succès."
                ),
                "format": "exercise",
                "difficulty_level": 4,
                "estimated_duration_min": 180,
            },
        ],
        5: [
            {
                "title_fr": "Collecte baseline completion rate et durée sprint planning",
                "description_fr": (
                    "Mesurer honnêtement ton sprint completion rate actuel et "
                    "la durée moyenne de tes sprint planning avant le module."
                ),
                "format": "exercise",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Bibliothèque personnelle de prompts et templates de sprint",
                "description_fr": (
                    "Conservation et amélioration continue de ta bibliothèque "
                    "de prompts adaptés à ton équipe, ton secteur, et ta cadence."
                ),
                "format": "tutorial",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Vue consolidée : parcours complet AI Project Manager",
                "description_fr": (
                    "Synthèse de ton parcours AI Project Manager : scores des "
                    "3 skills, KPIs avant/après, certificat, et bridge "
                    "commercial avec les systèmes Euklydia (AI Planning Engine, "
                    "AI Risk Intelligence System, AI Execution Optimization "
                    "System)."
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
def seed_ai_project_manager_modules(db):
    """
    Seed les 3 modules + 15 units + 42 lessons + jointures module_skills
    pour le rôle AI Project Manager.

    Lit le contenu des modules depuis content/roles/ai_project_manager/module_*.json
    via le content_loader. Préserve la structure pédagogique (UNITS_TEMPLATE,
    LESSONS_BY_MODULE) qui reste dans ce script.

    Idempotent : skip si déjà seedé (vérifie l'existence d'un module
    avec role='AI Project Manager' avant de continuer).

    Pré-requis : seed_ai_project_manager_diagnostic.py doit avoir été
    exécuté avant (il crée les 3 skills 'AI Project Planning',
    'AI Risk Intelligence', 'AI Execution & Productivity' référencées
    par skill_name dans les JSON modules).
    """
    # =========================================================================
    # 0. Chargement du contenu depuis les JSON
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
            f"⚠️  AI Project Manager modules déjà seedés "
            f"({existing_modules} modules pour role='{ROLE}'), skip."
        )
        return

    # =========================================================================
    # 2. Récupérer les skills (seedées par seed_ai_project_manager_diagnostic.py)
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
                f"Lance d'abord seed_ai_project_manager_diagnostic.py."
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
        # temporairement pour respecter le schéma. Sera retraduit en V2.
        # Mapping JSON (clés plates) → BDD (colonnes _fr et _en).
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
            is_active=module_data.get("is_active", True),
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
        f"✅ AI Project Manager modules seedés (depuis JSON) :\n"
        f"   • {len(modules_data)} modules (role='{ROLE}')\n"
        f"   • {total_units_created} units (5 par module)\n"
        f"   • {total_lessons_created} lessons\n"
        f"   • {total_module_skill_links} jointures module_skills"
    )
