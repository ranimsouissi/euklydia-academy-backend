# =============================
# Seuils de score (0-100)
# =============================
HIGH_MAX = 49    # score <= 49  → High priority  → Niveau Débutant
MED_MAX = 74     # score <= 74  → Medium priority → Niveau Intermédiaire
                 # score >= 75  → Low priority   → Niveau Avancé

PRIORITY_ORDER = {
    "High": 0,
    "Medium": 1,
    "Low": 2,
}

# =============================
# Rôles disponibles
# =============================
ROLE_IDS = {
    "ai_sales_specialist":      79,
    "ai_marketing_strategist":  80,
    "ai_designer":              81,
    "ai_project_manager":       82,
}


def get_level(score: int) -> str:
    """
    Retourne le NIVEAU DE MAÎTRISE DE L'APPRENANT (Débutant / Intermédiaire / Avancé).
    
    Ce niveau est différent du niveau de difficulté d'un module (Fondation / Pratique / Expert).
    Voir get_recommended_module_level() pour le niveau de module recommandé.
    """
    if score <= HIGH_MAX:
        return "Débutant"
    if score <= MED_MAX:
        return "Intermédiaire"
    return "Avancé"


def get_priority(score: int) -> str:
    if score <= HIGH_MAX:
        return "High"
    if score <= MED_MAX:
        return "Medium"
    return "Low"


def get_recommended_module_level(score: int) -> str:
    """
    Retourne le NIVEAU DE MODULE recommandé en fonction du score apprenant.
    
    ⚠️ Valeurs retournées en FRANÇAIS pour matcher la valeur stockée dans
    Module.level en DB (Fondation / Pratique / Expert).
    
    Mapping :
      - Score <= 49 (apprenant Débutant)      → Module Fondation
      - Score 50-74 (apprenant Intermédiaire) → Module Pratique
      - Score >= 75 (apprenant Avancé)         → Module Expert
    """
    if score <= HIGH_MAX:
        return "Fondation"
    if score <= MED_MAX:
        return "Pratique"
    return "Expert"


# =============================
# Profils par rôle — Dashboard (Use Case-Driven)
# =============================
# Descriptions repositionnées sur les 3 use cases business + KPIs mesurables.
# Aligné avec le positionnement "Use case-driven AI learning" de la plateforme.

ROLE_PROFILES = {

    # ── AI Sales Specialist (role_id=79) ─────────────────────────────────────
    "ai_sales_specialist": {
        "role_fr": "AI Sales Specialist",
        "role_en": "AI Sales Specialist",
        "novice": {
            "profile": "AI Novice",
            "profile_fr": "Novice IA",
            "description_fr": (
                "En tant que AI Sales Specialist débutant, vous découvrez vos 3 use cases "
                "business. Activez vos premiers AI Blueprints pour transformer votre approche "
                "commerciale : +25–40% de leads qualifiés, 2–3x de taux de réponse, "
                "et +15–25% de taux de closing."
            ),
            "description_en": (
                "As a beginner AI Sales Specialist, you are discovering your 3 business use cases. "
                "Activate your first AI Blueprints to transform your sales approach: "
                "+25–40% qualified leads, 2–3x reply rate, and +15–25% close rate."
            ),
            "cta_fr": "Voir ma Feuille de route IA →",
            "cta_en": "View my AI Roadmap →",
        },
        "practitioner": {
            "profile": "AI Practitioner",
            "profile_fr": "Praticien IA",
            "description_fr": (
                "En tant que AI Sales Specialist praticien, vous maîtrisez les fondamentaux "
                "de vos 3 use cases business. Activez vos AI Blueprints pour passer "
                "de la pratique à la maîtrise : +25–40% de leads qualifiés, 2–3x de taux "
                "de réponse, et +15–25% de taux de closing."
            ),
            "description_en": (
                "As a practitioner AI Sales Specialist, you have mastered the fundamentals "
                "of your 3 business use cases. Activate your AI Blueprints to move from "
                "practice to mastery: +25–40% qualified leads, 2–3x reply rate, "
                "and +15–25% close rate."
            ),
            "cta_fr": "Voir ma Feuille de route IA →",
            "cta_en": "View my AI Roadmap →",
        },
        "leader": {
            "profile": "AI Leader",
            "profile_fr": "Leader IA",
            "description_fr": (
                "En tant que AI Sales Specialist leader, vous êtes en avance sur vos 3 use cases "
                "business. Systématisez vos AI Blueprints et coachez votre équipe pour atteindre "
                "+25–40% de leads qualifiés, 2–3x de taux de réponse, et +15–25% "
                "de taux de closing à l'échelle de votre organisation."
            ),
            "description_en": (
                "As a leader AI Sales Specialist, you are ahead on your 3 business use cases. "
                "Systematize your AI Blueprints and coach your team to achieve +25–40% "
                "qualified leads, 2–3x reply rate, and +15–25% close rate "
                "at the scale of your organization."
            ),
            "cta_fr": "Voir ma Feuille de route IA →",
            "cta_en": "View my AI Roadmap →",
        },
    },

    # ── AI Marketing Strategist (role_id=80) ─────────────────────────────────
    "ai_marketing_strategist": {
        "role_fr": "AI Marketing Strategist",
        "role_en": "AI Marketing Strategist",
        "novice": {
            "profile": "AI Novice",
            "profile_fr": "Novice IA",
            "description_fr": (
                "En tant que AI Marketing Strategist débutant, vous découvrez vos 3 use cases "
                "business. Activez vos premiers AI Blueprints pour transformer votre marketing : "
                "+30–50% d'engagement, -20–30% de CAC, et +25% de conversion."
            ),
            "description_en": (
                "As a beginner AI Marketing Strategist, you are discovering your 3 business "
                "use cases. Activate your first AI Blueprints to transform your marketing: "
                "+30–50% engagement, -20–30% CAC, and +25% conversion."
            ),
            "cta_fr": "Voir ma Feuille de route IA →",
            "cta_en": "View my AI Roadmap →",
        },
        "practitioner": {
            "profile": "AI Practitioner",
            "profile_fr": "Praticien IA",
            "description_fr": (
                "En tant que AI Marketing Strategist praticien, vous maîtrisez les fondamentaux "
                "de vos 3 use cases business. Activez vos AI Blueprints pour passer "
                "de la pratique à la maîtrise : +30–50% d'engagement, -20–30% de CAC, "
                "et +25% de conversion."
            ),
            "description_en": (
                "As a practitioner AI Marketing Strategist, you have mastered the fundamentals "
                "of your 3 business use cases. Activate your AI Blueprints to move from practice "
                "to mastery: +30–50% engagement, -20–30% CAC, and +25% conversion."
            ),
            "cta_fr": "Voir ma Feuille de route IA →",
            "cta_en": "View my AI Roadmap →",
        },
        "leader": {
            "profile": "AI Leader",
            "profile_fr": "Leader IA",
            "description_fr": (
                "En tant que AI Marketing Strategist leader, vous êtes en avance sur vos "
                "3 use cases business. Systématisez vos AI Blueprints et coachez votre équipe "
                "pour atteindre +30–50% d'engagement, -20–30% de CAC, et +25% de conversion "
                "à l'échelle de votre organisation."
            ),
            "description_en": (
                "As a leader AI Marketing Strategist, you are ahead on your 3 business use cases. "
                "Systematize your AI Blueprints and coach your team to achieve +30–50% engagement, "
                "-20–30% CAC, and +25% conversion at the scale of your organization."
            ),
            "cta_fr": "Voir ma Feuille de route IA →",
            "cta_en": "View my AI Roadmap →",
        },
    },

    # ── AI Designer (role_id=81) ──────────────────────────────────────────────
    "ai_designer": {
        "role_fr": "AI Designer",
        "role_en": "AI Designer",
        "novice": {
            "profile": "AI Novice",
            "profile_fr": "Novice IA",
            "description_fr": (
                "En tant que AI Designer débutant, vous découvrez vos 3 use cases business. "
                "Activez vos premiers AI Blueprints pour transformer votre process créatif : "
                "5x faster ideation, +20–30% d'engagement UX, et +40% de consistency "
                "sur votre design system."
            ),
            "description_en": (
                "As a beginner AI Designer, you are discovering your 3 business use cases. "
                "Activate your first AI Blueprints to transform your creative process: "
                "5x faster ideation, +20–30% UX engagement, and +40% consistency "
                "across your design system."
            ),
            "cta_fr": "Voir ma Feuille de route IA →",
            "cta_en": "View my AI Roadmap →",
        },
        "practitioner": {
            "profile": "AI Practitioner",
            "profile_fr": "Praticien IA",
            "description_fr": (
                "En tant que AI Designer praticien, vous maîtrisez les fondamentaux "
                "de vos 3 use cases business. Activez vos AI Blueprints pour passer "
                "de la pratique à la maîtrise : 5x faster ideation, +20–30% d'engagement UX, "
                "et +40% de consistency sur votre design system."
            ),
            "description_en": (
                "As a practitioner AI Designer, you have mastered the fundamentals of your "
                "3 business use cases. Activate your AI Blueprints to move from practice to "
                "mastery: 5x faster ideation, +20–30% UX engagement, and +40% consistency "
                "across your design system."
            ),
            "cta_fr": "Voir ma Feuille de route IA →",
            "cta_en": "View my AI Roadmap →",
        },
        "leader": {
            "profile": "AI Leader",
            "profile_fr": "Leader IA",
            "description_fr": (
                "En tant que AI Designer leader, vous êtes en avance sur vos 3 use cases business. "
                "Systématisez vos AI Blueprints et coachez votre équipe créative pour atteindre "
                "5x faster ideation, +20–30% d'engagement UX, et +40% de consistency "
                "à l'échelle de votre organisation."
            ),
            "description_en": (
                "As a leader AI Designer, you are ahead on your 3 business use cases. "
                "Systematize your AI Blueprints and coach your creative team to achieve "
                "5x faster ideation, +20–30% UX engagement, and +40% consistency "
                "at the scale of your organization."
            ),
            "cta_fr": "Voir ma Feuille de route IA →",
            "cta_en": "View my AI Roadmap →",
        },
    },

    # ── AI Project Manager (role_id=82) ──────────────────────────────────────
    "ai_project_manager": {
        "role_fr": "AI Project Manager",
        "role_en": "AI Project Manager",
        "novice": {
            "profile": "AI Novice",
            "profile_fr": "Novice IA",
            "description_fr": (
                "En tant que AI Project Manager débutant, vous découvrez vos 3 use cases "
                "business. Activez vos premiers AI Blueprints pour transformer votre delivery : "
                "50–70% de temps économisé sur le planning, -30% de retards, "
                "et +25% de productivité d'équipe."
            ),
            "description_en": (
                "As a beginner AI Project Manager, you are discovering your 3 business use cases. "
                "Activate your first AI Blueprints to transform your delivery: 50–70% time saved "
                "on planning, -30% delays, and +25% team productivity."
            ),
            "cta_fr": "Voir ma Feuille de route IA →",
            "cta_en": "View my AI Roadmap →",
        },
        "practitioner": {
            "profile": "AI Practitioner",
            "profile_fr": "Praticien IA",
            "description_fr": (
                "En tant que AI Project Manager praticien, vous maîtrisez les fondamentaux "
                "de vos 3 use cases business. Activez vos AI Blueprints pour passer "
                "de la pratique à la maîtrise : 50–70% de temps économisé sur le planning, "
                "-30% de retards, et +25% de productivité d'équipe."
            ),
            "description_en": (
                "As a practitioner AI Project Manager, you have mastered the fundamentals "
                "of your 3 business use cases. Activate your AI Blueprints to move from practice "
                "to mastery: 50–70% time saved on planning, -30% delays, and +25% team productivity."
            ),
            "cta_fr": "Voir ma Feuille de route IA →",
            "cta_en": "View my AI Roadmap →",
        },
        "leader": {
            "profile": "AI Leader",
            "profile_fr": "Leader IA",
            "description_fr": (
                "En tant que AI Project Manager leader, vous êtes en avance sur vos 3 use cases "
                "business. Systématisez vos AI Blueprints et coachez votre équipe pour atteindre "
                "50–70% de temps économisé sur le planning, -30% de retards, et +25% "
                "de productivité à l'échelle de votre organisation."
            ),
            "description_en": (
                "As a leader AI Project Manager, you are ahead on your 3 business use cases. "
                "Systematize your AI Blueprints and coach your team to achieve 50–70% time saved "
                "on planning, -30% delays, and +25% productivity at the scale of your organization."
            ),
            "cta_fr": "Voir ma Feuille de route IA →",
            "cta_en": "View my AI Roadmap →",
        },
    },
}


def get_profile_summary(global_score: float, role_key: str) -> dict:
    """
    Retourne le profil simplifié pour le Dashboard.
    Basé sur le score global ET le rôle de l'apprenant.
    """
    role_data = ROLE_PROFILES.get(role_key, ROLE_PROFILES["ai_marketing_strategist"])

    if global_score <= HIGH_MAX:
        level_key = "novice"
    elif global_score <= MED_MAX:
        level_key = "practitioner"
    else:
        level_key = "leader"

    profile = role_data[level_key].copy()
    profile["role_fr"] = role_data["role_fr"]
    profile["role_en"] = role_data["role_en"]
    profile["global_score"] = round(global_score)

    return profile


def sort_skill_results(items):
    """
    Trie les skills par priorité (High → Medium → Low)
    puis par score croissant (les plus faibles en premier).
    """
    return sorted(
        items,
        key=lambda x: (PRIORITY_ORDER[x.priority], x.score)
    )