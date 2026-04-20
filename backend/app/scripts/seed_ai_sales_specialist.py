from app.models.skill import Skill
from app.models.question import Question
from app.models.user_response import UserResponse
from app.models.user_skill_score import UserSkillScore


def seed_ai_sales_specialist(db):
    # =============================
    # 0. Anti-doublon — skip si déjà seedé
    # =============================
    existing = db.query(Skill).filter(Skill.career_path_id == 79).first()
    if existing:
        print("⚠️ AI Sales Specialist — skills déjà seedés, skip.")
        return

    # =============================
    # 1. Créer les 5 skills — AI Sales Specialist (career_path_id = 79)
    # =============================
    skills_data = [
        {"name": "Prospection AI",              "description": "Capacité à identifier et prioriser les prospects avec l'AI", "career_path_id": 79},
        {"name": "CRM et Scoring de Leads",     "description": "Maîtrise des outils CRM AI et interprétation du scoring",   "career_path_id": 79},
        {"name": "Communication et Emails AI",  "description": "Rédaction et personnalisation d'emails avec l'AI",           "career_path_id": 79},
        {"name": "Analyse des Données Ventes",  "description": "Lecture et exploitation des données AI pour la vente",       "career_path_id": 79},
        {"name": "Ethique AI dans la Vente",    "description": "Application des bonnes pratiques éthiques avec l'AI",        "career_path_id": 79},
    ]

    skills = []
    for s in skills_data:
        skill = Skill(**s)
        db.add(skill)
        db.flush()
        skills.append(skill)

    s1, s2, s3, s4, s5 = skills

    # =============================
    # 2. Créer les 10 questions QCM
    # Distribution des bonnes réponses : B, C, D, B, C, A, C, D, B, A
    # =============================
    questions = [

        # ── SKILL 1 — Prospection AI ──

        # Q1 — correct: B
        Question(
            skill_id=s1.id,
            order=1,
            text="Vous avez 200 prospects à contacter cette semaine. Quel est le meilleur moyen d'utiliser l'AI pour prioriser votre travail ?",
            option_a="Contacter les 200 prospects dans l'ordre alphabétique",
            option_b="Utiliser Apollo.io pour identifier automatiquement les prospects les plus susceptibles d'acheter",
            option_c="Envoyer le même email à tout le monde sans priorisation",
            option_d="Attendre que les prospects vous contactent",
            correct_answer="B",
            explanation="Apollo.io utilise l'AI pour scorer et prioriser automatiquement les meilleurs prospects, ce qui permet au commercial de se concentrer sur les opportunités les plus prometteuses.",
        ),

        # Q2 — correct: C
        Question(
            skill_id=s1.id,
            order=2,
            text="Vous utilisez LinkedIn Sales Navigator AI pour prospecter des PME tunisiennes. L'AI vous suggère 50 prospects mais vous n'avez le temps de contacter que 10. Comment choisissez-vous ?",
            option_a="Vous prenez les 10 premiers de la liste sans regarder",
            option_b="Vous choisissez au hasard",
            option_c="Vous filtrez selon le score AI, le secteur d'activité et la taille de l'entreprise",
            option_d="Vous contactez tous les 50 rapidement sans personnalisation",
            correct_answer="C",
            explanation="Le bon AI Sales Specialist combine les filtres AI avec son jugement professionnel pour optimiser sa prospection et maximiser ses chances de succès.",
        ),

        # ── SKILL 2 — CRM et Scoring de Leads ──

        # Q3 — correct: D
        Question(
            skill_id=s2.id,
            order=3,
            text="Votre CRM HubSpot AI montre que 3 prospects ont un score de 90/100. Qu'est-ce que ce score signifie ?",
            option_a="Ces prospects ont acheté 90 produits",
            option_b="Ces prospects ont visité votre site 90 fois",
            option_c="Ces prospects ont dépensé 90 dinars chez vous",
            option_d="Ces prospects ont 90% de chances d'acheter prochainement",
            correct_answer="D",
            explanation="Le scoring AI prédit la probabilité d'achat de chaque prospect en analysant ses comportements : visites du site, ouvertures d'emails, téléchargements, etc.",
        ),

        # Q4 — correct: B
        Question(
            skill_id=s2.id,
            order=4,
            text="Votre HubSpot AI vous dit : ce prospect a visité votre site 5 fois, ouvert 3 emails et téléchargé votre catalogue. Son score est 85/100. Que faites-vous ?",
            option_a="Vous attendez qu'il vous contacte",
            option_b="Vous l'appelez immédiatement car il montre un intérêt évident",
            option_c="Vous lui envoyez encore plus d'emails automatiques",
            option_d="Vous ignorez ces informations car l'AI peut se tromper",
            correct_answer="B",
            explanation="Un score élevé combiné à des signaux forts d'intérêt indique le bon moment pour contacter directement le prospect et conclure la vente.",
        ),

        # ── SKILL 3 — Communication et Emails AI ──

        # Q5 — correct: C
        Question(
            skill_id=s3.id,
            order=5,
            text="Vous utilisez ChatGPT pour rédiger un email de prospection pour un client tunisien. Quelle est la meilleure approche ?",
            option_a="Copier exactement l'email généré par ChatGPT sans le modifier",
            option_b="Demander à ChatGPT de rédiger en anglais pour paraître professionnel",
            option_c="Demander à ChatGPT de rédiger en arabe ou français, puis personnaliser selon le contexte du client",
            option_d="Ne pas utiliser ChatGPT car les clients préfèrent les emails écrits à la main",
            correct_answer="C",
            explanation="La personnalisation culturelle et linguistique est essentielle pour le marché Afrique du Nord. L'AI rédige le contenu de base et le commercial l'adapte au contexte spécifique du client.",
        ),

        # Q6 — correct: A
        Question(
            skill_id=s3.id,
            order=6,
            text="Vous devez envoyer 100 emails personnalisés à 100 prospects différents. Sans AI cela prendrait 5 heures. Comment utilisez-vous l'AI pour faire cela en 30 minutes ?",
            option_a="Vous utilisez HubSpot AI pour créer des templates qui s'adaptent automatiquement au profil de chaque prospect",
            option_b="Vous envoyez le même email générique à tous",
            option_c="Vous embauchez quelqu'un pour écrire les emails",
            option_d="Vous réduisez le nombre d'emails à envoyer",
            correct_answer="A",
            explanation="Les templates AI de HubSpot permettent la personnalisation à grande échelle en quelques minutes, en adaptant automatiquement le contenu au profil de chaque prospect.",
        ),

        # ── SKILL 4 — Analyse des Données Ventes ──

        # Q7 — correct: C
        Question(
            skill_id=s4.id,
            order=7,
            text="Votre AI prédit que votre chiffre d'affaires ce mois sera de 50 000 TND mais votre objectif est 80 000 TND. Que faites-vous ?",
            option_a="Vous ignorez la prédiction AI",
            option_b="Vous attendez la fin du mois pour voir",
            option_c="Vous analysez immédiatement les données pour identifier les opportunités manquées et agissez maintenant",
            option_d="Vous baissez votre objectif à 50 000 TND",
            correct_answer="C",
            explanation="L'AI permet d'anticiper les résultats et d'agir proactivement avant la fin du mois pour atteindre les objectifs commerciaux.",
        ),

        # Q8 — correct: D
        Question(
            skill_id=s4.id,
            order=8,
            text="Google Analytics AI vous montre que 80% de vos clients tunisiens consultent vos offres entre 19h et 21h sur mobile. Comment utilisez-vous cette information ?",
            option_a="Vous continuez à envoyer vos emails le matin comme avant",
            option_b="Vous ignorez cette information car ce sont juste des statistiques",
            option_c="Vous appelez tous vos clients entre 19h et 21h",
            option_d="Vous programmez vos emails entre 19h et 21h et optimisez votre site pour mobile",
            correct_answer="D",
            explanation="Les données AI permettent d'optimiser le timing et le format pour maximiser l'impact commercial auprès des clients en Afrique du Nord.",
        ),

        # ── SKILL 5 — Ethique AI dans la Vente ──

        # Q9 — correct: B
        Question(
            skill_id=s5.id,
            order=9,
            text="L'AI vous donne accès à des données personnelles très détaillées sur vos prospects. Quelle est la pratique éthique ?",
            option_a="Utiliser toutes les données disponibles pour maximiser les ventes",
            option_b="Utiliser uniquement les données que les prospects ont accepté de partager",
            option_c="Vendre ces données à d'autres entreprises",
            option_d="Partager ces données avec toute votre équipe sans restriction",
            correct_answer="B",
            explanation="Le respect de la vie privée et le consentement sont fondamentaux dans l'utilisation éthique de l'AI en vente. Seules les données consenties doivent être utilisées.",
        ),

        # Q10 — correct: A
        Question(
            skill_id=s5.id,
            order=10,
            text="Votre outil AI génère des messages de relance très personnalisés en utilisant des données personnelles de vos prospects. Un prospect vous demande comment vous avez obtenu ces informations. Que faites-vous ?",
            option_a="Vous expliquez transparentement les données utilisées et proposez de les supprimer si souhaité",
            option_b="Vous évitez de répondre pour ne pas perdre la vente",
            option_c="Vous dites que c'est l'AI qui a trouvé ces informations, donc ce n'est pas votre responsabilité",
            option_d="Vous bloquez ce prospect car il pose trop de questions",
            correct_answer="A",
            explanation="La transparence sur l'utilisation des données est une obligation éthique et légale. Un AI Sales Specialist certifié Euklydia assume la responsabilité des outils qu'il utilise et respecte le droit des prospects à contrôler leurs données.",
        ),
    ]

    for q in questions:
        db.add(q)

    db.commit()
    print("✅ AI Sales Specialist — 5 skills + 10 questions seedés avec succès")