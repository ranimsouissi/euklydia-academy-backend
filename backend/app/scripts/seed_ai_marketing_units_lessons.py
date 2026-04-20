"""
Seed des units, lessons et activities — AI Marketing Strategist (role_id=80)
Module 1 — Fondations   : 5 unités, 14 leçons, contenu complet
Module 2 — Pratique     : 5 unités, 14 leçons, contenu complet
Module 3 — Expert       : 5 unités, 14 leçons, contenu complet
Total                   : 15 unités, 42 leçons, contenu détaillé

Ordre d'exécution :
  1. seed_ai_marketing_strategist.py
  2. seed_ai_marketing_modules.py
  3. seed_ai_marketing_units_lessons.py  ← ce fichier
"""

from app.models.module import Module
from app.models.unit import Unit
from app.models.lesson import Lesson
from app.models.activity import Activity


def seed_ai_marketing_units_lessons(db):

    # ── Récupérer les 3 modules ───────────────────────────────────────────────
    m1 = db.query(Module).filter_by(
        role="AI Marketing Strategist", journey_stage="foundation"
    ).first()
    m2 = db.query(Module).filter_by(
        role="AI Marketing Strategist", journey_stage="practice"
    ).first()
    m3 = db.query(Module).filter_by(
        role="AI Marketing Strategist", journey_stage="expert"
    ).first()

    if not all([m1, m2, m3]):
        print("❌ Modules AI Marketing Strategist introuvables — lancer seed_modules d'abord")
        return

    # ── Supprimer les données existantes ─────────────────────────────────────
    for module in [m1, m2, m3]:
        existing_units = db.query(Unit).filter_by(module_id=module.id).all()
        for u in existing_units:
            existing_lessons = db.query(Lesson).filter_by(unit_id=u.id).all()
            for lesson in existing_lessons:
                for activity in db.query(Activity).filter_by(lesson_id=lesson.id).all():
                    db.delete(activity)
                db.delete(lesson)
            db.delete(u)
    db.flush()

    # ════════════════════════════════════════════════════════════════════════
    # MODULE 1 — FONDATIONS
    # ════════════════════════════════════════════════════════════════════════

    # ── Unité 1 — L'AI dans le marketing ────────────────────────────────────
    u1_1 = Unit(
        module_id=m1.id, order=1,
        title_fr="L'AI dans le marketing",
        title_en="AI in Marketing",
        description_fr="Comprendre le marketing AI, ses outils essentiels et son contexte en Afrique du Nord.",
        description_en="Understand AI marketing, its essential tools and the North Africa context.",
        estimated_duration_min=26,
    )
    db.add(u1_1); db.flush()

    l1_1_1 = Lesson(
        unit_id=u1_1.id, order=1,
        title_fr="C'est quoi le marketing AI ?",
        title_en="What is AI marketing?",
        format="video", difficulty_level=1, estimated_duration_min=10,
        description_fr="Définition du marketing AI, 5 piliers, évolution historique.",
    )
    db.add(l1_1_1); db.flush()
    db.add(Activity(
        lesson_id=l1_1_1.id, order=1, type="video",
        title_fr="Vidéo — C'est quoi le marketing AI ?",
        is_assessed=False, is_required=True,
        content_fr={"duration_min": 10, "url_fr": None},
        content_en={"duration_min": 10, "url_en": None},
    ))
    db.add(Activity(
        lesson_id=l1_1_1.id, order=2, type="quiz",
        title_fr="Quiz — Le marketing AI",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "questions": [
                {
                    "id": 1,
                    "question": "Quel est le principal avantage du marketing AI pour une PME tunisienne à budget limité ?",
                    "options": [
                        "A) L'AI remplace tous les employés marketing",
                        "B) L'AI permet de produire du contenu professionnel à moindre coût",
                        "C) L'AI garantit automatiquement plus de ventes",
                        "D) L'AI élimine le besoin de connaître sa cible"
                    ],
                    "correct": "B",
                    "explanation": "Le marketing AI permet de produire du contenu professionnel à moindre coût et de rivaliser avec des marques à plus gros budget."
                },
                {
                    "id": 2,
                    "question": "Parmi les 5 piliers du marketing AI, lequel permet de toucher chaque client avec un message unique ?",
                    "options": [
                        "A) Création de contenu automatisée",
                        "B) Personnalisation à grande échelle",
                        "C) Automatisation des campagnes",
                        "D) Analyse prédictive"
                    ],
                    "correct": "B",
                    "explanation": "La personnalisation à grande échelle permet de créer un message unique pour chaque client automatiquement."
                },
                {
                    "id": 3,
                    "question": "Quel outil a marqué le début de l'ère du marketing AI grand public en 2022 ?",
                    "options": ["A) Canva AI", "B) Buffer AI", "C) ChatGPT", "D) Mailchimp AI"],
                    "correct": "C",
                    "explanation": "ChatGPT lancé en novembre 2022 a démocratisé l'accès à l'AI générative pour tous les professionnels du marketing."
                },
            ],
            "passing_score": 70,
        },
        hints_fr=[
            {"level": 1, "text": "Pense à ce que le marketing AI permet concrètement pour une PME au Maghreb."},
            {"level": 2, "text": "Le marketing AI réduit les coûts de production de contenu de 60 à 80%."},
        ],
    ))
    db.flush()

    l1_1_2 = Lesson(
        unit_id=u1_1.id, order=2,
        title_fr="Les outils AI essentiels du marketeur",
        title_en="Essential AI tools for marketers",
        format="video", difficulty_level=1, estimated_duration_min=8,
        description_fr="6 catégories d'outils AI, tableau comparatif, outils gratuits pour démarrer.",
        prerequisite_lesson_id=l1_1_1.id,
    )
    db.add(l1_1_2); db.flush()
    db.add(Activity(
        lesson_id=l1_1_2.id, order=1, type="video",
        title_fr="Vidéo — Les outils AI essentiels du marketeur",
        is_assessed=False, is_required=True,
        content_fr={"duration_min": 8, "url_fr": None},
    ))
    db.add(Activity(
        lesson_id=l1_1_2.id, order=2, type="quiz",
        title_fr="Quiz — Outils AI marketing",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "questions": [
                {
                    "id": 1,
                    "question": "Quel outil AI gratuit recommandez-vous pour démarrer la création de visuels marketing ?",
                    "options": ["A) Jasper AI", "B) Canva AI", "C) Hootsuite AI", "D) Klaviyo AI"],
                    "correct": "B",
                    "explanation": "Canva AI propose une version gratuite puissante pour créer des visuels professionnels sans compétences en design."
                },
                {
                    "id": 2,
                    "question": "Quelle catégorie d'outil AI permet de planifier et publier automatiquement sur tous les réseaux ?",
                    "options": ["A) Rédaction AI", "B) Email marketing AI", "C) Réseaux sociaux AI", "D) Analyse AI"],
                    "correct": "C",
                    "explanation": "Les outils de réseaux sociaux AI comme Buffer AI permettent de programmer les publications sur tous les réseaux depuis un seul tableau de bord."
                },
            ],
            "passing_score": 70,
        },
    ))
    db.flush()

    l1_1_3 = Lesson(
        unit_id=u1_1.id, order=3,
        title_fr="Le marketing AI dans le contexte MENA",
        title_en="AI marketing in the MENA context",
        format="video", difficulty_level=1, estimated_duration_min=8,
        description_fr="Spécificités MENA, bilinguisme AR/FR, calendrier culturel, cas PME tunisienne.",
        prerequisite_lesson_id=l1_1_2.id,
    )
    db.add(l1_1_3); db.flush()
    db.add(Activity(
        lesson_id=l1_1_3.id, order=1, type="video",
        title_fr="Vidéo — Le marketing AI dans le contexte MENA",
        is_assessed=False, is_required=True,
        content_fr={"duration_min": 8, "url_fr": None},
    ))
    db.add(Activity(
        lesson_id=l1_1_3.id, order=2, type="forum_discussion",
        title_fr="Forum — Le marketing AI dans votre contexte professionnel",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "question": "Comment le marketing AI peut-il aider votre secteur d'activité en Tunisie ? Partagez un exemple concret d'utilisation AI que vous aimeriez tester.",
            "consigne": "Répondre en minimum 5 lignes. Décrire votre secteur, un défi marketing concret et un outil AI à tester. Commenter au moins 2 contributions de vos pairs.",
        },
    ))
    db.flush()

    # ── Unité 2 — Créer du contenu avec l'AI ────────────────────────────────
    u1_2 = Unit(
        module_id=m1.id, order=2,
        title_fr="Créer du contenu avec l'AI",
        title_en="Creating Content with AI",
        description_fr="Maîtriser ChatGPT et Canva AI pour créer du contenu marketing bilingue adapté au marché Afrique du Nord.",
        estimated_duration_min=42,
    )
    db.add(u1_2); db.flush()

    l1_2_1 = Lesson(
        unit_id=u1_2.id, order=1,
        title_fr="Rédiger avec ChatGPT en arabe et en français",
        title_en="Writing with ChatGPT in Arabic and French",
        format="video", difficulty_level=2, estimated_duration_min=12,
        description_fr="Formule du prompt parfait, cas Ramadan Tunis, exercice pratique bilingue.",
    )
    db.add(l1_2_1); db.flush()
    db.add(Activity(lesson_id=l1_2_1.id, order=1, type="video",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(
        lesson_id=l1_2_1.id, order=2, type="exercise",
        title_fr="Exercice — Créez vos 3 premiers posts avec ChatGPT",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "1. Choisissez une marque ou secteur en Tunisie.\n2. Rédigez un prompt avec la formule Rôle + Contexte + Tâche + Format.\n3. Générez 3 posts Instagram bilingues AR/FR avec ChatGPT.\n4. Évaluez et personnalisez chaque post.",
            "livrable": "3 posts finalisés (screenshot ChatGPT + post final)",
            "criteres": {"qualite_prompt": "30%", "adaptation_culturelle_mena": "40%", "pertinence_hashtags": "30%"},
            "score_minimum": 70,
        },
        hints_fr=[
            {"level": 1, "text": "La formule du prompt : 'Tu es un expert en marketing digital pour le marché [pays]. Crée [nombre] [type de contenu]...'"},
            {"level": 2, "text": "Mentionnez toujours le contexte culturel MENA et la langue souhaitée dans votre prompt."},
        ],
    ))
    db.flush()

    l1_2_2 = Lesson(
        unit_id=u1_2.id, order=2,
        title_fr="Créer des visuels avec Canva AI",
        title_en="Creating visuals with Canva AI",
        format="tutorial", difficulty_level=2, estimated_duration_min=12,
        prerequisite_lesson_id=l1_2_1.id,
        description_fr="Prise en main Canva AI, Magic Design, Background Remover, palette MENA.",
    )
    db.add(l1_2_2); db.flush()
    db.add(Activity(lesson_id=l1_2_2.id, order=1, type="tutorial",
        title_fr="Tutoriel guidé — Canva AI pas à pas",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(
        lesson_id=l1_2_2.id, order=2, type="exercise",
        title_fr="Exercice — Créez votre kit visuel complet",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Créez 3 visuels avec Canva AI pour la même marque :\n1. Post Instagram carré (1080x1080px)\n2. Story Instagram (1080x1920px)\n3. Bannière email (600x200px)",
            "livrable": "3 fichiers PNG",
            "criteres": {"coherence_visuelle": "40%", "adaptation_culturelle_mena": "40%", "lisibilite_mobile": "20%"},
        },
    ))
    db.flush()

    l1_2_3 = Lesson(
        unit_id=u1_2.id, order=3,
        title_fr="Adapter le contenu au contexte MENA",
        title_en="Adapting content to the MENA context",
        format="video", difficulty_level=2, estimated_duration_min=10,
        prerequisite_lesson_id=l1_2_2.id,
        description_fr="5 codes culturels MENA, erreurs à éviter, cas campagne rentrée scolaire tunisienne.",
    )
    db.add(l1_2_3); db.flush()
    db.add(Activity(lesson_id=l1_2_3.id, order=1, type="video",
        is_assessed=False, is_required=True, content_fr={"duration_min": 10}))
    db.add(Activity(
        lesson_id=l1_2_3.id, order=2, type="exercise",
        title_fr="Exercice noté — Votre première campagne complète",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Créez une mini-campagne marketing complète pour une marque tunisienne :\n1. 3 posts Instagram AR/FR (ChatGPT) + 3 visuels (Canva AI)\n2. 1 email marketing complet + 1 bannière email\n3. 1 story Instagram mobile",
            "livrable": "Posts + visuels + email complet",
            "criteres": {"qualite_contenu_textuel": "40%", "qualite_visuels": "30%", "adaptation_culturelle_mena": "20%", "coherence_campagne": "10%"},
            "score_minimum": 70,
        },
        rubric_fr={"criteres": [
            {"nom": "Qualité du contenu textuel", "poids": 0.4, "description": "Pertinence, adaptation MENA, correction linguistique"},
            {"nom": "Qualité des visuels Canva AI", "poids": 0.3, "description": "Cohérence, adaptation aux formats, lisibilité mobile"},
            {"nom": "Adaptation culturelle MENA", "poids": 0.2, "description": "Codes culturels respectés, calendrier saisonnier"},
            {"nom": "Cohérence de la campagne", "poids": 0.1, "description": "Message unifié sur tous les formats"},
        ]},
    ))
    db.flush()

    # ── Unité 3 — Les réseaux sociaux avec l'AI ──────────────────────────────
    u1_3 = Unit(
        module_id=m1.id, order=3,
        title_fr="Les réseaux sociaux avec l'AI",
        title_en="Social Media with AI",
        description_fr="Gérer et planifier ses réseaux sociaux avec Buffer AI, créer un calendrier éditorial mensuel.",
        estimated_duration_min=38,
    )
    db.add(u1_3); db.flush()

    l1_3_1 = Lesson(unit_id=u1_3.id, order=1,
        title_fr="Gérer ses réseaux sociaux avec l'AI", title_en="Gérer ses réseaux sociaux avec l'AI", format="video",
        difficulty_level=1, estimated_duration_min=10,
        description_fr="État des réseaux en MENA 2026, 4 tâches automatisées, spécificités par plateforme.", description_en="État des réseaux en MENA 2026, 4 tâches automatisées, spécificités par plateforme.")
    db.add(l1_3_1); db.flush()
    db.add(Activity(lesson_id=l1_3_1.id, order=1, type="video",
        is_assessed=False, is_required=True, content_fr={"duration_min": 10}))
    db.add(Activity(lesson_id=l1_3_1.id, order=2, type="quiz",
        title_fr="Quiz — Réseaux sociaux AI",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={"questions": [
            {"id": 1, "question": "Quel réseau social est le plus utilisé en Tunisie en 2026 ?",
             "options": ["A) TikTok", "B) Instagram", "C) Facebook", "D) Twitter/X"],
             "correct": "C", "explanation": "Facebook reste le réseau numéro un en Tunisie avec plus de 7 millions d'utilisateurs actifs."},
            {"id": 2, "question": "Meta Business Suite AI vous montre que vos posts avec images reçoivent 3x plus d'engagement. Que faites-vous ?",
             "options": ["A) Continuer à publier du texte", "B) Adapter votre stratégie pour créer plus de contenu visuel avec Canva AI", "C) Ignorer ces données", "D) Supprimer vos anciens posts texte"],
             "correct": "B", "explanation": "Un bon AI Marketing Strategist réagit aux données et adapte sa stratégie."},
        ], "passing_score": 70}))
    db.flush()

    l1_3_2 = Lesson(unit_id=u1_3.id, order=2,
        title_fr="Planifier ses publications automatiquement avec Buffer AI",
        title_en="Planifier ses publications automatiquement avec Buffer AI",
        format="tutorial", difficulty_level=2, estimated_duration_min=10,
        prerequisite_lesson_id=l1_3_1.id,
        description_fr="Workflow hebdomadaire Buffer AI, mix de contenu 7 posts, créneaux optimaux MENA.", description_en="Workflow hebdomadaire Buffer AI, mix de contenu 7 posts, créneaux optimaux MENA.")
    db.add(l1_3_2); db.flush()
    db.add(Activity(lesson_id=l1_3_2.id, order=1, type="tutorial",
        is_assessed=False, is_required=True, content_fr={"duration_min": 10}))
    db.add(Activity(lesson_id=l1_3_2.id, order=2, type="exercise",
        title_fr="Exercice — Créez votre calendrier éditorial d'une semaine",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "consigne": "1. Créer un compte Buffer AI gratuit\n2. Connecter 2 réseaux sociaux (Facebook + Instagram)\n3. Générer 7 posts avec ChatGPT selon le mix recommandé\n4. Créer les visuels Canva AI\n5. Programmer dans Buffer AI avec les créneaux optimaux MENA",
            "livrable": "Screenshot du calendrier Buffer AI avec 7 posts programmés",
        }))
    db.flush()

    l1_3_3 = Lesson(unit_id=u1_3.id, order=3,
        title_fr="Mon premier calendrier de contenu AI",
        title_en="Mon premier calendrier de contenu AI",
        format="exercise", difficulty_level=3, estimated_duration_min=60,
        prerequisite_lesson_id=l1_3_2.id,
        description_fr="Projet pratique noté — calendrier éditorial mensuel complet (20 posts, 2 réseaux).", description_en="Projet pratique noté — calendrier éditorial mensuel complet (20 posts, 2 réseaux).")
    db.add(l1_3_3); db.flush()
    db.add(Activity(lesson_id=l1_3_3.id, order=1, type="exercise",
        title_fr="Projet noté — Mon premier calendrier éditorial mensuel",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Créez un calendrier éditorial d'un mois complet pour une marque tunisienne :\n1. 20 posts minimum sur 4 semaines et 2 réseaux\n2. Dossier de 20 visuels Canva AI\n3. Screenshot du calendrier Buffer AI programmé\n4. Note de 10 lignes sur votre stratégie éditoriale",
            "livrable": "Tableau contenu + 20 visuels + screenshot Buffer AI + note stratégique",
            "criteres": {"quantite_regularite": "30%", "qualite_contenu": "30%", "qualite_visuels": "20%", "mix_contenu": "20%"},
            "score_minimum": 70,
        },
        rubric_fr={"criteres": [
            {"nom": "Quantité et régularité", "poids": 0.3, "description": "20 posts minimum répartis sur 4 semaines"},
            {"nom": "Qualité du contenu", "poids": 0.3, "description": "Pertinence, adaptation MENA, correction linguistique"},
            {"nom": "Qualité des visuels", "poids": 0.2, "description": "Cohérence visuelle, formats adaptés"},
            {"nom": "Mix de contenu", "poids": 0.2, "description": "Équilibre éducatif/promotionnel/communauté"},
        ]}))
    db.flush()

    # ── Unité 4 — Mon premier email marketing AI ─────────────────────────────
    u1_4 = Unit(module_id=m1.id, order=4,
        title_fr="Mon premier email marketing AI",
        title_en="My First AI Email Marketing",
        description_fr="Créer et analyser des campagnes email avec Mailchimp AI, méthode Test-Analyse-Améliore.",
        estimated_duration_min=36)
    db.add(u1_4); db.flush()

    l1_4_1 = Lesson(unit_id=u1_4.id, order=1,
        title_fr="C'est quoi une campagne email ?", title_en="C'est quoi une campagne email ?", format="video",
        difficulty_level=1, estimated_duration_min=8,
        description_fr="4 types de campagnes, métriques clés, ROI email marketing MENA.", description_en="4 types de campagnes, métriques clés, ROI email marketing MENA.")
    db.add(l1_4_1); db.flush()
    db.add(Activity(lesson_id=l1_4_1.id, order=1, type="video",
        is_assessed=False, is_required=True, content_fr={"duration_min": 8}))
    db.add(Activity(lesson_id=l1_4_1.id, order=2, type="quiz",
        title_fr="Quiz — Email marketing fondamentaux",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={"questions": [
            {"id": 1, "question": "Quel type d'email atteint généralement le meilleur taux d'ouverture ?",
             "options": ["A) Newsletter mensuelle", "B) Email promotionnel", "C) Email de bienvenue", "D) Email de relance panier"],
             "correct": "C", "explanation": "L'email de bienvenue atteint 45 à 60% de taux d'ouverture car le contact vient de s'inscrire."},
            {"id": 2, "question": "Brevo AI vous montre que vos clients ouvrent leurs emails le soir. Que faites-vous ?",
             "options": ["A) Abandonner l'email marketing", "B) Continuer à envoyer le matin", "C) Reprogrammer vos envois le soir et personnaliser les objets avec l'AI", "D) Réduire le nombre d'emails"],
             "correct": "C", "explanation": "Optimiser le timing et personnaliser les objets sont les deux leviers principaux pour améliorer le taux d'ouverture."},
        ], "passing_score": 70}))
    db.flush()

    l1_4_2 = Lesson(unit_id=u1_4.id, order=2,
        title_fr="Créer sa première campagne avec Mailchimp AI",
        title_en="Créer sa première campagne avec Mailchimp AI",
        format="tutorial", difficulty_level=2, estimated_duration_min=12,
        prerequisite_lesson_id=l1_4_1.id,
        description_fr="Tutoriel Mailchimp AI pas à pas, Send Time Optimization, A/B test objet.", description_en="Tutoriel Mailchimp AI pas à pas, Send Time Optimization, A/B test objet.")
    db.add(l1_4_2); db.flush()
    db.add(Activity(lesson_id=l1_4_2.id, order=1, type="tutorial",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(lesson_id=l1_4_2.id, order=2, type="exercise",
        title_fr="Exercice — Créez et envoyez votre première campagne Mailchimp AI",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "consigne": "1. Créer compte Mailchimp AI gratuit\n2. Importer 10 contacts minimum\n3. Créer email promotionnel avec bannière Canva AI + texte ChatGPT\n4. Programmer avec Send Time Optimization\n5. Partager le rapport de performance",
            "livrable": "Screenshot du rapport Mailchimp après envoi",
        }))
    db.flush()

    l1_4_3 = Lesson(unit_id=u1_4.id, order=3,
        title_fr="Analyser les résultats de sa campagne",
        title_en="Analyser les résultats de sa campagne",
        format="video", difficulty_level=2, estimated_duration_min=10,
        prerequisite_lesson_id=l1_4_2.id,
        description_fr="Tableau de bord Mailchimp AI, grille de diagnostic, méthode Test-Analyse-Améliore.", description_en="Tableau de bord Mailchimp AI, grille de diagnostic, méthode Test-Analyse-Améliore.")
    db.add(l1_4_3); db.flush()
    db.add(Activity(lesson_id=l1_4_3.id, order=1, type="video",
        is_assessed=False, is_required=True, content_fr={"duration_min": 10}))
    db.add(Activity(lesson_id=l1_4_3.id, order=2, type="exercise",
        title_fr="Exercice — Analysez votre campagne et planifiez la suivante",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "consigne": "Sur la base de votre campagne envoyée :\n1. Analysez les 4 métriques clés\n2. Identifiez 1 variable à tester\n3. Rédigez 2 objets A/B test avec ChatGPT",
            "livrable": "Document 1 page : analyse + plan d'amélioration",
        }))
    db.flush()

    # ── Unité 5 — Éthique AI Débutant ────────────────────────────────────────
    u1_5 = Unit(module_id=m1.id, order=5,
        title_fr="Éthique AI — Niveau Débutant",
        title_en="AI Ethics — Beginner Level",
        description_fr="Droits d'auteur, transparence, responsabilité en marketing AI.",
        estimated_duration_min=28)
    db.add(u1_5); db.flush()

    l1_5_1 = Lesson(unit_id=u1_5.id, order=1,
        title_fr="Droits d'auteur et contenu généré par l'AI",
        title_en="Copyright and AI-generated Content",
        format="video", difficulty_level=1, estimated_duration_min=10,
        description_fr="CGU des outils AI, droits commerciaux, 5 règles d'or, tableau droits par outil.", description_en="CGU des outils AI, droits commerciaux, 5 règles d'or, tableau droits par outil.")
    db.add(l1_5_1); db.flush()
    db.add(Activity(lesson_id=l1_5_1.id, order=1, type="video",
        is_assessed=False, is_required=True, content_fr={"duration_min": 10}))
    db.add(Activity(lesson_id=l1_5_1.id, order=2, type="quiz",
        title_fr="Quiz — Droits d'auteur et AI",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={"questions": [
            {"id": 1,
             "question": "Vous utilisez Midjourney version gratuite pour une campagne commerciale. C'est :",
             "options": [
                 "A) Parfaitement légal — Midjourney est gratuit",
                 "B) Une violation des CGU — la version gratuite n'accorde pas les droits commerciaux",
                 "C) Légal si vous modifiez l'image dans Canva",
                 "D) Légal si la campagne est en Tunisie"
             ],
             "correct": "B",
             "explanation": "La version gratuite de Midjourney n'accorde pas les droits commerciaux — un abonnement payant est requis."},
        ], "passing_score": 70}))
    db.flush()

    l1_5_2 = Lesson(unit_id=u1_5.id, order=2,
        title_fr="Transparence et responsabilité en marketing AI",
        title_en="Transparence et responsabilité en marketing AI",
        format="case_study", difficulty_level=2, estimated_duration_min=30,
        prerequisite_lesson_id=l1_5_1.id,
        description_fr="3 cas pratiques interactifs MENA : Meriem, Karim, Nour. Charte éthique débutant.", description_en="3 cas pratiques interactifs MENA : Meriem, Karim, Nour. Charte éthique débutant.")
    db.add(l1_5_2); db.flush()
    db.add(Activity(lesson_id=l1_5_2.id, order=1, type="case_study",
        title_fr="Cas pratiques — Transparence et responsabilité",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "cas": [
                {
                    "titre": "Cas Meriem — La statistique inventée",
                    "contexte": "Meriem publie une statistique générée par ChatGPT sans vérifier la source. La statistique est inventée.",
                    "questions": ["Quelle erreur éthique Meriem a-t-elle commise ?", "Quelles sont les conséquences potentielles pour sa marque ?", "Comment aurait-elle dû procéder ?"],
                },
                {
                    "titre": "Cas Karim — Les faux avis clients",
                    "contexte": "Karim génère 10 faux avis clients avec ChatGPT et les publie sur Google My Business.",
                    "questions": ["Quelles lois Karim viole-t-il ?", "Quels sont les risques concrets pour son agence ?", "Quelle alternative éthique avait-il ?"],
                },
            ],
            "score_minimum": 70,
        }))
    db.flush()

    # ════════════════════════════════════════════════════════════════════════
    # MODULE 2 — PRATIQUE
    # ════════════════════════════════════════════════════════════════════════

    # ── Unité 1 — Automatiser ses campagnes marketing ────────────────────────
    u2_1 = Unit(module_id=m2.id, order=1,
        title_fr="Automatiser ses campagnes marketing",
        title_en="Automating Marketing Campaigns",
        estimated_duration_min=38)
    db.add(u2_1); db.flush()

    l2_1_1 = Lesson(unit_id=u2_1.id, order=1,
        title_fr="Créer des séquences de contenu automatisées",
        title_en="Creating automated content sequences",
        format="video", difficulty_level=3, estimated_duration_min=12,
        description_fr="Anatomie d'une séquence, triggers intelligents, timing optimal MENA, funnel de contenu automatisé.", description_en="Anatomie d'une séquence, triggers intelligents, timing optimal MENA, funnel de contenu automatisé.")
    db.add(l2_1_1); db.flush()
    db.add(Activity(lesson_id=l2_1_1.id, order=1, type="video",
        title_fr="Vidéo — Créer des séquences de contenu automatisées",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12, "url_fr": None}))
    db.add(Activity(
        lesson_id=l2_1_1.id, order=2, type="quiz",
        title_fr="Quiz — Séquences de contenu automatisées",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "questions": [
                {
                    "id": 1,
                    "question": "Vous gérez le marketing d'une école de langues à Tunis. Quelle séquence de contenu automatisée apporte le plus de valeur à vos prospects ?",
                    "options": [
                        "A) Envoyer le même post promotionnel chaque semaine",
                        "B) Créer une séquence : Conseil gratuit (J1) → Témoignage apprenant (J4) → Offre limitée (J10)",
                        "C) Publier uniquement quand vous avez du temps",
                        "D) Automatiser uniquement les posts du vendredi",
                    ],
                    "correct": "B",
                    "explanation": "Une séquence progressive apporte de la valeur d'abord (conseil), crée la confiance (témoignage) puis convertit (offre). C'est le principe du funnel de contenu automatisé.",
                },
                {
                    "id": 2,
                    "question": "Quel outil permet de créer une séquence de contenu qui s'adapte automatiquement selon le comportement de l'abonné ?",
                    "options": [
                        "A) Canva AI — pour les visuels uniquement",
                        "B) Buffer AI — uniquement pour programmer les posts",
                        "C) Mailchimp AI ou Brevo AI — séquences conditionnelles basées sur les actions",
                        "D) ChatGPT — pour rédiger les textes uniquement",
                    ],
                    "correct": "C",
                    "explanation": "Mailchimp AI et Brevo AI permettent des séquences conditionnelles : si l'abonné ouvre l'email A, il reçoit l'email B ; sinon il reçoit l'email C.",
                },
                {
                    "id": 3,
                    "question": "Vous créez une séquence pour le lancement d'une formation en ligne. Combien de contenus recommandez-vous sur 2 semaines ?",
                    "options": [
                        "A) 1 seul post d'annonce",
                        "B) 20 posts par jour",
                        "C) 6 à 8 contenus répartis sur 2 semaines — teasing, lancement, valeur, preuve, urgence, closing",
                        "D) 3 posts uniquement le jour J",
                    ],
                    "correct": "C",
                    "explanation": "6 à 8 contenus sur 2 semaines crée le bon rythme pour maintenir l'intérêt sans fatiguer l'audience. Chaque contenu a un rôle précis dans la séquence.",
                },
            ],
            "passing_score": 70,
        },
        hints_fr=[
            {"level": 1, "text": "Une séquence efficace suit la logique : Attirer → Engager → Convertir. Chaque contenu remplit une fonction précise."},
            {"level": 2, "text": "Timing idéal MENA : évitez les lundis matin et vendredis après-midi. Mardis et jeudis 18h-21h donnent les meilleurs résultats."},
        ],
    ))
    db.flush()

    l2_1_2 = Lesson(unit_id=u2_1.id, order=2,
        title_fr="Planifier 1 mois de contenu en 1 heure avec ChatGPT",
        title_en="Plan 1 month of content in 1 hour with ChatGPT",
        format="tutorial", difficulty_level=3, estimated_duration_min=60,
        prerequisite_lesson_id=l2_1_1.id,
        description_fr="Brief de marque, prompt calendrier mensuel, mix 40/30/30, validation MENA.", description_en="Brief de marque, prompt calendrier mensuel, mix 40/30/30, validation MENA.")
    db.add(l2_1_2); db.flush()
    db.add(Activity(lesson_id=l2_1_2.id, order=1, type="tutorial",
        title_fr="Tutoriel — Planifier 1 mois de contenu en 1 heure",
        is_assessed=False, is_required=True, content_fr={"duration_min": 60}))
    db.add(Activity(
        lesson_id=l2_1_2.id, order=2, type="exercise",
        title_fr="Projet noté — Mon calendrier de contenu mensuel AI complet",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": (
                "Créez un calendrier de contenu complet pour un mois entier avec ChatGPT.\n\n"
                "Étape 1 — Brief de marque (10 min) : choisissez une marque tunisienne, "
                "définissez secteur, cible, ton, objectif du mois, 3 mots clés.\n\n"
                "Étape 2 — Générer le calendrier (20 min) : prompt recommandé incluant "
                "mix 40% éducatif / 30% promotionnel / 30% communauté, "
                "2 réseaux (Facebook + Instagram), créneaux MENA.\n\n"
                "Étape 3 — Enrichir et valider (15 min) : vérifier l'équilibre, "
                "intégrer les événements locaux, ajouter au moins 1 post arabe/semaine.\n\n"
                "Étape 4 — Créer 5 visuels avec Canva AI.\n\n"
                "Étape 5 — Programmer 7 posts dans Buffer AI."
            ),
            "livrable": "Calendrier mensuel (20 posts min) + 5 visuels + screenshot Buffer AI + note stratégique 10 lignes.",
            "criteres": {
                "completude_calendrier": "25%",
                "qualite_contenu_genere": "30%",
                "adaptation_mena": "25%",
                "qualite_visuels_programmation": "20%",
            },
            "score_minimum": 70,
        },
        hints_fr=[
            {"level": 1, "text": "Plus le brief est précis, plus ChatGPT génère un calendrier pertinent. Donnez le maximum de contexte MENA."},
            {"level": 2, "text": "Créneaux optimaux MENA : Facebook → mardi/jeudi 19h-21h ; Instagram → lundi/mercredi/vendredi 18h-20h."},
            {"level": 3, "text": "Mix recommandé Tunisie : 40% éducatif (astuces, conseils), 30% promotionnel, 30% communauté (questions, sondages, témoignages)."},
        ],
        rubric_fr={"criteres": [
            {"nom": "Complétude du calendrier", "poids": 0.25, "description": "20 posts minimum, 4 semaines, 2 réseaux."},
            {"nom": "Qualité du contenu", "poids": 0.30, "description": "Mix respecté, pertinence culturelle, AR/FR."},
            {"nom": "Adaptation MENA", "poids": 0.25, "description": "Créneaux respectés, posts arabes, événements locaux."},
            {"nom": "Visuels et programmation", "poids": 0.20, "description": "5 visuels cohérents, Buffer AI configuré."},
        ]},
    ))
    db.flush()

    l2_1_3 = Lesson(unit_id=u2_1.id, order=3,
        title_fr="Automatiser les publications avec Buffer AI et Hootsuite AI",
        title_en="Automating publications with Buffer AI and Hootsuite AI",
        format="tutorial", difficulty_level=3, estimated_duration_min=30,
        prerequisite_lesson_id=l2_1_2.id,
        description_fr="Comparatif Buffer vs Hootsuite, workflow automatisé 7 jours, analyse des premières métriques.", description_en="Comparatif Buffer vs Hootsuite, workflow automatisé 7 jours, analyse des premières métriques.")
    db.add(l2_1_3); db.flush()
    db.add(Activity(lesson_id=l2_1_3.id, order=1, type="tutorial",
        title_fr="Tutoriel comparatif — Buffer AI vs Hootsuite AI",
        is_assessed=False, is_required=True, content_fr={"duration_min": 30}))
    db.add(Activity(
        lesson_id=l2_1_3.id, order=2, type="exercise",
        title_fr="Exercice — Configurer mon workflow d'automatisation complet",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": (
                "Partie 1 — Comparatif Buffer AI vs Hootsuite AI sur 6 critères : "
                "prix, facilité, réseaux, analytics, suggestions contenu, adapté PME MENA. "
                "Recommandez l'un pour 3 profils (freelance, PME, agence).\n\n"
                "Partie 2 — Workflow 7 jours : programmez 7 posts avec textes ChatGPT + visuels Canva AI "
                "aux créneaux optimaux MENA.\n\n"
                "Partie 3 — Après 48h : relevez les premières métriques et identifiez le meilleur type de post."
            ),
            "livrable": "Tableau comparatif + screenshot calendrier 7 jours + rapport métriques.",
            "criteres": {"qualite_comparatif": "30%", "completude_workflow_7j": "40%", "analyse_metriques": "30%"},
            "score_minimum": 70,
        },
        hints_fr=[
            {"level": 1, "text": "Testez vraiment les deux outils — l'expérience pratique vaut mieux qu'une recherche théorique."},
            {"level": 2, "text": "Buffer AI = freelances et PME. Hootsuite AI = agences multi-comptes."},
        ],
    ))
    db.flush()

    # ── Unité 2 — Analyser les données marketing AI ──────────────────────────
    u2_2 = Unit(module_id=m2.id, order=2,
        title_fr="Analyser les données marketing AI",
        title_en="Analysing AI Marketing Data",
        estimated_duration_min=34)
    db.add(u2_2); db.flush()

    l2_2_1 = Lesson(unit_id=u2_2.id, order=1,
        title_fr="Comprendre Google Analytics AI", title_en="Comprendre Google Analytics AI", format="video",
        difficulty_level=3, estimated_duration_min=12,
        description_fr="Métriques clés, taux de rebond mobile MENA, prédictions AI, 4 indicateurs essentiels.", description_en="Métriques clés, taux de rebond mobile MENA, prédictions AI, 4 indicateurs essentiels.")
    db.add(l2_2_1); db.flush()
    db.add(Activity(lesson_id=l2_2_1.id, order=1, type="video",
        title_fr="Vidéo — Comprendre Google Analytics AI",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(lesson_id=l2_2_1.id, order=2, type="quiz",
        title_fr="Quiz — Google Analytics AI",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "questions": [
                {
                    "id": 1,
                    "question": "Google Analytics AI vous montre un taux de rebond de 75% sur votre page d'accueil. Première action ?",
                    "options": [
                        "A) Désactiver Google Analytics",
                        "B) Analyser la vitesse de chargement et la clarté du message principal sur mobile",
                        "C) Doubler le budget publicitaire",
                        "D) Changer la couleur du site",
                    ],
                    "correct": "B",
                    "explanation": "75% de rebond : 3/4 des visiteurs partent sans interagir. En MENA, 70% du trafic est mobile — vitesse et lisibilité mobile sont les premières causes d'abandon.",
                },
                {
                    "id": 2,
                    "question": "Vos visiteurs passent 45s sur le blog mais 4 minutes sur la page témoignages. Que faites-vous ?",
                    "options": [
                        "A) Supprimer le blog",
                        "B) Créer plus de contenu témoignages et le mettre en avant dans la navigation",
                        "C) Raccourcir les articles à 45 secondes",
                        "D) Ignorer cette différence",
                    ],
                    "correct": "B",
                    "explanation": "4 minutes sur témoignages révèle un fort intérêt pour la preuve sociale. Dans la culture MENA, confiance et recommandations de pairs sont déterminantes.",
                },
                {
                    "id": 3,
                    "question": "L'AI prédit une baisse de trafic de 30% le mois prochain. Que faites-vous ?",
                    "options": [
                        "A) Paniquer et tout changer",
                        "B) Ignorer — l'AI se trompe",
                        "C) Analyser les causes possibles et préparer des actions préventives maintenant",
                        "D) Attendre la baisse",
                    ],
                    "correct": "C",
                    "explanation": "Les prédictions AI sont des signaux d'anticipation. La valeur est d'agir AVANT la baisse.",
                },
                {
                    "id": 4,
                    "question": "Quelle métrique indique le mieux la qualité de votre contenu marketing ?",
                    "options": [
                        "A) Nombre total de visiteurs",
                        "B) Temps moyen par page combiné au taux de conversion",
                        "C) Nombre de pages vues",
                        "D) Source de trafic principale",
                    ],
                    "correct": "B",
                    "explanation": "Temps moyen + taux de conversion est la combinaison la plus révélatrice : contenu engageant ET qui convertit.",
                },
            ],
            "passing_score": 70,
        },
        hints_fr=[
            {"level": 1, "text": "Google Analytics AI en MENA : 70% du trafic est mobile. Regardez toujours les métriques filtrées par mobile en premier."},
        ],
    ))
    db.flush()

    l2_2_2 = Lesson(unit_id=u2_2.id, order=2,
        title_fr="Lire et interpréter les insights marketing", title_en="Lire et interpréter les insights marketing", format="video",
        difficulty_level=3, estimated_duration_min=10,
        prerequisite_lesson_id=l2_2_1.id,
        description_fr="Tableau de bord multi-canaux, 3 insights actionnables, méthode donnée-interprétation-action.", description_en="Tableau de bord multi-canaux, 3 insights actionnables, méthode donnée-interprétation-action.")
    db.add(l2_2_2); db.flush()
    db.add(Activity(lesson_id=l2_2_2.id, order=1, type="video",
        title_fr="Vidéo — Lire et interpréter les insights marketing",
        is_assessed=False, is_required=True, content_fr={"duration_min": 10}))
    db.add(Activity(
        lesson_id=l2_2_2.id, order=2, type="exercise",
        title_fr="Exercice — Audit de performance de mes contenus",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": (
                "Tâche 1 — Collectez les données des 30 derniers jours sur toutes plateformes "
                "(Meta Business Suite + Mailchimp/Brevo).\n\n"
                "Tâche 2 — Tableau comparatif des 10 meilleurs et 5 moins bons contenus.\n\n"
                "Tâche 3 — 3 insights actionnables (donnée observée + interprétation + action à mener).\n\n"
                "Tâche 4 — Rédigez 3 nouveaux posts qui intègrent vos apprentissages."
            ),
            "livrable": "Tableau d'audit + 3 insights actionnables + 3 posts optimisés.",
            "criteres": {"rigueur_collecte": "30%", "pertinence_insights": "40%", "qualite_plan": "30%"},
            "score_minimum": 70,
        },
        hints_fr=[
            {"level": 1, "text": "Insight actionnable = donnée + interprétation + action concrète. Ex : 'Photos personnes réelles (+67% engagement) → créer 4 posts avec visages humains ce mois.'"},
        ],
    ))
    db.flush()

    l2_2_3 = Lesson(unit_id=u2_2.id, order=3,
        title_fr="Prendre des décisions basées sur les données — Cas PME tunisienne",
        title_en="Data-driven decisions — Tunisian SME case",
        format="case_study", difficulty_level=4, estimated_duration_min=45,
        prerequisite_lesson_id=l2_2_2.id,
        description_fr="Cas BioNatura : cosmétiques naturels Nabeul, audit complet données, stratégie data-driven.", description_en="Cas BioNatura : cosmétiques naturels Nabeul, audit complet données, stratégie data-driven.")
    db.add(l2_2_3); db.flush()
    db.add(Activity(
        lesson_id=l2_2_3.id, order=1, type="case_study",
        title_fr="Cas BioNatura — Décisions data-driven pour une marque bio tunisienne",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "contexte": "BioNatura est une marque tunisienne de cosmétiques naturels fondée à Nabeul en 2021.",
            "donnees": {
                "reseaux_sociaux": {"abonnes_facebook": 3200, "abonnes_instagram": 1850, "taux_engagement_moyen": "2.1%", "meilleur_post": "Tutoriel vidéo huile d'argan — 8 400 vues, 312 interactions", "pire_post": "Photo produit fond blanc — 45 interactions", "meilleur_creneau": "Mardi et jeudi 19h30-20h30"},
                "email_marketing": {"liste": "1 200 abonnées", "taux_ouverture": "19%", "taux_clic": "2.3%", "meilleur_objet": "'Votre peau mérite mieux ❤️' — 34%", "pire_objet": "'Newsletter BioNatura #4' — 9%"},
                "site_web": {"visiteurs_mensuel": 2800, "taux_rebond": "68%", "taux_conversion": "1.2%", "source_principale": "Facebook (52%), Direct (28%), Google (20%)"},
            },
            "questions": [
                {"id": 1, "question": "Analysez les données réseaux sociaux. Quels sont les 3 insights les plus importants et quelles actions immédiates Leila devrait-elle mener ?", "consigne": "Minimum 8 lignes avec chiffres."},
                {"id": 2, "question": "Le taux de rebond de 68% est préoccupant. Proposez 4 améliorations concrètes basées sur les données.", "consigne": "Pour chaque amélioration : problème, solution, outil AI."},
                {"id": 3, "question": "Rédigez 2 objets email A/B test pour BioNatura inspirés par les données.", "consigne": "Prompt ChatGPT + 2 objets + choix justifié."},
                {"id": 4, "question": "BioNatura veut doubler son CA en ligne en 6 mois. Proposez 5 actions prioritaires.", "consigne": "Chaque action : priorité, impact attendu, outil AI, délai."},
            ],
            "synthese": "En 12 lignes : plan des 30 premiers jours si vous étiez consultant de BioNatura.",
        },
    ))
    db.flush()

    # ── Unité 3 — Créer des publicités AI performantes ───────────────────────
    u2_3 = Unit(module_id=m2.id, order=3,
        title_fr="Créer des publicités AI performantes",
        title_en="Creating High-Performance AI Ads",
        estimated_duration_min=36)
    db.add(u2_3); db.flush()

    l2_3_1 = Lesson(unit_id=u2_3.id, order=1,
        title_fr="Facebook et Instagram Ads avec AI", title_en="Facebook et Instagram Ads avec AI", format="tutorial",
        difficulty_level=3, estimated_duration_min=12,
        description_fr="Advantage+ Audience AI, A/B test visuel humain vs produit, textes AR/FR, prévisions Meta AI.", description_en="Advantage+ Audience AI, A/B test visuel humain vs produit, textes AR/FR, prévisions Meta AI.")
    db.add(l2_3_1); db.flush()
    db.add(Activity(lesson_id=l2_3_1.id, order=1, type="tutorial",
        title_fr="Tutoriel — Facebook et Instagram Ads avec AI",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(
        lesson_id=l2_3_1.id, order=2, type="exercise",
        title_fr="Exercice — Créer ma première publicité Facebook/Instagram AI",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": (
                "Étape 1 — Objectif et cible : objectif, audience précise, budget simulé.\n"
                "Étape 2 — 2 visuels A/B (version A produit, version B personne/témoignage) en Canva AI.\n"
                "Étape 3 — Textes ChatGPT : titre (40 car), texte (125 car), description, CTA en AR et FR.\n"
                "Étape 4 — Configuration Advantage+ dans Meta + screenshot.\n"
                "Étape 5 — Analyser les prévisions Meta AI et commenter leur réalisme pour la Tunisie."
            ),
            "livrable": "Brief + 4 visuels + textes AR/FR + screenshot ciblage + analyse prévisions.",
            "criteres": {"precision_ciblage": "25%", "qualite_visuels_ab": "30%", "qualite_textes_bilingues": "30%", "analyse_previsions": "15%"},
            "score_minimum": 70,
        },
        hints_fr=[
            {"level": 1, "text": "Advantage+ Audience AI Meta donne souvent de meilleurs résultats que le ciblage manuel en Tunisie."},
            {"level": 2, "text": "Visuel avec visage humain surperforme de 20-40% en MENA — la confiance personnelle est clé."},
        ],
    ))
    db.flush()

    l2_3_2 = Lesson(unit_id=u2_3.id, order=2,
        title_fr="Google Ads avec AI", title_en="Google Ads avec AI", format="video",
        difficulty_level=3, estimated_duration_min=12,
        prerequisite_lesson_id=l2_3_1.id,
        description_fr="Performance Max AI, recherche mots clés AR/FR avec Semrush AI, assets texte optimisés, calcul ROI prévisionnel.", description_en="Performance Max AI, recherche mots clés AR/FR avec Semrush AI, assets texte optimisés, calcul ROI prévisionnel.")
    db.add(l2_3_2); db.flush()
    db.add(Activity(lesson_id=l2_3_2.id, order=1, type="video",
        title_fr="Vidéo — Google Ads avec AI",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(
        lesson_id=l2_3_2.id, order=2, type="exercise",
        title_fr="Exercice — Stratégie Google Ads AI pour le marché MENA",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": (
                "Partie 1 — Mots clés avec Semrush AI : 10 FR + 5 AR, volume, CPC, concurrence. "
                "Sélectionner 8 mots clés optimaux.\n\n"
                "Partie 2 — Structure campagne Performance Max : objectif, budget, groupes d'assets.\n\n"
                "Partie 3 — Assets texte ChatGPT : 3 titres courts, 3 titres longs, 2 descriptions en FR et AR.\n\n"
                "Partie 4 — Calcul ROI prévisionnel (clics prévus, conversions à 2%, valeur par conversion)."
            ),
            "livrable": "Liste mots clés + structure campagne + assets texte + calcul ROI.",
            "criteres": {"qualite_mots_cles": "35%", "structure_campagne": "25%", "qualite_assets": "25%", "rigueur_roi": "15%"},
            "score_minimum": 70,
        },
        hints_fr=[
            {"level": 1, "text": "Mots clés arabes en Tunisie : utilisez translittération ET caractères arabes — les deux formes sont utilisées."},
            {"level": 2, "text": "Performance Max recommandé pour PME tunisiennes : l'AI Google optimise sur tous les formats avec un seul budget."},
        ],
    ))
    db.flush()

    l2_3_3 = Lesson(unit_id=u2_3.id, order=3,
        title_fr="Ma campagne publicitaire MENA complète",
        title_en="My complete MENA advertising campaign",
        format="exercise", difficulty_level=4, estimated_duration_min=90,
        prerequisite_lesson_id=l2_3_2.id,
        description_fr="Projet intégrateur multicanal : Meta Ads + Google Ads + email de soutien + plan de pilotage.", description_en="Projet intégrateur multicanal : Meta Ads + Google Ads + email de soutien + plan de pilotage.")
    db.add(l2_3_3); db.flush()
    db.add(Activity(
        lesson_id=l2_3_3.id, order=1, type="exercise",
        title_fr="Projet noté — Ma campagne publicitaire MENA complète",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": (
                "Phase 1 — Stratégie : marque, objectif, budget 1 000 TND réparti (60% Meta / 30% Google / 10% email).\n\n"
                "Phase 2 — 2 pubs Meta distinctes (notoriété + conversion) avec visuels Canva AI et textes ChatGPT AR/FR.\n\n"
                "Phase 3 — Campagne Performance Max Google Ads avec 8 mots clés et assets complets.\n\n"
                "Phase 4 — Email de soutien avec objet optimisé, bannière Canva AI et CTA landing page.\n\n"
                "Phase 5 — Plan de pilotage : métriques par canal, fréquence d'analyse, critères de succès."
            ),
            "livrable": "Document stratégie + 2 pubs Meta + structure Google Ads + email + plan de pilotage.",
            "criteres": {"coherence_multicanale": "20%", "qualite_pubs_meta": "25%", "qualite_google": "25%", "qualite_email": "15%", "rigueur_pilotage": "15%"},
            "score_minimum": 70,
            "duree_estimee": "90 minutes",
        },
        hints_fr=[
            {"level": 1, "text": "Répartition budget MENA recommandée : 60% Facebook/Instagram, 30% Google, 10% Email."},
            {"level": 2, "text": "Retargeting Facebook très efficace en Tunisie : visiteurs du site 3x plus susceptibles de convertir."},
        ],
    ))
    db.flush()

    # ── Unité 4 — Stratégie de contenu AI avancée ────────────────────────────
    u2_4 = Unit(module_id=m2.id, order=4,
        title_fr="Stratégie de contenu AI avancée",
        title_en="Advanced AI Content Strategy",
        estimated_duration_min=38)
    db.add(u2_4); db.flush()

    l2_4_1 = Lesson(unit_id=u2_4.id, order=1,
        title_fr="SEO avec l'AI pour le marché MENA en arabe et français",
        title_en="SEO with AI for the MENA Market in Arabic and French",
        format="video", difficulty_level=3, estimated_duration_min=12,
        description_fr="Audit SEO Semrush AI, mots clés bilingues AR/FR, longue traîne MENA, optimisation contenu ChatGPT.", description_en="Audit SEO Semrush AI, mots clés bilingues AR/FR, longue traîne MENA, optimisation contenu ChatGPT.")
    db.add(l2_4_1); db.flush()
    db.add(Activity(lesson_id=l2_4_1.id, order=1, type="video",
        title_fr="Vidéo — SEO avec l'AI pour le marché MENA",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(
        lesson_id=l2_4_1.id, order=2, type="exercise",
        title_fr="Exercice — Optimiser une page web pour le SEO MENA avec l'AI",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": (
                "Étape 1 — Audit SEO : analysez une URL, identifiez 5 problèmes prioritaires.\n\n"
                "Étape 2 — Mots clés bilingues : 10 FR + 5 AR + 5 longue traîne MENA avec volume et concurrence.\n\n"
                "Étape 3 — Optimisation avec ChatGPT : H1 (FR+AR), méta-description (FR+AR, 160 car), premier paragraphe, 3 H2.\n\n"
                "Étape 4 — Plan éditorial SEO 3 mois : 6 articles avec titre, mot clé, intention, longueur, angle MENA."
            ),
            "livrable": "Audit + liste mots clés AR/FR + page optimisée + plan éditorial SEO.",
            "criteres": {"qualite_audit": "25%", "pertinence_mots_cles": "35%", "qualite_optimisation": "25%", "plan_editorial": "15%"},
            "score_minimum": 70,
        },
        hints_fr=[
            {"level": 1, "text": "SEO arabe Tunisie : arabe standard et français restent dominants pour requêtes professionnelles."},
            {"level": 2, "text": "Longue traîne MENA puissante : 'formation [métier] Tunisie', 'prix [service] Maroc' — moins de concurrence, intention forte."},
        ],
    ))
    db.flush()

    l2_4_2 = Lesson(unit_id=u2_4.id, order=2,
        title_fr="Créer des vidéos marketing avec Runway ML et ElevenLabs",
        title_en="Créer des vidéos marketing avec Runway ML et ElevenLabs",
        format="tutorial", difficulty_level=3, estimated_duration_min=30,
        prerequisite_lesson_id=l2_4_1.id,
        description_fr="Script ChatGPT, voix off ElevenLabs AR/FR, visuels Runway ML ou Canva AI, montage CapCut AI.", description_en="Script ChatGPT, voix off ElevenLabs AR/FR, visuels Runway ML ou Canva AI, montage CapCut AI.")
    db.add(l2_4_2); db.flush()
    db.add(Activity(lesson_id=l2_4_2.id, order=1, type="tutorial",
        title_fr="Tutoriel — Créer des vidéos marketing avec Runway ML et ElevenLabs",
        is_assessed=False, is_required=True, content_fr={"duration_min": 30}))
    db.add(Activity(
        lesson_id=l2_4_2.id, order=2, type="exercise",
        title_fr="Exercice — Créer ma première vidéo marketing AI",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": (
                "Étape 1 — Script ChatGPT (60s) : accroche, problème, solution, CTA.\n"
                "Étape 2 — Voix off ElevenLabs en français ou arabe, export MP3.\n"
                "Étape 3 — Visuels Canva AI (débutant) ou Runway ML (avancé) + montage CapCut AI.\n"
                "Étape 4 — Sous-titres automatiques AR/FR.\n"
                "Étape 5 — Export 3 formats : Stories 9:16, Feed 1:1, YouTube 16:9."
            ),
            "livrable": "Script + audio voix off + vidéo finale (1 format min) + 3 formats exportés.",
            "criteres": {"qualite_script": "25%", "qualite_voix_off": "25%", "qualite_montage": "30%", "adaptation_formats": "20%"},
            "score_minimum": 70,
        },
        hints_fr=[
            {"level": 1, "text": "ElevenLabs gratuit : 10 000 car/mois. Voix arabes : Farida (femme), Hamid (homme)."},
            {"level": 2, "text": "CapCut AI : sous-titres arabes essentiels — 40% des vidéos regardées sans son sur mobile MENA."},
        ],
    ))
    db.flush()

    l2_4_3 = Lesson(unit_id=u2_4.id, order=3,
        title_fr="Stratégie multicanale AI",
        title_en="AI multichannel strategy",
        format="exercise", difficulty_level=4, estimated_duration_min=90,
        prerequisite_lesson_id=l2_4_2.id,
        description_fr="Audit concurrents MENA, architecture 4 canaux simultanés, production d'échantillons, plan de pilotage mensuel.", description_en="Audit concurrents MENA, architecture 4 canaux simultanés, production d'échantillons, plan de pilotage mensuel.")
    db.add(l2_4_3); db.flush()
    db.add(Activity(
        lesson_id=l2_4_3.id, order=1, type="exercise",
        title_fr="Projet noté — Ma stratégie de contenu multicanale AI",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": (
                "Phase 1 — Audit 2 concurrents (canaux, fréquence, ton, forces/lacunes).\n\n"
                "Phase 2 — Architecture 4 canaux (Instagram 20 posts, Facebook 12, Email 4, Blog 2 articles) "
                "avec objectif, fréquence, ton, mix, KPIs par canal.\n\n"
                "Phase 3 — Production : 5 posts Instagram + 1 email complet + 1 article SEO 1000 mots.\n\n"
                "Phase 4 — Dashboard KPIs par canal, rythme de reporting, critères d'ajustement."
            ),
            "livrable": "Audit concurrents + architecture multicanale + échantillons produits + plan de pilotage.",
            "criteres": {"qualite_audit": "20%", "coherence_architecture": "25%", "qualite_production": "35%", "rigueur_pilotage": "20%"},
            "score_minimum": 70,
        },
        hints_fr=[
            {"level": 1, "text": "Audit concurrents MENA : Meta Business Suite onglet 'Pages à surveiller' + positions SEO Semrush."},
            {"level": 2, "text": "Cohérence multicanale : même message adapté au format. Lancement produit = 1 post Instagram émotionnel + 1 email informatif + 1 article détaillé + 1 pub conversion."},
        ],
    ))
    db.flush()

    # ── Unité 5 — Éthique AI Intermédiaire ───────────────────────────────────
    u2_5 = Unit(module_id=m2.id, order=5,
        title_fr="Éthique AI — Niveau Intermédiaire",
        title_en="AI Ethics — Intermediate Level",
        estimated_duration_min=26)
    db.add(u2_5); db.flush()

    l2_5_1 = Lesson(unit_id=u2_5.id, order=1,
        title_fr="Protection des données clients dans la région MENA",
        title_en="Protection des données clients dans la région MENA",
        format="video", difficulty_level=3, estimated_duration_min=12,
        description_fr="Lois MENA (Tunisie 2004-63, Maroc 09-08, UAE PDPL 2022), Meta Pixel, consentement, droit à l'effacement.", description_en="Lois MENA (Tunisie 2004-63, Maroc 09-08, UAE PDPL 2022), Meta Pixel, consentement, droit à l'effacement.")
    db.add(l2_5_1); db.flush()
    db.add(Activity(lesson_id=l2_5_1.id, order=1, type="video",
        title_fr="Vidéo — Protection des données clients dans la région MENA",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(lesson_id=l2_5_1.id, order=2, type="quiz",
        title_fr="Quiz — Protection des données marketing MENA",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "questions": [
                {
                    "id": 1,
                    "question": "Vous collectez des emails via un formulaire sur votre site tunisien. Quelle mention est obligatoire ?",
                    "options": [
                        "A) Aucune",
                        "B) Juste une case 'J'accepte les emails'",
                        "C) Comment les données seront utilisées et comment se désabonner",
                        "D) Le numéro du responsable marketing",
                    ],
                    "correct": "C",
                    "explanation": "La loi tunisienne 2004-63 exige une information claire sur l'usage des données et les droits de l'abonné.",
                },
                {
                    "id": 2,
                    "question": "Vous utilisez Meta Pixel. Que devez-vous obligatoirement faire ?",
                    "options": [
                        "A) Rien — Meta Pixel est invisible",
                        "B) Informer via bannière cookies que des données sont collectées pour la publicité",
                        "C) Seulement si plus de 10 000 visiteurs",
                        "D) Uniquement si vous revendez les données",
                    ],
                    "correct": "B",
                    "explanation": "Meta Pixel collecte des données comportementales. Bannière cookies avec option de refus obligatoire.",
                },
                {
                    "id": 3,
                    "question": "Un abonné demande la suppression de toutes ses données. Que faites-vous ?",
                    "options": [
                        "A) Ignorer",
                        "B) Désabonner seulement de la newsletter",
                        "C) Supprimer toutes ses données dans les 30 jours et confirmer par email",
                        "D) Lui demander de justifier",
                    ],
                    "correct": "C",
                    "explanation": "Le droit à l'effacement s'applique dans tout le MENA. Suppression complète obligatoire dans les 30 jours.",
                },
                {
                    "id": 4,
                    "question": "Votre email AI est ultra-personnalisé avec l'historique d'achat. Est-ce éthique ?",
                    "options": [
                        "A) Non — personnalisation automatique toujours intrusive",
                        "B) Oui, si l'abonné a consenti à l'utilisation de ces données",
                        "C) Oui, peu importe le consentement",
                        "D) Non — l'AI ne doit jamais utiliser les données d'achat",
                    ],
                    "correct": "B",
                    "explanation": "La personnalisation AI est éthique si elle repose sur un consentement éclairé et explicite.",
                },
            ],
            "passing_score": 70,
        },
        hints_fr=[
            {"level": 1, "text": "Règle simple : si votre client savait exactement comment vous utilisez ses données et n'était pas à l'aise, c'est probablement non éthique."},
            {"level": 2, "text": "Lois clés MENA : Tunisie (2004-63), Maroc (09-08), UAE (PDPL 2022), Arabie Saoudite (PDPL 2021)."},
        ],
    ))
    db.flush()

    l2_5_2 = Lesson(unit_id=u2_5.id, order=2,
        title_fr="Publicité responsable et éthique avec l'AI",
        title_en="Responsible and Ethical Advertising with AI",
        format="case_study", difficulty_level=3, estimated_duration_min=30,
        prerequisite_lesson_id=l2_5_1.id,
        description_fr="3 cas MENA : ciblage discriminatoire, deepfake publicitaire, surpersonnalisation anxiogène. Charte publicitaire AI.", description_en="3 cas MENA : ciblage discriminatoire, deepfake publicitaire, surpersonnalisation anxiogène. Charte publicitaire AI.")
    db.add(l2_5_2); db.flush()
    db.add(Activity(
        lesson_id=l2_5_2.id, order=1, type="case_study",
        title_fr="Cas pratiques — Publicité responsable avec l'AI en MENA",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "cas": [
                {
                    "id": 1,
                    "titre": "CAS 1 — Le ciblage discriminatoire",
                    "scenario": "Sana exclut des quartiers populaires de ses ciblages Meta Ads AI pour 'optimiser le ROI'.",
                    "question": "Quel problème éthique et légal a-t-elle créé ?",
                    "consigne": "Analyse éthique (5 lignes) + stratégie de ciblage alternative.",
                },
                {
                    "id": 2,
                    "titre": "CAS 2 — Le deepfake publicitaire",
                    "scenario": "Youssef génère une vidéo AI avec un 'chef célèbre fictif mais réaliste' qui recommande son restaurant.",
                    "question": "Où se situent les limites éthiques de l'AI générative en publicité ?",
                    "consigne": "Analyse + mention obligatoire à ajouter + version éthique.",
                },
                {
                    "id": 3,
                    "titre": "CAS 3 — La surpersonnalisation anxiogène",
                    "scenario": "Une app fitness cible les personnes en surpoids avec 'Vous avez pris X kg ce mois. Il est temps d'agir.'",
                    "question": "Pourquoi cette pratique est-elle problématique même si techniquement efficace ?",
                    "consigne": "Problème (5 lignes) + 3 messages alternatifs éthiques.",
                },
            ],
            "charte": "Rédigez en 10 lignes votre 'Charte de publicité AI responsable' : 5 engagements concrets.",
        },
    ))
    db.flush()

    # ════════════════════════════════════════════════════════════════════════
    # MODULE 3 — EXPERT
    # ════════════════════════════════════════════════════════════════════════

    # ── Unité 1 — Stratégie AI marketing globale ─────────────────────────────
    u3_1 = Unit(module_id=m3.id, order=1,
        title_fr="Stratégie AI marketing globale",
        title_en="Global AI Marketing Strategy",
        estimated_duration_min=42)
    db.add(u3_1); db.flush()

    l3_1_1 = Lesson(unit_id=u3_1.id, order=1,
        title_fr="Construire sa stratégie AI marketing", title_en="Construire sa stratégie AI marketing", format="video",
        difficulty_level=4, estimated_duration_min=15,
        description_fr="5 piliers stratégie AI marketing, diagnostic de maturité, matrice SWOT, feuille de route 90 jours.", description_en="5 piliers stratégie AI marketing, diagnostic de maturité, matrice SWOT, feuille de route 90 jours.")
    db.add(l3_1_1); db.flush()
    db.add(Activity(lesson_id=l3_1_1.id, order=1, type="video",
        title_fr="Vidéo — Construire sa stratégie AI marketing",
        is_assessed=False, is_required=True, content_fr={"duration_min": 15}))
    db.add(Activity(
        lesson_id=l3_1_1.id, order=2, type="exercise",
        title_fr="Exercice stratégique — Mon diagnostic de maturité AI marketing",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": (
                "Étape 1 — Grille de maturité (5 piliers, score 1-5) : outils AI, compétences équipe, "
                "qualité données, automatisation campagnes, culture data.\n\n"
                "Étape 2 — SWOT AI marketing dans le contexte MENA.\n\n"
                "Étape 3 — Feuille de route 90 jours (Mois 1 fondations, Mois 2 accélération, Mois 3 optimisation).\n\n"
                "Étape 4 — Cas business 12 lignes pour convaincre la direction."
            ),
            "livrable": "Grille maturité + SWOT + feuille de route 90j + cas business.",
            "criteres": {"rigueur_diagnostic": "25%", "qualite_swot": "20%", "realisme_feuille_route": "35%", "conviction_cas_business": "20%"},
            "score_minimum": 70,
        },
        hints_fr=[
            {"level": 1, "text": "Soyez honnête dans le diagnostic — un score surévalué mène à une feuille de route irréaliste."},
            {"level": 2, "text": "Quick wins Mois 1 typiques : activer ChatGPT pour contenu, configurer Buffer AI, lancer Meta Pixel + Google Analytics."},
        ],
    ))
    db.flush()

    l3_1_2 = Lesson(unit_id=u3_1.id, order=2,
        title_fr="Aligner le marketing AI avec les objectifs business", title_en="Aligner le marketing AI avec les objectifs business", format="video",
        difficulty_level=4, estimated_duration_min=12,
        prerequisite_lesson_id=l3_1_1.id,
        description_fr="KPIs marketing alignés sur objectifs business, modèle de croissance AI, cas TechEdu Maroc.", description_en="KPIs marketing alignés sur objectifs business, modèle de croissance AI, cas TechEdu Maroc.")
    db.add(l3_1_2); db.flush()
    db.add(Activity(lesson_id=l3_1_2.id, order=1, type="video",
        title_fr="Vidéo — Aligner le marketing AI avec les objectifs business",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(
        lesson_id=l3_1_2.id, order=2, type="case_study",
        title_fr="Cas pratique — Aligner la stratégie AI marketing de TechEdu Maroc",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "contexte": "TechEdu est une plateforme e-learning marocaine. Objectifs : 10 000 inscrits, 2M MAD CA, expansion Algérie et Tunisie.",
            "situation": "2 personnes marketing, budget 150 000 MAD/an, 8K Instagram, 3 500 newsletter, 5 000 visiteurs/mois, conversion 1.8%.",
            "questions": [
                {"id": 1, "question": "Comment aligner la stratégie AI marketing avec l'objectif 10 000 inscrits ?", "consigne": "3 piliers AI avec objectif, outil AI, KPI, budget."},
                {"id": 2, "question": "Expansion Algérie et Tunisie avec 20 000 MAD par marché. Stratégie AI ?", "consigne": "Plan par marché : canaux, adaptation culturelle, outils AI, métriques."},
                {"id": 3, "question": "Comment l'AI multiplie la productivité de 2 marketeurs par 3 ?", "consigne": "8 tâches à automatiser + temps économisé + redistribution."},
            ],
            "synthese": "Plan marketing AI annuel de TechEdu pour atteindre 10 000 inscrits en 15 lignes.",
        },
    ))
    db.flush()

    l3_1_3 = Lesson(unit_id=u3_1.id, order=3,
        title_fr="Présenter sa stratégie à la direction", title_en="Présenter sa stratégie à la direction", format="exercise",
        difficulty_level=5, estimated_duration_min=90,
        prerequisite_lesson_id=l3_1_2.id,
        description_fr="Pitch stratégique 12 slides, réponses aux 4 objections types (authenticité, compétences, ROI, remplacement équipe).", description_en="Pitch stratégique 12 slides, réponses aux 4 objections types (authenticité, compétences, ROI, remplacement équipe).")
    db.add(l3_1_3); db.flush()
    db.add(Activity(
        lesson_id=l3_1_3.id, order=1, type="exercise",
        title_fr="Projet — Présentation stratégie AI marketing à la direction",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": (
                "Préparez une présentation stratégique de 12 slides : "
                "contexte marché MENA, situation actuelle, concurrents AI, diagnostic maturité, "
                "vision 2027, 3 piliers stratégiques, feuille de route 90j, stack outils + budget, "
                "ROI projeté, gestion des risques, plan formation équipe, validation demandée.\n\n"
                "Réponses aux 4 objections : authenticité du contenu AI, compétences internes, "
                "preuve du ROI marketing digital, remplacement de l'équipe créative."
            ),
            "livrable": "Présentation 12 slides + document réponses aux 4 objections.",
            "criteres": {"structure_narrative": "25%", "solidite_arguments": "30%", "realisme_budget_roi": "25%", "qualite_objections": "20%"},
            "score_minimum": 70,
            "feedback": "mentor",
        },
        hints_fr=[
            {"level": 1, "text": "La direction pense en MAD/TND. Chaque slide doit répondre à : 'Qu'est-ce que ça nous rapporte ?'"},
            {"level": 2, "text": "Objection authenticité : l'AI crée la base, l'humain apporte l'âme. Montrez des exemples de marques MENA qui utilisent l'AI de façon transparente."},
        ],
    ))
    db.flush()

    # ── Unité 2 — Piloter une équipe marketing AI ────────────────────────────
    u3_2 = Unit(module_id=m3.id, order=2,
        title_fr="Piloter une équipe marketing AI",
        title_en="Leading an AI Marketing Team",
        estimated_duration_min=36)
    db.add(u3_2); db.flush()

    l3_2_1 = Lesson(unit_id=u3_2.id, order=1,
        title_fr="Former son équipe aux outils AI marketing", title_en="Former son équipe aux outils AI marketing", format="video",
        difficulty_level=4, estimated_duration_min=12,
        description_fr="Programme formation 4 semaines par profil, kit formateur, indicateurs d'adoption 30 jours.", description_en="Programme formation 4 semaines par profil, kit formateur, indicateurs d'adoption 30 jours.")
    db.add(l3_2_1); db.flush()
    db.add(Activity(lesson_id=l3_2_1.id, order=1, type="video",
        title_fr="Vidéo — Former son équipe aux outils AI marketing",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(
        lesson_id=l3_2_1.id, order=2, type="exercise",
        title_fr="Exercice — Concevoir le programme de formation AI marketing de mon équipe",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": (
                "Programme 4 semaines pour 4 profils (community manager, graphiste, chargé email, copywriter).\n"
                "Pour chaque semaine : thème, objectif, durée max 3h, format, outils, exercice, validation.\n\n"
                "Kit formateur : email d'invitation + grille évaluation avant/après + quiz validation 8 questions.\n\n"
                "Plan adoption 30 jours : indicateurs par profil, fréquence de suivi, célébration des succès."
            ),
            "livrable": "Programme 4 semaines + kit formateur + plan adoption.",
            "criteres": {"realisme_programme": "35%", "qualite_kit": "35%", "rigueur_adoption": "30%"},
            "score_minimum": 70,
        },
        hints_fr=[
            {"level": 1, "text": "Adaptez par profil : graphiste → Canva AI + Midjourney ; copywriter → ChatGPT + Jasper AI ; community manager → Buffer AI + Meta Business Suite."},
            {"level": 2, "text": "Semaine 1 recommandée : fondamentaux AI marketing tous ensembles pour créer la cohésion et une vision partagée."},
        ],
    ))
    db.flush()

    l3_2_2 = Lesson(unit_id=u3_2.id, order=2,
        title_fr="Orchestrer humains et AI dans le marketing", title_en="Orchestrer humains et AI dans le marketing", format="video",
        difficulty_level=4, estimated_duration_min=10,
        prerequisite_lesson_id=l3_2_1.id,
        description_fr="Matrice 4 quadrants 20 tâches, redéfinition des rôles par profil, workflow quotidien AI+Marketeur.", description_en="Matrice 4 quadrants 20 tâches, redéfinition des rôles par profil, workflow quotidien AI+Marketeur.")
    db.add(l3_2_2); db.flush()
    db.add(Activity(lesson_id=l3_2_2.id, order=1, type="video",
        title_fr="Vidéo — Orchestrer humains et AI dans le marketing",
        is_assessed=False, is_required=True, content_fr={"duration_min": 10}))
    db.add(Activity(
        lesson_id=l3_2_2.id, order=2, type="exercise",
        title_fr="Simulation — Workflow optimal AI + Équipe marketing",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": (
                "Partie 1 — Matrice 4 quadrants : 20 tâches marketing classées en "
                "AI seul / AI+Humain / Humain seul / À supprimer.\n\n"
                "Partie 2 — Évolution des rôles : tâches disparaissant, nouvelles compétences, "
                "comment présenter positivement.\n\n"
                "Partie 3 — Workflow quotidien idéal d'un marketeur AI (matin, pendant, soir)."
            ),
            "livrable": "Matrice 4 quadrants + analyse évolution rôles + workflow quotidien.",
            "criteres": {"pertinence_classification": "35%", "coherence_evolution": "35%", "praticite_workflow": "30%"},
            "score_minimum": 70,
        },
        hints_fr=[
            {"level": 1, "text": "AI seul : programmer posts, générer premières versions textes, analyser métriques, envoyer emails automatiques."},
            {"level": 2, "text": "Humain seul : définir stratégie de marque, construire relations influenceurs, gérer crises, décisions créatives finales."},
        ],
    ))
    db.flush()

    l3_2_3 = Lesson(unit_id=u3_2.id, order=3,
        title_fr="Maintenir l'authenticité de la marque avec l'AI",
        title_en="Maintaining brand authenticity with AI — Real Tunisian agency case",
        format="case_study", difficulty_level=5, estimated_duration_min=45,
        prerequisite_lesson_id=l3_2_2.id,
        description_fr="Cas Pixel Creative Tunisie : crise d'identité après adoption massive AI, Brand Voice Guide, nouveau process de création.", description_en="Cas Pixel Creative Tunisie : crise d'identité après adoption massive AI, Brand Voice Guide, nouveau process de création.")
    db.add(l3_2_3); db.flush()
    db.add(Activity(
        lesson_id=l3_2_3.id, order=1, type="case_study",
        title_fr="Cas agence Pixel Creative — Authenticité de marque avec l'AI",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "contexte": "Pixel Creative, agence marketing tunisienne, perd l'authenticité de ses marques après adoption massive AI. Clients : 'tous les posts se ressemblent'.",
            "problemes": ["Textes ChatGPT style générique", "Visuels Canva AI ressemblent aux concurrents", "L'équipe copie-colle sans personnaliser", "Direction artistique humaine disparue"],
            "questions": [
                {"id": 1, "question": "Causes profondes de la perte d'authenticité. Comment l'AI amplifie plutôt que noie la voix de marque ?", "consigne": "8 lignes, distinguer problème process vs compétences."},
                {"id": 2, "question": "Créez un 'Brand Voice Guide AI' pour une marque tunisienne : comment briefer ChatGPT et Canva AI pour respecter l'ADN de la marque ?", "consigne": "Guide 1 page : ton, mots à utiliser/éviter, style visuel, prompts brandés."},
                {"id": 3, "question": "Proposez un nouveau process de création de contenu AI qui garantit l'authenticité.", "consigne": "Workflow 5 étapes avec rôle humain ET rôle AI à chaque étape."},
            ],
        },
    ))
    db.flush()

    # ── Unité 3 — Mesurer le ROI du marketing AI ─────────────────────────────
    u3_3 = Unit(module_id=m3.id, order=3,
        title_fr="Mesurer le ROI du marketing AI",
        title_en="Measuring AI Marketing ROI",
        estimated_duration_min=36)
    db.add(u3_3); db.flush()

    l3_3_1 = Lesson(unit_id=u3_3.id, order=1,
        title_fr="Calculer le retour sur investissement marketing AI", title_en="Calculer le retour sur investissement marketing AI", format="video",
        difficulty_level=4, estimated_duration_min=12,
        description_fr="Méthodologie ROI marketing AI, gain productivité + économies + revenus additionnels, KPI le plus convaincant pour la direction.", description_en="Méthodologie ROI marketing AI, gain productivité + économies + revenus additionnels, KPI le plus convaincant pour la direction.")
    db.add(l3_3_1); db.flush()
    db.add(Activity(lesson_id=l3_3_1.id, order=1, type="video",
        title_fr="Vidéo — Calculer le ROI marketing AI",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(
        lesson_id=l3_3_1.id, order=2, type="quiz",
        title_fr="Quiz — ROI du marketing AI",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "questions": [
                {
                    "id": 1,
                    "question": "2 marketeurs économisent 2h/jour grâce à l'AI. Coût horaire 20 TND. Gain mensuel (22 jours) ?",
                    "options": ["A) 880 TND", "B) 1 760 TND", "C) 440 TND", "D) 3 520 TND"],
                    "correct": "B",
                    "explanation": "2 × 2h × 22j × 20 TND = 1 760 TND/mois. Sur 12 mois = 21 120 TND/an vs coût outils AI ~2 000-4 000 TND/an.",
                },
                {
                    "id": 2,
                    "question": "Avant AI : 20 posts/mois coût 800 TND. Avec AI : 60 posts/mois coût 150 TND. ROI ?",
                    "options": ["A) 50%", "B) 233%", "C) 433%", "D) 167%"],
                    "correct": "C",
                    "explanation": "(800-150)/150 × 100 = 433% de ROI sur la production de contenu.",
                },
                {
                    "id": 3,
                    "question": "Quel indicateur prouve le mieux le ROI d'une campagne de contenu AI à la direction ?",
                    "options": [
                        "A) Nombre de posts publiés",
                        "B) Nombre de followers gagnés",
                        "C) Coût par lead qualifié généré par contenu AI vs contenu traditionnel",
                        "D) Taux d'engagement moyen",
                    ],
                    "correct": "C",
                    "explanation": "Le coût par lead qualifié relie directement le contenu marketing à un résultat business mesurable.",
                },
            ],
            "passing_score": 70,
        },
        hints_fr=[
            {"level": 1, "text": "ROI = (Gains - Coût outils AI) / Coût outils AI × 100. Incluez gain de temps ET revenus additionnels."},
        ],
    ))
    db.flush()

    l3_3_2 = Lesson(unit_id=u3_3.id, order=2,
        title_fr="Créer son tableau de bord marketing AI", title_en="Créer son tableau de bord marketing AI", format="tutorial",
        difficulty_level=4, estimated_duration_min=60,
        prerequisite_lesson_id=l3_3_1.id,
        description_fr="Looker Studio gratuit, connexion Google Analytics + Meta + Mailchimp, KPIs par rôle, rapport hebdomadaire automatique.", description_en="Looker Studio gratuit, connexion Google Analytics + Meta + Mailchimp, KPIs par rôle, rapport hebdomadaire automatique.")
    db.add(l3_3_2); db.flush()
    db.add(Activity(
        lesson_id=l3_3_2.id, order=1, type="exercise",
        title_fr="Tutoriel — Créer mon tableau de bord marketing AI dans Looker Studio",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "steps": [
                "Créer un tableau de bord Looker Studio (Data Studio) gratuit connecté à Google Analytics",
                "Ajouter widgets réseaux sociaux : portée, engagement, croissance abonnés par réseau",
                "Intégrer métriques email : taux d'ouverture, taux de clic, désabonnements",
                "Configurer widget 'Acquisition' : sources de trafic et taux de conversion par canal",
                "Ajouter widget ROI : coût outils AI vs revenus générés par le marketing",
                "Configurer envoi automatique hebdomadaire à la direction",
            ],
            "consigne": "Créez le dashboard, soumettez screenshot (6 widgets minimum), rédigez note 10 lignes sur l'utilisation en réunion marketing.",
            "livrable": "Screenshot dashboard + note 10 lignes.",
            "criteres": {"completude_dashboard": "40%", "pertinence_kpis": "35%", "qualite_note": "25%"},
            "score_minimum": 70,
        },
        hints_fr=[
            {"level": 1, "text": "Looker Studio est gratuit et se connecte nativement à Google Analytics et Google Ads. Connecteurs Meta et Mailchimp disponibles via intégrations tierces."},
            {"level": 2, "text": "KPIs dashboard MENA : portée organique hebdomadaire, CPC par canal, taux d'ouverture email, taux de conversion site, ROI campagnes."},
        ],
    ))
    db.flush()

    l3_3_3 = Lesson(unit_id=u3_3.id, order=3,
        title_fr="Présenter les résultats à la direction", title_en="Présenter les résultats à la direction", format="exercise",
        difficulty_level=5, estimated_duration_min=90,
        prerequisite_lesson_id=l3_3_2.id,
        description_fr="Rapport trimestriel avec données avant/après fournies, calcul ROI détaillé, recommandations trimestre suivant.", description_en="Rapport trimestriel avec données avant/après fournies, calcul ROI détaillé, recommandations trimestre suivant.")
    db.add(l3_3_3); db.flush()
    db.add(Activity(
        lesson_id=l3_3_3.id, order=1, type="exercise",
        title_fr="Projet — Rapport de performance marketing AI trimestriel",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "scenario": (
                "Données avant AI : 8 posts/mois, 1 200 abonnés Instagram, engagement 1.8%, "
                "ouverture email 18%, 2 000 visiteurs/mois, coût contenu 1 200 TND/mois.\n\n"
                "Données après AI (3 mois) : 28 posts/mois, 3 400 abonnés, engagement 4.2%, "
                "ouverture email 31%, 5 800 visiteurs/mois, coût contenu 350 TND/mois, "
                "145 leads générés vs 38 avant AI."
            ),
            "consigne": (
                "Section 1 — Résumé exécutif : 3 chiffres clés, ROI calculé, conclusion.\n"
                "Section 2 — Analyse KPIs par canal avec commentaires.\n"
                "Section 3 — Calcul ROI complet + projection 12 mois.\n"
                "Section 4 — 3 recommandations prioritaires + 1 risque + budget supplémentaire."
            ),
            "livrable": "Rapport 4-6 pages + présentation 5 slides pour la direction.",
            "criteres": {"qualite_resume": "20%", "rigueur_analyse": "30%", "exactitude_roi": "25%", "pertinence_recommandations": "25%"},
            "score_minimum": 70,
            "feedback": "mentor",
        },
        hints_fr=[
            {"level": 1, "text": "Calcul ROI : économie production (850 TND × 3) + valeur leads additionnels (107 leads × valeur unitaire). Coût = 350 TND × 3 = 1 050 TND."},
        ],
    ))
    db.flush()

    # ── Unité 4 — Marketing AI avancé MENA ───────────────────────────────────
    u3_4 = Unit(module_id=m3.id, order=4,
        title_fr="Marketing AI avancé Afrique du Nord",
        title_en="Advanced AI Marketing North Africa",
        estimated_duration_min=40)
    db.add(u3_4); db.flush()

    l3_4_1 = Lesson(unit_id=u3_4.id, order=1,
        title_fr="Campagnes culturelles MENA : Ramadan, Aïd, événements locaux",
        title_en="Campagnes culturelles MENA : Ramadan, Aïd, événements locaux",
        format="video", difficulty_level=4, estimated_duration_min=15,
        description_fr="Calendrier saisonnier MENA, timing Ramadan (après Iftar), prompts spécialisés, projet campagne Ramadan complète.", description_en="Calendrier saisonnier MENA, timing Ramadan (après Iftar), prompts spécialisés, projet campagne Ramadan complète.")
    db.add(l3_4_1); db.flush()
    db.add(Activity(lesson_id=l3_4_1.id, order=1, type="video",
        title_fr="Vidéo — Campagnes culturelles MENA",
        is_assessed=False, is_required=True, content_fr={"duration_min": 15}))
    db.add(Activity(
        lesson_id=l3_4_1.id, order=2, type="exercise",
        title_fr="Projet — Ma campagne Ramadan AI complète",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": (
                "Phase 1 — Stratégie Ramadan : marque, message central, calendrier (pré-Ramadan, début, milieu, Laylat Al Qadr, Aïd).\n\n"
                "Phase 2 — Contenu : 5 posts Instagram AR/FR + visuel Laylat Al Qadr + email Ramadan Kareem + post Aïd El Fitr.\n\n"
                "Phase 3 — Analyse culturelle : choix culturels (couleurs, formules, timing) + 3 erreurs à éviter.\n\n"
                "Phase 4 — Calendrier de publication avec créneaux Ramadan (après Iftar)."
            ),
            "livrable": "Stratégie + 8 contenus créés + analyse culturelle + calendrier.",
            "criteres": {"pertinence_strategie": "25%", "qualite_contenus": "35%", "justesse_culturelle": "25%", "coherence_calendrier": "15%"},
            "score_minimum": 70,
        },
        hints_fr=[
            {"level": 1, "text": "Timing Ramadan MENA : engagement explose après l'Iftar (19h-22h). Meilleures publications de l'année souvent publiées durant Ramadan."},
            {"level": 2, "text": "Prompt ChatGPT Ramadan : 'Respecte ton chaleureux et familial, formules traditionnelles (رمضان كريم), évite contenu alimentaire avant l'Iftar.'"},
        ],
    ))
    db.flush()

    l3_4_2 = Lesson(unit_id=u3_4.id, order=2,
        title_fr="Marketing en arabe dialectal avec l'AI", title_en="Marketing en arabe dialectal avec l'AI", format="video",
        difficulty_level=4, estimated_duration_min=12,
        prerequisite_lesson_id=l3_4_1.id,
        description_fr="Dialectes MENA (tunisien, marocain, égyptien), code-switching FR+dialecte, prompts pour arabe dialectal authentique.", description_en="Dialectes MENA (tunisien, marocain, égyptien), code-switching FR+dialecte, prompts pour arabe dialectal authentique.")
    db.add(l3_4_2); db.flush()
    db.add(Activity(lesson_id=l3_4_2.id, order=1, type="video",
        title_fr="Vidéo — Marketing en arabe dialectal avec l'AI",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(
        lesson_id=l3_4_2.id, order=2, type="exercise",
        title_fr="Exercice — Créer du contenu en dialecte arabe avec ChatGPT",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": (
                "Partie 1 — Tableau comparatif 10 expressions marketing en 3 dialectes (tunisien, marocain, égyptien) + arabe standard.\n\n"
                "Partie 2 — Tester 3 approches pour dialecte tunisien et recommander la meilleure.\n\n"
                "Partie 3 — 3 posts Instagram en dialecte tunisien (humoristique, promotionnel FR+dialecte, communauté).\n\n"
                "Partie 4 — Validation culturelle de chaque post."
            ),
            "livrable": "Tableau dialectes + analyse 3 approches + 3 posts dialecte + validation.",
            "criteres": {"qualite_tableau": "25%", "pertinence_analyse": "25%", "authenticite_posts": "35%", "rigueur_validation": "15%"},
            "score_minimum": 70,
        },
        hints_fr=[
            {"level": 1, "text": "Code-switching FR+dialecte très naturel en Tunisie et Maroc — souvent plus authentique qu'arabe pur ou français pur."},
            {"level": 2, "text": "ChatGPT 4 gère mieux le dialecte. Améliorer avec few-shot prompting : donnez des exemples de votre dialecte cible dans le prompt."},
        ],
    ))
    db.flush()

    l3_4_3 = Lesson(unit_id=u3_4.id, order=3,
        title_fr="L'avenir du marketing AI en MENA", title_en="L'avenir du marketing AI en MENA", format="video",
        difficulty_level=4, estimated_duration_min=12,
        prerequisite_lesson_id=l3_4_2.id,
        description_fr="Tendances 2025-2027, métiers marketing les plus transformés, compétences rares que l'AI ne remplace pas.", description_en="Tendances 2025-2027, métiers marketing les plus transformés, compétences rares que l'AI ne remplace pas.")
    db.add(l3_4_3); db.flush()
    db.add(Activity(lesson_id=l3_4_3.id, order=1, type="video",
        title_fr="Vidéo — L'avenir du marketing AI en MENA",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(
        lesson_id=l3_4_3.id, order=2, type="forum_discussion",
        title_fr="Forum — Ma vision du marketing AI en MENA en 2028",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "question": (
                "3 dimensions :\n"
                "1) Quel métier marketing va le plus se transformer dans les 2 ans ?\n"
                "2) Quelle sera la compétence marketing la plus rare et précieuse en 2028 que l'AI ne peut pas remplacer ?\n"
                "3) Quelle opportunité unique le marché MENA offre-t-il aux marketeurs AI locaux ?"
            ),
            "consigne": "Minimum 15 lignes. Commentez 2 autres apprenants de façon constructive.",
        },
    ))
    db.flush()

    # ── Unité 5 — Gouvernance et Éthique AI Expert ────────────────────────────
    u3_5 = Unit(module_id=m3.id, order=5,
        title_fr="Gouvernance et Éthique AI — Niveau Expert",
        title_en="AI Governance and Ethics — Expert Level",
        estimated_duration_min=28)
    db.add(u3_5); db.flush()

    l3_5_1 = Lesson(unit_id=u3_5.id, order=1,
        title_fr="Créer sa politique marketing AI", title_en="Créer sa politique marketing AI", format="video",
        difficulty_level=5, estimated_duration_min=12,
        description_fr="8 sections d'une politique marketing AI, usages autorisés vs interdits, transparence clients, processus de validation contenu.", description_en="8 sections d'une politique marketing AI, usages autorisés vs interdits, transparence clients, processus de validation contenu.")
    db.add(l3_5_1); db.flush()
    db.add(Activity(lesson_id=l3_5_1.id, order=1, type="video",
        title_fr="Vidéo — Créer sa politique marketing AI",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(
        lesson_id=l3_5_1.id, order=2, type="exercise",
        title_fr="Projet — Rédiger la politique marketing AI de mon agence/entreprise",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": (
                "Document officiel en 8 sections :\n"
                "1. Préambule (valeurs). 2. Usages autorisés (10 min). 3. Usages interdits (6 min, ex : deepfakes, faux avis, stats inventées, ciblage discriminatoire). "
                "4. Transparence clients. 5. Droits d'auteur et IP. 6. Protection données clients. "
                "7. Processus de validation. 8. Mise à jour."
            ),
            "livrable": "Politique marketing AI officielle de 4 à 6 pages.",
            "criteres": {"completude_8_sections": "25%", "pertinence_interdictions": "30%", "rigueur_transparence": "25%", "operationnalite": "20%"},
            "score_minimum": 70,
        },
        hints_fr=[
            {"level": 1, "text": "Une bonne politique n'est pas un document juridique — c'est un guide pratique que votre équipe va vraiment utiliser."},
            {"level": 2, "text": "Interdictions clés en marketing MENA : deepfakes célébrités, faux avis Google, statistiques inventées, ciblage discriminatoire, contenu inapproprié aux valeurs culturelles."},
        ],
    ))
    db.flush()

    l3_5_2 = Lesson(unit_id=u3_5.id, order=2,
        title_fr="Gérer les crises de réputation liées à l'AI",
        title_en="Managing AI-related reputation crises",
        format="case_study", difficulty_level=5, estimated_duration_min=50,
        prerequisite_lesson_id=l3_5_1.id,
        description_fr="2 simulations de crise : publicité AI discriminatoire et contenu culturellement offensant pendant Ramadan. Plan de prévention.", description_en="2 simulations de crise : publicité AI discriminatoire et contenu culturellement offensant pendant Ramadan. Plan de prévention.")
    db.add(l3_5_2); db.flush()
    db.add(Activity(
        lesson_id=l3_5_2.id, order=1, type="case_study",
        title_fr="Simulation de crise — 2 scénarios de crise de réputation AI",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "scenarios": [
                {
                    "id": 1,
                    "titre": "CRISE 1 — La publicité discriminatoire AI",
                    "scenario": "Une pub AI exclut des quartiers populaires. Article journalistique partagé 5 000 fois en 4h.",
                    "questions": [
                        {"q": "5 premières actions dans les 2 heures.", "consigne": "Liste priorisée."},
                        {"q": "Post de crise officiel sur Instagram.", "consigne": "Transparent, empathique, 200 mots max."},
                        {"q": "3 mesures pour améliorer le process de validation AI.", "consigne": "Concrètes et immédiates."},
                    ],
                },
                {
                    "id": 2,
                    "titre": "CRISE 2 — Le contenu AI culturellement offensant",
                    "scenario": "Post AI publié pendant Ramadan avec photo de nourriture + mauvais usage d'une formule religieuse. 200 commentaires négatifs en 1h.",
                    "questions": [
                        {"q": "Plan d'action heure par heure sur les 6 premières heures.", "consigne": "Chronologique et précis."},
                        {"q": "Réponse officielle aux commentaires.", "consigne": "Empathique en arabe et français."},
                        {"q": "5 règles AI spécifiques pour les contenus Ramadan.", "consigne": "Avec exemples."},
                    ],
                },
            ],
            "plan_prevention": "Plan de prévention des crises AI marketing : 5 mesures concrètes à mettre en place dès demain.",
        },
    ))
    db.flush()


    # ════════════════════════════════════════════════════════════════════════
    # UNITÉ 6 — CERTIFICATION FINALE ✅
    # ════════════════════════════════════════════════════════════════════════

    u3_cert = Unit(
        module_id=m3.id, order=6,
        title_fr="Certification Finale — AI Marketing Strategist",
        title_en="Final Certification — AI Marketing Strategist",
        description_fr=(
            "Validation finale des compétences acquises sur les 3 modules. "
            "Test de 20 questions, projet complet et présentation devant le jury Euklydia."
        ),
        description_en=(
            "Final validation of skills acquired across the 3 modules. "
            "20-question test, complete project and Euklydia jury presentation."
        ),
        estimated_duration_min=90,
        is_active=True,
    )
    db.add(u3_cert); db.flush()

    # ── Leçon Cert.1 — Test 20 questions ─────────────────────────────────────
    l3_cert_1 = Lesson(
        unit_id=u3_cert.id, order=1,
        title_fr="Test de certification — 20 questions",
        title_en="Certification test — 20 questions",
        format="quiz", difficulty_level=5, estimated_duration_min=30,
        description_fr="Test final couvrant les 3 modules. Score minimum : 80% (16/20). Débloque le projet de certification.",
        description_en="Final test covering all 3 modules. Minimum score: 80% (16/20). Unlocks the certification project.",
    )
    db.add(l3_cert_1); db.flush()

    db.add(Activity(
        lesson_id=l3_cert_1.id, order=1, type="quiz",
        title_fr="Test final de certification — AI Marketing Strategist",
        title_en="Final certification test — AI Marketing Strategist",
        is_assessed=True, is_required=True, passing_score=80,
        content_fr={
            "instructions": "Ce test couvre les 3 modules. 30 minutes. Score minimum : 16/20 (80%) pour accéder au projet.",
            "questions": [
                # ── Module 1 — Fondations ──
                {"id": 1, "question": "Quel est le principal avantage du marketing AI pour une PME tunisienne ?",
                 "options": ["A) L'AI remplace tous les employés", "B) Produire du contenu professionnel à moindre coût", "C) L'AI garantit automatiquement les ventes", "D) L'AI élimine le besoin de connaître sa cible"],
                 "correct": "B", "explanation": "L'AI permet de produire du contenu professionnel à moindre coût.", "module": 1},
                {"id": 2, "question": "Quel outil AI gratuit recommandez-vous pour démarrer la création de visuels ?",
                 "options": ["A) Jasper AI", "B) Canva AI", "C) Hootsuite AI", "D) Klaviyo AI"],
                 "correct": "B", "explanation": "Canva AI propose une version gratuite puissante pour créer des visuels professionnels.", "module": 1},
                {"id": 3, "question": "Vous utilisez Midjourney version gratuite pour une campagne commerciale. C'est :",
                 "options": ["A) Parfaitement légal", "B) Une violation des CGU", "C) Légal si modifié dans Canva", "D) Légal en Tunisie"],
                 "correct": "B", "explanation": "La version gratuite Midjourney n'accorde pas les droits commerciaux.", "module": 1},
                {"id": 4, "question": "Brevo AI montre que vos clients ouvrent leurs emails le soir. Que faites-vous ?",
                 "options": ["A) Abandonner l'email marketing", "B) Continuer le matin", "C) Reprogrammer le soir et personnaliser les objets avec l'AI", "D) Réduire les envois"],
                 "correct": "C", "explanation": "Optimiser le timing et personnaliser les objets sont les deux leviers principaux.", "module": 1},
                {"id": 5, "question": "Meta Business Suite AI montre que vos posts avec images reçoivent 3x plus d'engagement. Que faites-vous ?",
                 "options": ["A) Continuer à publier du texte", "B) Adapter la stratégie pour créer plus de visuels avec Canva AI", "C) Ignorer ces données", "D) Supprimer les anciens posts texte"],
                 "correct": "B", "explanation": "Un bon AI Marketing Strategist réagit aux données et adapte sa stratégie.", "module": 1},
                # ── Module 2 — Pratique ──
                {"id": 6, "question": "Vous créez une séquence de contenu pour un lancement. Combien de contenus sur 2 semaines ?",
                 "options": ["A) 1 seul post", "B) 20 posts par jour", "C) 6 à 8 contenus répartis", "D) 3 posts le jour J"],
                 "correct": "C", "explanation": "6 à 8 contenus sur 2 semaines crée le bon rythme sans fatiguer l'audience.", "module": 2},
                {"id": 7, "question": "Google Analytics AI montre un taux de rebond de 75%. Première action ?",
                 "options": ["A) Désactiver GA", "B) Analyser vitesse de chargement et clarté sur mobile", "C) Doubler le budget pub", "D) Changer la couleur du site"],
                 "correct": "B", "explanation": "75% rebond = 3/4 des visiteurs partent. En Afrique du Nord, 70% du trafic est mobile.", "module": 2},
                {"id": 8, "question": "Un abonné demande la suppression de toutes ses données. Que faites-vous ?",
                 "options": ["A) Ignorer", "B) Désabonner uniquement", "C) Supprimer toutes ses données dans les 30 jours et confirmer", "D) Demander de justifier"],
                 "correct": "C", "explanation": "Le droit à l'effacement s'applique dans tout le MENA. Délai : 30 jours maximum.", "module": 2},
                {"id": 9, "question": "Avant AI : 20 posts/mois coût 800 TND. Avec AI : 60 posts/mois coût 150 TND. ROI ?",
                 "options": ["A) 50%", "B) 233%", "C) 433%", "D) 167%"],
                 "correct": "C", "explanation": "(800-150)/150 × 100 = 433% ROI sur la production de contenu.", "module": 2},
                {"id": 10, "question": "Quelle combinaison prouve le mieux la qualité du contenu marketing AI ?",
                 "options": ["A) Nombre de visiteurs", "B) Temps moyen par page combiné au taux de conversion", "C) Pages vues", "D) Source de trafic principale"],
                 "correct": "B", "explanation": "Temps moyen + taux conversion = contenu engageant ET qui convertit.", "module": 2},
                # ── Module 3 — Expert ──
                {"id": 11, "question": "Quelle est la première étape d'un diagnostic de maturité AI marketing ?",
                 "options": ["A) Choisir les outils AI", "B) Former l'équipe", "C) Évaluer les 5 piliers : outils, compétences, données, automatisation, culture data", "D) Lancer une campagne test"],
                 "correct": "C", "explanation": "Le diagnostic maturité sur 5 piliers révèle les lacunes avant toute action.", "module": 3},
                {"id": 12, "question": "Quel indicateur prouve le mieux le ROI d'une campagne de contenu AI à la direction ?",
                 "options": ["A) Nombre de posts publiés", "B) Nombre de followers", "C) Coût par lead qualifié généré par contenu AI vs traditionnel", "D) Taux d'engagement moyen"],
                 "correct": "C", "explanation": "Le coût par lead qualifié relie directement le contenu marketing à un résultat business.", "module": 3},
                {"id": 13, "question": "2 marketeurs économisent 2h/jour. Coût horaire 20 TND, 22 jours ouvrés. Gain mensuel ?",
                 "options": ["A) 880 TND", "B) 1 760 TND", "C) 440 TND", "D) 3 520 TND"],
                 "correct": "B", "explanation": "2 × 2h × 22j × 20 TND = 1 760 TND/mois.", "module": 3},
                {"id": 14, "question": "Quel timing est optimal pour publier pendant Ramadan en Afrique du Nord ?",
                 "options": ["A) Matin 8h-10h", "B) Midi 12h-14h", "C) Après-midi 16h-18h", "D) Après Iftar 19h-22h"],
                 "correct": "D", "explanation": "L'engagement explose après l'Iftar en Afrique du Nord — meilleures publications de l'année.", "module": 3},
                {"id": 15, "question": "Votre agence perd son authenticité après adoption AI. Première action ?",
                 "options": ["A) Arrêter l'AI", "B) Créer un Brand Voice Guide AI avec prompts brandés", "C) Changer d'outils AI", "D) Embaucher un community manager"],
                 "correct": "B", "explanation": "Le Brand Voice Guide AI briefer ChatGPT pour respecter l'ADN de chaque marque.", "module": 3},
                {"id": 16, "question": "Pourquoi co-construire la politique AI marketing avec l'équipe ?",
                 "options": ["A) La direction n'a pas les compétences", "B) Une politique acceptée sera appliquée — une politique imposée sera contournée", "C) C'est obligatoire légalement", "D) Cela réduit les coûts"],
                 "correct": "B", "explanation": "En Afrique du Nord, le changement accepté est 10x plus durable que le changement imposé.", "module": 3},
                {"id": 17, "question": "Quelle interdiction est essentielle dans une politique marketing AI en Afrique du Nord ?",
                 "options": ["A) Utiliser ChatGPT pour les newsletters", "B) Créer des deepfakes célébrités sans consentement", "C) Programmer des posts avec Buffer AI", "D) Générer des visuels avec Canva AI"],
                 "correct": "B", "explanation": "Les deepfakes célébrités sont illégaux et contraires à l'éthique.", "module": 3},
                {"id": 18, "question": "Un article accuse votre agence de publicité discriminatoire AI. Première réaction dans les 2 heures ?",
                 "options": ["A) Attendre que ça passe", "B) Ignorer et continuer", "C) Désactiver la campagne + réunion équipe + préparer communication officielle transparente", "D) Supprimer tous les commentaires"],
                 "correct": "C", "explanation": "Transparence rapide < 2h limite les dégâts. Silence = aveu.", "module": 3},
                {"id": 19, "question": "Quel outil est recommandé pour créer un tableau de bord marketing AI gratuit connectant GA + Meta ?",
                 "options": ["A) Excel", "B) Looker Studio (Data Studio)", "C) HubSpot Analytics", "D) Tableau"],
                 "correct": "B", "explanation": "Looker Studio est gratuit et se connecte nativement à Google Analytics et Google Ads.", "module": 3},
                {"id": 20, "question": "Quel est le score minimum requis pour la certification Euklydia AI Marketing Strategist ?",
                 "options": ["A) 70% test + 70/100 projet", "B) 80% test + 75/100 projet", "C) 90% test + 80/100 projet", "D) 75% test + 70/100 projet"],
                 "correct": "B", "explanation": "Certification Euklydia : 80% minimum au test + 75/100 minimum au projet.", "module": 3},
            ],
            "passing_score": 80,
            "duration_min": 30,
        },
        hints_fr=[
            {"level": 1, "text": "Relisez les key takeaways de chaque module avant de commencer le test."},
            {"level": 2, "text": "Modules 1 et 2 : fondamentaux et outils. Module 3 : stratégie, ROI et gouvernance."},
        ],
    ))
    db.flush()

    # ── Leçon Cert.2 — Projet de certification ───────────────────────────────
    l3_cert_2 = Lesson(
        unit_id=u3_cert.id, order=2,
        title_fr="Projet de certification — Dossier complet stratégie marketing AI",
        title_en="Certification project — Complete AI marketing strategy portfolio",
        format="exercise", difficulty_level=5, estimated_duration_min=480,
        description_fr="Projet intégrateur final. Évalué par le jury Euklydia sous 5 jours ouvrés.",
        description_en="Final integrative project. Evaluated by Euklydia jury within 5 business days.",
        prerequisite_lesson_id=l3_cert_1.id,
    )
    db.add(l3_cert_2); db.flush()

    db.add(Activity(
        lesson_id=l3_cert_2.id, order=1, type="exercise",
        title_fr="Projet de certification — AI Marketing Strategist Euklydia",
        title_en="Certification project — Euklydia AI Marketing Strategist",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "instructions": "6 livrables obligatoires. 7 jours après validation du test pour soumettre.",
            "livrables": [
                {"id": 1, "titre": "Diagnostic de maturité AI marketing",
                 "description": "Évaluation 5 piliers avec score actuel, cible et justification.",
                 "format": "2 pages maximum"},
                {"id": 2, "titre": "Stratégie AI marketing 12 mois",
                 "description": "Vision, OKRs mesurables, feuille de route 4 phases, budget par outil.",
                 "format": "3 à 5 pages"},
                {"id": 3, "titre": "Plan de contenu AI Afrique du Nord",
                 "description": "Calendrier éditorial 1 mois, mix contenu, adaptation culturelle, prompts utilisés.",
                 "format": "2 pages + exemples"},
                {"id": 4, "titre": "Politique AI marketing",
                 "description": "Document officiel 8 sections : usages autorisés/interdits, droits d'auteur, gouvernance données.",
                 "format": "3 à 5 pages"},
                {"id": 5, "titre": "Dashboard ROI marketing AI",
                 "description": "Captures Looker Studio + calcul ROI projeté 12 mois avec méthodologie.",
                 "format": "1 à 2 pages + captures"},
                {"id": 6, "titre": "Présentation direction",
                 "description": "Pitch 12 slides pour convaincre un comité de direction. Réponses aux 4 objections types.",
                 "format": "PDF ou PowerPoint"},
            ],
            "criteres_evaluation": {
                "diagnostic_maturite": "15%",
                "strategie_12_mois": "25%",
                "plan_contenu_afrique_du_nord": "15%",
                "politique_ai_marketing": "15%",
                "dashboard_roi": "15%",
                "presentation_direction": "15%",
            },
            "score_minimum": 75,
            "delai_soumission": "7 jours après validation du test",
            "feedback": "Jury Euklydia — 2 membres — dans les 5 jours ouvrés",
            "certification_obtenue": {
                "badge": "Badge LinkedIn officiel AI Marketing Strategist",
                "certificat": "Certificat PDF signé Euklydia",
                "annuaire": "Inscription Annuaire Euklydia Afrique du Nord",
                "validite": "2 ans",
            },
        },
        rubric_fr={"criteres": [
            {"nom": "Diagnostic de maturité AI", "poids": 0.15,
             "description": "Évaluation honnête, cohérente et justifiée des 5 piliers."},
            {"nom": "Stratégie AI marketing 12 mois", "poids": 0.25,
             "description": "Vision claire, OKRs mesurables, feuille de route réaliste et budgétée."},
            {"nom": "Plan de contenu Afrique du Nord", "poids": 0.15,
             "description": "Calendrier réaliste, adaptation culturelle authentic, prompts pertinents."},
            {"nom": "Politique AI marketing", "poids": 0.15,
             "description": "Document opérationnel, conforme aux lois Afrique du Nord, usages bien définis."},
            {"nom": "Dashboard ROI", "poids": 0.15,
             "description": "Calcul ROI méthodologiquement correct, KPIs pertinents, visuels Looker Studio."},
            {"nom": "Présentation direction", "poids": 0.15,
             "description": "Pitch convaincant, arguments chiffrés, réponses aux objections solides."},
        ]},
    ))
    db.flush()

    db.commit()
    print("✅ AI Marketing Strategist — units, lessons, activities insérées")
    print("   Module 1 — Fondations : 5 unités, 14 leçons (contenu complet)")
    print("   Module 2 — Pratique   : 5 unités, 14 leçons (contenu complet)")
    print("   Module 3 — Expert     : 6 unités, 16 leçons (+ certification finale)")
    print("   Total                 : 16 unités, 44 leçons")