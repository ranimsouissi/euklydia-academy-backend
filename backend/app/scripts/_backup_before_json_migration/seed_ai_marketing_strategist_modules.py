"""
Seed AI Marketing Strategist — Modules pédagogiques v2.0

Contenu pédagogique des 3 modules du parcours AI Marketing Strategist :
- Module 1 : Content Strategy Optimization
- Module 2 : Campaign Performance Optimization
- Module 3 : Audience Insights & Segmentation

Source : PDF "Parcours AI Marketing Strategist v1.0" — Avril 2026.
Aligné sur le pattern de seed_ai_sales_specialist_modules.py
(neutralisation des produits Euklydia, contextualisation Afrique du Nord,
3 personas régionaux distincts : Sarah/Yacine/Lina).

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

Idempotent : skip si déjà seedé (pattern aligné sur seed_ai_marketing_strategist_diagnostic.py).
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
ROLE = "AI Marketing Strategist"
CAREER_PATH_ID = 80  # cohérent avec seed_ai_marketing_strategist_diagnostic.py


# =============================================================================
# MODULE 1 — Content Strategy Optimization
# =============================================================================
MODULE_1 = {
    # ──── Identité du module ──────────────────────────────────────────────────
    "title_fr": "Content Strategy Optimization",
    "description_fr": (
        "Apprends à construire une stratégie de contenu IA-augmentée en Afrique "
        "du Nord : encode ta brand voice, structure un calendrier éditorial "
        "trimestriel, génère du contenu cohérent multi-canal (blog, LinkedIn, "
        "newsletter) et industrialise ton repurposing. Tu passeras d'une "
        "production réactive et chronophage (1-2h par contenu) à un pipeline "
        "structuré (15-25 min par contenu) avec un engagement mesurablement "
        "supérieur."
    ),
    "level": "Fondation",
    "role": ROLE,
    "journey_stage": "Funnel marketing — Stratégie éditoriale",
    "display_order": 1,
    "estimated_duration_min": 240,  # 3-4h
    "format": "blended",
    "is_active": True,

    "skill_name": "Stratégie et création de contenu IA",  # mapping vers skill_id

    # ──── Pédagogie ──────────────────────────────────────────────────────────
    "learning_objective_fr": (
        "À l'issue de ce module, l'apprenant sait (1) encoder une brand voice "
        "dans des prompts IA réutilisables, et (2) industrialiser sa production "
        "éditoriale multi-canal avec un calendrier trimestriel auto-piloté."
    ),
    "expected_outcome_fr": (
        "Réduction de 70 à 80 % du temps de production par contenu, "
        "+30 à +50 % d'amélioration relative du taux d'engagement "
        "(observatoire J+30/J+60), volume de publications multiplié par 3 à 5."
    ),
    "why_this_module_fr": (
        "Beaucoup d'équipes marketing B2B/B2C en Afrique du Nord produisent "
        "du contenu sans stratégie claire : posts isolés sur les réseaux, "
        "blog mis à jour sporadiquement, newsletter irrégulière. Le contenu "
        "existe mais il n'engage pas, ne génère pas de leads et ne construit "
        "pas de marque forte. La cause principale : pas de ligne éditoriale, "
        "pas de calendrier, pas de processus reproductible."
    ),
    "recommended_when_fr": (
        "Quand ton taux d'engagement moyen est < 2 %, que tu publies moins "
        "de 8 contenus/mois, ou que tu passes plus d'1h en moyenne à produire "
        "chaque contenu manuellement."
    ),
    "role_based_example_fr": (
        "Sarah, content manager dans une agence digitale à Casablanca, gère "
        "le contenu de 5 clients en parallèle. Le lundi matin, elle improvise : "
        "« qu'est-ce qu'on poste cette semaine ? ». Elle ouvre LinkedIn, "
        "regarde ce que font les concurrents, sort une idée, rédige un post "
        "en 15 minutes. Parfois ça marche, souvent ça tombe à plat. Sarah "
        "ressent un burn-out créatif récurrent (« je n'ai plus d'idées ») et "
        "son engagement moyen plafonne à 1.8 %. Avec ce module, Sarah encode "
        "la brand voice de ses 5 clients, construit un calendrier trimestriel "
        "avec saisonnalités régionales (Ramadan, rentrée scolaire, fêtes "
        "nationales), et passe de 4-6 contenus/semaine à 20-25 — avec un "
        "engagement moyen de 3.2 %."
    ),
    "takeaway_fr": (
        "Une brand voice bien encodée dans un prompt master réutilisable "
        "transforme la production de contenu d'une activité créative épisodique "
        "en un pipeline industriel cohérent. Le calendrier éditorial trimestriel "
        "n'est pas une contrainte : c'est ce qui libère la créativité en "
        "supprimant la décision quotidienne « qu'est-ce que je poste ? »."
    ),
    "action_point_fr": (
        "Cette semaine : sélectionne 3 contenus performants de ta marque, "
        "applique le Prompt 1 (Brand Voice) pour encoder ton profil éditorial, "
        "puis applique le Prompt 2 (Calendrier) sur le mois à venir avec "
        "1 saisonnalité régionale intégrée."
    ),
    "practical_application_fr": (
        "Application directe sur ta propre marque ou celle d'un client : pas "
        "de cas fictif. Tu construis ta bibliothèque de prompts personnelle, "
        "tu mesures le temps gagné, et tu publies au moins 2 contenus "
        "IA-augmentés sur tes vrais canaux dans la semaine."
    ),

    # ──── Compétences clés (8 axes) ──────────────────────────────────────────
    "key_concepts_fr": [
        "Définition et encodage d'une brand voice (ton, vocabulaire, style, do/don't)",
        "Prompts ChatGPT structurés par persona et thème éditorial",
        "Calendrier éditorial trimestriel avec saisonnalités régionales",
        "Repurposing multi-canal (blog → LinkedIn → newsletter → social)",
        "Mesure d'engagement par format, sujet et canal",
        "Bibliothèque de prompts versionnée et réutilisable",
        "Pipeline de production semi-automatisé (Notion AI / Make / ChatGPT)",
        "Adaptation bilingue (FR/AR) et culturelle Afrique du Nord",
    ],

    # ──── Module suivant ─────────────────────────────────────────────────────
    "next_recommended_module_fr": "Campaign Performance Optimization",

    # =========================================================================
    # JSON — Contenu pédagogique riche
    # =========================================================================

    # ──── PROMPTS — 3 prompts ChatGPT validés ───────────────────────────────
    "prompt_examples_fr": [
        {
            "id": "prompt_1_brand_voice_encoding",
            "title": "Prompt 1 — Brand Voice Encoding",
            "use_case": "Encoder la voix de marque dans un prompt master réutilisable pour toute génération IA",
            "tags": ["brand voice", "encoding", "prompt master"],
            "content": (
                "Tu es un content strategist senior B2B/B2C au Maghreb.\n"
                "Aide-moi à encoder la voix de ma marque pour un usage IA récurrent.\n\n"
                "MA MARQUE :\n"
                "- Nom : [NOM_MARQUE]\n"
                "- Secteur : [SECTEUR]\n"
                "- Cible principale : [PERSONA_PRINCIPAL]\n"
                "- Promesse de marque : [PROMESSE]\n"
                "- 3 valeurs : [VALEURS]\n"
                "- Concurrents : [CONCURRENTS]\n"
                "- Pays cibles : [PAYS_MAGHREB]\n"
                "- Langue dominante : [FR / AR / FR+AR mix]\n\n"
                "ÉCHANTILLON ÉDITORIAL :\n"
                "- 3 contenus performants : [COLLER_3_POSTS_OU_ARTICLES]\n"
                "- Niveau d'engagement de référence : [LIKES / COMMENTS / SHARES]\n\n"
                "CONSIGNE :\n"
                "GÉNÈRE :\n"
                "1. PROFIL ÉDITORIAL (3 paragraphes)\n"
                "   Ton, style, vocabulaire, longueur, structure\n"
                "2. 5 RÈGLES À RESPECTER (do)\n"
                "3. 5 RÈGLES À ÉVITER (don't)\n"
                "4. PROMPT MASTER RÉUTILISABLE\n"
                "   À utiliser comme préambule pour toute génération future\n"
                "5. TEST DE COHÉRENCE\n"
                "   Génère 3 phrases d'exemple selon ce profil"
            ),
            "variables": ["NOM_MARQUE", "SECTEUR", "PERSONA_PRINCIPAL", "PROMESSE",
                          "VALEURS", "CONCURRENTS", "PAYS_MAGHREB",
                          "COLLER_3_POSTS_OU_ARTICLES"],
            "expected_output": "Profil éditorial + do/don't + prompt master réutilisable + test de cohérence",
            "tools": ["ChatGPT (gratuit ou Plus)", "Claude"],
        },
        {
            "id": "prompt_2_editorial_calendar",
            "title": "Prompt 2 — Calendrier éditorial trimestriel",
            "use_case": "Construire un calendrier éditorial 3 mois multi-canal aligné sur les saisonnalités Maghreb",
            "tags": ["calendrier", "éditorial", "saisonnalités"],
            "content": (
                "Tu es un content strategist B2B/B2C au Maghreb.\n"
                "Construis un calendrier éditorial sur 3 mois aligné sur :\n\n"
                "- Brand voice : [COLLER_PROFIL_EDITORIAL]\n"
                "- Persona principal : [PERSONA]\n"
                "- Objectif business : [OBJECTIF]\n"
                "  (ex : générer 50 leads / mois, +20% trafic blog, +500 abonnés newsletter)\n"
                "- Canaux : [LINKEDIN / BLOG / NEWSLETTER / INSTAGRAM / TIKTOK]\n"
                "- Saisonnalité Maghreb à intégrer (Pending validation Achref/Oumeima) :\n"
                "  [Ramadan / Aïd / rentrée scolaire / fêtes nationales / soldes]\n\n"
                "CONTRAINTES :\n"
                "- 3 piliers thématiques maximum\n"
                "- Mix 70 % éducatif / 20 % inspirationnel / 10 % commercial\n"
                "- Cohérence entre canaux (un sujet décliné sur plusieurs formats)\n\n"
                "FORMAT DE SORTIE :\n"
                "Tableau Semaine | Pilier | Sujet | Canal | Format | Persona | CTA\n"
                "12 lignes pour les 12 semaines.\n\n"
                "EN BAS, AJOUTE :\n"
                "- Synthèse des 3 piliers\n"
                "- 5 idées de campagnes spéciales saisonnières\n"
                "- Recommandation de fréquence par canal"
            ),
            "variables": ["COLLER_PROFIL_EDITORIAL", "PERSONA", "OBJECTIF",
                          "LINKEDIN_BLOG_NEWSLETTER", "SAISONNALITES"],
            "expected_output": "Calendrier 12 semaines + synthèse piliers + campagnes saisonnières + fréquence par canal",
            "tools": ["ChatGPT", "Notion / Airtable (pour stockage)"],
        },
        {
            "id": "prompt_3_repurposing",
            "title": "Prompt 3 — Repurposing multi-canal",
            "use_case": "Transformer 1 contenu source en 5 formats adaptés à chaque canal pour démultiplier la portée",
            "tags": ["repurposing", "multi-canal", "adaptation"],
            "content": (
                "Tu es un content strategist multi-canal au Maghreb.\n"
                "Transforme ce contenu source en 5 formats adaptés.\n\n"
                "CONTENU SOURCE :\n"
                "- Format : [ARTICLE / VIDÉO / PODCAST / WEBINAR]\n"
                "- Texte : [COLLER_LE_CONTENU_INTEGRAL]\n"
                "- Public cible : [PERSONA]\n"
                "- Brand voice : [COLLER_PROFIL_EDITORIAL]\n"
                "- Langue préférée : [FR / AR / FR+AR mix]\n\n"
                "GÉNÈRE 5 ADAPTATIONS :\n"
                "1. POST LINKEDIN (200-300 mots, hook + insight + CTA)\n"
                "2. CARROUSEL LINKEDIN (8 slides, titres courts + body 30 mots)\n"
                "3. THREAD TWITTER/X (8-10 tweets de 250 caractères max)\n"
                "4. NEWSLETTER (objet + intro + 3 sections + CTA, 400 mots)\n"
                "5. SCRIPT REEL/TIKTOK (60 secondes, hook 3s + 5 plans + CTA)\n\n"
                "POUR CHAQUE ADAPTATION :\n"
                "- Garde le message clé\n"
                "- Adapte le ton au canal\n"
                "- Propose un visuel/B-roll\n"
                "- Si la langue préférée est FR+AR mix, intègre 1-2 expressions "
                "arabes naturelles si pertinent (ex : 'Bissaha', 'Inchallah')"
            ),
            "variables": ["FORMAT_SOURCE", "COLLER_LE_CONTENU_INTEGRAL", "PERSONA",
                          "COLLER_PROFIL_EDITORIAL", "LANGUE"],
            "expected_output": "5 adaptations multi-canal avec visuels suggérés",
            "tools": ["ChatGPT", "Canva AI / Midjourney (pour les visuels)"],
        },
    ],

    # ──── EXERCICE PRATIQUE — Mission terrain chronométrée ──────────────────
    "practical_exercise_fr": {
        "title": "Mission : Bâtis ton brand voice + calendrier éditorial du mois",
        "duration_minutes": 90,
        "tools_required": ["ChatGPT (gratuit)", "Notion ou Airtable"],
        "objective": (
            "Encoder ta brand voice dans un prompt master, construire un "
            "calendrier éditorial du mois avec saisonnalités régionales, et "
            "publier au moins 2 contenus IA-augmentés sur tes vrais canaux."
        ),
        "steps": [
            {
                "n": 1,
                "title": "Sélection des contenus de référence",
                "description": (
                    "Sélectionne 3 contenus performants de ta marque (ceux avec "
                    "le plus de likes, commentaires ou conversions). Note leur "
                    "engagement de référence."
                ),
            },
            {
                "n": "1.5",
                "title": "Chronométrage baseline (anti-biais)",
                "description": (
                    "Avant d'utiliser l'IA, chronomètre ton temps de production "
                    "habituel sur 1 contenu (sans IA). Tu compareras ce temps "
                    "à ta production IA-augmentée à l'étape 5."
                ),
            },
            {
                "n": 2,
                "title": "Encodage de la brand voice",
                "description": (
                    "Applique le Prompt 1 (Brand Voice) et sauvegarde le profil "
                    "éditorial + le prompt master dans Notion. Garde-les "
                    "réutilisables pour toutes tes futures générations."
                ),
            },
            {
                "n": 3,
                "title": "Construction du calendrier",
                "description": (
                    "Applique le Prompt 2 (Calendrier) sur le mois à venir avec "
                    "au moins 1 saisonnalité Maghreb intégrée (Ramadan, rentrée, "
                    "fête nationale, soldes)."
                ),
            },
            {
                "n": 4,
                "title": "Repurposing multi-canal",
                "description": (
                    "Génère 3 contenus avec le Prompt 3 (Repurposing) sur "
                    "1 sujet source unique. Décline-les sur 3 canaux différents "
                    "(ex : LinkedIn + newsletter + Reel)."
                ),
            },
            {
                "n": 5,
                "title": "Publication réelle",
                "description": (
                    "Publie au moins 2 contenus IA-augmentés sur tes vrais canaux "
                    "dans la semaine. Mesure le temps de production et compare "
                    "à ta baseline étape 1.5."
                ),
            },
            {
                "n": 6,
                "title": "Mesure d'engagement à J+7",
                "description": (
                    "Note l'engagement de tes 2+ contenus IA-augmentés (likes, "
                    "comments, shares) et compare à ta moyenne habituelle."
                ),
            },
        ],
        "success_criteria": [
            "Brand voice encodée dans un prompt master réutilisable",
            "Calendrier éditorial du mois bâti avec ≥ 1 saisonnalité régionale",
            "≥ 2 contenus IA-augmentés publiés et au moins 1 dépasse ta moyenne d'engagement habituelle",
        ],
        "maghreb_note": (
            "Pour les marques B2C ciblant un public arabophone, génère le "
            "contenu en français puis demande à ChatGPT de proposer une version "
            "arabe ou darija — l'output est de qualité acceptable pour les "
            "marques mainstream. Pour les marques de luxe ou très formelles, "
            "fais retravailler par un copywriter natif. Les saisonnalités "
            "Ramadan et Aïd sont les plus puissantes en termes d'engagement : "
            "prépare ton calendrier 4 semaines avant."
        ),
    },

    # ──── TABLEAUX COMPARATIFS — Tools, Workflows, KPIs ─────────────────────
    "comparison_tables_fr": {
        "tools": {
            "title": "Outils — Comparatif et alternatives Afrique du Nord",
            "headers": ["Outil", "Pricing", "Usage", "Note Maghreb"],
            "rows": [
                ["ChatGPT / Claude", "Gratuit / Plus 20 USD/mois",
                 "Génération des 3 prompts (brand voice, calendrier, repurposing)",
                 "Free tier suffisant pour démarrer"],
                ["Notion AI", "10 USD/utilisateur/mois",
                 "Calendrier éditorial + bibliothèque de prompts",
                 "Carte internationale requise"],
                ["Canva AI", "Free / Pro 12 USD/mois",
                 "Visuels accompagnant chaque contenu",
                 "Free tier généreux, accepte cartes locales"],
                ["Midjourney", "10-30 USD/mois",
                 "Visuels à fort impact pour campagnes premium",
                 "Carte internationale requise"],
                ["Buffer / Hootsuite", "Free / 15-99 USD/mois",
                 "Programmation multi-canal des publications",
                 "Buffer free tier = 3 canaux gratuits"],
                ["Make / Zapier", "Free / 20 USD/mois",
                 "Automatisation du pipeline content engine",
                 "n8n self-hosted ~5 USD/VPS = quasi-gratuit"],
                ["Alternatives Maghreb", "Variable",
                 "Airtable + ChatGPT manuel + Canva (stack low-cost)",
                 "Airtable free tier = 1200 records/base"],
            ],
        },
        "workflows": {
            "title": "Workflows — 2 niveaux de sophistication",
            "headers": ["Workflow", "Outils", "Setup", "Coût/mois", "Niveau"],
            "rows": [
                ["W1 : Production hebdo assistée IA (no-code)",
                 "Notion/Airtable + ChatGPT + Canva AI + Buffer",
                 "30-45 min première fois",
                 "0 USD (free tiers) à 22 USD/mois",
                 "Débutant"],
                ["W2 : Pipeline content engine automatisé (low-code)",
                 "Airtable + OpenAI API + Canva API + Slack + Make",
                 "3-5h première fois",
                 "~50-80 USD/mois (selon volume OpenAI)",
                 "Intermédiaire"],
                ["W2 low-cost Maghreb",
                 "Airtable + n8n self-hosted + ChatGPT manuel + Canva",
                 "4-6h première fois",
                 "~5 USD/mois (VPS n8n)",
                 "Intermédiaire"],
            ],
        },
        "kpi_targets": {
            "title": "KPIs cibles — Baseline personnalisée → Cible J+14",
            "headers": ["Indicateur", "Niveau temporel", "Baseline (J0)", "Cible"],
            "rows": [
                ["Temps de production par contenu", "Court terme (J+14)",
                 "À renseigner par l'apprenant",
                 "Réduction de 70 à 80 %"],
                ["Volume de publications par mois", "Court terme (J+14)",
                 "À renseigner",
                 "Multiplié par 3 à 5"],
                ["Taux d'engagement moyen",
                 "Observatoire (J+30/J+60)",
                 "À renseigner",
                 "+30 à +50 % d'amélioration relative"],
            ],
        },
    },

    # ──── SECTION CONTENT — Contenu narratif détaillé ───────────────────────
    "section_content_fr": {
        "use_case_detail": {
            "title": "Le problème business",
            "narrative": (
                "Beaucoup d'équipes marketing B2B/B2C en Afrique du Nord "
                "produisent du contenu sans stratégie claire : posts isolés "
                "sur les réseaux, blog mis à jour sporadiquement, newsletter "
                "irrégulière. Le contenu existe mais il n'engage pas, ne "
                "génère pas de leads et ne construit pas de marque forte."
            ),
            "pain_points": [
                "Engagement faible (taux d'interaction < 2 %)",
                "Aucun fil narratif cohérent autour de la marque",
                "Sujets choisis au feeling, pas alignés sur les personas",
                "Pas de calendrier éditorial, beaucoup de stress en fin de semaine",
                "Difficulté à mesurer ce qui fonctionne et ce qui ne fonctionne pas",
                "Burn-out créatif : « je n'ai plus d'idées »",
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
                 "examples": "Temps de production par contenu, volume publié"},
                {"level": "Moyen terme", "type": "Qualité (cohérence, brand voice)",
                 "horizon": "Mesurable J+14",
                 "examples": "Cohérence éditoriale entre canaux, % contenus alignés brand voice"},
                {"level": "Long terme", "type": "Impact business (engagement, leads)",
                 "horizon": "Observatoire J+30/J+60",
                 "examples": "Taux d'engagement moyen, leads générés via contenu"},
            ],
        },
        "kpi_measurement_method": {
            "title": "Méthode de collecte des KPIs",
            "milestones": [
                {"when": "J0", "what": "Formulaire de baseline auto-affiché en début de module (obligatoire pour valider le module)"},
                {"when": "J+7", "what": "Rappel par email + notification in-app"},
                {"when": "J+14", "what": "Formulaire de mesure d'impact auto-affiché + rappel"},
                {"when": "J+30", "what": "Rappel facultatif pour le KPI observatoire (taux d'engagement)"},
                {"when": "J+60", "what": "Rappel facultatif final + consolidation dashboard"},
            ],
        },
        "tutorials": [
            {"id": "t1", "title": "Encode ta brand voice en 30 minutes",
             "duration_min": 15, "format": "vidéo screencast + template Notion à dupliquer"},
            {"id": "t2", "title": "Bâtis ton calendrier éditorial trimestriel",
             "duration_min": 20, "format": "vidéo screencast + template Airtable"},
        ],
    },
}


# =============================================================================
# MODULE 2 — Campaign Performance Optimization
# =============================================================================
MODULE_2 = {
    "title_fr": "Campaign Performance Optimization",
    "description_fr": (
        "Construis et opère une growth loop IA en Afrique du Nord : génération "
        "créative à grande échelle (texte + visuel), A/B testing rigoureux, "
        "lecture des données de performance, scaling intelligent. Tu réduis "
        "ton CAC de 20 à 30 % en gardant la même enveloppe budgétaire, et tu "
        "passes d'un cycle d'itération de 2-3 semaines à 3-5 jours."
    ),
    "level": "Pratique",
    "role": ROLE,
    "journey_stage": "Funnel marketing — Acquisition payante",
    "display_order": 2,
    "estimated_duration_min": 300,  # 3-5h
    "format": "blended",
    "is_active": True,

    "skill_name": "Optimisation de campagnes et growth IA",

    "learning_objective_fr": (
        "À l'issue de ce module, l'apprenant sait (1) générer 10+ variantes "
        "d'ad copy et de visuels avec l'IA en moins d'1h, et (2) opérer une "
        "growth loop structurée (test → mesure → décision → itération) qui "
        "réduit le CAC de manière mesurable."
    ),
    "expected_outcome_fr": (
        "Réduction de 20 à 30 % du CAC sur la même enveloppe budgétaire, "
        "volume de créas testées multiplié par 5 à 10 (de 2-4/mois à 15-30/mois), "
        "cycle d'itération créative réduit de 2-3 semaines à 3-5 jours."
    ),
    "why_this_module_fr": (
        "Les équipes marketing en Afrique du Nord investissent en publicité "
        "(Meta Ads, Google Ads, TikTok Ads) mais sans méthode de génération "
        "créative ni boucle d'optimisation rigoureuse. Résultat : le CAC monte "
        "au fil du temps, les créas s'usent vite, et l'équipe est constamment "
        "dans la réaction plutôt que dans l'amélioration continue."
    ),
    "recommended_when_fr": (
        "Quand ton CAC dépasse ta cible de 30 % ou plus, que tu testes moins "
        "de 5 créas par mois, ou que ton cycle d'itération entre 2 tests "
        "dépasse 10 jours."
    ),
    "role_based_example_fr": (
        "Yacine, growth marketer chez une PME e-commerce à Tunis, gère un "
        "budget Meta Ads de 5 000 TND/mois. Il a 3 créas en ligne. Le CAC "
        "est passé de 25 TND à 45 TND en deux mois. Yacine ne sait pas si "
        "c'est dû à l'usure créative, à la saturation de l'audience, ou à "
        "l'augmentation de la concurrence. Il « teste » au feeling : double "
        "le budget de la créa qui semble marcher, coupe celles qui ne "
        "marchent plus. Avec ce module, Yacine génère 10 variantes d'ad copy "
        "en 5 minutes, produit 5 visuels en 20 minutes, structure un A/B "
        "test rigoureux, et réduit son CAC à 28 TND en 3 semaines."
    ),
    "takeaway_fr": (
        "Une growth loop IA repose sur 4 composants : génération à grande "
        "échelle (texte + visuel), déploiement automatique, collecte des "
        "données de performance, boucle d'apprentissage qui réinjecte les "
        "insights gagnants. Le test sans rigueur (« j'ai testé un peu ») "
        "donne des résultats non exploitables — c'est pour ça qu'on cadre "
        "l'A/B test avant de lancer."
    ),
    "action_point_fr": (
        "Cette semaine : identifie 1 campagne dont tu veux baisser le CAC, "
        "applique le Prompt 1 pour générer 10 variantes d'ad copy, sélectionne "
        "5 angles à tester, génère les visuels associés, et lance un A/B test "
        "structuré sur 5-7 jours."
    ),
    "practical_application_fr": (
        "Application directe sur ta propre campagne en cours : pas de cas "
        "fictif. Tu utilises tes vraies données de performance, tu mesures "
        "le CAC avant/après, et tu construis ta bibliothèque personnelle "
        "des angles publicitaires gagnants pour ton secteur."
    ),

    "key_concepts_fr": [
        "Leviers d'optimisation publicitaire (CTR, CPC, CVR, CAC, ROAS)",
        "Génération de 10+ variantes d'ad copy avec ChatGPT en 5 minutes",
        "Génération de visuels publicitaires avec Midjourney / DALL-E / AdCreative.ai",
        "Conception d'A/B test rigoureux (variables isolées, échantillon, durée)",
        "Lecture et interprétation des rapports Meta / Google / TikTok Ads",
        "Boucle d'apprentissage continue (test → mesure → décision → itération)",
        "Capitalisation et documentation des insights gagnants",
        "Adaptation aux plateformes dominantes Afrique du Nord (Meta, TikTok, WhatsApp)",
    ],

    "next_recommended_module_fr": "Audience Insights & Segmentation",

    # ──── PROMPTS — 3 prompts validés ───────────────────────────────────────
    "prompt_examples_fr": [
        {
            "id": "prompt_1_ad_copy_variants",
            "title": "Prompt 1 — 10 variantes d'ad copy",
            "use_case": "Produire en 5 minutes 10 angles publicitaires testables sur Meta / Google Ads",
            "tags": ["ad copy", "variantes", "angles publicitaires"],
            "content": (
                "Tu es un performance copywriter spécialisé Meta Ads et Google Ads "
                "au Maghreb.\n"
                "Génère 10 variantes d'ad copy testables.\n\n"
                "PRODUIT / OFFRE :\n"
                "- Description : [PRODUIT_OU_SERVICE]\n"
                "- Bénéfice principal : [BENEFICE_1]\n"
                "- Différenciateur : [DIFFERENCIATEUR]\n"
                "- Preuve sociale : [PREUVE_CHIFFREE]\n"
                "- Prix / promo : [PRIX_OU_PROMO]\n\n"
                "AUDIENCE CIBLE :\n"
                "- Persona : [PERSONA]\n"
                "- Pain points : [3_PAIN_POINTS]\n"
                "- Pays : [PAYS_MAGHREB]\n"
                "- Langue : [FR / AR / FR+AR mix]\n\n"
                "GÉNÈRE 10 VARIANTES SELON CES ANGLES :\n"
                "1. Problème/solution (hook douleur)\n"
                "2. Bénéfice direct (gain immédiat)\n"
                "3. Preuve sociale (témoignage / chiffre)\n"
                "4. Curiosité (question intrigante)\n"
                "5. Urgence (offre limitée)\n"
                "6. Avant/après (transformation)\n"
                "7. Comparatif (vs alternative)\n"
                "8. Storytelling (mini-histoire)\n"
                "9. Statistique choc (data hook)\n"
                "10. UGC style (témoignage authentique)\n\n"
                "POUR CHAQUE VARIANTE :\n"
                "- Headline (max 40 caractères)\n"
                "- Primary text (max 125 caractères)\n"
                "- CTA\n"
                "- Note : pourquoi cet angle peut performer sur cette audience"
            ),
            "variables": ["PRODUIT_OU_SERVICE", "BENEFICE_1", "DIFFERENCIATEUR",
                          "PREUVE_CHIFFREE", "PRIX_OU_PROMO", "PERSONA",
                          "3_PAIN_POINTS", "PAYS_MAGHREB", "LANGUE"],
            "expected_output": "10 variantes d'ad copy avec headline + primary text + CTA + justification",
            "tools": ["ChatGPT", "Claude"],
        },
        {
            "id": "prompt_2_visual_brief",
            "title": "Prompt 2 — Brief visuel pour IA générative",
            "use_case": "Produire un brief précis pour Midjourney / DALL-E et obtenir des visuels publicitaires de qualité dès la première itération",
            "tags": ["visuel", "brief", "IA générative"],
            "content": (
                "Tu es un directeur artistique digital spécialisé en publicité "
                "performance au Maghreb.\n"
                "Construis un brief visuel pour générer 3 visuels d'ad avec "
                "Midjourney / DALL-E.\n\n"
                "CAMPAGNE :\n"
                "- Produit : [PRODUIT]\n"
                "- Objectif : [CONVERSION / NOTORIÉTÉ / CONSIDÉRATION]\n"
                "- Ad copy associé : [COLLER_AD_COPY]\n"
                "- Audience : [PERSONA + PAYS]\n\n"
                "CONTRAINTES :\n"
                "- Format : [1:1 / 9:16 / 4:5]\n"
                "- Plateforme : [META / TIKTOK / GOOGLE]\n"
                "- Charte graphique : [COULEURS + STYLE]\n"
                "- Pas de texte intégré dans le visuel\n\n"
                "GÉNÈRE 3 BRIEFS :\n"
                "BRIEF 1 — Style « lifestyle réaliste »\n"
                "  Prompt MJ/DALL-E : [prompt complet en anglais]\n"
                "  Justification : [pourquoi ce style pour cette audience]\n\n"
                "BRIEF 2 — Style « product hero »\n"
                "  Prompt MJ/DALL-E : ...\n\n"
                "BRIEF 3 — Style « UGC / authentique »\n"
                "  Prompt MJ/DALL-E : ...\n\n"
                "BONUS Maghreb (Pending validation Achref/Oumeima) :\n"
                "  1 prompt MJ pour version culturellement adaptée Maghreb "
                "(modèles diversifiés, environnements urbains régionaux, palette "
                "chaude méditerranéenne)"
            ),
            "variables": ["PRODUIT", "OBJECTIF", "COLLER_AD_COPY", "PERSONA_PAYS",
                          "FORMAT", "PLATEFORME", "COULEURS_STYLE"],
            "expected_output": "3 briefs visuels + 1 bonus Maghreb avec prompts MJ/DALL-E prêts à utiliser",
            "tools": ["ChatGPT", "Midjourney", "DALL-E", "AdCreative.ai"],
        },
        {
            "id": "prompt_3_ab_test_plan",
            "title": "Prompt 3 — Plan d'A/B test structuré",
            "use_case": "Concevoir un plan de test rigoureux qui isole les variables et donne des résultats exploitables",
            "tags": ["A/B test", "expérimentation", "structuration"],
            "content": (
                "Tu es un growth analyst expérimenté en performance marketing au Maghreb.\n"
                "Construis un plan d'A/B test structuré pour ma campagne.\n\n"
                "CONTEXTE :\n"
                "- Plateforme : [META / GOOGLE / TIKTOK]\n"
                "- Objectif business : [CONVERSION / LEAD / VENTE]\n"
                "- Budget total disponible avec devise (TND/MAD/DZD/USD) : [BUDGET]\n"
                "- Durée souhaitée : [JOURS]\n"
                "- Question testée : [QUESTION_PRECISE]\n"
                "  (ex : « lifestyle vs product hero a-t-il un meilleur CTR ? »)\n\n"
                "GÉNÈRE LE PLAN :\n"
                "1. HYPOTHÈSE TESTÉE (1 phrase claire)\n"
                "2. VARIABLES\n"
                "   - Variable testée (1 seule)\n"
                "   - Variables maintenues constantes\n"
                "3. STRUCTURE DES GROUPES\n"
                "   - Groupe A : ...\n"
                "   - Groupe B : ...\n"
                "4. KPI PRIMAIRE + KPI SECONDAIRES\n"
                "5. TAILLE D'ÉCHANTILLON ET DURÉE recommandées\n"
                "6. RÈGLE DE DÉCISION\n"
                "   - Si A bat B de X % → action 1\n"
                "   - Si égalité statistique → action 2\n"
                "   - Si B bat A → action 3\n"
                "7. PROCHAIN TEST À LANCER (capitalisation des apprentissages)"
            ),
            "variables": ["PLATEFORME", "OBJECTIF", "BUDGET", "DUREE",
                          "QUESTION_PRECISE"],
            "expected_output": "Plan d'A/B test 7 sections avec hypothèse, variables, KPIs, règle de décision",
            "tools": ["ChatGPT", "Meta Ads Manager / Google Ads (pour le déploiement)"],
        },
    ],

    "practical_exercise_fr": {
        "title": "Mission : Lance un A/B test sur 5 nouvelles créas IA-augmentées",
        "duration_minutes": 120,
        "tools_required": [
            "ChatGPT",
            "Midjourney OU AdCreative.ai (essai gratuit)",
            "Meta Ads OU Google Ads (campagne en cours)",
        ],
        "objective": (
            "Industrialiser ton sprint créatif hebdomadaire : 10 ad copies + "
            "5 visuels + A/B test structuré, et identifier au moins 1 créa "
            "qui bat ta baseline de 10 % sur le CAC."
        ),
        "steps": [
            {"n": 1, "title": "Identification de la campagne",
             "description": "Identifie 1 campagne en cours dont tu veux baisser le CAC."},
            {"n": "1.5", "title": "Chronométrage baseline",
             "description": (
                 "Note ton temps de production manuelle habituel pour 1 créa "
                 "(brief + écriture + visuel). Tu compareras à la fin."
             )},
            {"n": 2, "title": "Génération de 10 ad copies",
             "description": (
                 "Applique le Prompt 1 et sélectionne 5 angles à tester selon "
                 "leur pertinence pour ton audience."
             )},
            {"n": 3, "title": "Génération des 5 visuels",
             "description": (
                 "Applique le Prompt 2 pour produire les briefs visuels, puis "
                 "génère les 5 visuels avec Midjourney ou AdCreative.ai."
             )},
            {"n": 4, "title": "Structuration de l'A/B test",
             "description": (
                 "Applique le Prompt 3 pour cadrer l'hypothèse, isoler la "
                 "variable testée, définir la règle de décision."
             )},
            {"n": 5, "title": "Lancement du test",
             "description": (
                 "Lance le test sur 5-7 jours avec un budget équilibré entre "
                 "les variantes (split test natif Meta Ads ou Google Ads)."
             )},
            {"n": 6, "title": "Lecture et décision à J+7",
             "description": (
                 "Applique la règle de décision définie à l'étape 4. Documente "
                 "les insights gagnants dans une fiche réutilisable."
             )},
        ],
        "success_criteria": [
            "10 ad copies + 5 visuels produits en moins de 90 min total",
            "A/B test structuré et lancé avec hypothèse claire",
            "Au moins 1 créa qui bat la baseline CAC de 10 % à J+7",
        ],
        "maghreb_note": (
            "TikTok Ads est particulièrement performant en Afrique du Nord sur "
            "la cible 18-35 ans, souvent avec un CAC 30-50 % inférieur à Meta. "
            "Si tu n'as jamais testé, profite de ce module pour lancer une "
            "première campagne TikTok en parallèle de ton A/B test Meta. "
            "Pour les visuels, privilégie un style « UGC / authentique » à un "
            "style « product hero » trop publicitaire — l'engagement est "
            "généralement 2-3× supérieur sur les audiences régionales."
        ),
    },

    "comparison_tables_fr": {
        "tools": {
            "title": "Outils — Comparatif et alternatives Afrique du Nord",
            "headers": ["Outil", "Pricing", "Usage", "Note Maghreb"],
            "rows": [
                ["ChatGPT / Claude", "Free / 20 USD/mois",
                 "Ad copy variants + plan A/B test + analyses",
                 "Free tier suffisant pour démarrer"],
                ["Midjourney / DALL-E", "10-30 USD/mois",
                 "Génération de visuels publicitaires",
                 "Carte internationale requise"],
                ["AdCreative.ai", "À partir de 25 USD/mois",
                 "Génération automatique d'ads (texte + visuel) + scoring IA",
                 "Free trial 7 jours, cartes locales TN/MA acceptées"],
                ["Meta Ads Manager", "Free (commission CPM)",
                 "Lancement et A/B testing des campagnes Meta",
                 "Plateforme dominante Maghreb sur 25-55 ans"],
                ["Google Ads", "Free (commission CPC)",
                 "Campagnes search + display",
                 "Très efficace sur l'intent commercial"],
                ["TikTok Ads", "Free (commission CPM)",
                 "Campagnes vidéo, audience 18-35 ans",
                 "CAC souvent 30-50 % inférieur à Meta sur cette cible"],
                ["Make / n8n", "Free / 20 USD/mois Make ou self-hosted n8n",
                 "Orchestration de la growth loop automatisée",
                 "n8n self-hosted ~5 USD/VPS = quasi-gratuit"],
            ],
        },
        "workflows": {
            "title": "Workflows — 2 niveaux de sophistication",
            "headers": ["Workflow", "Outils", "Setup", "Coût/mois", "Niveau"],
            "rows": [
                ["W1 : Sprint créatif hebdomadaire (no-code)",
                 "ChatGPT + Midjourney + Meta Ads Manager",
                 "30-45 min première fois",
                 "30-50 USD/mois (selon usage MJ)",
                 "Débutant"],
                ["W2 : Growth loop automatisée (low-code)",
                 "Meta Ads API + Make + OpenAI API + AdCreative API + Slack",
                 "3-5h première fois",
                 "~80-150 USD/mois (selon volume)",
                 "Intermédiaire"],
                ["W2 low-cost Maghreb",
                 "Meta Ads API + n8n + ChatGPT manuel + AdCreative free trial",
                 "4-6h première fois",
                 "~30 USD/mois (VPS n8n + AdCreative basic)",
                 "Intermédiaire"],
            ],
        },
        "kpi_targets": {
            "title": "KPIs cibles — Baseline personnalisée → Cible J+14",
            "headers": ["Indicateur", "Niveau temporel", "Baseline (J0)", "Cible"],
            "rows": [
                ["Volume de créas testées par mois", "Court terme (J+14)",
                 "À renseigner par l'apprenant",
                 "Multiplié par 5 à 10"],
                ["Cycle d'itération créative (jours entre tests)",
                 "Court terme (J+14)",
                 "À renseigner",
                 "Réduit à 3-5 jours"],
                ["CAC moyen", "Observatoire (J+30/J+60)",
                 "À renseigner",
                 "Réduction de 20 à 30 %"],
            ],
        },
    },

    "section_content_fr": {
        "use_case_detail": {
            "title": "Le problème business",
            "narrative": (
                "Les équipes marketing en Afrique du Nord investissent en "
                "publicité (Meta Ads, Google Ads, TikTok Ads) mais sans "
                "méthode de génération créative ni boucle d'optimisation "
                "rigoureuse. Résultat : le CAC monte au fil du temps, les "
                "créas s'usent vite, et l'équipe est constamment dans la "
                "réaction plutôt que dans l'amélioration continue."
            ),
            "pain_points": [
                "CAC élevé et instable (souvent 30-50 % au-dessus de la cible)",
                "Aucun A/B test structuré ni boucle d'apprentissage",
                "Créas produites manuellement, lentement, en faible volume",
                "Optimisation basée sur l'intuition, pas sur la donnée",
                "Difficulté à scaler les budgets sans dégrader la performance",
                "Pas de capitalisation : ce qui marche n'est pas documenté",
            ],
        },
        "tutorials": [
            {"id": "t1", "title": "Génère 10 ad copies en 5 minutes",
             "duration_min": 10, "format": "vidéo screencast"},
            {"id": "t2", "title": "Lance ton premier A/B test rigoureux",
             "duration_min": 20, "format": "vidéo screencast + template Notion"},
        ],
    },
}


# =============================================================================
# MODULE 3 — Audience Insights & Segmentation
# =============================================================================
MODULE_3 = {
    "title_fr": "Audience Insights & Segmentation",
    "description_fr": (
        "Extrais des personas data-driven à partir de tes propres données "
        "(CRM, GA4, Meta Insights, e-commerce), enrichis-les avec l'IA, et "
        "active chaque segment avec des messages personnalisés. Tu passes "
        "de 1-2 personas intuitifs à 4-6 personas data-driven, et tu observes "
        "une amélioration mesurable de ton taux de conversion grâce à un "
        "meilleur targeting."
    ),
    "level": "Expert",
    "role": ROLE,
    "journey_stage": "Funnel marketing — Ciblage data-driven",
    "display_order": 3,
    "estimated_duration_min": 180,  # 2-4h
    "format": "blended",
    "is_active": True,

    "skill_name": "Audience intelligence et segmentation IA",

    "learning_objective_fr": (
        "À l'issue de ce module, l'apprenant sait (1) extraire des personas "
        "data-driven à partir de ses propres données utilisateurs, et "
        "(2) activer chaque segment avec un messaging adapté pour améliorer "
        "son taux de conversion de manière mesurable."
    ),
    "expected_outcome_fr": (
        "Passage de 1-2 personas intuitifs à 4-6 personas data-driven, "
        "+25 % d'amélioration relative du taux de conversion sur les "
        "campagnes ciblées (observatoire J+30/J+60), relevance score "
        "Meta Ads / Google Ads ≥ 7/10."
    ),
    "why_this_module_fr": (
        "Beaucoup d'équipes marketing en Afrique du Nord ont accès à une "
        "masse de données utilisateurs (CRM, Google Analytics, Meta Insights, "
        "base e-commerce) mais n'arrivent pas à les transformer en personas "
        "actionnables. Résultat : la segmentation reste rudimentaire (âge + "
        "pays), les messages restent génériques, et le taux de conversion "
        "stagne ou régresse."
    ),
    "recommended_when_fr": (
        "Quand tu as 1 000+ utilisateurs/clients dans ta base mais que tu "
        "cibles « tout le monde » dans tes campagnes, que ton relevance "
        "score Meta est < 5/10, ou que ton taux de conversion stagne malgré "
        "une augmentation du budget."
    ),
    "role_based_example_fr": (
        "Lina, marketing manager d'une marque cosmétique au Maroc, a 25 000 "
        "clients dans sa base e-commerce et 40 000 abonnés Instagram. Quand "
        "elle lance une campagne, elle cible « femmes 25-45 ans Casablanca + "
        "Rabat ». Le ROAS est bas. Pourtant, dans sa base, il y a "
        "probablement 4 ou 5 segments très différents (jeunes urbaines "
        "bio-curieuses, mamans trentenaires fidèles à une marque, "
        "professionnelles 40+ premium...). Avec ce module, Lina extrait "
        "5 personas data-driven en 30 minutes, adapte son messaging par "
        "segment, et observe un taux de conversion qui passe de 1.3 % à "
        "2.1 % sur la campagne ciblée."
    ),
    "takeaway_fr": (
        "Un persona data-driven n'est pas un avatar inventé : il est extrait "
        "de signaux comportementaux réels (RFM, centres d'intérêt, parcours "
        "d'achat) et traduit en représentation actionnable par un LLM. La "
        "vraie valeur ne vient pas du persona lui-même mais de ce qu'il "
        "permet : un messaging adapté, un canal prioritaire, un budget bien "
        "alloué."
    ),
    "action_point_fr": (
        "Cette semaine : exporte un échantillon anonymisé de 50 utilisateurs "
        "de ta base, applique le Prompt 1 pour générer 4 personas "
        "data-driven, sélectionne le persona prioritaire pour ton prochain "
        "objectif business, et lance une campagne ciblée avec messaging adapté."
    ),
    "practical_application_fr": (
        "Application directe sur ta propre base utilisateurs : pas de cas "
        "fictif. Tu utilises tes vraies données (CRM ou GA4 ou e-commerce), "
        "tu construis tes 4-6 personas exploitables, et tu mesures le taux "
        "de conversion d'une campagne ciblée vs une campagne large."
    ),

    "key_concepts_fr": [
        "Frameworks de segmentation (RFM, behavioral, psychographique)",
        "Extraction de données multi-sources (CRM, GA4, Meta, e-commerce)",
        "Construction de personas data-driven via clustering IA + synthèse LLM",
        "Adaptation du messaging par persona (tonalité, bénéfices, canaux)",
        "Configuration d'audiences personnalisées dans Meta Ads / Google Ads",
        "Mesure de la pertinence du ciblage (relevance score, conversion par segment)",
        "Boucle d'apprentissage continu sur les segments performants",
        "Spécificités culturelles Afrique du Nord (langue, valeurs, parcours d'achat)",
    ],

    "next_recommended_module_fr": "Certificat AI Marketing Strategist + Bridge commercial",

    # ──── PROMPTS — 3 prompts validés ───────────────────────────────────────
    "prompt_examples_fr": [
        {
            "id": "prompt_1_personas_data_driven",
            "title": "Prompt 1 — Génération de personas data-driven",
            "use_case": "Transformer une base de données utilisateurs en 4-6 personas exploitables",
            "tags": ["personas", "data-driven", "clustering"],
            "content": (
                "Tu es un audience strategist senior B2B/B2C au Maghreb.\n"
                "Construis 4 à 6 personas data-driven à partir de ces données.\n\n"
                "DONNÉES UTILISATEURS :\n"
                "- Source : [CRM / GA4 / META / E-COMMERCE]\n"
                "- Volume total : [NOMBRE_UTILISATEURS]\n"
                "- Variables disponibles : [LISTER : âge, ville, panier moyen, "
                "fréquence, produits préférés, source d'acquisition, etc.]\n"
                "- Échantillon (50 lignes représentatives anonymisées) : "
                "[COLLER_ECHANTILLON]\n\n"
                "MON OFFRE :\n"
                "- Produit/service : [DESCRIPTION]\n"
                "- Pays cibles : [PAYS_MAGHREB]\n"
                "- Objectif : [ACQUISITION / RÉTENTION / UPSELL]\n\n"
                "POUR CHAQUE PERSONA GÉNÈRE :\n"
                "1. Nom évocateur (ex : « Yasmine la maman urbaine »)\n"
                "2. Description démographique (3 lignes)\n"
                "3. 3 pain points principaux\n"
                "4. 3 motivations d'achat\n"
                "5. Canaux préférés (avec ordre de priorité)\n"
                "6. Tonalité de communication recommandée\n"
                "7. 3 messages clés qui résonneraient\n"
                "8. Estimation : % de la base + valeur business\n"
                "9. Recommandation d'activation (campagne type, budget suggéré)\n\n"
                "EN CONCLUSION :\n"
                "- Quel persona prioriser pour [OBJECTIF] et pourquoi\n"
                "- Persona à éviter en acquisition payante (faible ROI attendu)"
            ),
            "variables": ["SOURCE", "NOMBRE_UTILISATEURS", "VARIABLES_DISPONIBLES",
                          "COLLER_ECHANTILLON", "DESCRIPTION", "PAYS_MAGHREB",
                          "OBJECTIF"],
            "expected_output": "4-6 personas avec 9 dimensions chacun + recommandation de priorisation",
            "tools": ["ChatGPT", "Claude"],
        },
        {
            "id": "prompt_2_rfm_segmentation",
            "title": "Prompt 2 — Segmentation comportementale RFM",
            "use_case": "Classer une base e-commerce ou CRM en segments actionnables selon Recency, Frequency, Monetary",
            "tags": ["RFM", "segmentation", "e-commerce"],
            "content": (
                "Tu es un data analyst CRM spécialisé en e-commerce au Maghreb.\n"
                "Analyse cette base et propose une segmentation RFM actionnable.\n\n"
                "BASE CLIENT :\n"
                "- Volume total : [NB_CLIENTS]\n"
                "- Période d'observation : [12_DERNIERS_MOIS]\n"
                "- Devise : [TND / MAD / DZD / EUR / USD]\n"
                "- Données disponibles : Recency, Frequency, Monetary\n"
                "- Échantillon (top 30 + bottom 30 anonymisés) : "
                "[COLLER_DONNÉES]\n\n"
                "MON OBJECTIF : [RÉTENTION / ACQUISITION / WIN-BACK]\n\n"
                "GÉNÈRE :\n"
                "1. SEUILS RFM ADAPTÉS À MON BUSINESS\n"
                "   - R : récence en jours (ex : R5 = 0-30, R1 = >180)\n"
                "   - F : nb commandes (ex : F5 = >10, F1 = 1)\n"
                "   - M : valeur cumulée (ex : M5 = top 20 % panier)\n"
                "2. 6 SEGMENTS PRIORITAIRES\n"
                "   - Champions (RFM 555)\n"
                "   - Loyaux (RFM 444-554)\n"
                "   - Potentiels (R5, F bas)\n"
                "   - À risque (R bas, F+M hauts)\n"
                "   - Hibernants (R très bas)\n"
                "   - Perdus (R1 F1 M1)\n"
                "3. POUR CHAQUE SEGMENT :\n"
                "   - % estimé de la base\n"
                "   - Valeur business\n"
                "   - Action recommandée (campagne, message, canal)\n"
                "   - Budget suggéré dans la devise locale\n"
                "4. PLAN D'ACTIVATION 30 JOURS"
            ),
            "variables": ["NB_CLIENTS", "PERIODE", "DEVISE", "COLLER_DONNEES",
                          "OBJECTIF"],
            "expected_output": "Seuils RFM + 6 segments avec actions + plan d'activation 30 jours",
            "tools": ["ChatGPT", "Excel / Google Sheets (pour les calculs RFM)"],
        },
        {
            "id": "prompt_3_persona_messaging",
            "title": "Prompt 3 — Activation par persona (messaging adapté)",
            "use_case": "Décliner 1 message produit en 4 versions adaptées chacune à un persona spécifique",
            "tags": ["messaging", "adaptation", "multi-persona"],
            "content": (
                "Tu es un copywriter B2C au Maghreb.\n"
                "Adapte le message produit à 4 personas distincts.\n\n"
                "MESSAGE SOURCE :\n"
                "- Produit : [PRODUIT]\n"
                "- Promesse générique : [MESSAGE_DE_BASE]\n\n"
                "PERSONAS À ACTIVER :\n"
                "- Persona 1 : [COLLER_PERSONA_1]\n"
                "- Persona 2 : [COLLER_PERSONA_2]\n"
                "- Persona 3 : [COLLER_PERSONA_3]\n"
                "- Persona 4 : [COLLER_PERSONA_4]\n\n"
                "POUR CHAQUE PERSONA, GÉNÈRE :\n"
                "1. Hook adapté (3 secondes pour capter)\n"
                "2. Bénéfice principal (le seul qui compte pour CE persona)\n"
                "3. Preuve sociale ciblée (témoignage / chiffre crédible)\n"
                "4. Objection probable + réponse\n"
                "5. CTA adapté au canal préféré\n"
                "6. Format publicitaire recommandé (carrousel / vidéo / image)\n\n"
                "FORMAT DE SORTIE :\n"
                "═══ PERSONA 1 : [Nom] ═══\n"
                "Hook : ...\n"
                "Bénéfice : ...\n"
                "Preuve : ...\n"
                "Objection + Réponse : ...\n"
                "CTA : ...\n"
                "Format : ..."
            ),
            "variables": ["PRODUIT", "MESSAGE_DE_BASE", "COLLER_PERSONA_1",
                          "COLLER_PERSONA_2", "COLLER_PERSONA_3", "COLLER_PERSONA_4"],
            "expected_output": "4 messages adaptés par persona avec hook, bénéfice, preuve, objection, CTA, format",
            "tools": ["ChatGPT", "Meta Ads Manager (pour configurer les audiences)"],
        },
    ],

    "practical_exercise_fr": {
        "title": "Mission : Construis 4 personas data-driven et active 1 campagne ciblée",
        "duration_minutes": 90,
        "tools_required": [
            "ChatGPT",
            "Ton CRM ou Google Analytics 4",
            "Meta Ads OU Google Ads",
        ],
        "objective": (
            "Extraire 4 personas data-driven de ta vraie base utilisateurs, "
            "lancer une campagne ciblée avec messaging adapté, et obtenir un "
            "taux de conversion supérieur de ≥ 15 % à une campagne large "
            "équivalente."
        ),
        "steps": [
            {"n": 1, "title": "Export anonymisé de l'échantillon",
             "description": (
                 "Exporte un échantillon anonymisé de tes données utilisateurs "
                 "(50 lignes représentatives). Anonymise les données "
                 "personnelles avant de les coller dans ChatGPT."
             )},
            {"n": "1.5", "title": "Chronométrage baseline",
             "description": (
                 "Note ton nombre de personas actuels (souvent 1-2 intuitifs) "
                 "et ton taux de conversion habituel sur les campagnes larges."
             )},
            {"n": 2, "title": "Génération des 4 personas",
             "description": (
                 "Applique le Prompt 1 et génère 4 personas data-driven "
                 "exploitables avec leurs 9 dimensions chacun."
             )},
            {"n": 3, "title": "Sélection du persona prioritaire",
             "description": (
                 "Sélectionne le persona prioritaire pour ton prochain objectif "
                 "business (acquisition, rétention, upsell)."
             )},
            {"n": 4, "title": "Adaptation du messaging",
             "description": (
                 "Applique le Prompt 3 pour générer le messaging adapté au "
                 "persona prioritaire (hook, bénéfice, preuve, CTA, format)."
             )},
            {"n": 5, "title": "Configuration audience custom",
             "description": (
                 "Configure une audience custom dans Meta Ads (ou Google Ads) "
                 "à partir de ton CRM ou de critères matchant le persona."
             )},
            {"n": 6, "title": "Lancement et mesure",
             "description": (
                 "Lance la campagne ciblée en parallèle d'une campagne large "
                 "équivalente. Mesure le taux de conversion sur 14 jours."
             )},
        ],
        "success_criteria": [
            "4 personas data-driven générés et documentés",
            "1 campagne ciblée lancée avec messaging adapté",
            "Taux de conversion de la campagne ciblée ≥ 15 % supérieur à la campagne large équivalente",
        ],
        "maghreb_note": (
            "Pour les marques B2C en Afrique du Nord, les segments les plus "
            "puissants sont souvent : (1) les jeunes urbaines bio-curieuses "
            "(Casablanca / Tunis / Alger 25-35 ans), (2) les mamans "
            "trentenaires fidèles aux marques (30-40 ans, parcours produit), "
            "(3) la diaspora maghrébine en Europe (souvent négligée mais à "
            "fort pouvoir d'achat). Pour les marques B2B, segmente par taille "
            "d'entreprise et secteur plutôt que par titre de poste — les "
            "intitulés de poste sont moins normalisés en Afrique du Nord "
            "qu'en Europe."
        ),
    },

    "comparison_tables_fr": {
        "tools": {
            "title": "Outils — Comparatif et alternatives Afrique du Nord",
            "headers": ["Outil", "Pricing", "Usage", "Note Maghreb"],
            "rows": [
                ["ChatGPT / Claude", "Free / 20 USD/mois",
                 "Génération personas + segmentation RFM + adaptation messaging",
                 "Free tier suffisant pour démarrer"],
                ["Google Analytics 4", "Gratuit",
                 "Source principale de données comportementales web",
                 "Standard en Afrique du Nord"],
                ["Meta Business Suite", "Gratuit",
                 "Audiences custom + insights démographiques",
                 "Indispensable pour Maghreb (Meta = canal dominant)"],
                ["HubSpot / Salesforce", "Variable",
                 "Données CRM clients + scoring + segmentation native",
                 "Cohérent si déjà utilisé en Module 1"],
                ["Mixpanel / Amplitude", "Free / 25-89 USD/mois",
                 "Analyse comportementale produit avancée",
                 "Optionnel pour V1, utile si SaaS / app mobile"],
                ["Make / Fivetran", "Free / 20 USD/mois",
                 "Synchronisation des sources de données",
                 "n8n self-hosted = quasi-gratuit"],
                ["BigQuery / Sheets", "Free / pay-per-use",
                 "Stockage et calcul RFM à grande échelle",
                 "Sheets suffit jusqu'à 50 000 lignes"],
            ],
        },
        "workflows": {
            "title": "Workflows — 2 niveaux de sophistication",
            "headers": ["Workflow", "Outils", "Setup", "Coût/mois", "Niveau"],
            "rows": [
                ["W1 : Audit personas trimestriel (no-code)",
                 "CRM/GA4 + Excel + ChatGPT + Notion + Meta Ads",
                 "30-60 min première fois",
                 "0 USD (free tiers)",
                 "Débutant"],
                ["W2 : Audience intelligence en continu (low-code)",
                 "Make + BigQuery + OpenAI API + Slack + Meta Ads API",
                 "4-6h première fois",
                 "~50-100 USD/mois (selon volume)",
                 "Intermédiaire"],
                ["W2 low-cost Maghreb",
                 "Sheets + n8n + ChatGPT manuel + Meta Ads Manager",
                 "5-7h première fois",
                 "~5 USD/mois (VPS n8n)",
                 "Intermédiaire"],
            ],
        },
        "kpi_targets": {
            "title": "KPIs cibles — Baseline personnalisée → Cible J+14",
            "headers": ["Indicateur", "Niveau temporel", "Baseline (J0)", "Cible"],
            "rows": [
                ["Nombre de personas activés", "Court terme (J+14)",
                 "1 ou 2 (intuition)",
                 "4 à 6 (data-driven)"],
                ["Relevance score Meta Ads", "Court terme (J+14)",
                 "À renseigner",
                 "≥ 7/10"],
                ["Taux de conversion (campagnes ciblées)",
                 "Observatoire (J+30/J+60)",
                 "À renseigner",
                 "+25 % d'amélioration relative"],
            ],
        },
    },

    "section_content_fr": {
        "use_case_detail": {
            "title": "Le problème business",
            "narrative": (
                "Beaucoup d'équipes marketing en Afrique du Nord ont accès "
                "à une masse de données utilisateurs (CRM, Google Analytics, "
                "Meta Insights, base e-commerce) mais n'arrivent pas à les "
                "transformer en personas actionnables. Résultat : la "
                "segmentation reste rudimentaire (âge + pays), les messages "
                "restent génériques, et le taux de conversion stagne ou régresse."
            ),
            "pain_points": [
                "Ciblage médiocre (CAC élevé, conversion basse)",
                "Messages génériques qui ne résonnent fortement avec personne",
                "Personas figés, basés sur l'intuition plutôt que sur la donnée",
                "Pas de personnalisation des parcours (email, ads, web)",
                "Données sous-exploitées : les insights restent dans les outils",
                "Cycle de vie client mal compris (acquisition vs rétention)",
            ],
            "maghreb_specifics": [
                "Multilinguisme (français / arabe / darija selon la cible)",
                "Importance de la diaspora (souvent négligée, fort pouvoir d'achat)",
                "Saisonnalités culturelles fortes (Ramadan, Aïd, rentrée scolaire)",
                "Intitulés de poste moins normalisés qu'en Europe (segmentation B2B par taille/secteur)",
            ],
        },
        "tutorials": [
            {"id": "t1", "title": "Génère 4 personas data-driven en 30 minutes",
             "duration_min": 15, "format": "vidéo screencast"},
            {"id": "t2", "title": "Configure une audience custom Meta basée sur tes personas",
             "duration_min": 20, "format": "vidéo screencast"},
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
            "Le contexte marketing spécifique en Afrique du Nord, les pain "
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
    # MODULE 1 — Content Strategy Optimization
    # =========================================================================
    1: {
        # Unit 1 — Comprendre le problème business
        1: [
            {
                "title_fr": "Le quotidien de Sarah : 5 clients à gérer, contenu improvisé",
                "description_fr": (
                    "Étude de cas concrète : Sarah, content manager dans une agence "
                    "digitale à Casablanca, et son problème de production réactive "
                    "sans stratégie ni calendrier."
                ),
                "format": "case_study",
                "difficulty_level": 1,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Pain points des équipes marketing B2B/B2C en Afrique du Nord",
                "description_fr": (
                    "Les 6 pain points typiques : engagement < 2 %, pas de fil "
                    "narratif, sujets au feeling, pas de calendrier, mesure "
                    "difficile, burn-out créatif."
                ),
                "format": "video",
                "difficulty_level": 1,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Pattern temporel des KPIs : court / moyen / long terme",
                "description_fr": (
                    "Comprendre pourquoi on distingue KPIs de productivité (J+14), "
                    "qualité (J+14), et impact business (J+30/J+60 observatoire) "
                    "pour le contenu."
                ),
                "format": "video",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
        ],
        # Unit 2 — Compétences activées
        2: [
            {
                "title_fr": "Les 8 compétences de la stratégie de contenu IA",
                "description_fr": (
                    "Tour d'horizon des 8 compétences : brand voice, prompts par "
                    "persona, calendrier trimestriel, repurposing, mesure, "
                    "bibliothèque, pipeline, adaptation FR/AR."
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
                "title_fr": "Prompt 1 — Brand Voice Encoding (anatomie du prompt master)",
                "description_fr": (
                    "Décortique le Prompt 1 : variables MARQUE, ECHANTILLON_EDITORIAL, "
                    "génération du profil + do/don't + prompt master réutilisable."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Prompt 2 — Calendrier éditorial trimestriel",
                "description_fr": (
                    "Construire un calendrier 12 semaines avec 3 piliers, mix "
                    "70/20/10, saisonnalités Maghreb (Ramadan, rentrée, fêtes), "
                    "5 campagnes spéciales."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Prompt 3 — Repurposing multi-canal",
                "description_fr": (
                    "Décliner 1 contenu source en 5 formats : LinkedIn post, "
                    "carrousel, thread Twitter, newsletter, script Reel/TikTok. "
                    "Adaptation FR/AR mix si pertinent."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Workflow 1 — Production hebdo assistée IA (no-code)",
                "description_fr": (
                    "Pipeline no-code : Notion calendrier → ChatGPT brand voice → "
                    "Canva AI visuels → Buffer programmation. Setup 30-45 min. "
                    "Free tier compatible."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 20,
            },
            {
                "title_fr": "Workflow 2 — Pipeline content engine automatisé (low-code)",
                "description_fr": (
                    "Pipeline complet : Airtable trigger → OpenAI API génération → "
                    "Canva API visuel → Slack validation humaine → publication "
                    "automatique. Version low-cost Maghreb avec n8n."
                ),
                "format": "tutorial",
                "difficulty_level": 4,
                "estimated_duration_min": 25,
            },
        ],
        # Unit 4 — Mission terrain
        4: [
            {
                "title_fr": "Mission : Bâtis ton brand voice + calendrier éditorial du mois",
                "description_fr": (
                    "90 minutes chronométrées sur ta vraie marque. Critères : brand "
                    "voice encodée, calendrier du mois bâti avec saisonnalité "
                    "régionale, ≥ 2 contenus IA-augmentés publiés."
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
                    "Comment mesurer honnêtement ton temps de production actuel et "
                    "ton taux d'engagement avant tout changement. Formulaire intégré."
                ),
                "format": "exercise",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Mécanisme de relance J+7 / J+14 / J+30",
                "description_fr": (
                    "Comprendre pourquoi on mesure plusieurs fois : isoler l'effet du "
                    "module, distinguer effet ponctuel vs durable, attendre "
                    "l'observatoire pour le taux d'engagement."
                ),
                "format": "video",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Lecture du dashboard et recommandation suivante",
                "description_fr": (
                    "Lire ton comparatif baseline vs J+14, mettre à jour ton score "
                    "skill 'Stratégie et création de contenu IA', et choisir ton "
                    "prochain module."
                ),
                "format": "tutorial",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
        ],
    },

    # =========================================================================
    # MODULE 2 — Campaign Performance Optimization
    # =========================================================================
    2: {
        1: [
            {
                "title_fr": "Le quotidien de Yacine : CAC qui double en 2 mois",
                "description_fr": (
                    "Étude de cas : Yacine, growth marketer chez une PME e-commerce "
                    "à Tunis, et son problème de CAC qui passe de 25 TND à 45 TND "
                    "sans qu'il sache pourquoi."
                ),
                "format": "case_study",
                "difficulty_level": 1,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Pain points de l'acquisition payante en Afrique du Nord",
                "description_fr": (
                    "Les 6 pain points : CAC élevé, pas d'A/B test, créas lentes, "
                    "optimisation à l'intuition, scaling difficile, pas de "
                    "capitalisation."
                ),
                "format": "video",
                "difficulty_level": 1,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Pourquoi TikTok Ads est l'avantage régional sur les 18-35 ans",
                "description_fr": (
                    "Données et patterns culturels qui font de TikTok Ads une "
                    "plateforme avec un CAC souvent 30-50 % inférieur à Meta "
                    "sur la cible jeune en Afrique du Nord."
                ),
                "format": "video",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
        ],
        2: [
            {
                "title_fr": "Les 8 compétences de l'optimisation de campagnes IA",
                "description_fr": (
                    "Leviers (CTR/CPC/CVR/CAC/ROAS), génération ad copy, génération "
                    "visuels, A/B testing, lecture rapports, growth loop, "
                    "capitalisation, plateformes Maghreb."
                ),
                "format": "video",
                "difficulty_level": 2,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Du test au feeling à la growth loop structurée",
                "description_fr": (
                    "Différence entre 'j'ai testé un peu' (résultats non "
                    "exploitables) et une growth loop rigoureuse (variables "
                    "isolées, taille d'échantillon, règle de décision)."
                ),
                "format": "video",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
        ],
        3: [
            {
                "title_fr": "Prompt 1 — 10 variantes d'ad copy en 5 minutes",
                "description_fr": (
                    "Décortique le Prompt 1 : 10 angles publicitaires (douleur, "
                    "bénéfice, preuve, curiosité, urgence, avant/après, comparatif, "
                    "storytelling, stat, UGC) + adaptation langue FR/AR."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Prompt 2 — Brief visuel pour Midjourney / DALL-E",
                "description_fr": (
                    "Construire 3 briefs visuels (lifestyle / product hero / UGC) + "
                    "1 bonus Maghreb culturellement adapté. Cadrage des prompts "
                    "MJ/DALL-E en anglais."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Prompt 3 — Plan d'A/B test rigoureux",
                "description_fr": (
                    "Cadrer hypothèse, isoler la variable testée, définir KPI "
                    "primaire + secondaires, taille d'échantillon, règle de "
                    "décision, prochain test à lancer."
                ),
                "format": "tutorial",
                "difficulty_level": 4,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Workflow 1 — Sprint créatif hebdomadaire (no-code)",
                "description_fr": (
                    "Pipeline no-code : ChatGPT 10 ad copies → sélection 5 → "
                    "Midjourney 5 visuels → Meta Ads Manager split test → décision "
                    "à J+5. Setup 30-45 min."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 20,
            },
            {
                "title_fr": "Workflow 2 — Growth loop automatisée (low-code)",
                "description_fr": (
                    "Pipeline complet : Meta Ads API export hebdo → calcul winners/"
                    "losers → OpenAI API 5 variantes → AdCreative API 5 visuels → "
                    "Slack validation → mise en ligne automatique."
                ),
                "format": "tutorial",
                "difficulty_level": 4,
                "estimated_duration_min": 25,
            },
        ],
        4: [
            {
                "title_fr": "Mission : Lance un A/B test sur 5 nouvelles créas IA-augmentées",
                "description_fr": (
                    "120 minutes étalées sur 7 jours. Critères : 10 ad copies + "
                    "5 visuels en moins de 90 min, A/B test structuré lancé, "
                    "≥ 1 créa qui bat la baseline CAC de 10 % à J+7."
                ),
                "format": "exercise",
                "difficulty_level": 4,
                "estimated_duration_min": 120,
            },
        ],
        5: [
            {
                "title_fr": "Collecte baseline CAC et volume de créas testées",
                "description_fr": (
                    "Mesurer honnêtement ton CAC actuel et ton nombre de créas "
                    "testées par mois avant le module."
                ),
                "format": "exercise",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Bibliothèque personnelle des créas testées",
                "description_fr": (
                    "Conservation des top 5 créas par performance + insights par "
                    "angle. Réutilisation et amélioration continue."
                ),
                "format": "tutorial",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Mise à jour du score skill et recommandation suivante",
                "description_fr": (
                    "Si skill 3 (Audience Insights) < 67/100, recommandation "
                    "Module 3. Sinon : certificat AI Marketing Strategist."
                ),
                "format": "tutorial",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
        ],
    },

    # =========================================================================
    # MODULE 3 — Audience Insights & Segmentation
    # =========================================================================
    3: {
        1: [
            {
                "title_fr": "Le quotidien de Lina : 25 000 clients, ciblage 'femmes 25-45 ans'",
                "description_fr": (
                    "Étude de cas : Lina, marketing manager d'une marque cosmétique "
                    "au Maroc, qui cible 'tout le monde' faute de personas et voit "
                    "son ROAS stagner."
                ),
                "format": "case_study",
                "difficulty_level": 1,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Pain points du ciblage en Afrique du Nord",
                "description_fr": (
                    "Les 6 pain points : ciblage médiocre, messages génériques, "
                    "personas intuitifs, pas de personnalisation, données sous-"
                    "exploitées, cycle de vie mal compris."
                ),
                "format": "video",
                "difficulty_level": 1,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Spécificités Maghreb : multilinguisme, diaspora, saisonnalités",
                "description_fr": (
                    "Pourquoi ces 3 dimensions changent la segmentation en Afrique "
                    "du Nord — multilinguisme FR/AR/darija, diaspora à fort "
                    "pouvoir d'achat, Ramadan/Aïd."
                ),
                "format": "video",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
        ],
        2: [
            {
                "title_fr": "Les 8 compétences de l'audience intelligence IA",
                "description_fr": (
                    "Frameworks (RFM, behavioral, psychographique), extraction "
                    "multi-sources, clustering IA, adaptation messaging, audiences "
                    "custom, mesure pertinence, boucle continue, spécificités Maghreb."
                ),
                "format": "video",
                "difficulty_level": 2,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Du persona intuitif au persona data-driven",
                "description_fr": (
                    "Différence fondamentale entre un avatar inventé (1 ou 2 "
                    "intuitions) et un persona extrait de signaux comportementaux "
                    "réels (RFM + intérêts + parcours d'achat)."
                ),
                "format": "video",
                "difficulty_level": 3,
                "estimated_duration_min": 10,
            },
        ],
        3: [
            {
                "title_fr": "Prompt 1 — Personas data-driven (9 dimensions par persona)",
                "description_fr": (
                    "Générer 4-6 personas avec : nom évocateur, démographie, pain "
                    "points, motivations, canaux, tonalité, messages clés, % base, "
                    "recommandation d'activation."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Prompt 2 — Segmentation comportementale RFM",
                "description_fr": (
                    "Définir les seuils RFM adaptés à ton business, identifier les "
                    "6 segments prioritaires (Champions, Loyaux, Potentiels, "
                    "À risque, Hibernants, Perdus) avec actions et budgets."
                ),
                "format": "tutorial",
                "difficulty_level": 4,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Prompt 3 — Activation par persona (messaging adapté)",
                "description_fr": (
                    "Décliner 1 message produit en 4 versions adaptées chacune à un "
                    "persona spécifique (hook, bénéfice, preuve, objection, CTA, "
                    "format publicitaire)."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 15,
            },
            {
                "title_fr": "Workflow 1 — Audit personas trimestriel (no-code)",
                "description_fr": (
                    "Pipeline no-code : export CRM/GA4 → échantillon 50 lignes → "
                    "Prompt 1 → validation équipe → documentation Notion → "
                    "audiences custom Meta. Setup 30-60 min."
                ),
                "format": "tutorial",
                "difficulty_level": 3,
                "estimated_duration_min": 20,
            },
            {
                "title_fr": "Workflow 2 — Audience intelligence en continu (low-code)",
                "description_fr": (
                    "Pipeline complet : Make sync CRM+GA4+Meta → BigQuery RFM → "
                    "détection segments émergents → OpenAI génération → Slack "
                    "insights → mise à jour audiences custom Meta API."
                ),
                "format": "tutorial",
                "difficulty_level": 4,
                "estimated_duration_min": 25,
            },
        ],
        4: [
            {
                "title_fr": "Mission : 4 personas data-driven + 1 campagne ciblée",
                "description_fr": (
                    "90 minutes étalées sur la semaine. Critères : 4 personas "
                    "documentés, 1 campagne ciblée lancée, taux de conversion "
                    "≥ 15 % supérieur à la campagne large équivalente."
                ),
                "format": "exercise",
                "difficulty_level": 4,
                "estimated_duration_min": 90,
            },
        ],
        5: [
            {
                "title_fr": "Collecte baseline nb personas et taux de conversion",
                "description_fr": (
                    "Mesurer ton nombre de personas actuels (souvent 1-2) et ton "
                    "taux de conversion habituel sur les campagnes larges."
                ),
                "format": "exercise",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Bibliothèque personnelle de personas avec messaging",
                "description_fr": (
                    "Conservation et amélioration continue de tes personas "
                    "data-driven et de leur messaging adapté. Mise à jour "
                    "trimestrielle recommandée."
                ),
                "format": "tutorial",
                "difficulty_level": 2,
                "estimated_duration_min": 10,
            },
            {
                "title_fr": "Vue consolidée des 3 modules : parcours complet",
                "description_fr": (
                    "Synthèse de ton parcours AI Marketing Strategist : scores des "
                    "3 skills, KPIs avant/après, certificat, et bridge commercial."
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
def seed_ai_marketing_strategist_modules(db):
    """
    Seed les 3 modules + 15 units + ~45 lessons + jointures module_skills
    pour le rôle AI Marketing Strategist.

    Source : PDF v1.0 — Avril 2026.

    Idempotent : skip si déjà seedé (vérifie l'existence d'un module
    avec role='AI Marketing Strategist' avant de continuer).

    Pré-requis : seed_ai_marketing_strategist_diagnostic.py doit avoir été
    exécuté avant (il crée les 3 skills 'Stratégie et création de contenu IA',
    'Optimisation de campagnes et growth IA', 'Audience intelligence et
    segmentation IA' référencées par skill_name dans MODULE_*).
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
            f"⚠️  AI Marketing Strategist modules déjà seedés "
            f"({existing_modules} modules pour role='{ROLE}'), skip."
        )
        return

    # =========================================================================
    # 1. Récupérer les skills (seedées par seed_ai_marketing_strategist_diagnostic.py)
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
                f"Lance d'abord seed_ai_marketing_strategist_diagnostic.py."
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
        f"✅ AI Marketing Strategist modules seedés :\n"
        f"   • {len(MODULES)} modules (role='{ROLE}')\n"
        f"   • {total_units_created} units (5 par module)\n"
        f"   • {total_lessons_created} lessons (~3 par unit)\n"
        f"   • {total_module_skill_links} jointures module_skills"
    )