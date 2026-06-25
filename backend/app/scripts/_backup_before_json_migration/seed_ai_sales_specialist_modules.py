"""
Seed AI Sales Specialist — Modules pédagogiques v2.0

Contenu pédagogique des 3 modules du parcours AI Sales Specialist :
- Module 1 : Lead Qualification Automation
- Module 2 : Personalized Outreach at Scale
- Module 3 : Sales Call Preparation

Source : PDF "Parcours AI Sales Specialist v2.0" — Validation 8 mai 2026.
105 corrections validées appliquées sur 9 phases.

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

Bilingue : V1 = FR uniquement. EN dupliqué de FR temporairement pour respecter
les contraintes NOT NULL (title_en, etc.) — sera retraduit en V2.

Idempotent : skip si déjà seedé (pattern aligné sur seed_ai_sales_specialist_diagnostic.py).
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
ROLE = "AI Sales Specialist"
CAREER_PATH_ID = 79  # cohérent avec seed_ai_sales_specialist_diagnostic.py


# =============================================================================
# MODULE 1 — Lead Qualification Automation
# =============================================================================
MODULE_1 = {
    # ──── Identité du module ──────────────────────────────────────────────────
    "title_fr": "Lead Qualification Automation",
    "description_fr": (
        "Apprends à qualifier tes leads B2B en Afrique du Nord avec l'IA, en "
        "utilisant des frameworks reconnus (BANT, fit produit, signaux d'achat) "
        "et en intégrant le scoring directement dans ton CRM. Tu passeras d'une "
        "qualification manuelle chronophage (10 min/lead) à un scoring "
        "structuré et reproductible (2-3 min/lead)."
    ),
    "level": "Fondation",
    "role": ROLE,
    "journey_stage": "Cycle de vente — Qualification",
    "display_order": 1,
    "estimated_duration_min": 240,  # 3-4h
    "format": "blended",
    "is_active": True,

    "skill_name": "Qualification IA des leads",  # mapping vers skill_id

    # ──── Pédagogie ──────────────────────────────────────────────────────────
    "learning_objective_fr": (
        "À l'issue de ce module, l'apprenant sait (1) qualifier ses leads "
        "avec des prompts IA structurés, et (2) automatiser ce scoring via "
        "un workflow intégré au CRM."
    ),
    "expected_outcome_fr": (
        "Réduction de 70 à 85 % du temps de qualification par lead, "
        "+25 à +40 % d'amélioration relative du taux de conversion lead → "
        "opportunité (observatoire J+30/J+60), > 80 % des fiches enrichies."
    ),
    "why_this_module_fr": (
        "Beaucoup d'équipes commerciales B2B en Afrique du Nord font face au "
        "même problème : un volume important de leads entrants et sortants, "
        "mais une qualification approximative et chronophage. Le commercial "
        "passe trop de temps sur des prospects à faible potentiel, ce qui "
        "dégrade le taux de conversion et démotive l'équipe."
    ),
    "recommended_when_fr": (
        "Quand tu reçois 30+ leads/semaine, que tu passes plus de 5h/semaine "
        "à les qualifier manuellement, ou que ton taux de conversion lead → "
        "opportunité est inférieur à 15 %."
    ),
    "role_based_example_fr": (
        "Karim, responsable commercial chez ABC Trading à Tunis (PME export "
        "agroalimentaire), reçoit chaque semaine entre 30 et 50 leads via son "
        "site web, des salons régionaux (Carthage Business Angels, GITEX "
        "Africa), et des recommandations bouche-à-oreille. Il passe en "
        "moyenne 10 minutes par lead à fouiller LinkedIn et son CRM, soit "
        "5 à 8 heures par semaine perdues en qualification manuelle. "
        "Avec ce module, Karim divise son temps de qualification par 4 et "
        "structure une méthode reproductible pour son équipe."
    ),
    "takeaway_fr": (
        "Un scoring IA bien construit (BANT + fit + signaux d'achat) "
        "transforme la qualification d'une activité subjective et "
        "chronophage en un processus rapide, reproductible et défendable "
        "auprès de l'équipe Marketing."
    ),
    "action_point_fr": (
        "Cette semaine : sélectionne tes 10 derniers leads non qualifiés, "
        "applique le Prompt 1 (BANT) à chacun, et compare le score IA à "
        "ton intuition. Identifie au moins 3 leads où l'écart est ≥ 25 points."
    ),
    "practical_application_fr": (
        "Application directe sur tes propres leads : pas de cas fictif. "
        "Tu utilises les prompts sur tes données CRM réelles, tu mesures "
        "le temps gagné, et tu reportes les scores dans ton CRM pour "
        "construire un historique défendable."
    ),

    # ──── Compétences clés (8 axes) ──────────────────────────────────────────
    "key_concepts_fr": [
        "Frameworks de qualification : BANT, fit produit, intent signals",
        "Prompts ChatGPT structurés pour évaluation de leads",
        "Détection de signaux d'achat sur LinkedIn et le web",
        "Classification A/B/C/D des leads selon priorité",
        "Activation du scoring natif CRM (HubSpot AI, Salesforce Einstein, Zoho Zia)",
        "Construction de workflows de scoring multi-étapes",
        "Mesure d'impact concret sur les KPIs commerciaux",
        "Adaptation au contexte B2B Afrique du Nord (cycles longs, références, relationnel)",
    ],

    # ──── Module suivant ─────────────────────────────────────────────────────
    "next_recommended_module_fr": "Personalized Outreach at Scale",

    # =========================================================================
    # JSON — Contenu pédagogique riche
    # =========================================================================

    # ──── PROMPTS — 3 prompts ChatGPT validés ───────────────────────────────
    "prompt_examples_fr": [
        {
            "id": "prompt_1_bant_scoring",
            "title": "Prompt 1 — BANT Scoring",
            "use_case": "Qualifier rapidement un nouveau lead selon BANT avec score sur 100",
            "tags": ["BANT", "scoring", "qualification"],
            "content": (
                "Tu es un expert commercial B2B au Maghreb avec 15 ans d'expérience.\n"
                "Évalue ce lead selon BANT et donne-moi un score sur 100 avec recommandation.\n\n"
                "LEAD :\n"
                "- Nom : [NOM_DU_CONTACT]\n"
                "- Poste : [POSTE]\n"
                "- Entreprise : [ENTREPRISE]\n"
                "- Secteur : [SECTEUR]\n"
                "- Taille : [TAILLE_EMPLOYES]\n"
                "- Pays : [PAYS]\n"
                "- Source : [SOURCE]\n"
                "- Message : [MESSAGE_DU_LEAD]\n"
                "- Budget évoqué (si connu) : [BUDGET]\n"
                "- Rôle dans la décision (si connu) : [ROLE_DECISION]\n\n"
                "MON OFFRE :\n"
                "- Nous vendons : [DESCRIPTION_OFFRE]\n"
                "- Cible idéale : [PROFIL_CLIENT_IDEAL]\n"
                "- Prix moyen avec devise (TND/MAD/DZD/EUR/USD) : [PRIX_MOYEN]\n\n"
                "CONSIGNE :\n"
                "1. BUDGET : capacité financière (0-25)\n"
                "2. AUTHORITY : pouvoir de décision (0-25)\n"
                "3. NEED : besoin réel et explicite (0-25)\n"
                "4. TIMELINE : délai d'achat (0-25)\n"
                "Si une info manque : scorer avec un signe ? et lister les manques.\n\n"
                "LOGIQUE DE DÉCISION (grille v2.0) :\n"
                "- Score ≥ 70 → Appel 24h (lead chaud)\n"
                "- Score 50-69 → Email cette semaine (lead tiède)\n"
                "- Score 30-49 → Nurturing (lead froid)\n"
                "- Score < 30 → Disqualifier (hors cible)\n\n"
                "FORMAT :\n"
                "SCORE : XX/100\n"
                "DÉTAIL : Budget XX/25 | Authority XX/25 | Need XX/25 | Timeline XX/25\n"
                "ACTION : [selon grille ci-dessus]\n"
                "POINTS DE VIGILANCE : [2-3 points]"
            ),
            "variables": ["NOM_DU_CONTACT", "POSTE", "ENTREPRISE", "SECTEUR", "TAILLE_EMPLOYES",
                          "PAYS", "SOURCE", "MESSAGE_DU_LEAD", "BUDGET", "ROLE_DECISION",
                          "DESCRIPTION_OFFRE", "PROFIL_CLIENT_IDEAL", "PRIX_MOYEN"],
            "expected_output": "Score sur 100 avec décomposition BANT + action recommandée + points de vigilance",
            "tools": ["ChatGPT (gratuit ou Plus)"],
        },
        {
            "id": "prompt_2_buying_signals",
            "title": "Prompt 2 — Buying Signals Detection",
            "use_case": "Détecter les signaux d'achat sur LinkedIn et le web pour prioriser un prospect",
            "tags": ["signaux", "LinkedIn", "intent"],
            "content": (
                "Tu es un analyste commercial B2B au Maghreb spécialisé dans la "
                "détection de signaux d'achat.\n\n"
                "PROSPECT :\n"
                "- Nom : [NOM]\n"
                "- Poste : [POSTE]\n"
                "- Entreprise : [ENTREPRISE]\n"
                "- Ancienneté : [ANCIENNETE]\n"
                "- Infos LinkedIn copiées (résumé, expérience, posts récents) : "
                "[INFOS_LINKEDIN_COPIEES]\n\n"
                "ENTREPRISE :\n"
                "- Activité : [DESCRIPTION]\n"
                "- Effectif : [EFFECTIF]\n"
                "- Croissance : [INDICATEUR_CROISSANCE]\n"
                "- Actualités 6 derniers mois (1-3 actualités factuelles avec date) : [ACTUALITES]\n"
                "- Postes ouverts : [RECRUTEMENTS]\n\n"
                "MON OFFRE : [DESCRIPTION_OFFRE]\n\n"
                "CONSIGNE :\n"
                "1. Identifie 3 à 5 signaux d'achat pertinents.\n"
                "2. Indique l'intensité : FORT / MOYEN / FAIBLE.\n"
                "3. Propose un angle d'approche commercial.\n"
                "   → Précise pour quel canal : email / LinkedIn / WhatsApp.\n"
                "4. Suggère 2 questions à poser au premier contact."
            ),
            "variables": ["NOM", "POSTE", "ENTREPRISE", "ANCIENNETE", "INFOS_LINKEDIN_COPIEES",
                          "DESCRIPTION", "EFFECTIF", "INDICATEUR_CROISSANCE", "ACTUALITES",
                          "RECRUTEMENTS", "DESCRIPTION_OFFRE"],
            "expected_output": "3-5 signaux d'achat avec intensité + angle d'approche par canal + questions",
            "tools": ["ChatGPT", "LinkedIn Sales Navigator (optionnel)"],
        },
        {
            "id": "prompt_3_classification",
            "title": "Prompt 3 — Classification A/B/C/D",
            "use_case": "Trier rapidement un batch de 10-20 leads en 4 catégories de priorité",
            "tags": ["classification", "priorisation", "batch"],
            "content": (
                "Tu es un manager commercial B2B au Maghreb.\n\n"
                "CATÉGORIES (alignées sur grille BANT v2.0) :\n"
                "- A = Score ≥ 70 → Appel 24h (lead chaud)\n"
                "- B = Score 50-69 → Email cette semaine (lead tiède)\n"
                "- C = Score 30-49 → Nurturing (lead froid)\n"
                "- D = Score < 30 → Disqualifier (hors cible)\n\n"
                "MON OFFRE : [DESCRIPTION_OFFRE]\n"
                "CIBLE IDÉALE : [PROFIL_CLIENT_IDEAL]\n"
                "PAYS CIBLES : [PAYS]\n\n"
                "LISTE (max 20 leads par batch ; faire plusieurs batches si plus) :\n"
                "Lead 1 :\n"
                "- Nom : [NOM] | Poste : [POSTE] | Entreprise : [ENTREPRISE]\n"
                "- Source : [SOURCE]\n"
                "- Notes (besoin exprimé + budget si évoqué + délai si mentionné) : [INFOS_BREVES]\n"
                "Lead 2 : ...\n\n"
                "FORMAT : tableau Lead | Catégorie | Justification | Action\n"
                "SYNTHÈSE : Total A / B / C / D + Recommandation globale"
            ),
            "variables": ["DESCRIPTION_OFFRE", "PROFIL_CLIENT_IDEAL", "PAYS", "NOM", "POSTE",
                          "ENTREPRISE", "SOURCE", "INFOS_BREVES"],
            "expected_output": "Tableau de classification + synthèse par catégorie",
            "tools": ["ChatGPT"],
        },
    ],

    # ──── EXERCICE PRATIQUE — Mission terrain chronométrée ──────────────────
    "practical_exercise_fr": {
        "title": "Mission : Score tes 10 derniers leads avec BANT",
        "duration_minutes": 60,
        "tools_required": ["ChatGPT (gratuit)", "Ton CRM ou un tableur"],
        "objective": (
            "Appliquer la méthode BANT IA sur tes vrais leads, mesurer "
            "objectivement le temps gagné, et construire un plan d'action "
            "concret sur 14 jours."
        ),
        "steps": [
            {
                "n": 1,
                "title": "Sélection des leads",
                "description": "Sélectionne tes 10 derniers leads non encore qualifiés.",
            },
            {
                "n": "1.5",
                "title": "Chronométrage baseline (anti-biais)",
                "description": (
                    "Chronomètre ton temps de qualification 'à l'ancienne' sur les "
                    "3 premiers leads (sans IA), puis chronomètre les 7 suivants "
                    "avec le Prompt 1 BANT. → Mesure objective du temps gagné."
                ),
            },
            {
                "n": 2,
                "title": "Préparation du bloc OFFRE",
                "description": (
                    "Prépare une fois pour toutes ton bloc « MON OFFRE » réutilisable "
                    "(description + cible + prix moyen avec devise locale)."
                ),
            },
            {
                "n": 3,
                "title": "Scoring avec BANT IA",
                "description": (
                    "Pour chaque lead : note d'abord ton intuition (X/100), puis "
                    "applique le Prompt 1 BANT, et compare. L'écart révèle tes biais "
                    "de jugement."
                ),
            },
            {
                "n": 4,
                "title": "Reporting structuré",
                "description": (
                    "Reporte score, action recommandée et écart intuition vs IA "
                    "dans le tableau de suivi."
                ),
            },
            {
                "n": "4.5",
                "title": "Enrichissement des fiches",
                "description": (
                    "Pour chaque lead, note si la fiche CRM était complète avant "
                    "(oui/non) et utilise le Prompt 2 (Buying Signals) pour enrichir. "
                    "→ Mesure objective du taux d'enrichissement."
                ),
            },
            {
                "n": 5,
                "title": "Plan d'action 14 jours",
                "description": (
                    "Décide d'un plan d'action sur 14 jours : priorité A → appel 24h, "
                    "B → email, C → nurturing, D → disqualifier."
                ),
            },
        ],
        "success_criteria": [
            "10 leads scorés en moins de 30 minutes total (vs 80-150 min en manuel)",
            "≥ 3 leads avec un écart ≥ 25 points entre intuition et IA",
            "Plan d'action concret défini pour les 10 leads (qui appeler en priorité)",
        ],
        "maghreb_note": (
            "Si tes leads sont en arabe ou en mix arabe/français, traduis les infos "
            "clés en français avant de les coller dans le prompt — ChatGPT donne "
            "d'aussi bons résultats. Pour les leads de salons régionaux (Carthage "
            "Business Angels, GITEX Africa), ajoute la mention « rencontré en "
            "physique » dans le prompt — le scoring sera plus précis."
        ),
    },

    # ──── TABLEAUX COMPARATIFS — Tools, Workflows, KPIs ─────────────────────
    "comparison_tables_fr": {
        "tools": {
            "title": "Outils — Comparatif et alternatives Afrique du Nord",
            "headers": ["Outil", "Pricing", "Usage", "Note Maghreb"],
            "rows": [
                ["ChatGPT", "Gratuit / Plus 20 USD/mois",
                 "Exécution des 3 prompts BANT, signaux, classification",
                 "Free tier suffisant pour démarrer"],
                ["HubSpot CRM", "Free / Starter 18$ / Pro 90$",
                 "Scoring IA + score manuel + workflows",
                 "Carte internationale requise pour Pro"],
                ["Zapier ou n8n", "Gratuit / 20 USD/mois Zapier ou self-hosted n8n",
                 "Orchestration workflow scoring auto",
                 "n8n self-hosted ~5 USD/VPS = quasi-gratuit"],
                ["Apollo / Clearbit", "Apollo Free / 49 USD/mois",
                 "Enrichissement données prospects",
                 "Apollo free tier permet ~50 enrichissements/mois"],
                ["Alternatives Maghreb", "Variable",
                 "Salesforce Einstein, Zoho CRM Zia, Pipedrive",
                 "Zoho CRM accepte cartes locales TN/DZ/MA"],
            ],
        },
        "workflows": {
            "title": "Workflows — 2 niveaux de sophistication",
            "headers": ["Workflow", "Outils", "Setup", "Coût/mois", "Niveau"],
            "rows": [
                ["W1 : HubSpot AI Lead Scoring (no-code)",
                 "HubSpot + ChatGPT", "15-20 min première fois",
                 "0 à 90 USD selon plan HubSpot", "Débutant"],
                ["W2 : Scoring auto via Zapier (low-code)",
                 "HubSpot + Zapier + Apollo + OpenAI API + Slack",
                 "2-4h première fois", "~180-200 USD/mois", "Intermédiaire"],
                ["W2 low-cost Maghreb",
                 "HubSpot + n8n + LinkedIn manuel + ChatGPT manuel + email",
                 "3-5h première fois", "~5 USD/mois (VPS n8n)", "Intermédiaire"],
            ],
        },
        "kpi_targets": {
            "title": "KPIs cibles — Baseline personnalisée → Cible J+14",
            "headers": ["Indicateur", "Niveau temporel", "Baseline (J0)", "Cible"],
            "rows": [
                ["Temps de qualification par lead", "Court terme (J+14)",
                 "À renseigner par l'apprenant", "Réduction de 70 à 85 %"],
                ["Taux d'enrichissement des fiches", "Court terme (J+14)",
                 "À renseigner", "> 80 % des fiches enrichies"],
                ["Taux de conversion lead → opportunité",
                 "Observatoire (J+30/J+60)", "À renseigner",
                 "+25 à +40 % d'amélioration relative"],
            ],
        },
    },

    # ──── SECTION CONTENT — Contenu narratif détaillé ───────────────────────
    "section_content_fr": {
        "use_case_detail": {
            "title": "Le problème business",
            "narrative": (
                "Beaucoup d'équipes commerciales B2B en Afrique du Nord font face "
                "au même problème : un volume important de leads entrants et "
                "sortants, mais une qualification approximative et chronophage."
            ),
            "pain_points": [
                "Taux de conversion lead → opportunité faible (10-15 %)",
                "Aucune méthode formalisée et reproductible",
                "Données prospects souvent incomplètes ou non enrichies",
                "Désalignement entre Marketing (« j'ai généré 50 leads ») et Sales (« 40 sont nuls »)",
                "Forecasting pipeline imprévisible",
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
                 "examples": "Temps de qualification, temps de préparation"},
                {"level": "Moyen terme", "type": "Qualité (data, fiches, notes)",
                 "horizon": "Mesurable J+14",
                 "examples": "Taux d'enrichissement, % appels documentés"},
                {"level": "Long terme", "type": "Impact business (conversion, RDV, close)",
                 "horizon": "Observatoire J+30/J+60",
                 "examples": "Taux de conversion, close rate"},
            ],
        },
        "kpi_measurement_method": {
            "title": "Méthode de collecte des KPIs",
            "milestones": [
                {"when": "J0", "what": "Formulaire de baseline auto-affiché en début de module (obligatoire pour valider le module)"},
                {"when": "J+7", "what": "Rappel par email + notification in-app"},
                {"when": "J+14", "what": "Formulaire de mesure d'impact auto-affiché + rappel"},
                {"when": "J+30", "what": "Rappel facultatif pour le KPI observatoire (taux de conversion)"},
                {"when": "J+60", "what": "Rappel facultatif final + consolidation dashboard"},
            ],
        },
        "tutorials": [
            {"id": "t1", "title": "Active HubSpot AI Lead Scoring",
             "duration_min": 8, "format": "vidéo screencast + checklist téléchargeable"},
            {"id": "t2", "title": "Score tes 10 premiers leads avec ChatGPT et BANT",
             "duration_min": 10, "format": "vidéo screencast + template Excel"},
        ],
    },
}


# Le Module 1 sera complété par les Module 2 et Module 3 dans la suite du fichier
# (cf. partie suivante du seed)


# =============================================================================
# MODULE 2 — Personalized Outreach at Scale
# =============================================================================
MODULE_2 = {
    "title_fr": "Personalized Outreach at Scale",
    "description_fr": (
        "Conçois et déploie des séquences de prospection multi-canal "
        "(email + LinkedIn + WhatsApp) personnalisées par persona avec l'IA. "
        "Tu passeras d'un reply rate de 2-5 % avec emails génériques à un "
        "reply rate 2 à 3× plus élevé grâce à la personnalisation à l'échelle, "
        "tout en intégrant WhatsApp — canal dominant en Afrique du Nord."
    ),
    "level": "Pratique",
    "role": ROLE,
    "journey_stage": "Cycle de vente — Prospection",
    "display_order": 2,
    "estimated_duration_min": 300,  # 3-5h
    "format": "blended",
    "is_active": True,

    "skill_name": "Prospection hyper-personnalisée",

    "learning_objective_fr": (
        "À l'issue de ce module, l'apprenant sait concevoir et déployer des "
        "séquences de prospection multi-canal (email + LinkedIn + WhatsApp) "
        "personnalisées par persona avec l'IA, qui maintiennent la qualité "
        "tout en augmentant les RDV qualifiés."
    ),
    "expected_outcome_fr": (
        "Reply rate multi-canal multiplié par 2 à 3, +50 à +100 % de RDV "
        "qualifiés par semaine, > 50 % des prospects touchés sur au moins "
        "2 canaux (vs 0 % en mono-canal)."
    ),
    "why_this_module_fr": (
        "Les commerciaux B2B en Afrique du Nord rencontrent une difficulté "
        "majeure dans la prospection sortante : envoyer des messages génériques "
        "produit des taux de réponse très bas (autour de 2-5 %), tandis que "
        "la personnalisation manuelle prospect par prospect est trop lente "
        "pour atteindre un volume significatif. Et WhatsApp — canal dominant "
        "au Maghreb — est largement sous-exploité."
    ),
    "recommended_when_fr": (
        "Quand ton reply rate sur cold email est < 10 %, que tu utilises "
        "uniquement l'email comme canal, ou que tu obtiens moins de 3 RDV "
        "qualifiés par semaine pour 50+ prospects contactés."
    ),
    "role_based_example_fr": (
        "Karim, commercial B2B dans une PME tunisienne de services aux "
        "entreprises, veut faire grandir son pipeline. Il identifie 200 "
        "prospects (Directeurs Achats de PME industrielles 50-200 employés "
        "en Tunisie/Algérie/Maroc). Il commence à leur écrire un par un sur "
        "LinkedIn — après 30 messages il abandonne. Il bascule sur des cold "
        "emails copiés-collés, mais le reply rate tombe à 3 %. Avec ce "
        "module, Karim construit 3 séquences segmentées par persona, intègre "
        "WhatsApp pour les prospects clés, et passe de 1-2 RDV/semaine à 4-5."
    ),
    "takeaway_fr": (
        "La personnalisation à l'échelle ne se résume pas au prénom dans "
        "l'objet d'email : c'est une stack qui combine enrichissement, IA "
        "générative, séquencement multi-canal et A/B testing. Le canal "
        "WhatsApp en Afrique du Nord est un avantage compétitif majeur "
        "encore peu exploité."
    ),
    "action_point_fr": (
        "Cette semaine : identifie 30 prospects cibles, segmente-les en 2-3 "
        "personas, génère une séquence multi-canal pour chaque persona avec "
        "le Prompt 2, et lance la campagne avec un A/B test sur 3 variantes "
        "d'objet."
    ),
    "practical_application_fr": (
        "Application directe sur tes propres prospects et secteur. Tu "
        "construis une séquence reproductible pour ton ICP, mesures le reply "
        "rate par variante, et identifies le canal de meilleure conversion."
    ),

    "key_concepts_fr": [
        "Personnalisation à l'échelle vs templates segmentés (différence essentielle)",
        "Génération d'emails personnalisés par persona avec ChatGPT",
        "Construction de séquences multi-touch (email + LinkedIn + WhatsApp)",
        "Segmentation par persona et logique d'A/B test sur l'accroche",
        "Contextualisation par actualité ou signal pertinent du prospect",
        "Mesure reply rate, meeting rate, qualité des réponses",
        "Adaptation au canal et à la langue (WhatsApp + FR/AR/EN selon contexte)",
        "Couverture multi-canal Afrique du Nord (intégration WhatsApp Business)",
    ],

    "next_recommended_module_fr": "Sales Call Preparation",

    # ──── PROMPTS — 3 prompts validés ───────────────────────────────────────
    "prompt_examples_fr": [
        {
            "id": "prompt_1_cold_email",
            "title": "Prompt 1 — Cold email personnalisé",
            "use_case": "Générer un cold email court et personnalisé à partir du profil LinkedIn",
            "tags": ["cold email", "personnalisation", "LinkedIn"],
            "content": (
                "Tu es un copywriter B2B spécialisé en outreach commercial au Maghreb.\n"
                "Génère un cold email court (max 120 mots) pour ce prospect.\n\n"
                "PROSPECT :\n"
                "- Nom : [NOM] | Poste : [POSTE] | Entreprise : [ENTREPRISE]\n"
                "- Secteur : [SECTEUR] | Pays : [PAYS]\n"
                "- Langue préférée : [FR / AR / EN / mix]\n"
                "- Infos LinkedIn copiées (résumé, expérience, posts récents) : "
                "[INFOS_LINKEDIN_COPIEES]\n\n"
                "MON OFFRE :\n"
                "- Je vends : [DESCRIPTION_OFFRE]\n"
                "- Bénéfice principal : [VALUE_PROPOSITION]\n"
                "- Preuve sociale : [CLIENT_REFERENCE]\n\n"
                "CONSIGNE :\n"
                "1. Accroche personnalisée basée sur les infos LinkedIn (1-2 phrases).\n"
                "2. Lien avec mon offre (1 phrase).\n"
                "3. Preuve sociale rapide (1 phrase).\n"
                "4. CTA soft : proposer un call court (1 phrase).\n"
                "5. Signature : nom + poste + entreprise (3 lignes max).\n\n"
                "Adapte la langue à la préférence du prospect. Pour 'mix', utilise un "
                "français professionnel avec 1-2 expressions arabes naturelles si pertinent.\n\n"
                "Génère également :\n"
                "- Un objet d'email (max 8 mots).\n"
                "- Une variante alternative pour A/B test."
            ),
            "variables": ["NOM", "POSTE", "ENTREPRISE", "SECTEUR", "PAYS",
                          "INFOS_LINKEDIN_COPIEES", "DESCRIPTION_OFFRE",
                          "VALUE_PROPOSITION", "CLIENT_REFERENCE"],
            "expected_output": "Cold email + objet + variante A/B test",
            "tools": ["ChatGPT"],
        },
        {
            "id": "prompt_2_multi_touch_sequence",
            "title": "Prompt 2 — Séquence multi-touch par persona",
            "use_case": "Construire une séquence de 4 messages multi-canal pour un persona",
            "tags": ["séquence", "multi-canal", "persona"],
            "content": (
                "Tu es un expert en outreach B2B multi-canal au Maghreb.\n"
                "Construis une séquence de 4 messages pour ce persona.\n\n"
                "PERSONA CIBLE :\n"
                "- Profil (format suggéré : Poste + Type entreprise + Taille) : [NOM_PERSONA]\n"
                "- Pain points typiques : [3_PAIN_POINTS]\n"
                "- Objections fréquentes : [2_OBJECTIONS]\n\n"
                "MON OFFRE :\n"
                "- Description : [DESCRIPTION_OFFRE]\n"
                "- Différenciation : [POINT_DE_DIFFERENCIATION]\n\n"
                "Cadence souhaitée : [STANDARD / SERREE / ESPACEE]\n\n"
                "CONSIGNE — séquence en 4 touches :\n"
                "Touch 1 (Jour 1) : Email d'introduction (max 100 mots)\n"
                "Touch 2 (Jour 4) : Connexion LinkedIn + message court (max 50 mots)\n"
                "Touch 3 (Jour 8) : Email de relance avec valeur (max 80 mots, CTA call 15 min)\n"
                "Touch 4 (Jour 12) : Message WhatsApp (recommandé Maghreb)\n"
                "  - Si le prospect n'a pas répondu après 3 touches\n"
                "  - Message ultra-court (3-4 lignes), ton chaleureux\n"
                "  - Voir Prompt 3 (WhatsApp Maghreb) pour la rédaction"
            ),
            "variables": ["NOM_PERSONA", "3_PAIN_POINTS", "2_OBJECTIONS",
                          "DESCRIPTION_OFFRE", "POINT_DE_DIFFERENCIATION"],
            "expected_output": "Séquence de 4 messages multi-canal sur 12 jours",
            "tools": ["ChatGPT"],
        },
        {
            "id": "prompt_3_whatsapp_maghreb",
            "title": "Prompt 3 — Message WhatsApp Maghreb",
            "use_case": "Adapter un email cold pour le canal WhatsApp avec ton chaleureux régional",
            "tags": ["WhatsApp", "Afrique du Nord", "adaptation canal"],
            "content": (
                "Note : ce prompt s'utilise APRÈS le Prompt 1 (Cold email). "
                "Colle ici l'email généré pour l'adapter à WhatsApp.\n\n"
                "Tu es un expert en outreach B2B au Maghreb. Adapte ce message pour WhatsApp.\n\n"
                "CONTEXTE WHATSAPP MAGHREB :\n"
                "- Style direct mais respectueux\n"
                "- Salutation chaleureuse adaptée à la culture\n"
                "- Court (3-4 lignes max, pas un email déguisé)\n"
                "- Voix humaine, pas marketing\n\n"
                "MESSAGE EMAIL ORIGINAL : [COLLER_EMAIL_GENERE]\n"
                "PROSPECT : Nom, Pays, Langue préférée [FR/AR/EN]\n\n"
                "GÉNÈRE :\n"
                "1. Version WhatsApp : courte, chaleureuse, naturelle.\n"
                "2. Salutation par pays (Pending validation Achref/Oumeima) :\n"
                "   - Tunisie/Algérie : 'Sahha' / 'Bonjour'\n"
                "   - Maroc : 'Salam' / 'Bonjour'\n"
                "   - Égypte/Libye : 'Asalam alaykum' / 'Bonjour'\n"
                "3. Inclus 1 emoji approprié maximum.\n"
                "4. CTA simple, adapté au contexte. Suggestions :\n"
                "   (1) demander un call court\n"
                "   (2) poser une question ouverte\n"
                "   (3) partager une ressource utile"
            ),
            "variables": ["COLLER_EMAIL_GENERE", "NOM", "PAYS", "LANGUE"],
            "expected_output": "Message WhatsApp court (3-4 lignes) avec salutation régionale",
            "tools": ["ChatGPT", "WhatsApp Business app"],
        },
    ],

    "practical_exercise_fr": {
        "title": "Mission : Lance ta première séquence personnalisée multi-canal sur 30 prospects",
        "duration_minutes": 90,
        "tools_required": [
            "ChatGPT",
            "Apollo (free) ou LinkedIn Sales Navigator",
            "Brevo OU Lemlist (essai gratuit)",
            "WhatsApp Business",
        ],
        "objective": (
            "Construire une séquence multi-canal segmentée par persona, "
            "lancer un A/B test, et obtenir au moins 1 RDV qualifié à J+14."
        ),
        "steps": [
            {"n": 1, "title": "Identification des prospects",
             "description": "Identifie 30 prospects cibles via Apollo ou LinkedIn Sales Navigator."},
            {"n": 2, "title": "Segmentation par persona",
             "description": "Segmente-les en 2-3 personas distincts."},
            {"n": 3, "title": "Génération des séquences",
             "description": (
                 "Pour chaque persona, génère une séquence multi-touch couvrant au "
                 "moins 2 canaux (email + LinkedIn ou email + WhatsApp) avec le Prompt 2."
             )},
            {"n": 4, "title": "Lancement multi-canal",
             "description": (
                 "Lance les séquences en t'assurant qu'au moins 50 % des prospects "
                 "sont touchés sur au moins 2 canaux."
             )},
            {"n": "4.5", "title": "Adaptation WhatsApp",
             "description": (
                 "Sur les 30 prospects, sélectionne les 5-10 dont tu as le numéro "
                 "WhatsApp. Adapte le message email avec le Prompt 3 (WhatsApp Maghreb) "
                 "et envoie-le manuellement via WhatsApp Business."
             )},
            {"n": 5, "title": "A/B test sur l'objet",
             "description": "Active un A/B test sur 3 variantes d'objet d'email."},
            {"n": 6, "title": "Mesure des résultats à J+14",
             "description": "Mesure : reply rate, meeting rate, qualité des réponses."},
        ],
        "success_criteria": [
            "Reply rate ≥ 1.5× ta baseline",
            "≥ 50 % des prospects touchés sur au moins 2 canaux",
            "Au moins 1 RDV qualifié obtenu (ou agendé pour J+14)",
        ],
        "maghreb_note": (
            "WhatsApp Business est l'avantage régional clé. La plupart de tes "
            "concurrents l'ignorent encore — c'est ta fenêtre d'opportunité. "
            "Pour les prospects en arabe/français mixte, génère 2 versions du "
            "message et choisis la plus naturelle après lecture."
        ),
    },

    "comparison_tables_fr": {
        "tools": {
            "title": "Outils d'outreach — Comparatif Afrique du Nord",
            "headers": ["Outil", "Pricing", "Usage", "Note Maghreb"],
            "rows": [
                ["ChatGPT", "Gratuit / Plus 20$/mois",
                 "Génération emails et messages multi-canal",
                 "Free tier suffisant pour démarrer"],
                ["Apollo / Sales Nav", "Apollo Free / 49$/mois",
                 "Identification + enrichissement prospects",
                 "Apollo free = 50 enrichissements/mois"],
                ["Lemlist", "À partir de 39$/mois",
                 "Séquences multi-touch + A/B test",
                 "Carte internationale requise"],
                ["Brevo (alternative)", "Free tier",
                 "Cold email + séquences (gratuit jusqu'à 300/jour)",
                 "Accepte cartes locales TN/MA"],
                ["WhatsApp Business", "Gratuit (app) / Twilio API à l'usage",
                 "Canal additionnel essentiel Maghreb",
                 "App mobile gratuite suffit pour <100 prospects/mois"],
                ["PhantomBuster", "À partir de 56$/mois",
                 "Automatisation LinkedIn",
                 "Optionnel pour V1"],
            ],
        },
        "workflows": {
            "title": "Workflows d'outreach — 2 niveaux",
            "headers": ["Workflow", "Outils", "Setup", "Coût/mois", "Niveau"],
            "rows": [
                ["W1 : Cold email manuel assisté ChatGPT",
                 "ChatGPT + Apollo free + Brevo + WhatsApp Business",
                 "30-45 min première fois", "0 USD (free tiers)",
                 "Débutant"],
                ["W2 : Séquence multi-canal automatisée",
                 "Apollo + OpenAI API + Lemlist + PhantomBuster",
                 "2-4h première fois", "~250 USD/mois",
                 "Intermédiaire"],
                ["W2 low-cost Maghreb",
                 "Brevo + n8n + ChatGPT manuel + WhatsApp Business",
                 "3-5h première fois", "~5 USD/mois (VPS n8n)",
                 "Intermédiaire"],
            ],
        },
        "kpi_targets": {
            "title": "KPIs cibles — Outreach personnalisé",
            "headers": ["Indicateur", "Niveau temporel", "Baseline (J0)", "Cible (J+14)"],
            "rows": [
                ["Reply rate moyen multi-canal", "Court terme",
                 "À renseigner", "2 à 3× la baseline"],
                ["Nombre de RDV qualifiés / semaine", "Impact business",
                 "À renseigner", "+50 à +100 %"],
                ["% prospects touchés sur ≥ 2 canaux", "KPI Maghreb",
                 "0 % (mono-canal)", "> 50 %"],
            ],
        },
    },

    "section_content_fr": {
        "use_case_detail": {
            "title": "Le problème business",
            "narrative": (
                "Les commerciaux B2B en Afrique du Nord rencontrent une difficulté "
                "majeure dans la prospection sortante : envoyer des messages génériques "
                "produit des taux de réponse très bas (autour de 2-5 %), tandis que la "
                "personnalisation manuelle prospect par prospect est trop lente pour "
                "atteindre un volume significatif."
            ),
            "pain_points": [
                "Reply rate très bas (5-10 %) avec emails génériques",
                "Personnalisation limitée au prénom et nom de l'entreprise",
                "Aucune segmentation par persona ni A/B testing",
                "Outreach mono-canal (souvent email uniquement)",
                "Faible taux de RDV obtenus (1-2 RDV/semaine pour 50 prospects)",
                "Pas d'utilisation de WhatsApp, pourtant canal dominant en Afrique du Nord",
            ],
        },
        "tutorials": [
            {"id": "t1", "title": "Génère ton premier cold email IA en 5 minutes",
             "duration_min": 10, "format": "vidéo screencast"},
            {"id": "t2", "title": "Configure ta première séquence Lemlist multi-touch (+ alt. Brevo/Apollo)",
             "duration_min": 20, "format": "vidéo screencast + comparatif outils"},
        ],
    },
}


# =============================================================================
# MODULE 3 — Sales Call Preparation
# =============================================================================
MODULE_3 = {
    "title_fr": "Sales Call Preparation",
    "description_fr": (
        "Prépare, exécute et analyse tes appels commerciaux avec l'aide "
        "d'agents IA : briefing pré-call complet en 3 minutes, copilot "
        "temps réel pour la gestion d'objections, transcription automatique "
        "et mise à jour CRM. Tu réduis ton temps de préparation de 70-85 % "
        "et documentes 100 % de tes appels."
    ),
    "level": "Expert",
    "role": ROLE,
    "journey_stage": "Cycle de vente — Closing",
    "display_order": 3,
    "estimated_duration_min": 180,  # 2-4h
    "format": "blended",
    "is_active": True,

    "skill_name": "Conversations commerciales assistées par IA",

    "learning_objective_fr": (
        "À l'issue de ce module, l'apprenant sait préparer, exécuter et "
        "analyser ses appels commerciaux avec l'aide d'agents IA — gagnant "
        "en productivité et en qualité de données dès les premiers appels, "
        "et augmentant son taux de closing sur le moyen terme."
    ),
    "expected_outcome_fr": (
        "Réduction de 70 à 85 % du temps de préparation par appel, > 95 % "
        "des appels documentés dans le CRM, +15 à +25 % d'amélioration "
        "relative du close rate (observatoire J+30/J+60)."
    ),
    "why_this_module_fr": (
        "Les appels commerciaux représentent le moment de vérité du cycle "
        "de vente. Pourtant, beaucoup de commerciaux y arrivent insuffisamment "
        "préparés et exploitent mal leurs appels post-mortem (notes "
        "incomplètes, mise à jour CRM partielle). En Afrique du Nord, la "
        "dimension relationnelle, le multilinguisme et le calendrier culturel "
        "ajoutent une complexité que peu de copilots intègrent nativement."
    ),
    "recommended_when_fr": (
        "Quand tu as 3+ appels commerciaux par jour, que ton temps de "
        "préparation par appel dépasse 15 minutes, ou que moins de 80 % de "
        "tes appels sont correctement documentés dans le CRM."
    ),
    "role_based_example_fr": (
        "Karim a 5 appels prévus aujourd'hui. Avant chaque appel, il consulte "
        "rapidement le profil LinkedIn du prospect (5 min). Pendant l'appel, "
        "quand le prospect émet une objection sur le prix, il improvise. "
        "Après l'appel, il prend des notes au stylo qu'il oubliera de mettre "
        "dans le CRM. Karim arrive souvent à l'appel avec un sentiment "
        "d'impréparation, et redoute particulièrement les objections sur le "
        "prix qu'il sait mal gérer. Avec ce module, Karim génère un briefing "
        "complet en 3 minutes, utilise un copilot pour gérer les objections "
        "en temps réel, et documente 100 % de ses appels automatiquement."
    ),
    "takeaway_fr": (
        "Un agent multi-fonction couvre le cycle complet : briefing pré-call, "
        "transcription temps réel, suggestions d'objection handling, post-call "
        "analysis, deal scoring, mise à jour CRM. Les solutions partielles "
        "(briefing seul, transcription seule) manquent l'aspect critique du "
        "temps réel — c'est là que se gagne ou se perd l'appel."
    ),
    "action_point_fr": (
        "Cette semaine : identifie 5 appels importants, génère leur briefing "
        "avec le Prompt 1, utilise Otter/Fireflies/Notta pour la transcription, "
        "et applique le Prompt 3 pour le résumé post-appel et la mise à jour CRM."
    ),
    "practical_application_fr": (
        "Application directe sur tes vrais appels de la semaine. Tu mesures "
        "ton temps de préparation avant/après et tu construis ta bibliothèque "
        "personnelle d'objection handling à partir de tes appels réels."
    ),

    "key_concepts_fr": [
        "Pre-call briefing assisté par IA (poste, entreprise, actualités, pain points)",
        "Génération d'un briefing complet en 3 minutes",
        "Anticipation et gestion temps réel des objections",
        "Copilots temps réel : Fireflies, Otter, Notta, Gong",
        "Transcription et résumé automatique des appels",
        "Mise à jour CRM automatique avec les insights de l'appel",
        "Mesure de la qualité des appels et identification des axes de progression",
        "Adaptation au contexte Afrique du Nord (langue, dimension relationnelle, calendrier culturel)",
    ],

    "next_recommended_module_fr": "Certificat AI Sales Specialist + Bridge commercial",

    # ──── PROMPTS — 3 prompts validés ───────────────────────────────────────
    "prompt_examples_fr": [
        {
            "id": "prompt_1_pre_call_briefing",
            "title": "Prompt 1 — Pre-call briefing complet",
            "use_case": "Générer une fiche de préparation 8 sections en 3 minutes avant un RDV",
            "tags": ["briefing", "préparation", "pré-call"],
            "content": (
                "Tu es un sales engineer B2B expérimenté au Maghreb. Génère un "
                "briefing pré-call complet pour ce rendez-vous commercial.\n\n"
                "PROSPECT :\n"
                "- Nom : [NOM] | Poste : [POSTE] | Entreprise : [ENTREPRISE]\n"
                "- Secteur : [SECTEUR] | Effectif : [EFFECTIF] | Pays : [PAYS]\n"
                "- Infos LinkedIn copiées : [INFOS_LINKEDIN_COPIEES]\n\n"
                "CONTEXTE :\n"
                "- Source du lead : [SOURCE]\n"
                "- Échanges précédents : [HISTORIQUE_BREF]\n"
                "- Objectif de mon appel : [OBJECTIF]\n"
                "- Langue prévue de l'appel : [FR / AR-FR mix / EN]\n\n"
                "MON OFFRE : [DESCRIPTION_OFFRE]\n\n"
                "GÉNÈRE UN BRIEFING STRUCTURÉ :\n"
                "1. RÉSUMÉ EXÉCUTIF (3 lignes)\n"
                "2. OBJECTIFS DE L'APPEL (3 max)\n"
                "3. 5 QUESTIONS À POSER (du plus ouvert au plus précis)\n"
                "4. 3 OBJECTIONS PROBABLES (avec réponse préparée)\n"
                "5. ANGLE D'ACCROCHE\n"
                "6. SIGNAUX D'ACHAT À DÉTECTER\n"
                "7. NEXT STEPS POSSIBLES (3 scénarios : positif / mitigé / négatif)\n"
                "8. CONTEXTE RELATIONNEL MAGHREB\n"
                "   - Connaissance commune potentielle (LinkedIn mutual connections)\n"
                "   - Parcours commun à explorer (école, université, ville)\n"
                "   - Référence régionale qu'on peut citer (client commun, entreprise locale)\n\n"
                "Adapte les questions et l'angle d'accroche à la langue de l'appel."
            ),
            "variables": ["NOM", "POSTE", "ENTREPRISE", "SECTEUR", "EFFECTIF", "PAYS",
                          "INFOS_LINKEDIN_COPIEES", "SOURCE", "HISTORIQUE_BREF",
                          "OBJECTIF", "DESCRIPTION_OFFRE"],
            "expected_output": "Briefing 8 sections (résumé, objectifs, questions, objections, angle, signaux, next steps, relationnel)",
            "tools": ["ChatGPT"],
        },
        {
            "id": "prompt_2_objection_library",
            "title": "Prompt 2 — Bibliothèque d'objection handling",
            "use_case": "Construire une bibliothèque réutilisable d'objections et réponses préparées",
            "tags": ["objections", "bibliothèque", "préparation"],
            "content": (
                "Tu es un coach commercial B2B au Maghreb.\n"
                "Construis une bibliothèque d'objection handling pour mon offre.\n\n"
                "MON OFFRE :\n"
                "- Description : [DESCRIPTION_OFFRE]\n"
                "- Prix moyen avec devise (TND/MAD/DZD/EUR/USD) : [PRIX_MOYEN]\n"
                "- Cible : [CIBLE]\n"
                "- Différenciation : [DIFFERENCIATION]\n\n"
                "LISTE DE 3 À 10 OBJECTIONS COURANTES DANS TON SECTEUR :\n"
                "1. [OBJECTION_1] (ex : 'C'est trop cher')\n"
                "2. [OBJECTION_2] (ex : 'On a déjà un fournisseur')\n"
                "3-10. ...\n\n"
                "NOTE MAGHREB : si tes objections incluent des dimensions "
                "relationnelles ('je dois en parler à mon associé', 'vous êtes "
                "recommandé par qui ?') ou de calendrier culturel ('après le "
                "Ramadan'), précise-le pour des réponses adaptées au contexte régional.\n\n"
                "POUR CHAQUE OBJECTION, GÉNÈRE :\n"
                "1. Reformulation empathique\n"
                "2. Question d'approfondissement\n"
                "3. Réponse argumentée (preuve sociale + différenciation + ROI)\n"
                "4. Phrase de re-engagement"
            ),
            "variables": ["DESCRIPTION_OFFRE", "PRIX_MOYEN", "CIBLE", "DIFFERENCIATION",
                          "OBJECTION_1", "OBJECTION_2"],
            "expected_output": "Bibliothèque de 3-10 objections avec réponse en 4 étapes",
            "tools": ["ChatGPT"],
        },
        {
            "id": "prompt_3_post_call_analysis",
            "title": "Prompt 3 — Résumé post-appel et next steps",
            "use_case": "Analyser une transcription d'appel et générer un rapport structuré + suivi",
            "tags": ["post-call", "analyse", "CRM"],
            "content": (
                "Tu es un sales operations manager au Maghreb. Analyse cette transcription d'appel.\n\n"
                "TRANSCRIPTION : [COLLER_LA_TRANSCRIPTION_OTTER_FIREFLIES_NOTTA]\n"
                "CONTEXTE : Prospect, Date, Durée appel\n\n"
                "NOTE : si la transcription contient des passages incompréhensibles "
                "ou en arabe non transcrit (marqués [inaudible] ou [arabe]), "
                "travaille uniquement avec les portions claires et précise dans le "
                "rapport ce qui n'a pas pu être analysé.\n\n"
                "GÉNÈRE UN RAPPORT STRUCTURÉ :\n"
                "1. SCORE DEAL HEALTH (0-100) basé sur la grille v2.0 :\n"
                "   - Engagement émotionnel du prospect (0-25)\n"
                "   - Clarté du besoin exprimé (0-25)\n"
                "   - Présence d'un budget évoqué (0-25)\n"
                "   - Champion interne identifié + decision process clair (0-25)\n"
                "2. PAIN POINTS IDENTIFIÉS (max 3)\n"
                "3. CHAMPION INTERNE\n"
                "4. DECISION PROCESS\n"
                "5. OBJECTIONS NON RÉSOLUES\n"
                "6. ACTIONS NEXT STEPS (numérotées avec délai)\n"
                "7. MISE À JOUR CRM\n"
                "8. SUIVI SUGGÉRÉ\n"
                "   - Canal recommandé : email / WhatsApp / LinkedIn (selon préférence évoquée)\n"
                "   - Brouillon de message (max 100 mots, adapté au canal)"
            ),
            "variables": ["COLLER_LA_TRANSCRIPTION_OTTER_FIREFLIES_NOTTA"],
            "expected_output": "Rapport 8 sections avec deal health, pain points, next steps, CRM update, suivi",
            "tools": ["ChatGPT", "Otter / Fireflies / Notta (pour la transcription)"],
        },
    ],

    "practical_exercise_fr": {
        "title": "Mission : Applique le briefing IA + transcription sur 5 appels cette semaine",
        "duration_minutes": 60,
        "tools_required": [
            "ChatGPT",
            "Otter.ai OU Fireflies OU Notta.ai (pour FR)",
            "Ton CRM",
        ],
        "objective": (
            "Tester sur 5 appels réels la chaîne complète briefing → "
            "transcription → post-call summary, et mesurer le temps gagné."
        ),
        "steps": [
            {"n": 1, "title": "Sélection des appels",
             "description": "Identifie 5 appels prévus dans ta semaine (priorise les plus importants)."},
            {"n": 2, "title": "Briefing pré-call",
             "description": "24h avant chaque appel : génère un briefing avec le Prompt 1."},
            {"n": "2.5", "title": "Contexte relationnel Maghreb",
             "description": (
                 "Avant de générer le briefing, ajoute dans le Prompt 1 une section "
                 "'Contexte relationnel' Maghreb (connaissance commune, parcours "
                 "commun, référence régionale)."
             )},
            {"n": 3, "title": "Chronométrage du gain",
             "description": (
                 "Chronomètre ton temps de préparation et compare aux ~20 min en manuel."
             )},
            {"n": 4, "title": "Transcription temps réel",
             "description": "Pendant l'appel : active Otter / Fireflies / Notta pour la transcription."},
            {"n": 5, "title": "Résumé post-appel",
             "description": "Après chaque appel : génère le résumé avec le Prompt 3."},
            {"n": 6, "title": "Mise à jour CRM",
             "description": "Mets à jour le CRM avec les next steps identifiés."},
            {"n": 7, "title": "Bilan en 3 lignes",
             "description": (
                 "Combien d'appels documentés avant/après ? Quel insight aurais-je "
                 "manqué sans la transcription ?"
             )},
        ],
        "success_criteria": [
            "5 appels documentés à 100 % dans le CRM",
            "Temps de préparation moyen ≤ 10 min/appel (vs ~20 min en manuel)",
            "Au moins 2 next steps précis identifiés par appel",
        ],
        "maghreb_note": (
            "Otter et Fireflies sont optimisés pour l'anglais. Pour des appels "
            "en pur français, considère Notta.ai (free 120 min/mois). Pour des "
            "appels mêlant arabe/français/dialecte, accepte que la transcription "
            "sera imparfaite — concentre-toi sur le post-call summary à partir "
            "de tes notes manuelles."
        ),
    },

    "comparison_tables_fr": {
        "tools": {
            "title": "Outils de Sales Call — Comparatif Afrique du Nord",
            "headers": ["Outil", "Pricing", "Usage", "Note Maghreb"],
            "rows": [
                ["ChatGPT", "Gratuit / Plus 20$/mois",
                 "Briefing, objection handling, post-appel",
                 "Free tier suffit pour démarrer"],
                ["Otter.ai", "Gratuit (300 min/mois) / 17$/mois",
                 "Transcription EN principalement",
                 "Limité sur le français Maghreb"],
                ["Fireflies", "Free / 18$/mois",
                 "Copilot temps réel + résumé auto",
                 "Carte internationale requise pour Pro"],
                ["Notta.ai", "Free tier 120 min/mois",
                 "Meilleur sur le français Maghreb",
                 "Recommandé pour appels FR"],
                ["Microsoft Teams / Google Meet",
                 "Souvent inclus dans suites pro",
                 "Transcription native FR",
                 "Si déjà dans la stack, l'utiliser en priorité"],
                ["WhisperAI", "Gratuit (open source) ou via API",
                 "Excellent multilingue, manipulation requise",
                 "Pour profils techniques uniquement"],
                ["HubSpot / Salesforce", "Variable",
                 "Stockage notes, deal stages, historique",
                 "Cohérent avec Module 1 (scoring)"],
            ],
        },
        "workflows": {
            "title": "Workflows de Sales Call — 2 niveaux",
            "headers": ["Workflow", "Outils", "Setup", "Coût/mois", "Niveau"],
            "rows": [
                ["W1 : Préparation manuelle assistée IA (no-code)",
                 "ChatGPT + LinkedIn + CRM + Otter/Notta",
                 "20-30 min première fois",
                 "0-17 USD/mois",
                 "Débutant"],
                ["W2 : Briefing automatique 24h avant l'appel (low-code)",
                 "Google Calendar + HubSpot API + OpenAI API + Gmail + Fireflies/Notta",
                 "2-3h première fois",
                 "~10-30 USD/mois (OpenAI selon volume)",
                 "Intermédiaire"],
            ],
        },
        "kpi_targets": {
            "title": "KPIs cibles — Sales Call",
            "headers": ["Indicateur", "Niveau temporel", "Baseline (J0)", "Cible"],
            "rows": [
                ["Temps de préparation par appel", "Court terme (J+14)",
                 "À renseigner", "Réduction de 70 à 85 %"],
                ["% appels documentés dans le CRM", "Court terme (J+14)",
                 "À renseigner", "> 95 %"],
                ["Close rate des opportunités", "Observatoire (J+30/J+60)",
                 "À renseigner", "+15 à +25 % d'amélioration relative"],
            ],
        },
    },

    "section_content_fr": {
        "use_case_detail": {
            "title": "Le problème business",
            "narrative": (
                "Les appels commerciaux représentent le moment de vérité du cycle "
                "de vente. Pourtant, beaucoup de commerciaux y arrivent insuffisamment "
                "préparés et exploitent mal leurs appels post-mortem (notes "
                "incomplètes, mise à jour CRM partielle)."
            ),
            "pain_points": [
                "Préparation rapide (5 min) basée uniquement sur LinkedIn",
                "Improvisation face aux objections sur le prix",
                "Notes papier oubliées, CRM non mis à jour",
                "Sentiment d'impréparation et stress avant les appels critiques",
                "Multilinguisme FR/AR/EN mal géré",
                "Calendrier culturel (Ramadan, fêtes, weekends différents) non intégré",
            ],
            "maghreb_specifics": [
                "Multilinguisme (français/arabe/anglais selon l'interlocuteur)",
                "Importance des relations personnelles (références, parcours commun, recommandations)",
                "Calendrier culturel (Ramadan, fêtes, weekends différents selon les pays)",
            ],
        },
        "tutorials": [
            {"id": "t1", "title": "Génère ton premier briefing pré-call en 3 minutes",
             "duration_min": 10, "format": "vidéo screencast"},
            {"id": "t2", "title": "Configure Fireflies + workflow post-appel automatique (+ alt. Notta.ai pour FR)",
             "duration_min": 15, "format": "vidéo screencast + comparatif"},
        ],
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

    Source : PDF v2.0 — Validation 8 mai 2026.

    Idempotent : skip si déjà seedé (vérifie l'existence d'un module
    avec role='AI Sales Specialist' avant de continuer).

    Pré-requis : seed_ai_sales_specialist_diagnostic.py doit avoir été
    exécuté avant (il crée les 3 skills 'Qualification IA des leads',
    'Prospection hyper-personnalisée', 'Conversations commerciales
    assistées par IA' référencées par skill_name dans MODULE_*).
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
            f"⚠️  AI Sales Specialist modules déjà seedés "
            f"({existing_modules} modules pour role='{ROLE}'), skip."
        )
        return

    # =========================================================================
    # 1. Récupérer les skills (seedées par seed_ai_sales_specialist_diagnostic.py)
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
                f"Lance d'abord seed_ai_sales_specialist_diagnostic.py."
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
        f"✅ AI Sales Specialist modules seedés :\n"
        f"   • {len(MODULES)} modules (role='{ROLE}')\n"
        f"   • {total_units_created} units (5 par module)\n"
        f"   • {total_lessons_created} lessons (~3 par unit)\n"
        f"   • {total_module_skill_links} jointures module_skills"
    )