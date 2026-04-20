"""
Seed des units, lessons et activities — AI Sales Specialist (role_id=79)
Module 1 — Fondations   : 5 unités, 14 leçons
Module 2 — Pratique     : 5 unités, 14 leçons
Module 3 — Expert       : 6 unités, 16 leçons (+ certification finale)
Total                   : 16 unités, 44 leçons

Corrections appliquées :
  ✅ M1 — Doublon db.add(u1_4) supprimé
  ✅ M1 — Quiz leçons 1.2, 2.2, 3.1 enrichis (3 questions chacun)
  ✅ M2 — Vidéos ajoutées leçons 4.1, 4.2, 4.3
  ✅ M2 — passing_score=0 leçon 4.1 (évaluation manuelle)
  ✅ M2 — Titre leçon 2.3 harmonisé
  ✅ M3 — Vidéo ajoutée leçon 3.2
  ✅ M3 — passing_score=0 leçons 1.3 et 3.3 (feedback mentor)
  ✅ M3 — Certification finale : unité 6 + test 20Q + projet

Ordre d'exécution :
  1. seed_ai_sales_diagnostic.py
  2. seed_ai_sales_modules.py
  3. seed_ai_sales_units_lessons.py  ← ce fichier
"""

from app.models.module import Module
from app.models.unit import Unit
from app.models.lesson import Lesson
from app.models.activity import Activity


def seed_ai_sales_units_lessons(db):

    # ── Récupérer les 3 modules ───────────────────────────────────────────────
    m1 = db.query(Module).filter_by(role="AI Sales Specialist", journey_stage="foundation").first()
    m2 = db.query(Module).filter_by(role="AI Sales Specialist", journey_stage="practice").first()
    m3 = db.query(Module).filter_by(role="AI Sales Specialist", journey_stage="expert").first()

    if not all([m1, m2, m3]):
        print("❌ Modules AI Sales Specialist introuvables — lancer seed_modules d'abord")
        return

    # ── Supprimer les données existantes pour éviter les doublons ─────────────
    for module in [m1, m2, m3]:
        existing_units = db.query(Unit).filter_by(module_id=module.id).all()
        for u in existing_units:
            for lesson in db.query(Lesson).filter_by(unit_id=u.id).all():
                for activity in db.query(Activity).filter_by(lesson_id=lesson.id).all():
                    db.delete(activity)
                db.delete(lesson)
            db.delete(u)
    db.flush()

    # ════════════════════════════════════════════════════════════════════════
    # UNITÉ 1 — L'AI DANS LA VENTE
    # ════════════════════════════════════════════════════════════════════════

    u1_1 = Unit(
        module_id=m1.id, order=1,
        title_fr="L'AI dans la vente",
        title_en="AI in Sales",
        description_fr="Comprendre ce qu'est l'AI, ses outils et son contexte en Afrique du Nord.",
        description_en="Understand what AI is, its tools and the North Africa context.",
        estimated_duration_min=26,
    )
    db.add(u1_1); db.flush()

    # ── Leçon 1.1 ────────────────────────────────────────────────────────────
    l1_1_1 = Lesson(
        unit_id=u1_1.id, order=1,
        title_fr="C'est quoi l'AI pour un commercial ?",
        title_en="What is AI for a salesperson?",
        format="video", difficulty_level=1, estimated_duration_min=10,
        description_fr="Définition de l'AI, 4 usages commerciaux, règle d'or AI + Humain.",
        description_en="AI definition, 4 commercial uses, AI + Human golden rule.",
    )
    db.add(l1_1_1); db.flush()

    db.add(Activity(
        lesson_id=l1_1_1.id, order=1, type="video",
        title_fr="Vidéo — C'est quoi l'AI pour un commercial ?",
        title_en="Video — What is AI for a salesperson?",
        is_assessed=False, is_required=True,
        content_fr={"duration_min": 10, "url_fr": None},
        content_en={"duration_min": 10, "url_en": None},
    ))
    db.add(Activity(
        lesson_id=l1_1_1.id, order=2, type="quiz",
        title_fr="Quiz — L'AI dans la vente",
        title_en="Quiz — AI in sales",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "questions": [
                {
                    "id": 1,
                    "question": "Qu'est-ce que l'AI permet principalement à un commercial ?",
                    "options": [
                        "A) Remplacer complètement le commercial",
                        "B) Analyser, prédire et automatiser pour travailler plus efficacement",
                        "C) Supprimer le besoin d'un CRM",
                        "D) Appeler les clients automatiquement"
                    ],
                    "correct": "B",
                    "explanation": "L'AI analyse, prédit et automatise. Elle amplifie l'efficacité du commercial sans le remplacer."
                },
                {
                    "id": 2,
                    "question": "Quel outil est un CRM avec AI intégré ?",
                    "options": ["A) Canva", "B) Midjourney", "C) HubSpot AI", "D) Runway ML"],
                    "correct": "C",
                    "explanation": "HubSpot AI intègre l'intelligence artificielle nativement pour le scoring et la rédaction."
                },
                {
                    "id": 3,
                    "question": "Quelle est la règle d'or de l'AI pour un commercial ?",
                    "options": [
                        "A) L'AI remplace le commercial sur toutes les tâches",
                        "B) L'AI amplifie le commercial — elle ne le remplace pas",
                        "C) L'AI fonctionne uniquement en anglais",
                        "D) L'AI est réservée aux grandes entreprises"
                    ],
                    "correct": "B",
                    "explanation": "L'AI est un outil d'amplification — le commercial reste indispensable pour la relation humaine."
                },
            ],
            "passing_score": 70,
        },
        hints_fr=[
            {"level": 1, "text": "Pense à ce que l'AI fait concrètement pour un commercial au quotidien."},
            {"level": 2, "text": "L'AI analyse des données, prédit des comportements et automatise des tâches répétitives."},
        ],
    ))
    db.flush()

    # ── Leçon 1.2 — Quiz enrichi (3 questions) ───────────────────────────────
    l1_1_2 = Lesson(
        unit_id=u1_1.id, order=2,
        title_fr="Les outils AI du commercial",
        title_en="Sales AI tools",
        format="video", difficulty_level=1, estimated_duration_min=8,
        description_fr="5 catégories d'outils AI, focus ChatGPT + HubSpot AI pour débutants.",
        description_en="5 AI tool categories, focus ChatGPT + HubSpot AI for beginners.",
        prerequisite_lesson_id=l1_1_1.id,
    )
    db.add(l1_1_2); db.flush()

    db.add(Activity(
        lesson_id=l1_1_2.id, order=1, type="video",
        title_fr="Vidéo — Les outils AI du commercial",
        title_en="Video — Sales AI tools",
        is_assessed=False, is_required=True,
        content_fr={"duration_min": 8, "url_fr": None},
    ))
    db.add(Activity(
        lesson_id=l1_1_2.id, order=2, type="quiz",
        title_fr="Quiz — Outils AI",
        title_en="Quiz — AI Tools",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "questions": [
                {
                    "id": 1,
                    "question": "Quel outil recommandez-vous pour un commercial débutant avec un budget < 30$/mois ?",
                    "options": [
                        "A) Salesforce Enterprise + LinkedIn Sales Navigator",
                        "B) HubSpot gratuit + ChatGPT gratuit",
                        "C) Tableau AI + Outreach",
                        "D) Oracle CRM + ActiveCampaign"
                    ],
                    "correct": "B",
                    "explanation": "HubSpot gratuit + ChatGPT gratuit couvre 80% des besoins d'une PME pour moins de 30$/mois."
                },
                # ✅ Question ajoutée
                {
                    "id": 2,
                    "question": "Quelle est la catégorie principale de ChatGPT dans le contexte commercial ?",
                    "options": [
                        "A) CRM (Customer Relationship Management)",
                        "B) Outil de génération de contenu et d'assistance à la rédaction",
                        "C) Outil d'analyse de données financières",
                        "D) Plateforme d'emailing automatisé"
                    ],
                    "correct": "B",
                    "explanation": "ChatGPT appartient à la catégorie des outils de génération de contenu — il aide à rédiger emails, scripts, prompts et résumés."
                },
                # ✅ Question ajoutée
                {
                    "id": 3,
                    "question": "Quel outil est le plus adapté pour gérer les contacts et suivre les deals d'un commercial débutant ?",
                    "options": [
                        "A) ChatGPT",
                        "B) Canva",
                        "C) HubSpot CRM gratuit",
                        "D) Google Sheets uniquement"
                    ],
                    "correct": "C",
                    "explanation": "HubSpot CRM gratuit est conçu spécifiquement pour gérer contacts, deals et pipeline — contrairement aux autres options qui ne sont pas des CRM."
                },
            ],
            "passing_score": 70,
        },
    ))
    db.flush()

    # ── Leçon 1.3 ────────────────────────────────────────────────────────────
    l1_1_3 = Lesson(
        unit_id=u1_1.id, order=3,
        title_fr="L'AI dans le contexte MENA",
        title_en="AI in the MENA context",
        format="video", difficulty_level=1, estimated_duration_min=8,
        description_fr="Réalités MENA, opportunités, défis culturels, calendrier saisonnier.",
        description_en="MENA realities, opportunities, cultural challenges, seasonal calendar.",
        prerequisite_lesson_id=l1_1_2.id,
    )
    db.add(l1_1_3); db.flush()

    db.add(Activity(
        lesson_id=l1_1_3.id, order=1, type="video",
        title_fr="Vidéo — L'AI dans le contexte MENA",
        is_assessed=False, is_required=True,
        content_fr={"duration_min": 8, "url_fr": None},
    ))
    db.add(Activity(
        lesson_id=l1_1_3.id, order=2, type="forum_discussion",
        title_fr="Forum — L'AI dans votre contexte professionnel",
        title_en="Forum — AI in your professional context",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "question": "Dans votre contexte professionnel en Tunisie ou dans votre pays, quel est selon vous le plus grand défi pour adopter l'AI dans la vente ? Et quelle opportunité voyez-vous ?",
            "consigne": "Répondre en minimum 5 lignes. Commenter la réponse d'au moins un autre apprenant.",
        },
    ))
    db.flush()

    # ════════════════════════════════════════════════════════════════════════
    # UNITÉ 2 — MON PREMIER CRM AVEC AI
    # ════════════════════════════════════════════════════════════════════════

    u1_2 = Unit(
        module_id=m1.id, order=2,
        title_fr="Mon premier CRM avec AI",
        title_en="My First CRM with AI",
        description_fr="Comprendre le CRM, ses super-pouvoirs AI, configurer HubSpot.",
        description_en="Understand CRM, its AI superpowers, configure HubSpot.",
        estimated_duration_min=34,
    )
    db.add(u1_2); db.flush()

    # ── Leçon 2.1 ────────────────────────────────────────────────────────────
    l1_2_1 = Lesson(
        unit_id=u1_2.id, order=1,
        title_fr="C'est quoi un CRM ?",
        title_en="What is a CRM?",
        format="video", difficulty_level=1, estimated_duration_min=12,
        description_fr="Définition CRM, 5 fonctions essentielles, pipeline en 6 étapes MENA.",
        description_en="CRM definition, 5 essential functions, 6-stage MENA pipeline.",
    )
    db.add(l1_2_1); db.flush()

    db.add(Activity(
        lesson_id=l1_2_1.id, order=1, type="video",
        is_assessed=False, is_required=True, content_fr={"duration_min": 12},
    ))
    db.add(Activity(
        lesson_id=l1_2_1.id, order=2, type="exercise",
        title_fr="Cartographier votre pipeline commercial",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "consigne": "Prenez votre liste actuelle de prospects. Classez-les dans les 6 étapes du pipeline. Identifiez l'étape où vous avez le plus de blocages.",
            "livrable": "Tableau avec vos prospects répartis en 6 étapes",
            "duree_estimee": "20 minutes",
        },
    ))
    db.flush()

    # ── Leçon 2.2 — Quiz enrichi (3 questions) ───────────────────────────────
    l1_2_2 = Lesson(
        unit_id=u1_2.id, order=2,
        title_fr="Comment l'AI améliore le CRM",
        title_en="How AI improves CRM",
        format="video", difficulty_level=2, estimated_duration_min=10,
        prerequisite_lesson_id=l1_2_1.id,
        description_fr="4 super-pouvoirs AI : scoring, churn, suggestions, rédaction. Cas Karim à Sfax.",
    )
    db.add(l1_2_2); db.flush()

    db.add(Activity(
        lesson_id=l1_2_2.id, order=1, type="video",
        is_assessed=False, is_required=True, content_fr={"duration_min": 10},
    ))
    db.add(Activity(
        lesson_id=l1_2_2.id, order=2, type="quiz",
        title_fr="Quiz — CRM avec AI",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "questions": [
                {
                    "id": 1,
                    "question": "Quelle est la différence entre un CRM classique et un CRM avec AI ?",
                    "options": [
                        "A) Le CRM classique est gratuit, le CRM AI est payant",
                        "B) Le CRM classique stocke passivement ; le CRM AI analyse et recommande proactivement",
                        "C) Le CRM AI remplace complètement le commercial",
                        "D) Il n'y a pas de différence significative"
                    ],
                    "correct": "B",
                    "explanation": "Le CRM AI est proactif — il analyse et recommande. Le CRM classique est passif — il stocke."
                },
                # ✅ Question ajoutée
                {
                    "id": 2,
                    "question": "Un prospect a visité votre page tarifs 3 fois cette semaine. Que fait HubSpot AI ?",
                    "options": [
                        "A) Rien — HubSpot ne suit pas les visites",
                        "B) Il augmente automatiquement le score de ce prospect et vous alerte",
                        "C) Il envoie automatiquement un devis au prospect",
                        "D) Il supprime le prospect des prospects froids"
                    ],
                    "correct": "B",
                    "explanation": "HubSpot AI détecte les signaux d'intention d'achat (visites répétées de la page tarifs) et augmente le score du prospect pour prioriser votre action."
                },
                # ✅ Question ajoutée
                {
                    "id": 3,
                    "question": "Qu'est-ce que la prédiction de churn dans un CRM AI ?",
                    "options": [
                        "A) Prédire quels prospects vont acheter",
                        "B) Identifier les clients existants risquant de ne pas renouveler ou partir",
                        "C) Calculer automatiquement les commissions des commerciaux",
                        "D) Filtrer les emails indésirables"
                    ],
                    "correct": "B",
                    "explanation": "Le churn prediction analyse les comportements des clients existants pour détecter ceux qui risquent de partir — permettant une action proactive de rétention."
                },
            ],
            "passing_score": 70,
        },
    ))
    db.flush()

    # ── Leçon 2.3 ────────────────────────────────────────────────────────────
    l1_2_3 = Lesson(
        unit_id=u1_2.id, order=3,
        title_fr="Mon premier CRM en pratique",
        title_en="My first CRM in practice",
        format="tutorial", difficulty_level=2, estimated_duration_min=45,
        prerequisite_lesson_id=l1_2_2.id,
        description_fr="Tutoriel HubSpot pas à pas : compte, pipeline, contacts, deals, scoring.",
    )
    db.add(l1_2_3); db.flush()

    db.add(Activity(
        lesson_id=l1_2_3.id, order=1, type="exercise",
        title_fr="Tutoriel HubSpot — 6 étapes",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "steps": [
                "Créer votre compte HubSpot gratuit sur hubspot.com/fr",
                "Configurer votre pipeline en 6 étapes MENA",
                "Ajouter 5 contacts minimum avec informations complètes",
                "Créer 3 deals et les positionner dans le pipeline",
                "Activer et lire le scoring AI des leads",
                "Soumettre une capture d'écran de votre vue pipeline",
            ],
            "livrable": "Capture d'écran pipeline + 5 contacts + 3 deals",
            "criteres": {
                "exhaustivite_informations": "40%",
                "pertinence_positionnement": "40%",
                "qualite_notes": "20%",
            },
            "score_minimum": 70,
        },
        hints_fr=[
            {"level": 1, "text": "Commencez par créer votre compte — le bouton 'Démarrer gratuitement' est en haut à droite sur hubspot.com/fr"},
            {"level": 2, "text": "Pour configurer le pipeline : Ventes > Deals > ⚙️ > Modifier les étapes"},
            {"level": 3, "text": "Les 6 étapes MENA recommandées : Nouveau contact → Prise de contact → Qualification → Proposition → Négociation → Gagné/Perdu"},
        ],
    ))
    db.flush()

    # ════════════════════════════════════════════════════════════════════════
    # UNITÉ 3 — MA PREMIÈRE PROSPECTION AI
    # ════════════════════════════════════════════════════════════════════════

    u1_3 = Unit(
        module_id=m1.id, order=3,
        title_fr="Ma première prospection AI",
        title_en="My First AI Prospection",
        estimated_duration_min=26,
    )
    db.add(u1_3); db.flush()

    # ── Leçon 3.1 — Quiz enrichi (3 questions) ───────────────────────────────
    l1_3_1 = Lesson(
        unit_id=u1_3.id, order=1,
        title_fr="C'est quoi la prospection ?",
        title_en="What is prospection?",
        format="video", difficulty_level=1, estimated_duration_min=8,
        description_fr="3 types de prospection, 5 étapes, codes culturels MENA.",
    )
    db.add(l1_3_1); db.flush()

    db.add(Activity(
        lesson_id=l1_3_1.id, order=1, type="video",
        is_assessed=False, is_required=True,
        content_fr={"duration_min": 8, "url_fr": None},
    ))
    db.add(Activity(
        lesson_id=l1_3_1.id, order=2, type="quiz",
        title_fr="Quiz — La prospection commerciale",
        title_en="Quiz — Commercial prospection",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "questions": [
                {
                    "id": 1,
                    "question": "Quelle est la définition de la prospection commerciale ?",
                    "options": [
                        "A) Fidéliser les clients existants",
                        "B) Identifier, contacter et qualifier des clients potentiels",
                        "C) Gérer les réclamations",
                        "D) Rédiger des propositions"
                    ],
                    "correct": "B",
                    "explanation": "La prospection est la première étape du cycle de vente — identifier et qualifier des clients potentiels."
                },
                # ✅ Question ajoutée
                {
                    "id": 2,
                    "question": "Quelle est la différence entre prospection froide et prospection chaude ?",
                    "options": [
                        "A) La prospection froide est en hiver, la chaude en été",
                        "B) La froide cible des inconnus sans contact préalable, la chaude cible des personnes déjà en relation avec vous",
                        "C) La froide utilise des emails, la chaude utilise le téléphone",
                        "D) Il n'y a pas de différence pratique entre les deux"
                    ],
                    "correct": "B",
                    "explanation": "La prospection froide s'adresse à des inconnus (cold outreach). La prospection chaude s'adresse à des prospects déjà en contact — taux de conversion 5 à 10x supérieur."
                },
                # ✅ Question ajoutée
                {
                    "id": 3,
                    "question": "Dans le contexte MENA, quel canal est souvent plus efficace que LinkedIn pour la prospection B2B PME ?",
                    "options": [
                        "A) Instagram",
                        "B) TikTok",
                        "C) WhatsApp",
                        "D) Pinterest"
                    ],
                    "correct": "C",
                    "explanation": "En MENA, WhatsApp est un canal B2B majeur — beaucoup de dirigeants de PME préfèrent un message WhatsApp professionnel à un email ou un message LinkedIn."
                },
            ],
            "passing_score": 70,
        },
    ))
    db.flush()

    # ── Leçon 3.2 ────────────────────────────────────────────────────────────
    l1_3_2 = Lesson(
        unit_id=u1_3.id, order=2,
        title_fr="Identifier les bons prospects",
        title_en="Identify the right prospects",
        format="video", difficulty_level=2, estimated_duration_min=10,
        prerequisite_lesson_id=l1_3_1.id,
        description_fr="ICP, méthode BANT, signaux d'achat AI, cas Sonia EdTech.",
    )
    db.add(l1_3_2); db.flush()

    db.add(Activity(
        lesson_id=l1_3_2.id, order=1, type="video",
        is_assessed=False, is_required=True,
        content_fr={"duration_min": 10, "url_fr": None},
    ))
    db.add(Activity(
        lesson_id=l1_3_2.id, order=2, type="exercise",
        title_fr="Définir mon ICP et identifier 5 prospects prioritaires",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": "Remplissez la fiche ICP basée sur vos 3 meilleurs clients. Identifiez 5 prospects correspondants dans HubSpot.",
            "livrable": "Fiche ICP + 5 prospects avec justification",
            "criteres": {"completude_icp": "50%", "pertinence_prospects": "50%"},
        },
        hints_fr=[
            {"level": 1, "text": "Pensez à vos 3 meilleurs clients actuels — qu'ont-ils en commun en termes de secteur, taille, ville ?"},
        ],
    ))
    db.flush()

    # ── Leçon 3.3 ────────────────────────────────────────────────────────────
    l1_3_3 = Lesson(
        unit_id=u1_3.id, order=3,
        title_fr="Mon premier prompt de prospection",
        title_en="My first prospection prompt",
        format="exercise", difficulty_level=2, estimated_duration_min=30,
        prerequisite_lesson_id=l1_3_2.id,
        description_fr="Structure en 5 éléments, 4 prompts MENA prêts à l'emploi.",
    )
    db.add(l1_3_3); db.flush()

    db.add(Activity(
        lesson_id=l1_3_3.id, order=1, type="prompt_practice",
        title_fr="Bibliothèque de prompts MENA",
        is_assessed=False, has_hints=True,
        content_fr={"prompts": [
            {
                "titre": "Email prospection froide B2B Tunisie",
                "prompt": "Tu es un expert commercial B2B spécialisé dans les PME tunisiennes. Rédige un email de prospection froide en français pour contacter [NOM], [POSTE] chez [ENTREPRISE]...",
            },
            {
                "titre": "Relance après silence",
                "prompt": "Tu es un commercial B2B expérimenté en Tunisie. Rédige un message de relance cordial pour [NOM] qui n'a pas répondu depuis [X] jours...",
            },
        ]},
        hints_fr=[
            {"level": 1, "text": "Un bon prompt contient : Rôle + Contexte + Objectif + Contraintes + Personnalisation."},
            {"level": 2, "text": "Exemple de rôle : 'Tu es un expert commercial B2B spécialisé dans les PME tunisiennes.'"},
        ],
    ))
    db.add(Activity(
        lesson_id=l1_3_3.id, order=2, type="exercise",
        title_fr="Rédiger mon premier email de prospection AI",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": (
                "1. Choisissez un prospect de votre liste.\n"
                "2. Rédigez un prompt complet (5 éléments).\n"
                "3. Générez l'email avec ChatGPT.\n"
                "4. Personnalisez (3 modifications minimum).\n"
                "5. Soumettez : prompt + email généré + email personnalisé."
            ),
            "criteres": {"qualite_prompt": "30%", "pertinence_email": "30%", "personnalisation": "40%"},
            "score_minimum": 70,
        },
        rubric_fr={"criteres": [
            {"nom": "Structure du prompt", "poids": 0.3, "description": "Les 5 éléments sont présents et cohérents"},
            {"nom": "Pertinence de l'email", "poids": 0.3, "description": "L'email est adapté au prospect cible"},
            {"nom": "Qualité de la personnalisation", "poids": 0.4, "description": "Au moins 3 modifications personnelles pertinentes"},
        ]},
    ))
    db.flush()

    # ════════════════════════════════════════════════════════════════════════
    # UNITÉ 4 — MON PREMIER EMAIL AI
    # ════════════════════════════════════════════════════════════════════════

    u1_4 = Unit(
        module_id=m1.id, order=4,
        title_fr="Mon premier email AI",
        title_en="My First AI Email",
        description_fr="Rédiger, personnaliser et envoyer des emails de prospection avec ChatGPT.",
        description_en="Write, personalise and send prospecting emails with ChatGPT.",
        estimated_duration_min=50,
    )
    db.add(u1_4); db.flush()  # ✅ Une seule fois (doublon supprimé)

    # ── Leçon 4.1 ────────────────────────────────────────────────────────────
    l1_4_1 = Lesson(
        unit_id=u1_4.id, order=1,
        title_fr="Rédiger avec ChatGPT",
        title_en="Writing with ChatGPT",
        format="video", difficulty_level=2, estimated_duration_min=12,
        description_fr="Anatomie d'un bon prompt, 3 types d'emails commerciaux, démonstration en direct.",
        description_en="Anatomy of a good prompt, 3 types of commercial emails, live demo.",
    )
    db.add(l1_4_1); db.flush()

    db.add(Activity(
        lesson_id=l1_4_1.id, order=1, type="video",
        title_fr="Vidéo — Rédiger avec ChatGPT",
        title_en="Video — Writing with ChatGPT",
        is_assessed=False, is_required=True,
        content_fr={"duration_min": 12, "url_fr": None},
        content_en={"duration_min": 12, "url_en": None},
    ))
    db.add(Activity(
        lesson_id=l1_4_1.id, order=2, type="quiz",
        title_fr="Quiz — Rédiger avec ChatGPT",
        title_en="Quiz — Writing with ChatGPT",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "questions": [
                {
                    "id": 1,
                    "question": "Vous demandez à ChatGPT de rédiger un email et le résultat est trop générique. Quelle est la cause principale ?",
                    "options": [
                        "A) ChatGPT ne peut pas rédiger des emails commerciaux",
                        "B) Votre prompt manque de contexte : secteur, nom du prospect, objectif précis",
                        "C) Il faut passer à la version payante de ChatGPT",
                        "D) Les emails générés par AI sont toujours génériques",
                    ],
                    "correct": "B",
                    "explanation": "La qualité de l'output dépend directement de la qualité du prompt. Un prompt avec contexte produit un email ciblé et pertinent.",
                },
                {
                    "id": 2,
                    "question": "Parmi ces prompts, lequel va produire le meilleur email de prospection pour le marché tunisien ?",
                    "options": [
                        "A) 'Écris un email de vente'",
                        "B) 'Écris un email professionnel'",
                        "C) 'Tu es un expert commercial B2B en Tunisie. Rédige un email de prospection froide en français pour Mehdi Karim, DG d'une PME industrielle à Sfax. Ton cordial, 150 mots maximum.'",
                        "D) 'Rédige un email pour vendre un logiciel RH'",
                    ],
                    "correct": "C",
                    "explanation": "Un bon prompt contient 5 éléments : Rôle, Contexte, Objectif, Contraintes et Personnalisation.",
                },
                {
                    "id": 3,
                    "question": "ChatGPT vous génère un email de prospection. Quelle est la meilleure pratique avant de l'envoyer ?",
                    "options": [
                        "A) L'envoyer immédiatement — ChatGPT est fiable",
                        "B) Le relire, vérifier les faits, ajouter des détails personnels et adapter le ton",
                        "C) Le traduire en anglais pour paraître plus professionnel",
                        "D) Le raccourcir à 3 phrases maximum",
                    ],
                    "correct": "B",
                    "explanation": "L'AI génère une base solide mais le commercial doit toujours personnaliser et vérifier avant envoi.",
                },
                {
                    "id": 4,
                    "question": "Quel est le principal avantage d'utiliser ChatGPT pour rédiger des emails commerciaux ?",
                    "options": [
                        "A) Garantir un taux d'ouverture de 100%",
                        "B) Éliminer le besoin de connaître le produit vendu",
                        "C) Réduire le temps de rédaction de 80% tout en maintenant un niveau de qualité élevé",
                        "D) Envoyer des emails sans validation humaine",
                    ],
                    "correct": "C",
                    "explanation": "ChatGPT réduit drastiquement le temps de rédaction — le commercial consacre le temps gagné à la personnalisation.",
                },
            ],
            "passing_score": 70,
        },
        hints_fr=[
            {"level": 1, "text": "Pense aux 5 éléments d'un bon prompt : Rôle, Contexte, Objectif, Contraintes, Personnalisation."},
            {"level": 2, "text": "ChatGPT est un amplificateur — il produit la structure, le commercial apporte la valeur ajoutée humaine."},
        ],
    ))
    db.flush()

    # ── Leçon 4.2 ────────────────────────────────────────────────────────────
    l1_4_2 = Lesson(
        unit_id=u1_4.id, order=2,
        title_fr="Personnaliser en arabe et en français",
        title_en="Personalise in Arabic and French",
        format="video", difficulty_level=2, estimated_duration_min=8,
        description_fr="Codes culturels MENA, formules de politesse par langue, 3 erreurs à éviter.",
        description_en="MENA cultural codes, politeness formulas by language, 3 mistakes to avoid.",
        prerequisite_lesson_id=l1_4_1.id,
    )
    db.add(l1_4_2); db.flush()

    db.add(Activity(
        lesson_id=l1_4_2.id, order=1, type="video",
        title_fr="Vidéo — Personnaliser en arabe et en français",
        title_en="Video — Personalise in Arabic and French",
        is_assessed=False, is_required=True,
        content_fr={"duration_min": 8, "url_fr": None},
    ))
    db.add(Activity(
        lesson_id=l1_4_2.id, order=2, type="exercise",
        title_fr="Exercice — Adapter un email au contexte MENA",
        title_en="Exercise — Adapt an email to the MENA context",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": (
                "Email de base (ChatGPT) :\n"
                "Objet : Notre solution peut vous aider\n"
                "Bonjour, je me permets de vous contacter au sujet de notre logiciel. "
                "Notre solution aide les entreprises à augmenter leurs ventes de 30%. "
                "Seriez-vous disponible pour un appel de 15 minutes ?\n\n"
                "Tâche 1 : Adaptez pour Karim Ben Ali, PDG PME à Tunis (distribution alimentaire). "
                "Rédigez en français avec codes culturels tunisiens.\n\n"
                "Tâche 2 : Adaptez pour Khalid Al-Mansouri, Directeur Commercial à Casablanca "
                "(immobilier). Rédigez en français marocain formel."
            ),
            "livrable": "2 emails adaptés avec explication de vos 3 modifications principales par email.",
            "criteres": {
                "adaptation_culturelle": "40%",
                "personnalisation_prospect": "40%",
                "qualite_redaction": "20%",
            },
            "duree_estimee": "25 minutes",
        },
        hints_fr=[
            {"level": 1, "text": "Pour Tunis : 'Cher Monsieur', référence locale, terminez par 'Bien cordialement'."},
            {"level": 2, "text": "Pour Casablanca : ton plus formel, 'Monsieur le Directeur', références immobilier marocain."},
            {"level": 3, "text": "3 modifications clés : (1) Objet spécifique, (2) Référence secteur, (3) CTA adapté au calendrier local."},
        ],
        rubric_fr={"criteres": [
            {"nom": "Adaptation culturelle", "poids": 0.4, "description": "Formules de politesse appropriées, codes culturels respectés."},
            {"nom": "Personnalisation du prospect", "poids": 0.4, "description": "Nom, poste, ville et secteur intégrés naturellement."},
            {"nom": "Qualité de rédaction", "poids": 0.2, "description": "Pas de fautes, structure claire, longueur 100-180 mots."},
        ]},
    ))
    db.flush()

    # ── Leçon 4.3 ────────────────────────────────────────────────────────────
    l1_4_3 = Lesson(
        unit_id=u1_4.id, order=3,
        title_fr="Mon premier email de prospection",
        title_en="My first prospection email",
        format="exercise", difficulty_level=3, estimated_duration_min=30,
        description_fr="Projet intégrateur : sélectionner un prospect, construire le prompt, générer et personnaliser l'email.",
        description_en="Integrative project: select a prospect, build the prompt, generate and personalise the email.",
        prerequisite_lesson_id=l1_4_2.id,
    )
    db.add(l1_4_3); db.flush()

    db.add(Activity(
        lesson_id=l1_4_3.id, order=1, type="exercise",
        title_fr="Projet — Mon premier email de prospection AI complet",
        title_en="Project — My first complete AI prospection email",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": (
                "Étape 1 — Choisissez un prospect réel (nom, poste, entreprise, secteur, ville, besoin).\n\n"
                "Étape 2 — Construisez votre prompt (5 éléments : Rôle + Contexte + Objectif + Contraintes + Personnalisation).\n\n"
                "Étape 3 — Générez l'email avec ChatGPT. Si insatisfaisant, affinez le prompt.\n\n"
                "Étape 4 — Personnalisez avec 4 modifications minimum : "
                "(1) activité récente de l'entreprise, (2) référence marché local, "
                "(3) CTA précis avec date/heure, (4) signature complète.\n\n"
                "Étape 5 — Soumettez : fiche prospect + prompt + email généré + email final personnalisé."
            ),
            "livrable": (
                "Document avec :\n"
                "1. Fiche prospect\n"
                "2. Prompt complet (5 éléments identifiés)\n"
                "3. Email généré par ChatGPT (non modifié)\n"
                "4. Email final personnalisé (modifications surlignées)"
            ),
            "criteres": {
                "qualite_prompt": "25%",
                "pertinence_email_genere": "25%",
                "qualite_personnalisation": "35%",
                "professionnalisme_final": "15%",
            },
            "score_minimum": 70,
            "duree_estimee": "30 à 45 minutes",
        },
        hints_fr=[
            {"level": 1, "text": "Commencez par la fiche prospect — plus vous avez de détails, plus votre prompt sera précis."},
            {"level": 2, "text": "Structure prompt : 'Tu es [RÔLE]. Rédige un email [TYPE] en [LANGUE] pour [NOM], [POSTE] chez [ENTREPRISE] à [VILLE]...'"},
            {"level": 3, "text": "Pour la personnalisation : cherchez sur LinkedIn un événement récent à mentionner — cela multiplie le taux de réponse par 3."},
        ],
        rubric_fr={"criteres": [
            {"nom": "Qualité du prompt", "poids": 0.25, "description": "Les 5 éléments sont présents, le prompt est exploitable directement dans ChatGPT."},
            {"nom": "Pertinence de l'email généré", "poids": 0.25, "description": "L'email est en adéquation avec le prompt, structure correcte."},
            {"nom": "Qualité de la personnalisation", "poids": 0.35, "description": "4 modifications pertinentes, au moins 1 référence spécifique au contexte local."},
            {"nom": "Professionnalisme de l'email final", "poids": 0.15, "description": "Pas de fautes, objet accrocheur, signature complète, ton MENA adapté."},
        ]},
    ))
    db.flush()

    # ════════════════════════════════════════════════════════════════════════
    # UNITÉ 5 — ÉTHIQUE AI BASIQUE
    # ════════════════════════════════════════════════════════════════════════

    u1_5 = Unit(
        module_id=m1.id, order=5,
        title_fr="Éthique AI basique en vente",
        title_en="Basic AI Ethics in Sales",
        description_fr="Les règles fondamentales de l'éthique AI dans la vente.",
        description_en="Fundamental rules of AI ethics in sales.",
        estimated_duration_min=40,
    )
    db.add(u1_5); db.flush()

    # ── Leçon 5.1 ────────────────────────────────────────────────────────────
    l1_5_1 = Lesson(
        unit_id=u1_5.id, order=1,
        title_fr="Les règles fondamentales de l'éthique AI",
        title_en="Fundamental rules of AI ethics",
        format="video", difficulty_level=1, estimated_duration_min=10,
        description_fr="5 principes éthiques, cadre légal MENA, consentement éclairé, signaux d'alerte.",
        description_en="5 ethical principles, MENA legal framework, informed consent, warning signs.",
    )
    db.add(l1_5_1); db.flush()

    db.add(Activity(
        lesson_id=l1_5_1.id, order=1, type="video",
        title_fr="Vidéo — Les règles fondamentales de l'éthique AI",
        title_en="Video — Fundamental rules of AI ethics",
        is_assessed=False, is_required=True,
        content_fr={"duration_min": 10, "url_fr": None},
    ))
    db.add(Activity(
        lesson_id=l1_5_1.id, order=2, type="quiz",
        title_fr="Quiz — Éthique AI fondamentale",
        title_en="Quiz — Fundamental AI ethics",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "questions": [
                {
                    "id": 1,
                    "question": "Un prospect vous a donné son email pour recevoir votre catalogue. Pouvez-vous l'utiliser pour des relances automatiques via HubSpot ?",
                    "options": [
                        "A) Oui, il a donné son email donc vous pouvez l'utiliser pour tout type de communication",
                        "B) Non, il a consenti uniquement pour le catalogue — il faut son accord explicite pour les relances",
                        "C) Oui, tant que les emails sont professionnels",
                        "D) Non, il est interdit d'utiliser l'AI pour les relances",
                    ],
                    "correct": "B",
                    "explanation": "Le consentement éclairé est spécifique à l'usage déclaré. Il faut un consentement explicite pour chaque usage différent.",
                },
                {
                    "id": 2,
                    "question": "Votre AI collecte des données sur le comportement en ligne de vos prospects. Quelle est la pratique éthique ?",
                    "options": [
                        "A) Collecter le maximum de données — plus c'est précis, mieux c'est",
                        "B) Collecter uniquement les données nécessaires, informer les prospects et respecter leur droit d'accès",
                        "C) Partager ces données avec vos partenaires commerciaux",
                        "D) Ne pas informer les prospects pour ne pas les inquiéter",
                    ],
                    "correct": "B",
                    "explanation": "Le principe de minimisation : on ne collecte que ce qui est strictement nécessaire. La transparence est obligatoire.",
                },
                {
                    "id": 3,
                    "question": "Votre AI suggère d'utiliser la vulnérabilité financière d'un prospect pour créer une urgence artificielle. Que faites-vous ?",
                    "options": [
                        "A) Vous suivez la recommandation — l'AI optimise les ventes",
                        "B) Vous refusez — exploiter la vulnérabilité d'un prospect est une manipulation contraire à l'éthique",
                        "C) Vous utilisez l'information avec discrétion",
                        "D) Vous demandez l'avis de votre manager avant",
                    ],
                    "correct": "B",
                    "explanation": "L'éthique AI interdit d'exploiter les vulnérabilités des prospects. Cette pratique est aussi illégale dans de nombreux pays MENA.",
                },
                {
                    "id": 4,
                    "question": "Un prospect demande : 'Utilisez-vous une AI pour me contacter ?' Quelle est la bonne réponse ?",
                    "options": [
                        "A) 'Non, je vous écris personnellement' (même si l'AI rédige les emails)",
                        "B) 'Je ne peux pas vous répondre à ce sujet'",
                        "C) 'Oui, j'utilise des outils AI pour personnaliser mes communications, mais chaque email est validé par moi'",
                        "D) Ignorer la question et changer de sujet",
                    ],
                    "correct": "C",
                    "explanation": "La transparence sur l'utilisation de l'AI est une obligation éthique. Mentir est une faute professionnelle grave.",
                },
                {
                    "id": 5,
                    "question": "Lequel de ces comportements est conforme à l'éthique AI dans la vente ?",
                    "options": [
                        "A) Analyser les émotions d'un prospect lors d'un appel vidéo sans le prévenir",
                        "B) Personnaliser vos emails sur la base des préférences exprimées par le prospect",
                        "C) Accéder aux emails privés d'un prospect pour mieux le comprendre",
                        "D) Créer de faux avis clients pour augmenter la crédibilité",
                    ],
                    "correct": "B",
                    "explanation": "Personnaliser sur la base de préférences exprimées est éthique. Les options A, C et D violent la vie privée ou la confiance.",
                },
            ],
            "passing_score": 70,
        },
        hints_fr=[
            {"level": 1, "text": "Règle d'or : si vous n'êtes pas à l'aise pour dire au prospect exactement comment vous utilisez l'AI, c'est probablement non-éthique."},
            {"level": 2, "text": "5 principes fondamentaux : (1) Consentement éclairé, (2) Minimisation données, (3) Transparence, (4) Non-manipulation, (5) Responsabilité humaine."},
        ],
    ))
    db.flush()

    # ── Leçon 5.2 ────────────────────────────────────────────────────────────
    l1_5_2 = Lesson(
        unit_id=u1_5.id, order=2,
        title_fr="Cas pratiques éthiques simples",
        title_en="Simple ethical case studies",
        format="case_study", difficulty_level=2, estimated_duration_min=30,
        description_fr="3 cas réels de dilemmes éthiques AI rencontrés par des commerciaux MENA.",
        description_en="3 real ethical dilemmas faced by MENA salespeople.",
        prerequisite_lesson_id=l1_5_1.id,
    )
    db.add(l1_5_2); db.flush()

    db.add(Activity(
        lesson_id=l1_5_2.id, order=1, type="case_study",
        title_fr="Cas pratiques — 3 dilemmes éthiques AI",
        title_en="Case studies — 3 AI ethics dilemmas",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "introduction": (
                "Analysez 3 situations réelles. Pour chaque cas : "
                "(1) identifier le problème éthique, (2) choisir la meilleure décision, "
                "(3) justifier en minimum 3 lignes."
            ),
            "cas": [
                {
                    "id": 1,
                    "titre": "CAS 1 — La base de données achetée",
                    "scenario": (
                        "Sami (startup EdTech Tunis) doit utiliser une base de 5 000 contacts "
                        "achetée sur internet pour une campagne HubSpot AI. "
                        "Ces personnes n'ont donné aucun consentement."
                    ),
                    "question": "Que devrait faire Sami ?",
                    "options": [
                        "A) Suivre les instructions du manager sans poser de questions",
                        "B) Utiliser la base mais envoyer uniquement des emails informatifs",
                        "C) Refuser, expliquer les risques légaux et proposer une alternative avec consentement",
                        "D) Utiliser la base pour les prospects B2B uniquement",
                    ],
                    "correct": "C",
                    "explication": "Utiliser une base sans consentement est illégal (Tunisie : loi 2004-63). Sami doit refuser et proposer des alternatives légales.",
                },
                {
                    "id": 2,
                    "titre": "CAS 2 — La personnalisation trop intrusive",
                    "scenario": (
                        "Nour (assurance Casablanca) détecte via AI que M. Benali traverse un divorce. "
                        "L'outil suggère d'utiliser cette info pour personnaliser l'email d'assurance vie."
                    ),
                    "question": "Que devrait faire Nour ?",
                    "options": [
                        "A) Utiliser la suggestion — c'est de la personnalisation avancée",
                        "B) Refuser d'utiliser cette information sensible, envoyer un email standard",
                        "C) Utiliser l'information mais de façon plus subtile",
                        "D) Demander d'abord à M. Benali s'il veut être contacté",
                    ],
                    "correct": "B",
                    "explication": "Exploiter des informations personnelles sensibles sans consentement est une violation grave de la vie privée.",
                },
                {
                    "id": 3,
                    "titre": "CAS 3 — L'AI qui 'ment'",
                    "scenario": (
                        "Yasmine (agence immobilière Dubai) doit programmer son chatbot AI "
                        "pour se présenter comme 'Yasmine, votre conseillère personnelle' "
                        "sans préciser que c'est une AI."
                    ),
                    "question": "Quelle est la bonne décision ?",
                    "options": [
                        "A) Suivre la demande — les clients préfèrent parler à un humain",
                        "B) Configurer le chatbot comme 'Yasmine AI, assistante virtuelle' en précisant qu'un humain prend le relais",
                        "C) Désactiver le chatbot et répondre manuellement",
                        "D) Laisser l'AI répondre sans se présenter",
                    ],
                    "correct": "B",
                    "explication": "Se faire passer pour un humain est une tromperie. La transparence renforce la confiance à long terme.",
                },
            ],
            "consigne_globale": (
                "Pour chaque cas : (1) lisez le scénario, (2) choisissez votre réponse, "
                "(3) justifiez en minimum 3 lignes, (4) répondez à 1 point de discussion."
            ),
            "livrable": "Document avec vos 3 analyses. Commentez la réponse d'un autre apprenant sur le forum.",
        },
        hints_fr=[
            {"level": 1, "text": "3 questions clés : (1) Le prospect a-t-il consenti ? (2) Seriez-vous à l'aise si le prospect savait ? (3) Cette pratique crée-t-elle de la valeur ou exploite-t-elle une faiblesse ?"},
            {"level": 2, "text": "L'éthique AI est un avantage concurrentiel en MENA — la confiance est la monnaie principale de l'échange commercial."},
        ],
    ))
    db.flush()

    # ════════════════════════════════════════════════════════════════════════
    # UNITÉ 1 — AUTOMATISER SA PROSPECTION
    # ════════════════════════════════════════════════════════════════════════

    u2_1 = Unit(
        module_id=m2.id, order=1,
        title_fr="Automatiser sa prospection",
        title_en="Automating Prospection",
        description_fr="Créer des séquences d'emails automatiques et des workflows de relance.",
        description_en="Create automatic email sequences and follow-up workflows.",
        estimated_duration_min=82,
    )
    db.add(u2_1); db.flush()

    # ── Leçon 1.1 ────────────────────────────────────────────────────────────
    l2_1_1 = Lesson(
        unit_id=u2_1.id, order=1,
        title_fr="Les séquences d'emails automatiques",
        title_en="Automatic email sequences",
        format="video", difficulty_level=3, estimated_duration_min=12,
        description_fr="Définition d'une séquence, anatomie en 5 étapes, timing optimal MENA, démo HubSpot Sequences.",
        description_en="Sequence definition, 5-step anatomy, optimal MENA timing, HubSpot Sequences demo.",
    )
    db.add(l2_1_1); db.flush()

    db.add(Activity(
        lesson_id=l2_1_1.id, order=1, type="video",
        title_fr="Vidéo — Les séquences d'emails automatiques",
        title_en="Video — Automatic email sequences",
        is_assessed=False, is_required=True,
        content_fr={"duration_min": 12, "url_fr": None},
    ))
    db.add(Activity(
        lesson_id=l2_1_1.id, order=2, type="quiz",
        title_fr="Quiz — Séquences d'emails automatiques",
        title_en="Quiz — Automatic email sequences",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "questions": [
                {
                    "id": 1,
                    "question": "Vous créez une séquence d'emails pour des prospects B2B tunisiens. Quel timing est le plus adapté ?",
                    "options": [
                        "A) Email 1 (Jour 1), Email 2 (Jour 2), Email 3 (Jour 3) — rythme quotidien",
                        "B) Email 1 (Jour 1), Email 2 (Jour 4), Email 3 (Jour 10) — rythme progressif",
                        "C) Envoyer tous les emails le même jour pour maximiser l'impact",
                        "D) Attendre que le prospect réponde avant d'envoyer le suivant",
                    ],
                    "correct": "B",
                    "explanation": "Un rythme progressif respecte le prospect et évite d'être perçu comme du spam. En MENA, les relances trop rapprochées sont contre-productives.",
                },
                {
                    "id": 2,
                    "question": "Votre séquence a un taux d'ouverture de 60% (email 1), 40% (email 2), 25% (email 3), 15% (email 4). Que faire ?",
                    "options": [
                        "A) Tout garder — les chiffres sont normaux",
                        "B) Analyser pourquoi le taux chute après l'email 2 et optimiser l'objet et le contenu des emails 3 et 4",
                        "C) Supprimer les emails 3 et 4 qui ont peu d'impact",
                        "D) Augmenter la fréquence d'envoi pour compenser",
                    ],
                    "correct": "B",
                    "explanation": "Une chute brutale signale un problème de pertinence ou de timing. L'AI Sales Specialist analyse et optimise en continu.",
                },
                {
                    "id": 3,
                    "question": "Un prospect ouvre votre email mais ne répond pas. L'AI suggère de continuer la séquence. Que faites-vous ?",
                    "options": [
                        "A) Continuer la séquence automatiquement sans intervenir",
                        "B) Analyser quel lien il a cliqué et personnaliser manuellement le prochain email en fonction de son intérêt détecté",
                        "C) Arrêter la séquence — il n'est pas intéressé",
                        "D) L'appeler immédiatement",
                    ],
                    "correct": "B",
                    "explanation": "Un prospect qui ouvre mais ne répond pas est intéressé mais pas encore prêt. L'AI + jugement humain fait la différence.",
                },
                {
                    "id": 4,
                    "question": "Quel est le nombre d'emails recommandé dans une séquence de prospection froide B2B pour le marché MENA ?",
                    "options": [
                        "A) 1 à 2 emails — ne pas insister",
                        "B) 3 à 5 emails — suffisant pour créer le contact sans harceler",
                        "C) 10 à 15 emails — la persévérance paye toujours",
                        "D) Autant que nécessaire jusqu'à obtenir une réponse",
                    ],
                    "correct": "B",
                    "explanation": "3 à 5 emails bien espacés est le standard MENA. Au-delà, le risque de spam augmente et la réputation se dégrade.",
                },
            ],
            "passing_score": 70,
        },
        hints_fr=[
            {"level": 1, "text": "Une séquence efficace apporte de la valeur à chaque étape — elle ne harcèle pas."},
            {"level": 2, "text": "En MENA, évitez les envois le vendredi après-midi et pendant Ramadan."},
        ],
    ))
    db.flush()

    # ── Leçon 1.2 ────────────────────────────────────────────────────────────
    l2_1_2 = Lesson(
        unit_id=u2_1.id, order=2,
        title_fr="Automatiser les relances commerciales",
        title_en="Automate follow-ups",
        format="video", difficulty_level=3, estimated_duration_min=10,
        description_fr="Triggers de relance intelligents, 4 types de relances, règles HubSpot, éviter les pièges du spam.",
        description_en="Smart follow-up triggers, 4 types of follow-ups, HubSpot automation rules, avoiding spam pitfalls.",
        prerequisite_lesson_id=l2_1_1.id,
    )
    db.add(l2_1_2); db.flush()

    db.add(Activity(
        lesson_id=l2_1_2.id, order=1, type="video",
        title_fr="Vidéo — Automatiser les relances commerciales",
        is_assessed=False, is_required=True,
        content_fr={"duration_min": 10, "url_fr": None},
    ))
    db.add(Activity(
        lesson_id=l2_1_2.id, order=2, type="exercise",
        title_fr="Exercice — Concevoir mon workflow de relance automatique",
        title_en="Exercise — Design my automatic follow-up workflow",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": (
                "Étape 1 — Définir vos triggers\n"
                "Listez 3 événements déclencheurs pertinents (ouverture d'email, visite page tarifs, inactivité X jours).\n\n"
                "Étape 2 — Cartographier le workflow\n"
                "Pour chaque trigger : (1) action déclenchée, (2) délai, (3) canal (email / notification / tâche manuelle).\n\n"
                "Étape 3 — Rédiger 2 emails de relance avec ChatGPT\n"
                "(1) prospect qui a ouvert sans répondre, (2) prospect inactif depuis 14 jours. Personnalisez pour le marché MENA.\n\n"
                "Étape 4 — Configurer dans HubSpot\n"
                "Mettez en place au moins 1 workflow et soumettez une capture d'écran."
            ),
            "livrable": "Tableau des triggers, schéma du workflow, 2 emails de relance, capture d'écran HubSpot.",
            "criteres": {
                "pertinence_triggers": "25%",
                "logique_workflow": "25%",
                "qualite_emails_relance": "35%",
                "implementation_hubspot": "15%",
            },
            "duree_estimee": "45 à 60 minutes",
        },
        hints_fr=[
            {"level": 1, "text": "Commencez par les triggers les plus simples : ouverture sans réponse après 3 jours, visite page tarifs sans contact."},
            {"level": 2, "text": "Dans HubSpot : Automatisation > Workflows > Créer un workflow > Basé sur les contacts."},
            {"level": 3, "text": "Pour la relance après silence, apportez une nouvelle valeur : 'J'ai pensé à vous en lisant cet article sur [secteur]...'"},
        ],
        rubric_fr={"criteres": [
            {"nom": "Pertinence des triggers", "poids": 0.25, "description": "3 triggers réalistes, pertinents MENA, exploitables dans HubSpot."},
            {"nom": "Logique du workflow", "poids": 0.25, "description": "Workflow cohérent, délais adaptés MENA, actions proportionnelles."},
            {"nom": "Qualité des emails de relance", "poids": 0.35, "description": "2 emails apportant une valeur nouvelle, personnalisés culturellement."},
            {"nom": "Implémentation HubSpot", "poids": 0.15, "description": "Au moins 1 workflow créé avec capture d'écran valide."},
        ]},
    ))
    db.flush()

    # ── Leçon 1.3 ────────────────────────────────────────────────────────────
    l2_1_3 = Lesson(
        unit_id=u2_1.id, order=3,
        title_fr="Ma première campagne automatisée",
        title_en="My first automated campaign",
        format="exercise", difficulty_level=3, estimated_duration_min=60,
        description_fr="Projet intégrateur : construire et lancer une campagne de prospection automatisée complète avec HubSpot.",
        description_en="Integrative project: build and launch a complete automated prospection campaign with HubSpot.",
        prerequisite_lesson_id=l2_1_2.id,
    )
    db.add(l2_1_3); db.flush()

    db.add(Activity(
        lesson_id=l2_1_3.id, order=1, type="exercise",
        title_fr="Projet — Ma première campagne automatisée complète",
        title_en="Project — My first complete automated campaign",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": (
                "Phase 1 — Définition (15 min)\n"
                "Choisissez un segment cible précis. Définissez objectif, nombre de prospects (min 10), produit/service, durée.\n\n"
                "Phase 2 — Contenu (30 min)\n"
                "Rédigez avec ChatGPT 3 emails : Email 1 (J1) valeur ajoutée, Email 2 (J5) preuve sociale MENA, Email 3 (J12) CTA fort.\n\n"
                "Phase 3 — Configuration HubSpot (15 min)\n"
                "Créez la séquence, configurez les délais, importez 5 contacts minimum, activez le suivi.\n\n"
                "Phase 4 — Lancement et analyse\n"
                "Testez sur 2-3 contacts si possible. Sinon, définissez les KPIs et seuils de succès."
            ),
            "livrable": "Fiche campagne + 3 emails + captures HubSpot + tableau KPIs.",
            "criteres": {
                "definition_segment": "15%",
                "qualite_sequence_emails": "35%",
                "configuration_hubspot": "25%",
                "pilotage_kpis": "25%",
            },
            "score_minimum": 70,
            "duree_estimee": "60 à 90 minutes",
        },
        hints_fr=[
            {"level": 1, "text": "Un segment très précis (10 prospects qualifiés) donne de meilleurs résultats qu'une campagne générique sur 100."},
            {"level": 2, "text": "Email 2 (preuve sociale) : '[Entreprise similaire] a utilisé [votre solution] et a obtenu [résultat] en [durée].'"},
            {"level": 3, "text": "KPIs MENA : taux d'ouverture > 35%, taux de clic > 5%, taux de réponse > 3%, conversion RDV > 1%."},
        ],
        rubric_fr={"criteres": [
            {"nom": "Définition du segment", "poids": 0.15, "description": "Segment précis, réaliste, objectifs mesurables."},
            {"nom": "Qualité de la séquence d'emails", "poids": 0.35, "description": "3 emails distincts avec valeur progressive, personnalisés MENA, CTA clair."},
            {"nom": "Configuration HubSpot", "poids": 0.25, "description": "Séquence créée, délais configurés, contacts importés, suivi activé."},
            {"nom": "Pilotage des KPIs", "poids": 0.25, "description": "KPIs pertinents avec seuils réalistes pour le marché MENA."},
        ]},
    ))
    db.flush()

    # ════════════════════════════════════════════════════════════════════════
    # UNITÉ 2 — ANALYSER LES DONNÉES CLIENTS
    # ════════════════════════════════════════════════════════════════════════

    u2_2 = Unit(
        module_id=m2.id, order=2,
        title_fr="Analyser les données clients",
        title_en="Analysing Customer Data",
        description_fr="Lire les insights AI, prédire les comportements d'achat, décisions data-driven.",
        description_en="Read AI insights, predict buying behaviours, data-driven decisions.",
        estimated_duration_min=65,
    )
    db.add(u2_2); db.flush()

    # ── Leçon 2.1 ────────────────────────────────────────────────────────────
    l2_2_1 = Lesson(
        unit_id=u2_2.id, order=1,
        title_fr="Lire et interpréter les insights AI",
        title_en="Reading AI insights",
        format="video", difficulty_level=3, estimated_duration_min=10,
        description_fr="Types d'insights, lecture tableau de bord HubSpot AI, 5 métriques clés, pièges d'interprétation.",
        description_en="Types of insights, HubSpot AI dashboard, 5 key metrics, interpretation pitfalls.",
    )
    db.add(l2_2_1); db.flush()

    db.add(Activity(
        lesson_id=l2_2_1.id, order=1, type="video",
        title_fr="Vidéo — Lire et interpréter les insights AI",
        is_assessed=False, is_required=True,
        content_fr={"duration_min": 10, "url_fr": None},
    ))
    db.add(Activity(
        lesson_id=l2_2_1.id, order=2, type="quiz",
        title_fr="Quiz — Interpréter les insights AI",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "questions": [
                {
                    "id": 1,
                    "question": "HubSpot AI montre : 'Taux de conversion Pipeline : 12%'. Qu'est-ce que cela signifie ?",
                    "options": [
                        "A) 12% de vos emails sont ouverts",
                        "B) 12 prospects sur 100 qui entrent dans votre pipeline deviennent des clients",
                        "C) Vous avez perdu 12% de vos clients ce mois",
                        "D) Votre taux de réponse aux emails est de 12%",
                    ],
                    "correct": "B",
                    "explanation": "Le taux de conversion pipeline mesure combien de prospects entrant dans le processus de vente finissent par acheter. La moyenne B2B MENA est entre 8% et 20%.",
                },
                {
                    "id": 2,
                    "question": "L'AI prédit : 'Probabilité d'atteindre l'objectif mensuel : 65%'. Nous sommes le 10 du mois. Que faites-vous ?",
                    "options": [
                        "A) Ne rien faire — 65% c'est acceptable",
                        "B) Attendre la fin du mois",
                        "C) Identifier immédiatement les deals à 60-80% de probabilité et les activer en priorité",
                        "D) Demander à l'AI de changer sa prédiction",
                    ],
                    "correct": "C",
                    "explanation": "65% au début du mois = signal d'alerte. Il faut agir maintenant. Les deals à 60-80% sont les plus actionnables.",
                },
                {
                    "id": 3,
                    "question": "Votre taux d'ouverture est passé de 45% à 22% ce mois. Quelle est la première chose à analyser ?",
                    "options": [
                        "A) Le nombre total d'emails envoyés",
                        "B) La qualité de votre connexion internet",
                        "C) Si vos emails sont en spam, si l'objet a changé, si le segment a changé",
                        "D) Si HubSpot a un bug d'affichage",
                    ],
                    "correct": "C",
                    "explanation": "Une chute brutale signale 3 causes possibles : délivrabilité dégradée, changement d'objet, segment moins qualifié. Diagnostiquer avant d'agir.",
                },
                {
                    "id": 4,
                    "question": "80% de vos ventes viennent de 20% de vos prospects. Quelle décision prenez-vous ?",
                    "options": [
                        "A) Traiter tous les prospects de la même façon pour être équitable",
                        "B) Concentrer 80% de votre temps et de l'effort AI sur ces 20% à fort potentiel",
                        "C) Arrêter de prospecter les 80% restants définitivement",
                        "D) Doubler le volume global de prospection",
                    ],
                    "correct": "B",
                    "explanation": "Principe de Pareto appliqué à la vente AI. Identifier votre ICP dans les données et concentrer l'effort sur ce profil est la stratégie la plus efficace.",
                },
            ],
            "passing_score": 70,
        },
        hints_fr=[
            {"level": 1, "text": "Les insights AI sont des signaux, pas des certitudes. Ils guident votre action mais ne remplacent pas votre jugement."},
            {"level": 2, "text": "5 métriques clés : taux d'ouverture, taux de clic, taux de conversion pipeline, vélocité des deals, score moyen des leads."},
        ],
    ))
    db.flush()

    # ── Leçon 2.2 ────────────────────────────────────────────────────────────
    l2_2_2 = Lesson(
        unit_id=u2_2.id, order=2,
        title_fr="Prédire les comportements d'achat",
        title_en="Predict buying behaviours",
        format="video", difficulty_level=3, estimated_duration_min=10,
        description_fr="Signaux d'achat détectables par l'AI, modèles prédictifs, cas pratique prospect chaud.",
        description_en="AI-detectable buying signals, predictive models, hot prospect case study.",
        prerequisite_lesson_id=l2_2_1.id,
    )
    db.add(l2_2_2); db.flush()

    db.add(Activity(
        lesson_id=l2_2_2.id, order=1, type="video",
        title_fr="Vidéo — Prédire les comportements d'achat",
        is_assessed=False, is_required=True,
        content_fr={"duration_min": 10, "url_fr": None},
    ))
    db.add(Activity(
        lesson_id=l2_2_2.id, order=2, type="exercise",
        title_fr="Exercice — Analyser les signaux d'achat de mes prospects",
        title_en="Exercise — Analyse buying signals from my prospects",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": (
                "Tâche 1 — Audit prospects chauds\n"
                "Filtrez dans HubSpot les contacts avec score AI > 70. "
                "Pour les 5 premiers : score AI, dernière activité, étape pipeline, temps depuis dernier contact.\n\n"
                "Tâche 2 — Classement par priorité\n"
                "Classez en 3 niveaux : Rouge (action immédiate), Orange (48h), Vert (nurturing auto). Justifiez par les données.\n\n"
                "Tâche 3 — Plan d'action\n"
                "Pour vos 2 prospects Rouge : canal, message, heure. Utilisez ChatGPT pour rédiger si c'est un email."
            ),
            "livrable": "Tableau 5 prospects + classement justifié + plan d'action pour les 2 prospects rouges.",
            "criteres": {
                "lecture_donnees_hubspot": "30%",
                "pertinence_classement": "35%",
                "qualite_plan_action": "35%",
            },
            "duree_estimee": "35 à 45 minutes",
        },
        hints_fr=[
            {"level": 1, "text": "HubSpot : Contacts > Filtrer > Score du contact > supérieur à 70."},
            {"level": 2, "text": "Signaux forts = action immédiate : visite page tarifs, téléchargement catalogue, 3+ ouvertures en 7 jours, demande de démo."},
        ],
        rubric_fr={"criteres": [
            {"nom": "Lecture des données HubSpot", "poids": 0.30, "description": "Données correctement extraites pour les 5 prospects."},
            {"nom": "Pertinence du classement", "poids": 0.35, "description": "Classement Rouge/Orange/Vert cohérent avec les signaux et bien justifié."},
            {"nom": "Qualité du plan d'action", "poids": 0.35, "description": "Actions concrètes, immédiates, personnalisées et exploitables."},
        ]},
    ))
    db.flush()

    # ── Leçon 2.3 — ✅ Titre harmonisé ───────────────────────────────────────
    l2_2_3 = Lesson(
        unit_id=u2_2.id, order=3,
        title_fr="Décisions data-driven — Cas TechServ Tunisie",  # ✅ harmonisé
        title_en="Data-driven decisions — TechServ case",
        format="case_study", difficulty_level=4, estimated_duration_min=45,
        description_fr="Cas réel d'une PME tunisienne qui a transformé ses résultats grâce à l'analyse AI.",
        description_en="Real case of a Tunisian SME that transformed its sales results through AI analysis.",
        prerequisite_lesson_id=l2_2_2.id,
    )
    db.add(l2_2_3); db.flush()

    db.add(Activity(
        lesson_id=l2_2_3.id, order=1, type="case_study",
        title_fr="Cas TechServ — Décisions data-driven dans une PME tunisienne",
        title_en="TechServ case — Data-driven decisions in a Tunisian SME",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "contexte": (
                "TechServ est une PME tunisienne de 15 salariés spécialisée dans "
                "la maintenance informatique pour les PME industrielles. "
                "CA : 450 000 TND/an. Objectif : 600 000 TND l'année suivante."
            ),
            "situation": (
                "Après 3 mois HubSpot AI, le tableau de bord révèle :\n"
                "- 65% des ventes = 20% des clients (textile + agro)\n"
                "- Conversion prospects froids : 3% / Conversion référés : 34%\n"
                "- 40% des deals bloqués depuis > 30 jours\n"
                "- Emails envoyés le mardi matin : 2x plus de réponses\n"
                "- 3 meilleurs commerciaux : 60% du temps en tâches administratives"
            ),
            "questions": [
                {
                    "id": 1,
                    "question": "Quelle est la décision stratégique la plus importante que Mohamed devrait prendre en priorité ?",
                    "consigne": "Répondez en minimum 5 lignes, justifiez avec les chiffres du cas.",
                    "pistes": ["Quel segment a le meilleur ROI ?", "Quelle source de leads est la plus efficace ?"],
                },
                {
                    "id": 2,
                    "question": "Les 40% de deals bloqués depuis 30 jours représentent un manque à gagner. Proposez une stratégie pour les débloquer avec l'AI.",
                    "consigne": "Décrivez 3 actions concrètes avec les outils AI à utiliser.",
                },
                {
                    "id": 3,
                    "question": "Comment utiliseriez-vous la donnée 'mardi matin x2 de réponses' pour optimiser la stratégie de communication ?",
                    "consigne": "Proposez un plan d'action pour les 30 prochains jours.",
                },
                {
                    "id": 4,
                    "question": "Les commerciaux passent 60% de leur temps en tâches administratives. Quelles automatisations proposez-vous ?",
                    "consigne": "Listez 4 automatisations prioritaires avec l'outil AI recommandé pour chacune.",
                },
            ],
            "conclusion": "Rédigez une synthèse de 10 lignes : vos 3 recommandations prioritaires pour aider TechServ à atteindre 600 000 TND.",
        },
        hints_fr=[
            {"level": 1, "text": "Identifiez les chiffres les plus frappants — ils pointent vers les décisions prioritaires."},
            {"level": 2, "text": "Le ratio 3% vs 34% est le signal le plus fort — la stratégie de référencement client est probablement la clé."},
        ],
    ))
    db.flush()

    # ════════════════════════════════════════════════════════════════════════
    # UNITÉ 3 — PERSONNALISER À GRANDE ÉCHELLE
    # ════════════════════════════════════════════════════════════════════════

    u2_3 = Unit(
        module_id=m2.id, order=3,
        title_fr="Personnaliser à grande échelle",
        title_en="Personalising at Scale",
        description_fr="Personnalisation de masse avec l'AI, adaptation au contexte Afrique du Nord, campagnes multi-segments.",
        description_en="Mass personalisation with AI, North Africa context adaptation, multi-segment campaigns.",
        estimated_duration_min=112,
    )
    db.add(u2_3); db.flush()

    # ── Leçon 3.1 ────────────────────────────────────────────────────────────
    l2_3_1 = Lesson(
        unit_id=u2_3.id, order=1,
        title_fr="La personnalisation de masse avec l'AI",
        title_en="Mass personalisation with AI",
        format="video", difficulty_level=3, estimated_duration_min=12,
        description_fr="Tokens de personnalisation, segmentation dynamique, variables intelligentes HubSpot.",
        description_en="Personalisation tokens, dynamic segmentation, HubSpot smart variables.",
    )
    db.add(l2_3_1); db.flush()

    db.add(Activity(
        lesson_id=l2_3_1.id, order=1, type="video",
        title_fr="Vidéo — La personnalisation de masse avec l'AI",
        is_assessed=False, is_required=True,
        content_fr={"duration_min": 12, "url_fr": None},
    ))
    db.add(Activity(
        lesson_id=l2_3_1.id, order=2, type="quiz",
        title_fr="Quiz — Personnalisation de masse",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "questions": [
                {
                    "id": 1,
                    "question": "Quelle est la différence entre personnalisation basique et personnalisation intelligente avec l'AI ?",
                    "options": [
                        "A) La personnalisation basique utilise le prénom, l'AI ne change rien d'autre",
                        "B) La basique insère le prénom et l'entreprise ; l'AI adapte le contenu, l'offre et le timing selon le comportement réel",
                        "C) Seule la personnalisation AI est efficace — la basique ne sert à rien",
                        "D) Il n'y a pas de différence significative",
                    ],
                    "correct": "B",
                    "explanation": "La personnalisation intelligente adapte le message selon les comportements réels du prospect — bien au-delà du simple prénom.",
                },
                {
                    "id": 2,
                    "question": "Vous avez 300 prospects dans 4 secteurs. Comment l'AI aide à personnaliser à cette échelle ?",
                    "options": [
                        "A) En envoyant le même email à tous avec juste le prénom changé",
                        "B) En écrivant 300 emails différents manuellement",
                        "C) En créant 4 templates sectoriels avec variables dynamiques, l'AI adaptant le contenu selon le segment",
                        "D) En sélectionnant les 50 meilleurs prospects seulement",
                    ],
                    "correct": "C",
                    "explanation": "La personnalisation à grande échelle = segmentation + variables dynamiques. 4 templates, HubSpot AI remplit automatiquement les variables.",
                },
                {
                    "id": 3,
                    "question": "Votre email personnalisé AI a un taux de clic de 8% vs 2% pour le générique. Quelle est la principale raison ?",
                    "options": [
                        "A) L'email personnalisé est plus long donc plus convaincant",
                        "B) L'email personnalisé contient plus de liens",
                        "C) Le prospect perçoit une pertinence directe — le contenu répond à son besoin spécifique",
                        "D) L'AI optimise automatiquement le code HTML",
                    ],
                    "correct": "C",
                    "explanation": "La pertinence perçue est le moteur de l'engagement. Un prospect qui voit ses enjeux reflétés est 3 à 4x plus susceptible de cliquer.",
                },
            ],
            "passing_score": 70,
        },
        hints_fr=[
            {"level": 1, "text": "La personnalisation intelligente répond à : 'Pourquoi ce message, pour cette personne, à ce moment précis ?'"},
        ],
    ))
    db.flush()

    # ── Leçon 3.2 ────────────────────────────────────────────────────────────
    l2_3_2 = Lesson(
        unit_id=u2_3.id, order=2,
        title_fr="Adapter les messages au contexte MENA",
        title_en="Adapt messages to the MENA context",
        format="video", difficulty_level=3, estimated_duration_min=10,
        description_fr="Différences Maghreb vs Golfe, personnalisation saisonnière Ramadan, langues et registres.",
        description_en="Maghreb vs Gulf differences, Ramadan seasonal personalisation, languages and registers.",
        prerequisite_lesson_id=l2_3_1.id,
    )
    db.add(l2_3_2); db.flush()

    db.add(Activity(
        lesson_id=l2_3_2.id, order=1, type="video",
        title_fr="Vidéo — Adapter les messages au contexte MENA",
        is_assessed=False, is_required=True,
        content_fr={"duration_min": 10, "url_fr": None},
    ))
    db.add(Activity(
        lesson_id=l2_3_2.id, order=2, type="exercise",
        title_fr="Exercice — Créer ma bibliothèque de templates MENA",
        title_en="Exercise — Build my MENA template library",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": (
                "Créez 4 templates d'emails adaptés :\n\n"
                "Template 1 — Tunisie B2B (français) : PME industrielle, ton cordial et professionnel.\n"
                "Template 2 — Maroc B2B (français formel) : entreprise moyenne, respect hiérarchie.\n"
                "Template 3 — Période Ramadan (MENA universel) : timing iftar, ton respectueux.\n"
                "Template 4 — Golfe (anglais ou arabe) : très professionnel, concis, orienté ROI.\n\n"
                "Pour chaque template : prompt ChatGPT utilisé + email généré + 3 adaptations culturelles justifiées."
            ),
            "livrable": "4 templates avec prompt, email généré, et 3 adaptations culturelles justifiées pour chacun.",
            "criteres": {
                "pertinence_culturelle": "45%",
                "qualite_prompts": "25%",
                "qualite_redaction": "30%",
            },
            "duree_estimee": "45 à 60 minutes",
        },
        hints_fr=[
            {"level": 1, "text": "Pour Ramadan : 'Respecte le caractère sacré du mois, adapte le timing (envoi après iftar), évite tout vocabulaire trop commercial.'"},
            {"level": 2, "text": "Maghreb = relation avant transaction, FR/AR. Golfe = décision rapide, ROI en premier, EN/AR, très formel."},
        ],
        rubric_fr={"criteres": [
            {"nom": "Pertinence culturelle", "poids": 0.45, "description": "Chaque template reflète authentiquement les codes culturels du contexte cible."},
            {"nom": "Qualité des prompts", "poids": 0.25, "description": "Les prompts incluent le contexte culturel, le ton et les contraintes spécifiques."},
            {"nom": "Qualité de rédaction", "poids": 0.30, "description": "4 templates professionnels, sans fautes, avec structure claire et CTA adapté."},
        ]},
    ))
    db.flush()

    # ── Leçon 3.3 ────────────────────────────────────────────────────────────
    l2_3_3 = Lesson(
        unit_id=u2_3.id, order=3,
        title_fr="Ma campagne personnalisée MENA",
        title_en="My personalised MENA campaign",
        format="exercise", difficulty_level=4, estimated_duration_min=90,
        description_fr="Projet intégrateur avancé : campagne multi-segments MENA avec personnalisation dynamique.",
        description_en="Advanced integrative project: multi-segment MENA campaign with dynamic personalisation.",
        prerequisite_lesson_id=l2_3_2.id,
    )
    db.add(l2_3_3); db.flush()

    db.add(Activity(
        lesson_id=l2_3_3.id, order=1, type="exercise",
        title_fr="Projet — Campagne personnalisée MENA multi-segments",
        title_en="Project — Multi-segment personalised MENA campaign",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": (
                "Phase 1 — Segmentation (20 min) : définissez 2 segments MENA distincts avec profil, enjeux, argument de vente, ton/langue.\n\n"
                "Phase 2 — Contenu (40 min) : pour chaque segment, créez 3 emails (J1 contact, J5 valeur+cas client, J12 closing).\n\n"
                "Phase 3 — Configuration HubSpot (20 min) : 2 listes segmentées, 2 séquences distinctes, personnalisation dynamique.\n\n"
                "Phase 4 — Pilotage (10 min) : KPIs attendus, fréquence analyse, critères de succès, ajustements prévus."
            ),
            "livrable": "Fiches 2 segments + 6 emails + captures HubSpot + tableau de bord prévisionnel.",
            "criteres": {
                "qualite_segmentation": "20%",
                "pertinence_emails_par_segment": "40%",
                "configuration_hubspot": "20%",
                "rigueur_pilotage": "20%",
            },
            "score_minimum": 70,
            "duree_estimee": "90 minutes",
        },
        hints_fr=[
            {"level": 1, "text": "Les 2 segments doivent être suffisamment différents — si vous pourriez envoyer le même email aux deux, ils ne sont pas assez différenciés."},
            {"level": 2, "text": "Pour l'Email 2 : 'Une PME similaire à Sfax a utilisé [solution] et a obtenu [résultat] en [durée].' La spécificité géographique augmente la crédibilité."},
        ],
        rubric_fr={"criteres": [
            {"nom": "Qualité de la segmentation", "poids": 0.20, "description": "2 segments distincts, précis, avec profil et enjeux bien définis."},
            {"nom": "Pertinence des emails par segment", "poids": 0.40, "description": "6 emails vraiment différents, personnalisation au-delà du prénom."},
            {"nom": "Configuration HubSpot", "poids": 0.20, "description": "2 séquences distinctes avec personnalisation dynamique activée."},
            {"nom": "Rigueur du pilotage", "poids": 0.20, "description": "KPIs définis par segment avec seuils réalistes et plan de réaction."},
        ]},
    ))
    db.flush()

    # ════════════════════════════════════════════════════════════════════════
    # UNITÉ 4 — OUTILS AI AVANCÉS
    # ════════════════════════════════════════════════════════════════════════

    u2_4 = Unit(
        module_id=m2.id, order=4,
        title_fr="Outils AI avancés",
        title_en="Advanced AI Tools",
        description_fr="HubSpot AI en profondeur, Zoho AI MENA, intégration ChatGPT-CRM.",
        description_en="HubSpot AI in depth, Zoho AI MENA, ChatGPT-CRM integration.",
        estimated_duration_min=69,
    )
    db.add(u2_4); db.flush()

    # ── Leçon 4.1 — ✅ Vidéo ajoutée + passing_score=0 ───────────────────────
    l2_4_1 = Lesson(
        unit_id=u2_4.id, order=1,
        title_fr="HubSpot AI en profondeur",
        title_en="HubSpot AI in depth",
        format="tutorial", difficulty_level=4, estimated_duration_min=12,
        description_fr="Fonctionnalités avancées : prédictions de closing, assistant rédaction AI, rapports personnalisés.",
        description_en="Advanced features: closing predictions, AI writing assistant, custom reports.",
    )
    db.add(l2_4_1); db.flush()

    # ✅ Activité 1 — Vidéo (ajoutée)
    db.add(Activity(
        lesson_id=l2_4_1.id, order=1, type="video",
        title_fr="Vidéo — HubSpot AI en profondeur : 6 fonctionnalités clés",
        title_en="Video — HubSpot AI in depth: 6 key features",
        is_assessed=False, is_required=True,
        content_fr={"duration_min": 12, "url_fr": None},
        content_en={"duration_min": 12, "url_en": None},
    ))
    # ✅ Activité 2 — Tutoriel (order décalé à 2, passing_score=0)
    db.add(Activity(
        lesson_id=l2_4_1.id, order=2, type="tutorial",
        title_fr="Tutoriel — HubSpot AI avancé : 6 fonctionnalités clés",
        title_en="Tutorial — Advanced HubSpot AI: 6 key features",
        is_assessed=True, is_required=True, passing_score=0,  # ✅ 0 car évaluation manuelle
        content_fr={
            "steps": [
                "Activer et configurer le scoring prédictif des leads (Sales Hub > Contacts > Score prédictif)",
                "Utiliser l'assistant AI pour rédiger des emails directement dans HubSpot (icône ✨ dans l'éditeur d'email)",
                "Créer un rapport personnalisé avec les métriques de performance AI (Rapports > Créer un rapport > Sales)",
                "Configurer les prédictions de closing sur les deals (Ventes > Deals > Prévisions)",
                "Mettre en place une liste active segmentée par comportement AI (Contacts > Listes > Liste active)",
                "Connecter HubSpot à ChatGPT via Zapier pour enrichir les fiches contacts automatiquement",
            ],
            "consigne": "Suivez les 6 étapes. Pour chaque étape : capture d'écran + 2 lignes sur l'utilité concrète.",
            "livrable": "6 captures d'écran + 6 commentaires (2 lignes chacun).",
            "criteres": {
                "completion_etapes": "60%",
                "pertinence_commentaires": "40%",
            },
        },
        hints_fr=[
            {"level": 1, "text": "Si certaines fonctionnalités sont verrouillées sur votre plan, décrivez leur usage et faites une capture de l'interface verrouillée."},
            {"level": 2, "text": "Zapier : Créer un Zap > Trigger HubSpot (Nouveau contact) > Action OpenAI (Créer un résumé du contact)."},
        ],
    ))
    db.flush()

    # ── Leçon 4.2 — ✅ Vidéo ajoutée ─────────────────────────────────────────
    l2_4_2 = Lesson(
        unit_id=u2_4.id, order=2,
        title_fr="Zoho AI pour le marché MENA",
        title_en="Zoho AI for MENA market",
        format="tutorial", difficulty_level=3, estimated_duration_min=12,
        description_fr="Zia (assistant AI de Zoho), scoring MENA adapté, avantages vs HubSpot pour les PME Maghreb.",
        description_en="Zia (Zoho AI assistant), adapted MENA scoring, advantages vs HubSpot for Maghreb SMEs.",
        prerequisite_lesson_id=l2_4_1.id,
    )
    db.add(l2_4_2); db.flush()

    # ✅ Activité 1 — Vidéo (ajoutée)
    db.add(Activity(
        lesson_id=l2_4_2.id, order=1, type="video",
        title_fr="Vidéo — Zoho AI pour le marché MENA",
        title_en="Video — Zoho AI for MENA market",
        is_assessed=False, is_required=True,
        content_fr={"duration_min": 10, "url_fr": None},
        content_en={"duration_min": 10, "url_en": None},
    ))
    # ✅ Activité 2 — Tutoriel (order décalé à 2)
    db.add(Activity(
        lesson_id=l2_4_2.id, order=2, type="tutorial",
        title_fr="Tutoriel comparatif — Zoho AI vs HubSpot AI pour le MENA",
        title_en="Comparative tutorial — Zoho AI vs HubSpot AI for MENA",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": (
                "Partie 1 — Explorez ou documentez les fonctionnalités AI de Zoho CRM : Zia, scoring, workflows, support arabe.\n\n"
                "Partie 2 — Tableau comparatif sur 8 critères : prix, facilité, scoring AI, support arabe/français, "
                "intégrations MENA, personnalisation, support client, PME vs ETI.\n\n"
                "Partie 3 — Recommandations par profil :\n"
                "Profil A : startup tech tunisienne, budget < 50$/mois, 3 commerciaux.\n"
                "Profil B : PME industrielle marocaine, 10 commerciaux, budget flexible.\n"
                "Profil C : filiale groupe du Golfe, 20 commerciaux, besoin arabe natif."
            ),
            "livrable": "Tableau comparatif 8 critères + 3 recommandations justifiées (min 5 lignes chacune).",
            "criteres": {
                "exhaustivite_tableau": "35%",
                "pertinence_recommandations": "45%",
                "qualite_argumentation": "20%",
            },
            "score_minimum": 70,
        },
        hints_fr=[
            {"level": 1, "text": "Sans compte Zoho : zoho.com/crm/zia-ai-features propose une démo complète des fonctionnalités AI."},
            {"level": 2, "text": "Zoho pour MENA : interface arabe native, prix DHS/TND, support client en arabe. HubSpot : écosystème plus large, plus d'intégrations."},
        ],
    ))
    db.flush()

    # ── Leçon 4.3 — ✅ Vidéo ajoutée ─────────────────────────────────────────
    l2_4_3 = Lesson(
        unit_id=u2_4.id, order=3,
        title_fr="Intégrer ChatGPT dans son CRM",
        title_en="Integrate ChatGPT into CRM",
        format="tutorial", difficulty_level=4, estimated_duration_min=45,
        description_fr="Connexion via Zapier/Make, enrichissement fiches contacts, résumés d'appels automatiques.",
        description_en="Connection via Zapier/Make, contact enrichment automation, automatic call summaries.",
        prerequisite_lesson_id=l2_4_2.id,
    )
    db.add(l2_4_3); db.flush()

    # ✅ Activité 1 — Vidéo (ajoutée)
    db.add(Activity(
        lesson_id=l2_4_3.id, order=1, type="video",
        title_fr="Vidéo — Intégrer ChatGPT dans son CRM via Zapier",
        title_en="Video — Integrate ChatGPT into your CRM via Zapier",
        is_assessed=False, is_required=True,
        content_fr={"duration_min": 12, "url_fr": None},
        content_en={"duration_min": 12, "url_en": None},
    ))
    # ✅ Activité 2 — Exercice (order décalé à 2)
    db.add(Activity(
        lesson_id=l2_4_3.id, order=2, type="exercise",
        title_fr="Projet — Intégrer ChatGPT dans mon workflow CRM",
        title_en="Project — Integrate ChatGPT into my CRM workflow",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": (
                "Étape 1 — Choisissez votre cas d'usage parmi :\n"
                "(A) Résumé automatique après chaque appel commercial\n"
                "(B) Enrichissement automatique des fiches contacts\n"
                "(C) Email de suivi automatique après chaque réunion\n"
                "(D) Suggestion de prochaine action pour les deals bloqués\n\n"
                "Étape 2 — Concevez le flux : Trigger + Action AI (prompt ChatGPT) + Output (où va le résultat dans le CRM).\n\n"
                "Étape 3 — Implémentez avec Zapier ou Make. Testez et soumettez captures d'écran.\n\n"
                "Étape 4 — Évaluez le gain de temps par semaine et calculez le gain annuel pour votre équipe."
            ),
            "livrable": "Description cas d'usage + schéma flux + captures Zapier/Make + exemple résultat + calcul gain de temps.",
            "criteres": {
                "pertinence_cas_usage": "20%",
                "logique_flux": "25%",
                "implementation_technique": "35%",
                "calcul_roi_temps": "20%",
            },
            "score_minimum": 70,
            "duree_estimee": "45 à 60 minutes",
        },
        hints_fr=[
            {"level": 1, "text": "Cas d'usage (C) le plus simple : trigger = nouvelle note HubSpot > ChatGPT résume > email de suivi créé."},
            {"level": 2, "text": "Zapier : New Zap > Trigger = HubSpot (Note créée) > Action = OpenAI (Send prompt) > Action = HubSpot (Envoyer email)."},
        ],
    ))
    db.flush()

    # ════════════════════════════════════════════════════════════════════════
    # UNITÉ 5 — ÉTHIQUE AI INTERMÉDIAIRE
    # ════════════════════════════════════════════════════════════════════════

    u2_5 = Unit(
        module_id=m2.id, order=5,
        title_fr="Éthique AI — Niveau Intermédiaire",
        title_en="AI Ethics — Intermediate Level",
        description_fr="Gestion responsable des données clients, éviter la manipulation avec l'AI.",
        description_en="Responsible client data management, avoiding manipulation with AI.",
        estimated_duration_min=42,
    )
    db.add(u2_5); db.flush()

    # ── Leçon 5.1 ────────────────────────────────────────────────────────────
    l2_5_1 = Lesson(
        unit_id=u2_5.id, order=1,
        title_fr="Gérer les données clients responsablement",
        title_en="Responsible data management",
        format="video", difficulty_level=3, estimated_duration_min=12,
        description_fr="RGPD et équivalents MENA, droits des prospects, durée conservation, politique confidentialité.",
        description_en="GDPR and MENA equivalents, prospect rights, data retention, privacy policy.",
    )
    db.add(l2_5_1); db.flush()

    db.add(Activity(
        lesson_id=l2_5_1.id, order=1, type="video",
        title_fr="Vidéo — Gérer les données clients responsablement",
        is_assessed=False, is_required=True,
        content_fr={"duration_min": 12, "url_fr": None},
    ))
    db.add(Activity(
        lesson_id=l2_5_1.id, order=2, type="quiz",
        title_fr="Quiz — Gestion responsable des données",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "questions": [
                {
                    "id": 1,
                    "question": "Un prospect demande : 'Supprimez toutes les données que vous avez sur moi.' Que faites-vous ?",
                    "options": [
                        "A) Ignorer la demande — il est dans votre CRM légalement",
                        "B) Supprimer uniquement son email de votre liste",
                        "C) Supprimer l'ensemble de ses données dans les 30 jours et confirmer par email",
                        "D) Lui demander de justifier sa demande avant d'agir",
                    ],
                    "correct": "C",
                    "explanation": "Le droit à l'effacement est fondamental dans les législations MENA (Tunisie loi 2004-63, Maroc loi 09-08, UAE PDPL 2022). Délai : 30 jours maximum.",
                },
                {
                    "id": 2,
                    "question": "Vous collectez des emails via un formulaire web. Quelle mention est obligatoire ?",
                    "options": [
                        "A) Aucune — les formulaires web ne nécessitent pas de mention légale",
                        "B) Juste une case 'J'accepte les conditions générales'",
                        "C) Une mention indiquant : comment les données seront utilisées, qui les traite, comment exercer ses droits",
                        "D) Le numéro de téléphone du responsable juridique",
                    ],
                    "correct": "C",
                    "explanation": "Le consentement éclairé requiert une information complète au moment de la collecte.",
                },
                {
                    "id": 3,
                    "question": "Combien de temps pouvez-vous conserver les données d'un prospect inactif depuis 2 ans ?",
                    "options": [
                        "A) Indéfiniment — il est dans votre base CRM",
                        "B) Maximum 3 ans en règle générale pour les prospects inactifs",
                        "C) Maximum 10 ans",
                        "D) Il n'y a pas de limite légale pour les données B2B",
                    ],
                    "correct": "B",
                    "explanation": "Le principe de limitation de conservation impose de ne pas garder des données plus longtemps que nécessaire. 3 ans est la norme MENA pour prospects inactifs.",
                },
                {
                    "id": 4,
                    "question": "Votre AI détecte des problèmes de trésorerie d'un prospect via LinkedIn. Pouvez-vous stocker cette info dans votre CRM ?",
                    "options": [
                        "A) Oui, si c'est une information publique sur LinkedIn",
                        "B) Oui, si c'est utile pour votre stratégie",
                        "C) Non — les données financières sensibles sans consentement explicite ne peuvent pas être stockées",
                        "D) Oui, si vous ne la partagez pas avec des tiers",
                    ],
                    "correct": "C",
                    "explanation": "Même publiques, les données sensibles ne peuvent pas être collectées sans consentement explicite pour un usage commercial.",
                },
                {
                    "id": 5,
                    "question": "Vous quittez votre entreprise. Pouvez-vous emporter la base de données clients ?",
                    "options": [
                        "A) Oui, si vous avez contribué à la constituer",
                        "B) Oui, pour vos contacts personnels que vous connaissiez avant",
                        "C) Non, la base clients appartient à l'entreprise et est protégée",
                        "D) Oui, si les clients vous donnent leur accord par SMS",
                    ],
                    "correct": "C",
                    "explanation": "La base clients est un actif de l'entreprise protégé par le secret des affaires. L'emporter est une violation légale grave dans tous les pays MENA.",
                },
            ],
            "passing_score": 70,
        },
        hints_fr=[
            {"level": 1, "text": "Règle de base : si vous n'êtes pas sûr, demandez-vous si le prospect a explicitement consenti à cet usage précis."},
            {"level": 2, "text": "4 droits fondamentaux des prospects : droit d'accès, rectification, effacement, opposition."},
        ],
    ))
    db.flush()

    # ── Leçon 5.2 ────────────────────────────────────────────────────────────
    l2_5_2 = Lesson(
        unit_id=u2_5.id, order=2,
        title_fr="Éviter la manipulation avec l'AI",
        title_en="Avoid manipulation with AI",
        format="case_study", difficulty_level=3, estimated_duration_min=30,
        description_fr="3 cas sur les frontières entre persuasion légitime et manipulation : dark patterns, urgence artificielle, profilage abusif.",
        description_en="3 case studies on the boundaries between legitimate persuasion and manipulation.",
        prerequisite_lesson_id=l2_5_1.id,
    )
    db.add(l2_5_2); db.flush()

    db.add(Activity(
        lesson_id=l2_5_2.id, order=1, type="case_study",
        title_fr="Cas pratiques — Persuasion vs Manipulation avec l'AI",
        title_en="Case studies — Persuasion vs Manipulation with AI",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "introduction": (
                "3 cas pour reconnaître et éviter les pratiques manipulatoires "
                "tout en restant un commercial efficace."
            ),
            "cas": [
                {
                    "id": 1,
                    "titre": "CAS 1 — L'urgence artificielle",
                    "scenario": (
                        "Karim (SaaS Tunis) envoie automatiquement : "
                        "'⚠️ OFFRE LIMITÉE : Nous n'avons plus que 2 places disponibles.' "
                        "En réalité, il n'y a pas de limite de places."
                    ),
                    "question": "Identifiez le problème éthique et proposez une alternative efficace ET éthique.",
                    "consigne": "(1) Analyse éthique en 3 lignes, (2) votre version de l'email alternatif éthique.",
                },
                {
                    "id": 2,
                    "titre": "CAS 2 — Le profilage psychologique non consenti",
                    "scenario": (
                        "Leila utilise un outil AI qui analyse les profils LinkedIn pour détecter "
                        "les traits DISC et adapter automatiquement le style de communication "
                        "pour ses 500 prospects sans les informer."
                    ),
                    "question": "Cette pratique est-elle éthique ? Où se situe la limite ?",
                    "consigne": "(1) Votre position avec justification (5 lignes min), (2) comment utiliser cet outil de façon éthique.",
                },
                {
                    "id": 3,
                    "titre": "CAS 3 — L'hyper-personnalisation intimidante",
                    "scenario": (
                        "Omar (Casablanca) écrit : 'J'ai remarqué que vous avez visité notre site "
                        "3 fois cette semaine, dont 2 fois depuis votre bureau et 1 fois depuis votre domicile.' "
                        "Monsieur Alami répond : 'Comment avez-vous ces informations ? Je suis choqué.'"
                    ),
                    "question": "Qu'a fait Omar de problématique ? Comment répondre à Alami ?",
                    "consigne": "(1) Analyse erreur d'Omar (3 lignes), (2) email de réponse à Alami, (3) version correcte de l'email original.",
                },
            ],
            "synthese": "Rédigez en 8 lignes votre charte personnelle 'IA et vente éthique' : les 5 principes que vous vous engagez à respecter.",
        },
        hints_fr=[
            {"level": 1, "text": "Test éthique : imaginez que votre prospect lit exactement ce que vous faites avec ses données. Seriez-vous à l'aise ?"},
            {"level": 2, "text": "Persuasion = montrer la valeur réelle au bon moment. Manipulation = exploiter les peurs ou biais pour forcer une décision."},
        ],
    ))
    db.flush()

    # ════════════════════════════════════════════════════════════════════════
    # UNITÉ 1 — STRATÉGIE AI SALES GLOBALE
    # ════════════════════════════════════════════════════════════════════════

    u3_1 = Unit(
        module_id=m3.id, order=1,
        title_fr="Stratégie AI Sales globale",
        title_en="Global AI Sales Strategy",
        description_fr="Construire, adapter et présenter une stratégie AI Sales complète pour le marché MENA.",
        description_en="Build, adapt and present a complete AI Sales strategy for the MENA market.",
        estimated_duration_min=117,
    )
    db.add(u3_1); db.flush()

    # ── Leçon 1.1 ────────────────────────────────────────────────────────────
    l3_1_1 = Lesson(
        unit_id=u3_1.id, order=1,
        title_fr="Construire sa stratégie AI Sales",
        title_en="Build your AI Sales strategy",
        format="video", difficulty_level=4, estimated_duration_min=15,
        description_fr="Les 5 piliers d'une stratégie AI Sales, diagnostic de maturité AI, feuille de route 90 jours.",
        description_en="5 pillars of an AI Sales strategy, AI maturity diagnostic, 90-day roadmap.",
    )
    db.add(l3_1_1); db.flush()

    db.add(Activity(
        lesson_id=l3_1_1.id, order=1, type="video",
        title_fr="Vidéo — Construire sa stratégie AI Sales",
        title_en="Video — Build your AI Sales strategy",
        is_assessed=False, is_required=True,
        content_fr={"duration_min": 15, "url_fr": None},
    ))
    db.add(Activity(
        lesson_id=l3_1_1.id, order=2, type="exercise",
        title_fr="Exercice stratégique — Mon diagnostic de maturité AI Sales",
        title_en="Strategic exercise — My AI Sales maturity diagnostic",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": (
                "Étape 1 — Diagnostic de maturité\n"
                "Évaluez sur 5 piliers (score 1 à 5) :\n"
                "Pilier 1 — Outils AI en place, Pilier 2 — Compétences équipe,\n"
                "Pilier 3 — Qualité des données, Pilier 4 — Processus automatisés,\n"
                "Pilier 5 — Culture data et adoption AI.\n"
                "Pour chaque pilier : score actuel, score cible 6 mois, lacune principale.\n\n"
                "Étape 2 — Quick wins\n"
                "3 actions à fort impact en 30 jours + 3 actions structurantes 60-90 jours.\n\n"
                "Étape 3 — Feuille de route 90 jours\n"
                "Plan 3 phases (Mois 1/2/3) avec : actions, responsables, outils AI, KPIs, budget.\n\n"
                "Étape 4 — Cas business\n"
                "10 lignes : pourquoi investir maintenant, ROI attendu, risques si on n'agit pas."
            ),
            "livrable": "Grille diagnostic + quick wins + feuille de route 90 jours + cas business.",
            "criteres": {
                "rigueur_diagnostic": "25%",
                "pertinence_quick_wins": "25%",
                "qualite_feuille_de_route": "35%",
                "conviction_cas_business": "15%",
            },
            "score_minimum": 70,
            "duree_estimee": "60 à 75 minutes",
        },
        hints_fr=[
            {"level": 1, "text": "Soyez honnête sur les lacunes — un diagnostic surévalué mène à une feuille de route irréaliste."},
            {"level": 2, "text": "Quick wins 30 jours : activer scoring AI HubSpot, former à 2 prompts ChatGPT essentiels, 1 séquence emails automatique."},
            {"level": 3, "text": "'Nos commerciaux passent 3h/jour en tâches admin. L'AI peut libérer 1h30/jour = 150h/mois redirigées vers la vente.'"},
        ],
        rubric_fr={"criteres": [
            {"nom": "Rigueur du diagnostic", "poids": 0.25, "description": "5 piliers évalués honnêtement avec écarts justifiés."},
            {"nom": "Pertinence des quick wins", "poids": 0.25, "description": "3 quick wins réalisables en 30 jours, à fort impact."},
            {"nom": "Qualité de la feuille de route", "poids": 0.35, "description": "Plan 90 jours réaliste, séquencé, avec responsables, outils et KPIs."},
            {"nom": "Conviction du cas business", "poids": 0.15, "description": "Argumentation chiffrée, pourquoi agir maintenant est clairement démontré."},
        ]},
    ))
    db.flush()

    # ── Leçon 1.2 ────────────────────────────────────────────────────────────
    l3_1_2 = Lesson(
        unit_id=u3_1.id, order=2,
        title_fr="Adapter la stratégie AI Sales au contexte MENA",
        title_en="Adapt AI Sales strategy to the MENA context",
        format="video", difficulty_level=4, estimated_duration_min=12,
        description_fr="Spécificités B2B MENA, contraintes réglementaires, partenariats locaux, cycles de décision.",
        description_en="B2B MENA specificities, regulatory constraints, local partnerships, decision cycles.",
        prerequisite_lesson_id=l3_1_1.id,
    )
    db.add(l3_1_2); db.flush()

    db.add(Activity(
        lesson_id=l3_1_2.id, order=1, type="video",
        title_fr="Vidéo — Adapter la stratégie AI Sales au contexte MENA",
        is_assessed=False, is_required=True,
        content_fr={"duration_min": 12, "url_fr": None},
    ))
    db.add(Activity(
        lesson_id=l3_1_2.id, order=2, type="case_study",
        title_fr="Cas pratique — Adapter une stratégie AI Sales à deux marchés MENA",
        title_en="Case study — Adapting an AI Sales strategy to two MENA markets",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "contexte": (
                "FinEdge est une fintech tunisienne (logiciel gestion financière PME), "
                "180 clients, 3 ans d'existence. Elle veut s'étendre au Maroc et aux UAE."
            ),
            "donnees": {
                "tunisie_actuel": {"clients": 180, "panier_moyen": "8 000 TND/an", "cycle_vente": "45 jours", "taux_conversion": "18%"},
                "maroc_cible": {"taille_marche": "85 000 PME formelles", "langue": "Français + Darija", "concurrents": "Sage Maroc, Odoo"},
                "uae_cible": {"taille_marche": "350 000 SMEs", "langue": "Anglais + Arabe", "specificites": "PDPL 2022, décision rapide, ROI premier critère"},
            },
            "questions": [
                {"id": 1, "question": "Comparez les stratégies AI Sales pour le Maroc et les UAE. En quoi doivent-elles être fondamentalement différentes ?", "axes": ["Outils AI", "Approche prospection", "Personnalisation culturelle", "Cycle de vente"]},
                {"id": 2, "question": "FinEdge a un budget de 2 000 USD/mois par marché. Proposez une allocation optimale pour chaque marché.", "contrainte": "Justifiez chaque outil par rapport aux spécificités du marché."},
                {"id": 3, "question": "Quels sont les 3 principaux risques d'expansion et comment les mitiger ?", "consigne": "Pour chaque risque : description, probabilité, plan de mitigation."},
            ],
            "synthese": "15 lignes : dans quel ordre FinEdge devrait entrer sur ces 2 marchés, pourquoi, et avec quelle stratégie prioritaire ?",
        },
        hints_fr=[
            {"level": 1, "text": "Maroc : proximité culturelle mais marché plus concurrentiel. UAE : cycle court mais exigences de preuve très élevées."},
            {"level": 2, "text": "UAE : LinkedIn Sales Navigator + Apollo.io indispensables. Maroc : WhatsApp Business AI + HubSpot plus adaptés aux PME locales."},
        ],
    ))
    db.flush()

    # ── Leçon 1.3 — ✅ passing_score=0 (feedback mentor) ─────────────────────
    l3_1_3 = Lesson(
        unit_id=u3_1.id, order=3,
        title_fr="Présenter sa stratégie AI Sales à la direction",
        title_en="Present AI Sales strategy to leadership",
        format="exercise", difficulty_level=5, estimated_duration_min=90,
        description_fr="Structurer un pitch stratégique, convaincre un comité de direction, répondre aux objections.",
        description_en="Structuring a strategic pitch, convincing a sceptical board, handling objections.",
        prerequisite_lesson_id=l3_1_2.id,
    )
    db.add(l3_1_3); db.flush()

    db.add(Activity(
        lesson_id=l3_1_3.id, order=1, type="exercise",
        title_fr="Projet — Présentation stratégie AI Sales à la direction",
        title_en="Project — AI Sales strategy board presentation",
        is_assessed=True, is_required=True, passing_score=0,  # ✅ 0 car feedback mentor
        content_fr={
            "consigne": (
                "Préparez une présentation de 10 à 15 slides pour convaincre la direction d'investir.\n\n"
                "Structure : Slide 1 Titre, Slide 2 État actuel, Slide 3 Opportunité AI, "
                "Slide 4 Diagnostic maturité, Slide 5 Vision 12 mois, Slide 6 3 piliers stratégie, "
                "Slide 7 Feuille de route 90J, Slide 8 Stack outils + budget, Slide 9 ROI projeté, "
                "Slide 10 Gestion risques, Slide 11 Plan formation, Slide 12 Validation + prochaines étapes.\n\n"
                "Préparez aussi les réponses à 4 objections :\n"
                "1) 'C'est trop cher pour notre stade.'\n"
                "2) 'Nos commerciaux ne vont pas adopter.'\n"
                "3) 'On risque de perdre la relation humaine.'\n"
                "4) 'Nos données ne sont pas assez structurées.'"
            ),
            "livrable": "Présentation 10-15 slides (PDF ou PPT) + document 2 pages réponses aux 4 objections.",
            "criteres": {
                "structure_logique_pitch": "25%",
                "solidite_arguments_chiffres": "30%",
                "realisme_feuille_route_budget": "25%",
                "qualite_reponses_objections": "20%",
            },
            "score_minimum": 70,
            "duree_estimee": "90 à 120 minutes",
            "feedback": "mentor",
            "note_evaluation": "Évaluation manuelle par mentor Euklydia sous 5 jours ouvrés.",
        },
        hints_fr=[
            {"level": 1, "text": "La direction pense en TND/EUR, pas en fonctionnalités. Chaque slide doit répondre : 'Qu'est-ce que ça nous rapporte ?'"},
            {"level": 2, "text": "Objection coût : calculez le coût de NE PAS adopter l'AI. Ex : '5 commerciaux × 2h/jour × 250 jours × coût horaire = X TND/an perdus.'"},
            {"level": 3, "text": "Objection adoption : proposez un pilote 30 jours avec 2 commerciaux volontaires. Réduire le risque perçu est la clé."},
        ],
        rubric_fr={"criteres": [
            {"nom": "Structure et logique du pitch", "poids": 0.25, "description": "Narration claire, chaque slide a un message clé, progression logique."},
            {"nom": "Solidité des arguments et chiffres", "poids": 0.30, "description": "Arguments étayés par données réelles ou réalistes, ROI calculé avec méthodologie transparente."},
            {"nom": "Réalisme de la feuille de route et budget", "poids": 0.25, "description": "Plan 90 jours réaliste, budget justifié outil par outil."},
            {"nom": "Qualité des réponses aux objections", "poids": 0.20, "description": "4 objections adressées avec empathie, contre-arguments solides et propositions concrètes."},
        ]},
    ))
    db.flush()

    # ════════════════════════════════════════════════════════════════════════
    # UNITÉ 2 — PILOTER UNE ÉQUIPE AI SALES
    # ════════════════════════════════════════════════════════════════════════

    u3_2 = Unit(
        module_id=m3.id, order=2,
        title_fr="Piloter une équipe AI Sales",
        title_en="Leading an AI Sales Team",
        description_fr="Former, orchestrer et gérer la résistance au changement dans une équipe AI Sales.",
        description_en="Train, orchestrate and manage change resistance in an AI Sales team.",
        estimated_duration_min=67,
    )
    db.add(u3_2); db.flush()

    # ── Leçon 2.1 ────────────────────────────────────────────────────────────
    l3_2_1 = Lesson(
        unit_id=u3_2.id, order=1,
        title_fr="Former ses collègues à l'AI",
        title_en="Train colleagues in AI",
        format="video", difficulty_level=4, estimated_duration_min=12,
        description_fr="Concevoir un programme de formation AI Sales interne, méthodes pédagogiques, mesurer l'adoption.",
        description_en="Design an internal AI Sales training programme, pedagogical methods, measuring adoption.",
    )
    db.add(l3_2_1); db.flush()

    db.add(Activity(
        lesson_id=l3_2_1.id, order=1, type="video",
        title_fr="Vidéo — Former ses collègues à l'AI",
        is_assessed=False, is_required=True,
        content_fr={"duration_min": 12, "url_fr": None},
    ))
    db.add(Activity(
        lesson_id=l3_2_1.id, order=2, type="exercise",
        title_fr="Exercice — Concevoir mon programme de formation AI Sales interne",
        title_en="Exercise — Design my internal AI Sales training programme",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": (
                "Vous formez 5 collègues commerciaux à l'AI Sales. Concevez un programme 4 semaines.\n\n"
                "Module A — Programme\n"
                "Pour chaque semaine : thème, objectif, durée (max 2h), format, outil AI, exercice, critère validation.\n\n"
                "Module B — Kit formateur\n"
                "(1) Email d'invitation (ton motivant, bénéfices clairs),\n"
                "(2) 5 règles du participant,\n"
                "(3) Quiz fin de formation (5 questions).\n\n"
                "Module C — Suivi adoption 30 jours\n"
                "Indicateurs (utilisation HubSpot, emails AI générés, temps économisé), fréquence de suivi."
            ),
            "livrable": "Programme 4 semaines + kit formateur (email + règles + quiz) + plan suivi adoption.",
            "criteres": {"realisme_programme": "35%", "qualite_kit_formateur": "35%", "rigueur_suivi_adoption": "30%"},
            "score_minimum": 70,
            "duree_estimee": "60 minutes",
        },
        hints_fr=[
            {"level": 1, "text": "Les commerciaux apprennent par la pratique — 50% minimum de temps hands-on par session."},
            {"level": 2, "text": "S1 : ChatGPT emails. S2 : HubSpot AI scoring. S3 : Campagne automatisée. S4 : Analyse données et optimisation."},
        ],
        rubric_fr={"criteres": [
            {"nom": "Réalisme du programme", "poids": 0.35, "description": "Faisable en 4 semaines, objectifs mesurables, progression cohérente."},
            {"nom": "Qualité du kit formateur", "poids": 0.35, "description": "Email motivant, règles pertinentes, quiz validant les acquis clés."},
            {"nom": "Rigueur du suivi d'adoption", "poids": 0.30, "description": "Indicateurs concrets et mesurables, plan de suivi réaliste."},
        ]},
    ))
    db.flush()

    # ── Leçon 2.2 ────────────────────────────────────────────────────────────
    l3_2_2 = Lesson(
        unit_id=u3_2.id, order=2,
        title_fr="Orchestrer humains et AI dans la vente",
        title_en="Orchestrate humans and AI in sales",
        format="video", difficulty_level=4, estimated_duration_min=10,
        description_fr="Matrice de décision AI vs humain, tâches à automatiser, modèle de collaboration optimale.",
        description_en="AI vs human decision matrix, tasks to automate, optimal collaboration model.",
        prerequisite_lesson_id=l3_2_1.id,
    )
    db.add(l3_2_2); db.flush()

    db.add(Activity(
        lesson_id=l3_2_2.id, order=1, type="video",
        title_fr="Vidéo — Orchestrer humains et AI dans la vente",
        is_assessed=False, is_required=True,
        content_fr={"duration_min": 10, "url_fr": None},
    ))
    db.add(Activity(
        lesson_id=l3_2_2.id, order=2, type="exercise",
        title_fr="Simulation — Concevoir le modèle de collaboration AI + Équipe",
        title_en="Simulation — Design the AI + Team collaboration model",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": (
                "Partie 1 — Matrice 4 quadrants\n"
                "Listez 15 tâches commerciales. Classez dans :\n"
                "A) AI seul, B) AI + Humain, C) Humain seul, D) À supprimer.\n\n"
                "Partie 2 — Redéfinition des rôles\n"
                "Comment le rôle des commerciaux évolue ? Nouvelles compétences ? Comment présenter positivement ?\n\n"
                "Partie 3 — Protocole quotidien\n"
                "Que fait l'AI avant l'arrivée du commercial, pendant les RDV, en fin de journée ?"
            ),
            "livrable": "Matrice 4 quadrants (15 tâches) + analyse évolution rôles + protocole quotidien.",
            "criteres": {"pertinence_classification": "35%", "coherence_evolution_roles": "35%", "praticite_protocole_quotidien": "30%"},
            "score_minimum": 70,
            "duree_estimee": "45 à 60 minutes",
        },
        hints_fr=[
            {"level": 1, "text": "Empathie, jugement complexe, relation de confiance → Humain. Répétitif, basé sur données, scalable → AI."},
            {"level": 2, "text": "Scoring leads = AI seul. Email prospection = AI + Humain. Négociation finale = Humain seul. Saisie CRM = À supprimer."},
        ],
    ))
    db.flush()

    # ── Leçon 2.3 ────────────────────────────────────────────────────────────
    l3_2_3 = Lesson(
        unit_id=u3_2.id, order=3,
        title_fr="Gérer la résistance au changement",
        title_en="Manage resistance to change",
        format="case_study", difficulty_level=5, estimated_duration_min=45,
        description_fr="Cas réel : équipe commerciale tunisienne résistante à l'adoption AI. Diagnostic, stratégies, indicateurs.",
        description_en="Real case: Tunisian sales team resistant to AI adoption. Diagnosis, strategies, indicators.",
        prerequisite_lesson_id=l3_2_2.id,
    )
    db.add(l3_2_3); db.flush()

    db.add(Activity(
        lesson_id=l3_2_3.id, order=1, type="case_study",
        title_fr="Cas Pharma Maghreb — Gérer la résistance d'une équipe commerciale",
        title_en="Pharma Maghreb case — Managing a sales team's resistance",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "contexte": (
                "Pharma Maghreb : distributeur pharmaceutique tunisien, 80 salariés, "
                "12 délégués médicaux (ancienneté moyenne 8 ans). "
                "Déploiement HubSpot AI annoncé. Vous êtes le responsable digital sales."
            ),
            "situation": (
                "Après 2 semaines : 4 délégués ont créé leur compte mais ne l'utilisent pas, "
                "3 sont ouvertement opposés ('L'AI va nous remplacer'), "
                "5 sont neutres attentistes, le manager senior dit 'on verra si ça marche'. "
                "Résultats attendus dans 60 jours."
            ),
            "questions": [
                {"id": 1, "question": "Analysez les 3 types de résistance et leur cause profonde.", "consigne": "Pour chaque résistance : nom, manifestation, cause profonde, profil."},
                {"id": 2, "question": "Comment gérez-vous le manager commercial senior en premier ? Rédigez le script de conversation.", "consigne": "Script 15-20 répliques. Objectif : le transformer en champion du projet."},
                {"id": 3, "question": "Plan d'activation sur 60 jours pour 9 délégués sur 12.", "consigne": "Plan semaine par semaine (8 semaines) avec actions et indicateurs."},
                {"id": 4, "question": "'J'ai 10 ans de relation avec mes clients — si je leur envoie des emails automatiques, je perds leur confiance.' Comment répondez-vous ?", "consigne": "Réponse empathique et convaincante en 8 à 10 lignes."},
            ],
            "synthese": "10 lignes : les 5 leçons retenues pour toute future conduite du changement AI Sales en PME MENA.",
        },
        hints_fr=[
            {"level": 1, "text": "3 familles de résistance : peur (perdre son emploi), inertie (habitudes), scepticisme (doute efficacité). Chacune demande une approche différente."},
            {"level": 2, "text": "Pour le manager senior : ne parlez pas de fonctionnalités, parlez de ses KPIs personnels. Un quick win personnel > 10 arguments généraux."},
        ],
    ))
    db.flush()

    # ════════════════════════════════════════════════════════════════════════
    # UNITÉ 3 — MESURER LE ROI DE L'AI
    # ════════════════════════════════════════════════════════════════════════

    u3_3 = Unit(
        module_id=m3.id, order=3,
        title_fr="Mesurer le ROI de l'AI",
        title_en="Measuring AI ROI",
        description_fr="Calculer le ROI, créer le dashboard AI Sales, présenter les résultats à la direction.",
        description_en="Calculate ROI, build AI Sales dashboard, present results to leadership.",
        estimated_duration_min=162,
    )
    db.add(u3_3); db.flush()

    # ── Leçon 3.1 ────────────────────────────────────────────────────────────
    l3_3_1 = Lesson(
        unit_id=u3_3.id, order=1,
        title_fr="Calculer le retour sur investissement AI",
        title_en="Calculate AI ROI",
        format="video", difficulty_level=4, estimated_duration_min=12,
        description_fr="Méthodologie ROI AI Sales, KPIs quantitatifs et qualitatifs, modèle simplifié, erreurs à éviter.",
        description_en="AI Sales ROI methodology, quantitative and qualitative KPIs, simplified model, errors to avoid.",
    )
    db.add(l3_3_1); db.flush()

    db.add(Activity(
        lesson_id=l3_3_1.id, order=1, type="video",
        title_fr="Vidéo — Calculer le retour sur investissement AI",
        is_assessed=False, is_required=True,
        content_fr={"duration_min": 12, "url_fr": None},
    ))
    db.add(Activity(
        lesson_id=l3_3_1.id, order=2, type="quiz",
        title_fr="Quiz — ROI de l'AI Sales",
        title_en="Quiz — AI Sales ROI",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "questions": [
                {
                    "id": 1,
                    "question": "4 commerciaux économisent 1h30/jour. Coût horaire : 25 TND/h. Gain mensuel (20 jours ouvrés) ?",
                    "options": ["A) 1 500 TND/mois", "B) 3 000 TND/mois", "C) 6 000 TND/mois", "D) 750 TND/mois"],
                    "correct": "C",
                    "explanation": "4 × 1,5h × 20 jours × 25 TND = 6 000 TND/mois. Sur 12 mois = 72 000 TND/an.",
                },
                {
                    "id": 2,
                    "question": "Taux conversion : 8% → 12% après AI. Panier 5 000 TND, 100 prospects/mois. Gain mensuel en revenus ?",
                    "options": ["A) 5 000 TND", "B) 10 000 TND", "C) 20 000 TND", "D) 40 000 TND"],
                    "correct": "C",
                    "explanation": "Avant : 100×8%×5000 = 40 000. Après : 100×12%×5000 = 60 000. Gain = 20 000 TND/mois.",
                },
                {
                    "id": 3,
                    "question": "Quel est l'indicateur le plus convaincant pour prouver le ROI de l'AI Sales à la direction ?",
                    "options": [
                        "A) Le nombre de fonctionnalités AI utilisées",
                        "B) Le nombre d'emails envoyés par l'AI",
                        "C) La vélocité des deals réduite ET le taux de conversion amélioré avec impact revenus chiffré",
                        "D) Le taux de satisfaction des commerciaux",
                    ],
                    "correct": "C",
                    "explanation": "La direction parle revenus et efficacité. Ces 2 métriques se traduisent directement en TND/an.",
                },
                {
                    "id": 4,
                    "question": "Quelle est la principale erreur à éviter quand on calcule le ROI de l'AI Sales ?",
                    "options": [
                        "A) Inclure les coûts de formation dans le calcul",
                        "B) Attribuer à l'AI toutes les améliorations sans isoler les autres facteurs",
                        "C) Présenter le ROI trop tôt avant 6 mois",
                        "D) Inclure les gains de productivité indirects",
                    ],
                    "correct": "B",
                    "explanation": "Il faut isoler l'impact AI des autres variables (saison, recrutement, produit). Utiliser un groupe contrôle si possible.",
                },
            ],
            "passing_score": 70,
        },
        hints_fr=[
            {"level": 1, "text": "ROI = (Gains - Coût AI) / Coût AI × 100. Un ROI > 200% en 12 mois est réaliste pour une équipe bien formée."},
        ],
    ))
    db.flush()

    # ── Leçon 3.2 — ✅ Vidéo ajoutée + exercice décalé en order=2 ────────────
    l3_3_2 = Lesson(
        unit_id=u3_3.id, order=2,
        title_fr="Créer son tableau de bord AI Sales",
        title_en="Build your AI Sales dashboard",
        format="tutorial", difficulty_level=4, estimated_duration_min=60,
        description_fr="Dashboard HubSpot personnalisé, KPIs par rôle (commercial, manager, DG), rapports automatiques.",
        description_en="Custom HubSpot dashboard, KPI selection by role, weekly report automation.",
        prerequisite_lesson_id=l3_3_1.id,
    )
    db.add(l3_3_2); db.flush()

    # ✅ Activité 1 — Vidéo (ajoutée)
    db.add(Activity(
        lesson_id=l3_3_2.id, order=1, type="video",
        title_fr="Vidéo — Créer son tableau de bord AI Sales dans HubSpot",
        title_en="Video — Build your AI Sales dashboard in HubSpot",
        is_assessed=False, is_required=True,
        content_fr={"duration_min": 12, "url_fr": None},
        content_en={"duration_min": 12, "url_en": None},
    ))
    # ✅ Activité 2 — Exercice (order décalé à 2)
    db.add(Activity(
        lesson_id=l3_3_2.id, order=2, type="exercise",
        title_fr="Tutoriel — Construire mon dashboard AI Sales dans HubSpot",
        title_en="Tutorial — Build my AI Sales dashboard in HubSpot",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "steps": [
                "Créer un nouveau dashboard (Rapports > Tableaux de bord > Créer un tableau de bord)",
                "Ajouter 5 widgets KPIs : nouveaux prospects/semaine, taux conversion, vélocité deals, CA prévu AI, score moyen leads",
                "Configurer le widget 'Prévision de revenus AI' avec les données du pipeline",
                "Ajouter un rapport d'activité équipe : emails, appels, réunions planifiées",
                "Configurer l'envoi automatique rapport hebdomadaire (Paramètres > Rapports > Planifier)",
                "Créer une vue manager : performance individuelle par commercial avec scoring AI comparé",
            ],
            "consigne": "Suivez les 6 étapes, soumettez une capture du dashboard final + note 10 lignes sur son utilisation en réunion d'équipe.",
            "livrable": "Capture d'écran dashboard HubSpot (min 5 widgets) + note explicative 10 lignes.",
            "criteres": {
                "completude_dashboard": "40%",
                "pertinence_kpis_choisis": "35%",
                "qualite_note_manageriale": "25%",
            },
            "score_minimum": 70,
            "duree_estimee": "60 minutes",
        },
        hints_fr=[
            {"level": 1, "text": "Créez 3 dashboards distincts : commercial (mes performances), manager (équipe), direction (vue business)."},
            {"level": 2, "text": "Widget le plus utile en réunion : 'Deals par étape de pipeline' — identifie immédiatement où ça bloque."},
        ],
    ))
    db.flush()

    # ── Leçon 3.3 — ✅ passing_score=0 (feedback mentor) ─────────────────────
    l3_3_3 = Lesson(
        unit_id=u3_3.id, order=3,
        title_fr="Présenter les résultats à la direction",
        title_en="Present results to leadership",
        format="exercise", difficulty_level=5, estimated_duration_min=90,
        description_fr="Rapport de performance AI Sales trimestriel, storytelling avec les données, recommandations.",
        description_en="Quarterly AI Sales performance report, data storytelling, recommendations.",
        prerequisite_lesson_id=l3_3_2.id,
    )
    db.add(l3_3_3); db.flush()

    db.add(Activity(
        lesson_id=l3_3_3.id, order=1, type="exercise",
        title_fr="Projet — Rapport de performance AI Sales trimestriel",
        title_en="Project — Quarterly AI Sales performance report",
        is_assessed=True, is_required=True, passing_score=0,  # ✅ 0 car feedback mentor
        content_fr={
            "scenario": (
                "Données disponibles :\n"
                "Avant AI (T-1) : CA 380 000 TND, conversion 9%, cycle 52j, admin 3h/j, ouverture emails 28%\n"
                "Après AI (T0) : CA 445 000 TND, conversion 13%, cycle 38j, admin 1h30/j, ouverture 41%\n"
                "Coût AI : 8 500 TND sur 3 mois"
            ),
            "consigne": (
                "Section 1 — Résumé exécutif (1 page) : 3 chiffres clés, ROI calculé, conclusion.\n\n"
                "Section 2 — Analyse détaillée (2 pages) : évolution chaque KPI, ce qui a marché, ce qui n'a pas encore donné de résultats.\n\n"
                "Section 3 — ROI et rentabilité : calcul complet + projection 12 mois.\n\n"
                "Section 4 — Recommandations : 3 actions prioritaires, 1 point d'attention, budget supplémentaire justifié."
            ),
            "livrable": "Rapport 4 à 6 pages + présentation 5 slides résumée pour la direction.",
            "criteres": {
                "qualite_resume_executif": "20%",
                "rigueur_analyse_kpis": "30%",
                "exactitude_calcul_roi": "25%",
                "pertinence_recommandations": "25%",
            },
            "score_minimum": 70,
            "feedback": "mentor",
            "note_evaluation": "Évaluation manuelle par mentor Euklydia sous 5 jours ouvrés.",
            "duree_estimee": "90 minutes",
        },
        hints_fr=[
            {"level": 1, "text": "Commencez par le résumé exécutif — il guide tout le reste. La direction lit le résumé avant le détail."},
            {"level": 2, "text": "ROI : Gain revenus = 65 000. Gain productivité = 4×1,5h×65j×25 = 9 750. Total = 74 750. Coût = 8 500. ROI = 779%."},
        ],
        rubric_fr={"criteres": [
            {"nom": "Qualité du résumé exécutif", "poids": 0.20, "description": "Lisible en 2 minutes, 3 chiffres clés mis en valeur, conclusion claire."},
            {"nom": "Rigueur de l'analyse KPIs", "poids": 0.30, "description": "Chaque KPI analysé avec contexte, améliorations et points faibles identifiés honnêtement."},
            {"nom": "Exactitude du calcul ROI", "poids": 0.25, "description": "Méthodologie ROI correcte, tous les coûts inclus, projection 12 mois réaliste."},
            {"nom": "Pertinence des recommandations", "poids": 0.25, "description": "3 actions concrètes, prioritaires et directement actionnables par la direction."},
        ]},
    ))
    db.flush()

    # ════════════════════════════════════════════════════════════════════════
    # UNITÉ 4 — AI SALES AVANCÉ MENA
    # ════════════════════════════════════════════════════════════════════════

    u3_4 = Unit(
        module_id=m3.id, order=4,
        title_fr="AI Sales avancé MENA",
        title_en="Advanced AI Sales MENA",
        description_fr="Cas B2B tunisiens, stratégies Maghreb et Golfe, avenir de l'AI Sales en MENA.",
        description_en="Tunisian B2B cases, Maghreb and Gulf strategies, future of AI Sales in MENA.",
        estimated_duration_min=84,
    )
    db.add(u3_4); db.flush()

    # ── Leçon 4.1 ────────────────────────────────────────────────────────────
    l3_4_1 = Lesson(
        unit_id=u3_4.id, order=1,
        title_fr="Cas complexes B2B tunisiens",
        title_en="Complex B2B Tunisian cases",
        format="case_study", difficulty_level=5, estimated_duration_min=60,
        description_fr="3 cas réels d'entreprises tunisiennes : analyse des stratégies, résultats et facteurs de succès.",
        description_en="3 real cases of Tunisian companies: strategy analysis, results and success factors.",
    )
    db.add(l3_4_1); db.flush()

    db.add(Activity(
        lesson_id=l3_4_1.id, order=1, type="case_study",
        title_fr="3 Cas B2B tunisiens — Analyse expert",
        title_en="3 Tunisian B2B cases — Expert analysis",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "introduction": "Analysez ces 3 cas en adoptant la posture d'un consultant AI Sales senior.",
            "cas": [
                {
                    "id": 1, "titre": "CAS LOGISOFT — PME SaaS Tunis",
                    "contexte": "LogiSoft (logiciel gestion PME industrielles, 45 clients, croissance stagnante 18 mois, 75% bouche-à-oreille).",
                    "action_menee": "HubSpot AI + Apollo.io + ChatGPT sur 6 mois. Formation 2 semaines. 3 séquences ciblées.",
                    "resultats": "Mois 3 : 12 leads qualifiés. Mois 4-6 : 8 nouveaux contrats. CA +67%. Investissement AI : 6 200 TND.",
                    "questions": [
                        "Analysez les facteurs de succès de LogiSoft.",
                        "Pourquoi les résultats n'arrivent qu'au mois 3 ? Comment gérer cette période creuse ?",
                        "Quelles sont les 3 prochaines étapes pour les 6 mois suivants ?",
                    ],
                },
                {
                    "id": 2, "titre": "CAS MEDFORM — Formation médicale Sfax",
                    "contexte": "MedForm (formation continue santé, 2 800 médecins, taux inscription en baisse de 18% à 11%).",
                    "action_menee": "Segmentation AI 15 spécialités + personnalisation ChatGPT + timing optimisé (jeudi soir) + A/B testing.",
                    "resultats": "Taux ouverture +85%, inscription +64%, revenus +43% en 4 mois, temps marketing -60%.",
                    "questions": [
                        "Pourquoi la segmentation par spécialité a-t-elle eu un impact si fort ?",
                        "Quel est le rôle de la donnée comportementale (jeudi soir) ?",
                        "Comment appliquer cette stratégie au marché algérien ?",
                    ],
                },
                {
                    "id": 3, "titre": "CAS CONSTRUCTPLUS — BTP Sousse",
                    "contexte": "ConstructPlus (matériaux construction, cycle vente 90 jours, prospects perdus par manque de suivi).",
                    "action_menee": "Scoring AI HubSpot + automatisation relances par profil + WhatsApp Business + formation 1 commercial.",
                    "resultats": "Cycle -35% (90→58j), prospects perdus -80%, conversion +40% (15→21%), 2,5x plus de prospects gérés.",
                    "questions": [
                        "Pourquoi l'intégration WhatsApp Business est-elle adaptée au marché tunisien BTP ?",
                        "Comment le scoring AI résout-il le problème des prospects perdus ?",
                        "ConstructPlus recrute un 2e commercial. Comment maximiser l'impact AI avec 2 personnes ?",
                    ],
                },
            ],
            "synthese": "15 lignes : 'Les 7 facteurs de succès d'une implémentation AI Sales dans une PME tunisienne'.",
        },
        hints_fr=[
            {"level": 1, "text": "Pour chaque cas : cherchez le facteur différenciant spécifique au contexte tunisien."},
        ],
    ))
    db.flush()

    # ── Leçon 4.2 ────────────────────────────────────────────────────────────
    l3_4_2 = Lesson(
        unit_id=u3_4.id, order=2,
        title_fr="Stratégies B2B Maghreb et Golfe",
        title_en="B2B strategies Maghreb and Gulf",
        format="video", difficulty_level=5, estimated_duration_min=12,
        description_fr="Différences Maghreb vs Golfe, cycles de décision B2B par pays, outils AI adaptés, pénétration marché.",
        description_en="Maghreb vs Gulf differences, B2B decision cycles by country, AI tools, market penetration.",
        prerequisite_lesson_id=l3_4_1.id,
    )
    db.add(l3_4_2); db.flush()

    db.add(Activity(
        lesson_id=l3_4_2.id, order=1, type="video",
        title_fr="Vidéo — Stratégies B2B Maghreb et Golfe",
        is_assessed=False, is_required=True,
        content_fr={"duration_min": 12, "url_fr": None},
    ))
    db.add(Activity(
        lesson_id=l3_4_2.id, order=2, type="exercise",
        title_fr="Exercice stratégique — Plan d'expansion AI Sales dans un nouveau marché MENA",
        title_en="Strategic exercise — AI Sales expansion plan in a new MENA market",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": (
                "Choisissez un marché MENA (Maroc, Algérie, Égypte, Arabie Saoudite, UAE ou Qatar).\n\n"
                "Analyse de marché (1 page) : taille, maturité digitale B2B, concurrents, spécificités culturelles/réglementaires.\n\n"
                "Stratégie AI Sales adaptée (1 page) : stack outils justifié, canaux prospection, langue/ton, timing saisonnier.\n\n"
                "Plan d'action 90 jours (1 page) : M1 préparation, M2 lancement, M3 optimisation. Actions, outils, KPIs, budget.\n\n"
                "Risques et facteurs de succès : 3 risques avec mitigation, 3 facteurs clés."
            ),
            "livrable": "Mini business plan d'expansion de 3 à 4 pages.",
            "criteres": {
                "pertinence_analyse_marche": "25%",
                "adequation_strategie_ai": "35%",
                "realisme_plan_action": "25%",
                "maturite_analyse_risques": "15%",
            },
            "score_minimum": 70,
            "duree_estimee": "60 à 75 minutes",
        },
        hints_fr=[
            {"level": 1, "text": "Faites une vraie recherche — LinkedIn, articles récents, rapports Deloitte/McKinsey MENA. La pertinence dépend de la qualité des sources."},
            {"level": 2, "text": "UAE/Saudi : LinkedIn Sales Navigator + contenu anglais haute qualité + certifications = crédibilité. Très compétitif et digital-first."},
        ],
    ))
    db.flush()

    # ── Leçon 4.3 ────────────────────────────────────────────────────────────
    l3_4_3 = Lesson(
        unit_id=u3_4.id, order=3,
        title_fr="L'avenir de l'AI Sales en MENA",
        title_en="Future of AI Sales in MENA",
        format="video", difficulty_level=4, estimated_duration_min=12,
        description_fr="Tendances AI Sales 2025-2027 MENA, agents AI autonomes, évolution rôle commercial, compétences futures.",
        description_en="AI Sales trends 2025-2027 MENA, autonomous AI agents, evolution of the sales role.",
        prerequisite_lesson_id=l3_4_2.id,
    )
    db.add(l3_4_3); db.flush()

    db.add(Activity(
        lesson_id=l3_4_3.id, order=1, type="video",
        title_fr="Vidéo — L'avenir de l'AI Sales en MENA",
        is_assessed=False, is_required=True,
        content_fr={"duration_min": 12, "url_fr": None},
    ))
    db.add(Activity(
        lesson_id=l3_4_3.id, order=2, type="forum_discussion",
        title_fr="Forum — Ma vision de l'AI Sales en MENA dans 3 ans",
        title_en="Forum — My vision of AI Sales in MENA in 3 years",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "question": (
                "Quelle est votre vision de l'évolution du métier commercial MENA d'ici 2027-2028 ?\n\n"
                "1) Quelles tâches du commercial vont complètement disparaître ?\n"
                "2) Quelles nouvelles compétences vont devenir indispensables ?\n"
                "3) Quel type d'entreprise MENA sera le plus transformé par l'AI Sales — et pourquoi ?"
            ),
            "consigne": "Minimum 15 lignes. Commentez la vision de 2 autres apprenants avec une réponse constructive.",
        },
        hints_fr=[
            {"level": 1, "text": "Pensez aux tâches que vous faisiez il y a 5 ans et que l'AI remplace déjà. Extrapolez cette tendance sur 3 ans."},
        ],
    ))
    db.flush()

    # ════════════════════════════════════════════════════════════════════════
    # UNITÉ 5 — GOUVERNANCE ET ÉTHIQUE AI AVANCÉE
    # ════════════════════════════════════════════════════════════════════════

    u3_5 = Unit(
        module_id=m3.id, order=5,
        title_fr="Gouvernance et Éthique AI — Niveau Expert",
        title_en="AI Governance and Ethics — Expert Level",
        description_fr="Créer sa politique AI Sales, gérer les crises éthiques AI en MENA.",
        description_en="Create your AI Sales policy, manage AI ethics crises in MENA.",
        estimated_duration_min=62,
    )
    db.add(u3_5); db.flush()

    # ── Leçon 5.1 ────────────────────────────────────────────────────────────
    l3_5_1 = Lesson(
        unit_id=u3_5.id, order=1,
        title_fr="Créer sa politique AI Sales",
        title_en="Create your AI Sales policy",
        format="video", difficulty_level=5, estimated_duration_min=12,
        description_fr="Composantes d'une politique AI Sales, gouvernance des données, processus validation, alignement valeurs.",
        description_en="Components of an AI Sales policy, data governance, validation process, values alignment.",
    )
    db.add(l3_5_1); db.flush()

    db.add(Activity(
        lesson_id=l3_5_1.id, order=1, type="video",
        title_fr="Vidéo — Créer sa politique AI Sales",
        is_assessed=False, is_required=True,
        content_fr={"duration_min": 12, "url_fr": None},
    ))
    db.add(Activity(
        lesson_id=l3_5_1.id, order=2, type="exercise",
        title_fr="Projet — Rédiger la politique AI Sales de mon entreprise",
        title_en="Project — Write my company's AI Sales policy",
        is_assessed=True, is_required=True, passing_score=70,
        content_fr={
            "consigne": (
                "Rédigez la politique AI Sales officielle de votre entreprise (8 sections obligatoires) :\n\n"
                "1. Préambule et valeurs\n"
                "2. Usages autorisés (min 8 avec conditions)\n"
                "3. Usages interdits (min 5 avec justification)\n"
                "4. Règles de gestion des données clients\n"
                "5. Processus de validation des nouveaux outils AI\n"
                "6. Droits et recours des prospects/clients\n"
                "7. Responsabilités\n"
                "8. Mise à jour (fréquence et responsable)"
            ),
            "livrable": "Document politique AI Sales de 3 à 5 pages, professionnel et opérationnel.",
            "criteres": {
                "completude_structure": "25%",
                "pertinence_usages_autorises_interdits": "30%",
                "rigueur_gouvernance_donnees": "25%",
                "operationnalite_document": "20%",
            },
            "score_minimum": 70,
            "duree_estimee": "60 à 75 minutes",
        },
        hints_fr=[
            {"level": 1, "text": "Une bonne politique est un guide pratique que vos commerciaux vont réellement lire — pas un document juridique austère."},
            {"level": 2, "text": "Usages interdits essentiels : achat bases sans consentement, profilage psychologique non consenti, fausse urgence, chatbot se faisant passer pour humain."},
        ],
        rubric_fr={"criteres": [
            {"nom": "Complétude de la structure", "poids": 0.25, "description": "Les 8 sections sont présentes et développées de façon substantielle."},
            {"nom": "Pertinence des usages autorisés/interdits", "poids": 0.30, "description": "Usages réalistes adaptés MENA, interdictions justifiées éthiquement et légalement."},
            {"nom": "Rigueur de la gouvernance des données", "poids": 0.25, "description": "Conforme aux exigences légales MENA (Tunisie 2004-63 ou équivalent), pratique et vérifiable."},
            {"nom": "Opérationnalité du document", "poids": 0.20, "description": "Clair, utilisable par un commercial non-juriste, sans jargon excessif."},
        ]},
    ))
    db.flush()

    # ── Leçon 5.2 ────────────────────────────────────────────────────────────
    l3_5_2 = Lesson(
        unit_id=u3_5.id, order=2,
        title_fr="Gérer les crises éthiques AI",
        title_en="Manage AI ethics crises",
        format="case_study", difficulty_level=5, estimated_duration_min=50,
        description_fr="Simulation 2 crises majeures : fuite données CRM et scandale manipulation algorithmique.",
        description_en="Simulation of 2 major crises: CRM data breach and algorithmic manipulation scandal.",
        prerequisite_lesson_id=l3_5_1.id,
    )
    db.add(l3_5_2); db.flush()

    db.add(Activity(
        lesson_id=l3_5_2.id, order=1, type="case_study",
        title_fr="Simulation de crise — 2 scénarios de crise éthique AI",
        title_en="Crisis simulation — 2 AI ethics crisis scenarios",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "introduction": "Ces 2 simulations vous préparent à réagir vite et bien face à une crise AI.",
            "scenarios": [
                {
                    "id": 1, "titre": "CRISE 1 — La fuite de données CRM",
                    "contexte": (
                        "Lundi 8h30 : un prestataire ayant accès à votre HubSpot a été piraté. "
                        "1 200 prospects compromis dont 3 clients VIP. "
                        "Vous avez 2 heures avant que ça fuite sur les réseaux."
                    ),
                    "questions": [
                        {"q": "5 premières actions dans les 2 heures ?", "consigne": "Liste priorisée avec justification."},
                        {"q": "Rédigez l'email de notification aux 1 200 prospects.", "consigne": "Transparent, empathique, conforme aux obligations légales."},
                        {"q": "Comment gérez-vous les 3 clients VIP ?", "consigne": "Approche personnalisée différente de l'email de masse."},
                        {"q": "Mesures préventives pour éviter une récidive ?", "consigne": "Plan de sécurisation en 5 points."},
                    ],
                },
                {
                    "id": 2, "titre": "CRISE 2 — Le scandale de manipulation algorithmique",
                    "contexte": (
                        "Un journaliste publie : 'Comment [Votre Entreprise] manipule ses clients avec l'AI.' "
                        "Article partagé 2 000 fois sur LinkedIn en 6 heures. "
                        "Vos 10 plus gros clients vous appellent."
                    ),
                    "questions": [
                        {"q": "Réaction publique LinkedIn dans les 3 heures ?", "consigne": "Post officiel entreprise, max 200 mots."},
                        {"q": "Comment gérez-vous l'appel de vos 10 plus gros clients ?", "consigne": "Script téléphonique 10-15 répliques."},
                        {"q": "Actions internes envers le commercial et l'équipe ?", "consigne": "Plan interne 5 étapes avec communication équipe."},
                        {"q": "Comment transformer cette crise en opportunité éthique ?", "consigne": "Plan reconstruction confiance sur 90 jours."},
                    ],
                },
            ],
            "bilan_final": "Votre 'Plan de préparation aux crises AI' : 5 actions concrètes à mettre en place dès demain. Minimum 10 lignes.",
        },
        hints_fr=[
            {"level": 1, "text": "Transparence rapide > silence prolongé. Communiquer honnêtement en < 24h limite les dégâts de réputation."},
            {"level": 2, "text": "Crise 1 : notification obligatoire à l'INPDP (loi tunisienne 2004-63) et aux personnes concernées. Ne pas notifier est une faute aggravante."},
        ],
    ))
    db.flush()

    # ════════════════════════════════════════════════════════════════════════
    # UNITÉ 6 — CERTIFICATION FINALE ✅ (ajoutée)
    # ════════════════════════════════════════════════════════════════════════

    u3_cert = Unit(
        module_id=m3.id, order=6,
        title_fr="Certification Finale — AI Sales Specialist",
        title_en="Final Certification — AI Sales Specialist",
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
        title_fr="Test final de certification — AI Sales Specialist",
        title_en="Final certification test — AI Sales Specialist",
        is_assessed=True, is_required=True, passing_score=80,
        content_fr={
            "instructions": "Ce test couvre les 3 modules. 30 minutes. Score minimum : 16/20 (80%) pour accéder au projet.",
            "questions": [
                # ── Module 1 — Fondations ──────────────────────────────────
                {"id": 1, "question": "Qu'est-ce que l'AI permet principalement à un commercial ?", "options": ["A) Remplacer complètement le commercial", "B) Analyser, prédire et automatiser pour travailler plus efficacement", "C) Supprimer le besoin d'un CRM", "D) Appeler les clients automatiquement"], "correct": "B", "explanation": "L'AI amplifie le commercial — elle ne le remplace pas.", "module": 1},
                {"id": 2, "question": "Quelle est la principale différence entre un CRM classique et un CRM avec AI ?", "options": ["A) Le CRM classique est gratuit, le CRM AI est payant", "B) Le CRM classique stocke passivement ; le CRM AI analyse et recommande proactivement", "C) Le CRM AI remplace complètement le commercial", "D) Il n'y a pas de différence significative"], "correct": "B", "explanation": "Le CRM AI est proactif — analyse et recommande. Le CRM classique est passif.", "module": 1},
                {"id": 3, "question": "Quels sont les 5 éléments d'un bon prompt de prospection ?", "options": ["A) Titre, corps, signature, objet, pièce jointe", "B) Rôle, contexte, objectif, contraintes, personnalisation", "C) Langue, ton, longueur, format, destinataire", "D) Introduction, problème, solution, prix, conclusion"], "correct": "B", "explanation": "Rôle + Contexte + Objectif + Contraintes + Personnalisation.", "module": 1},
                {"id": 4, "question": "Quelle est la longueur idéale d'un email de prospection froide B2B MENA ?", "options": ["A) 50 mots", "B) 300 mots", "C) 120 à 150 mots", "D) 500 mots"], "correct": "C", "explanation": "120-150 mots est la longueur optimale pour un email de prospection froide B2B.", "module": 1},
                {"id": 5, "question": "Un commercial copie le contrat d'un client dans ChatGPT. Que fait-il de problématique ?", "options": ["A) Rien — ChatGPT est sécurisé", "B) Il expose des données confidentielles à un tiers sans autorisation", "C) Il perd du temps inutilement", "D) Il enfreint uniquement les règles de son entreprise"], "correct": "B", "explanation": "Les données confidentielles ne doivent jamais être partagées dans des outils AI publics.", "module": 1},
                # ── Module 2 — Pratique ────────────────────────────────────
                {"id": 6, "question": "Qu'est-ce qui déclenche l'arrêt automatique d'une séquence HubSpot ?", "options": ["A) L'expiration du délai de 21 jours", "B) La réponse du prospect à n'importe quel email", "C) Quand le prospect visite votre site web", "D) Quand vous désactivez manuellement"], "correct": "B", "explanation": "Les séquences HubSpot s'arrêtent automatiquement dès qu'un prospect répond.", "module": 2},
                {"id": 7, "question": "Un prospect a un lead score de 85 dans HubSpot. Que faire ?", "options": ["A) L'inscrire dans une séquence de 21 jours", "B) Attendre qu'il vous contacte", "C) Le contacter dans les 2 heures avec une proposition personnalisée", "D) Lui envoyer automatiquement votre brochure"], "correct": "C", "explanation": "Score 85 = fenêtre d'achat ouverte. Chaque heure perdue réduit la probabilité de conversion.", "module": 2},
                {"id": 8, "question": "Pour 80 prospects en 3 secteurs, quel niveau de personnalisation est optimal ?", "options": ["A) Niveau 4 — hyper-personnalisation individuelle", "B) Niveau 1 — uniquement le prénom", "C) Niveau 2 — 3 variantes contextuelles par secteur", "D) Aucune personnalisation"], "correct": "C", "explanation": "Pour 80 prospects en 3 secteurs, le Niveau 2 est le meilleur rapport efficacité/effort.", "module": 2},
                {"id": 9, "question": "Pourquoi Zoho CRM est-il populaire parmi les PME MENA ?", "options": ["A) Zoho a plus de fonctionnalités AI que HubSpot", "B) Interface en arabe, prix bas (14$/mois) et serveurs régionaux MENA", "C) Zoho est uniquement disponible en MENA", "D) Zoho est gratuit pour les PME tunisiennes"], "correct": "B", "explanation": "Zoho gagne sur : interface en arabe, prix accessible et conformité des données locales.", "module": 2},
                {"id": 10, "question": "Une PME tunisienne prospectant des clients en France est-elle soumise au RGPD ?", "options": ["A) Non — le RGPD ne s'applique qu'aux entreprises européennes", "B) Oui — si elle collecte des données de personnes résidant en Europe", "C) Uniquement si elle a un bureau en Europe", "D) Uniquement si elle réalise plus de 1M€ de CA"], "correct": "B", "explanation": "Le RGPD s'applique selon le lieu de résidence des prospects, pas le lieu de l'entreprise.", "module": 2},
                # ── Module 3 — Expert ──────────────────────────────────────
                {"id": 11, "question": "CRM AI actif + séquences déployées mais sans ROI mesuré ni gouvernance = quel niveau de maturité ?", "options": ["A) Niveau 1 — Initiation", "B) Niveau 2 — Adoption", "C) Niveau 3 — Optimisation", "D) Niveau 4 — Transformation"], "correct": "B", "explanation": "Niveau 2 = CRM AI actif, séquences déployées, mais ROI non mesuré et gouvernance absente.", "module": 3},
                {"id": 12, "question": "Pourquoi le modèle de formation en cascade avec champions AI est-il efficace en MENA ?", "options": ["A) Parce qu'il coûte moins cher", "B) Parce que l'apprentissage par les pairs est culturellement plus efficace en MENA", "C) Parce que les champions AI ont toujours raison", "D) Parce que le management n'a pas à s'impliquer"], "correct": "B", "explanation": "Un collègue qui montre ses résultats AI est 5x plus convaincant qu'une présentation du management.", "module": 3},
                {"id": 13, "question": "PME investit 6 000 TND dans l'AI Sales, génère 72 000 TND de bénéfices. Quel est le ROI ?", "options": ["A) 72%", "B) 720%", "C) 1100%", "D) 600%"], "correct": "C", "explanation": "ROI = (72 000 - 6 000) / 6 000 × 100 = 1100%.", "module": 3},
                {"id": 14, "question": "Quelle section du dashboard AI Sales est lue quotidiennement par les commerciaux ?", "options": ["A) Section 4 — ROI et impact business", "B) Section 1 — Performance pipeline", "C) Section 3 — Productivité équipe", "D) Section 2 — Efficacité campagnes"], "correct": "B", "explanation": "Section 1 (performance pipeline) = vue quotidienne des commerciaux — deals actifs, probabilités, alertes.", "module": 3},
                {"id": 15, "question": "Dans un groupe familial tunisien (3 générations), quel est le principe le plus important ?", "options": ["A) Contacter uniquement le DAF car il contrôle le budget", "B) Respecter la hiérarchie familiale — le DG fondateur a le dernier mot", "C) Éviter les rencontres physiques et tout gérer par email AI", "D) Proposer une réduction de 30% pour accélérer la décision"], "correct": "B", "explanation": "Dans un groupe familial tunisien, la hiérarchie familiale prime sur la hiérarchie fonctionnelle.", "module": 3},
                {"id": 16, "question": "Pourquoi la politique AI Sales doit-elle être co-construite avec l'équipe ?", "options": ["A) Parce que la direction n'a pas les compétences pour la rédiger", "B) Parce qu'en MENA, une politique acceptée sera appliquée — une politique imposée sera contournée", "C) Parce que la co-construction est obligatoire légalement", "D) Parce que cela réduit les coûts"], "correct": "B", "explanation": "En MENA, le changement accepté est 10x plus durable que le changement imposé.", "module": 3},
                {"id": 17, "question": "4 commerciaux économisent 1h30/jour. Coût horaire 25 TND/h, 20 jours ouvrés. Gain mensuel ?", "options": ["A) 1 500 TND/mois", "B) 3 000 TND/mois", "C) 6 000 TND/mois", "D) 750 TND/mois"], "correct": "C", "explanation": "4 × 1,5h × 20 × 25 = 6 000 TND/mois.", "module": 3},
                {"id": 18, "question": "Quelle est la principale erreur à éviter quand on calcule le ROI de l'AI Sales ?", "options": ["A) Inclure les coûts de formation", "B) Attribuer à l'AI toutes les améliorations sans isoler les autres facteurs", "C) Présenter le ROI trop tôt avant 6 mois", "D) Inclure les gains de productivité indirects"], "correct": "B", "explanation": "Il faut isoler l'impact AI des autres variables (saison, recrutement, produit).", "module": 3},
                {"id": 19, "question": "Quel marché MENA a le cycle de décision B2B le plus court ?", "options": ["A) Algérie", "B) Arabie Saoudite", "C) Tunisie", "D) Émirats Arabes Unis (UAE)"], "correct": "D", "explanation": "Les UAE ont un cycle de décision rapide, orienté ROI immédiat et tech-friendly.", "module": 3},
                {"id": 20, "question": "Quel est le score minimum requis pour la certification Euklydia AI Sales Specialist ?", "options": ["A) 70% au test + 70/100 au projet", "B) 80% au test + 75/100 au projet", "C) 90% au test + 80/100 au projet", "D) 75% au test + 70/100 au projet"], "correct": "B", "explanation": "Certification Euklydia : 80% minimum au test + 75/100 minimum au projet.", "module": 3},
            ],
            "passing_score": 80,
            "duration_min": 30,
        },
        content_en={
            "instructions": "This test covers all 3 modules. 30 minutes. Minimum score: 16/20 (80%).",
            "passing_score": 80,
            "duration_min": 30,
        },
        hints_fr=[
            {"level": 1, "text": "Relisez les key takeaways de chaque module avant de commencer le test."},
        ],
    ))
    db.flush()

    # ── Leçon Cert.2 — Projet de certification ───────────────────────────────
    l3_cert_2 = Lesson(
        unit_id=u3_cert.id, order=2,
        title_fr="Projet de certification — Dossier complet",
        title_en="Certification project — Complete portfolio",
        format="exercise", difficulty_level=5, estimated_duration_min=480,
        description_fr="Projet intégrateur final : dossier complet de transformation AI Sales. Évalué par le jury Euklydia sous 5 jours ouvrés.",
        description_en="Final integrative project: complete AI Sales transformation portfolio. Evaluated by Euklydia jury within 5 business days.",
        prerequisite_lesson_id=l3_cert_1.id,
    )
    db.add(l3_cert_2); db.flush()

    db.add(Activity(
        lesson_id=l3_cert_2.id, order=1, type="exercise",
        title_fr="Projet de certification — AI Sales Specialist Euklydia",
        title_en="Certification project — Euklydia AI Sales Specialist",
        is_assessed=True, is_required=True, passing_score=0,
        content_fr={
            "instructions": "6 livrables obligatoires. 7 jours après validation du test pour soumettre.",
            "livrables": [
                {"id": 1, "titre": "Diagnostic de maturité AI", "description": "Évaluation 5 piliers avec score actuel, cible et justification.", "format": "2 pages maximum"},
                {"id": 2, "titre": "Stratégie AI Sales 12 mois", "description": "Vision, OKRs mesurables, feuille de route 4 phases, budget par outil.", "format": "3 à 5 pages"},
                {"id": 3, "titre": "Plan de formation équipe", "description": "Programme 4 semaines, méthode cascade, indicateurs d'adoption.", "format": "2 pages"},
                {"id": 4, "titre": "Politique AI Sales", "description": "Document officiel avec usages autorisés/interdits, gouvernance données, responsabilités.", "format": "3 à 5 pages"},
                {"id": 5, "titre": "Dashboard ROI", "description": "Captures HubSpot + calcul ROI projeté 12 mois avec méthodologie transparente.", "format": "1 à 2 pages + captures"},
                {"id": 6, "titre": "Présentation direction", "description": "Pitch 10-15 slides pour convaincre un comité de direction. Réponses aux 4 objections types.", "format": "PDF ou PowerPoint"},
            ],
            "criteres_evaluation": {
                "diagnostic_maturite": "15%",
                "strategie_12_mois": "25%",
                "plan_formation": "15%",
                "politique_ai_sales": "15%",
                "dashboard_roi": "15%",
                "presentation_direction": "15%",
            },
            "score_minimum": 75,
            "delai_soumission": "7 jours après validation du test",
            "feedback": "Jury Euklydia — 2 membres — dans les 5 jours ouvrés",
            "certification_obtenue": {
                "badge": "Badge LinkedIn officiel AI Sales Specialist",
                "certificat": "Certificat PDF signé Euklydia",
                "annuaire": "Inscription Annuaire Euklydia MENA",
                "validite": "2 ans",
            },
        },
        content_en={
            "instructions": "6 mandatory deliverables. 7 days after test validation to submit.",
            "minimum_score": 75,
            "deadline": "7 days after test validation",
            "feedback": "Euklydia jury — 2 members — within 5 business days",
        },
        rubric_fr={"criteres": [
            {"nom": "Diagnostic de maturité AI", "poids": 0.15, "description": "Évaluation honnête, cohérente et justifiée des 5 piliers."},
            {"nom": "Stratégie AI Sales 12 mois", "poids": 0.25, "description": "Vision claire, OKRs mesurables, feuille de route réaliste et budgétée."},
            {"nom": "Plan de formation équipe", "poids": 0.15, "description": "Programme faisable, méthode cascade, indicateurs d'adoption concrets."},
            {"nom": "Politique AI Sales", "poids": 0.15, "description": "Document opérationnel, conforme aux lois MENA, usages bien définis."},
            {"nom": "Dashboard ROI", "poids": 0.15, "description": "Calcul ROI méthodologiquement correct, KPIs pertinents, visuels HubSpot."},
            {"nom": "Présentation direction", "poids": 0.15, "description": "Pitch convaincant, arguments chiffrés, réponses aux objections solides."},
        ]},
    ))
    db.flush()


    db.commit()
    print("✅ AI Sales Specialist — units, lessons, activities insérées")
    print("   Module 1 : 5 unités, 14 leçons (contenu complet)")
    print("   Module 2 : 5 unités, 14 leçons (contenu complet)")
    print("   Module 3 : 6 unités, 16 leçons (+ certification finale)")
    print("   Total    : 16 unités, 44 leçons")