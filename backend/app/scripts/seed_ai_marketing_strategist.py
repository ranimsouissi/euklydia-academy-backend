from app.models.skill import Skill
from app.models.question import Question
from app.models.user_response import UserResponse
from app.models.user_skill_score import UserSkillScore


def seed_ai_marketing_strategist(db):
    # =============================
    # 0. Anti-doublon — skip si déjà seedé
    # =============================
    existing = db.query(Skill).filter(Skill.career_path_id == 80).first()
    if existing:
        print("⚠️ AI Marketing Strategist — skills déjà seedés, skip.")
        return

    # =============================
    # 1. Créer les 5 skills — AI Marketing Strategist (career_path_id = 80)
    # =============================
    skills_data = [
        {"name": "Création de contenu AI",        "description": "Capacité à créer du contenu marketing adapté au marché Afrique du Nord", "career_path_id": 80},
        {"name": "Gestion réseaux sociaux AI",     "description": "Maîtrise des outils AI pour les réseaux sociaux",                       "career_path_id": 80},
        {"name": "Email marketing AI",             "description": "Capacité à créer et optimiser des campagnes email avec l'AI",            "career_path_id": 80},
        {"name": "Publicité AI",                   "description": "Maîtrise de la publicité digitale avec l'AI",                            "career_path_id": 80},
        {"name": "Analyse des données marketing",  "description": "Lecture et exploitation des données AI en marketing",                    "career_path_id": 80},
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
    # Distribution des bonnes réponses : B, D, C, A, C, A, B, D, B, C
    # =============================
    questions = [

        # ── SKILL 1 — Création de contenu AI ──

        # Q1 — correct: B
        Question(
            skill_id=s1.id,
            order=1,
            text="Vous devez créer 30 posts pour le mois de Ramadan pour une entreprise tunisienne. Quel est le meilleur outil AI à utiliser ?",
            option_a="Utiliser uniquement Word pour écrire les posts manuellement",
            option_b="Utiliser ChatGPT pour générer les textes en arabe et français et Canva AI pour les visuels adaptés",
            option_c="Copier les posts d'une marque américaine et les traduire",
            option_d="Publier les mêmes posts chaque jour",
            correct_answer="B",
            explanation="La combinaison ChatGPT + Canva AI permet de créer du contenu culturellement adapté rapidement et en grande quantité, tout en respectant les spécificités du marché Afrique du Nord.",
        ),

        # Q2 — correct: D
        Question(
            skill_id=s1.id,
            order=2,
            text="Votre client veut lancer une nouvelle formation professionnelle. Il vous demande de créer en 2 heures : 10 posts Instagram, 5 emails et 3 visuels. Comment utilisez-vous l'AI ?",
            option_a="Vous dites que c'est impossible en 2 heures",
            option_b="Vous créez uniquement les posts Instagram et ignorez le reste",
            option_c="Vous copiez du contenu existant sur internet",
            option_d="Vous utilisez ChatGPT pour les textes, Canva AI pour les visuels et Mailchimp AI pour les emails",
            correct_answer="D",
            explanation="L'AI permet de créer plusieurs types de contenu simultanément en un temps record. La clé est d'utiliser les bons outils en parallèle pour maximiser la productivité.",
        ),

        # ── SKILL 2 — Gestion réseaux sociaux AI ──

        # Q3 — correct: C
        Question(
            skill_id=s2.id,
            order=3,
            text="Vous gérez les réseaux sociaux d'une PME tunisienne. Quel outil AI vous permet de planifier et publier automatiquement sur tous les réseaux en même temps ?",
            option_a="Microsoft Word",
            option_b="Google Maps",
            option_c="Buffer AI ou Hootsuite AI",
            option_d="Adobe Photoshop",
            correct_answer="C",
            explanation="Buffer AI et Hootsuite AI permettent de gérer et automatiser tous les réseaux sociaux depuis un seul tableau de bord, en programmant les publications à l'avance.",
        ),

        # Q4 — correct: A
        Question(
            skill_id=s2.id,
            order=4,
            text="Meta Business Suite AI vous montre que vos posts avec des images reçoivent 3 fois plus d'engagement que les posts texte. Que faites-vous ?",
            option_a="Vous adaptez immédiatement votre stratégie pour créer plus de contenu visuel avec Canva AI",
            option_b="Vous continuez à publier principalement du texte",
            option_c="Vous ignorez ces données car ce sont juste des statistiques",
            option_d="Vous supprimez tous vos anciens posts texte",
            correct_answer="A",
            explanation="Les données AI permettent d'adapter la stratégie contenu pour maximiser l'engagement. Un bon AI Marketing Strategist réagit rapidement aux insights fournis par l'AI.",
        ),

        # ── SKILL 3 — Email marketing AI ──

        # Q5 — correct: C
        Question(
            skill_id=s3.id,
            order=5,
            text="Vous envoyez une campagne email à 5 000 clients tunisiens. Votre taux d'ouverture est de 8%. Brevo AI vous montre que vos clients ouvrent leurs emails le soir. Que faites-vous ?",
            option_a="Vous abandonnez l'email marketing",
            option_b="Vous continuez à envoyer le matin car c'est votre habitude",
            option_c="Vous reprogrammez vos envois le soir et personnalisez les objets des emails avec l'AI",
            option_d="Vous réduisez le nombre d'emails envoyés",
            correct_answer="C",
            explanation="Optimiser le timing d'envoi et personnaliser les objets sont les deux leviers principaux pour améliorer le taux d'ouverture. Les données AI permettent cette optimisation précisément.",
        ),

        # Q6 — correct: A
        Question(
            skill_id=s3.id,
            order=6,
            text="Vous devez créer une séquence de 5 emails automatiques pour accueillir les nouveaux clients d'une plateforme e-learning. Comment organisez-vous cette séquence avec l'AI ?",
            option_a="Vous créez avec Mailchimp AI une séquence progressive : bienvenue, premiers pas, conseils, témoignage, offre spéciale",
            option_b="Vous envoyez 5 emails identiques",
            option_c="Vous envoyez tous les emails le même jour",
            option_d="Vous n'envoyez qu'un seul email de bienvenue",
            correct_answer="A",
            explanation="Une séquence progressive et automatisée crée une expérience personnalisée pour chaque client et augmente significativement l'engagement et la fidélisation.",
        ),

        # ── SKILL 4 — Publicité AI ──

        # Q7 — correct: B
        Question(
            skill_id=s4.id,
            order=7,
            text="Vous lancez une campagne Facebook Ads AI pour promouvoir une plateforme de formation professionnelle en Tunisie. Quel ciblage choisissez-vous ?",
            option_a="Cibler tout le monde en Tunisie sans distinction",
            option_b="Cibler les professionnels tunisiens de 25 à 45 ans intéressés par la technologie et le développement professionnel",
            option_c="Cibler uniquement les personnes à Tunis ville",
            option_d="Cibler les moins de 18 ans car ils sont actifs sur Facebook",
            correct_answer="B",
            explanation="Un ciblage précis basé sur les intérêts et le profil professionnel maximise le retour sur investissement publicitaire et attire les apprenants les plus susceptibles de s'inscrire.",
        ),

        # Q8 — correct: D
        Question(
            skill_id=s4.id,
            order=8,
            text="Votre campagne Google Ads AI a un coût par clic de 2 TND mais votre budget est limité à 500 TND par mois. L'AI vous suggère d'optimiser les mots clés. Comment procédez-vous ?",
            option_a="Vous arrêtez la campagne car le budget est trop limité",
            option_b="Vous augmentez le budget sans analyser les résultats",
            option_c="Vous gardez les mêmes mots clés sans optimisation",
            option_d="Vous utilisez Semrush AI pour identifier les mots clés les moins chers mais les plus efficaces",
            correct_answer="D",
            explanation="L'optimisation des mots clés avec Semrush AI permet de maximiser l'impact avec un budget limité, en identifiant les mots clés à fort potentiel et faible concurrence.",
        ),

        # ── SKILL 5 — Analyse des données marketing ──

        # Q9 — correct: B
        Question(
            skill_id=s5.id,
            order=9,
            text="Google Analytics AI vous montre que 70% de vos visiteurs quittent votre site en moins de 10 secondes. Qu'est-ce que cela signifie et que faites-vous ?",
            option_a="C'est normal, ne faites rien",
            option_b="Votre site charge trop lentement ou votre contenu n'est pas attractif — vous devez améliorer l'expérience utilisateur",
            option_c="Vos visiteurs sont satisfaits et reviennent plus tard",
            option_d="Vous supprimez Google Analytics",
            correct_answer="B",
            explanation="Un taux de rebond élevé indique un problème d'expérience utilisateur. L'AI Marketing Strategist doit analyser les données et agir rapidement pour améliorer la performance du site.",
        ),

        # Q10 — correct: C
        Question(
            skill_id=s5.id,
            order=10,
            text="Votre campagne Ramadan sur Instagram a généré 10 000 vues mais seulement 50 clics vers votre site. Meta Business Suite AI vous montre un taux de conversion de 0.5%. Que faites-vous ?",
            option_a="Vous êtes satisfait car 10 000 vues c'est beaucoup",
            option_b="Vous arrêtez la campagne immédiatement",
            option_c="Vous analysez le contenu et le call-to-action, identifiez ce qui bloque le clic, et modifiez le visuel ou le texte pour améliorer le taux de conversion",
            option_d="Vous doublez le budget sans changer le contenu",
            correct_answer="C",
            explanation="Un bon taux de vues avec un faible taux de conversion indique un problème dans le message ou le call-to-action. L'AI Marketing Strategist analyse les données et modifie le contenu avant d'investir davantage.",
        ),
    ]

    for q in questions:
        db.add(q)

    db.commit()
    print("✅ AI Marketing Strategist — 5 skills + 10 questions seedés avec succès")