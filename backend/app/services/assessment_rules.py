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
    if score <= HIGH_MAX:
        return "Beginner"
    if score <= MED_MAX:
        return "Intermediate"
    return "Advanced"


# =============================
# Profils par rôle — Command Center
# =============================

ROLE_PROFILES = {

    # ── AI Sales Specialist (role_id=79) ─────────────────────────────────────
    "ai_sales_specialist": {
        "role_fr": "AI Sales Specialist",
        "role_en": "AI Sales Specialist",
        "novice": {
            "profile": "AI Novice",
            "profile_fr": "Novice IA",
            "description_fr": (
                "En tant que AI Sales Specialist débutant, vous découvrez comment l'AI "
                "peut transformer votre approche commerciale. "
                "Concentrez-vous sur la maîtrise des outils de prospection AI "
                "comme HubSpot AI et Apollo.io pour automatiser "
                "vos premières tâches de vente sur le marché d'Afrique du Nord."
            ),
            "description_en": (
                "As a beginner AI Sales Specialist, you are discovering how AI "
                "can transform your sales approach. "
                "Focus on mastering AI prospecting tools like HubSpot AI and Apollo.io "
                "to automate your first sales tasks across the North Africa market."
            ),
            "cta_fr": "Voir ma Feuille de route IA →",
            "cta_en": "View my AI Roadmap →",
        },
        "practitioner": {
            "profile": "AI Practitioner",
            "profile_fr": "Praticien IA",
            "description_fr": (
                "En tant que AI Sales Specialist praticien, vous maîtrisez les bases "
                "de la vente augmentée par l'AI. "
                "Vous êtes prêt à automatiser vos séquences de prospection, "
                "analyser les signaux d'achat et personnaliser vos approches "
                "à grande échelle sur le marché d'Afrique du Nord."
            ),
            "description_en": (
                "As a practitioner AI Sales Specialist, you have mastered the basics "
                "of AI-augmented selling. "
                "You are ready to automate your prospecting sequences, "
                "analyse buying signals and personalise your outreach "
                "at scale across the North Africa market."
            ),
            "cta_fr": "Voir ma Feuille de route IA →",
            "cta_en": "View my AI Roadmap →",
        },
        "leader": {
            "profile": "AI Leader",
            "profile_fr": "Leader IA",
            "description_fr": (
                "En tant que AI Sales Specialist leader, vous pilotez une stratégie "
                "commerciale AI complète. "
                "Vous formez votre équipe, mesurez le ROI de vos outils AI "
                "et positionnez votre organisation comme référence "
                "en vente AI en Afrique du Nord."
            ),
            "description_en": (
                "As a leader AI Sales Specialist, you lead a complete AI sales strategy. "
                "You train your team, measure the ROI of your AI tools "
                "and position your organisation as a reference "
                "in AI sales across North Africa."
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
                "En tant que AI Marketing Strategist débutant, vous faites vos premiers pas "
                "dans le marketing augmenté par l'AI. "
                "Concentrez-vous sur la création de contenu bilingue AR/FR "
                "avec ChatGPT et Canva AI, et sur la planification "
                "de vos premières campagnes adaptées au marché d'Afrique du Nord."
            ),
            "description_en": (
                "As a beginner AI Marketing Strategist, you are taking your first steps "
                "in AI-augmented marketing. "
                "Focus on creating bilingual AR/FR content with ChatGPT and Canva AI, "
                "and on planning your first campaigns adapted to the North Africa market."
            ),
            "cta_fr": "Voir ma Feuille de route IA →",
            "cta_en": "View my AI Roadmap →",
        },
        "practitioner": {
            "profile": "AI Practitioner",
            "profile_fr": "Praticien IA",
            "description_fr": (
                "En tant que AI Marketing Strategist praticien, vous maîtrisez "
                "les fondamentaux du marketing AI. "
                "Vous êtes prêt à automatiser vos campagnes multicanales, "
                "analyser vos données avec Google Analytics AI "
                "et créer des publicités performantes sur Meta et Google "
                "pour le marché d'Afrique du Nord."
            ),
            "description_en": (
                "As a practitioner AI Marketing Strategist, you have mastered "
                "the fundamentals of AI marketing. "
                "You are ready to automate your multichannel campaigns, "
                "analyse your data with Google Analytics AI "
                "and create high-performance ads on Meta and Google "
                "for the North Africa market."
            ),
            "cta_fr": "Voir ma Feuille de route IA →",
            "cta_en": "View my AI Roadmap →",
        },
        "leader": {
            "profile": "AI Leader",
            "profile_fr": "Leader IA",
            "description_fr": (
                "En tant que AI Marketing Strategist leader, vous pilotez "
                "une stratégie marketing AI globale. "
                "Vous formez votre équipe, mesurez le ROI de vos campagnes AI, "
                "créez des contenus culturellement adaptés pour Ramadan "
                "et les événements d'Afrique du Nord, et positionnez votre marque "
                "comme référence dans la région."
            ),
            "description_en": (
                "As a leader AI Marketing Strategist, you lead a complete AI marketing strategy. "
                "You train your team, measure the ROI of your AI campaigns, "
                "create culturally adapted content for Ramadan and North Africa events, "
                "and position your brand as a reference in the region."
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
                "En tant que AI Designer débutant, vous découvrez comment l'AI "
                "révolutionne la création visuelle. "
                "Concentrez-vous sur la génération de vos premières images "
                "avec Midjourney et Canva AI, en apprenant à adapter vos prompts "
                "aux codes culturels et visuels du marché d'Afrique du Nord."
            ),
            "description_en": (
                "As a beginner AI Designer, you are discovering how AI "
                "is revolutionising visual creation. "
                "Focus on generating your first images with Midjourney and Canva AI, "
                "learning to adapt your prompts to the cultural "
                "and visual codes of the North Africa market."
            ),
            "cta_fr": "Voir ma Feuille de route IA →",
            "cta_en": "View my AI Roadmap →",
        },
        "practitioner": {
            "profile": "AI Practitioner",
            "profile_fr": "Praticien IA",
            "description_fr": (
                "En tant que AI Designer praticien, vous maîtrisez les fondamentaux "
                "du design augmenté par l'AI. "
                "Vous êtes prêt à créer des interfaces UI/UX complètes avec Figma AI, "
                "des vidéos professionnelles avec Runway ML "
                "et des identités visuelles bilingues arabe/français "
                "parfaitement adaptées au marché d'Afrique du Nord."
            ),
            "description_en": (
                "As a practitioner AI Designer, you have mastered the fundamentals "
                "of AI-augmented design. "
                "You are ready to create complete UI/UX interfaces with Figma AI, "
                "professional videos with Runway ML "
                "and bilingual Arabic/French visual identities "
                "perfectly adapted to the North Africa market."
            ),
            "cta_fr": "Voir ma Feuille de route IA →",
            "cta_en": "View my AI Roadmap →",
        },
        "leader": {
            "profile": "AI Leader",
            "profile_fr": "Leader IA",
            "description_fr": (
                "En tant que AI Designer leader, vous pilotez une stratégie design AI complète. "
                "Vous maîtrisez la calligraphie arabe et le design moderne, "
                "vous formez votre équipe créative aux outils AI "
                "et créez des identités visuelles qui allient "
                "authenticité culturelle nord-africaine et excellence créative."
            ),
            "description_en": (
                "As a leader AI Designer, you lead a complete AI design strategy. "
                "You master Arabic calligraphy and modern design, "
                "train your creative team on AI tools "
                "and create visual identities that combine "
                "North African cultural authenticity and creative excellence."
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
                "En tant que AI Project Manager débutant, vous découvrez comment l'AI "
                "transforme la gestion de projet. "
                "Concentrez-vous sur la génération automatique de plannings "
                "avec ClickUp AI et Notion AI, et sur la coordination de votre équipe "
                "dans le contexte des projets digitaux d'Afrique du Nord."
            ),
            "description_en": (
                "As a beginner AI Project Manager, you are discovering how AI "
                "transforms project management. "
                "Focus on automatically generating project plans "
                "with ClickUp AI and Notion AI, and on coordinating your team "
                "in the context of North Africa digital projects."
            ),
            "cta_fr": "Voir ma Feuille de route IA →",
            "cta_en": "View my AI Roadmap →",
        },
        "practitioner": {
            "profile": "AI Practitioner",
            "profile_fr": "Praticien IA",
            "description_fr": (
                "En tant que AI Project Manager praticien, vous maîtrisez "
                "les fondamentaux de la gestion de projet AI. "
                "Vous êtes prêt à automatiser vos workflows, prédire les risques "
                "et gérer simultanément plusieurs projets d'Afrique du Nord "
                "avec les tableaux de bord intelligents de ClickUp AI et Monday AI."
            ),
            "description_en": (
                "As a practitioner AI Project Manager, you have mastered "
                "the fundamentals of AI project management. "
                "You are ready to automate your workflows, predict risks "
                "and simultaneously manage multiple North Africa projects "
                "with intelligent dashboards from ClickUp AI and Monday AI."
            ),
            "cta_fr": "Voir ma Feuille de route IA →",
            "cta_en": "View my AI Roadmap →",
        },
        "leader": {
            "profile": "AI Leader",
            "profile_fr": "Leader IA",
            "description_fr": (
                "En tant que AI Project Manager leader, vous pilotez "
                "la transformation AI de votre organisation. "
                "Vous orchestrez humains et AI dans des projets complexes, "
                "formez vos équipes à la conduite du changement AI "
                "et mesurez le ROI de vos outils AI "
                "pour des projets digitaux à fort impact en Afrique du Nord."
            ),
            "description_en": (
                "As a leader AI Project Manager, you lead the AI transformation "
                "of your organisation. "
                "You orchestrate humans and AI in complex projects, "
                "train your teams in AI change management "
                "and measure the ROI of your AI tools "
                "for high-impact digital projects across North Africa."
            ),
            "cta_fr": "Voir ma Feuille de route IA →",
            "cta_en": "View my AI Roadmap →",
        },
    },
}


def get_profile_summary(global_score: float, role_key: str) -> dict:
    """
    Retourne le profil simplifié pour le Command Center.
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