from app.models.skill import Skill
from app.models.question import Question
from app.models.user_response import UserResponse
from app.models.user_skill_score import UserSkillScore


def seed_ai_designer(db):
    # =============================
    # 0. Anti-doublon — skip si déjà seedé
    # =============================
    existing = db.query(Skill).filter(Skill.career_path_id == 81).first()
    if existing:
        print("⚠️ AI Designer — skills déjà seedés, skip.")
        return

    # =============================
    # 1. Créer les 5 skills — AI Designer (career_path_id = 81)
    # =============================
    skills_data = [
        {"name": "Génération d'images AI",               "description": "Capacité à générer des images adaptées au marché Afrique du Nord", "career_path_id": 81},
        {"name": "Design UI/UX avec AI",                  "description": "Maîtrise des outils AI pour la conception d'interfaces",           "career_path_id": 81},
        {"name": "Création vidéo et animation AI",        "description": "Capacité à produire des vidéos avec l'AI",                         "career_path_id": 81},
        {"name": "Brand Assets avec AI",                  "description": "Maîtrise de la création d'identités visuelles avec l'AI",          "career_path_id": 81},
        {"name": "Éthique et propriété intellectuelle AI","description": "Application des bonnes pratiques éthiques en design AI",           "career_path_id": 81},
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
    # Distribution des bonnes réponses : C, B, D, C, C, A, B, D, B, A
    # =============================
    questions = [

        # ── SKILL 1 — Génération d'images AI ──

        # Q1 — correct: C
        Question(
            skill_id=s1.id,
            order=1,
            text="Vous devez créer une affiche publicitaire pour une marque tunisienne. Quel outil AI utilisez-vous pour générer des images uniques et créatives ?",
            option_a="Microsoft Word",
            option_b="Google Maps",
            option_c="Midjourney ou Adobe Firefly",
            option_d="HubSpot AI",
            correct_answer="C",
            explanation="Midjourney et Adobe Firefly sont les outils AI leaders pour la génération d'images professionnelles et créatives, avec des résultats de très haute qualité.",
        ),

        # Q2 — correct: B
        Question(
            skill_id=s1.id,
            order=2,
            text="Vous utilisez Midjourney pour générer une image pour un client tunisien. L'AI génère une image avec des personnages aux traits occidentaux. Que faites-vous ?",
            option_a="Vous acceptez l'image sans modification",
            option_b="Vous affinez votre prompt en précisant des traits culturels adaptés au marché Afrique du Nord pour une image plus pertinente",
            option_c="Vous abandonnez Midjourney et dessinez à la main",
            option_d="Vous envoyez l'image au client sans vérification",
            correct_answer="B",
            explanation="Un bon AI Designer sait affiner ses prompts pour obtenir des résultats culturellement adaptés au marché Afrique du Nord. Le prompting précis est une compétence clé.",
        ),

        # ── SKILL 2 — Design UI/UX avec AI ──

        # Q3 — correct: D
        Question(
            skill_id=s2.id,
            order=3,
            text="Vous devez créer une maquette d'application mobile pour une startup tunisienne. Quel outil AI vous aide à générer des wireframes rapidement ?",
            option_a="Mailchimp AI",
            option_b="Apollo.io",
            option_c="Google Analytics",
            option_d="Figma AI ou Uizard AI",
            correct_answer="D",
            explanation="Figma AI et Uizard AI permettent de générer des wireframes et maquettes d'interfaces rapidement avec l'AI, en partant d'une simple description textuelle.",
        ),

        # Q4 — correct: C
        Question(
            skill_id=s2.id,
            order=4,
            text="Votre client veut créer une application mobile e-commerce pour le marché tunisien. Quels éléments de design devez-vous adapter au contexte local ?",
            option_a="Rien de spécial, le design est universel",
            option_b="Uniquement changer les couleurs pour les rendre plus colorées",
            option_c="Adapter les codes couleurs culturels, optimiser pour mobile et choisir la langue selon la cible : français pour les professionnels, arabe ou français pour le grand public",
            option_d="Traduire uniquement les textes sans modifier le design",
            correct_answer="C",
            explanation="Le design pour le marché tunisien nécessite une adaptation au contexte local : codes visuels culturels, optimisation mobile (80% des utilisateurs tunisiens sont sur mobile), et choix de langue adapté à la cible — français pour le B2B, arabe ou français pour le grand public.",
        ),

        # ── SKILL 3 — Création vidéo et animation AI ──

        # Q5 — correct: C
        Question(
            skill_id=s3.id,
            order=5,
            text="Vous devez créer une courte vidéo publicitaire de 30 secondes pour une PME tunisienne sans équipe de tournage. Quel outil AI utilisez-vous ?",
            option_a="Adobe Photoshop",
            option_b="Microsoft Excel",
            option_c="Runway ML ou Synthesia",
            option_d="HubSpot AI",
            correct_answer="C",
            explanation="Runway ML et Synthesia permettent de créer des vidéos professionnelles avec l'AI sans équipe de tournage ni budget important, idéales pour les PME en Afrique du Nord.",
        ),

        # Q6 — correct: A
        Question(
            skill_id=s3.id,
            order=6,
            text="Votre client veut une vidéo avec une voix off en arabe tunisien. Comment utilisez-vous l'AI pour créer cette voix off ?",
            option_a="Vous utilisez ElevenLabs AI pour générer une voix off réaliste en arabe",
            option_b="Vous enregistrez vous-même la voix off",
            option_c="Vous sous-titrez uniquement sans voix off",
            option_d="Vous utilisez une voix off en anglais car l'AI ne supporte pas l'arabe",
            correct_answer="A",
            explanation="ElevenLabs AI génère des voix off très réalistes en arabe et en français, parfaitement adaptées au contexte tunisien et au marché Afrique du Nord.",
        ),

        # ── SKILL 4 — Brand Assets avec AI ──

        # Q7 — correct: B
        Question(
            skill_id=s4.id,
            order=7,
            text="Un client vous demande de créer son identité visuelle complète avec l'AI. Par quoi commencez-vous ?",
            option_a="Vous créez directement les cartes de visite",
            option_b="Vous générez plusieurs versions du logo avec Midjourney, puis vous définissez la palette et la typographie",
            option_c="Vous copiez l'identité visuelle d'une grande marque",
            option_d="Vous attendez que le client vous envoie ses idées",
            correct_answer="B",
            explanation="La création d'une identité visuelle complète commence toujours par le logo, puis se décline en palette de couleurs, typographie et templates cohérents.",
        ),

        # Q8 — correct: D
        Question(
            skill_id=s4.id,
            order=8,
            text="Vous créez le système de brand assets pour une entreprise tunisienne. Le client veut son logo avec calligraphie arabe et design moderne. Comment procédez-vous avec l'AI ?",
            option_a="Vous dites au client que c'est impossible de combiner les deux",
            option_b="Vous utilisez uniquement la typographie latine car l'AI ne supporte pas l'arabe",
            option_c="Vous créez deux logos séparés : un en arabe et un en latin",
            option_d="Vous utilisez Adobe Firefly avec des prompts combinant calligraphie arabe et design moderne, puis affinez dans Figma AI",
            correct_answer="D",
            explanation="Adobe Firefly et Figma AI permettent de créer des identités visuelles qui combinent calligraphie arabe et design moderne, parfaitement adaptés au marché Afrique du Nord.",
        ),

        # ── SKILL 5 — Éthique et propriété intellectuelle AI ──

        # Q9 — correct: B
        Question(
            skill_id=s5.id,
            order=9,
            text="Vous générez une image avec Midjourney pour un client qui veut l'utiliser commercialement. Que devez-vous vérifier avant de livrer ?",
            option_a="Rien, toutes les images AI sont libres de droits",
            option_b="Vous vérifiez les conditions d'utilisation de Midjourney pour l'usage commercial et informez le client",
            option_c="Vous vendez l'image sans vérification",
            option_d="Vous dites au client que les images AI ne peuvent jamais être utilisées commercialement",
            correct_answer="B",
            explanation="Chaque outil AI a ses propres conditions d'utilisation commerciale. Un AI Designer professionnel doit toujours vérifier et informer son client des droits applicables.",
        ),

        # Q10 — correct: A
        Question(
            skill_id=s5.id,
            order=10,
            text="Vous créez un logo avec Midjourney pour un client en vous inspirant fortement du style d'un designer tunisien célèbre. Le client est satisfait. Quelle est la bonne pratique éthique ?",
            option_a="Vous informez le client que le style s'inspire d'un designer existant et proposez de créer un style original et unique",
            option_b="Vous livrez le logo car l'AI l'a généré donc il n'y a pas de problème",
            option_c="Vous copiez exactement le style sans mentionner la source",
            option_d="Vous demandez au designer original de valider sans informer le client",
            correct_answer="A",
            explanation="Un AI Designer professionnel respecte la propriété intellectuelle créative. S'inspirer fortement du style d'un artiste sans transparence peut constituer une violation éthique, même si l'image est générée par l'AI.",
        ),
    ]

    for q in questions:
        db.add(q)

    db.commit()
    print("✅ AI Designer — 5 skills + 10 questions seedés avec succès")