"""
Seed AI Marketing Strategist — Modules pédagogiques (refactoré v1.1)

Charge le contenu depuis content/roles/ai_marketing_strategist/module_*.json
(architecture Option 3 — JSON externe comme source de vérité).

Contenu pédagogique des 3 modules du parcours AI Marketing Strategist :
- Module 1 : Content Strategy Optimization
- Module 2 : Campaign Performance Optimization
- Module 3 : Audience Insights & Segmentation

Source : PDF Parcours AI Marketing Strategist v1.1 — Mai 2026.

Architecture pédagogique : chaque module est structuré en 5 unités logiques
qui regroupent les 7 sections du PDF (Use Case, KPI, Skills, Execution Content,
Execution Task, KPI Measurement, Progress Update).

Refactor : le contenu pédagogique (MODULE_1/2/3) est externalisé dans des
fichiers JSON content/roles/ai_marketing_strategist/module_*.json. Ce script
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
ROLE = "AI Marketing Strategist"
CAREER_PATH_ID = 80
ROLE_SLUG = "ai_marketing_strategist"


# =============================================================================
# UNITS — 5 unités par module (total : 15)
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
# LESSONS — Préservé tel quel depuis le seed original Marketing
# Structure : LESSONS_BY_MODULE[module_display_order][unit_order] = [list of lessons]
# =============================================================================
LESSONS_BY_MODULE = {
    # =========================================================================
    # MODULE 1 — Content Strategy Optimization
    # =========================================================================
    1: {
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
    Seed les 3 modules + 15 units + 42 lessons + jointures module_skills
    pour le rôle AI Marketing Strategist.

    Charge le contenu des modules depuis
    content/roles/ai_marketing_strategist/ (architecture Option 3).

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
            f"⚠️  AI Marketing Strategist modules déjà seedés "
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
                f"Lance d'abord seed_ai_marketing_strategist_diagnostic.py."
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
        f"✅ AI Marketing Strategist modules seedés (depuis JSON) :\n"
        f"   • {len(modules_data)} modules (role='{ROLE}')\n"
        f"   • {total_units_created} units (5 par module)\n"
        f"   • {total_lessons_created} lessons\n"
        f"   • {total_module_skill_links} jointures module_skills"
    )
