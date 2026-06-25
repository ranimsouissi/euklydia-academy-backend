"""
Seed AI Project Manager — Modules pédagogiques v1.0

Contenu pédagogique des 3 modules du parcours AI Project Manager :
- Module 1 : Project Planning Automation
- Module 2 : Risk Identification
- Module 3 : Team Productivity Optimization

Source : PDF "Parcours AI Project Manager v1.0" — Avril 2026 (Ranim Souissi).

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
- prompt_examples_fr   → les 3 prompts ChatGPT par module
- practical_exercise_fr → l'Execution Task chronométrée
- comparison_tables_fr  → les tableaux de tools, KPIs, workflows
- section_content_fr    → le Use Case détaillé + sections complémentaires

DIFFÉRENCE IMPORTANTE vs AI Sales / AI Designer : le bridge commercial du
parcours AI Project Manager s'appuie sur les produits existants Euklydia
(Asana Workforce & Talent Management Agent + HR Platform) et NON sur un
produit phare intégré nouveau. Cette spécificité est documentée dans le
section_content_fr du Module 3.

Bilingue : V1 = FR uniquement. EN dupliqué de FR temporairement pour respecter
les contraintes NOT NULL (title_en, etc.) — sera retraduit en V2.

Idempotent : skip si déjà seedé (pattern aligné sur seed_ai_project_manager_diagnostic.py).
"""
from __future__ import annotations

from app.models.module import Module
from app.models.unit import Unit
from app.models.lesson import Lesson
from app.models.module_skill import ModuleSkill
from app.models.skill import Skill


# =============================================================================
# Constantes
# =============================================================================
ROLE = "AI Project Manager"
CAREER_PATH_ID = 82  # cohérent avec seed_ai_project_manager_diagnostic.py


# =============================================================================
# MODULE 1 — Project Planning Automation
# =============================================================================
MODULE_1 = {
    # ──── Identité du module ──────────────────────────────────────────────────
    "title_fr": "Project Planning Automation",
    "description_fr": (
        "Apprends à construire un plan projet IA-augmenté en moins de 1 heure : "
        "décomposition automatique en phases et tâches, estimations appuyées "
        "par des projets similaires, mapping des dépendances, intégration "
        "directe dans Notion, Asana ou ClickUp. Tu libères 50 à 70 % de ton "
        "temps de planification pour des activités à plus forte valeur ajoutée."
    ),
    "level": "Fondation",
    "role": ROLE,
    "journey_stage": "Cycle de pilotage — Planification",
    "display_order": 1,
    "estimated_duration_min": 240,  # 3-4h
    "format": "blended",
    "is_active": True,

    "skill_name": "AI Project Planning",  # mapping vers skill_id

    # ──── Pédagogie ──────────────────────────────────────────────────────────
    "learning_objective_fr": (
        "À l'issue de ce module, l'apprenant sait (1) construire un plan "
        "projet complet en moins de 1h avec ChatGPT et un brief structuré, "
        "(2) recalibrer ses estimations à partir de l'historique de projets "
        "similaires, et (3) maintenir le plan à jour en continu via une "
        "boucle de revue."
    ),
    "expected_outcome_fr": (
        "Réduction de 50 à 70 % du temps de création d'un plan projet "
        "(30-60 min vs 2-3 jours), précision des estimations améliorée "
        "(écart < 10 % vs 20-30 %), dépendances mappées dès le J0 "
        "(vs découvertes en cours de route)."
    ),
    "why_this_module_fr": (
        "Beaucoup de project managers au Maghreb passent plusieurs jours à "
        "structurer un nouveau plan projet : décomposition en phases, "
        "estimation des tâches, mapping des dépendances, allocation aux "
        "équipes. C'est un travail nécessaire mais répétitif qui prend du "
        "temps au détriment des activités à plus forte valeur ajoutée "
        "(coaching d'équipe, gestion des stakeholders, anticipation "
        "stratégique)."
    ),
    "recommended_when_fr": (
        "Quand tu démarres 2+ projets par mois, que ton temps moyen de "
        "création d'un plan dépasse 1 jour, ou que tes estimations ont "
        "régulièrement un écart de plus de 20 % avec le réel."
    ),
    "role_based_example_fr": (
        "Karim, project manager dans une PME tech à Tunis, gère 3 équipes "
        "en parallèle. Quand un nouveau projet démarre, il passe 2 jours "
        "entiers à construire le planning sur Notion : il liste les tâches "
        "dans sa tête, les estime au feeling, mappe les dépendances en mode "
        "brainstorming. Le résultat est souvent incomplet, des tâches sont "
        "oubliées, les dépendances mal identifiées. Pendant ce temps, ses "
        "équipes attendent et il n'a pas le temps d'animer les sprint "
        "reviews. Avec ce module, Karim livre un plan complet en 1h et "
        "récupère du temps pour le coaching et les stakeholders."
    ),
    "takeaway_fr": (
        "L'IA ne remplace pas la réflexion stratégique du PM, mais "
        "industrialise la partie répétitive de la planification "
        "(décomposition, estimation, dépendances). Le PM se recentre sur "
        "ce qu'il fait de mieux : le pilotage humain, la gestion des "
        "stakeholders, l'anticipation."
    ),
    "action_point_fr": (
        "Cette semaine : choisis un projet à venir, prépare le brief "
        "structuré (objectif, livrables, équipe, contraintes), applique "
        "le Prompt 1 (roadmap) et le Prompt 2 (estimations recalibrées), "
        "et présente le plan à ton équipe en moins de 90 minutes."
    ),
    "practical_application_fr": (
        "Application directe sur tes propres projets : pas de cas fictif. "
        "Tu utilises les prompts sur tes vrais briefs, tu mesures le temps "
        "économisé, et tu construis ta bibliothèque personnelle de plans "
        "templates par type de projet."
    ),

    # ──── Compétences clés (7 axes) ──────────────────────────────────────────
    "key_concepts_fr": [
        "Structure d'un plan projet professionnel (phases, jalons, livrables, dépendances)",
        "Construction d'un brief structuré pour génération IA",
        "Utilisation de ChatGPT/Claude pour générer une roadmap complète en moins de 1h",
        "Maîtrise de Notion AI pour la base projet (timeline, base de tâches, dashboards)",
        "Maîtrise d'Asana ou ClickUp avec leurs templates IA-augmentés",
        "Bibliothèque de plans templates par type de projet (dev, marketing, ops, transformation)",
        "Boucle de revue + ajustement automatique du plan en continu",
    ],

    # ──── Module suivant ─────────────────────────────────────────────────────
    "next_recommended_module_fr": "Risk Identification",

    # =========================================================================
    # JSON — Contenu pédagogique riche
    # =========================================================================

    # ──── PROMPTS — 3 prompts validés ───────────────────────────────────────
    "prompt_examples_fr": [
        {
            "id": "prompt_1_roadmap",
            "title": "Prompt 1 — Génération de roadmap projet complète",
            "use_case": "Transformer un brief projet vague en roadmap structurée en moins de 1h",
            "tags": ["roadmap", "planification", "PMP"],
            "content": (
                "Tu es un project manager senior certifié PMP avec 15 ans d'expérience.\n"
                "Construis une roadmap projet complète et structurée.\n\n"
                "BRIEF PROJET :\n"
                "- Nom : [NOM_PROJET]\n"
                "- Objectif business : [OBJECTIF]\n"
                "- Livrables attendus : [LIVRABLES_PRINCIPAUX]\n"
                "- Deadline : [DATE_LIMITE]\n"
                "- Budget : [BUDGET]\n"
                "- Équipe disponible : [PROFILS_ET_NOMBRE]\n"
                "- Type de projet : [DEV / MARKETING / OPS / TRANSFORMATION]\n"
                "- Contraintes connues : [CONTRAINTES]\n\n"
                "GÉNÈRE UNE ROADMAP EN 6 SECTIONS :\n"
                "1. PHASES PROJET (4 à 6 phases macro)\n"
                "   Pour chaque phase : objectif, durée, livrables clés\n\n"
                "2. DÉCOMPOSITION EN TÂCHES (par phase)\n"
                "   Liste détaillée avec :\n"
                "   - Nom de la tâche\n"
                "   - Estimation (jours-homme)\n"
                "   - Profil requis\n"
                "   - Tâches prérequises\n\n"
                "3. JALONS CLÉS (3 à 5 milestones)\n"
                "   Date estimée + critère de validation\n\n"
                "4. DÉPENDANCES CRITIQUES\n"
                "   Identifier le chemin critique du projet\n\n"
                "5. RISQUES INITIAUX (top 5)\n"
                "   Probabilité × Impact + suggestion de mitigation\n\n"
                "6. RECOMMANDATIONS DE SUIVI\n"
                "   Cadence des points, KPI à tracker, format de reporting\n\n"
                "FORMAT DE SORTIE : tableau Markdown exploitable dans Notion"
            ),
            "variables": ["NOM_PROJET", "OBJECTIF", "LIVRABLES_PRINCIPAUX",
                          "DATE_LIMITE", "BUDGET", "PROFILS_ET_NOMBRE",
                          "CONTRAINTES"],
            "expected_output": "Roadmap 6 sections : phases, tâches, jalons, dépendances, risques, suivi",
            "tools": ["ChatGPT (gratuit ou Plus)", "Notion / Asana / ClickUp"],
        },
        {
            "id": "prompt_2_estimation",
            "title": "Prompt 2 — Estimation comparative basée sur projets similaires",
            "use_case": "Affiner les estimations d'un nouveau projet à partir de l'historique",
            "tags": ["estimation", "historique", "recalibrage"],
            "content": (
                "Tu es un project manager senior expert en estimation.\n"
                "Affine les estimations de mon nouveau projet à partir de l'historique.\n\n"
                "NOUVEAU PROJET :\n"
                "- Type : [TYPE_PROJET]\n"
                "- Scope : [DESCRIPTION_DETAILLEE]\n"
                "- Complexité ressentie : [FAIBLE / MOYENNE / ÉLEVÉE]\n\n"
                "PROJETS SIMILAIRES TERMINÉS (historique) :\n"
                "Pour chacun, fournis :\n"
                "- Nom : [PROJET_X]\n"
                "- Type : [TYPE]\n"
                "- Estimé initial : [JOURS-HOMME]\n"
                "- Réel final : [JOURS-HOMME]\n"
                "- Écart : [%]\n"
                "- Cause principale d'écart : [CAUSE]\n\n"
                "PROJET 1 : ...\n"
                "PROJET 2 : ...\n"
                "PROJET 3 : ...\n\n"
                "GÉNÈRE :\n"
                "1. ESTIMATION RÉCALIBRÉE\n"
                "   - Estimation optimiste : [J/H]\n"
                "   - Estimation réaliste : [J/H]\n"
                "   - Estimation pessimiste : [J/H]\n"
                "   - Recommandation officielle (avec marge de sécurité) : [J/H]\n\n"
                "2. ZONES À RISQUE\n"
                "   Tâches/phases historiquement sous-estimées\n\n"
                "3. APPRENTISSAGES À APPLIQUER\n"
                "   Top 3 leçons des projets précédents à intégrer\n\n"
                "4. CONFIANCE GLOBALE\n"
                "   Note de 1 à 10 sur la fiabilité de l'estimation"
            ),
            "variables": ["TYPE_PROJET", "DESCRIPTION_DETAILLEE", "PROJET_X",
                          "TYPE"],
            "expected_output": "Estimation recalibrée (3 fourchettes) + zones à risque + apprentissages + confiance",
            "tools": ["ChatGPT", "Historique des projets terminés"],
        },
        {
            "id": "prompt_3_mise_a_jour",
            "title": "Prompt 3 — Mise à jour automatique du plan projet",
            "use_case": "Mettre à jour le plan projet à chaque sprint review sans tout refaire",
            "tags": ["mise à jour", "agile", "pilotage"],
            "content": (
                "Tu es un project manager senior, expert en pilotage agile.\n"
                "Mets à jour mon plan projet en intégrant les nouveaux éléments.\n\n"
                "PLAN ACTUEL :\n"
                "[COLLER_LE_PLAN_PROJET_ACTUEL]\n\n"
                "ÉVÉNEMENTS DEPUIS LE DERNIER POINT :\n"
                "- Tâches terminées : [LISTE]\n"
                "- Tâches en cours : [LISTE_AVEC_AVANCEMENT]\n"
                "- Blocages identifiés : [DESCRIPTION]\n"
                "- Changements de scope : [AJOUTS_OU_RETRAITS]\n"
                "- Ressources modifiées : [DÉPARTS / ARRIVÉES]\n\n"
                "MA QUESTION :\n"
                "[POSE_TA_QUESTION_SPÉCIFIQUE]\n"
                "(ex : « la deadline du 30 juin est-elle encore tenable ? »)\n\n"
                "GÉNÈRE LA MISE À JOUR :\n"
                "1. STATUT GLOBAL (Vert / Jaune / Rouge)\n"
                "   Avec justification chiffrée\n\n"
                "2. IMPACT DES ÉVÉNEMENTS\n"
                "   Sur quoi chaque événement modifie le plan\n\n"
                "3. PLAN RÉVISÉ\n"
                "   Phases / jalons / dates mis à jour\n\n"
                "4. RECOMMANDATIONS D'ACTIONS\n"
                "   - Quick wins (cette semaine)\n"
                "   - Décisions à arbitrer (avec sponsor)\n"
                "   - Risques à monitorer de près\n\n"
                "5. COMMUNICATION SUGGÉRÉE\n"
                "   Brouillon de message Slack à l'équipe + email aux stakeholders"
            ),
            "variables": ["COLLER_LE_PLAN_PROJET_ACTUEL", "LISTE",
                          "LISTE_AVEC_AVANCEMENT", "DESCRIPTION",
                          "AJOUTS_OU_RETRAITS", "POSE_TA_QUESTION_SPÉCIFIQUE"],
            "expected_output": "Mise à jour 5 sections : statut, impacts, plan révisé, actions, communication",
            "tools": ["ChatGPT", "Notion / Asana / ClickUp"],
        },
    ],

    # ──── EXERCICE PRATIQUE — Mission terrain chronométrée ──────────────────
    "practical_exercise_fr": {
        "title": "Mission : Génère un plan projet complet en 1h sur un projet réel",
        "duration_minutes": 90,
        "tools_required": [
            "ChatGPT (gratuit)",
            "Notion ou Asana",
        ],
        "objective": (
            "Construire un plan projet IA-augmenté sur un projet réel en moins "
            "de 90 minutes, l'importer dans Notion/Asana, et obtenir la "
            "validation de ton équipe ou sponsor."
        ),
        "steps": [
            {
                "n": 1,
                "title": "Choix du projet",
                "description": (
                    "Choisis un projet à venir (idéalement à démarrer dans les "
                    "2 semaines)."
                ),
            },
            {
                "n": 2,
                "title": "Brief structuré",
                "description": (
                    "Prépare le brief structuré (objectif, livrables, équipe, "
                    "contraintes)."
                ),
            },
            {
                "n": 3,
                "title": "Roadmap complète",
                "description": (
                    "Applique le Prompt 1 et obtiens la roadmap complète en "
                    "6 sections."
                ),
            },
            {
                "n": 4,
                "title": "Recalibrage des estimations",
                "description": (
                    "Applique le Prompt 2 pour recalibrer les 5 estimations "
                    "principales (en utilisant 3+ projets similaires terminés)."
                ),
            },
            {
                "n": 5,
                "title": "Import dans l'outil",
                "description": (
                    "Importe le plan dans Notion ou Asana avec les dépendances "
                    "identifiées."
                ),
            },
            {
                "n": 6,
                "title": "Présentation et validation",
                "description": (
                    "Présente le plan à ton équipe (ou sponsor) et collecte le "
                    "feedback."
                ),
            },
        ],
        "success_criteria": [
            "Plan projet complet livré en moins de 90 minutes (vs 2-3 jours en manuel)",
            "Plan validé par ton équipe ou sponsor (au moins 1 retour positif)",
            "Au moins 5 dépendances critiques identifiées dès le J0",
        ],
        "maghreb_note": (
            "Pour les équipes hybrides Tunis-Casablanca-Alger, intègre dans le "
            "brief les contraintes de calendrier régional (Ramadan, fêtes "
            "nationales différentes selon les pays, weekends Vendredi-Samedi vs "
            "Samedi-Dimanche). ChatGPT les intègre bien si tu les mentionnes "
            "explicitement. Pour les PME avec budgets serrés, demande au prompt "
            "de proposer une version « MVP » et une version « complète » de la "
            "roadmap."
        ),
    },

    # ──── TABLEAUX COMPARATIFS — Tools, Workflows, KPIs ─────────────────────
    "comparison_tables_fr": {
        "tools": {
            "title": "Outils — Comparatif Maghreb",
            "headers": ["Outil", "Pricing", "Usage", "Note Maghreb"],
            "rows": [
                ["ChatGPT / Claude", "Free / 20 USD/mois",
                 "Génération de roadmap, estimations, mises à jour plan",
                 "Free tier suffisant pour démarrer"],
                ["Notion + Notion AI", "Free / 10 USD/utilisateur/mois",
                 "Plan projet, base de tâches, timeline, documentation",
                 "Free tier convient à un PM solo"],
                ["Asana", "Free (jusqu'à 15 users) / 11-25 USD/user",
                 "Gestion de projets et sprints avec IA intégrée",
                 "Carte internationale requise pour Premium"],
                ["ClickUp", "Free / 7-12 USD/user/mois",
                 "Alternative complète : tâches + docs + objectifs + IA",
                 "Free tier généreux, bon pour PME"],
                ["Make / n8n", "Free / 20 USD/mois",
                 "Automatisation des syncs et mises à jour automatiques",
                 "n8n self-hosted ~5 USD/VPS = quasi-gratuit"],
                ["Loom (optionnel)", "Free / 12 USD/mois",
                 "Vidéos de communication aux stakeholders",
                 "Free tier 5 vidéos/mois suffit"],
            ],
        },
        "workflows": {
            "title": "Workflows — 2 niveaux de sophistication",
            "headers": ["Workflow", "Outils", "Setup", "Coût/mois", "Niveau"],
            "rows": [
                ["W1 : Bootstrap d'un plan projet en 1h (no-code)",
                 "ChatGPT + Notion ou Asana",
                 "20-30 min première fois",
                 "0 à 30 USD selon outils",
                 "Débutant"],
                ["W2 : Mise à jour continue du plan (low-code)",
                 "Asana/Jira API + Make/n8n + ChatGPT API + Slack + Notion",
                 "3-5h première fois",
                 "~30-50 USD/mois",
                 "Intermédiaire"],
                ["W2 low-cost Maghreb",
                 "Asana free + n8n self-hosted + ChatGPT manuel + Slack",
                 "4-6h première fois",
                 "~5 USD/mois (VPS n8n)",
                 "Intermédiaire"],
            ],
        },
        "kpi_targets": {
            "title": "KPIs cibles — Baseline personnalisée → Cible",
            "headers": ["Indicateur", "Niveau temporel", "Baseline (J0)", "Cible"],
            "rows": [
                ["Temps de création d'un plan projet complet", "Court terme (J+14)",
                 "À renseigner par l'apprenant",
                 "30 à 60 min (vs 2-3 jours → -70 %)"],
                ["Précision des estimations (vs réel)", "Moyen terme (J+30)",
                 "Écart 20 à 30 %",
                 "Écart < 10 %"],
                ["Identification des dépendances", "Court terme (J+14)",
                 "Découvertes en cours de route",
                 "Mappées dès le J0"],
            ],
        },
    },

    # ──── SECTION CONTENT — Contenu narratif détaillé ───────────────────────
    "section_content_fr": {
        "use_case_detail": {
            "title": "Le problème business",
            "narrative": (
                "Beaucoup de project managers au Maghreb passent plusieurs jours "
                "à structurer un nouveau plan projet : décomposition en phases, "
                "estimation des tâches, mapping des dépendances, allocation aux "
                "équipes. C'est un travail nécessaire mais répétitif qui prend du "
                "temps au détriment des activités à plus forte valeur ajoutée."
            ),
            "pain_points": [
                "Planification lente (2 à 3 jours pour un plan projet de qualité moyenne)",
                "Tâches oubliées ou mal estimées (entre 20 et 30 % d'écart sur le temps réel)",
                "Dépendances non identifiées dès le départ → blocages en cours de route",
                "Pas de réutilisation des plans des projets précédents similaires",
                "Le PM est en retard sur ses autres responsabilités (coaching, stakeholders)",
                "Plans peu lisibles et peu engageants pour les équipes",
            ],
        },
        "kpi_pattern": {
            "title": "Pattern temporel des KPIs (3 niveaux)",
            "description": (
                "Chaque module mesure ses KPIs sur trois niveaux temporels distincts, "
                "rendant le parcours défendable académiquement et crédible commercialement."
            ),
            "levels": [
                {"level": "Court terme", "type": "Productivité (temps gagné)",
                 "horizon": "Mesurable J+14",
                 "examples": "Temps de création du plan, dépendances identifiées au J0"},
                {"level": "Moyen terme", "type": "Qualité (précision estimations)",
                 "horizon": "Mesurable J+30",
                 "examples": "Écart estimé/réel, satisfaction équipe sur le plan"},
                {"level": "Long terme", "type": "Impact business (livraisons à temps)",
                 "horizon": "Observatoire J+60",
                 "examples": "% projets livrés à la deadline, dérive moyenne"},
            ],
        },
        "kpi_measurement_method": {
            "title": "Méthode de collecte des KPIs",
            "milestones": [
                {"when": "J0", "what": "Formulaire de baseline auto-affiché en début de module (obligatoire pour valider le module)"},
                {"when": "J+7", "what": "Rappel par email + notification in-app"},
                {"when": "J+14", "what": "Formulaire de mesure d'impact auto-affiché + rappel"},
                {"when": "J+30", "what": "Rappel pour KPIs moyen terme (précision estimations)"},
            ],
        },
        "tutorials": [
            {"id": "t1", "title": "Génère ton premier plan projet en 1h",
             "duration_min": 15, "format": "vidéo screencast + template Notion à dupliquer"},
            {"id": "t2", "title": "Recalibre tes estimations avec l'historique",
             "duration_min": 20, "format": "vidéo screencast + template Notion historique projets"},
        ],
    },
}


# =============================================================================
# MODULE 2 — Risk Identification
# =============================================================================
MODULE_2 = {
    "title_fr": "Risk Identification",
    "description_fr": (
        "Conduis une risk discovery IA-augmentée qui identifie 80 % des "
        "risques majeurs dès le J0, met en place une veille continue via "
        "l'analyse des comptes-rendus et tickets, et déclenche les playbooks "
        "de mitigation adaptés. Tu réduis tes retards projet de 30 % minimum."
    ),
    "level": "Pratique",
    "role": ROLE,
    "journey_stage": "Cycle de pilotage — Risques",
    "display_order": 2,
    "estimated_duration_min": 300,  # 3-5h
    "format": "blended",
    "is_active": True,

    "skill_name": "AI Risk Intelligence",

    "learning_objective_fr": (
        "À l'issue de ce module, l'apprenant sait (1) conduire un atelier de "
        "risk discovery exhaustif en 1 heure (15-25 risques structurés), "
        "(2) détecter les signaux faibles dans les comptes-rendus et tickets, "
        "et (3) construire des playbooks de mitigation activables "
        "immédiatement."
    ),
    "expected_outcome_fr": (
        "−30 % de retards projet sur l'année (vs 60-80 % de projets en "
        "retard), 15-25 risques identifiés au démarrage (vs 3-5 génériques), "
        "délai entre apparition d'un signal et action correctrice de 0-3 "
        "jours (vs 1-4 semaines)."
    ),
    "why_this_module_fr": (
        "Beaucoup d'équipes projet au Maghreb fonctionnent en mode réactif "
        "face aux risques : on découvre les problèmes quand ils surviennent "
        "(retard d'un fournisseur, départ d'un membre clé, dépendance "
        "technique cachée), puis on improvise. Cette approche génère des "
        "retards, des dépassements de budget et de la frustration. "
        "L'identification proactive des risques est connue depuis longtemps "
        "en gestion de projet, mais elle reste rarement appliquée car "
        "perçue comme chronophage."
    ),
    "recommended_when_fr": (
        "Quand 50 %+ de tes projets accumulent des retards, que ton risk "
        "register contient moins de 5 risques génériques, ou que tu réagis "
        "aux problèmes au lieu de les anticiper."
    ),
    "role_based_example_fr": (
        "Karim pilote un projet de migration cloud sur 4 mois. Au démarrage, "
        "il fait une « petite analyse de risques » de 30 minutes en comité : "
        "3 risques sont identifiés. Trois mois plus tard, le projet a 6 "
        "semaines de retard. Causes : un fournisseur qui n'a pas livré à "
        "temps, une dépendance API non identifiée, un développeur clé qui a "
        "démissionné, un changement de scope demandé par la direction. Aucun "
        "de ces risques n'avait été anticipé. Avec ce module, Karim conduit "
        "une risk discovery exhaustive et met en place une veille continue."
    ),
    "takeaway_fr": (
        "L'anticipation des risques n'est pas une affaire de chance ou "
        "d'expérience seule : c'est une méthode reproductible. La risk "
        "intelligence IA-augmentée transforme une activité subjective en "
        "un processus structuré qui couvre 6 catégories (technique, humain, "
        "fournisseur, scope, financier, externe) et déclenche des playbooks "
        "préparés."
    ),
    "action_point_fr": (
        "Cette semaine : choisis un projet en cours, prépare le brief enrichi "
        "(équipe, stack, fournisseurs, stakeholders), applique le Prompt 1 "
        "(risk discovery), anime un atelier équipe de 45 min pour valider, "
        "et construis 3 playbooks de mitigation pour les risques majeurs."
    ),
    "practical_application_fr": (
        "Application directe sur tes vrais projets en cours. Tu construis "
        "ta bibliothèque de playbooks par type de risque, tu mesures la "
        "réduction des retards, et tu structures une cadence de revue "
        "hebdomadaire."
    ),

    "key_concepts_fr": [
        "Framework de gestion des risques du PMI (Project Management Institute)",
        "Conduite d'une session de risk discovery exhaustive en 1 heure",
        "Construction d'un risk register structuré (probabilité × impact × mitigation)",
        "Détection des signaux faibles dans les comptes-rendus, tickets et messages Slack",
        "Construction de playbooks de mitigation par type de risque (technique, humain, fournisseur)",
        "Mise en place d'une veille continue automatisée du risque",
        "Communication des risques aux stakeholders avec le bon niveau de détail",
    ],

    "next_recommended_module_fr": "Team Productivity Optimization",

    "prompt_examples_fr": [
        {
            "id": "prompt_1_risk_discovery",
            "title": "Prompt 1 — Atelier de risk discovery exhaustif",
            "use_case": "Conduire une session structurée qui couvre les 6 catégories principales de risques",
            "tags": ["risk discovery", "atelier", "PMI"],
            "content": (
                "Tu es un risk manager senior certifié PMP/PMI-RMP avec 15 ans d'expérience.\n"
                "Conduis un atelier de risk discovery exhaustif sur ce projet.\n\n"
                "PROJET ANALYSÉ :\n"
                "- Nom : [NOM_PROJET]\n"
                "- Objectif : [OBJECTIF]\n"
                "- Durée : [DUREE_PREVUE]\n"
                "- Budget : [BUDGET]\n"
                "- Équipe : [PROFILS_ET_NOMBRE]\n"
                "- Type : [DEV / TRANSFORMATION / OPS / MARKETING]\n"
                "- Stack technique / fournisseurs : [TECH_ET_PARTENAIRES]\n"
                "- Stakeholders clés : [SPONSORS_ET_PARTIES_PRENANTES]\n\n"
                "POUR CHAQUE CATÉGORIE, IDENTIFIE 3 À 5 RISQUES :\n"
                "1. RISQUES TECHNIQUES\n"
                "   (architecture, performance, sécurité, dette technique...)\n\n"
                "2. RISQUES HUMAINS / ÉQUIPE\n"
                "   (turnover, surcharge, compétences manquantes, conflits...)\n\n"
                "3. RISQUES FOURNISSEURS / PARTENAIRES\n"
                "   (retard livraison, dépendance, qualité, contractuel...)\n\n"
                "4. RISQUES DE SCOPE\n"
                "   (changements demandés, périmètre flou, sur-spécification...)\n\n"
                "5. RISQUES FINANCIERS\n"
                "   (dépassement budget, retard de paiement, taux de change...)\n\n"
                "6. RISQUES EXTERNES\n"
                "   (réglementaire, géopolitique, Maghreb-spécifique : fêtes, pannes électricité,\n"
                "   disponibilité talents...)\n\n"
                "POUR CHAQUE RISQUE GÉNÈRE :\n"
                "- Description claire (1 phrase)\n"
                "- Probabilité (1-5)\n"
                "- Impact (1-5)\n"
                "- Score de criticité (proba × impact)\n"
                "- Signal d'alerte précoce à surveiller\n"
                "- Action de mitigation préventive\n"
                "- Plan de contingence si le risque se matérialise\n"
                "- Owner désigné dans l'équipe\n\n"
                "FINIS PAR :\n"
                "- Top 5 risques à priorité absolue\n"
                "- Recommandation de cadence de revue (hebdo / bimensuel)"
            ),
            "variables": ["NOM_PROJET", "OBJECTIF", "DUREE_PREVUE", "BUDGET",
                          "PROFILS_ET_NOMBRE", "TECH_ET_PARTENAIRES",
                          "SPONSORS_ET_PARTIES_PRENANTES"],
            "expected_output": "15-25 risques structurés sur 6 catégories + Top 5 + cadence de revue",
            "tools": ["ChatGPT (gratuit ou Plus)", "Notion / Asana"],
        },
        {
            "id": "prompt_2_signaux_faibles",
            "title": "Prompt 2 — Détection de signaux faibles dans les comptes-rendus",
            "use_case": "Analyser comptes-rendus et messages Slack pour détecter automatiquement les signaux faibles",
            "tags": ["signaux faibles", "veille", "Slack"],
            "content": (
                "Tu es un risk analyst senior, expert en analyse sémantique de communications projet.\n"
                "Analyse ces extraits et identifie les signaux faibles cachés.\n\n"
                "CONTEXTE PROJET :\n"
                "- Nom : [PROJET]\n"
                "- Phase actuelle : [PHASE]\n"
                "- Risques déjà identifiés : [TOP_5_RISQUES_REGISTRE]\n\n"
                "DOCUMENTS À ANALYSER :\n"
                "- Comptes-rendus de réunion (2 dernières semaines) : [COLLER]\n"
                "- Messages Slack pertinents : [COLLER]\n"
                "- Tickets bloqués / en retard : [COLLER]\n"
                "- Emails stakeholders : [COLLER]\n\n"
                "GÉNÈRE UNE ANALYSE EN 5 SECTIONS :\n"
                "1. SIGNAUX FAIBLES DÉTECTÉS\n"
                "   Pour chaque signal :\n"
                "   - Citation exacte (avec source)\n"
                "   - Risque potentiel sous-jacent\n"
                "   - Lien avec un risque connu (si oui) ou nouveau\n"
                "   - Niveau d'attention requis (faible / moyen / élevé)\n\n"
                "2. CHANGEMENTS DE TON / SENTIMENT\n"
                "   - Membres de l'équipe : moral, engagement, frustration\n"
                "   - Stakeholders : confiance, agacement, désengagement\n\n"
                "3. SUJETS RÉCURRENTS NON RÉSOLUS\n"
                "   Problèmes mentionnés à plusieurs reprises sans avancée\n\n"
                "4. CONTRADICTIONS DÉTECTÉES\n"
                "   Décalage entre ce qui est dit et ce qui est fait\n\n"
                "5. RECOMMANDATIONS D'ACTIONS\n"
                "   - Conversations à avoir cette semaine (avec qui, sur quoi)\n"
                "   - Mises à jour à apporter au risk register\n"
                "   - Communication suggérée aux stakeholders"
            ),
            "variables": ["PROJET", "PHASE", "TOP_5_RISQUES_REGISTRE",
                          "COLLER"],
            "expected_output": "Analyse 5 sections : signaux faibles, sentiment, sujets récurrents, contradictions, actions",
            "tools": ["ChatGPT", "Slack", "Asana / Jira"],
        },
        {
            "id": "prompt_3_playbook",
            "title": "Prompt 3 — Playbook de mitigation par type de risque",
            "use_case": "Construire des playbooks de réponse standardisés pour les types de risques courants",
            "tags": ["playbook", "mitigation", "incident"],
            "content": (
                "Tu es un risk manager senior, expert en réponse aux incidents projet.\n"
                "Construis un playbook de mitigation complet pour ce type de risque.\n\n"
                "RISQUE À ADRESSER :\n"
                "- Type : [TECHNIQUE / HUMAIN / FOURNISSEUR / SCOPE / FINANCIER / EXTERNE]\n"
                "- Description : [DESCRIPTION_RISQUE]\n"
                "- Sévérité actuelle : [FAIBLE / MOYENNE / ÉLEVÉE / CRITIQUE]\n"
                "- Contexte projet : [PHASE_ACTUELLE_+_DEADLINE]\n\n"
                "GÉNÈRE LE PLAYBOOK EN 7 SECTIONS :\n"
                "1. SIGNAUX D'ACTIVATION\n"
                "   Comment savoir que ce playbook doit être déclenché\n\n"
                "2. ÉVALUATION RAPIDE (15 min)\n"
                "   Questions clés à poser pour confirmer / qualifier\n\n"
                "3. ACTIONS IMMÉDIATES (24h)\n"
                "   - Action 1 : qui fait quoi, dans quel délai\n"
                "   - Action 2 : ...\n"
                "   - Action 3 : ...\n\n"
                "4. PARTIES PRENANTES À INFORMER\n"
                "   - Qui : équipe, sponsor, client\n"
                "   - Quoi : message clé adapté à chaque audience\n"
                "   - Quand : timing recommandé\n\n"
                "5. PLAN DE CONTINGENCE (si l'action immédiate ne suffit pas)\n"
                "   Plans B et C structurés avec critères de bascule\n\n"
                "6. SUIVI POST-INCIDENT\n"
                "   - Indicateurs à monitorer pour vérifier la résolution\n"
                "   - Cadence des points (jusqu'à clôture)\n\n"
                "7. APPRENTISSAGES À CAPITALISER\n"
                "   - Mise à jour du risk register pour les futurs projets\n"
                "   - Documentation à ajouter dans la base de connaissances"
            ),
            "variables": ["DESCRIPTION_RISQUE", "PHASE_ACTUELLE_+_DEADLINE"],
            "expected_output": "Playbook 7 sections : activation, évaluation, actions 24h, communication, contingence, suivi, apprentissages",
            "tools": ["ChatGPT", "Notion (base de connaissances)"],
        },
    ],

    "practical_exercise_fr": {
        "title": "Mission : Conduis un atelier risk discovery sur ton projet en cours",
        "duration_minutes": 120,
        "tools_required": [
            "ChatGPT",
            "Notion ou Asana",
        ],
        "objective": (
            "Conduire une risk discovery exhaustive sur un projet réel et "
            "construire un risk register validé par l'équipe avec 3 playbooks "
            "de mitigation activables."
        ),
        "steps": [
            {"n": 1, "title": "Choix du projet",
             "description": "Choisis 1 projet en cours (idéalement en phase de démarrage ou milieu)."},
            {"n": 2, "title": "Brief enrichi",
             "description": "Prépare le brief projet enrichi (équipe, stack, fournisseurs, stakeholders)."},
            {"n": 3, "title": "Risk discovery IA",
             "description": "Applique le Prompt 1 et obtiens 15-25 risques structurés sur 6 catégories."},
            {"n": 4, "title": "Atelier équipe",
             "description": "Anime un atelier équipe (45 min) pour valider, ajouter, prioriser les risques avec ton équipe."},
            {"n": 5, "title": "Top 5 + playbooks",
             "description": "Sélectionne le Top 5 et construis 3 playbooks de mitigation avec le Prompt 3."},
            {"n": 6, "title": "Cadence de revue",
             "description": "Configure une revue hebdomadaire dans le calendrier de l'équipe + désigne un owner par risque."},
        ],
        "success_criteria": [
            "Risk register avec au moins 15 risques validés par l'équipe",
            "Owner désigné pour chaque risque",
            "Playbook construit pour les 3 risques majeurs",
        ],
        "maghreb_note": (
            "Pour la catégorie « Risques externes Maghreb-spécifiques », pense "
            "explicitement à : décalage de calendrier (Ramadan, Aïd, fêtes "
            "nationales), pannes électriques régulières (Tunisie, Algérie), "
            "disponibilité talents (rareté de certains profils tech), "
            "contraintes réglementaires (RGPD européen pour clients UE, lois "
            "locales sur la donnée). Ces risques sont souvent ignorés des "
            "checklists internationales mais peuvent décaler un projet de "
            "plusieurs semaines."
        ),
    },

    "comparison_tables_fr": {
        "tools": {
            "title": "Outils — Comparatif Maghreb",
            "headers": ["Outil", "Pricing", "Usage", "Note Maghreb"],
            "rows": [
                ["ChatGPT / Claude", "Free / 20 USD/mois",
                 "Risk discovery + signaux faibles + playbooks de mitigation",
                 "Free tier suffisant pour démarrer"],
                ["Notion + Notion AI", "Free / 10 USD/utilisateur/mois",
                 "Risk register, playbooks, base de connaissances post-projet",
                 "Free tier convient à un PM solo"],
                ["Asana / Monday.com", "Free / variable",
                 "Suivi des risques avec champs custom (probabilité, impact, owner)",
                 "Asana free convient à une petite équipe"],
                ["Slack", "Free / 7-12 USD/user/mois",
                 "Source des signaux faibles + canal de notification automatique",
                 "Free tier conserve 90j de messages"],
                ["Make / n8n", "Free / 20 USD/mois",
                 "Orchestration du workflow de veille continue",
                 "n8n self-hosted = quasi-gratuit"],
                ["Loom", "Free / 12 USD/mois",
                 "Communication asynchrone des risques aux stakeholders",
                 "Free tier 5 vidéos/mois suffit"],
            ],
        },
        "workflows": {
            "title": "Workflows — 2 niveaux",
            "headers": ["Workflow", "Outils", "Setup", "Coût/mois", "Niveau"],
            "rows": [
                ["W1 : Risk discovery au démarrage projet (no-code, 2h)",
                 "ChatGPT + Notion / Asana",
                 "30 min première fois",
                 "0 à 30 USD selon outils",
                 "Débutant"],
                ["W2 : Veille continue des signaux faibles (low-code)",
                 "Slack + Asana/Jira API + Make/n8n + ChatGPT API + Notion",
                 "4-6h première fois",
                 "~30-60 USD/mois",
                 "Intermédiaire"],
            ],
        },
        "kpi_targets": {
            "title": "KPIs cibles — Risk Identification",
            "headers": ["Indicateur", "Niveau temporel", "Baseline (J0)", "Cible"],
            "rows": [
                ["Nombre de risques identifiés au démarrage", "Court terme (J+14)",
                 "3 à 5 risques génériques", "15 à 25 risques structurés"],
                ["Délai signal → action correctrice", "Court terme (J+14)",
                 "1 à 4 semaines (réactif)", "0 à 3 jours (proactif)"],
                ["Retards projet sur l'année", "Long terme (J+30 / fin de projet)",
                 "Présents sur 60-80 % des projets", "−30 % de retards"],
            ],
        },
    },

    "section_content_fr": {
        "use_case_detail": {
            "title": "Le problème business",
            "narrative": (
                "Beaucoup d'équipes projet au Maghreb fonctionnent en mode "
                "réactif face aux risques : on découvre les problèmes quand ils "
                "surviennent (retard d'un fournisseur, départ d'un membre clé, "
                "dépendance technique cachée), puis on improvise. Cette approche "
                "génère des retards, des dépassements de budget et de la "
                "frustration."
            ),
            "pain_points": [
                "Issues réactives au lieu de risques anticipés (cause de 70 % des retards)",
                "Registre des risques minimaliste, jamais mis à jour pendant le projet",
                "Pas de signaux faibles capturés dans les comptes-rendus quotidiens",
                "Pas de playbooks de mitigation préparés en avance",
                "Communication des risques aux stakeholders trop tardive",
                "Apprentissage post-projet limité (les leçons ne capitalisent pas)",
            ],
        },
        "tutorials": [
            {"id": "t1", "title": "Conduis ton premier atelier risk discovery",
             "duration_min": 20, "format": "vidéo screencast"},
            {"id": "t2", "title": "Détecte les signaux faibles en 15 minutes par semaine",
             "duration_min": 15, "format": "vidéo screencast + template export Slack/Asana"},
        ],
    },
}


# =============================================================================
# MODULE 3 — Team Productivity Optimization
# =============================================================================
MODULE_3 = {
    "title_fr": "Team Productivity Optimization",
    "description_fr": (
        "Optimise la productivité de ton équipe avec l'IA : priorisation du "
        "backlog selon Eisenhower + RICE, sprint planning en 30 minutes au "
        "lieu de 2 heures, équilibrage automatique de la charge, dashboard "
        "performance hebdomadaire, rétrospectives data-driven. Tu observes "
        "+25 % de productivité d'équipe."
    ),
    "level": "Expert",
    "role": ROLE,
    "journey_stage": "Cycle de pilotage — Exécution",
    "display_order": 3,
    "estimated_duration_min": 300,  # 3-5h
    "format": "blended",
    "is_active": True,

    "skill_name": "AI Execution & Productivity",

    "learning_objective_fr": (
        "À l'issue de ce module, l'apprenant sait (1) prioriser un backlog "
        "de 50-200 tickets en moins de 10 minutes via Eisenhower + RICE, "
        "(2) équilibrer la charge entre membres de l'équipe avec l'IA, et "
        "(3) animer une rétrospective IA-augmentée en 30 minutes."
    ),
    "expected_outcome_fr": (
        "+25 % de sprint completion rate (75-85 % vs 60 %), durée du sprint "
        "planning réduite de 2-3h à 30-45 min, écart de charge entre membres "
        "réduit de 30-50 % à moins de 15 %."
    ),
    "why_this_module_fr": (
        "Beaucoup d'équipes projet au Maghreb travaillent dur mais avancent "
        "lentement : backlog inflationniste, tâches qui traînent en cours, "
        "sprints qui ne se terminent pas, charge mal répartie entre les "
        "membres. Le project manager passe son temps à courir après les "
        "tâches au lieu d'optimiser le système. Les rituels agiles (daily, "
        "sprint planning, retrospective) sont parfois perçus comme une "
        "perte de temps plutôt qu'un levier de productivité."
    ),
    "recommended_when_fr": (
        "Quand ton sprint completion rate est inférieur à 70 %, que ton "
        "sprint planning dépasse 1h, ou que certains membres sont en "
        "surcharge pendant que d'autres sont en sous-charge."
    ),
    "role_based_example_fr": (
        "L'équipe de Karim a 80 tickets dans le backlog Jira. À chaque "
        "sprint planning, Karim improvise une priorisation au feeling : "
        "« celui-ci est urgent, celui-là est important ». Au bout du sprint "
        "de 2 semaines, seulement 60 % des tickets prévus sont livrés. "
        "Certains développeurs sont surchargés, d'autres en sous-charge. "
        "Personne n'a une vision claire de qui fait quoi. Avec ce module, "
        "Karim conduit un sprint planning en 30 minutes, équilibre la "
        "charge, et observe un sprint completion rate de 80 %."
    ),
    "takeaway_fr": (
        "La productivité d'équipe ne se décrète pas : elle s'optimise via "
        "un système. Eisenhower + RICE pour prioriser, équilibrage IA pour "
        "la charge, rétrospectives data-driven pour l'amélioration continue. "
        "Le PM se transforme de « courailleur de tâches » en architecte de "
        "performance."
    ),
    "action_point_fr": (
        "Cette semaine : exporte ton backlog actuel, applique le Prompt 1 "
        "(priorisation Eisenhower + RICE), applique le Prompt 2 (équilibrage "
        "charge), conduis ton sprint planning en 30 minutes, et mesure le "
        "completion rate à la fin du sprint."
    ),
    "practical_application_fr": (
        "Application directe sur ton équipe et ton backlog réel. Tu "
        "construis ta bibliothèque de prompts de sprint, tu mesures "
        "l'amélioration de la performance, et tu structures un rituel "
        "agile efficace et engageant."
    ),

    "key_concepts_fr": [
        "Matrice Eisenhower et framework RICE (Reach, Impact, Confidence, Effort)",
        "Conduite d'un sprint planning IA-augmenté en 30-45 minutes",
        "Équilibrage de la charge de travail entre les membres avec l'IA",
        "Construction d'un dashboard performance d'équipe hebdomadaire",
        "Détection des signaux de burn-out et de sous-charge avant qu'ils impactent",
        "Maîtrise de Jira AI ou ClickUp AI pour automatiser le suivi",
        "Animation de rétrospectives data-driven avec recommandations IA",
    ],

    "next_recommended_module_fr": "Certificat AI Project Manager + Bridge commercial Asana Workforce / HR Platform",

    "prompt_examples_fr": [
        {
            "id": "prompt_1_priorisation",
            "title": "Prompt 1 — Priorisation du backlog Eisenhower + RICE",
            "use_case": "Trier 50-200 tickets en appliquant Eisenhower et RICE",
            "tags": ["Eisenhower", "RICE", "priorisation"],
            "content": (
                "Tu es un product manager senior, expert en priorisation produit.\n"
                "Priorise ce backlog en appliquant Eisenhower + RICE.\n\n"
                "CONTEXTE :\n"
                "- Produit / projet : [DESCRIPTION]\n"
                "- Objectif business du trimestre : [OBJECTIF]\n"
                "- Capacité de l'équipe (sprint) : [POINTS_OU_JOURS]\n"
                "- Persona utilisateur principal : [PERSONA]\n\n"
                "BACKLOG À PRIORISER :\n"
                "Pour chaque ticket :\n"
                "- ID : [TICKET-XXX]\n"
                "- Titre : [TITRE]\n"
                "- Description courte : [DESC]\n"
                "- Demandeur : [QUI]\n"
                "- Estimation : [JOURS]\n\n"
                "TICKET 1 : ...\n"
                "TICKET 2 : ...\n"
                "[etc. jusqu'à 50-200 tickets]\n\n"
                "GÉNÈRE LA PRIORISATION :\n"
                "1. CLASSIFICATION EISENHOWER (4 quadrants)\n"
                "   - Q1 : urgent + important (à faire maintenant)\n"
                "   - Q2 : non-urgent + important (à planifier)\n"
                "   - Q3 : urgent + non-important (à déléguer)\n"
                "   - Q4 : non-urgent + non-important (à éliminer)\n\n"
                "2. SCORING RICE\n"
                "   Pour chaque ticket Q1 et Q2 :\n"
                "   - Reach : combien d'utilisateurs impactés (1-10)\n"
                "   - Impact : effet par utilisateur (1-3)\n"
                "   - Confidence : niveau de certitude (% : 50/80/100)\n"
                "   - Effort : jours-homme requis\n"
                "   - Score RICE = (R × I × C) / E\n\n"
                "3. RECOMMANDATION SPRINT\n"
                "   Top 10 tickets à prendre dans le prochain sprint\n"
                "   Justification du choix\n\n"
                "4. TICKETS À ÉLIMINER\n"
                "   Tickets Q4 + low RICE → suggérer un retrait du backlog\n\n"
                "5. ALERTES\n"
                "   - Sur-représentation d'un demandeur\n"
                "   - Tickets très anciens à archiver\n"
                "   - Manque de tickets sur l'objectif trimestriel"
            ),
            "variables": ["DESCRIPTION", "OBJECTIF", "POINTS_OU_JOURS",
                          "PERSONA", "TICKET-XXX", "TITRE", "DESC", "QUI",
                          "JOURS"],
            "expected_output": "Classification 4 quadrants + scoring RICE + Top 10 sprint + tickets à éliminer + alertes",
            "tools": ["ChatGPT", "Jira / ClickUp (export backlog)"],
        },
        {
            "id": "prompt_2_equilibrage",
            "title": "Prompt 2 — Équilibrage de la charge d'équipe",
            "use_case": "Affecter intelligemment les tickets aux membres en équilibrant charge et compétences",
            "tags": ["équilibrage", "charge", "scrum"],
            "content": (
                "Tu es un scrum master senior expérimenté.\n"
                "Affecte les tickets aux membres en équilibrant charge et compétences.\n\n"
                "ÉQUIPE :\n"
                "Pour chaque membre :\n"
                "- Nom / pseudo : [NOM]\n"
                "- Capacité du sprint (jours / story points) : [CAPACITE]\n"
                "- Compétences principales : [SKILLS]\n"
                "- Préférences / aversions connues : [PREFERENCES]\n"
                "- Charge actuelle (sprint en cours) : [CHARGE]\n\n"
                "MEMBRE 1 : ...\n"
                "MEMBRE 2 : ...\n"
                "[etc.]\n\n"
                "TICKETS À AFFECTER (issus du prompt 1) :\n"
                "[COLLER_TOP_10_TICKETS_PRIORISES]\n\n"
                "GÉNÈRE :\n"
                "1. PROPOSITION D'AFFECTATION\n"
                "   Pour chaque ticket :\n"
                "   - Membre recommandé\n"
                "   - Justification (skill match + charge)\n"
                "   - Membre backup en cas d'absence\n\n"
                "2. RÉPARTITION DE CHARGE FINALE\n"
                "   Tableau par membre :\n"
                "   - Capacité : X jours\n"
                "   - Allocation : Y jours\n"
                "   - Taux de charge : Z %\n\n"
                "3. ÉQUILIBRAGE\n"
                "   - Écart max entre membres\n"
                "   - Identifier les surcharges (>110 %)\n"
                "   - Identifier les sous-charges (<70 %)\n\n"
                "4. RECOMMANDATIONS\n"
                "   - Tickets à déplacer pour rééquilibrer\n"
                "   - Membres à coacher / pairer\n"
                "   - Risques de burn-out à surveiller\n\n"
                "5. SCRIPT DE COMMUNICATION ÉQUIPE\n"
                "   Brouillon de message Slack pour annoncer le sprint"
            ),
            "variables": ["NOM", "CAPACITE", "SKILLS", "PREFERENCES",
                          "CHARGE", "COLLER_TOP_10_TICKETS_PRIORISES"],
            "expected_output": "Affectation par ticket + répartition de charge + alertes équilibrage + recommandations + script Slack",
            "tools": ["ChatGPT", "Jira / ClickUp"],
        },
        {
            "id": "prompt_3_retrospective",
            "title": "Prompt 3 — Rétrospective IA-augmentée",
            "use_case": "Animer une rétrospective fin de sprint en 30 minutes avec analyse data-driven",
            "tags": ["rétrospective", "agile", "data-driven"],
            "content": (
                "Tu es un agile coach senior, expert en facilitation de rétrospectives.\n"
                "Anime une rétrospective complète et actionable.\n\n"
                "DONNÉES DU SPRINT TERMINÉ :\n"
                "- Numéro / nom : [SPRINT_X]\n"
                "- Durée : [JOURS]\n"
                "- Tickets prévus : [N_PREVUS]\n"
                "- Tickets livrés : [N_LIVRES]\n"
                "- Sprint completion rate : [%]\n"
                "- Bugs introduits en prod : [N_BUGS]\n"
                "- Tickets reportés : [N_REPORTES]\n"
                "- Charge réelle vs estimée : [ECART]\n\n"
                "DONNÉES QUALITATIVES :\n"
                "- Verbatim membres équipe : [COLLER_FEEDBACK]\n"
                "- Incidents / blocages : [LISTE]\n"
                "- Demandes de scope changes : [LISTE]\n\n"
                "GÉNÈRE LA RÉTROSPECTIVE EN 5 SECTIONS :\n"
                "1. SYNTHÈSE QUANTITATIVE\n"
                "   - Performance vs sprint précédent\n"
                "   - Tendance sur 3 derniers sprints\n\n"
                "2. CE QUI A BIEN FONCTIONNÉ (3 à 5 points)\n"
                "   Avec preuves chiffrées ou citations\n\n"
                "3. POINTS D'AMÉLIORATION (3 à 5 points)\n"
                "   Causes racines (pas symptômes)\n\n"
                "4. ACTIONS CONCRÈTES POUR LE PROCHAIN SPRINT\n"
                "   Pour chaque action :\n"
                "   - Quoi exactement\n"
                "   - Owner\n"
                "   - Critère de succès mesurable\n\n"
                "5. SIGNAUX FAIBLES À NE PAS MANQUER\n"
                "   - Tendances négatives émergentes\n"
                "   - Membres en risque burn-out\n"
                "   - Pratiques à pérenniser\n\n"
                "6. SCRIPT D'ANIMATION 30 MIN\n"
                "   Comment dérouler la séance avec l'équipe"
            ),
            "variables": ["SPRINT_X", "JOURS", "N_PREVUS", "N_LIVRES",
                          "N_BUGS", "N_REPORTES", "ECART", "COLLER_FEEDBACK",
                          "LISTE"],
            "expected_output": "Rétrospective 6 sections : synthèse, succès, améliorations, actions, signaux faibles, script 30 min",
            "tools": ["ChatGPT", "Jira / ClickUp (data sprint)"],
        },
    ],

    "practical_exercise_fr": {
        "title": "Mission : Conduis un sprint planning IA-augmenté + une rétrospective",
        "duration_minutes": 180,
        "tools_required": [
            "ChatGPT",
            "Jira ou ClickUp",
            "Notion",
        ],
        "objective": (
            "Conduire un sprint planning structuré en 30-45 min avec "
            "priorisation IA + équilibrage de charge, puis animer la "
            "rétrospective fin de sprint avec une amélioration mesurable de "
            "la performance d'équipe."
        ),
        "steps": [
            {"n": 1, "title": "Choix du sprint",
             "description": "Choisis 1 sprint à venir (idéalement avec un backlog d'au moins 30 tickets)."},
            {"n": 2, "title": "Priorisation Eisenhower + RICE",
             "description": "Applique le Prompt 1 et obtiens la priorisation classification + scoring RICE."},
            {"n": 3, "title": "Équilibrage de charge",
             "description": "Applique le Prompt 2 pour équilibrer la charge sur les membres de l'équipe."},
            {"n": 4, "title": "Sprint planning",
             "description": "Anime le sprint planning en 30-45 min avec la proposition IA + validation collective."},
            {"n": 5, "title": "Rétrospective",
             "description": "À la fin du sprint : applique le Prompt 3 pour préparer la rétrospective data-driven."},
            {"n": 6, "title": "Animation et capitalisation",
             "description": "Anime la rétrospective et documente les actions retenues dans Notion."},
        ],
        "success_criteria": [
            "Sprint completion rate de l'équipe en hausse d'au moins 10 % par rapport au sprint précédent",
            "Satisfaction de l'équipe sur le format ≥ 4/5",
            "Au moins 3 actions concrètes documentées avec owner et critère de succès",
        ],
        "maghreb_note": (
            "Pour les équipes hybrides Tunis-Casablanca-Alger, attention aux "
            "écarts horaires et aux weekends différents (Vendredi-Samedi vs "
            "Samedi-Dimanche). Pendant le Ramadan, ajuste la capacité par "
            "membre (typiquement -20 à -30 %) — ne le découvre pas en cours "
            "de sprint. Pour les rétrospectives en équipe multiculturelle, "
            "encourage le feedback écrit anonyme avant la séance, certains "
            "membres seront plus à l'aise pour exprimer les difficultés "
            "à l'écrit qu'à l'oral."
        ),
    },

    "comparison_tables_fr": {
        "tools": {
            "title": "Outils — Comparatif Maghreb",
            "headers": ["Outil", "Pricing", "Usage", "Note Maghreb"],
            "rows": [
                ["ChatGPT / Claude", "Free / 20 USD/mois",
                 "Priorisation backlog + équilibrage charge + rétrospective",
                 "Free tier suffisant pour démarrer"],
                ["Jira + Atlassian Intelligence", "Free / 7-14 USD/user/mois",
                 "Suivi des tickets et sprints, IA intégrée",
                 "Free tier convient à équipes < 10"],
                ["ClickUp + ClickUp AI", "Free / 7-12 USD/user/mois",
                 "Alternative tout-en-un avec IA native",
                 "Free tier généreux pour PME"],
                ["Notion AI", "Free / 10 USD/utilisateur/mois",
                 "Documentation rétrospectives et apprentissages",
                 "Free tier convient"],
                ["Slack", "Free / 7-12 USD/user/mois",
                 "Communication sprint + canal de notifications dashboard",
                 "Free tier conserve 90j de messages"],
                ["Looker Studio / Notion", "Free / variable",
                 "Construction du dashboard performance hebdomadaire",
                 "Looker Studio gratuit, suffit largement"],
                ["Make / n8n", "Free / 20 USD/mois",
                 "Automatisation des syncs et workflows performance",
                 "n8n self-hosted = quasi-gratuit"],
            ],
        },
        "workflows": {
            "title": "Workflows — 2 niveaux",
            "headers": ["Workflow", "Outils", "Setup", "Coût/mois", "Niveau"],
            "rows": [
                ["W1 : Sprint planning éclair en 30 min (no-code)",
                 "ChatGPT + Jira ou ClickUp + Slack",
                 "30 min première fois",
                 "0 à 30 USD selon outils",
                 "Débutant"],
                ["W2 : Dashboard performance hebdo + rétrospective auto (low-code)",
                 "Jira/ClickUp API + Make/n8n + ChatGPT API + Looker Studio + Slack",
                 "5-8h première fois",
                 "~50-100 USD/mois",
                 "Intermédiaire"],
            ],
        },
        "kpi_targets": {
            "title": "KPIs cibles — Team Productivity Optimization",
            "headers": ["Indicateur", "Niveau temporel", "Baseline (J0)", "Cible"],
            "rows": [
                ["Durée du sprint planning", "Court terme (J+14)",
                 "2 à 3 heures", "30 à 45 minutes"],
                ["Sprint completion rate", "Moyen terme (J+30 / 2 sprints)",
                 "60 % du sprint livré", "+25 % (75-85 %)"],
                ["Équilibrage de la charge entre membres", "Moyen terme (J+30)",
                 "Écart 30-50 % entre les plus / moins chargés", "Écart < 15 %"],
            ],
        },
    },

    "section_content_fr": {
        "use_case_detail": {
            "title": "Le problème business",
            "narrative": (
                "Beaucoup d'équipes projet au Maghreb travaillent dur mais "
                "avancent lentement : backlog inflationniste, tâches qui "
                "traînent en cours, sprints qui ne se terminent pas, charge "
                "mal répartie entre les membres. Le project manager passe son "
                "temps à courir après les tâches au lieu d'optimiser le système."
            ),
            "pain_points": [
                "Productivité faible : seulement 60 % du sprint planifié est livré",
                "Priorisation au feeling, pas alignée sur la valeur business",
                "Charge mal équilibrée entre les membres (burn-out d'un côté, ennui de l'autre)",
                "Backlog en croissance permanente, pas de tri régulier",
                "Sprint planning chronophage et peu structuré",
                "Pas de visibilité claire sur la performance individuelle / équipe",
            ],
        },
        "tutorials": [
            {"id": "t1", "title": "Priorise 100 tickets en 10 minutes",
             "duration_min": 15, "format": "vidéo screencast"},
            {"id": "t2", "title": "Anime une rétrospective IA-augmentée",
             "duration_min": 20, "format": "vidéo screencast + template Notion"},
        ],
        "commercial_bridge": {
            "title": "Bridge commercial : Produits existants Euklydia",
            "specificity_note": (
                "Contrairement aux autres parcours (AI Sales / AI Designer) qui "
                "présentent un produit phare unique (Sales Copilot Multi Agent / "
                "BrandStudio), le parcours AI Project Manager s'appuie sur les "
                "produits existants Euklydia déjà déployés chez des clients "
                "comme preuves de crédibilité et points d'entrée commerciaux. "
                "L'offre commerciale exacte (forfait, périmètre, pricing) sera "
                "ajustée au cas par cas selon les résultats du diagnostic et le "
                "contexte client."
            ),
            "products": [
                {
                    "name": "Asana Workforce & Talent Management Agent",
                    "description": (
                        "Agent IA développé par Euklydia, intégré à Asana, qui "
                        "assiste sur les sujets de workforce et talent management "
                        "au sein des équipes projet."
                    ),
                    "owner": "Achref",
                    "status": "Démo vidéo à produire pour intégration au parcours",
                },
                {
                    "name": "HR Platform",
                    "description": (
                        "Plateforme RH développée par Euklydia, complémentaire au "
                        "pilotage de projet pour les sujets de gestion d'équipe "
                        "(compétences, allocation, performance)."
                    ),
                    "owner": "Otmane",
                    "status": "Scope précis et articulation avec le parcours à confirmer avec CEO",
                },
            ],
            "internal_systems_mapping": [
                {"module": "Module 1 — Project Planning Automation",
                 "system": "AI Planning Engine",
                 "kpi": "50-70 % temps gagné en planification"},
                {"module": "Module 2 — Risk Identification",
                 "system": "AI Risk Intelligence System",
                 "kpi": "−30 % de retards projet"},
                {"module": "Module 3 — Team Productivity Optimization",
                 "system": "AI Execution Optimization System",
                 "kpi": "+25 % de productivité d'équipe"},
            ],
            "future_consolidation_note": (
                "Ces 3 systèmes peuvent être présentés ensemble comme une suite "
                "future « Project Excellence Suite » si la stratégie produit "
                "Euklydia décide de consolider une offre dédiée AI PM. À valider "
                "avec CEO."
            ),
            "cta": (
                "Book a demo and launch a 14-day pilot on your own data to "
                "unlock AI-powered project management performance."
            ),
        },
    },
}


# =============================================================================
# Liste des modules à seeder
# =============================================================================
MODULES = [MODULE_1, MODULE_2, MODULE_3]


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
                    "commercial avec les produits existants Euklydia (Asana "
                    "Workforce & Talent Management Agent + HR Platform)."
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
    Seed les 3 modules + 15 units + ~45 lessons + jointures module_skills
    pour le rôle AI Project Manager.

    Source : PDF v1.0 — Avril 2026.

    Idempotent : skip si déjà seedé (vérifie l'existence d'un module
    avec role='AI Project Manager' avant de continuer).

    Pré-requis : seed_ai_project_manager_diagnostic.py doit avoir été
    exécuté avant (il crée les 3 skills 'AI Project Planning',
    'AI Risk Intelligence', 'AI Execution & Productivity' référencées
    par skill_name dans MODULE_*).
    """
    # =========================================================================
    # 0. Anti-doublon — skip si déjà seedé
    # =========================================================================
    existing_modules = (
        db.query(Module)
        .filter(Module.role == ROLE)
        .count()
    )
    if existing_modules >= len(MODULES):
        print(
            f"⚠️  AI Project Manager modules déjà seedés "
            f"({existing_modules} modules pour role='{ROLE}'), skip."
        )
        return

    # =========================================================================
    # 1. Récupérer les skills (seedées par seed_ai_project_manager_diagnostic.py)
    # =========================================================================
    skills_by_name = {}
    for module_data in MODULES:
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
    # 2. Insérer les 3 modules + units + lessons + jointures module_skills
    # =========================================================================
    total_units_created = 0
    total_lessons_created = 0
    total_module_skill_links = 0

    for module_data in MODULES:
        # Skip individuel si module déjà existant (par title_fr + role)
        existing_module = (
            db.query(Module)
            .filter(
                Module.title_fr == module_data["title_fr"],
                Module.role == ROLE,
            )
            .first()
        )
        if existing_module:
            continue

        # ─── 2.1 Créer le module ──────────────────────────────────────────
        # Note : title_en, level sont NOT NULL → on duplique le FR dans EN
        # temporairement pour respecter le schéma. Sera retraduit en V2.
        module = Module(
            title_fr=module_data["title_fr"],
            title_en=module_data["title_fr"],  # FR temporaire dans EN
            description_fr=module_data["description_fr"],
            description_en=module_data["description_fr"],
            learning_objective_fr=module_data["learning_objective_fr"],
            learning_objective_en=module_data["learning_objective_fr"],
            level=module_data["level"],
            estimated_duration_min=module_data["estimated_duration_min"],
            format=module_data["format"],
            role=module_data["role"],
            journey_stage=module_data["journey_stage"],
            display_order=module_data["display_order"],
            expected_outcome_fr=module_data["expected_outcome_fr"],
            expected_outcome_en=module_data["expected_outcome_fr"],
            key_concepts_fr=module_data["key_concepts_fr"],
            key_concepts_en=module_data["key_concepts_fr"],
            role_based_example_fr=module_data["role_based_example_fr"],
            role_based_example_en=module_data["role_based_example_fr"],
            takeaway_fr=module_data["takeaway_fr"],
            takeaway_en=module_data["takeaway_fr"],
            action_point_fr=module_data["action_point_fr"],
            action_point_en=module_data["action_point_fr"],
            practical_application_fr=module_data["practical_application_fr"],
            practical_application_en=module_data["practical_application_fr"],
            recommended_when_fr=module_data["recommended_when_fr"],
            recommended_when_en=module_data["recommended_when_fr"],
            why_this_module_fr=module_data["why_this_module_fr"],
            why_this_module_en=module_data["why_this_module_fr"],
            next_recommended_module_fr=module_data["next_recommended_module_fr"],
            next_recommended_module_en=module_data["next_recommended_module_fr"],
            comparison_tables_fr=module_data["comparison_tables_fr"],
            comparison_tables_en=module_data["comparison_tables_fr"],
            prompt_examples_fr=module_data["prompt_examples_fr"],
            prompt_examples_en=module_data["prompt_examples_fr"],
            section_content_fr=module_data["section_content_fr"],
            section_content_en=module_data["section_content_fr"],
            practical_exercise_fr=module_data["practical_exercise_fr"],
            practical_exercise_en=module_data["practical_exercise_fr"],
            is_active=module_data["is_active"],
        )
        db.add(module)
        db.flush()  # pour récupérer module.id

        # ─── 2.2 Créer la jointure module_skills ─────────────────────────
        skill = skills_by_name[module_data["skill_name"]]
        module_skill_link = ModuleSkill(
            module_id=module.id,
            skill_id=skill.id,
        )
        db.add(module_skill_link)
        total_module_skill_links += 1

        # ─── 2.3 Créer les 5 units du module ─────────────────────────────
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

        # ─── 2.4 Créer les lessons par unit ──────────────────────────────
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
        f"✅ AI Project Manager modules seedés :\n"
        f"   • {len(MODULES)} modules (role='{ROLE}')\n"
        f"   • {total_units_created} units (5 par module)\n"
        f"   • {total_lessons_created} lessons (~3 par unit)\n"
        f"   • {total_module_skill_links} jointures module_skills"
    )