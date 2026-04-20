"""
Seed Units, Lessons, Activities — AI Designer (role_id=81)
Module 1 — Fondations : 5 unités, 14 leçons, contenu complet
Module 2 — Pratique   : 5 unités, 14 leçons, contenu complet
Module 3 — Expert     : 5 unités, 14 leçons, contenu complet
Total                 : 15 unités, 42 leçons

Ordre d'exécution :
  1. seed_ai_designer_assessment.py
  2. seed_ai_designer_modules.py
  3. seed_ai_designer_units_lessons.py  ← ce fichier
"""

from app.models.module import Module
from app.models.unit import Unit
from app.models.lesson import Lesson
from app.models.activity import Activity


def seed_ai_designer_units_lessons(db):

    # ── Récupérer les 3 modules ───────────────────────────────────────────────
    m1 = db.query(Module).filter_by(role="AI Designer", journey_stage="foundation").first()
    m2 = db.query(Module).filter_by(role="AI Designer", journey_stage="practice").first()
    m3 = db.query(Module).filter_by(role="AI Designer", journey_stage="expert").first()

    if not all([m1, m2, m3]):
        print("❌ Modules AI Designer introuvables — lancer seed_ai_designer_modules.py d'abord")
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

    # ── Unité 1 — L'AI dans le design ────────────────────────────────────────
    u1_1 = Unit(module_id=m1.id, order=1,
        title_fr="L'AI dans le design",
        title_en="AI in Design",
        description_fr="Comprendre le design AI, ses outils essentiels et ses spécificités pour le marché Afrique du Nord.",
        estimated_duration_min=26)
    db.add(u1_1); db.flush()

    l1_1_1 = Lesson(unit_id=u1_1.id, order=1,
        title_fr="C'est quoi le design AI ?",
        title_en="C'est quoi le design AI ?", format="video",
        difficulty_level=1, estimated_duration_min=10,
        description_fr="Définition du design AI, révolution créative, 5 catégories d'outils, évolution historique.")
    db.add(l1_1_1); db.flush()
    db.add(Activity(lesson_id=l1_1_1.id, order=1, type="video",
        title_fr="Vidéo — C'est quoi le design AI ?",
        is_assessed=False, is_required=True, content_fr={"duration_min": 10, "url_fr": None}))
    db.add(Activity(lesson_id=l1_1_1.id, order=2, type="quiz",
        title_fr="Quiz — Le design AI",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={"questions": [
            {"id": 1,
             "question": "Quel est le principal avantage du design AI pour un graphiste indépendant tunisien ?",
             "options": [
                 "A) L'AI remplace complètement les compétences créatives",
                 "B) L'AI permet de produire des visuels professionnels plus rapidement et à moindre coût",
                 "C) L'AI garantit automatiquement l'originalité de chaque création",
                 "D) L'AI élimine le besoin de connaître les outils de design traditionnels"
             ],
             "correct": "B",
             "explanation": "Le design AI permet de produire des visuels professionnels plus rapidement et à moindre coût, permettant aux designers MENA de rivaliser avec les grandes agences."},
            {"id": 2,
             "question": "Parmi les 5 catégories d'outils design AI, laquelle est indispensable pour créer une identité visuelle complète ?",
             "options": [
                 "A) Outils de génération de texte uniquement",
                 "B) Outils de génération d'images + UI/UX + Brand Assets",
                 "C) Uniquement les outils de création vidéo",
                 "D) Les outils d'analyse de données"
             ],
             "correct": "B",
             "explanation": "Une identité visuelle complète nécessite la combinaison d'outils de génération d'images (Midjourney), UI/UX (Figma AI) et brand assets (Looka AI, Adobe Express AI)."},
        ], "passing_score": 70},
        hints_fr=[
            {"level": 1, "text": "Le design AI ne remplace pas la créativité humaine — il l'amplifie. Le designer reste le directeur artistique."},
        ]))
    db.flush()

    l1_1_2 = Lesson(unit_id=u1_1.id, order=2,
        title_fr="Les outils AI essentiels du designer",
        title_en="Les outils AI essentiels du designer", format="video",
        difficulty_level=1, estimated_duration_min=8,
        description_fr="5 catégories d'outils, tableau comparatif prix/niveau, stack gratuit pour démarrer.",
        prerequisite_lesson_id=l1_1_1.id)
    db.add(l1_1_2); db.flush()
    db.add(Activity(lesson_id=l1_1_2.id, order=1, type="video",
        title_fr="Vidéo — Les outils AI essentiels du designer",
        is_assessed=False, is_required=True, content_fr={"duration_min": 8}))
    db.add(Activity(lesson_id=l1_1_2.id, order=2, type="quiz",
        title_fr="Quiz — Outils AI design",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={"questions": [
            {"id": 1,
             "question": "Quel outil AI gratuit recommandez-vous pour démarrer la génération d'images ?",
             "options": ["A) Midjourney", "B) Canva AI", "C) Adobe Illustrator AI", "D) Stable Diffusion"],
             "correct": "B",
             "explanation": "Canva AI propose une version gratuite puissante pour créer des visuels professionnels sans compétences avancées en design."},
            {"id": 2,
             "question": "Pour créer des wireframes d'application mobile rapidement avec l'AI, quel outil choisissez-vous ?",
             "options": ["A) Canva AI", "B) Midjourney", "C) Figma AI ou Uizard AI", "D) ElevenLabs"],
             "correct": "C",
             "explanation": "Figma AI et Uizard AI sont spécialisés dans la création de wireframes et maquettes UI/UX à partir d'une description textuelle."},
        ], "passing_score": 70}))
    db.flush()

    l1_1_3 = Lesson(unit_id=u1_1.id, order=3,
        title_fr="Le design AI dans le contexte MENA",
        title_en="Le design AI dans le contexte MENA", format="video",
        difficulty_level=1, estimated_duration_min=8,
        description_fr="Spécificités visuelles MENA, direction RTL, typographie arabe, codes couleurs culturels, cas marque tunisienne.",
        prerequisite_lesson_id=l1_1_2.id)
    db.add(l1_1_3); db.flush()
    db.add(Activity(lesson_id=l1_1_3.id, order=1, type="video",
        title_fr="Vidéo — Le design AI dans le contexte MENA",
        is_assessed=False, is_required=True, content_fr={"duration_min": 8}))
    db.add(Activity(lesson_id=l1_1_3.id, order=2, type="forum_discussion",
        title_fr="Forum — Le design AI dans votre contexte créatif",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "question": "Comment le design AI peut-il valoriser l'esthétique visuelle tunisienne et arabe ? Partagez un exemple de projet design MENA que vous aimeriez réaliser avec l'AI.",
            "consigne": "Minimum 5 lignes. Décrivez votre secteur, un défi design concret et un outil AI à tester. Commentez au moins 2 contributions de vos pairs.",
        }))
    db.flush()

    # ── Unité 2 — Générer ses premières images AI ─────────────────────────────
    u1_2 = Unit(module_id=m1.id, order=2,
        title_fr="Générer ses premières images AI",
        title_en="Generating your First AI Images",
        description_fr="Maîtriser Midjourney et Canva AI pour créer des images adaptées au marché Afrique du Nord.",
        estimated_duration_min=42)
    db.add(u1_2); db.flush()

    l1_2_1 = Lesson(unit_id=u1_2.id, order=1,
        title_fr="Introduction à Midjourney",
        title_en="Introduction à Midjourney", format="tutorial",
        difficulty_level=2, estimated_duration_min=12,
        description_fr="Interface Midjourney, premiers prompts, paramètres de base, account setup.")
    db.add(l1_2_1); db.flush()
    db.add(Activity(lesson_id=l1_2_1.id, order=1, type="tutorial",
        title_fr="Tutoriel guidé — Midjourney pas à pas",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(lesson_id=l1_2_1.id, order=2, type="exercise",
        title_fr="Exercice — Générez vos 3 premières images avec Midjourney",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "1. Créez un compte Midjourney.\n2. Générez 3 images pour une marque tunisienne de votre choix.\n3. Testez au moins 2 paramètres différents (--ar, --style, --v).\n4. Comparez les résultats et choisissez la meilleure image.",
            "livrable": "3 images générées + capture des prompts utilisés + justification du choix final.",
            "criteres": {"maitrise_interface": "30%", "qualite_prompts": "40%", "qualite_images": "30%"},
            "score_minimum": 70,
        },
        hints_fr=[
            {"level": 1, "text": "Commencez par des prompts simples : '[sujet], [style], [ambiance], --ar 16:9'. Ajoutez des détails progressivement."},
            {"level": 2, "text": "Pour le marché MENA : ajoutez 'North African aesthetic', 'Arabic style', 'Tunisian culture' dans votre prompt pour des résultats plus adaptés."},
        ]))
    db.flush()

    l1_2_2 = Lesson(unit_id=u1_2.id, order=2,
        title_fr="Créer des prompts visuels efficaces",
        title_en="Créer des prompts visuels efficaces", format="video",
        difficulty_level=2, estimated_duration_min=12,
        description_fr="Anatomie du prompt parfait, mots clés visuels, style, ambiance, technique, négatifs, itération.",
        prerequisite_lesson_id=l1_2_1.id)
    db.add(l1_2_2); db.flush()
    db.add(Activity(lesson_id=l1_2_2.id, order=1, type="video",
        title_fr="Vidéo — Créer des prompts visuels efficaces",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(lesson_id=l1_2_2.id, order=2, type="exercise",
        title_fr="Exercice — Maîtriser l'art du prompt visuel",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Créez 5 prompts progressifs pour le même sujet :\n1. Prompt basique (5 mots)\n2. Prompt avec style artistique\n3. Prompt avec ambiance et éclairage\n4. Prompt avec contexte culturel MENA\n5. Prompt complet optimisé\nComparez les 5 résultats et analysez l'évolution de la qualité.",
            "livrable": "5 prompts + 5 images générées + analyse comparative.",
            "criteres": {"progression_qualite": "40%", "adaptation_mena": "35%", "analyse_comparative": "25%"},
            "score_minimum": 70,
        },
        hints_fr=[
            {"level": 1, "text": "Structure du prompt parfait : Sujet + Style + Ambiance + Technique + Paramètres. Ex : 'Tunisian woman entrepreneur, modern minimalist, golden hour lighting, professional photography, --ar 1:1 --v 6'"},
            {"level": 2, "text": "Négatifs utiles pour le MENA : '--no western, cartoon, blurry, low quality, watermark'"},
        ]))
    db.flush()

    l1_2_3 = Lesson(unit_id=u1_2.id, order=3,
        title_fr="Générer des images adaptées au marché MENA",
        title_en="Générer des images adaptées au marché MENA", format="exercise",
        difficulty_level=3, estimated_duration_min=60,
        description_fr="Projet noté — campagne visuelle complète pour une marque tunisienne avec Midjourney et Adobe Firefly.",
        prerequisite_lesson_id=l1_2_2.id)
    db.add(l1_2_3); db.flush()
    db.add(Activity(lesson_id=l1_2_3.id, order=1, type="exercise",
        title_fr="Projet noté — Ma première campagne visuelle MENA",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Créez une campagne visuelle complète pour une marque tunisienne réelle ou fictive :\n\n1. Générez 5 visuels avec Midjourney culturellement adaptés MENA\n2. Créez 3 variantes avec Adobe Firefly (droits commerciaux inclus)\n3. Adaptez pour 3 formats : post Instagram (1:1), story (9:16), bannière web (16:9)\n4. Rédigez une note de 10 lignes sur vos choix culturels et esthétiques",
            "livrable": "8 visuels finaux (formats variés) + note de direction artistique.",
            "criteres": {
                "qualite_prompts": "25%",
                "adaptation_culturelle_mena": "35%",
                "maitrise_formats": "20%",
                "note_artistique": "20%",
            },
            "score_minimum": 70,
        },
        rubric_fr={"criteres": [
            {"nom": "Qualité des prompts", "poids": 0.25, "description": "Prompts précis, culturellement contextualisés, itération visible."},
            {"nom": "Adaptation culturelle MENA", "poids": 0.35, "description": "Codes visuels MENA respectés, typographie adaptée, esthétique locale."},
            {"nom": "Maîtrise des formats", "poids": 0.20, "description": "3 formats corrects, compositions adaptées à chaque format."},
            {"nom": "Note artistique", "poids": 0.20, "description": "Cohérence de la direction artistique, justification des choix."},
        ]}))
    db.flush()

    # ── Unité 3 — Design UI/UX basique avec AI ────────────────────────────────
    u1_3 = Unit(module_id=m1.id, order=3,
        title_fr="Design UI/UX basique avec AI",
        title_en="Basic UI/UX Design with AI",
        description_fr="Créer ses premiers wireframes avec Figma AI et adapter le design au contexte MENA.",
        estimated_duration_min=38)
    db.add(u1_3); db.flush()

    l1_3_1 = Lesson(unit_id=u1_3.id, order=1,
        title_fr="C'est quoi l'UI/UX ?",
        title_en="C'est quoi l'UI/UX ?", format="video",
        difficulty_level=1, estimated_duration_min=10,
        description_fr="UI vs UX, principes de base, spécificités mobiles MENA, direction RTL, exemples d'apps arabes.")
    db.add(l1_3_1); db.flush()
    db.add(Activity(lesson_id=l1_3_1.id, order=1, type="video",
        title_fr="Vidéo — C'est quoi l'UI/UX ?",
        is_assessed=False, is_required=True, content_fr={"duration_min": 10}))
    db.add(Activity(lesson_id=l1_3_1.id, order=2, type="quiz",
        title_fr="Quiz — Fondamentaux UI/UX",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={"questions": [
            {"id": 1,
             "question": "Quelle est la différence principale entre UI et UX ?",
             "options": [
                 "A) UI = ce que l'utilisateur ressent, UX = ce qu'il voit",
                 "B) UI = l'aspect visuel de l'interface, UX = l'expérience globale de l'utilisateur",
                 "C) UI et UX sont exactement la même chose",
                 "D) UI = mobile, UX = desktop"
             ],
             "correct": "B",
             "explanation": "UI (User Interface) concerne l'aspect visuel et graphique, tandis que UX (User Experience) concerne l'expérience globale, l'ergonomie et la facilité d'utilisation."},
            {"id": 2,
             "question": "Vous designez une application en arabe pour le marché tunisien. Quelle est la première adaptation à faire ?",
             "options": [
                 "A) Changer uniquement les couleurs",
                 "B) Inverser la direction de lecture : passer en RTL (droite à gauche)",
                 "C) Utiliser une police latine avec caractères arabes",
                 "D) Aucune adaptation nécessaire"
             ],
             "correct": "B",
             "explanation": "La direction RTL (Right-to-Left) est fondamentale pour les interfaces arabes. Elle change tout : navigation, icônes, mise en page, et logique de lecture."},
        ], "passing_score": 70}))
    db.flush()

    l1_3_2 = Lesson(unit_id=u1_3.id, order=2,
        title_fr="Créer ses premiers wireframes avec Figma AI",
        title_en="Créer ses premiers wireframes avec Figma AI", format="tutorial",
        difficulty_level=2, estimated_duration_min=12,
        description_fr="Interface Figma AI, génération wireframes depuis texte, composants auto-générés, export.",
        prerequisite_lesson_id=l1_3_1.id)
    db.add(l1_3_2); db.flush()
    db.add(Activity(lesson_id=l1_3_2.id, order=1, type="tutorial",
        title_fr="Tutoriel guidé — Figma AI pas à pas",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(lesson_id=l1_3_2.id, order=2, type="exercise",
        title_fr="Exercice — Créez votre premier wireframe avec Figma AI",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Créez un wireframe d'application mobile pour une startup tunisienne :\n1. Choisissez un secteur (e-commerce, livraison, éducation...)\n2. Générez le wireframe avec Figma AI depuis une description textuelle\n3. Créez minimum 3 écrans : accueil, liste, détail\n4. Vérifiez la lisibilité mobile (taille des éléments cliquables)",
            "livrable": "3 écrans wireframe exportés en PNG.",
            "criteres": {"structure_navigation": "35%", "lisibilite_mobile": "35%", "coherence_ecrans": "30%"},
            "score_minimum": 70,
        }))
    db.flush()

    l1_3_3 = Lesson(unit_id=u1_3.id, order=3,
        title_fr="Adapter le design au contexte MENA",
        title_en="Adapter le design au contexte MENA", format="video",
        difficulty_level=2, estimated_duration_min=10,
        description_fr="RTL en pratique, typographies arabes, codes couleurs culturels, cas app e-commerce tunisienne.",
        prerequisite_lesson_id=l1_3_2.id)
    db.add(l1_3_3); db.flush()
    db.add(Activity(lesson_id=l1_3_3.id, order=1, type="video",
        title_fr="Vidéo — Adapter le design UI/UX au contexte MENA",
        is_assessed=False, is_required=True, content_fr={"duration_min": 10}))
    db.add(Activity(lesson_id=l1_3_3.id, order=2, type="exercise",
        title_fr="Exercice — Adapter un design LTR en RTL",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Prenez un wireframe existant (fourni ou créé précédemment) et adaptez-le pour le marché arabe :\n1. Inversez la direction en RTL\n2. Remplacez les polices latines par Google Fonts Arabic\n3. Adaptez la palette de couleurs aux codes culturels MENA\n4. Vérifiez chaque élément (icônes, flèches, navigation)",
            "livrable": "Version LTR + Version RTL côte à côte + note d'adaptation.",
            "criteres": {"correcte_direction_rtl": "40%", "typographie_arabe": "30%", "coherence_visuelle": "30%"},
            "score_minimum": 70,
        }))
    db.flush()

    # ── Unité 4 — Créer ses premiers brand assets ─────────────────────────────
    u1_4 = Unit(module_id=m1.id, order=4,
        title_fr="Créer ses premiers brand assets",
        title_en="Creating your First Brand Assets",
        description_fr="Créer un logo, une palette de couleurs et des templates de base avec les outils AI.",
        estimated_duration_min=36)
    db.add(u1_4); db.flush()

    l1_4_1 = Lesson(unit_id=u1_4.id, order=1,
        title_fr="C'est quoi un système de brand assets ?",
        title_en="C'est quoi un système de brand assets ?", format="video",
        difficulty_level=1, estimated_duration_min=10,
        description_fr="Logo, palette, typographie, templates — les 4 piliers de l'identité visuelle, exemples MENA.")
    db.add(l1_4_1); db.flush()
    db.add(Activity(lesson_id=l1_4_1.id, order=1, type="video",
        title_fr="Vidéo — C'est quoi un système de brand assets ?",
        is_assessed=False, is_required=True, content_fr={"duration_min": 10}))
    db.add(Activity(lesson_id=l1_4_1.id, order=2, type="quiz",
        title_fr="Quiz — Fondamentaux brand assets",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={"questions": [
            {"id": 1,
             "question": "Quel est l'ordre correct pour créer une identité visuelle complète avec l'AI ?",
             "options": [
                 "A) Templates → Logo → Palette → Typographie",
                 "B) Logo → Palette de couleurs → Typographie → Templates",
                 "C) Typographie → Palette → Templates → Logo",
                 "D) L'ordre n'a pas d'importance"
             ],
             "correct": "B",
             "explanation": "Le logo est le point de départ — il définit l'ADN visuel de la marque. La palette et la typographie en découlent, puis les templates reprennent tous ces éléments de façon cohérente."},
        ], "passing_score": 70}))
    db.flush()

    l1_4_2 = Lesson(unit_id=u1_4.id, order=2,
        title_fr="Créer un logo simple avec l'AI",
        title_en="Créer un logo simple avec l'AI", format="tutorial",
        difficulty_level=2, estimated_duration_min=12,
        description_fr="Looka AI tutoriel, Midjourney pour logos conceptuels, Adobe Firefly pour logos vectoriels.",
        prerequisite_lesson_id=l1_4_1.id)
    db.add(l1_4_2); db.flush()
    db.add(Activity(lesson_id=l1_4_2.id, order=1, type="tutorial",
        title_fr="Tutoriel guidé — Créer un logo avec Looka AI",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(lesson_id=l1_4_2.id, order=2, type="exercise",
        title_fr="Exercice — Créez votre premier logo AI",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Créez 3 versions de logo pour une marque tunisienne :\n1. Version avec Looka AI (logo automatique)\n2. Version conceptuelle avec Midjourney\n3. Version finale retravaillée dans Canva AI\nChoisissez la meilleure version et justifiez votre choix.",
            "livrable": "3 versions de logo + choix final justifié.",
            "criteres": {"originalite": "35%", "adaptation_marche_mena": "35%", "qualite_technique": "30%"},
            "score_minimum": 70,
        },
        hints_fr=[
            {"level": 1, "text": "Pour un logo MENA efficace : combinez un symbole universel avec un élément culturel local. Ex : arche arabe stylisée + forme moderne."},
        ]))
    db.flush()

    l1_4_3 = Lesson(unit_id=u1_4.id, order=3,
        title_fr="Créer une palette de couleurs avec Coolors AI",
        title_en="Créer une palette de couleurs avec Coolors AI", format="video",
        difficulty_level=1, estimated_duration_min=8,
        description_fr="Coolors AI, Adobe Color, signification des couleurs dans la culture MENA, palettes harmonieuses.",
        prerequisite_lesson_id=l1_4_2.id)
    db.add(l1_4_3); db.flush()
    db.add(Activity(lesson_id=l1_4_3.id, order=1, type="video",
        title_fr="Vidéo — Créer une palette de couleurs avec Coolors AI",
        is_assessed=False, is_required=True, content_fr={"duration_min": 8}))
    db.add(Activity(lesson_id=l1_4_3.id, order=2, type="exercise",
        title_fr="Exercice — Créez la palette de couleurs de votre marque",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "consigne": "Créez une palette de couleurs cohérente pour votre marque tunisienne :\n1. Utilisez Coolors AI pour générer 3 palettes différentes\n2. Analysez la signification culturelle de chaque couleur dans le contexte MENA\n3. Choisissez votre palette finale (5 couleurs : primaire, secondaire, accent, fond, texte)\n4. Créez un document de palette avec codes HEX et usage de chaque couleur",
            "livrable": "Document palette finale (5 couleurs) avec codes HEX et justification culturelle.",
        }))
    db.flush()

    # ── Unité 5 — Éthique AI basique en design ────────────────────────────────
    u1_5 = Unit(module_id=m1.id, order=5,
        title_fr="Éthique AI basique en design",
        title_en="Basic AI Ethics in Design",
        description_fr="Droits d'auteur, propriété intellectuelle et transparence client en design AI.",
        estimated_duration_min=28)
    db.add(u1_5); db.flush()

    l1_5_1 = Lesson(unit_id=u1_5.id, order=1,
        title_fr="Droits d'auteur et images générées par l'AI",
        title_en="Droits d'auteur et images générées par l'AI", format="video",
        difficulty_level=1, estimated_duration_min=10,
        description_fr="CGU Midjourney/Firefly/DALL-E, droits commerciaux par outil, 5 règles d'or du design AI éthique.")
    db.add(l1_5_1); db.flush()
    db.add(Activity(lesson_id=l1_5_1.id, order=1, type="video",
        title_fr="Vidéo — Droits d'auteur et images AI",
        is_assessed=False, is_required=True, content_fr={"duration_min": 10}))
    db.add(Activity(lesson_id=l1_5_1.id, order=2, type="quiz",
        title_fr="Quiz — Droits d'auteur et design AI",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={"questions": [
            {"id": 1,
             "question": "Vous utilisez Midjourney version gratuite pour créer un logo commercial. C'est :",
             "options": [
                 "A) Parfaitement légal — Midjourney est un outil",
                 "B) Une violation des CGU — la version gratuite interdit l'usage commercial",
                 "C) Légal si vous modifiez l'image à 50%",
                 "D) Légal en Tunisie car les lois sont différentes"
             ],
             "correct": "B",
             "explanation": "La version gratuite de Midjourney interdit explicitement l'usage commercial. Un abonnement Pro ($60/mois) est nécessaire pour les droits commerciaux complets."},
            {"id": 2,
             "question": "Adobe Firefly génère des images avec des droits commerciaux inclus car :",
             "options": [
                 "A) Adobe est une grande entreprise donc c'est automatiquement légal",
                 "B) Adobe Firefly est entraîné uniquement sur des contenus sous licence Adobe, incluant les droits commerciaux",
                 "C) Toutes les images générées par AI sont libres de droits",
                 "D) Adobe offre une assurance légale gratuite"
             ],
             "correct": "B",
             "explanation": "Adobe Firefly a été spécifiquement conçu avec des données d'entraînement sous licence, ce qui garantit les droits commerciaux pour les créations générées."},
        ], "passing_score": 70}))
    db.flush()

    l1_5_2 = Lesson(unit_id=u1_5.id, order=2,
        title_fr="Transparence avec les clients sur l'usage de l'AI",
        title_en="Transparence avec les clients sur l'usage de l'AI", format="case_study",
        difficulty_level=2, estimated_duration_min=30,
        description_fr="2 cas pratiques : designer qui cache l'usage AI vs designer transparent. Charte éthique débutant.",
        prerequisite_lesson_id=l1_5_1.id)
    db.add(l1_5_2); db.flush()
    db.add(Activity(lesson_id=l1_5_2.id, order=1, type="case_study",
        title_fr="Cas pratiques — Transparence et responsabilité en design AI",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "cas": [
                {
                    "titre": "Cas Sami — Le logo 'fait main'",
                    "contexte": "Sami, designer freelance à Tunis, utilise Midjourney pour créer un logo. Il présente le résultat à son client comme 'entièrement créé à la main' et facture le tarif d'un travail manuel.",
                    "questions": [
                        "Quelles erreurs éthiques Sami a-t-il commises ?",
                        "Quels sont les risques légaux et réputationnels pour lui ?",
                        "Comment aurait-il dû présenter son travail AI au client ?",
                    ],
                },
                {
                    "titre": "Cas Nadia — La transparence comme avantage",
                    "contexte": "Nadia est designer à Casablanca. Elle explique à ses clients qu'elle utilise l'AI pour accélérer la phase d'exploration créative, ce qui lui permet de proposer plus d'options dans le même budget.",
                    "questions": [
                        "Comment la transparence de Nadia est-elle un avantage concurrentiel ?",
                        "Quelle formulation recommandez-vous pour présenter l'AI à un client sceptique ?",
                    ],
                },
            ],
            "score_minimum": 70,
        }))
    db.flush()

    # ════════════════════════════════════════════════════════════════════════
    # MODULE 2 — PRATIQUE
    # ════════════════════════════════════════════════════════════════════════

    # ── Unité 1 — Prompting visuel avancé ────────────────────────────────────
    u2_1 = Unit(module_id=m2.id, order=1,
        title_fr="Prompting visuel avancé",
        title_en="Advanced Visual Prompting",
        estimated_duration_min=36)
    db.add(u2_1); db.flush()

    l2_1_1 = Lesson(unit_id=u2_1.id, order=1,
        title_fr="Les techniques avancées de prompting",
        title_en="Les techniques avancées de prompting", format="video",
        difficulty_level=3, estimated_duration_min=12,
        description_fr="Prompts négatifs, pondération, références d'images, chaînage de prompts, styles artistiques.")
    db.add(l2_1_1); db.flush()
    db.add(Activity(lesson_id=l2_1_1.id, order=1, type="video",
        title_fr="Vidéo — Techniques avancées de prompting visuel",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(lesson_id=l2_1_1.id, order=2, type="exercise",
        title_fr="Exercice — Maîtriser les techniques avancées",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Testez 4 techniques avancées de prompting :\n1. Prompt avec référence image (--iw)\n2. Prompt avec négatifs détaillés\n3. Prompt avec pondération de styles (style1::2 style2::1)\n4. Chaînage : utilisez une image générée comme référence pour la suivante\nDocumentez chaque technique avec le prompt + résultat + analyse.",
            "livrable": "4 prompts avancés + images résultats + analyse comparative.",
            "criteres": {"maitrise_techniques": "40%", "qualite_resultats": "35%", "qualite_analyse": "25%"},
            "score_minimum": 70,
        }))
    db.flush()

    l2_1_2 = Lesson(unit_id=u2_1.id, order=2,
        title_fr="Prompting culturel pour le marché MENA",
        title_en="Prompting culturel pour le marché MENA", format="video",
        difficulty_level=3, estimated_duration_min=10,
        description_fr="Vocabulaire visuel arabe, esthétiques géographiques MENA, fêtes et événements, codes couleurs régionaux.",
        prerequisite_lesson_id=l2_1_1.id)
    db.add(l2_1_2); db.flush()
    db.add(Activity(lesson_id=l2_1_2.id, order=1, type="video",
        title_fr="Vidéo — Prompting culturel MENA",
        is_assessed=False, is_required=True, content_fr={"duration_min": 10}))
    db.add(Activity(lesson_id=l2_1_2.id, order=2, type="exercise",
        title_fr="Exercice — Bibliothèque de prompts MENA",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Créez une bibliothèque de 10 prompts culturels MENA réutilisables :\n5 prompts pour campagnes Ramadan (différents tons)\n3 prompts pour identités visuelles MENA modernes\n2 prompts pour interfaces mobiles arabes\nPour chaque prompt : résultat généré + cas d'usage recommandé.",
            "livrable": "Bibliothèque de 10 prompts MENA + images générées.",
            "criteres": {"pertinence_culturelle": "45%", "reutilisabilite": "30%", "qualite_images": "25%"},
            "score_minimum": 70,
        }))
    db.flush()

    l2_1_3 = Lesson(unit_id=u2_1.id, order=3,
        title_fr="Itération et amélioration des résultats",
        title_en="Itération et amélioration des résultats", format="tutorial",
        difficulty_level=3, estimated_duration_min=30,
        description_fr="Workflow d'itération, variation et upscaling, inpainting pour corrections ciblées.",
        prerequisite_lesson_id=l2_1_2.id)
    db.add(l2_1_3); db.flush()
    db.add(Activity(lesson_id=l2_1_3.id, order=1, type="tutorial",
        title_fr="Tutoriel — Workflow d'itération visuelle",
        is_assessed=False, is_required=True, content_fr={"duration_min": 30}))
    db.add(Activity(lesson_id=l2_1_3.id, order=2, type="exercise",
        title_fr="Exercice — Perfectionner une image en 5 itérations",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Partez d'un prompt basique et itérez jusqu'à l'image parfaite :\nItération 1 : prompt de base\nItération 2 : ajout de style\nItération 3 : variation + upscaling\nItération 4 : inpainting pour corriger un élément\nItération 5 : image finale retravaillée dans Canva AI\nDocumentez chaque étape.",
            "livrable": "5 images d'itération + documentation du processus.",
            "criteres": {"progression_qualite": "40%", "maitrise_outils": "35%", "documentation": "25%"},
            "score_minimum": 70,
        }))
    db.flush()

    # ── Unité 2 — Design UI/UX avancé avec AI ────────────────────────────────
    u2_2 = Unit(module_id=m2.id, order=2,
        title_fr="Design UI/UX avancé avec AI",
        title_en="Advanced UI/UX Design with AI",
        estimated_duration_min=38)
    db.add(u2_2); db.flush()

    l2_2_1 = Lesson(unit_id=u2_2.id, order=1,
        title_fr="Créer des interfaces complètes avec Figma AI",
        title_en="Créer des interfaces complètes avec Figma AI", format="tutorial",
        difficulty_level=3, estimated_duration_min=15,
        description_fr="Design system Figma AI, composants auto-générés, prototype interactif, handoff développeur.")
    db.add(l2_2_1); db.flush()
    db.add(Activity(lesson_id=l2_2_1.id, order=1, type="tutorial",
        title_fr="Tutoriel avancé — Figma AI design system",
        is_assessed=False, is_required=True, content_fr={"duration_min": 15}))
    db.add(Activity(lesson_id=l2_2_1.id, order=2, type="exercise",
        title_fr="Exercice — Créer une interface complète avec Figma AI",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Créez une interface d'application mobile complète avec Figma AI :\n1. Générez un design system (couleurs, typographie, composants)\n2. Créez 5 écrans complets (onboarding, accueil, recherche, détail, profil)\n3. Ajoutez les interactions et animations de base\n4. Exportez pour handoff développeur",
            "livrable": "Fichier Figma avec 5 écrans + design system + prototype cliquable.",
            "criteres": {"completude_design_system": "30%", "qualite_ecrans": "35%", "prototype_interactions": "20%", "handoff": "15%"},
            "score_minimum": 70,
        }))
    db.flush()

    l2_2_2 = Lesson(unit_id=u2_2.id, order=2,
        title_fr="Intégrer l'AI dans le processus UX",
        title_en="Intégrer l'AI dans le processus UX", format="video",
        difficulty_level=3, estimated_duration_min=12,
        description_fr="User research avec AI, persona generation, user journey mapping automatisé, A/B testing visuel.",
        prerequisite_lesson_id=l2_2_1.id)
    db.add(l2_2_2); db.flush()
    db.add(Activity(lesson_id=l2_2_2.id, order=1, type="video",
        title_fr="Vidéo — L'AI dans le processus UX",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(lesson_id=l2_2_2.id, order=2, type="exercise",
        title_fr="Exercice — Créer des personas et user journeys avec l'AI",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Utilisez ChatGPT pour créer le profil UX complet d'une app tunisienne :\n1. Générez 3 personas utilisateurs MENA détaillés (âge, métier, comportements digitaux)\n2. Créez le user journey map pour chaque persona\n3. Identifiez les 3 pain points principaux\n4. Proposez des solutions UI/UX concrètes",
            "livrable": "3 personas + 3 user journeys + analyse pain points + solutions UI.",
            "criteres": {"realisme_personas_mena": "35%", "qualite_user_journeys": "35%", "pertinence_solutions": "30%"},
            "score_minimum": 70,
        }))
    db.flush()

    l2_2_3 = Lesson(unit_id=u2_2.id, order=3,
        title_fr="Interface bilingue arabe/français avec AI",
        title_en="Interface bilingue arabe/français avec AI", format="exercise",
        difficulty_level=4, estimated_duration_min=90,
        description_fr="Projet noté — interface complète bilingue RTL/LTR, typographie mixte, navigation adaptée.",
        prerequisite_lesson_id=l2_2_2.id)
    db.add(l2_2_3); db.flush()
    db.add(Activity(lesson_id=l2_2_3.id, order=1, type="exercise",
        title_fr="Projet noté — Interface bilingue arabe/français",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Créez une interface mobile complète bilingue AR/FR pour une startup tunisienne :\n\nPhase 1 — Version française (LTR) : 4 écrans complets avec Figma AI\nPhase 2 — Version arabe (RTL) : adaptation complète des mêmes 4 écrans\nPhase 3 — Switch de langue : bouton de bascule AR/FR intégré à l'interface\nPhase 4 — Test culturel : vérifiez les 5 codes culturels MENA (couleurs, icônes, images, textes, navigation)",
            "livrable": "8 écrans (4 FR + 4 AR) + documentation des adaptations culturelles.",
            "criteres": {
                "qualite_version_fr": "25%",
                "qualite_version_ar_rtl": "35%",
                "coherence_bilingue": "25%",
                "adaptation_culturelle": "15%",
            },
            "score_minimum": 70,
            "duree_estimee": "90 minutes",
        }))
    db.flush()

    # ── Unité 3 — Créer des vidéos avec l'AI ─────────────────────────────────
    u2_3 = Unit(module_id=m2.id, order=3,
        title_fr="Créer des vidéos avec l'AI",
        title_en="Creating Videos with AI",
        estimated_duration_min=38)
    db.add(u2_3); db.flush()

    l2_3_1 = Lesson(unit_id=u2_3.id, order=1,
        title_fr="Introduction à Runway ML",
        title_en="Introduction à Runway ML", format="tutorial",
        difficulty_level=3, estimated_duration_min=12,
        description_fr="Interface Runway ML, Gen-2 text-to-video, image-to-video, motion brush, export.")
    db.add(l2_3_1); db.flush()
    db.add(Activity(lesson_id=l2_3_1.id, order=1, type="tutorial",
        title_fr="Tutoriel guidé — Runway ML pas à pas",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(lesson_id=l2_3_1.id, order=2, type="exercise",
        title_fr="Exercice — Créez votre première vidéo avec Runway ML",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Créez 3 clips vidéo courts (5-10 secondes) avec Runway ML :\n1. Text-to-video : décrivez une scène MENA\n2. Image-to-video : animez une de vos images Midjourney\n3. Motion brush : ajoutez un mouvement ciblé à une image statique\nMontez les 3 clips dans CapCut AI.",
            "livrable": "3 clips courts + montage final 30 secondes.",
            "criteres": {"maitrise_runway": "40%", "qualite_clips": "35%", "montage_capcut": "25%"},
            "score_minimum": 70,
        }))
    db.flush()

    l2_3_2 = Lesson(unit_id=u2_3.id, order=2,
        title_fr="Voix off en arabe et français avec ElevenLabs",
        title_en="Voix off en arabe et français avec ElevenLabs", format="tutorial",
        difficulty_level=3, estimated_duration_min=12,
        description_fr="ElevenLabs interface, voix arabes disponibles, clonage de voix, synchronisation avec vidéo.",
        prerequisite_lesson_id=l2_3_1.id)
    db.add(l2_3_2); db.flush()
    db.add(Activity(lesson_id=l2_3_2.id, order=1, type="tutorial",
        title_fr="Tutoriel guidé — ElevenLabs AR/FR",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(lesson_id=l2_3_2.id, order=2, type="exercise",
        title_fr="Exercice — Créer une voix off bilingue AR/FR",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Créez une voix off professionnelle bilingue :\n1. Rédigez un script de 30 secondes en français et en arabe\n2. Générez la version française avec une voix neutre professionnelle\n3. Générez la version arabe avec une voix adaptée au marché MENA\n4. Synchronisez avec votre vidéo Runway ML dans CapCut AI",
            "livrable": "Script bilingue + 2 fichiers audio + vidéo finale avec voix off.",
            "criteres": {"qualite_script": "25%", "naturalite_voix_off": "35%", "synchronisation": "40%"},
            "score_minimum": 70,
        }))
    db.flush()

    l2_3_3 = Lesson(unit_id=u2_3.id, order=3,
        title_fr="Ma première vidéo publicitaire AI complète",
        title_en="Ma première vidéo publicitaire AI complète", format="exercise",
        difficulty_level=4, estimated_duration_min=90,
        description_fr="Projet intégrateur : vidéo publicitaire 30-60 secondes entièrement produite avec AI.",
        prerequisite_lesson_id=l2_3_2.id)
    db.add(l2_3_3); db.flush()
    db.add(Activity(lesson_id=l2_3_3.id, order=1, type="exercise",
        title_fr="Projet noté — Ma première vidéo publicitaire AI complète",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Créez une vidéo publicitaire complète (30-60 secondes) pour une PME MENA :\n\nPhase 1 — Script ChatGPT : accroche, problème, solution, CTA (FR et AR)\nPhase 2 — Visuels Midjourney + Runway ML : clips animés culturellement adaptés\nPhase 3 — Voix off ElevenLabs : version française + version arabe\nPhase 4 — Montage CapCut AI : assemblage, sous-titres, musique libre de droits\nPhase 5 — Export : 3 formats (Stories 9:16, Feed 1:1, YouTube 16:9)",
            "livrable": "Vidéo finale (3 formats) + script bilingue + note de réalisation.",
            "criteres": {
                "qualite_script_storyboard": "20%",
                "qualite_visuels": "30%",
                "qualite_voix_off": "20%",
                "montage_final": "20%",
                "adaptation_formats": "10%",
            },
            "score_minimum": 70,
        }))
    db.flush()

    # ── Unité 4 — Système de brand assets complet ─────────────────────────────
    u2_4 = Unit(module_id=m2.id, order=4,
        title_fr="Système de brand assets complet",
        title_en="Complete Brand Assets System",
        estimated_duration_min=38)
    db.add(u2_4); db.flush()

    l2_4_1 = Lesson(unit_id=u2_4.id, order=1,
        title_fr="Créer une identité visuelle complète",
        title_en="Créer une identité visuelle complète", format="video",
        difficulty_level=3, estimated_duration_min=12,
        description_fr="Processus complet : brief → exploration → logo → palette → typographie → guidelines MENA.")
    db.add(l2_4_1); db.flush()
    db.add(Activity(lesson_id=l2_4_1.id, order=1, type="video",
        title_fr="Vidéo — Créer une identité visuelle complète avec l'AI",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(lesson_id=l2_4_1.id, order=2, type="exercise",
        title_fr="Projet — Identité visuelle complète pour une marque MENA",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Créez l'identité visuelle complète d'une marque tunisienne :\n1. Brief créatif (secteur, valeurs, cible, tone of voice)\n2. Logo principal + déclinaisons (couleur, noir, blanc, arabe)\n3. Palette de couleurs (5 couleurs + codes HEX)\n4. Typographies (principale + secondaire, en latin et arabe)\n5. Mini brand guidelines (1 page A4)",
            "livrable": "Dossier brand complet : logo + palette + typo + guidelines.",
            "criteres": {"coherence_identite": "35%", "adaptation_mena": "30%", "completude": "20%", "qualite_guidelines": "15%"},
            "score_minimum": 70,
        }))
    db.flush()

    l2_4_2 = Lesson(unit_id=u2_4.id, order=2,
        title_fr="Templates réseaux sociaux avec AI",
        title_en="Templates réseaux sociaux avec AI", format="tutorial",
        difficulty_level=3, estimated_duration_min=12,
        description_fr="Adobe Express AI, Canva AI templates brandés, kit de 10 templates cohérents pour réseaux sociaux.",
        prerequisite_lesson_id=l2_4_1.id)
    db.add(l2_4_2); db.flush()
    db.add(Activity(lesson_id=l2_4_2.id, order=1, type="tutorial",
        title_fr="Tutoriel — Templates réseaux sociaux brandés",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(lesson_id=l2_4_2.id, order=2, type="exercise",
        title_fr="Exercice — Kit de 10 templates réseaux sociaux",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Créez un kit de 10 templates cohérents pour votre marque :\n2 templates post Instagram (promotionnel + éducatif)\n2 templates Stories (annonce + citation)\n2 templates Facebook (événement + article)\n2 templates LinkedIn (article + statistique)\n2 templates email (bannière FR + bannière AR)",
            "livrable": "Kit 10 templates exportés (PNG/PDF) + fichiers sources Canva.",
            "criteres": {"coherence_brand": "40%", "qualite_design": "35%", "variete_formats": "25%"},
            "score_minimum": 70,
        }))
    db.flush()

    l2_4_3 = Lesson(unit_id=u2_4.id, order=3,
        title_fr="Guide d'utilisation de la marque",
        title_en="Guide d'utilisation de la marque", format="exercise",
        difficulty_level=4, estimated_duration_min=60,
        description_fr="Projet noté — Brand book complet avec règles d'usage, do's and don'ts, exemples MENA.",
        prerequisite_lesson_id=l2_4_2.id)
    db.add(l2_4_3); db.flush()
    db.add(Activity(lesson_id=l2_4_3.id, order=1, type="exercise",
        title_fr="Projet noté — Brand book complet",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Rédigez le brand book complet de votre marque tunisienne (10-15 pages) :\n1. Présentation de la marque et ses valeurs\n2. Logo : versions, espaces de protection, usages interdits\n3. Palette de couleurs avec codes HEX, RGB, CMJN\n4. Typographies en latin ET arabe avec règles d'usage\n5. Iconographie et style photographique\n6. Exemples d'applications : print, digital, MENA spécifique\n7. Do's and Don'ts visuels",
            "livrable": "Brand book PDF 10-15 pages.",
            "criteres": {"completude": "25%", "qualite_exemples": "30%", "adaptation_mena": "25%", "presentabilite": "20%"},
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
        title_fr="Droits commerciaux des images AI",
        title_en="Droits commerciaux des images AI", format="video",
        difficulty_level=3, estimated_duration_min=12,
        description_fr="Tableau comparatif droits commerciaux par outil, contrats clients, mentions légales, protection MENA.")
    db.add(l2_5_1); db.flush()
    db.add(Activity(lesson_id=l2_5_1.id, order=1, type="video",
        title_fr="Vidéo — Droits commerciaux des images AI",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(lesson_id=l2_5_1.id, order=2, type="quiz",
        title_fr="Quiz — Droits commerciaux design AI",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={"questions": [
            {"id": 1,
             "question": "Votre client veut utiliser une image générée avec Midjourney Pro sur ses emballages produits vendus en Tunisie et au Maroc. Est-ce légalement possible ?",
             "options": [
                 "A) Non — les images Midjourney ne peuvent jamais être utilisées sur des produits physiques",
                 "B) Oui — l'abonnement Midjourney Pro inclut les droits commerciaux pour tous usages",
                 "C) Seulement si vous ajoutez la mention 'Généré par Midjourney'",
                 "D) Seulement pour les produits vendus en ligne"
             ],
             "correct": "B",
             "explanation": "L'abonnement Midjourney Pro inclut les droits commerciaux complets, y compris pour les supports physiques comme les emballages produits."},
            {"id": 2,
             "question": "Vous créez un logo avec Adobe Firefly pour un client. Ce logo ressemble à celui d'une marque internationale. Que faites-vous ?",
             "options": [
                 "A) Livrez quand même — Adobe Firefly inclut une protection légale",
                 "B) Régénérez avec un prompt différent et vérifiez l'originalité avant livraison",
                 "C) Modifiez la couleur et livrez",
                 "D) Demandez au client de prendre la responsabilité légale"
             ],
             "correct": "B",
             "explanation": "Même avec Adobe Firefly, la ressemblance avec une marque existante peut exposer à des poursuites. Toujours vérifier l'originalité et régénérer si nécessaire."},
        ], "passing_score": 70}))
    db.flush()

    l2_5_2 = Lesson(unit_id=u2_5.id, order=2,
        title_fr="Propriété intellectuelle et design AI",
        title_en="Propriété intellectuelle et design AI", format="case_study",
        difficulty_level=3, estimated_duration_min=30,
        description_fr="3 cas MENA : contrefaçon involontaire, deepfake visuel, appropriation culturelle en design AI.",
        prerequisite_lesson_id=l2_5_1.id)
    db.add(l2_5_2); db.flush()
    db.add(Activity(lesson_id=l2_5_2.id, order=1, type="case_study",
        title_fr="Cas pratiques — Propriété intellectuelle design AI MENA",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "cas": [
                {
                    "titre": "CAS 1 — La contrefaçon involontaire",
                    "scenario": "Youssef génère un logo pour une startup marocaine avec Midjourney. Le résultat ressemble fortement au logo d'une grande marque internationale sans qu'il s'en rende compte. La startup commence à utiliser ce logo sur tous ses supports.",
                    "questions": ["Quelles sont les responsabilités légales de Youssef et de la startup ?", "Comment prévenir ce type de situation ?", "Que faire maintenant que le logo est déjà en circulation ?"],
                },
                {
                    "titre": "CAS 2 — L'appropriation culturelle",
                    "scenario": "Une agence de design à Tunis utilise l'AI pour créer des visuels 'inspirés de la culture berbère' pour un client étranger, sans consulter de spécialiste culturel.",
                    "questions": ["Pourquoi cette pratique peut être problématique ?", "Comment utiliser l'AI de façon respectueuse pour créer des visuels culturels MENA ?"],
                },
            ],
            "charte": "Rédigez en 8 lignes votre 'Charte de design AI éthique' pour votre pratique professionnelle.",
        }))
    db.flush()

    # ════════════════════════════════════════════════════════════════════════
    # MODULE 3 — EXPERT
    # ════════════════════════════════════════════════════════════════════════

    # ── Unité 1 — Stratégie design AI globale ────────────────────────────────
    u3_1 = Unit(module_id=m3.id, order=1,
        title_fr="Stratégie design AI globale",
        title_en="Global AI Design Strategy",
        estimated_duration_min=42)
    db.add(u3_1); db.flush()

    l3_1_1 = Lesson(unit_id=u3_1.id, order=1,
        title_fr="Construire son workflow design AI complet",
        title_en="Construire son workflow design AI complet", format="video",
        difficulty_level=4, estimated_duration_min=15,
        description_fr="Workflow de production AI, intégration dans les projets clients, gestion des révisions, productivité × 5.")
    db.add(l3_1_1); db.flush()
    db.add(Activity(lesson_id=l3_1_1.id, order=1, type="video",
        title_fr="Vidéo — Construire son workflow design AI complet",
        is_assessed=False, is_required=True, content_fr={"duration_min": 15}))
    db.add(Activity(lesson_id=l3_1_1.id, order=2, type="exercise",
        title_fr="Exercice stratégique — Mon workflow design AI",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Concevez votre workflow design AI complet :\n1. Cartographiez vos 15 tâches design actuelles\n2. Classez-les : AI seul / AI+Humain / Humain seul\n3. Pour chaque tâche AI : quel outil, quelle durée estimée, quel gain de temps\n4. Calculez votre gain de productivité mensuel en heures et en revenus\n5. Créez un document de processus que vous pourriez partager à un client",
            "livrable": "Cartographie workflow + calcul productivité + document de processus.",
            "criteres": {"pertinence_classification": "30%", "calcul_productivite": "30%", "qualite_document": "40%"},
            "score_minimum": 70,
        }))
    db.flush()

    l3_1_2 = Lesson(unit_id=u3_1.id, order=2,
        title_fr="Intégrer l'AI dans tous les projets créatifs",
        title_en="Intégrer l'AI dans tous les projets créatifs", format="video",
        difficulty_level=4, estimated_duration_min=12,
        description_fr="Phases créatives et points d'injection AI, brief client AI-ready, livrables augmentés.",
        prerequisite_lesson_id=l3_1_1.id)
    db.add(l3_1_2); db.flush()
    db.add(Activity(lesson_id=l3_1_2.id, order=1, type="video",
        title_fr="Vidéo — Intégrer l'AI dans tous les projets créatifs",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(lesson_id=l3_1_2.id, order=2, type="case_study",
        title_fr="Cas pratique — Transformer un projet traditionnel en projet AI",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "contexte": "Une agence de design à Tunis reçoit une commande : refonte complète de l'identité visuelle d'une chaîne de restaurants tunisiens (logo, menu, signalétique, digital). Budget : 8 000 TND, délai : 3 semaines.",
            "questions": [
                {"id": 1, "question": "Comment intégreriez-vous l'AI dans chaque phase du projet (brief, exploration, création, révision, livraison) ?"},
                {"id": 2, "question": "Quels outils AI utiliseriez-vous pour chaque livrable ? Justifiez vos choix."},
                {"id": 3, "question": "Comment présenteriez-vous l'utilisation de l'AI au client pour maximiser sa confiance ?"},
            ],
        }))
    db.flush()

    l3_1_3 = Lesson(unit_id=u3_1.id, order=3,
        title_fr="Présenter sa stratégie AI aux clients",
        title_en="Présenter sa stratégie AI aux clients", format="exercise",
        difficulty_level=5, estimated_duration_min=90,
        description_fr="Pitch stratégique 10 slides, réponses aux objections clients, démonstration live de valeur ajoutée.",
        prerequisite_lesson_id=l3_1_2.id)
    db.add(l3_1_3); db.flush()
    db.add(Activity(lesson_id=l3_1_3.id, order=1, type="exercise",
        title_fr="Projet — Présentation stratégie design AI à un client",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Préparez une présentation de 10 slides pour convaincre un client d'adopter une approche design AI :\n1. Le design AI aujourd'hui — révolution créative\n2. Notre processus augmenté par l'AI\n3. Ce que ça change pour votre projet\n4. Exemples de réalisations AI (vos meilleurs travaux)\n5. Gain de temps et qualité\n6. Transparence sur les outils utilisés\n7. Droits et propriété intellectuelle\n8. Budget et délais optimisés\n9. Références clients MENA\n10. Prochaines étapes\n\nRéponses aux 3 objections : 'L'AI c'est froid et sans âme', 'Tout le monde peut faire pareil', 'C'est moins cher donc moins bien'",
            "livrable": "Présentation 10 slides + réponses aux 3 objections.",
            "criteres": {"structure_narrative": "25%", "qualite_exemples": "30%", "transparence_ethique": "20%", "reponses_objections": "25%"},
            "score_minimum": 70,
            "feedback": "mentor",
        }))
    db.flush()

    # ── Unité 2 — Piloter une équipe design AI ────────────────────────────────
    u3_2 = Unit(module_id=m3.id, order=2,
        title_fr="Piloter une équipe design AI",
        title_en="Leading an AI Design Team",
        estimated_duration_min=36)
    db.add(u3_2); db.flush()

    l3_2_1 = Lesson(unit_id=u3_2.id, order=1,
        title_fr="Former son équipe aux outils AI design",
        title_en="Former son équipe aux outils AI design", format="video",
        difficulty_level=4, estimated_duration_min=12,
        description_fr="Programme formation 4 semaines par profil (graphiste, UI/UX, motion), indicateurs d'adoption.")
    db.add(l3_2_1); db.flush()
    db.add(Activity(lesson_id=l3_2_1.id, order=1, type="video",
        title_fr="Vidéo — Former son équipe design aux outils AI",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(lesson_id=l3_2_1.id, order=2, type="exercise",
        title_fr="Exercice — Programme de formation AI design pour mon équipe",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Concevez un programme de formation AI design pour une équipe de 3 profils (graphiste, UI/UX designer, motion designer) :\n\nPour chaque profil :\n- Outils AI prioritaires à maîtriser\n- Programme 4 semaines (objectifs, exercices, validation)\n- Indicateurs d'adoption\n\nKit formateur : email d'invitation motivant + grille d'évaluation avant/après",
            "livrable": "Programme 4 semaines × 3 profils + kit formateur.",
            "criteres": {"adaptation_profils": "40%", "realisme_programme": "35%", "qualite_kit": "25%"},
            "score_minimum": 70,
        }))
    db.flush()

    l3_2_2 = Lesson(unit_id=u3_2.id, order=2,
        title_fr="Orchestrer créativité humaine et AI",
        title_en="Orchestrer créativité humaine et AI", format="video",
        difficulty_level=4, estimated_duration_min=10,
        description_fr="Direction artistique augmentée, rôle du DA dans l'ère AI, ce que l'AI ne remplacera jamais.",
        prerequisite_lesson_id=l3_2_1.id)
    db.add(l3_2_2); db.flush()
    db.add(Activity(lesson_id=l3_2_2.id, order=1, type="video",
        title_fr="Vidéo — Orchestrer créativité humaine et AI",
        is_assessed=False, is_required=True, content_fr={"duration_min": 10}))
    db.add(Activity(lesson_id=l3_2_2.id, order=2, type="exercise",
        title_fr="Exercice — Workflow créatif humain + AI optimal",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Concevez le modèle de collaboration optimal créativité humaine + AI :\n1. Matrice 20 tâches design (4 quadrants : AI seul / AI+DA / DA seul / À supprimer)\n2. Redéfinir le rôle du Directeur Artistique dans l'ère AI\n3. Ce que l'AI ne remplacera jamais en design (liste + justification)\n4. Workflow quotidien idéal d'un designer AI",
            "livrable": "Matrice quadrants + redéfinition rôle DA + workflow quotidien.",
            "criteres": {"pertinence_matrice": "35%", "vision_role_da": "35%", "praticite_workflow": "30%"},
            "score_minimum": 70,
        }))
    db.flush()

    l3_2_3 = Lesson(unit_id=u3_2.id, order=3,
        title_fr="Maintenir l'authenticité de la marque avec l'AI",
        title_en="Maintaining brand authenticity with AI — Real Tunisian agency case",
        format="case_study", difficulty_level=5, estimated_duration_min=45,
        description_fr="Cas agence tunisienne : crise d'identité visuelle après adoption massive AI, Brand Vision Guide.",
        prerequisite_lesson_id=l3_2_2.id)
    db.add(l3_2_3); db.flush()
    db.add(Activity(lesson_id=l3_2_3.id, order=1, type="case_study",
        title_fr="Cas agence design — Authenticité visuelle avec l'AI",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "contexte": "VisualCraft est une agence design tunisienne réputée pour son style distinctif inspiré du patrimoine arabe moderne. Après avoir adopté massivement l'AI, ses clients se plaignent : 'Vos créations ont perdu leur âme tunisienne. On dirait du stock photo générique.'",
            "questions": [
                {"id": 1, "question": "Comment l'AI a-t-elle dilué l'identité distinctive de VisualCraft ? Analysez les causes profondes."},
                {"id": 2, "question": "Créez un 'Brand Vision Prompt Guide' pour VisualCraft : comment briefer Midjourney et Adobe Firefly pour qu'ils produisent le style distinctif de l'agence ?"},
                {"id": 3, "question": "Proposez un processus de création AI qui garantit l'authenticité visuelle et l'ADN créatif de l'agence."},
            ],
        }))
    db.flush()

    # ── Unité 3 — Design AI avancé MENA ──────────────────────────────────────
    u3_3 = Unit(module_id=m3.id, order=3,
        title_fr="Design AI avancé Afrique du Nord",
        title_en="Advanced AI Design North Africa",
        estimated_duration_min=40)
    db.add(u3_3); db.flush()

    l3_3_1 = Lesson(unit_id=u3_3.id, order=1,
        title_fr="Calligraphie arabe et design moderne",
        title_en="Calligraphie arabe et design moderne", format="video",
        difficulty_level=4, estimated_duration_min=15,
        description_fr="Histoire de la calligraphie arabe, outils AI pour la calligraphie, fusion moderne-traditionnel, cas identités visuelles premium MENA.")
    db.add(l3_3_1); db.flush()
    db.add(Activity(lesson_id=l3_3_1.id, order=1, type="video",
        title_fr="Vidéo — Calligraphie arabe et design moderne avec l'AI",
        is_assessed=False, is_required=True, content_fr={"duration_min": 15}))
    db.add(Activity(lesson_id=l3_3_1.id, order=2, type="exercise",
        title_fr="Projet — Identité visuelle calligraphie arabe + design moderne",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Créez une identité visuelle premium qui fusionne calligraphie arabe et design moderne :\n1. Explorez 5 styles calligraphiques arabes avec Midjourney et Adobe Firefly\n2. Créez un logo fusionnant calligraphie arabe + design contemporain\n3. Développez une typographie bilingue cohérente (arabe + latin)\n4. Appliquez sur 3 supports : carte de visite, en-tête, digital\n5. Note sur les choix culturels et esthétiques",
            "livrable": "Identité complète (logo + typo + 3 supports) + note artistique.",
            "criteres": {"fusion_calligraphie_moderne": "35%", "coherence_bilingue": "30%", "qualite_applications": "20%", "note_artistique": "15%"},
            "score_minimum": 70,
        }))
    db.flush()

    l3_3_2 = Lesson(unit_id=u3_3.id, order=2,
        title_fr="Identités visuelles bilingues avec l'AI",
        title_en="Identités visuelles bilingues avec l'AI", format="video",
        difficulty_level=4, estimated_duration_min=12,
        description_fr="Systèmes visuels bilingues AR/FR, cohérence cross-culturelle, typographies mixtes, exemples marques MENA leaders.",
        prerequisite_lesson_id=l3_3_1.id)
    db.add(l3_3_2); db.flush()
    db.add(Activity(lesson_id=l3_3_2.id, order=1, type="video",
        title_fr="Vidéo — Identités visuelles bilingues avec l'AI",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(lesson_id=l3_3_2.id, order=2, type="exercise",
        title_fr="Projet — Système visuel bilingue complet AR/FR",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Créez un système visuel bilingue complet pour une marque MENA :\n1. Logo en version arabe + version française + version mixte\n2. Adaptation de tous les supports en AR et FR\n3. Règles de coexistence des deux systèmes typographiques\n4. Guide d'usage : quand utiliser quelle version",
            "livrable": "Système visuel bilingue complet + guide d'usage.",
            "criteres": {"coherence_bilingue": "40%", "qualite_adaptations": "35%", "guide_usage": "25%"},
            "score_minimum": 70,
        }))
    db.flush()

    l3_3_3 = Lesson(unit_id=u3_3.id, order=3,
        title_fr="Tendances du design AI en MENA",
        title_en="Tendances du design AI en MENA", format="video",
        difficulty_level=4, estimated_duration_min=12,
        description_fr="Tendances 2025-2027, nouveaux outils émergents, opportunités de niche MENA, avenir du métier de designer.",
        prerequisite_lesson_id=l3_3_2.id)
    db.add(l3_3_3); db.flush()
    db.add(Activity(lesson_id=l3_3_3.id, order=1, type="video",
        title_fr="Vidéo — Tendances du design AI en MENA",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(lesson_id=l3_3_3.id, order=2, type="forum_discussion",
        title_fr="Forum — Ma vision du design AI en MENA en 2028",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "question": "3 dimensions :\n1) Quelle compétence design sera la plus précieuse en 2028 que l'AI ne peut pas remplacer ?\n2) Quelle opportunité unique le marché MENA offre-t-il aux designers AI locaux ?\n3) Comment la calligraphie arabe et l'esthétique MENA peuvent-elles devenir un avantage concurrentiel mondial ?",
            "consigne": "Minimum 15 lignes. Commentez 2 autres apprenants de façon constructive.",
        }))
    db.flush()

    # ── Unité 4 — Mesurer le ROI du design AI ────────────────────────────────
    u3_4 = Unit(module_id=m3.id, order=4,
        title_fr="Mesurer le ROI du design AI",
        title_en="Measuring AI Design ROI",
        estimated_duration_min=36)
    db.add(u3_4); db.flush()

    l3_4_1 = Lesson(unit_id=u3_4.id, order=1,
        title_fr="Calculer la valeur créée par l'AI",
        title_en="Calculer la valeur créée par l'AI", format="video",
        difficulty_level=4, estimated_duration_min=12,
        description_fr="Méthode calcul ROI design AI, gain temps × valeur heure, volume projets augmenté, cas chiffres réels MENA.")
    db.add(l3_4_1); db.flush()
    db.add(Activity(lesson_id=l3_4_1.id, order=1, type="video",
        title_fr="Vidéo — Calculer la valeur créée par l'AI design",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(lesson_id=l3_4_1.id, order=2, type="exercise",
        title_fr="Exercice — Calculer mon ROI design AI personnel",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Calculez votre ROI design AI sur 3 mois :\n\nDonnées avant AI :\n- Temps moyen par logo : 8h → Après AI : 3h\n- Projets/mois : 4 → Après AI : 10\n- Prix unitaire logo : 800 TND\n- Coût outils AI : 150 TND/mois\n\nCalculez : gain de temps, revenus additionnels, ROI, projection 12 mois.\nRédigez un pitch de 5 lignes pour présenter ce ROI à un client potentiel.",
            "livrable": "Tableau calcul ROI + projection 12 mois + pitch client.",
            "criteres": {"exactitude_calculs": "40%", "pertinence_projection": "35%", "qualite_pitch": "25%"},
            "score_minimum": 70,
        }))
    db.flush()

    l3_4_2 = Lesson(unit_id=u3_4.id, order=2,
        title_fr="Présenter les résultats à ses clients",
        title_en="Présenter les résultats à ses clients", format="exercise",
        difficulty_level=5, estimated_duration_min=60,
        description_fr="Rapport de valeur créative AI pour client, before/after visuel, métriques d'impact business.",
        prerequisite_lesson_id=l3_4_1.id)
    db.add(l3_4_2); db.flush()
    db.add(Activity(lesson_id=l3_4_2.id, order=1, type="exercise",
        title_fr="Projet — Rapport de valeur design AI pour client",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Créez un rapport de valeur design AI pour un client fictif :\n1. Résumé exécutif (1 page) : livrables, délais, valeur créée\n2. Before/After visuel : comparaison approche traditionnelle vs AI\n3. Métriques d'impact : temps économisé, options supplémentaires proposées, cohérence obtenue\n4. Recommandations pour les prochains projets\n5. Présentation 5 slides pour le client",
            "livrable": "Rapport 3-4 pages + présentation 5 slides.",
            "criteres": {"qualite_rapport": "30%", "before_after_visuel": "30%", "pertinence_metriques": "25%", "presentation": "15%"},
            "score_minimum": 70,
            "feedback": "mentor",
        }))
    db.flush()

    l3_4_3 = Lesson(unit_id=u3_4.id, order=3,
        title_fr="Optimiser son workflow AI continuellement",
        title_en="Optimiser son workflow AI continuellement", format="exercise",
        difficulty_level=5, estimated_duration_min=45,
        description_fr="Veille outils AI, processus d'adoption de nouveaux outils, communauté de pratique design AI MENA.",
        prerequisite_lesson_id=l3_4_2.id)
    db.add(l3_4_3); db.flush()
    db.add(Activity(lesson_id=l3_4_3.id, order=1, type="exercise",
        title_fr="Exercice stratégique — Plan d'optimisation continue",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Créez votre plan d'optimisation continue du workflow design AI :\n1. Système de veille : 5 sources pour suivre les nouveaux outils AI design\n2. Processus d'évaluation d'un nouvel outil (critères, test, décision)\n3. Plan de montée en compétences : 1 nouvel outil/mois sur 6 mois\n4. Comment partager votre expertise avec la communauté design MENA",
            "livrable": "Plan veille + processus évaluation + roadmap compétences 6 mois.",
            "criteres": {"realisme_veille": "25%", "rigueur_processus": "35%", "ambition_roadmap": "25%", "partage_communaute": "15%"},
            "score_minimum": 70,
        }))
    db.flush()

    # ── Unité 5 — Gouvernance et Éthique AI Expert ────────────────────────────
    u3_5 = Unit(module_id=m3.id, order=5,
        title_fr="Gouvernance et Éthique AI — Niveau Expert",
        title_en="AI Governance and Ethics — Expert Level",
        estimated_duration_min=28)
    db.add(u3_5); db.flush()

    l3_5_1 = Lesson(unit_id=u3_5.id, order=1,
        title_fr="Créer sa politique design AI",
        title_en="Créer sa politique design AI", format="video",
        difficulty_level=5, estimated_duration_min=12,
        description_fr="8 sections politique design AI : usages, interdits, transparence, droits, processus validation, mise à jour.")
    db.add(l3_5_1); db.flush()
    db.add(Activity(lesson_id=l3_5_1.id, order=1, type="video",
        title_fr="Vidéo — Créer sa politique design AI",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12}))
    db.add(Activity(lesson_id=l3_5_1.id, order=2, type="exercise",
        title_fr="Projet — Rédiger la politique design AI de mon agence",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Rédigez la politique design AI officielle de votre agence (4-6 pages) :\n1. Préambule — valeurs créatives et engagement éthique\n2. Outils AI autorisés (liste avec conditions)\n3. Usages interdits (6 min : deepfakes, contrefaçon, appropriation culturelle, faux portfolios...)\n4. Transparence clients — comment informer de l'usage AI\n5. Droits d'auteur et propriété intellectuelle\n6. Processus de validation avant livraison client\n7. Formation continue de l'équipe\n8. Mise à jour semestrielle",
            "livrable": "Politique design AI officielle 4-6 pages.",
            "criteres": {"completude_8_sections": "25%", "pertinence_interdictions": "30%", "transparence_client": "25%", "operationnalite": "20%"},
            "score_minimum": 70,
        }))
    db.flush()

    l3_5_2 = Lesson(unit_id=u3_5.id, order=2,
        title_fr="Gérer les crises éthiques créatives AI",
        title_en="Gérer les crises éthiques créatives AI", format="case_study",
        difficulty_level=5, estimated_duration_min=50,
        description_fr="2 simulations de crise : plagiat AI découvert par un client et deepfake visuel détourné.",
        prerequisite_lesson_id=l3_5_1.id)
    db.add(l3_5_2); db.flush()
    db.add(Activity(lesson_id=l3_5_2.id, order=1, type="case_study",
        title_fr="Simulation de crise — 2 scénarios de crise éthique design AI",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "scenarios": [
                {
                    "id": 1,
                    "titre": "CRISE 1 — Le plagiat involontaire découvert",
                    "scenario": "Votre agence livre une identité visuelle créée avec AI à un client marocain. 2 semaines après, le client découvre que le logo ressemble fortement à celui d'une marque émirati. Il menace de vous poursuivre en justice et publie sur LinkedIn.",
                    "questions": [
                        {"q": "5 actions immédiates dans les 24 heures.", "consigne": "Liste priorisée."},
                        {"q": "Message de réponse au post LinkedIn.", "consigne": "Professionnel, empathique, 150 mots max."},
                        {"q": "3 mesures pour améliorer votre processus de validation.", "consigne": "Concrètes et immédiates."},
                    ],
                },
                {
                    "id": 2,
                    "titre": "CRISE 2 — Le deepfake détourné",
                    "scenario": "Des images générées par AI que vous avez créées pour un client tunisien sont détournées et utilisées dans une campagne de désinformation. Les images circulent massivement sur les réseaux sociaux.",
                    "questions": [
                        {"q": "Plan d'action heure par heure sur les 6 premières heures.", "consigne": "Chronologique et précis."},
                        {"q": "Déclaration officielle de votre agence.", "consigne": "Claire, responsable, en français et arabe."},
                        {"q": "5 mesures préventives à mettre en place immédiatement.", "consigne": "Techniques et organisationnelles."},
                    ],
                },
            ],
            "plan_prevention": "Plan de prévention des crises éthiques design AI : 5 mesures concrètes à mettre en place dès demain.",
        }))
    db.flush()


    # ════════════════════════════════════════════════════════════════════════
    # UNITÉ 6 — CERTIFICATION FINALE ✅
    # ════════════════════════════════════════════════════════════════════════

    u3_cert = Unit(
        module_id=m3.id, order=6,
        title_fr="Certification Finale — AI Designer",
        title_en="Final Certification — AI Designer",
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
        title_fr="Test final de certification — AI Designer",
        title_en="Final certification test — AI Designer",
        is_assessed=True, is_required=True, passing_score=80,
        content_fr={
            "instructions": "Ce test couvre les 3 modules. 30 minutes. Score minimum : 16/20 (80%).",
            "questions": [
                # ── Module 1 — Fondations ──
                {"id": 1,
                 "question": "Quel est le principal avantage du design AI pour un graphiste indépendant tunisien ?",
                 "options": ["A) L'AI remplace toutes les compétences créatives", "B) L'AI permet de produire des visuels professionnels plus rapidement et à moindre coût", "C) L'AI garantit l'originalité automatique", "D) L'AI élimine le besoin des outils traditionnels"],
                 "correct": "B", "explanation": "Le design AI amplifie la productivité sans remplacer la créativité humaine.", "module": 1},
                {"id": 2,
                 "question": "Pour créer des wireframes d'application mobile rapidement avec l'AI, quel outil choisissez-vous ?",
                 "options": ["A) Canva AI", "B) Midjourney", "C) Figma AI ou Uizard AI", "D) ElevenLabs"],
                 "correct": "C", "explanation": "Figma AI et Uizard AI sont spécialisés dans la création de wireframes UI/UX.", "module": 1},
                {"id": 3,
                 "question": "Vous utilisez Midjourney version gratuite pour créer un logo commercial. C'est :",
                 "options": ["A) Parfaitement légal", "B) Une violation des CGU — la version gratuite interdit l'usage commercial", "C) Légal si modifié à 50%", "D) Légal en Tunisie"],
                 "correct": "B", "explanation": "La version gratuite de Midjourney interdit explicitement l'usage commercial.", "module": 1},
                {"id": 4,
                 "question": "Vous designez une app en arabe pour le marché tunisien. Quelle est la première adaptation à faire ?",
                 "options": ["A) Changer uniquement les couleurs", "B) Inverser la direction de lecture : passer en RTL", "C) Utiliser une police latine avec caractères arabes", "D) Aucune adaptation"],
                 "correct": "B", "explanation": "La direction RTL est fondamentale pour les interfaces arabes.", "module": 1},
                {"id": 5,
                 "question": "Pourquoi Adobe Firefly inclut les droits commerciaux ?",
                 "options": ["A) Adobe est une grande entreprise", "B) Entraîné uniquement sur des contenus sous licence Adobe", "C) Toutes les images AI sont libres de droits", "D) Adobe offre une assurance légale"],
                 "correct": "B", "explanation": "Adobe Firefly a été entraîné sur des données sous licence, garantissant les droits commerciaux.", "module": 1},
                # ── Module 2 — Pratique ──
                {"id": 6,
                 "question": "Quel paramètre Midjourney permet d'utiliser une image comme référence de style ?",
                 "options": ["A) --ar", "B) --iw", "C) --v", "D) --no"],
                 "correct": "B", "explanation": "--iw (image weight) contrôle l'influence d'une image de référence dans la génération.", "module": 2},
                {"id": 7,
                 "question": "Votre client veut utiliser une image Midjourney Pro sur ses emballages au Maroc et Tunisie. C'est :",
                 "options": ["A) Impossible — Midjourney interdit les produits physiques", "B) Légal — l'abonnement Pro inclut tous les droits commerciaux", "C) Légal seulement en ligne", "D) Uniquement avec mention 'Généré par Midjourney'"],
                 "correct": "B", "explanation": "L'abonnement Midjourney Pro inclut les droits commerciaux complets y compris supports physiques.", "module": 2},
                {"id": 8,
                 "question": "Vous créez une interface bilingue AR/FR. Quelle adaptation est obligatoire pour la version arabe ?",
                 "options": ["A) Changer les couleurs", "B) Passer en RTL + adapter typographies + inverser icônes directionnelles", "C) Uniquement traduire les textes", "D) Aucune adaptation visuelle nécessaire"],
                 "correct": "B", "explanation": "Une interface RTL nécessite l'inversion complète : direction, typographies arabes, icônes directionnelles.", "module": 2},
                {"id": 9,
                 "question": "Quel outil génère des voix off réalistes en arabe pour vos vidéos ?",
                 "options": ["A) Runway ML", "B) ElevenLabs", "C) Canva AI", "D) Figma AI"],
                 "correct": "B", "explanation": "ElevenLabs génère des voix off très réalistes en arabe et en français.", "module": 2},
                {"id": 10,
                 "question": "L'esthétique visuelle MENA génère une image avec des personnages aux traits occidentaux. Que faites-vous ?",
                 "options": ["A) Acceptez l'image", "B) Ajoutez 'North African aesthetic, Arabic style' dans le prompt et régénérez", "C) Abandonnez Midjourney", "D) Envoyez au client sans vérification"],
                 "correct": "B", "explanation": "Affiner le prompt avec des références culturelles précises est la compétence clé du designer MENA.", "module": 2},
                # ── Module 3 — Expert ──
                {"id": 11,
                 "question": "Quel est l'ordre correct pour calculer le ROI design AI ?",
                 "options": ["A) (Revenus AI - Coût outils) / Coût outils × 100", "B) Revenus AI / Coût outils", "C) Gain temps × tarif horaire uniquement", "D) Nombre de projets × prix unitaire"],
                 "correct": "A", "explanation": "ROI = (Bénéfices - Coût outils) / Coût outils × 100. Inclure gain temps ET revenus additionnels.", "module": 3},
                {"id": 12,
                 "question": "Un designer passe de 4 logos/mois à 10 logos/mois grâce à l'AI, à 800 TND/logo. Gain mensuel ?",
                 "options": ["A) 3 200 TND", "B) 4 800 TND", "C) 8 000 TND", "D) 6 400 TND"],
                 "correct": "B", "explanation": "(10-4) × 800 TND = 4 800 TND de revenus additionnels par mois.", "module": 3},
                {"id": 13,
                 "question": "Comment prévenir qu'un logo AI ressemble à une marque existante ?",
                 "options": ["A) Adobe Firefly protège automatiquement", "B) Vérifier sur Google Images + outils de détection de similarité avant livraison", "C) C'est la responsabilité du client", "D) Ajouter une clause dans le contrat"],
                 "correct": "B", "explanation": "La vérification d'originalité avant livraison est une obligation professionnelle du designer AI.", "module": 3},
                {"id": 14,
                 "question": "Quel style design combine calligraphie arabe et design moderne pour le marché Afrique du Nord ?",
                 "options": ["A) Bauhaus traditionnel", "B) Arabesque moderne — fusion patrimoine arabe et design contemporain", "C) Minimalisme japonais", "D) Flat design occidental"],
                 "correct": "B", "explanation": "L'Arabesque moderne est une niche unique qui valorise le patrimoine visuel arabe avec les codes du design contemporain.", "module": 3},
                {"id": 15,
                 "question": "Votre agence perd son identité distinctive après adoption AI. Première action ?",
                 "options": ["A) Arrêter l'AI", "B) Créer un Brand Vision Prompt Guide avec prompts brandés spécifiques à votre ADN", "C) Changer d'outils AI", "D) Embaucher un DA supplémentaire"],
                 "correct": "B", "explanation": "Le Brand Vision Prompt Guide encode l'ADN créatif de l'agence dans les prompts pour maintenir l'authenticité.", "module": 3},
                {"id": 16,
                 "question": "Un client découvre que votre logo ressemble à une marque internationale. Première action dans les 24h ?",
                 "options": ["A) Ignorer", "B) Retirer le logo + contacter le client + préparer une communication transparente + régénérer", "C) Modifier la couleur du logo", "D) Demander au client de s'occuper des légaux"],
                 "correct": "B", "explanation": "Transparence rapide + action corrective immédiate = gestion de crise professionnelle.", "module": 3},
                {"id": 17,
                 "question": "Quelles interdictions sont essentielles dans une politique design AI en Afrique du Nord ?",
                 "options": ["A) Utiliser Canva AI pour des posts", "B) Deepfakes célébrités, contrefaçon involontaire, appropriation culturelle non consentie, faux portfolios AI", "C) Créer des logos avec Midjourney", "D) Générer des images pour les réseaux sociaux"],
                 "correct": "B", "explanation": "Ces 4 interdictions sont les risques éthiques et légaux majeurs du design AI.", "module": 3},
                {"id": 18,
                 "question": "Comment présenter l'usage de l'AI à un client sceptique qui dit 'L'AI c'est froid et sans âme' ?",
                 "options": ["A) Lui cacher l'usage de l'AI", "B) Montrer comment l'AI accélère l'exploration créative et vous permet d'offrir plus d'options avec la même âme", "C) Lui dire que l'AI c'est l'avenir et qu'il doit s'adapter", "D) Baisser vos tarifs"],
                 "correct": "B", "explanation": "L'AI augmente la créativité humaine — le designer reste le directeur artistique et apporte l'âme.", "module": 3},
                {"id": 19,
                 "question": "Quel avantage unique les designers Afrique du Nord ont-ils dans l'ère AI ?",
                 "options": ["A) Aucun avantage particulier", "B) La maîtrise de l'esthétique arabe et berbère — une niche mondiale que les AI occidentales maîtrisent mal", "C) Des outils AI moins chers", "D) Plus de temps libre"],
                 "correct": "B", "explanation": "L'esthétique arabe, la calligraphie et les codes visuels MENA sont une niche mondiale à fort potentiel.", "module": 3},
                {"id": 20,
                 "question": "Quel est le score minimum requis pour la certification Euklydia AI Designer ?",
                 "options": ["A) 70% test + 70/100 projet", "B) 80% test + 75/100 projet", "C) 90% test + 80/100 projet", "D) 75% test + 70/100 projet"],
                 "correct": "B", "explanation": "Certification Euklydia : 80% minimum au test + 75/100 minimum au projet.", "module": 3},
            ],
            "passing_score": 80,
            "duration_min": 30,
        },
        hints_fr=[
            {"level": 1, "text": "Relisez les key takeaways de chaque module avant de commencer."},
            {"level": 2, "text": "Module 1 : outils et éthique basique. Module 2 : création avancée. Module 3 : stratégie et gouvernance."},
        ],
    ))
    db.flush()

    # ── Leçon Cert.2 — Projet de certification ───────────────────────────────
    l3_cert_2 = Lesson(
        unit_id=u3_cert.id, order=2,
        title_fr="Projet de certification — Dossier complet design AI",
        title_en="Certification project — Complete AI design portfolio",
        format="exercise", difficulty_level=5, estimated_duration_min=480,
        description_fr="Projet intégrateur final. Évalué par le jury Euklydia sous 5 jours ouvrés.",
        description_en="Final integrative project. Evaluated by Euklydia jury within 5 business days.",
        prerequisite_lesson_id=l3_cert_1.id,
    )
    db.add(l3_cert_2); db.flush()

    db.add(Activity(
        lesson_id=l3_cert_2.id, order=1, type="exercise",
        title_fr="Projet de certification — AI Designer Euklydia",
        title_en="Certification project — Euklydia AI Designer",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "instructions": "6 livrables obligatoires. 7 jours après validation du test pour soumettre.",
            "livrables": [
                {"id": 1, "titre": "Portfolio design AI",
                 "description": "10 créations AI représentatives avec note sur l'outil, le prompt et le contexte culturel Afrique du Nord.",
                 "format": "PDF ou lien Behance/Figma"},
                {"id": 2, "titre": "Identité visuelle bilingue AR/FR complète",
                 "description": "Logo + palette + typographie + brand guidelines + 5 applications.",
                 "format": "Dossier PDF + fichiers sources"},
                {"id": 3, "titre": "Interface mobile complète bilingue",
                 "description": "5 écrans en version FR (LTR) + 5 écrans en version AR (RTL) avec Figma AI.",
                 "format": "Fichier Figma + export PNG"},
                {"id": 4, "titre": "Vidéo publicitaire AI complète",
                 "description": "30-60 secondes : Midjourney + Runway ML + ElevenLabs + CapCut AI. Bilingue AR/FR.",
                 "format": "MP4 (3 formats)"},
                {"id": 5, "titre": "Politique design AI de mon agence",
                 "description": "Document officiel 8 sections conforme aux pratiques éthiques Afrique du Nord.",
                 "format": "PDF 4-6 pages"},
                {"id": 6, "titre": "Présentation stratégique clients",
                 "description": "Pitch 10 slides pour présenter l'approche design AI + réponses aux 3 objections.",
                 "format": "PDF ou PowerPoint"},
            ],
            "criteres_evaluation": {
                "portfolio_qualite": "20%",
                "identite_visuelle_bilingue": "20%",
                "interface_mobile_bilingue": "15%",
                "video_publicitaire": "15%",
                "politique_design_ai": "15%",
                "presentation_strategique": "15%",
            },
            "score_minimum": 75,
            "delai_soumission": "7 jours après validation du test",
            "feedback": "Jury Euklydia — 2 membres — dans les 5 jours ouvrés",
            "certification_obtenue": {
                "badge": "Badge LinkedIn officiel AI Designer",
                "certificat": "Certificat PDF signé Euklydia",
                "annuaire": "Inscription Annuaire Euklydia Afrique du Nord",
                "validite": "2 ans",
            },
        },
        rubric_fr={"criteres": [
            {"nom": "Portfolio design AI", "poids": 0.20,
             "description": "10 créations de qualité professionnelle, adaptation culturelle Afrique du Nord visible."},
            {"nom": "Identité visuelle bilingue", "poids": 0.20,
             "description": "Cohérence AR/FR, calligraphie arabe valorisée, brand guidelines opérationnels."},
            {"nom": "Interface mobile bilingue", "poids": 0.15,
             "description": "RTL correct, typographies arabes adaptées, UX cohérente sur les 10 écrans."},
            {"nom": "Vidéo publicitaire AI", "poids": 0.15,
             "description": "Production complète, voix off bilingue, adaptation culturelle, 3 formats."},
            {"nom": "Politique design AI", "poids": 0.15,
             "description": "8 sections, interdictions pertinentes, transparence client, conforme lois Afrique du Nord."},
            {"nom": "Présentation stratégique", "poids": 0.15,
             "description": "Pitch convaincant, exemples concrets, réponses aux objections solides."},
        ]},
    ))
    db.flush()

    db.commit()
    print("✅ AI Designer — units, lessons, activities insérées")
    print("   Module 1 — Fondations : 5 unités, 14 leçons (contenu complet)")
    print("   Module 2 — Pratique   : 5 unités, 14 leçons (contenu complet)")
    print("   Module 3 — Expert     : 6 unités, 16 leçons (+ certification finale)")
    print("   Total                 : 16 unités, 44 leçons")