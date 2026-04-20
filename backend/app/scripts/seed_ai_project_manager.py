from app.models.skill import Skill
from app.models.question import Question
from app.models.user_response import UserResponse
from app.models.user_skill_score import UserSkillScore


def seed_ai_project_manager(db):
    # =============================
    # 0. Anti-doublon — skip si déjà seedé
    # =============================
    existing = db.query(Skill).filter(Skill.career_path_id == 82).first()
    if existing:
        print("⚠️ AI Project Manager — skills déjà seedés, skip.")
        return

    # =============================
    # 1. Créer les 5 skills — AI Project Manager (career_path_id = 82)
    # =============================
    skills_data = [
        {"name": "Planification de projets avec AI",  "description": "Capacité à générer et gérer des plannings avec l'AI",               "career_path_id": 82},
        {"name": "Outils de gestion de projet AI",    "description": "Maîtrise des outils AI de gestion de projet",                        "career_path_id": 82},
        {"name": "Analyse des risques et données AI", "description": "Capacité à prédire et gérer les risques avec l'AI",                   "career_path_id": 82},
        {"name": "Orchestration humain-AI",           "description": "Capacité à coordonner humains et AI efficacement",                    "career_path_id": 82},
        {"name": "Gouvernance et éthique AI",         "description": "Application des bonnes pratiques éthiques en gestion AI",             "career_path_id": 82},
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
    # Distribution des bonnes réponses : B, D, A, B, C, B, C, D, C, A
    # =============================
    questions = [

        # ── SKILL 1 — Planification de projets avec AI ──

        # Q1 — correct: B
        Question(
            skill_id=s1.id,
            order=1,
            text="Vous devez planifier le lancement d'un nouveau projet digital en 3 mois. Quel outil AI vous aide à générer automatiquement le planning complet du projet ?",
            option_a="Canva AI",
            option_b="ClickUp AI ou Notion AI",
            option_c="Mailchimp AI",
            option_d="Midjourney",
            correct_answer="B",
            explanation="ClickUp AI et Notion AI permettent de générer automatiquement des plannings complets avec tâches, délais et responsables en quelques secondes à partir d'une simple description.",
        ),

        # Q2 — correct: D
        Question(
            skill_id=s1.id,
            order=2,
            text="Votre équipe tunisienne de 8 personnes doit lancer une plateforme digitale en 60 jours. L'AI vous propose un planning mais certaines tâches semblent impossibles dans les délais. Que faites-vous ?",
            option_a="Vous acceptez le planning AI sans le modifier",
            option_b="Vous abandonnez le planning AI et revenez à Excel",
            option_c="Vous réduisez le nombre de tâches sans consulter l'équipe",
            option_d="Vous analysez les tâches critiques, ajustez les délais irréalistes et validez avec votre équipe",
            correct_answer="D",
            explanation="L'AI génère un planning de base mais le PM doit toujours valider avec son équipe et ajuster selon les contraintes réelles du marché local et les capacités de chaque membre.",
        ),

        # ── SKILL 2 — Outils de gestion de projet AI ──

        # Q3 — correct: A
        Question(
            skill_id=s2.id,
            order=3,
            text="Votre équipe utilise Trello pour gérer ses projets mais vous voulez intégrer l'AI pour automatiser les tâches répétitives. Quelle est la meilleure alternative ?",
            option_a="Utiliser ClickUp AI ou Monday AI qui intègrent l'AI nativement",
            option_b="Revenir aux post-its physiques",
            option_c="Utiliser uniquement WhatsApp pour communiquer",
            option_d="Continuer avec Trello sans changement",
            correct_answer="A",
            explanation="ClickUp AI et Monday AI intègrent l'AI nativement pour automatiser les tâches, générer des rapports et prédire les risques, bien au-delà des capacités de Trello.",
        ),

        # Q4 — correct: B
        Question(
            skill_id=s2.id,
            order=4,
            text="Vous gérez 3 projets simultanément pour des clients en Afrique du Nord. Chaque projet a son équipe et ses délais. Comment utilisez-vous l'AI pour tout coordonner efficacement ?",
            option_a="Vous gérez chaque projet séparément dans des fichiers Excel différents",
            option_b="Vous utilisez Notion AI pour créer un espace centralisé avec tableaux de bord automatiques pour les 3 projets",
            option_c="Vous embauchez 3 assistants pour chaque projet",
            option_d="Vous abandonnez un des projets car c'est trop compliqué",
            correct_answer="B",
            explanation="Notion AI permet de centraliser plusieurs projets avec des tableaux de bord automatiques, offrant une vision globale et détaillée simultanément pour tous les projets.",
        ),

        # ── SKILL 3 — Analyse des risques et données AI ──

        # Q5 — correct: C
        Question(
            skill_id=s3.id,
            order=5,
            text="L'AI de votre outil de gestion prédit que votre projet a 70% de risque de dépasser le délai prévu. Que faites-vous ?",
            option_a="Vous ignorez la prédiction et continuez normalement",
            option_b="Vous attendez que le retard se confirme avant d'agir",
            option_c="Vous analysez les tâches critiques, réorganisez les priorités et informez le client proactivement",
            option_d="Vous dites au client que l'AI se trompe toujours",
            correct_answer="C",
            explanation="Une prédiction AI de risque élevé doit déclencher une action immédiate. Le bon PM agit de façon proactive avant que le problème ne survienne réellement.",
        ),

        # Q6 — correct: B
        Question(
            skill_id=s3.id,
            order=6,
            text="Votre tableau de bord AI montre que 3 membres de votre équipe tunisienne sont surchargés à 150% de leur capacité cette semaine. Que faites-vous ?",
            option_a="Vous ignorez les données car votre équipe peut gérer la pression",
            option_b="Vous utilisez l'AI pour redistribuer automatiquement les tâches et équilibrer la charge",
            option_c="Vous attendez que les membres de l'équipe se plaignent",
            option_d="Vous annulez des tâches importantes sans consulter personne",
            correct_answer="B",
            explanation="L'AI permet de détecter les déséquilibres de charge de travail et de proposer une redistribution automatique pour maintenir la productivité et le bien-être de l'équipe.",
        ),

        # ── SKILL 4 — Orchestration humain-AI ──

        # Q7 — correct: C
        Question(
            skill_id=s4.id,
            order=7,
            text="Votre équipe résiste à l'utilisation des outils AI de gestion de projet. Certains membres disent que l'AI va les remplacer. Comment gérez-vous cette situation ?",
            option_a="Vous imposez les outils AI sans explication",
            option_b="Vous abandonnez les outils AI pour garder la paix dans l'équipe",
            option_c="Vous organisez des sessions de formation, montrez comment l'AI aide sans remplacer, et invitez chaque membre à tester les outils et donner son avis",
            option_d="Vous remplacez les membres résistants",
            correct_answer="C",
            explanation="La conduite du changement est essentielle. Un bon AI PM forme son équipe, dissipe les craintes et implique chacun dans la transformation vers l'AI.",
        ),

        # Q8 — correct: D
        Question(
            skill_id=s4.id,
            order=8,
            text="L'AI de votre outil propose automatiquement d'assigner une tâche sensible à un collaborateur déjà surchargé. Comment réagissez-vous ?",
            option_a="Vous acceptez la suggestion AI sans la remettre en question",
            option_b="Vous ignorez toutes les suggestions AI à l'avenir",
            option_c="Vous demandez au collaborateur surchargé d'accepter la tâche",
            option_d="Vous vérifiez la suggestion AI, considérez le contexte humain et prenez la décision finale vous-même",
            correct_answer="D",
            explanation="L'AI fait des suggestions mais le PM garde toujours la décision finale, surtout pour les situations qui impliquent des facteurs humains complexes.",
        ),

        # ── SKILL 5 — Gouvernance et éthique AI ──

        # Q9 — correct: C
        Question(
            skill_id=s5.id,
            order=9,
            text="Votre entreprise veut utiliser l'AI pour évaluer automatiquement les performances des membres de l'équipe. Quelle est votre réaction en tant que AI Project Manager ?",
            option_a="Vous mettez en place le système AI immédiatement sans consultation",
            option_b="Vous refusez complètement d'utiliser l'AI pour les évaluations",
            option_c="Vous analysez les biais potentiels, consultez l'équipe, définissez des critères transparents et gardez l'humain au centre",
            option_d="Vous laissez l'AI décider seul des promotions et licenciements",
            correct_answer="C",
            explanation="L'évaluation des performances humaines par l'AI doit être encadrée avec des règles éthiques claires, de la transparence totale et une supervision humaine obligatoire.",
        ),

        # Q10 — correct: A
        Question(
            skill_id=s5.id,
            order=10,
            text="Votre outil AI collecte automatiquement des données détaillées sur le comportement de travail de chaque membre de votre équipe (heures de connexion, vitesse d'exécution, pauses). Que faites-vous de ces données ?",
            option_a="Vous utilisez ces données uniquement pour améliorer l'organisation du travail, en informant l'équipe de ce qui est collecté et pourquoi",
            option_b="Vous les utilisez pour surveiller et sanctionner les membres les moins productifs",
            option_c="Vous les partagez publiquement avec toute l'équipe pour créer de la compétition",
            option_d="Vous les vendez à des partenaires RH pour optimiser les recrutements futurs",
            correct_answer="A",
            explanation="Les données comportementales de l'équipe doivent être utilisées uniquement pour améliorer l'organisation, jamais pour surveiller ou sanctionner. La transparence et le consentement sont non-négociables dans une gouvernance AI éthique.",
        ),
    ]

    for q in questions:
        db.add(q)

    db.commit()
    print("✅ AI Project Manager — 5 skills + 10 questions seedés avec succès")