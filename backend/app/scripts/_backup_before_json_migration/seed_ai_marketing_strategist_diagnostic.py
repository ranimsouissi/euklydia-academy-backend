"""
Seed AI Marketing Strategist — Euklydia Academy v2.0

Contenu pédagogique du diagnostic AI Marketing Strategist :
- 3 skills (logique 1 skill = 1 module)
- 9 questions QCM (3 par skill : Connaissance / Application / Maîtrise)

Aligné sur le pattern de seed_ai_sales_specialist_diagnostic.py
(noms d'outils neutralisés en architectures génériques, distracteurs renforcés,
explications pédagogiques, contextualisation Afrique du Nord).

Career path : AI Marketing Strategist (id=80).

Idempotent : skip si déjà seedé (pattern aligné sur seed_career_paths.py).
"""
from sqlalchemy import text
from app.models.skill import Skill
from app.models.question import Question


CAREER_PATH_ID = 80  # AI Marketing Strategist


# =============================================================================
# Skills — 3 compétences cœur (logique 1 skill = 1 module)
# =============================================================================
SKILLS = [
    {
        "name": "Stratégie et création de contenu IA",
        "description": (
            "Capacité à utiliser l'IA pour concevoir une stratégie éditoriale, encoder "
            "une brand voice et produire du contenu cohérent multi-canal (blog, "
            "LinkedIn, newsletter, réseaux sociaux). Compétence couvrant 8 axes : "
            "définition de brand voice, prompts structurés par persona, calendrier "
            "éditorial trimestriel, repurposing multi-canal, mesure d'engagement, "
            "bibliothèque de prompts versionnée, pipeline de production semi-automatisé, "
            "et adaptation bilingue (FR/AR) Afrique du Nord."
        ),
    },
    {
        "name": "Optimisation de campagnes et growth IA",
        "description": (
            "Capacité à concevoir, déployer et optimiser des campagnes publicitaires "
            "multi-plateformes (Meta Ads, Google Ads, TikTok Ads) avec l'IA, en visant "
            "la baisse du CAC et l'amélioration du ROAS. Compétence couvrant 8 axes : "
            "leviers d'optimisation (CTR/CPC/CVR/CAC/ROAS), génération de variantes "
            "d'ad copy, génération de visuels IA, A/B testing rigoureux, lecture des "
            "rapports de performance, growth loop d'apprentissage continu, "
            "capitalisation des insights gagnants, et adaptation aux plateformes "
            "dominantes Afrique du Nord."
        ),
    },
    {
        "name": "Audience intelligence et segmentation IA",
        "description": (
            "Capacité à analyser une base utilisateurs, générer des personas data-driven "
            "et segmenter l'audience pour personnaliser messages et campagnes. "
            "Compétence couvrant 8 axes : frameworks de segmentation (RFM, "
            "comportementale, psychographique), extraction de données multi-sources "
            "(CRM/GA4/Meta), construction de personas par clustering IA, adaptation du "
            "messaging par persona, configuration d'audiences personnalisées, mesure "
            "de la pertinence du ciblage, boucle d'apprentissage continu, et "
            "spécificités culturelles Afrique du Nord."
        ),
    },
]


# =============================================================================
# Questions — 9 QCM (3 par skill : Connaissance / Application / Maîtrise)
# Les questions sont indexées par position dans SKILLS (0=skill 1, 1=skill 2, 2=skill 3)
# =============================================================================
QUESTIONS = [
    # =========================================================================
    # Skill 1 — Stratégie et création de contenu IA
    # =========================================================================
    {
        "skill_index": 0,  # Stratégie et création de contenu IA
        "order": 1,
        "text": "Qu'est-ce qu'une « brand voice » dans un contexte de marketing de contenu IA ?",
        "option_a": "Le ton de la voix utilisé dans les publicités audio et vidéo",
        "option_b": (
            "L'identité éditoriale d'une marque (ton, vocabulaire, style) qu'on encode "
            "dans l'IA pour produire du contenu cohérent à grande échelle"
        ),
        "option_c": "Le nom du compte officiel d'une marque sur les réseaux sociaux",
        "option_d": "La signature sonore (jingle) associée à une marque",
        "correct_answer": "B",
        "explanation": (
            "La brand voice est l'identité éditoriale codifiée d'une marque (ton, "
            "vocabulaire, style, do/don't) qu'on encode dans des prompts IA réutilisables "
            "pour garantir la cohérence de tous les contenus produits. Ce n'est ni un "
            "élément audio, ni un identifiant de compte, ni un jingle."
        ),
    },
    {
        "skill_index": 0,
        "order": 2,
        "text": (
            "Tu dois publier 4 articles de blog par mois pour une marque B2B en Afrique "
            "du Nord. Quelle est la méthode la plus efficace avec l'IA ?"
        ),
        "option_a": "Demander à ChatGPT « écris-moi un article sur le marketing digital »",
        "option_b": (
            "Construire un calendrier éditorial trimestriel, créer des prompts "
            "structurés par persona et thème, puis itérer en révision humaine"
        ),
        "option_c": "Reformuler des articles de concurrents avec un outil de paraphrase",
        "option_d": "Écrire les 4 articles à la main sans IA pour garantir la qualité",
        "correct_answer": "B",
        "explanation": (
            "L'approche structurée combine (1) un calendrier éditorial qui aligne le "
            "contenu sur les objectifs business, (2) des prompts par persona/thème "
            "pour garantir la pertinence, et (3) une révision humaine pour la qualité. "
            "Les prompts vagues produisent du contenu générique, la reformulation pose "
            "des problèmes éthiques et SEO, et l'écriture 100% manuelle ne scale pas."
        ),
    },
    {
        "skill_index": 0,
        "order": 3,
        "text": (
            "Tu veux industrialiser la production de contenu (blog + LinkedIn + "
            "newsletter) avec une ligne éditoriale cohérente et un calendrier "
            "auto-piloté. Quelle architecture est la plus robuste à long terme ?"
        ),
        "option_a": "Tout faire manuellement chaque lundi sur un outil de gestion de tâches",
        "option_b": "Utiliser uniquement les templates par défaut d'un outil de design graphique",
        "option_c": (
            "Combiner une bibliothèque de prompts versionnée par persona, un système "
            "qui ancre la brand voice dans la génération, un calendrier éditorial "
            "automatisé et une revue humaine systématique"
        ),
        "option_d": "Externaliser à un freelance et abandonner l'usage de l'IA",
        "correct_answer": "C",
        "explanation": (
            "Une architecture robuste combine 4 composants : (1) bibliothèque de prompts "
            "versionnée par persona pour la reproductibilité, (2) ancrage de la brand "
            "voice dans la génération pour la cohérence, (3) calendrier éditorial "
            "automatisé pour la cadence, (4) revue humaine pour la qualité. Les autres "
            "options sont soit non-scalables, soit incohérentes avec une stratégie IA."
        ),
    },
    # =========================================================================
    # Skill 2 — Optimisation de campagnes et growth IA
    # =========================================================================
    {
        "skill_index": 1,  # Optimisation de campagnes et growth IA
        "order": 1,
        "text": "Que signifie CAC dans un contexte de campagne marketing ?",
        "option_a": "Coût d'Affichage Cumulé sur les plateformes publicitaires",
        "option_b": (
            "Coût d'Acquisition Client : montant moyen dépensé en publicité pour "
            "acquérir un nouveau client"
        ),
        "option_c": "Conversion d'Audience Ciblée : taux de transformation d'une audience",
        "option_d": "Cost Adjustment Calculation : ajustement automatique des enchères",
        "correct_answer": "B",
        "explanation": (
            "Le CAC (Coût d'Acquisition Client) est l'indicateur clé de l'efficacité "
            "d'une campagne d'acquisition : total dépensé / nombre de clients acquis. "
            "C'est le KPI principal à optimiser en growth marketing, à mettre en regard "
            "de la LTV (Lifetime Value) pour évaluer la rentabilité."
        ),
    },
    {
        "skill_index": 1,
        "order": 2,
        "text": (
            "Ta campagne d'acquisition payante a un CAC élevé (60% au-dessus de ta "
            "cible). Quelle approche IA est la plus efficace pour le réduire ?"
        ),
        "option_a": "Augmenter le budget pour compenser le CAC élevé par le volume",
        "option_b": (
            "Lancer un A/B test multi-créa avec 5+ variantes générées par IA "
            "(angles, accroches, visuels), couper les sous-performantes et scaler "
            "les gagnantes"
        ),
        "option_c": "Garder la même créa et changer uniquement le ciblage de l'audience",
        "option_d": "Arrêter immédiatement la campagne payante et basculer 100% en SEO",
        "correct_answer": "B",
        "explanation": (
            "Un CAC élevé est souvent dû à l'usure créative ou à un mauvais "
            "product-market-message fit. La solution est d'industrialiser le test "
            "créatif avec l'IA : générer plusieurs angles, tester rigoureusement, "
            "scaler les gagnants. Augmenter le budget aggrave le problème, changer "
            "uniquement l'audience néglige la créa, et arrêter le payant est une "
            "réaction excessive."
        ),
    },
    {
        "skill_index": 1,
        "order": 3,
        "text": (
            "Tu veux mettre en place une « growth loop » IA qui génère, teste et "
            "optimise les créas publicitaires en continu. Quelle architecture est "
            "nécessaire ?"
        ),
        "option_a": "Un tableur partagé avec envoi manuel des créas chaque vendredi",
        "option_b": "Uniquement les outils natifs de la plateforme publicitaire",
        "option_c": (
            "Une stack combinant : (1) génération IA d'ad copy et de visuels, "
            "(2) déploiement automatique sur les plateformes publicitaires, "
            "(3) collecte des données de performance, (4) boucle d'apprentissage "
            "qui réinjecte les insights gagnants dans la génération suivante"
        ),
        "option_d": "Un graphiste freelance produisant 50 visuels par mois sans IA",
        "correct_answer": "C",
        "explanation": (
            "Une growth loop industrielle nécessite 4 composants : génération IA "
            "(texte + visuel) pour la quantité, déploiement automatique pour la "
            "vitesse, collecte des performances pour la mesure, et boucle "
            "d'apprentissage pour capitaliser sur les gagnants. Les processus "
            "manuels et les outils isolés ne permettent pas l'itération continue à "
            "grande échelle."
        ),
    },
    # =========================================================================
    # Skill 3 — Audience intelligence et segmentation IA
    # =========================================================================
    {
        "skill_index": 2,  # Audience intelligence et segmentation IA
        "order": 1,
        "text": "Qu'est-ce qu'un persona marketing « data-driven » ?",
        "option_a": "Un avatar fictif inventé à partir de l'intuition de l'équipe marketing",
        "option_b": (
            "Une représentation synthétique d'un segment client construite à partir de "
            "données réelles (analytics, CRM, feedback) et enrichie par l'IA"
        ),
        "option_c": "Le profil démographique du fondateur de l'entreprise",
        "option_d": "La page « À propos » du site web de la marque",
        "correct_answer": "B",
        "explanation": (
            "Un persona data-driven est construit à partir de données comportementales "
            "réelles (analytics, CRM, feedback client) et enrichi par l'IA pour générer "
            "une représentation actionnable d'un segment. Il s'oppose au persona "
            "intuitif (option A) qui repose sur des hypothèses non vérifiées."
        ),
    },
    {
        "skill_index": 2,
        "order": 2,
        "text": (
            "Tu as 10 000 utilisateurs dans ta base mais ton ciblage publicitaire est "
            "imprécis. Comment l'IA peut-elle améliorer ta segmentation ?"
        ),
        "option_a": "Cibler tout le monde de manière identique pour maximiser le reach",
        "option_b": (
            "Faire une segmentation comportementale (recency, frequency, monetary + "
            "centres d'intérêt) avec un LLM qui traduit la donnée en personas "
            "actionnables"
        ),
        "option_c": "Segmenter uniquement par tranche d'âge et zone géographique",
        "option_d": "Acheter une base externe enrichie sans la qualifier au préalable",
        "correct_answer": "B",
        "explanation": (
            "Une segmentation efficace combine signaux comportementaux (RFM : Recency, "
            "Frequency, Monetary) et signaux d'intérêt, traduits par un LLM en personas "
            "actionnables avec messaging adapté. Le ciblage uniforme dilue le budget, "
            "la segmentation démographique seule est trop grossière, et l'achat de "
            "bases externes pose des problèmes de qualité et de conformité."
        ),
    },
    {
        "skill_index": 2,
        "order": 3,
        "text": (
            "Tu veux déployer un système d'audience intelligence en continu qui détecte "
            "automatiquement les nouveaux segments à fort potentiel. Quelles "
            "capacités doit-il avoir ?"
        ),
        "option_a": "Un export CSV trimestriel des données utilisateurs",
        "option_b": "Uniquement les rapports natifs d'un outil d'analytics web",
        "option_c": (
            "Une stack combinant : (1) connexion continue aux sources (CRM + analytics + "
            "plateformes pub), (2) clustering IA pour détecter les segments émergents, "
            "(3) génération automatique de personas et de recommandations, "
            "(4) synchronisation des audiences vers les plateformes publicitaires"
        ),
        "option_d": "Un formulaire de 50 questions à faire remplir à chaque utilisateur",
        "correct_answer": "C",
        "explanation": (
            "Un système d'audience intelligence en continu nécessite 4 composants : "
            "connexion multi-sources pour la donnée fraîche, clustering IA pour la "
            "détection automatique de segments, génération de personas pour "
            "l'actionabilité, et synchronisation vers les plateformes pub pour "
            "l'activation. Les approches ponctuelles ou unilatérales ne permettent "
            "pas la détection en temps réel des opportunités émergentes."
        ),
    },
]


def seed_ai_marketing_strategist_diagnostic(db):
    """
    Seed les 3 skills + 9 questions du diagnostic AI Marketing Strategist v2.

    Idempotent : skip si déjà seedé.
    """
    # =========================================================================
    # 0. Anti-doublon — skip si déjà seedé
    # =========================================================================
    existing_skills = (
        db.query(Skill)
        .filter(Skill.career_path_id == CAREER_PATH_ID)
        .count()
    )
    if existing_skills >= len(SKILLS):
        print(
            f"⚠️  AI Marketing Strategist déjà seedé "
            f"({existing_skills} skills sur career_path {CAREER_PATH_ID}), skip."
        )
        return

    # =========================================================================
    # 1. Insérer les 3 skills
    # =========================================================================
    skill_objects = []
    for skill_data in SKILLS:
        # Vérifier si la skill existe déjà (au cas par cas, en plus du check global)
        existing_skill = (
            db.query(Skill)
            .filter(
                Skill.name == skill_data["name"],
                Skill.career_path_id == CAREER_PATH_ID,
            )
            .first()
        )
        if existing_skill:
            skill_objects.append(existing_skill)
            continue

        skill = Skill(
            name=skill_data["name"],
            description=skill_data["description"],
            career_path_id=CAREER_PATH_ID,
        )
        db.add(skill)
        skill_objects.append(skill)

    # Flush pour obtenir les IDs auto-générés des skills
    db.flush()

    # =========================================================================
    # 2. Insérer les 9 questions (3 par skill)
    # =========================================================================
    for question_data in QUESTIONS:
        skill = skill_objects[question_data["skill_index"]]

        # Vérifier si la question existe déjà (par texte + skill_id)
        existing_question = (
            db.query(Question)
            .filter(
                Question.text == question_data["text"],
                Question.skill_id == skill.id,
            )
            .first()
        )
        if existing_question:
            continue

        question = Question(
            text=question_data["text"],
            option_a=question_data["option_a"],
            option_b=question_data["option_b"],
            option_c=question_data["option_c"],
            option_d=question_data["option_d"],
            correct_answer=question_data["correct_answer"],
            explanation=question_data["explanation"],
            order=question_data["order"],
            skill_id=skill.id,
        )
        db.add(question)

    db.flush()

    print(
        f"✅ AI Marketing Strategist seedé : "
        f"{len(SKILLS)} skills + {len(QUESTIONS)} questions "
        f"(career_path {CAREER_PATH_ID})"
    )