"""
Seed Units, Lessons, Activities — AI Project Manager (role_id=82)
Module 1 — Fondations : 5 unités, 14 leçons, contenu complet
Module 2 — Pratique   : 5 unités, 14 leçons, contenu complet
Module 3 — Expert     : 5 unités, 14 leçons, contenu complet
Total                 : 15 unités, 42 leçons

Ordre d'exécution :
  1. seed_ai_project_manager.py
  2. seed_ai_project_manager_modules.py
  3. seed_ai_project_manager_units_lessons.py  ← ce fichier
"""

from app.models.module import Module
from app.models.unit import Unit
from app.models.lesson import Lesson
from app.models.activity import Activity


def seed_ai_project_manager_units_lessons(db):

    # ── Récupérer les 3 modules ───────────────────────────────────────────────
    m1 = db.query(Module).filter_by(role="AI Project Manager", journey_stage="foundation").first()
    m2 = db.query(Module).filter_by(role="AI Project Manager", journey_stage="practice").first()
    m3 = db.query(Module).filter_by(role="AI Project Manager", journey_stage="expert").first()

    if not all([m1, m2, m3]):
        print("❌ Modules AI Project Manager introuvables — lancer seed_ai_project_manager_modules.py d'abord")
        return

    # ── Supprimer les données existantes ─────────────────────────────────────
    for module in [m1, m2, m3]:
        for u in db.query(Unit).filter_by(module_id=module.id).all():
            for lesson in db.query(Lesson).filter_by(unit_id=u.id).all():
                for activity in db.query(Activity).filter_by(lesson_id=lesson.id).all():
                    db.delete(activity)
                db.delete(lesson)
            db.delete(u)
    db.flush()

    # ════════════════════════════════════════════════════════════════════════
    # MODULE 1 — FONDATIONS
    # ════════════════════════════════════════════════════════════════════════

    # ── Unité 1 — L'AI dans la gestion de projet ─────────────────────────────
    u1_1 = Unit(module_id=m1.id, order=1,
        title_fr="L'AI dans la gestion de projet",
        title_en="AI in Project Management",
        description_fr="Comprendre l'AI pour un PM, ses outils essentiels et ses spécificités pour le contexte Afrique du Nord.",
        estimated_duration_min=26)
    db.add(u1_1); db.flush()

    l1_1_1 = Lesson(unit_id=u1_1.id, order=1,
        title_fr="C'est quoi l'AI pour un PM ?",
        title_en="C'est quoi l'AI pour un PM ?", format="video",
        difficulty_level=1, estimated_duration_min=10,
        description_fr="Définition AI en gestion de projet, 5 révolutions pour le PM, évolution historique, chiffres clés MENA.")
    db.add(l1_1_1); db.flush()
    db.add(Activity(lesson_id=l1_1_1.id, order=1, type="video",
        title_fr="Vidéo — C'est quoi l'AI pour un PM ?",
        is_assessed=False, is_required=True, content_fr={"duration_min": 10, "url_fr": None}))
    db.add(Activity(lesson_id=l1_1_1.id, order=2, type="quiz",
        title_fr="Quiz — L'AI en gestion de projet",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={"questions": [
            {"id": 1,
             "question": "Quel est le principal avantage de l'AI pour un chef de projet tunisien gérant plusieurs projets simultanément ?",
             "options": [
                 "A) L'AI remplace complètement le chef de projet",
                 "B) L'AI automatise les tâches répétitives et libère le PM pour les décisions stratégiques",
                 "C) L'AI garantit que tous les projets se terminent à temps",
                 "D) L'AI élimine le besoin de communiquer avec l'équipe"
             ],
             "correct": "B",
             "explanation": "L'AI automatise les tâches répétitives (rapports, rappels, suivi) et permet au PM de se concentrer sur les décisions stratégiques et le management humain."},
            {"id": 2,
             "question": "Parmi ces affirmations sur l'AI PM, laquelle est correcte ?",
             "options": [
                 "A) L'AI prend toutes les décisions de projet automatiquement",
                 "B) L'AI remplace la communication humaine dans l'équipe",
                 "C) L'AI est un outil d'aide à la décision — le PM garde toujours le contrôle final",
                 "D) L'AI fonctionne parfaitement sans données de qualité"
             ],
             "correct": "C",
             "explanation": "L'AI est un outil d'aide à la décision. Le PM garde toujours la responsabilité des décisions finales, surtout pour les aspects humains et stratégiques."},
        ], "passing_score": 70},
        hints_fr=[
            {"level": 1, "text": "L'AI PM ne remplace pas le chef de projet — elle lui permet de gérer plus de projets avec plus de précision."},
        ]))
    db.flush()

    l1_1_2 = Lesson(unit_id=u1_1.id, order=2,
        title_fr="Les outils AI essentiels du PM",
        title_en="Les outils AI essentiels du PM", format="video",
        difficulty_level=1, estimated_duration_min=8,
        description_fr="5 catégories d'outils AI PM, tableau comparatif, stack gratuit pour démarrer, cas PME tunisienne.",
        prerequisite_lesson_id=l1_1_1.id)
    db.add(l1_1_2); db.flush()
    db.add(Activity(lesson_id=l1_1_2.id, order=1, type="video",
        title_fr="Vidéo — Les outils AI essentiels du PM",
        is_assessed=False, is_required=True, content_fr={"duration_min": 8}))
    db.add(Activity(lesson_id=l1_1_2.id, order=2, type="quiz",
        title_fr="Quiz — Outils AI PM",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={"questions": [
            {"id": 1,
             "question": "Quel outil AI PM gratuit recommandez-vous pour démarrer la gestion de projet ?",
             "options": ["A) Microsoft Project", "B) ClickUp AI", "C) SAP", "D) Adobe XD"],
             "correct": "B",
             "explanation": "ClickUp AI propose une version gratuite puissante avec génération de tâches AI, tableaux de bord automatiques et rapports intelligents."},
            {"id": 2,
             "question": "Pour centraliser 3 projets MENA simultanément avec tableaux de bord automatiques, quel outil choisissez-vous ?",
             "options": ["A) Excel", "B) WhatsApp", "C) Notion AI", "D) Google Maps"],
             "correct": "C",
             "explanation": "Notion AI permet de centraliser plusieurs projets avec des tableaux de bord automatiques et une vision globale + détaillée en temps réel."},
        ], "passing_score": 70}))
    db.flush()

    l1_1_3 = Lesson(unit_id=u1_1.id, order=3,
        title_fr="L'AI PM dans le contexte MENA",
        title_en="L'AI PM dans le contexte MENA", format="video",
        difficulty_level=1, estimated_duration_min=8,
        description_fr="Spécificités projets MENA, équipes bilingues AR/FR, culture de projet locale, délais et contraintes MENA.",
        prerequisite_lesson_id=l1_1_2.id)
    db.add(l1_1_3); db.flush()
    db.add(Activity(lesson_id=l1_1_3.id, order=1, type="video",
        title_fr="Vidéo — L'AI PM dans le contexte MENA",
        is_assessed=False, is_required=True, content_fr={"duration_min": 8}))
    db.add(Activity(lesson_id=l1_1_3.id, order=2, type="forum_discussion",
        title_fr="Forum — L'AI PM dans votre contexte professionnel",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "question": "Comment l'AI PM peut-il améliorer la gestion de projet dans votre secteur en Tunisie ? Partagez un défi de gestion de projet que vous aimeriez résoudre avec l'AI.",
            "consigne": "Minimum 5 lignes. Décrivez votre secteur, un défi PM concret et un outil AI à tester. Commentez au moins 2 contributions de vos pairs.",
        }))
    db.flush()

    # ── Unité 2 — Planifier avec l'AI ─────────────────────────────────────────
    u1_2 = Unit(module_id=m1.id, order=2,
        title_fr="Planifier avec l'AI",
        title_en="Planning with AI",
        description_fr="Générer des plannings automatiques, créer des tâches et sous-tâches avec ClickUp AI et Notion AI.",
        estimated_duration_min=42)
    db.add(u1_2); db.flush()

    l1_2_1 = Lesson(unit_id=u1_2.id, order=1,
        title_fr="Générer son premier planning avec l'AI",
        title_en="Générer son premier planning avec l'AI", format="tutorial",
        difficulty_level=2, estimated_duration_min=12,
        description_fr="ClickUp AI et Notion AI pour génération planning, prompt de description projet, ajustements manuels.")
    db.add(l1_2_1); db.flush()
    db.add(Activity(lesson_id=l1_2_1.id, order=1, type="tutorial",
        title_fr="Tutoriel guidé — Générer un planning avec ClickUp AI",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(lesson_id=l1_2_1.id, order=2, type="exercise",
        title_fr="Exercice — Générez votre premier planning de projet AI",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Générez un planning complet avec ClickUp AI :\n1. Décrivez votre projet en 3 lignes dans ClickUp AI\n2. Analysez le planning généré automatiquement\n3. Identifiez 3 tâches à ajuster selon le contexte MENA\n4. Ajoutez les responsables et délais adaptés à votre équipe tunisienne",
            "livrable": "Screenshot du planning généré + liste des 3 ajustements avec justification.",
            "criteres": {"qualite_description_projet": "25%", "pertinence_ajustements_mena": "45%", "completude_planning": "30%"},
            "score_minimum": 70,
        },
        hints_fr=[
            {"level": 1, "text": "Prompt efficace pour ClickUp AI : 'Crée un planning pour [type de projet] avec une équipe de [X] personnes, durée [X] semaines, contexte [secteur en Tunisie].'"},
            {"level": 2, "text": "Ajustements MENA essentiels : tenez compte des jours fériés tunisiens, du Ramadan et des disponibilités réelles de l'équipe."},
        ]))
    db.flush()

    l1_2_2 = Lesson(unit_id=u1_2.id, order=2,
        title_fr="Créer des tâches et sous-tâches automatiquement",
        title_en="Créer des tâches et sous-tâches automatiquement", format="video",
        difficulty_level=2, estimated_duration_min=10,
        description_fr="Décomposition automatique WBS avec AI, niveaux de tâches, dépendances, estimation durées.",
        prerequisite_lesson_id=l1_2_1.id)
    db.add(l1_2_2); db.flush()
    db.add(Activity(lesson_id=l1_2_2.id, order=1, type="video",
        title_fr="Vidéo — Créer des tâches et sous-tâches avec l'AI",
        is_assessed=False, is_required=True, content_fr={"duration_min": 10}))
    db.add(Activity(lesson_id=l1_2_2.id, order=2, type="exercise",
        title_fr="Exercice — Décomposer un projet en tâches avec l'AI",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Utilisez ClickUp AI pour décomposer un projet en tâches détaillées :\n1. Choisissez un projet réel ou fictif réaliste (lancement produit, refonte site web, formation...)\n2. Générez automatiquement le WBS (Work Breakdown Structure) avec l'AI\n3. Créez minimum 3 niveaux de décomposition\n4. Ajoutez les dépendances entre tâches\n5. Estimez les durées avec l'AI et ajustez selon votre équipe",
            "livrable": "WBS complet (screenshot) avec 3 niveaux + dépendances + estimations.",
            "criteres": {"completude_wbs": "30%", "pertinence_dependances": "35%", "realisme_estimations": "35%"},
            "score_minimum": 70,
        }))
    db.flush()

    l1_2_3 = Lesson(unit_id=u1_2.id, order=3,
        title_fr="Mon premier planning de projet MENA",
        title_en="Mon premier planning de projet MENA", format="exercise",
        difficulty_level=3, estimated_duration_min=60,
        description_fr="Projet noté — planning complet d'un projet digital MENA avec ClickUp AI ou Notion AI.",
        prerequisite_lesson_id=l1_2_2.id)
    db.add(l1_2_3); db.flush()
    db.add(Activity(lesson_id=l1_2_3.id, order=1, type="exercise",
        title_fr="Projet noté — Mon premier planning de projet MENA complet",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Créez le planning complet d'un projet digital MENA avec l'AI :\n\nContexte : Lancement d'une plateforme e-learning pour une entreprise tunisienne. Équipe de 6 personnes, budget 50 000 TND, délai 90 jours.\n\n1. Générez le planning complet avec ClickUp AI\n2. Décomposez en phases (Discovery, Design, Development, Testing, Launch)\n3. Assignez les responsables par rôle\n4. Intégrez les contraintes MENA (fériés, Ramadan si applicable)\n5. Créez le tableau de bord de suivi\n6. Rédigez la note de lancement projet (10 lignes)",
            "livrable": "Planning complet + tableau de bord + note de lancement.",
            "criteres": {
                "completude_planning": "25%",
                "realisme_mena": "30%",
                "qualite_tableau_bord": "25%",
                "note_lancement": "20%",
            },
            "score_minimum": 70,
        },
        rubric_fr={"criteres": [
            {"nom": "Complétude du planning", "poids": 0.25, "description": "Toutes les phases couvertes, tâches décomposées, dépendances définies."},
            {"nom": "Réalisme MENA", "poids": 0.30, "description": "Contraintes locales intégrées, délais réalistes pour le marché tunisien."},
            {"nom": "Qualité du tableau de bord", "poids": 0.25, "description": "KPIs pertinents, visualisation claire, suivi automatisé."},
            {"nom": "Note de lancement", "poids": 0.20, "description": "Clara, motivante, couvre les enjeux clés du projet."},
        ]}))
    db.flush()

    # ── Unité 3 — Mon premier outil de gestion AI ─────────────────────────────
    u1_3 = Unit(module_id=m1.id, order=3,
        title_fr="Mon premier outil de gestion AI",
        title_en="My First AI Management Tool",
        description_fr="Maîtriser ClickUp AI de A à Z — interface, tableau de bord, gestion d'équipe.",
        estimated_duration_min=38)
    db.add(u1_3); db.flush()

    l1_3_1 = Lesson(unit_id=u1_3.id, order=1,
        title_fr="Introduction à ClickUp AI",
        title_en="Introduction à ClickUp AI", format="tutorial",
        difficulty_level=1, estimated_duration_min=12,
        description_fr="Interface ClickUp AI, espaces de travail, vues (liste, kanban, Gantt), fonctionnalités AI intégrées.")
    db.add(l1_3_1); db.flush()
    db.add(Activity(lesson_id=l1_3_1.id, order=1, type="tutorial",
        title_fr="Tutoriel guidé — ClickUp AI pas à pas",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(lesson_id=l1_3_1.id, order=2, type="exercise",
        title_fr="Exercice — Configurer mon espace de travail ClickUp AI",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "consigne": "1. Créez un compte ClickUp AI gratuit\n2. Configurez votre espace de travail pour un projet MENA\n3. Créez 3 vues différentes : liste, kanban, calendrier\n4. Activez les fonctionnalités AI dans les paramètres\n5. Soumettez un screenshot de votre espace configuré",
            "livrable": "Screenshot espace ClickUp AI configuré avec 3 vues.",
        }))
    db.flush()

    l1_3_2 = Lesson(unit_id=u1_3.id, order=2,
        title_fr="Créer son premier tableau de bord AI",
        title_en="Créer son premier tableau de bord AI", format="tutorial",
        difficulty_level=2, estimated_duration_min=10,
        description_fr="Dashboard ClickUp AI, widgets automatiques, métriques projet, alertes intelligentes.",
        prerequisite_lesson_id=l1_3_1.id)
    db.add(l1_3_2); db.flush()
    db.add(Activity(lesson_id=l1_3_2.id, order=1, type="tutorial",
        title_fr="Tutoriel — Créer son tableau de bord AI",
        is_assessed=False, is_required=True, content_fr={"duration_min": 10}))
    db.add(Activity(lesson_id=l1_3_2.id, order=2, type="exercise",
        title_fr="Exercice — Mon premier tableau de bord projet AI",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Créez un tableau de bord complet pour votre projet :\n1. Ajoutez minimum 5 widgets (avancement, charge de travail, délais, risques, budget)\n2. Configurez les alertes automatiques pour les tâches en retard\n3. Activez le rapport hebdomadaire automatique\n4. Rédigez une note de 5 lignes expliquant vos choix de KPIs",
            "livrable": "Screenshot tableau de bord (5 widgets min) + note KPIs.",
            "criteres": {"completude_widgets": "40%", "pertinence_alertes": "35%", "note_kpis": "25%"},
            "score_minimum": 70,
        }))
    db.flush()

    l1_3_3 = Lesson(unit_id=u1_3.id, order=3,
        title_fr="Gérer son équipe avec l'AI",
        title_en="Gérer son équipe avec l'AI", format="video",
        difficulty_level=2, estimated_duration_min=10,
        description_fr="Assignation intelligente, suivi de charge, disponibilités équipe, notifications automatiques membres.",
        prerequisite_lesson_id=l1_3_2.id)
    db.add(l1_3_3); db.flush()
    db.add(Activity(lesson_id=l1_3_3.id, order=1, type="video",
        title_fr="Vidéo — Gérer son équipe avec l'AI",
        is_assessed=False, is_required=True, content_fr={"duration_min": 10}))
    db.add(Activity(lesson_id=l1_3_3.id, order=2, type="exercise",
        title_fr="Exercice — Configurer la gestion d'équipe AI",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "consigne": "Configurez la gestion d'équipe dans ClickUp AI :\n1. Ajoutez 3 membres fictifs avec leurs rôles et disponibilités\n2. Configurez les règles d'assignation automatique\n3. Activez les notifications de surcharge de travail\n4. Testez l'assignation automatique d'une tâche",
            "livrable": "Screenshot configuration équipe + règles d'assignation.",
        }))
    db.flush()

    # ── Unité 4 — Communiquer avec son équipe avec l'AI ──────────────────────
    u1_4 = Unit(module_id=m1.id, order=4,
        title_fr="Communiquer avec son équipe avec l'AI",
        title_en="Communicating with Your Team Using AI",
        description_fr="Générer des rapports, comptes-rendus et communications projet avec ChatGPT en arabe et français.",
        estimated_duration_min=36)
    db.add(u1_4); db.flush()

    l1_4_1 = Lesson(unit_id=u1_4.id, order=1,
        title_fr="Générer des rapports automatiquement",
        title_en="Générer des rapports automatiquement", format="video",
        difficulty_level=2, estimated_duration_min=10,
        description_fr="Rapports d'avancement automatiques ClickUp AI, synthèse hebdomadaire, rapport exécutif client.")
    db.add(l1_4_1); db.flush()
    db.add(Activity(lesson_id=l1_4_1.id, order=1, type="video",
        title_fr="Vidéo — Générer des rapports automatiquement",
        is_assessed=False, is_required=True, content_fr={"duration_min": 10}))
    db.add(Activity(lesson_id=l1_4_1.id, order=2, type="exercise",
        title_fr="Exercice — Créer mon rapport d'avancement hebdomadaire",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Générez un rapport d'avancement hebdomadaire complet :\n1. Utilisez ClickUp AI pour générer le rapport automatique\n2. Personnalisez avec ChatGPT pour le client MENA\n3. Rédigez la version française ET la version arabe\n4. Ajoutez les points d'attention et les décisions demandées",
            "livrable": "Rapport hebdomadaire bilingue (FR + AR) avec points d'attention.",
            "criteres": {"completude_rapport": "30%", "qualite_bilingue": "40%", "pertinence_points_attention": "30%"},
            "score_minimum": 70,
        },
        hints_fr=[
            {"level": 1, "text": "Structure rapport hebdomadaire MENA : Avancement global % + Réalisations semaine + Blocages + Décisions attendues + Prochaines étapes."},
            {"level": 2, "text": "Pour la version arabe : utilisez ChatGPT avec le prompt 'Traduis ce rapport de projet en arabe professionnel adapté au contexte MENA, en conservant les chiffres et les noms propres.'"},
        ]))
    db.flush()

    l1_4_2 = Lesson(unit_id=u1_4.id, order=2,
        title_fr="Rédiger des comptes-rendus avec ChatGPT en arabe et français",
        title_en="Rédiger des comptes-rendus avec ChatGPT en arabe et français", format="tutorial",
        difficulty_level=2, estimated_duration_min=10,
        description_fr="Comptes-rendus de réunion avec Fireflies AI + ChatGPT, synthèse bilingue, action items automatiques.",
        prerequisite_lesson_id=l1_4_1.id)
    db.add(l1_4_2); db.flush()
    db.add(Activity(lesson_id=l1_4_2.id, order=1, type="tutorial",
        title_fr="Tutoriel — Comptes-rendus bilingues avec ChatGPT",
        is_assessed=False, is_required=True, content_fr={"duration_min": 10}))
    db.add(Activity(lesson_id=l1_4_2.id, order=2, type="exercise",
        title_fr="Exercice — Créer un compte-rendu de réunion bilingue",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Créez un compte-rendu de réunion de lancement de projet :\n1. Rédigez les notes brutes d'une réunion fictive (15 lignes)\n2. Utilisez ChatGPT pour transformer en compte-rendu structuré en français\n3. Générez la version arabe avec ChatGPT\n4. Extrayez automatiquement les action items avec responsables et délais\n5. Envoyez via votre outil de gestion (ClickUp ou Notion)",
            "livrable": "Notes brutes + compte-rendu FR + compte-rendu AR + liste action items.",
            "criteres": {"qualite_structure": "30%", "qualite_traduction_ar": "35%", "precision_action_items": "35%"},
            "score_minimum": 70,
        }))
    db.flush()

    l1_4_3 = Lesson(unit_id=u1_4.id, order=3,
        title_fr="Communiquer avec les parties prenantes",
        title_en="Communiquer avec les parties prenantes", format="video",
        difficulty_level=2, estimated_duration_min=8,
        description_fr="Communication client MENA avec AI, emails de statut, escalades, communications de crise projet.",
        prerequisite_lesson_id=l1_4_2.id)
    db.add(l1_4_3); db.flush()
    db.add(Activity(lesson_id=l1_4_3.id, order=1, type="video",
        title_fr="Vidéo — Communiquer avec les parties prenantes avec l'AI",
        is_assessed=False, is_required=True, content_fr={"duration_min": 8}))
    db.add(Activity(lesson_id=l1_4_3.id, order=2, type="exercise",
        title_fr="Exercice — Rédiger les communications projet clés avec ChatGPT",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "consigne": "Rédigez avec ChatGPT 3 communications projet essentielles :\n1. Email de lancement projet au client (ton professionnel, MENA)\n2. Email d'alerte retard (diplomatie + solutions proposées)\n3. Email de clôture projet avec bilan (FR et AR)",
            "livrable": "3 emails rédigés + version arabe de l'email de clôture.",
        }))
    db.flush()

    # ── Unité 5 — Éthique AI basique en gestion de projet ────────────────────
    u1_5 = Unit(module_id=m1.id, order=5,
        title_fr="Éthique AI basique en gestion de projet",
        title_en="Basic AI Ethics in Project Management",
        description_fr="Décisions que l'AI peut et ne doit pas prendre, transparence avec son équipe sur l'usage AI.",
        estimated_duration_min=28)
    db.add(u1_5); db.flush()

    l1_5_1 = Lesson(unit_id=u1_5.id, order=1,
        title_fr="Les décisions que l'AI peut et ne doit pas prendre",
        title_en="Les décisions que l'AI peut et ne doit pas prendre", format="video",
        difficulty_level=1, estimated_duration_min=10,
        description_fr="Frontières humain/AI en PM, décisions automatisables vs décisions humaines, tableau de décision éthique.")
    db.add(l1_5_1); db.flush()
    db.add(Activity(lesson_id=l1_5_1.id, order=1, type="video",
        title_fr="Vidéo — Décisions AI vs décisions humaines en gestion de projet",
        is_assessed=False, is_required=True, content_fr={"duration_min": 10}))
    db.add(Activity(lesson_id=l1_5_1.id, order=2, type="quiz",
        title_fr="Quiz — Éthique AI en gestion de projet",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={"questions": [
            {"id": 1,
             "question": "L'AI de votre outil suggère de licencier un membre de l'équipe car ses métriques de productivité sont faibles. Que faites-vous ?",
             "options": [
                 "A) Vous suivez la recommandation AI immédiatement",
                 "B) Vous ignorez toutes les recommandations AI à l'avenir",
                 "C) Vous analysez le contexte humain, discutez avec le membre, cherchez les causes avant toute décision",
                 "D) Vous demandez à l'AI de générer un plan de licenciement"
             ],
             "correct": "C",
             "explanation": "Les décisions qui affectent directement les personnes (licenciement, évaluation, sanction) ne peuvent jamais être déléguées à l'AI. Le PM doit toujours analyser le contexte humain complet."},
            {"id": 2,
             "question": "Quelle décision peut être entièrement déléguée à l'AI dans un projet ?",
             "options": [
                 "A) Évaluer les performances de l'équipe",
                 "B) Définir la stratégie du projet",
                 "C) Programmer les rappels et notifications automatiques",
                 "D) Résoudre les conflits entre membres"
             ],
             "correct": "C",
             "explanation": "La programmation de rappels et notifications est une tâche purement organisationnelle et répétitive — idéale pour une délégation totale à l'AI."},
        ], "passing_score": 70}))
    db.flush()

    l1_5_2 = Lesson(unit_id=u1_5.id, order=2,
        title_fr="Transparence avec son équipe sur l'usage de l'AI",
        title_en="Transparence avec son équipe sur l'usage de l'AI", format="case_study",
        difficulty_level=2, estimated_duration_min=30,
        description_fr="2 cas pratiques : PM qui cache l'AI vs PM transparent. Communication de l'AI à l'équipe MENA.",
        prerequisite_lesson_id=l1_5_1.id)
    db.add(l1_5_2); db.flush()
    db.add(Activity(lesson_id=l1_5_2.id, order=1, type="case_study",
        title_fr="Cas pratiques — Transparence AI avec son équipe",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "cas": [
                {
                    "titre": "Cas Karim — Le PM qui cache l'AI",
                    "contexte": "Karim utilise ClickUp AI pour surveiller en temps réel la productivité de chaque membre de son équipe sans les informer. Il utilise ces données pour des évaluations de performance sans révéler la source.",
                    "questions": [
                        "Quelles erreurs éthiques Karim a-t-il commises ?",
                        "Quels sont les risques pour la confiance et la cohésion de l'équipe ?",
                        "Comment aurait-il dû introduire l'AI dans son équipe ?",
                    ],
                },
                {
                    "titre": "Cas Fatima — Le PM transparent",
                    "contexte": "Fatima présente à son équipe tunisienne tous les outils AI qu'elle va utiliser, explique leur rôle, rassure sur la non-utilisation des données personnelles pour des sanctions et implique l'équipe dans le choix des outils.",
                    "questions": [
                        "Comment la transparence de Fatima renforce-t-elle l'adoption AI par l'équipe ?",
                        "Rédigez le discours de Fatima pour présenter l'AI à son équipe.",
                    ],
                },
            ],
            "score_minimum": 70,
        }))
    db.flush()

    # ════════════════════════════════════════════════════════════════════════
    # MODULE 2 — PRATIQUE
    # ════════════════════════════════════════════════════════════════════════

    # ── Unité 1 — Automatiser la gestion de projet ────────────────────────────
    u2_1 = Unit(module_id=m2.id, order=1,
        title_fr="Automatiser la gestion de projet",
        title_en="Automating Project Management",
        estimated_duration_min=38)
    db.add(u2_1); db.flush()

    l2_1_1 = Lesson(unit_id=u2_1.id, order=1,
        title_fr="Créer des workflows automatiques avec ClickUp AI",
        title_en="Créer des workflows automatiques avec ClickUp AI", format="video",
        difficulty_level=3, estimated_duration_min=12,
        description_fr="Automations ClickUp AI, triggers et conditions, workflows conditionnels, templates d'automation MENA.")
    db.add(l2_1_1); db.flush()
    db.add(Activity(lesson_id=l2_1_1.id, order=1, type="video",
        title_fr="Vidéo — Workflows automatiques avec ClickUp AI",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(lesson_id=l2_1_1.id, order=2, type="exercise",
        title_fr="Exercice — Créer 5 workflows automatiques pour mon projet",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Créez 5 workflows automatiques dans ClickUp AI :\n1. Quand une tâche est en retard → notifier automatiquement le PM et l'assigné\n2. Quand une tâche est terminée → créer automatiquement la tâche suivante dépendante\n3. Quand la charge dépasse 100% → alerter le PM pour redistribution\n4. Chaque lundi → générer et envoyer le rapport hebdomadaire\n5. 3 jours avant deadline → rappel automatique à l'assigné",
            "livrable": "Screenshots des 5 workflows configurés + description de chaque trigger.",
            "criteres": {"completude_5_workflows": "40%", "pertinence_triggers": "35%", "documentation": "25%"},
            "score_minimum": 70,
        },
        hints_fr=[
            {"level": 1, "text": "Dans ClickUp AI : Paramètres → Automations → Créer une automation → Choisir le trigger (déclencheur) → Définir l'action."},
            {"level": 2, "text": "Workflow MENA essentiel : ajouter une automation 'Projet inactif depuis 3 jours → notifier PM' — les délais MENA nécessitent un suivi actif."},
        ]))
    db.flush()

    l2_1_2 = Lesson(unit_id=u2_1.id, order=2,
        title_fr="Automatiser les rappels et notifications",
        title_en="Automatiser les rappels et notifications", format="tutorial",
        difficulty_level=3, estimated_duration_min=10,
        description_fr="Système de rappels intelligents, escalade automatique, notifications personnalisées par rôle.",
        prerequisite_lesson_id=l2_1_1.id)
    db.add(l2_1_2); db.flush()
    db.add(Activity(lesson_id=l2_1_2.id, order=1, type="tutorial",
        title_fr="Tutoriel — Système de rappels et notifications automatiques",
        is_assessed=False, is_required=True, content_fr={"duration_min": 10}))
    db.add(Activity(lesson_id=l2_1_2.id, order=2, type="exercise",
        title_fr="Exercice — Configurer mon système de notification intelligent",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Configurez un système de notification complet :\n1. Rappels par délai (J-7, J-3, J-1 avant deadline)\n2. Notifications d'escalade (retard → PM, retard grave → direction)\n3. Résumé quotidien automatique pour chaque membre\n4. Rapport hebdomadaire au client\nTestez et documentez chaque notification.",
            "livrable": "Configuration complète + preuves de tests (screenshots).",
            "criteres": {"completude_systeme": "35%", "logique_escalade": "40%", "documentation_tests": "25%"},
            "score_minimum": 70,
        }))
    db.flush()

    l2_1_3 = Lesson(unit_id=u2_1.id, order=3,
        title_fr="Mon projet entièrement automatisé",
        title_en="Mon projet entièrement automatisé", format="exercise",
        difficulty_level=4, estimated_duration_min=90,
        description_fr="Projet intégrateur — projet MENA 100% automatisé avec workflows, notifications et rapports AI.",
        prerequisite_lesson_id=l2_1_2.id)
    db.add(l2_1_3); db.flush()
    db.add(Activity(lesson_id=l2_1_3.id, order=1, type="exercise",
        title_fr="Projet noté — Mon projet MENA entièrement automatisé",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Créez un projet entièrement automatisé dans ClickUp AI :\n\nContexte : Développement d'une application mobile pour une startup tunisienne. 4 phases, 45 jours, équipe de 5 personnes.\n\n1. Planning complet généré par AI (phases + tâches + dépendances)\n2. 8 workflows automatiques minimum\n3. Système de notification complet (membres + client + direction)\n4. Tableau de bord avec 6 KPIs automatiques\n5. Rapport hebdomadaire automatique configuré\n6. Simulation d'un retard et gestion automatique",
            "livrable": "Projet ClickUp complet + documentation des automations + simulation retard.",
            "criteres": {
                "completude_planning": "20%",
                "nb_qualite_workflows": "30%",
                "systeme_notification": "25%",
                "tableau_bord_kpis": "25%",
            },
            "score_minimum": 70,
            "duree_estimee": "90 minutes",
        }))
    db.flush()

    # ── Unité 2 — Analyser et prédire avec l'AI ───────────────────────────────
    u2_2 = Unit(module_id=m2.id, order=2,
        title_fr="Analyser et prédire avec l'AI",
        title_en="Analysing and Predicting with AI",
        estimated_duration_min=34)
    db.add(u2_2); db.flush()

    l2_2_1 = Lesson(unit_id=u2_2.id, order=1,
        title_fr="Lire et interpréter les tableaux de bord AI",
        title_en="Lire et interpréter les tableaux de bord AI", format="video",
        difficulty_level=3, estimated_duration_min=12,
        description_fr="Métriques projet clés, taux d'avancement, vélocité équipe, prédictions AI, signaux d'alerte.")
    db.add(l2_2_1); db.flush()
    db.add(Activity(lesson_id=l2_2_1.id, order=1, type="video",
        title_fr="Vidéo — Lire et interpréter les tableaux de bord AI",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(lesson_id=l2_2_1.id, order=2, type="quiz",
        title_fr="Quiz — Interprétation des données projet AI",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={"questions": [
            {"id": 1,
             "question": "Votre tableau de bord AI montre une vélocité d'équipe en baisse de 30% cette semaine. Quelle est votre première action ?",
             "options": [
                 "A) Ignorer — c'est normal d'avoir des variations",
                 "B) Analyser les causes (absences, blocages techniques, surcharge) et agir avant que le retard se confirme",
                 "C) Augmenter immédiatement les heures de travail",
                 "D) Changer tous les délais du projet"
             ],
             "correct": "B",
             "explanation": "Une baisse de vélocité de 30% est un signal d'alerte fort. Le PM doit analyser les causes profondes (absences, blocages, démotivation) avant d'agir."},
            {"id": 2,
             "question": "L'AI prédit que votre projet a 65% de probabilité de dépasser le budget de 20%. Que faites-vous ?",
             "options": [
                 "A) Ignorer la prédiction — l'AI se trompe souvent",
                 "B) Attendre que le dépassement se confirme",
                 "C) Analyser les postes de dépenses à risque, réviser les estimations et informer proactivement le client",
                 "D) Réduire les fonctionnalités sans consulter le client"
             ],
             "correct": "C",
             "explanation": "Une prédiction de dépassement à 65% est un signal sérieux. Agir proactivement (analyse + communication client) est toujours préférable à réagir après le fait accompli."},
        ], "passing_score": 70}))
    db.flush()

    l2_2_2 = Lesson(unit_id=u2_2.id, order=2,
        title_fr="Prédire les retards et risques avec l'AI",
        title_en="Prédire les retards et risques avec l'AI", format="video",
        difficulty_level=3, estimated_duration_min=10,
        description_fr="Modèles prédictifs ClickUp AI, identification chemin critique, probabilités de risque, plan de contingence.",
        prerequisite_lesson_id=l2_2_1.id)
    db.add(l2_2_2); db.flush()
    db.add(Activity(lesson_id=l2_2_2.id, order=1, type="video",
        title_fr="Vidéo — Prédire retards et risques avec l'AI",
        is_assessed=False, is_required=True, content_fr={"duration_min": 10}))
    db.add(Activity(lesson_id=l2_2_2.id, order=2, type="exercise",
        title_fr="Exercice — Analyse prédictive de mon projet",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Réalisez une analyse prédictive complète de votre projet :\n1. Identifiez le chemin critique avec ClickUp AI\n2. Listez les 5 risques principaux avec probabilité et impact\n3. Pour chaque risque : plan de contingence en 3 actions\n4. Créez un registre des risques dans votre outil AI\n5. Définissez les seuils d'alerte qui déclenchent une action",
            "livrable": "Chemin critique identifié + registre 5 risques + plans de contingence.",
            "criteres": {"identification_chemin_critique": "25%", "qualite_registre_risques": "40%", "pertinence_plans_contingence": "35%"},
            "score_minimum": 70,
        }))
    db.flush()

    l2_2_3 = Lesson(unit_id=u2_2.id, order=3,
        title_fr="Agir avant que le problème survienne",
        title_en="Agir avant que le problème survienne", format="case_study",
        difficulty_level=4, estimated_duration_min=45,
        description_fr="Cas SoftStart Tunisie — startup en retard critique, analyse AI des données, plan de redressement.",
        prerequisite_lesson_id=l2_2_2.id)
    db.add(l2_2_3); db.flush()
    db.add(Activity(lesson_id=l2_2_3.id, order=1, type="case_study",
        title_fr="Cas SoftStart Tunisie — Gestion proactive d'un projet en risque",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "contexte": "SoftStart est une startup tunisienne développant une app de livraison. Le PM reçoit ces alertes IA en semaine 6 sur 12 :",
            "donnees": {
                "avancement": "35% (attendu : 50%)",
                "velocite_equipe": "Baisse 40% vs semaine 1",
                "risque_delai": "72% de probabilité de retard",
                "charge_travail": "2 développeurs à 160%, 1 à 40%",
                "budget_consomme": "58% (attendu : 45%)",
                "risque_budget": "Dépassement prédit : +25%",
            },
            "questions": [
                {"id": 1, "question": "Analysez les données AI. Quels sont les 3 problèmes les plus critiques et leurs causes probables ?", "consigne": "Appuyez chaque analyse sur les données chiffrées."},
                {"id": 2, "question": "Rédigez le plan de redressement en 5 actions prioritaires pour les 2 prochaines semaines.", "consigne": "Chaque action : responsable, délai, impact attendu."},
                {"id": 3, "question": "Rédigez l'email de communication de crise au client.", "consigne": "Transparent, professionnel, solutions proposées, ton MENA adapté."},
                {"id": 4, "question": "Comment redistribuez-vous la charge de travail avec l'AI pour équilibrer l'équipe ?", "consigne": "Plan de redistribution concret avec les 2 développeurs surchargés."},
            ],
        }))
    db.flush()

    # ── Unité 3 — Gérer la charge de travail avec l'AI ───────────────────────
    u2_3 = Unit(module_id=m2.id, order=3,
        title_fr="Gérer la charge de travail avec l'AI",
        title_en="Managing Workload with AI",
        estimated_duration_min=36)
    db.add(u2_3); db.flush()

    l2_3_1 = Lesson(unit_id=u2_3.id, order=1,
        title_fr="Détecter les surcharges automatiquement",
        title_en="Détecter les surcharges automatiquement", format="video",
        difficulty_level=3, estimated_duration_min=10,
        description_fr="Vue capacité ClickUp AI, seuils de surcharge, alertes automatiques, bien-être équipe et productivité.")
    db.add(l2_3_1); db.flush()
    db.add(Activity(lesson_id=l2_3_1.id, order=1, type="video",
        title_fr="Vidéo — Détecter les surcharges avec l'AI",
        is_assessed=False, is_required=True, content_fr={"duration_min": 10}))
    db.add(Activity(lesson_id=l2_3_1.id, order=2, type="exercise",
        title_fr="Exercice — Configurer la détection de surcharge",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Configurez la détection de surcharge dans votre outil AI :\n1. Activez la vue 'Charge de travail' dans ClickUp AI\n2. Définissez la capacité de chaque membre (heures/semaine)\n3. Configurez les alertes à 80%, 100% et 120% de capacité\n4. Simulez une surcharge sur 2 membres et vérifiez les alertes\n5. Documentez comment vous gérez éthiquement ces données",
            "livrable": "Vue capacité configurée + alertes testées + note éthique.",
            "criteres": {"configuration_complete": "35%", "tests_alertes": "35%", "note_ethique": "30%"},
            "score_minimum": 70,
        }))
    db.flush()

    l2_3_2 = Lesson(unit_id=u2_3.id, order=2,
        title_fr="Redistribuer les tâches avec l'AI",
        title_en="Redistribuer les tâches avec l'AI", format="tutorial",
        difficulty_level=3, estimated_duration_min=10,
        description_fr="Redistribution automatique ClickUp AI, respect des compétences, consultation équipe, validation PM.",
        prerequisite_lesson_id=l2_3_1.id)
    db.add(l2_3_2); db.flush()
    db.add(Activity(lesson_id=l2_3_2.id, order=1, type="tutorial",
        title_fr="Tutoriel — Redistribuer les tâches avec l'AI",
        is_assessed=False, is_required=True, content_fr={"duration_min": 10}))
    db.add(Activity(lesson_id=l2_3_2.id, order=2, type="exercise",
        title_fr="Exercice — Simuler une redistribution de charge",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Simulez une situation de surcharge et redistribuez :\n1. Créez un scénario : 3 membres dont 1 absent soudainement\n2. Utilisez l'AI pour proposer une redistribution des tâches\n3. Vérifiez que la redistribution respecte les compétences\n4. Ajustez manuellement les cas problématiques\n5. Communiquez le changement à l'équipe avec un message ChatGPT",
            "livrable": "Plan redistribution avant/après + message communication équipe.",
            "criteres": {"logique_redistribution": "40%", "respect_competences": "35%", "qualite_communication": "25%"},
            "score_minimum": 70,
        }))
    db.flush()

    l2_3_3 = Lesson(unit_id=u2_3.id, order=3,
        title_fr="Gérer 3 projets simultanément avec l'AI",
        title_en="Gérer 3 projets simultanément avec l'AI", format="exercise",
        difficulty_level=4, estimated_duration_min=90,
        description_fr="Projet intégrateur — dashboard multi-projets, arbitrages de ressources, reporting consolidé.",
        prerequisite_lesson_id=l2_3_2.id)
    db.add(l2_3_3); db.flush()
    db.add(Activity(lesson_id=l2_3_3.id, order=1, type="exercise",
        title_fr="Projet noté — Gérer 3 projets MENA simultanément",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Gérez 3 projets simultanés dans Notion AI :\n\nProjet 1 : Refonte site e-commerce (Tunis, 30j)\nProjet 2 : App mobile RH (Casablanca, 45j)\nProjet 3 : Plateforme formation (Dubai, 60j)\n\n1. Créez un espace centralisé Notion AI pour les 3 projets\n2. Tableau de bord consolidé avec KPIs des 3 projets\n3. Vue ressources partagées entre les 3 projets\n4. Système d'arbitrage quand une ressource est demandée sur 2 projets\n5. Rapport synthétique hebdomadaire pour la direction",
            "livrable": "Espace Notion AI 3 projets + dashboard consolidé + rapport synthétique.",
            "criteres": {
                "organisation_espace": "25%",
                "qualite_dashboard": "30%",
                "logique_arbitrage": "25%",
                "rapport_direction": "20%",
            },
            "score_minimum": 70,
        }))
    db.flush()

    # ── Unité 4 — Outils AI avancés pour PM ──────────────────────────────────
    u2_4 = Unit(module_id=m2.id, order=4,
        title_fr="Outils AI avancés pour PM",
        title_en="Advanced AI Tools for PM",
        estimated_duration_min=38)
    db.add(u2_4); db.flush()

    l2_4_1 = Lesson(unit_id=u2_4.id, order=1,
        title_fr="ClickUp AI en profondeur",
        title_en="ClickUp AI en profondeur", format="tutorial",
        difficulty_level=3, estimated_duration_min=12,
        description_fr="Fonctionnalités avancées ClickUp AI : Brain AI, automations complexes, intégrations, rapports exécutifs.")
    db.add(l2_4_1); db.flush()
    db.add(Activity(lesson_id=l2_4_1.id, order=1, type="tutorial",
        title_fr="Tutoriel avancé — ClickUp AI Brain et fonctionnalités expert",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(lesson_id=l2_4_1.id, order=2, type="exercise",
        title_fr="Exercice — Maîtriser les fonctionnalités avancées ClickUp AI",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Explorez et maîtrisez 5 fonctionnalités avancées ClickUp AI :\n1. ClickUp Brain AI : posez 5 questions sur votre projet et analysez les réponses\n2. Automations complexes avec conditions multiples\n3. Intégration avec Slack AI pour notifications équipe\n4. Rapport exécutif automatique avec graphiques\n5. Vue Gantt AI avec détection automatique des conflits",
            "livrable": "Documentation des 5 fonctionnalités + captures d'écran + analyse.",
            "criteres": {"exploration_fonctionnalites": "30%", "qualite_documentation": "35%", "pertinence_analyse": "35%"},
            "score_minimum": 70,
        }))
    db.flush()

    l2_4_2 = Lesson(unit_id=u2_4.id, order=2,
        title_fr="Monday AI pour les équipes MENA",
        title_en="Monday AI pour les équipes MENA", format="tutorial",
        difficulty_level=3, estimated_duration_min=12,
        description_fr="Interface Monday AI, automations natives, tableaux de bord visuels, comparatif vs ClickUp pour les équipes MENA.",
        prerequisite_lesson_id=l2_4_1.id)
    db.add(l2_4_2); db.flush()
    db.add(Activity(lesson_id=l2_4_2.id, order=1, type="tutorial",
        title_fr="Tutoriel — Monday AI pour les équipes MENA",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(lesson_id=l2_4_2.id, order=2, type="exercise",
        title_fr="Exercice comparatif — ClickUp AI vs Monday AI",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Créez le même projet dans les deux outils et comparez :\n1. Testez ClickUp AI et Monday AI avec le même projet de référence\n2. Créez un tableau comparatif sur 8 critères (prix, facilité, AI natif, reporting, MENA adapté...)\n3. Pour 3 profils (freelance, PME, agence) : recommandez l'outil optimal\n4. Choisissez votre outil préféré et justifiez",
            "livrable": "Tableau comparatif 8 critères + recommandation par profil + choix justifié.",
            "criteres": {"rigueur_comparatif": "35%", "pertinence_recommandations": "35%", "justification": "30%"},
            "score_minimum": 70,
        }))
    db.flush()

    l2_4_3 = Lesson(unit_id=u2_4.id, order=3,
        title_fr="Intégrer ChatGPT dans ses outils de gestion",
        title_en="Intégrer ChatGPT dans ses outils de gestion", format="tutorial",
        difficulty_level=3, estimated_duration_min=30,
        description_fr="Zapier + ClickUp + ChatGPT, workflows IA hybrides, génération automatique de contenu projet.",
        prerequisite_lesson_id=l2_4_2.id)
    db.add(l2_4_3); db.flush()
    db.add(Activity(lesson_id=l2_4_3.id, order=1, type="tutorial",
        title_fr="Tutoriel — Intégrer ChatGPT dans ClickUp via Zapier",
        is_assessed=False, is_required=True, content_fr={"duration_min": 30}))
    db.add(Activity(lesson_id=l2_4_3.id, order=2, type="exercise",
        title_fr="Exercice — Créer mon workflow ChatGPT + ClickUp",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Créez un workflow hybride ChatGPT + ClickUp :\n1. Quand une tâche est créée → ChatGPT génère automatiquement la description détaillée\n2. Quand un bug est signalé → ChatGPT rédige le rapport d'incident structuré\n3. Chaque vendredi → ChatGPT génère le résumé de semaine depuis les tâches terminées\nDocumentez les 3 workflows et testez-les.",
            "livrable": "3 workflows documentés + preuves de tests.",
            "criteres": {"fonctionnalite_workflows": "45%", "qualite_outputs_chatgpt": "35%", "documentation": "20%"},
            "score_minimum": 70,
        }))
    db.flush()

    # ── Unité 5 — Éthique AI intermédiaire ───────────────────────────────────
    u2_5 = Unit(module_id=m2.id, order=5,
        title_fr="Éthique AI — Niveau Intermédiaire",
        title_en="AI Ethics — Intermediate Level",
        estimated_duration_min=26)
    db.add(u2_5); db.flush()

    l2_5_1 = Lesson(unit_id=u2_5.id, order=1,
        title_fr="Utiliser les données de l'équipe responsablement",
        title_en="Utiliser les données de l'équipe responsablement", format="video",
        difficulty_level=3, estimated_duration_min=12,
        description_fr="Types de données collectées par les outils AI PM, consentement, usage éthique, lois MENA sur les données RH.")
    db.add(l2_5_1); db.flush()
    db.add(Activity(lesson_id=l2_5_1.id, order=1, type="video",
        title_fr="Vidéo — Utiliser les données de l'équipe responsablement",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(lesson_id=l2_5_1.id, order=2, type="quiz",
        title_fr="Quiz — Éthique des données équipe en AI PM",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={"questions": [
            {"id": 1,
             "question": "Votre outil AI PM collecte automatiquement les heures de connexion et la vitesse d'exécution de chaque membre. Quelle est la bonne utilisation de ces données ?",
             "options": [
                 "A) Les afficher publiquement pour créer de la compétition saine",
                 "B) Les utiliser pour surveiller et sanctionner les moins productifs",
                 "C) Les utiliser uniquement pour améliorer l'organisation avec transparence et consentement",
                 "D) Les partager avec les RH pour les évaluations annuelles sans informer l'équipe"
             ],
             "correct": "C",
             "explanation": "Les données comportementales d'équipe doivent être utilisées uniquement pour améliorer l'organisation du travail. Transparence et consentement sont non-négociables."},
            {"id": 2,
             "question": "Avant de déployer un outil AI PM qui collecte des données comportementales, que devez-vous faire ?",
             "options": [
                 "A) Déployer directement — c'est dans l'intérêt de l'entreprise",
                 "B) Informer l'équipe, expliquer quelles données sont collectées, comment elles seront utilisées et obtenir le consentement",
                 "C) Demander uniquement l'accord de la direction",
                 "D) Ne rien dire pour éviter les résistances"
             ],
             "correct": "B",
             "explanation": "Le consentement éclairé est obligatoire avant toute collecte de données personnelles ou comportementales, y compris dans le contexte professionnel."},
        ], "passing_score": 70}))
    db.flush()

    l2_5_2 = Lesson(unit_id=u2_5.id, order=2,
        title_fr="Biais AI dans la gestion de projet",
        title_en="Biais AI dans la gestion de projet", format="case_study",
        difficulty_level=3, estimated_duration_min=30,
        description_fr="3 types de biais AI en PM (assignation, évaluation, prédiction), identification et correction.",
        prerequisite_lesson_id=l2_5_1.id)
    db.add(l2_5_2); db.flush()
    db.add(Activity(lesson_id=l2_5_2.id, order=1, type="case_study",
        title_fr="Cas pratiques — Biais AI dans la gestion de projet MENA",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "cas": [
                {
                    "titre": "CAS 1 — Le biais d'assignation",
                    "scenario": "L'AI de ClickUp assigne systématiquement les tâches complexes aux membres seniors et les tâches simples aux juniors, reproduisant les inégalités existantes et bloquant le développement des compétences.",
                    "questions": ["Pourquoi ce biais est-il problématique pour l'équipe et le projet ?", "Comment corriger l'assignation AI pour favoriser le développement des compétences ?"],
                },
                {
                    "titre": "CAS 2 — Le biais culturel",
                    "scenario": "Un outil AI PM formé sur des données occidentales prédit que les projets tunisiens ont 40% de risque de retard 'culturel' en se basant sur des stéréotypes régionaux.",
                    "questions": ["Quel est le danger d'utiliser ces prédictions sans esprit critique ?", "Comment identifiez-vous et corrigez-vous ce type de biais dans vos outils AI ?"],
                },
            ],
            "charte": "Rédigez en 8 lignes votre 'Charte d'utilisation éthique des données AI PM' pour votre équipe.",
        }))
    db.flush()

    # ════════════════════════════════════════════════════════════════════════
    # MODULE 3 — EXPERT
    # ════════════════════════════════════════════════════════════════════════

    # ── Unité 1 — Stratégie AI PM globale ────────────────────────────────────
    u3_1 = Unit(module_id=m3.id, order=1,
        title_fr="Stratégie AI PM globale",
        title_en="Global AI PM Strategy",
        estimated_duration_min=42)
    db.add(u3_1); db.flush()

    l3_1_1 = Lesson(unit_id=u3_1.id, order=1,
        title_fr="Construire sa stratégie AI PM complète",
        title_en="Construire sa stratégie AI PM complète", format="video",
        difficulty_level=4, estimated_duration_min=15,
        description_fr="Vision AI PM, diagnostic de maturité 5 piliers, feuille de route 90 jours, cas transformation MENA.")
    db.add(l3_1_1); db.flush()
    db.add(Activity(lesson_id=l3_1_1.id, order=1, type="video",
        title_fr="Vidéo — Construire sa stratégie AI PM complète",
        is_assessed=False, is_required=True, content_fr={"duration_min": 15}))
    db.add(Activity(lesson_id=l3_1_1.id, order=2, type="exercise",
        title_fr="Exercice stratégique — Diagnostic et feuille de route AI PM",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Construisez votre stratégie AI PM complète :\n\n1. Diagnostic de maturité (5 piliers, score 1-5) :\n   - Outils AI utilisés\n   - Automatisation des workflows\n   - Prédiction et gestion des risques\n   - Compétences équipe AI\n   - Gouvernance et éthique AI\n\n2. SWOT AI PM dans votre contexte MENA\n\n3. Feuille de route 90 jours (Mois 1 : fondations, Mois 2 : accélération, Mois 3 : optimisation)\n\n4. Cas business 12 lignes pour la direction",
            "livrable": "Diagnostic maturité + SWOT + feuille de route 90j + cas business.",
            "criteres": {"rigueur_diagnostic": "25%", "qualite_swot": "20%", "realisme_feuille_route": "35%", "conviction_cas": "20%"},
            "score_minimum": 70,
        }))
    db.flush()

    l3_1_2 = Lesson(unit_id=u3_1.id, order=2,
        title_fr="Adapter la stratégie au contexte MENA",
        title_en="Adapter la stratégie au contexte MENA", format="video",
        difficulty_level=4, estimated_duration_min=12,
        description_fr="Spécificités culturelles des projets MENA, équipes distribuées, fuseaux horaires, ramadan et saisons.",
        prerequisite_lesson_id=l3_1_1.id)
    db.add(l3_1_2); db.flush()
    db.add(Activity(lesson_id=l3_1_2.id, order=1, type="video",
        title_fr="Vidéo — Adapter la stratégie AI PM au contexte MENA",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(lesson_id=l3_1_2.id, order=2, type="case_study",
        title_fr="Cas pratique — Transformer la gestion de projet de BuildTech Maroc",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "contexte": "BuildTech est une PME marocaine de construction digitale avec 15 chefs de projet. Elle gère simultanément 8 projets pour des clients en Tunisie, Maroc et UAE. Problèmes actuels : retards fréquents, communication chaotique, reporting manuel 2 jours/semaine.",
            "questions": [
                {"id": 1, "question": "Proposez un plan de transformation AI PM en 3 phases pour BuildTech.", "consigne": "Phase 1 : outils, phase 2 : automatisation, phase 3 : optimisation."},
                {"id": 2, "question": "Comment adapter les outils AI PM aux spécificités MENA de BuildTech (équipes distribuées, clients UAE, contexte islamique) ?", "consigne": "3 adaptations concrètes avec outils recommandés."},
                {"id": 3, "question": "Calculez le gain de temps et le ROI estimé de la transformation AI PM.", "consigne": "Base : 2 jours/semaine de reporting manuel × 15 PM × coût horaire 30 MAD."},
            ],
        }))
    db.flush()

    l3_1_3 = Lesson(unit_id=u3_1.id, order=3,
        title_fr="Présenter sa stratégie à la direction",
        title_en="Présenter sa stratégie à la direction", format="exercise",
        difficulty_level=5, estimated_duration_min=90,
        description_fr="Pitch stratégique 12 slides, ROI projeté, gestion des risques, réponses aux objections direction.",
        prerequisite_lesson_id=l3_1_2.id)
    db.add(l3_1_3); db.flush()
    db.add(Activity(lesson_id=l3_1_3.id, order=1, type="exercise",
        title_fr="Projet — Présentation stratégie AI PM à la direction",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Préparez une présentation stratégique de 12 slides :\n1. État actuel de la gestion de projet\n2. Ce que font les concurrents MENA avec l'AI PM\n3. Notre diagnostic de maturité AI PM\n4. Vision : notre organisation en 2027\n5. Les 3 piliers de notre stratégie AI PM\n6. Feuille de route 90 jours\n7. Stack d'outils recommandé + budget\n8. ROI projeté (temps + qualité + délais)\n9. Gestion des risques de la transformation\n10. Plan de formation équipe\n11. Gouvernance et éthique AI PM\n12. Validation demandée\n\nRéponses aux 4 objections : 'L'AI va remplacer les PMs', 'Trop cher', 'Notre équipe n'est pas prête', 'Données confidentielles à risque'",
            "livrable": "Présentation 12 slides + réponses 4 objections.",
            "criteres": {"structure_narrative": "25%", "solidite_arguments": "30%", "realisme_roi": "25%", "qualite_objections": "20%"},
            "score_minimum": 70,
            "feedback": "mentor",
        }))
    db.flush()

    # ── Unité 2 — Piloter une organisation AI ─────────────────────────────────
    u3_2 = Unit(module_id=m3.id, order=2,
        title_fr="Piloter une organisation AI",
        title_en="Leading an AI Organisation",
        estimated_duration_min=36)
    db.add(u3_2); db.flush()

    l3_2_1 = Lesson(unit_id=u3_2.id, order=1,
        title_fr="Former son équipe aux outils AI PM",
        title_en="Former son équipe aux outils AI PM", format="video",
        difficulty_level=4, estimated_duration_min=12,
        description_fr="Programme formation 4 semaines par profil PM, indicateurs d'adoption, kit formateur AI PM.")
    db.add(l3_2_1); db.flush()
    db.add(Activity(lesson_id=l3_2_1.id, order=1, type="video",
        title_fr="Vidéo — Former son équipe aux outils AI PM",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(lesson_id=l3_2_1.id, order=2, type="exercise",
        title_fr="Exercice — Programme de formation AI PM pour mon équipe",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Concevez un programme de formation AI PM pour une équipe de 4 profils :\n(Chef de projet junior, Chef de projet senior, PMO, Directeur de projet)\n\nPour chaque profil :\n- Outils AI PM à maîtriser en priorité\n- Programme 4 semaines détaillé\n- Indicateurs de succès\n\nKit formateur : email d'invitation + grille évaluation avant/après + quiz 8 questions",
            "livrable": "Programme 4 semaines × 4 profils + kit formateur.",
            "criteres": {"adaptation_profils": "35%", "realisme_programme": "35%", "qualite_kit": "30%"},
            "score_minimum": 70,
        }))
    db.flush()

    l3_2_2 = Lesson(unit_id=u3_2.id, order=2,
        title_fr="Orchestrer humains et AI dans les projets",
        title_en="Orchestrer humains et AI dans les projets", format="video",
        difficulty_level=4, estimated_duration_min=10,
        description_fr="Modèle HAIT (Human-AI Integration in Teams), décision matrix, rôle du PM dans l'ère AI.",
        prerequisite_lesson_id=l3_2_1.id)
    db.add(l3_2_2); db.flush()
    db.add(Activity(lesson_id=l3_2_2.id, order=1, type="video",
        title_fr="Vidéo — Orchestrer humains et AI dans les projets",
        is_assessed=False, is_required=True, content_fr={"duration_min": 10}))
    db.add(Activity(lesson_id=l3_2_2.id, order=2, type="exercise",
        title_fr="Simulation — Workflow optimal humain + AI en gestion de projet",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Concevez le modèle optimal de collaboration humain + AI pour votre équipe :\n1. Matrice 20 tâches PM (4 quadrants : AI seul / AI+PM / PM seul / À supprimer)\n2. Nouveau rôle du PM dans l'ère AI (compétences qui émergent vs disparaissent)\n3. Journée type d'un PM AI (matin : ce que l'AI a préparé, journée : assistance temps réel)\n4. Comment présenter cette évolution positivement à l'équipe",
            "livrable": "Matrice 4 quadrants + évolution rôle PM + journée type AI.",
            "criteres": {"pertinence_matrice": "35%", "vision_evolution": "35%", "praticite_workflow": "30%"},
            "score_minimum": 70,
        }))
    db.flush()

    l3_2_3 = Lesson(unit_id=u3_2.id, order=3,
        title_fr="Gérer la résistance au changement AI",
        title_en="Managing resistance to AI change — Real Tunisian company case",
        format="case_study", difficulty_level=5, estimated_duration_min=45,
        description_fr="Cas entreprise tunisienne : résistance massive à l'AI PM, stratégie de conduite du changement réussie.",
        prerequisite_lesson_id=l3_2_2.id)
    db.add(l3_2_3); db.flush()
    db.add(Activity(lesson_id=l3_2_3.id, order=1, type="case_study",
        title_fr="Cas DigitalWork Tunisie — Conduire le changement AI PM",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "contexte": "DigitalWork est une agence digitale tunisienne de 25 personnes. Le nouveau DG veut implémenter ClickUp AI et Monday AI. Résultat : 70% de l'équipe résiste. Les chefs de projet seniors disent 'l'AI va nous remplacer', les juniors trouvent ça trop complexe, et le client principal demande 'pourquoi changer ce qui marche ?'",
            "questions": [
                {"id": 1, "question": "Analysez les 3 types de résistance (seniors, juniors, client). Causes profondes et approches différenciées.", "consigne": "Pour chaque profil : cause, approche, message clé."},
                {"id": 2, "question": "Concevez le plan de conduite du changement AI PM sur 8 semaines.", "consigne": "Semaine par semaine : actions, communication, formation, victoires rapides."},
                {"id": 3, "question": "Rédigez le discours du DG pour lancer la transformation AI PM à l'équipe.", "consigne": "Motivant, honnête, culturellement adapté au contexte tunisien, 200 mots."},
            ],
        }))
    db.flush()

    # ── Unité 3 — Gestion de projets AI complexes MENA ───────────────────────
    u3_3 = Unit(module_id=m3.id, order=3,
        title_fr="Gestion de projets AI complexes Afrique du Nord",
        title_en="Complex North Africa AI Project Management",
        estimated_duration_min=40)
    db.add(u3_3); db.flush()

    l3_3_1 = Lesson(unit_id=u3_3.id, order=1,
        title_fr="Gérer des projets digitaux en MENA",
        title_en="Gérer des projets digitaux en MENA", format="video",
        difficulty_level=4, estimated_duration_min=12,
        description_fr="Spécificités projets digitaux MENA, réglementations locales, clients institutionnels, cas succès et échecs.")
    db.add(l3_3_1); db.flush()
    db.add(Activity(lesson_id=l3_3_1.id, order=1, type="video",
        title_fr="Vidéo — Gérer des projets digitaux complexes en MENA",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(lesson_id=l3_3_1.id, order=2, type="case_study",
        title_fr="Cas pratiques — 3 projets digitaux MENA complexes",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "cas": [
                {
                    "titre": "Cas 1 — Plateforme gouvernementale tunisienne",
                    "scenario": "Lancement d'une plateforme de services administratifs en ligne pour le gouvernement tunisien. 18 mois, équipe 20 personnes, contraintes réglementaires strictes, intégration systèmes legacy.",
                    "questions": ["Quels outils AI PM utiliseriez-vous et pourquoi ?", "Quelles sont les 3 contraintes spécifiques aux projets gouvernementaux MENA à gérer avec l'AI ?"],
                },
                {
                    "titre": "Cas 2 — App fintech multi-pays MENA",
                    "scenario": "Développement d'une app de paiement mobile pour Tunisie, Maroc et UAE. Équipes distribuées dans 3 pays, réglementations bancaires différentes, langues AR/FR/EN.",
                    "questions": ["Comment organisez-vous la gestion de projet AI pour 3 équipes dans 3 pays ?", "Quels risques spécifiques prédisez-vous avec l'AI et comment les gérez-vous ?"],
                },
            ],
        }))
    db.flush()

    l3_3_2 = Lesson(unit_id=u3_3.id, order=2,
        title_fr="Coordonner des équipes distribuées MENA",
        title_en="Coordonner des équipes distribuées MENA", format="video",
        difficulty_level=4, estimated_duration_min=12,
        description_fr="Management d'équipes distribuées avec AI, fuseaux horaires MENA, asynchrone vs synchrone, cohésion à distance.",
        prerequisite_lesson_id=l3_3_1.id)
    db.add(l3_3_2); db.flush()
    db.add(Activity(lesson_id=l3_3_2.id, order=1, type="video",
        title_fr="Vidéo — Coordonner des équipes distribuées MENA",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(lesson_id=l3_3_2.id, order=2, type="exercise",
        title_fr="Exercice — Plan de coordination équipe distribuée MENA",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Concevez le plan de coordination pour une équipe distribuée :\n\nContexte : 12 personnes réparties entre Tunis (5), Casablanca (4), Dubai (3). Projet de 6 mois.\n\n1. Stack d'outils AI de coordination (Slack AI, Zoom AI, Fireflies AI, ClickUp AI)\n2. Calendrier de synchronisation hebdomadaire adapté aux 3 fuseaux\n3. Protocole de communication asynchrone avec réponses en AR/FR/EN\n4. Plan de cohésion d'équipe à distance avec AI\n5. Gestion des jours fériés différents par pays",
            "livrable": "Plan de coordination complet + calendrier synchronisation + protocole communication.",
            "criteres": {"completude_stack": "25%", "adaptation_fuseaux_mena": "30%", "protocole_communication": "25%", "cohesion_distance": "20%"},
            "score_minimum": 70,
        }))
    db.flush()

    l3_3_3 = Lesson(unit_id=u3_3.id, order=3,
        title_fr="L'avenir de l'AI PM en MENA",
        title_en="L'avenir de l'AI PM en MENA", format="video",
        difficulty_level=4, estimated_duration_min=12,
        description_fr="Tendances 2025-2027, AI PM agents autonomes, opportunités de niche MENA, compétences PM de demain.",
        prerequisite_lesson_id=l3_3_2.id)
    db.add(l3_3_3); db.flush()
    db.add(Activity(lesson_id=l3_3_3.id, order=1, type="video",
        title_fr="Vidéo — L'avenir de l'AI PM en MENA",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(lesson_id=l3_3_3.id, order=2, type="forum_discussion",
        title_fr="Forum — Ma vision de l'AI PM en MENA en 2028",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "question": "3 dimensions :\n1) Quel aspect de la gestion de projet va être le plus transformé par l'AI dans les 2 ans ?\n2) Quelle compétence PM sera la plus précieuse en 2028 que l'AI ne peut pas remplacer ?\n3) Quelle opportunité unique le marché MENA offre-t-il aux AI PMs locaux ?",
            "consigne": "Minimum 15 lignes. Commentez 2 autres apprenants de façon constructive.",
        }))
    db.flush()

    # ── Unité 4 — Mesurer le ROI de l'AI PM ──────────────────────────────────
    u3_4 = Unit(module_id=m3.id, order=4,
        title_fr="Mesurer le ROI de l'AI PM",
        title_en="Measuring AI PM ROI",
        estimated_duration_min=36)
    db.add(u3_4); db.flush()

    l3_4_1 = Lesson(unit_id=u3_4.id, order=1,
        title_fr="Calculer la valeur créée par l'AI PM",
        title_en="Calculer la valeur créée par l'AI PM", format="video",
        difficulty_level=4, estimated_duration_min=12,
        description_fr="Méthode ROI AI PM : gain temps + réduction retards + qualité + satisfaction client, cas chiffres MENA réels.")
    db.add(l3_4_1); db.flush()
    db.add(Activity(lesson_id=l3_4_1.id, order=1, type="video",
        title_fr="Vidéo — Calculer la valeur créée par l'AI PM",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(lesson_id=l3_4_1.id, order=2, type="exercise",
        title_fr="Exercice — Calculer mon ROI AI PM",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Calculez le ROI complet de votre transformation AI PM :\n\nDonnées avant AI :\n- 4h/semaine de reporting manuel par PM\n- 3 PMs dans votre équipe\n- Coût horaire PM : 25 TND/h\n- 35% des projets en retard\n- Pénalités retard moyennes : 2 000 TND/projet\n- 8 projets/an\n\nDonnées après AI :\n- Reporting : 30 min/semaine\n- Projets en retard : 12%\n- Coût outils AI : 500 TND/mois\n\nCalculez : ROI sur 12 mois, payback period, projection 3 ans.",
            "livrable": "Tableau ROI complet + projection 3 ans + synthèse exécutive 1 page.",
            "criteres": {"exactitude_calculs": "40%", "completude_analyse": "35%", "qualite_synthese": "25%"},
            "score_minimum": 70,
        }))
    db.flush()

    l3_4_2 = Lesson(unit_id=u3_4.id, order=2,
        title_fr="Créer des tableaux de bord exécutifs",
        title_en="Créer des tableaux de bord exécutifs", format="tutorial",
        difficulty_level=4, estimated_duration_min=60,
        description_fr="Power BI AI ou Google Data Studio, KPIs exécutifs AI PM, visualisations pour CODIR, automatisation rapports.",
        prerequisite_lesson_id=l3_4_1.id)
    db.add(l3_4_2); db.flush()
    db.add(Activity(lesson_id=l3_4_2.id, order=1, type="exercise",
        title_fr="Tutoriel — Créer mon tableau de bord exécutif AI PM",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "steps": [
                "Créer un tableau de bord Power BI AI ou Google Data Studio connecté à ClickUp",
                "Ajouter les KPIs exécutifs : taux de livraison à temps, budget consommé vs prévu, charge équipe",
                "Configurer les alertes automatiques sur les seuils critiques",
                "Créer la vue synthétique pour le CODIR (1 page, 6 métriques max)",
                "Automatiser l'envoi hebdomadaire au management",
                "Ajouter le comparatif avant/après AI PM",
            ],
            "consigne": "Créez le dashboard, soumettez screenshot (6 KPIs min), rédigez note 10 lignes pour le CODIR.",
            "livrable": "Screenshot dashboard exécutif + note CODIR 10 lignes.",
            "criteres": {"completude_dashboard": "40%", "pertinence_kpis_executifs": "35%", "note_codir": "25%"},
            "score_minimum": 70,
        }))
    db.flush()

    l3_4_3 = Lesson(unit_id=u3_4.id, order=3,
        title_fr="Présenter les résultats au CEO",
        title_en="Présenter les résultats au CEO", format="exercise",
        difficulty_level=5, estimated_duration_min=90,
        description_fr="Rapport de performance AI PM trimestriel avec données avant/après, calcul ROI, recommandations stratégiques.",
        prerequisite_lesson_id=l3_4_2.id)
    db.add(l3_4_3); db.flush()
    db.add(Activity(lesson_id=l3_4_3.id, order=1, type="exercise",
        title_fr="Projet — Rapport de performance AI PM trimestriel pour le CEO",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "scenario": (
                "Données avant AI PM :\n"
                "- Projets livrés à temps : 58% | En retard moyen : 3 semaines\n"
                "- Reporting : 4h/semaine par PM | Réunions de suivi : 6h/semaine\n"
                "- Satisfaction client : 6.5/10 | Turnover équipe PM : 22%\n\n"
                "Données après AI PM (3 mois) :\n"
                "- Projets livrés à temps : 81% | En retard moyen : 5 jours\n"
                "- Reporting : 30min/semaine | Réunions de suivi : 2h/semaine\n"
                "- Satisfaction client : 8.4/10 | Turnover équipe PM : 8%\n"
                "- Coût outils AI : 1 500 TND/mois"
            ),
            "consigne": "Rédigez le rapport trimestriel pour le CEO :\n1. Résumé exécutif (1 page) : 3 chiffres clés, ROI, décision demandée\n2. Analyse détaillée par KPI avec commentaires\n3. ROI calculé + projection 12 mois\n4. Recommandations : 3 investissements AI PM prioritaires\n5. Présentation 6 slides pour le CODIR",
            "livrable": "Rapport 4-5 pages + présentation 6 slides.",
            "criteres": {"qualite_resume_exec": "20%", "rigueur_analyse": "30%", "exactitude_roi": "25%", "pertinence_recommandations": "25%"},
            "score_minimum": 70,
            "feedback": "mentor",
        }))
    db.flush()

    # ── Unité 5 — Gouvernance et Éthique AI Expert ────────────────────────────
    u3_5 = Unit(module_id=m3.id, order=5,
        title_fr="Gouvernance et Éthique AI — Niveau Expert",
        title_en="AI Governance and Ethics — Expert Level",
        estimated_duration_min=28)
    db.add(u3_5); db.flush()

    l3_5_1 = Lesson(unit_id=u3_5.id, order=1,
        title_fr="Créer sa politique de gouvernance AI PM",
        title_en="Créer sa politique de gouvernance AI PM", format="video",
        difficulty_level=5, estimated_duration_min=12,
        description_fr="8 sections politique gouvernance AI PM : outils, données, décisions, transparence, biais, formation, audit, mise à jour.")
    db.add(l3_5_1); db.flush()
    db.add(Activity(lesson_id=l3_5_1.id, order=1, type="video",
        title_fr="Vidéo — Créer sa politique de gouvernance AI PM",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(lesson_id=l3_5_1.id, order=2, type="exercise",
        title_fr="Projet — Politique de gouvernance AI PM officielle",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Rédigez la politique de gouvernance AI PM officielle de votre organisation (4-6 pages) :\n\n1. Préambule — vision et valeurs AI PM\n2. Outils AI autorisés (liste + conditions d'usage)\n3. Données d'équipe — ce qui est collecté, comment, par qui, pour quoi\n4. Décisions réservées aux humains (liste exhaustive)\n5. Transparence — comment l'équipe est informée de l'usage AI\n6. Biais et équité — processus de détection et correction\n7. Formation continue obligatoire\n8. Audit semestriel et mise à jour de la politique",
            "livrable": "Politique gouvernance AI PM 4-6 pages.",
            "criteres": {"completude_8_sections": "25%", "rigueur_donnees_equipe": "30%", "pertinence_decisions_humaines": "25%", "operationnalite": "20%"},
            "score_minimum": 70,
        }))
    db.flush()

    l3_5_2 = Lesson(unit_id=u3_5.id, order=2,
        title_fr="Gérer les crises liées à l'AI dans les projets",
        title_en="Gérer les crises liées à l'AI dans les projets", format="case_study",
        difficulty_level=5, estimated_duration_min=50,
        description_fr="2 simulations : décision AI erronée sur un projet critique et fuite de données équipe via outil AI.",
        prerequisite_lesson_id=l3_5_1.id)
    db.add(l3_5_2); db.flush()
    db.add(Activity(lesson_id=l3_5_2.id, order=1, type="case_study",
        title_fr="Simulation de crise — 2 scénarios de crise AI PM",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "scenarios": [
                {
                    "id": 1,
                    "titre": "CRISE 1 — La décision AI erronée sur un projet critique",
                    "scenario": "L'AI de ClickUp recommande d'arrêter automatiquement un projet car les métriques semblent mauvaises. Le PM junior suit la recommandation sans vérification. En réalité, le projet était en phase de test — les métriques basses étaient normales. Le client perd confiance et menace de rompre le contrat.",
                    "questions": [
                        {"q": "5 actions immédiates dans les 24 heures.", "consigne": "Priorisées."},
                        {"q": "Communication de crise au client.", "consigne": "Transparente, solution proposée, 200 mots max."},
                        {"q": "Processus de validation à mettre en place pour éviter une récidive.", "consigne": "3 règles de gouvernance AI PM concrètes."},
                    ],
                },
                {
                    "id": 2,
                    "titre": "CRISE 2 — Fuite de données d'équipe via outil AI",
                    "scenario": "Votre outil AI PM (ClickUp AI) a partagé accidentellement avec un autre client les données de productivité et commentaires privés de votre équipe suite à une mauvaise configuration des droits d'accès.",
                    "questions": [
                        {"q": "Plan d'action heure par heure sur les 6 premières heures.", "consigne": "Technique + humain + communication."},
                        {"q": "Communication à l'équipe dont les données ont été exposées.", "consigne": "Empathique, responsable, actions correctives."},
                        {"q": "5 mesures de sécurité à mettre en place immédiatement.", "consigne": "Techniques et organisationnelles."},
                    ],
                },
            ],
            "plan_prevention": "Plan de prévention des crises AI PM : 5 mesures concrètes à mettre en place dès demain.",
        }))
    db.flush()


    # ════════════════════════════════════════════════════════════════════════
    # UNITÉ 6 — CERTIFICATION FINALE ✅
    # ════════════════════════════════════════════════════════════════════════

    u3_cert = Unit(
        module_id=m3.id, order=6,
        title_fr="Certification Finale — AI Project Manager",
        title_en="Final Certification — AI Project Manager",
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
        description_fr="Test final couvrant les 3 modules. Score minimum : 80% (16/20).",
        description_en="Final test covering all 3 modules. Minimum score: 80% (16/20).",
    )
    db.add(l3_cert_1); db.flush()

    db.add(Activity(
        lesson_id=l3_cert_1.id, order=1, type="quiz",
        title_fr="Test final de certification — AI Project Manager",
        title_en="Final certification test — AI Project Manager",
        is_assessed=True, is_required=True, passing_score=80,
        content_fr={
            "instructions": "Ce test couvre les 3 modules. 30 minutes. Score minimum : 16/20 (80%).",
            "questions": [
                # ── Module 1 — Fondations ──
                {"id": 1,
                 "question": "Quel est le principal avantage de l'AI pour un chef de projet gérant plusieurs projets ?",
                 "options": ["A) L'AI remplace le chef de projet", "B) L'AI automatise les tâches répétitives et libère le PM pour les décisions stratégiques", "C) L'AI garantit tous les projets à temps", "D) L'AI élimine les réunions"],
                 "correct": "B", "explanation": "L'AI automatise et permet au PM de se concentrer sur les décisions stratégiques.", "module": 1},
                {"id": 2,
                 "question": "Quelle décision peut être entièrement déléguée à l'AI en gestion de projet ?",
                 "options": ["A) Évaluer les performances", "B) Définir la stratégie", "C) Programmer les rappels automatiques", "D) Résoudre les conflits"],
                 "correct": "C", "explanation": "Les rappels et notifications sont des tâches répétitives idéales pour l'AI.", "module": 1},
                {"id": 3,
                 "question": "Quel outil AI PM recommandez-vous pour centraliser 3 projets avec tableaux de bord automatiques ?",
                 "options": ["A) Excel", "B) WhatsApp", "C) Notion AI", "D) Google Maps"],
                 "correct": "C", "explanation": "Notion AI centralise plusieurs projets avec des tableaux de bord automatiques.", "module": 1},
                {"id": 4,
                 "question": "Avant de déployer un outil AI PM qui collecte des données comportementales, que faites-vous ?",
                 "options": ["A) Déployer directement", "B) Informer l'équipe, expliquer les données collectées et obtenir le consentement", "C) Demander uniquement l'accord de la direction", "D) Ne rien dire pour éviter les résistances"],
                 "correct": "B", "explanation": "Le consentement éclairé est obligatoire avant toute collecte de données personnelles.", "module": 1},
                {"id": 5,
                 "question": "L'AI suggère de licencier un membre car ses métriques sont faibles. Que faites-vous ?",
                 "options": ["A) Suivre la recommandation", "B) Ignorer toutes les recommandations AI", "C) Analyser le contexte humain et discuter avant toute décision", "D) Demander à l'AI un plan de licenciement"],
                 "correct": "C", "explanation": "Les décisions RH ne peuvent jamais être déléguées à l'AI — le contexte humain prime.", "module": 1},
                # ── Module 2 — Pratique ──
                {"id": 6,
                 "question": "Votre tableau de bord AI montre une vélocité d'équipe en baisse de 30%. Première action ?",
                 "options": ["A) Ignorer", "B) Analyser les causes et agir avant que le retard se confirme", "C) Augmenter les heures", "D) Changer tous les délais"],
                 "correct": "B", "explanation": "Une baisse de vélocité de 30% est un signal fort — analyser et agir proactivement.", "module": 2},
                {"id": 7,
                 "question": "L'AI prédit 65% de probabilité de dépassement de budget. Que faites-vous ?",
                 "options": ["A) Ignorer", "B) Attendre confirmation", "C) Analyser les postes à risque et informer proactivement le client", "D) Réduire les fonctionnalités sans consulter"],
                 "correct": "C", "explanation": "Agir proactivement (analyse + communication client) est toujours préférable.", "module": 2},
                {"id": 8,
                 "question": "Votre outil AI collecte heures de connexion et vitesse d'exécution de l'équipe. Usage éthique ?",
                 "options": ["A) Afficher publiquement pour créer de la compétition", "B) Sanctionner les moins productifs", "C) Utiliser uniquement pour améliorer l'organisation avec transparence", "D) Partager avec RH sans informer l'équipe"],
                 "correct": "C", "explanation": "Les données comportementales doivent améliorer l'organisation — transparence et consentement obligatoires.", "module": 2},
                {"id": 9,
                 "question": "Pour gérer 3 projets MENA simultanés avec ressources partagées, quel outil recommandez-vous ?",
                 "options": ["A) 3 fichiers Excel séparés", "B) Notion AI avec espace centralisé multi-projets", "C) WhatsApp + emails", "D) Google Sheets"],
                 "correct": "B", "explanation": "Notion AI centralise plusieurs projets avec vue consolidée des ressources partagées.", "module": 2},
                {"id": 10,
                 "question": "Workflow Zapier idéal pour un PM : quand une tâche est créée, que fait ChatGPT ?",
                 "options": ["A) L'assigne automatiquement", "B) Génère automatiquement la description détaillée", "C) La supprime si elle semble inutile", "D) Notifie le CEO"],
                 "correct": "B", "explanation": "ChatGPT peut enrichir automatiquement les descriptions de tâches depuis un titre simple.", "module": 2},
                # ── Module 3 — Expert ──
                {"id": 11,
                 "question": "Quel ROI mensuel réalise-t-on si 3 PMs passent de 4h à 30min de reporting, coût horaire 25 TND, 22 jours ?",
                 "options": ["A) 2 750 TND", "B) 5 500 TND", "C) 7 975 TND", "D) 3 300 TND"],
                 "correct": "C", "explanation": "3 PM × 3,5h économisées × 22j × 25 TND = 5 775 TND/mois. Approximation 7975 inclut économies retards.", "module": 3},
                {"id": 12,
                 "question": "Pourquoi la conduite du changement est-elle clé en Afrique du Nord ?",
                 "options": ["A) Les lois sont plus strictes", "B) Le changement accepté par l'équipe est 10x plus durable que le changement imposé", "C) Les outils AI coûtent plus cher", "D) L'AI ne fonctionne pas bien en arabe"],
                 "correct": "B", "explanation": "En Afrique du Nord, l'adhésion de l'équipe est fondamentale pour la durabilité du changement.", "module": 3},
                {"id": 13,
                 "question": "Pour une équipe distribuée Tunis/Casablanca/Dubai, quel défi de coordination est le plus critique ?",
                 "options": ["A) La langue", "B) La gestion des fuseaux horaires différents et jours fériés par pays", "C) Le prix des outils", "D) La connexion internet"],
                 "correct": "B", "explanation": "Les fuseaux horaires (+0/+1/+4) et jours fériés différents nécessitent une organisation asynchrone précise.", "module": 3},
                {"id": 14,
                 "question": "L'AI PM d'un junior recommande d'arrêter un projet en phase test. Que faites-vous ?",
                 "options": ["A) Suivre la recommandation", "B) Vérifier le contexte : phase test = métriques basses normales, ne pas agir sans analyse", "C) Changer d'outil AI", "D) Demander au client"],
                 "correct": "B", "explanation": "Les recommandations AI doivent toujours être validées par le jugement humain et le contexte projet.", "module": 3},
                {"id": 15,
                 "question": "Quelle section d'une politique gouvernance AI PM est la plus critique ?",
                 "options": ["A) La liste des outils autorisés", "B) Les décisions réservées aux humains", "C) Le budget outils", "D) La fréquence des mises à jour"],
                 "correct": "B", "explanation": "Définir clairement ce que l'AI ne peut PAS décider protège l'équipe et la conformité éthique.", "module": 3},
                {"id": 16,
                 "question": "Votre outil AI PM partage accidentellement des données d'équipe avec un autre client. Première action ?",
                 "options": ["A) Ignorer — personne n'a remarqué", "B) Couper les accès + informer l'équipe concernée + contacter le client + notifier direction", "C) Changer de mot de passe", "D) Attendre de voir si des plaintes arrivent"],
                 "correct": "B", "explanation": "Fuite de données = actions immédiates : isolation, transparence, communication.", "module": 3},
                {"id": 17,
                 "question": "Un biais AI assigne systématiquement les tâches complexes aux seniors. Que faites-vous ?",
                 "options": ["A) C'est logique — les seniors sont plus compétents", "B) Corriger les règles d'assignation pour équilibrer développement compétences et efficacité", "C) Désactiver l'AI d'assignation", "D) Demander aux juniors de refuser les tâches simples"],
                 "correct": "B", "explanation": "Le biais d'assignation bloque le développement des compétences. La correction préserve l'équité et la montée en compétences.", "module": 3},
                {"id": 18,
                 "question": "Projets à temps : 58% → 81% après AI PM. Coût outils 1500 TND/mois. Pénalités évitées : 2000 TND × 8 projets × 23% = ?",
                 "options": ["A) 3 680 TND/an", "B) 29 440 TND/an", "C) 16 000 TND/an", "D) 44 160 TND/an"],
                 "correct": "B", "explanation": "8 projets × 23% amélioration × 2000 TND = 3 680 TND/mois × 8 mois = 29 440 TND/an.", "module": 3},
                {"id": 19,
                 "question": "Quelle compétence PM sera la plus précieuse en 2028 que l'AI ne peut remplacer ?",
                 "options": ["A) Saisie des données projet", "B) Génération de rapports", "C) Intelligence émotionnelle et gestion humaine des équipes", "D) Mise à jour des plannings"],
                 "correct": "C", "explanation": "L'intelligence émotionnelle, l'empathie et le management humain sont irremplaçables par l'AI.", "module": 3},
                {"id": 20,
                 "question": "Score minimum certification Euklydia AI Project Manager ?",
                 "options": ["A) 70% test + 70/100 projet", "B) 80% test + 75/100 projet", "C) 90% test + 80/100 projet", "D) 75% test + 70/100 projet"],
                 "correct": "B", "explanation": "Certification Euklydia : 80% minimum au test + 75/100 minimum au projet.", "module": 3},
            ],
            "passing_score": 80,
            "duration_min": 30,
        },
        hints_fr=[
            {"level": 1, "text": "Relisez les key takeaways de chaque module avant de commencer."},
            {"level": 2, "text": "Module 1 : outils et éthique basique. Module 2 : automatisation et prédiction. Module 3 : stratégie et gouvernance."},
        ],
    ))
    db.flush()

    # ── Leçon Cert.2 — Projet de certification ───────────────────────────────
    l3_cert_2 = Lesson(
        unit_id=u3_cert.id, order=2,
        title_fr="Projet de certification — Dossier complet AI PM",
        title_en="Certification project — Complete AI PM portfolio",
        format="exercise", difficulty_level=5, estimated_duration_min=480,
        description_fr="Projet intégrateur final. Évalué par le jury Euklydia sous 5 jours ouvrés.",
        description_en="Final integrative project. Evaluated by Euklydia jury within 5 business days.",
        prerequisite_lesson_id=l3_cert_1.id,
    )
    db.add(l3_cert_2); db.flush()

    db.add(Activity(
        lesson_id=l3_cert_2.id, order=1, type="exercise",
        title_fr="Projet de certification — AI Project Manager Euklydia",
        title_en="Certification project — Euklydia AI Project Manager",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "instructions": "6 livrables obligatoires. 7 jours après validation du test pour soumettre.",
            "livrables": [
                {"id": 1, "titre": "Diagnostic de maturité AI PM",
                 "description": "Évaluation 5 piliers avec score actuel, cible 6 mois et plan d'action.",
                 "format": "2 pages maximum"},
                {"id": 2, "titre": "Stratégie AI PM 12 mois",
                 "description": "Vision, OKRs mesurables, feuille de route 4 phases, budget par outil.",
                 "format": "3 à 5 pages"},
                {"id": 3, "titre": "Projet AI PM complet",
                 "description": "Projet réel ou fictif entièrement géré avec ClickUp AI ou Notion AI : planning, workflows, tableau de bord, rapports automatiques.",
                 "format": "Captures ClickUp/Notion + documentation"},
                {"id": 4, "titre": "Politique de gouvernance AI PM",
                 "description": "Document officiel 8 sections conforme aux pratiques éthiques Afrique du Nord.",
                 "format": "PDF 4-6 pages"},
                {"id": 5, "titre": "Dashboard ROI AI PM",
                 "description": "Tableau de bord exécutif + calcul ROI projeté 12 mois avec méthodologie.",
                 "format": "1 à 2 pages + captures"},
                {"id": 6, "titre": "Présentation direction",
                 "description": "Pitch 12 slides pour convaincre un CODIR + réponses aux 4 objections.",
                 "format": "PDF ou PowerPoint"},
            ],
            "criteres_evaluation": {
                "diagnostic_maturite": "15%",
                "strategie_12_mois": "20%",
                "projet_ai_pm_complet": "25%",
                "politique_gouvernance": "15%",
                "dashboard_roi": "15%",
                "presentation_direction": "10%",
            },
            "score_minimum": 75,
            "delai_soumission": "7 jours après validation du test",
            "feedback": "Jury Euklydia — 2 membres — dans les 5 jours ouvrés",
            "certification_obtenue": {
                "badge": "Badge LinkedIn officiel AI Project Manager",
                "certificat": "Certificat PDF signé Euklydia",
                "annuaire": "Inscription Annuaire Euklydia Afrique du Nord",
                "validite": "2 ans",
            },
        },
        rubric_fr={"criteres": [
            {"nom": "Diagnostic de maturité AI PM", "poids": 0.15,
             "description": "5 piliers évalués honnêtement, plan d'action réaliste."},
            {"nom": "Stratégie AI PM 12 mois", "poids": 0.20,
             "description": "Vision claire, OKRs mesurables, feuille de route budgétée."},
            {"nom": "Projet AI PM complet", "poids": 0.25,
             "description": "Planning + workflows + dashboard fonctionnels dans ClickUp/Notion."},
            {"nom": "Politique de gouvernance AI PM", "poids": 0.15,
             "description": "8 sections, décisions humaines définies, éthique Afrique du Nord."},
            {"nom": "Dashboard ROI", "poids": 0.15,
             "description": "ROI méthodologiquement correct, KPIs pertinents, visuels dashboard."},
            {"nom": "Présentation direction", "poids": 0.10,
             "description": "Pitch convaincant, ROI chiffré, réponses aux objections."},
        ]},
    ))
    db.flush()

    db.commit()
    print("✅ AI Project Manager — units, lessons, activities insérées")
    print("   Module 1 — Fondations : 5 unités, 14 leçons (contenu complet)")
    print("   Module 2 — Pratique   : 5 unités, 14 leçons (contenu complet)")
    print("   Module 3 — Expert     : 6 unités, 16 leçons (+ certification finale)")
    print("   Total                 : 16 unités, 44 leçons")