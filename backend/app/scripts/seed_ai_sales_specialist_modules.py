from app.models.module import Module
from app.models.module_skill import ModuleSkill
from app.models.skill import Skill


def seed_ai_sales_specialist_modules(db):
    # =============================
    # Récupérer les skills AI Sales Specialist (career_path_id = 79)
    # =============================
    skills = db.query(Skill).filter(Skill.career_path_id == 79).order_by(Skill.id.desc()).limit(5).all()
    skills = list(reversed(skills))
    if not skills:
        print("❌ Aucun skill trouvé pour AI Sales Specialist (career_path_id=79)")
        return

    skill_ids = [s.id for s in skills]
    print(f"✅ Skills trouvés : {[s.name for s in skills]}")

    # =============================
    # Supprimer les anciens modules de ce rôle
    # =============================
    existing_modules = db.query(Module).filter(Module.role == "AI Sales Specialist").all()
    for m in existing_modules:
        db.query(ModuleSkill).filter(ModuleSkill.module_id == m.id).delete()
        db.delete(m)
    db.flush()

    # =============================
    # MODULE 1 — Fondations (Débutant)
    # =============================
    module_fondations = Module(
        title_en="AI Sales Specialist — Foundations",
        title_fr="AI Sales Specialist — Fondations",
        description_en=(
            "Your first steps with AI in sales. Learn to use ChatGPT for emails, "
            "understand CRM AI basics, identify hot prospects, and apply ethical principles "
            "in the MENA market context."
        ),
        description_fr=(
            "Vos premiers pas avec l'AI dans la vente. Apprenez à utiliser ChatGPT pour les emails, "
            "comprendre les bases du CRM AI, identifier les prospects chauds et appliquer "
            "les principes éthiques dans le contexte du marché Afrique du Nord."
        ),
        learning_objective_en=(
            "Use ChatGPT to write prospecting emails, read a CRM AI report, "
            "identify hot prospects, create simple prompts for sales, "
            "and respect basic ethical rules."
        ),
        learning_objective_fr=(
            "Utiliser ChatGPT pour rédiger des emails de prospection, lire un rapport CRM AI, "
            "identifier les prospects chauds, créer des prompts simples pour la vente "
            "et respecter les règles éthiques de base."
        ),
        level="Beginner",
        estimated_duration_min=180,
        format="video + quiz + practical exercises",
        role="AI Sales Specialist",
        journey_stage="foundation",
        display_order=1,
        expected_outcome_fr=(
            "À la fin de ce module, l'apprenant utilise ChatGPT quotidiennement pour rédiger "
            "ses emails de prospection, a configuré HubSpot AI avec son pipeline Afrique du Nord, "
            "identifie ses leads chauds grâce au scoring, et applique les règles éthiques de base."
        ),
        expected_outcome_en=(
            "By the end of this module, the learner uses ChatGPT daily to write prospecting emails, "
            "has configured HubSpot AI with their North Africa pipeline, identifies hot leads via scoring, "
            "and applies basic ethical rules."
        ),
        key_concepts_en=[
            "AI in sales: what it changes today",
            "Essential sales AI tools (ChatGPT, HubSpot AI, Zoho AI)",
            "CRM basics and AI lead scoring",
            "First prospection AI prompt",
            "Writing personalised emails in Arabic and French",
            "Basic AI ethics in sales",
        ],
        key_concepts_fr=[
            "L'AI dans la vente : ce qu'elle change aujourd'hui",
            "Outils AI essentiels du commercial (ChatGPT, HubSpot AI, Zoho AI)",
            "Bases du CRM et scoring de leads AI",
            "Premier prompt de prospection AI",
            "Rédiger des emails personnalisés en arabe et français",
            "Éthique AI basique dans la vente",
        ],
        # ── Quiz questions (toutes les unités) ──────────────────────────────
        quiz_questions_fr=[
            # Unité 1
            {
                "unite": 1,
                "lecon": 1,
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
                "unite": 1,
                "lecon": 2,
                "question": "Quel outil est un CRM avec AI intégré ?",
                "options": ["A) Canva", "B) Midjourney", "C) HubSpot AI", "D) Runway ML"],
                "correct": "C",
                "explanation": "HubSpot AI est un CRM qui intègre l'intelligence artificielle nativement pour le scoring et la rédaction."
            },
            {
                "unite": 1,
                "lecon": 3,
                "question": "Quelle est la meilleure pratique éthique quand on utilise ChatGPT pour ses emails ?",
                "options": [
                    "A) Envoyer l'email généré sans le lire",
                    "B) Relire, personnaliser et adapter l'email avant envoi",
                    "C) Copier exactement ce que ChatGPT génère",
                    "D) Utiliser ChatGPT uniquement pour les clients VIP"
                ],
                "correct": "B",
                "explanation": "L'AI assiste le commercial mais l'humain doit toujours valider et personnaliser."
            },
            # Unité 2
            {
                "unite": 2,
                "lecon": 1,
                "question": "Que signifie l'acronyme CRM ?",
                "options": [
                    "A) Computer Revenue Management",
                    "B) Customer Relationship Management",
                    "C) Commercial Results Monitoring",
                    "D) Client Reporting Module"
                ],
                "correct": "B",
                "explanation": "CRM = Customer Relationship Management — la gestion de la relation client."
            },
            {
                "unite": 2,
                "lecon": 2,
                "question": "Quel est le principal avantage d'un CRM avec AI par rapport à Excel ?",
                "options": [
                    "A) Excel coûte plus cher",
                    "B) Le CRM centralise tout, automatise les rappels et permet la collaboration en équipe",
                    "C) Excel ne peut pas stocker des noms de clients",
                    "D) Le CRM est uniquement pour les grandes entreprises"
                ],
                "correct": "B",
                "explanation": "Le CRM AI est proactif — il analyse les données et fait des recommandations, contrairement à Excel qui est passif."
            },
            {
                "unite": 2,
                "lecon": 3,
                "question": "Le scoring AI HubSpot peut sembler imprécis au début. Pourquoi ?",
                "options": [
                    "A) HubSpot AI est défaillant pour les marchés MENA",
                    "B) Il a besoin de données d'interactions pour s'améliorer — normal avec peu de données initiales",
                    "C) La version gratuite ne supporte pas le scoring",
                    "D) Il faut payer pour activer cette fonctionnalité"
                ],
                "correct": "B",
                "explanation": "Le scoring AI s'améliore avec le temps et les données. Il est normal qu'il soit moins précis au démarrage."
            },
            # Unité 3
            {
                "unite": 3,
                "lecon": 1,
                "question": "Quelle est la définition correcte de la prospection commerciale ?",
                "options": [
                    "A) L'ensemble des actions pour fidéliser les clients existants",
                    "B) L'ensemble des actions pour identifier, contacter et qualifier des clients potentiels",
                    "C) La gestion des réclamations clients",
                    "D) La rédaction de propositions commerciales"
                ],
                "correct": "B",
                "explanation": "La prospection est la première étape du cycle de vente — identifier et qualifier des clients potentiels."
            },
            {
                "unite": 3,
                "lecon": 2,
                "question": "Que signifie ICP dans le contexte de la prospection commerciale ?",
                "options": [
                    "A) International Commercial Process",
                    "B) Ideal Customer Profile — Profil du Client Idéal",
                    "C) Integrated CRM Platform",
                    "D) Intelligent Contact Priority"
                ],
                "correct": "B",
                "explanation": "L'ICP est la description précise du client idéal qui achète le plus facilement et reste le plus longtemps."
            },
            {
                "unite": 3,
                "lecon": 3,
                "question": "Quels sont les 5 éléments d'un bon prompt de prospection ?",
                "options": [
                    "A) Titre, corps, signature, objet, pièce jointe",
                    "B) Rôle, contexte, objectif, contraintes, personnalisation",
                    "C) Langue, ton, longueur, format, destinataire",
                    "D) Introduction, problème, solution, prix, conclusion"
                ],
                "correct": "B",
                "explanation": "Un prompt efficace contient : rôle (qui joue l'AI), contexte, objectif, contraintes et personnalisation."
            },
            # Unité 4
            {
                "unite": 4,
                "lecon": 1,
                "question": "Quel est l'élément le plus important d'un email commercial pour décider s'il sera ouvert ?",
                "options": ["A) La signature", "B) L'objet", "C) La longueur du message", "D) La pièce jointe"],
                "correct": "B",
                "explanation": "47% des destinataires décident d'ouvrir ou non un email uniquement sur la base de l'objet."
            },
            {
                "unite": 4,
                "lecon": 2,
                "question": "Un client tunisien vous répond en arabe. Quelle langue utilisez-vous pour répondre ?",
                "options": [
                    "A) Français, car c'est plus professionnel",
                    "B) Anglais, car c'est la langue internationale",
                    "C) Arabe standard, pour respecter la langue de votre interlocuteur",
                    "D) La darija tunisienne pour être plus proche"
                ],
                "correct": "C",
                "explanation": "Toujours répondre dans la langue de confort du prospect. L'arabe standard est la norme B2B écrite."
            },
            {
                "unite": 4,
                "lecon": 3,
                "question": "Quelle est la longueur idéale d'un email de prospection froide ?",
                "options": [
                    "A) 50 mots — plus c'est court, mieux c'est",
                    "B) 300 mots — il faut tout expliquer en détail",
                    "C) 120 à 150 mots — suffisant pour capter l'attention",
                    "D) 500 mots — pour montrer le sérieux de votre démarche"
                ],
                "correct": "C",
                "explanation": "120-150 mots est la longueur optimale pour un email de prospection froide B2B."
            },
            # Unité 5
            {
                "unite": 5,
                "lecon": 1,
                "question": "Un commercial copie le contrat d'un client dans ChatGPT. Que fait-il de problématique ?",
                "options": [
                    "A) Rien — ChatGPT est un outil sécurisé",
                    "B) Il expose des données confidentielles d'un client à un tiers sans autorisation",
                    "C) Il perd du temps inutilement",
                    "D) Il enfreint uniquement les règles de son entreprise"
                ],
                "correct": "B",
                "explanation": "Les données confidentielles ne doivent jamais être partagées dans des outils AI publics — règle de respect des données."
            },
            {
                "unite": 5,
                "lecon": 2,
                "question": "Pourquoi l'éthique AI est-elle particulièrement importante en MENA ?",
                "options": [
                    "A) Parce que les lois MENA sont plus strictes que les lois européennes",
                    "B) Parce que la confiance personnelle est au cœur de la relation commerciale en MENA",
                    "C) Parce que les outils AI ne fonctionnent pas bien en arabe",
                    "D) Parce que les clients MENA n'utilisent pas internet"
                ],
                "correct": "B",
                "explanation": "En MENA, la confiance est la monnaie principale de l'échange commercial. Une violation éthique détruit cette confiance."
            },
        ],
        quiz_questions_en=[
            {
                "unite": 1, "lecon": 1,
                "question": "What does AI mainly allow a salesperson to do?",
                "options": [
                    "A) Completely replace the salesperson",
                    "B) Analyse, predict and automate to work more efficiently",
                    "C) Eliminate the need for a CRM",
                    "D) Call clients automatically"
                ],
                "correct": "B",
                "explanation": "AI analyses, predicts and automates. It amplifies the salesperson's efficiency without replacing them."
            },
            {
                "unite": 1, "lecon": 2,
                "question": "Which tool is a CRM with integrated AI?",
                "options": ["A) Canva", "B) Midjourney", "C) HubSpot AI", "D) Runway ML"],
                "correct": "C",
                "explanation": "HubSpot AI is a CRM that natively integrates artificial intelligence for scoring and writing assistance."
            },
        ],
        # ── Prompt examples ─────────────────────────────────────────────────
        prompt_examples_fr=[
            {
                "unite": 3,
                "lecon": 3,
                "titre": "Prompt email de prospection froide — B2B Tunisie",
                "prompt": (
                    "Tu es un expert commercial B2B spécialisé dans les PME tunisiennes. "
                    "Rédige un email de prospection froide en français pour contacter [NOM DU PROSPECT], "
                    "[POSTE] chez [NOM ENTREPRISE], une entreprise de [SECTEUR] basée à [VILLE]. "
                    "Mon produit est [DESCRIPTION PRODUIT]. Le problème que je résous est [PROBLÈME PRINCIPAL]. "
                    "L'email doit faire 120 à 150 mots, avoir un objet accrocheur, être chaleureux et respectueux "
                    "des codes culturels tunisiens, et se terminer par une demande de rendez-vous de 20 minutes."
                ),
                "usage": "Premier contact avec un prospect inconnu en Tunisie"
            },
            {
                "unite": 3,
                "lecon": 3,
                "titre": "Prompt message de relance après silence",
                "prompt": (
                    "Tu es un commercial B2B expérimenté en Tunisie. Rédige un message de relance en français "
                    "pour [NOM DU PROSPECT] qui n'a pas répondu à mon email envoyé il y a [X] jours. "
                    "Le ton doit être cordial et non insistant, adapté à la culture MENA. "
                    "Le message doit faire 60 à 80 mots et proposer une alternative simple."
                ),
                "usage": "Relance d'un prospect silencieux après 5-7 jours"
            },
            {
                "unite": 4,
                "lecon": 1,
                "titre": "Prompt objet d'email — 3 variantes",
                "prompt": (
                    "Génère 3 variantes d'objet d'email pour un commercial qui prospecte [POSTE] "
                    "dans le secteur [SECTEUR] en Tunisie. Les objets doivent être accrocheurs, "
                    "personnalisés et adaptés au contexte MENA. Évite les objets génériques comme "
                    "'Notre solution pour votre entreprise'."
                ),
                "usage": "Tester différents objets pour améliorer le taux d'ouverture"
            },
            {
                "unite": 4,
                "lecon": 2,
                "titre": "Prompt traduction-adaptation email en arabe",
                "prompt": (
                    "Traduis et adapte cet email commercial en arabe standard (arabe littéraire moderne). "
                    "L'email est destiné à [POSTE DU PROSPECT] dans une entreprise [SECTEUR] en [PAYS]. "
                    "Assure-toi que le ton est professionnel et respectueux selon les codes culturels arabes, "
                    "que les formules de politesse sont appropriées, et que le message reste naturel "
                    "et ne sonne pas comme une traduction littérale.\n\n"
                    "Voici l'email en français : [EMAIL]"
                ),
                "usage": "Adapter un email français en arabe standard pour les marchés arabophones"
            },
        ],
        prompt_examples_en=[
            {
                "unite": 3, "lecon": 3,
                "title": "Cold prospection email prompt — B2B Tunisia",
                "prompt": (
                    "You are a B2B sales expert specialised in Tunisian SMEs. "
                    "Write a cold prospection email in French for [PROSPECT NAME], "
                    "[JOB TITLE] at [COMPANY NAME], a [SECTOR] company based in [CITY]. "
                    "My product is [PRODUCT DESCRIPTION]. The problem I solve is [MAIN PROBLEM]. "
                    "The email should be 120-150 words, have a catchy subject, be warm and respectful "
                    "of Tunisian cultural codes, and end with a request for a 20-minute meeting."
                ),
                "usage": "First contact with an unknown prospect in Tunisia"
            },
        ],
        # ── Practical exercises ──────────────────────────────────────────────
        practical_exercise_fr={
            "module": "Fondations",
            "exercises": [
                {
                    "unite": 2,
                    "lecon": 1,
                    "titre": "Cartographier votre pipeline commercial",
                    "consigne": (
                        "Prenez votre liste actuelle de prospects (même si elle est dans Excel ou dans un carnet). "
                        "Identifiez dans quelle étape du pipeline se trouve chacun d'eux. "
                        "Comptez combien de prospects vous avez par étape. "
                        "Identifiez l'étape où vous avez le plus de blocages."
                    ),
                    "livrable": "Un tableau manuscrit ou numérique avec vos prospects répartis en 6 étapes",
                    "duree_estimee": "20 minutes"
                },
                {
                    "unite": 3,
                    "lecon": 2,
                    "titre": "Définir mon ICP et identifier mes 5 prospects prioritaires",
                    "consigne": (
                        "Part 1 : Remplissez la fiche ICP avec vos propres critères, "
                        "basés sur vos 3 meilleurs clients actuels.\n"
                        "Part 2 : Dans votre CRM HubSpot, filtrez vos contacts par le score le plus élevé. "
                        "Identifiez les 5 contacts qui correspondent le mieux à votre ICP. "
                        "Pour chacun, notez pourquoi il correspond à votre ICP."
                    ),
                    "livrable": "Votre fiche ICP remplie + liste de 5 prospects prioritaires avec justification",
                    "criteres": "ICP complet et cohérent (50%), pertinence des 5 prospects sélectionnés (50%)",
                    "duree_estimee": "30 minutes"
                },
                {
                    "unite": 4,
                    "lecon": 3,
                    "titre": "Mon premier email de prospection AI (Exercice noté)",
                    "consigne": (
                        "1. Choisissez l'un de vos 5 prospects prioritaires identifiés.\n"
                        "2. Rédigez un prompt complet en utilisant la structure en 5 éléments.\n"
                        "3. Soumettez votre prompt à ChatGPT et obtenez un email de prospection.\n"
                        "4. Personnalisez l'email généré (minimum 3 modifications personnelles).\n"
                        "5. Soumettez sur la plateforme : votre prompt + email généré + email personnalisé."
                    ),
                    "livrable": "Prompt + email généré + email personnalisé",
                    "criteres": {
                        "qualite_prompt": "30%",
                        "pertinence_email": "30%",
                        "qualite_personnalisation": "40%"
                    },
                    "score_minimum": 70,
                    "duree_estimee": "30 minutes"
                },
            ]
        },
        practical_exercise_en={
            "module": "Foundations",
            "exercises": [
                {
                    "unite": 4, "lecon": 3,
                    "title": "My first AI prospection email (Graded exercise)",
                    "instructions": (
                        "1. Choose one of your 5 priority prospects.\n"
                        "2. Write a complete prompt using the 5-element structure.\n"
                        "3. Submit your prompt to ChatGPT and get a prospection email.\n"
                        "4. Personalise the generated email (minimum 3 personal modifications).\n"
                        "5. Submit on the platform: your prompt + generated email + personalised email."
                    ),
                    "deliverable": "Prompt + generated email + personalised email",
                    "minimum_score": 70,
                    "estimated_duration": "30 minutes"
                }
            ]
        },
        # ── Comparison tables ────────────────────────────────────────────────
        comparison_tables_fr={
            "outils_ai_fondations": {
                "titre": "Stack AI pour commercial débutant MENA",
                "colonnes": ["Outil", "Usage principal", "Pour qui ?", "Prix"],
                "lignes": [
                    ["ChatGPT", "Rédiger emails, scripts, prompts", "Tout niveau", "Gratuit / 20$/mois"],
                    ["HubSpot AI", "CRM + scoring leads + emails", "Débutant", "Gratuit → 20$/mois"],
                    ["Zoho CRM AI", "CRM adapté PME MENA", "Débutant/Inter.", "14$/mois"],
                    ["Brevo", "Email marketing, populaire MENA", "Débutant", "Gratuit → 25$/mois"],
                    ["Google Analytics AI", "Analyser comportement prospects", "Tout niveau", "Gratuit"],
                ]
            },
            "excel_vs_crm": {
                "titre": "Excel vs CRM — Comparaison",
                "colonnes": ["Critère", "Avec Excel", "Avec un CRM AI"],
                "lignes": [
                    ["Organisation des données", "Dispersées dans plusieurs fichiers", "Tout centralisé en un seul endroit"],
                    ["Rappels automatiques", "Aucun rappel", "Rappels et tâches automatiques"],
                    ["Collaboration équipe", "Pas de collaboration temps réel", "Équipe synchronisée en temps réel"],
                    ["Historique interactions", "Pas d'historique conversations", "Historique complet de chaque interaction"],
                    ["Analyse automatique", "Aucune analyse automatique", "Tableaux de bord et rapports automatiques"],
                ]
            },
            "emails_bons_mauvais_objets": {
                "titre": "Objets d'emails : à éviter vs efficaces",
                "colonnes": ["❌ Objet à éviter", "✅ Objet efficace"],
                "lignes": [
                    ["Notre solution pour votre entreprise", "Comment [Entreprise X] a doublé ses RDV en 3 semaines"],
                    ["Présentation de nos services", "Une question rapide sur votre processus commercial, M. Ben Ali"],
                    ["Offre spéciale pour vous", "3 PME tunisiennes de votre secteur ont résolu ce problème"],
                    ["Partenariat potentiel", "Vous perdez peut-être des prospects sans le savoir"],
                ]
            }
        },
        comparison_tables_en={
            "ai_tools_foundations": {
                "title": "AI Stack for Beginner MENA Salesperson",
                "columns": ["Tool", "Main use", "For who?", "Price"],
                "rows": [
                    ["ChatGPT", "Write emails, scripts, prompts", "All levels", "Free / $20/month"],
                    ["HubSpot AI", "CRM + lead scoring + emails", "Beginner", "Free → $20/month"],
                    ["Brevo", "Email marketing, popular in MENA", "Beginner", "Free → $25/month"],
                ]
            }
        },
        # ── Role-based examples (cas pratiques MENA) ────────────────────────
        role_based_example_fr=(
            "Cas Fatima — Commerciale à Tunis :\n"
            "Fatima avait 150 prospects dans son CRM. Normalement, elle passait 2 heures par jour "
            "à décider qui appeler en premier. Avec HubSpot AI, en 5 minutes, l'outil identifie "
            "les 15 prospects les plus chauds de la semaine. Fatima passe ses 2 heures à appeler "
            "ces 15 personnes avec un message personnalisé généré en partie par ChatGPT.\n\n"
            "Résultat : 4 rendez-vous obtenus contre 1 ou 2 habituellement.\n\n"
            "Cas ICP — Sonia (EdTech Tunis) :\n"
            "Sonia avait 200 prospects sans priorité. Elle a défini son ICP : directeurs de lycées "
            "privés, région Grand Tunis, budget > 2000 TND/an. Apollo.io lui a identifié 34 contacts "
            "correspondant exactement. En 2 semaines : 8 rendez-vous — contre 1 habituellement."
        ),
        role_based_example_en=(
            "Case Fatima — Salesperson in Tunis:\n"
            "Fatima had 150 prospects in her CRM and spent 2 hours daily deciding who to call first. "
            "With HubSpot AI, in 5 minutes, the tool identifies the 15 hottest prospects of the week. "
            "Fatima uses her 2 hours to call these 15 people with a personalised message generated "
            "partly by ChatGPT.\n\nResult: 4 meetings booked instead of 1-2 previously."
        ),
        action_point_fr=(
            "1. Créer votre compte HubSpot gratuit cette semaine\n"
            "2. Configurer votre pipeline en 6 étapes adaptées au marché MENA\n"
            "3. Ajouter 10 contacts et créer 3 deals\n"
            "4. Rédiger votre premier email de prospection avec ChatGPT\n"
            "5. Définir votre ICP en vous basant sur vos 3 meilleurs clients actuels"
        ),
        action_point_en=(
            "1. Create your free HubSpot account this week\n"
            "2. Configure your pipeline with 6 MENA-adapted stages\n"
            "3. Add 10 contacts and create 3 deals\n"
            "4. Write your first prospection email with ChatGPT\n"
            "5. Define your ICP based on your 3 best current clients"
        ),
        # ── Section content (structure complète) ────────────────────────────
        section_content_fr={
            "unite1": {
                "title": "Unité 1 — L'AI dans la vente",
                "duration": "~26 minutes",
                "lessons": [
                    {"id": "1.1", "title": "C'est quoi l'AI pour un commercial ?", "format": "Vidéo 10 min + Quiz", "description": "Définition de l'AI, 4 usages commerciaux (scoring, rédaction, prédiction churn, analyse), ce que l'AI ne fait pas, règle d'or AI + Humain."},
                    {"id": "1.2", "title": "Les outils AI du commercial", "format": "Vidéo 8 min + Tableau comparatif", "description": "5 catégories d'outils AI, focus ChatGPT + HubSpot AI pour débutants, conseil : maîtriser les outils gratuits avant d'investir."},
                    {"id": "1.3", "title": "L'AI dans le contexte MENA", "format": "Vidéo 8 min + Forum discussion", "description": "Réalités du marché MENA, opportunités (gap digitalisation, multilinguisme), défis (langue arabe, confiance client, budget), calendrier saisonnier."},
                ]
            },
            "unite2": {
                "title": "Unité 2 — Mon premier CRM avec AI",
                "duration": "~34 minutes + tutoriel",
                "lessons": [
                    {"id": "2.1", "title": "C'est quoi un CRM ?", "format": "Vidéo 12 min + Exercice", "description": "Définition CRM, 5 fonctions essentielles, pipeline en 6 étapes adapté MENA, Excel vs CRM, exercice cartographie pipeline."},
                    {"id": "2.2", "title": "Comment l'AI améliore le CRM", "format": "Vidéo 10 min + Quiz", "description": "4 super-pouvoirs AI : scoring, churn, suggestions, rédaction. Cas Karim à Sfax (1 → 5 deals). Règle d'or AI + Humain."},
                    {"id": "2.3", "title": "Mon premier CRM en pratique", "format": "Tutoriel HubSpot pas à pas", "description": "6 étapes : création compte, pipeline, contacts, deals, scoring. Exercice noté : 5 contacts + 3 deals + pipeline capture."},
                ]
            },
            "unite3": {
                "title": "Unité 3 — Ma première prospection AI",
                "duration": "~26 minutes + exercices",
                "lessons": [
                    {"id": "3.1", "title": "C'est quoi la prospection ?", "format": "Vidéo 8 min + Quiz", "description": "3 types de prospection (froide/tiède/chaude), processus en 5 étapes, codes culturels MENA (confiance, Ramadan, WhatsApp vs LinkedIn)."},
                    {"id": "3.2", "title": "Identifier les bons prospects", "format": "Vidéo 10 min + Exercice", "description": "Définir son ICP, méthode BANT, signaux d'achat AI, cas Sonia EdTech (1 → 8 rendez-vous)."},
                    {"id": "3.3", "title": "Mon premier prompt de prospection", "format": "Tutoriel + Exercice noté", "description": "Structure en 5 éléments, bibliothèque de 4 prompts MENA prêts à l'emploi, erreurs à éviter."},
                ]
            },
            "unite4": {
                "title": "Unité 4 — Mon premier email AI",
                "duration": "~32 minutes + exercice noté",
                "lessons": [
                    {"id": "4.1", "title": "Rédiger avec ChatGPT", "format": "Vidéo 12 min + Démonstration", "description": "6 éléments d'un email efficace, l'objet comme clé de l'ouverture, tableau objets bons vs mauvais, démonstration live M. Hamdi à Sousse."},
                    {"id": "4.2", "title": "Personnaliser en arabe et français", "format": "Vidéo 8 min + Exercice", "description": "Règle fondamentale : langue du prospect. Prompt traduction-adaptation culturelle. Formules de politesse arabes. Erreurs fréquentes."},
                    {"id": "4.3", "title": "Mon premier email de prospection", "format": "Exercice pratique noté", "description": "Fiche prospect, prompt complet, email FR + AR, grille d'évaluation 100 points, score minimum 70/100."},
                ]
            },
            "unite5": {
                "title": "Unité 5 — Éthique AI basique",
                "duration": "~22 minutes + cas pratiques",
                "lessons": [
                    {"id": "5.1", "title": "Les règles fondamentales", "format": "Vidéo 10 min + Quiz éthique", "description": "5 règles : transparence, validation humaine, respect données, non-manipulation, équité. Tableau ligne rouge vs alternative. Test éthique personnel."},
                    {"id": "5.2", "title": "Cas pratiques éthiques simples", "format": "Cas interactifs", "description": "6 situations éthiques réelles : email trop parfait, données confidentielles, fausse urgence, témoignage inventé, scoring discriminatoire, email sans relecture."},
                ]
            },
            "test_final": {
                "title": "Test Final — Fondations",
                "format": "10 questions QCM",
                "duration": "30 minutes",
                "score_minimum": "8/10",
                "acces_suivant": "Module 2 — Pratique"
            }
        },
        section_content_en={
            "unite1": {
                "title": "Unit 1 — AI in Sales",
                "duration": "~26 minutes",
                "lessons": [
                    {"id": "1.1", "title": "What is AI for a salesperson?", "format": "10 min video + Quiz"},
                    {"id": "1.2", "title": "Sales AI tools", "format": "8 min video + Comparison table"},
                    {"id": "1.3", "title": "AI in the MENA context", "format": "8 min video + Forum"},
                ]
            },
            "unite2": {
                "title": "Unit 2 — My First CRM with AI",
                "duration": "~34 minutes + tutorial",
                "lessons": [
                    {"id": "2.1", "title": "What is a CRM?", "format": "12 min video + Exercise"},
                    {"id": "2.2", "title": "How AI improves CRM", "format": "10 min video + Quiz"},
                    {"id": "2.3", "title": "My first CRM in practice", "format": "HubSpot step-by-step tutorial"},
                ]
            },
            "unite3": {
                "title": "Unit 3 — My First AI Prospection",
                "duration": "~26 minutes + exercises",
                "lessons": [
                    {"id": "3.1", "title": "What is prospection?", "format": "8 min video + Quiz"},
                    {"id": "3.2", "title": "Identify the right prospects", "format": "10 min video + Exercise"},
                    {"id": "3.3", "title": "My first prospection prompt", "format": "Tutorial + Graded exercise"},
                ]
            },
            "unite4": {
                "title": "Unit 4 — My First AI Email",
                "duration": "~32 minutes + graded exercise",
                "lessons": [
                    {"id": "4.1", "title": "Writing with ChatGPT", "format": "12 min video + Demo"},
                    {"id": "4.2", "title": "Personalise in Arabic and French", "format": "8 min video + Exercise"},
                    {"id": "4.3", "title": "My first prospection email", "format": "Graded practical exercise"},
                ]
            },
            "unite5": {
                "title": "Unit 5 — Basic AI Ethics",
                "duration": "~22 minutes + interactive cases",
                "lessons": [
                    {"id": "5.1", "title": "Fundamental rules", "format": "10 min video + Ethics quiz"},
                    {"id": "5.2", "title": "Simple ethical case studies", "format": "Interactive cases"},
                ]
            },
            "final_test": {
                "title": "Final Test — Foundations",
                "format": "10 MCQ questions",
                "duration": "30 minutes",
                "minimum_score": "8/10",
                "next_access": "Module 2 — Practice"
            }
        },
        takeaway_fr="L'AI ne remplace pas le commercial — elle lui permet de se concentrer sur les prospects les plus prometteurs.",
        takeaway_en="AI does not replace the salesperson — it allows them to focus on the most promising prospects.",
        recommended_when_fr="Recommandé quand votre score est 0/2 sur un ou plusieurs skills (niveau Débutant).",
        recommended_when_en="Recommended when your score is 0/2 on one or more skills (Beginner level).",
        why_this_module_fr="Avant d'utiliser les outils AI de vente, vous avez besoin de comprendre les fondamentaux et le contexte Afrique du Nord.",
        why_this_module_en="Before using sales AI tools, you need to understand the fundamentals and the North Africa context.",
        next_recommended_module_fr="AI Sales Specialist — Pratique",
        next_recommended_module_en="AI Sales Specialist — Practice",
        is_active=True,
    )
    db.add(module_fondations)
    db.flush()

    # =============================
    # MODULE 2 — Pratique (Intermédiaire)
    # =============================
    module_pratique = Module(
        title_en="AI Sales Specialist — Practice",
        title_fr="AI Sales Specialist — Pratique",
        description_en=(
            "Automate your prospection and analyse client data with AI. "
            "Create automated email sequences, master HubSpot AI and Zoho AI, "
            "personalise at scale for the North Africa market."
        ),
        description_fr=(
            "Automatisez votre prospection et analysez les données clients avec l'AI. "
            "Créez des séquences d'emails automatisées, maîtrisez HubSpot AI et Zoho AI, "
            "personnalisez à grande échelle pour le marché Afrique du Nord."
        ),
        learning_objective_en=(
            "Create automated prospection sequences, analyse client data with AI, "
            "personalise 100 messages in 1 hour, master HubSpot AI and Zoho AI, "
            "manage data ethically."
        ),
        learning_objective_fr=(
            "Créer des séquences de prospection automatisées, analyser les données clients avec l'AI, "
            "personnaliser 100 messages en 1 heure, maîtriser HubSpot AI et Zoho AI, "
            "gérer les données éthiquement."
        ),
        level="Intermediate",
        estimated_duration_min=240,
        format="video + practical exercises + graded project",
        role="AI Sales Specialist",
        journey_stage="practice",
        display_order=2,
        expected_outcome_fr=(
            "À la fin de ce module, l'apprenant a une campagne de prospection automatisée active, "
            "lit et interprète les insights AI de son CRM, personnalise ses messages pour plusieurs "
            "marchés MENA simultanément, et gère les données clients de façon conforme."
        ),
        expected_outcome_en=(
            "By the end of this module, the learner has an active automated prospection campaign, "
            "reads and interprets AI insights from their CRM, personalises messages for multiple "
            "MENA markets simultaneously, and manages client data compliantly."
        ),
        key_concepts_en=[
            "Automated email sequences with HubSpot",
            "Analysing client data with AI",
            "Mass personalisation for MENA",
            "HubSpot AI and Zoho AI advanced features",
            "Integrating ChatGPT into CRM via Zapier",
            "Responsible data management (RGPD + MENA laws)",
        ],
        key_concepts_fr=[
            "Séquences d'emails automatisées avec HubSpot",
            "Analyser les données clients avec l'AI",
            "Personnalisation à grande échelle pour le MENA",
            "HubSpot AI et Zoho AI en profondeur",
            "Intégrer ChatGPT dans son CRM via Zapier",
            "Gestion responsable des données (RGPD + lois MENA)",
        ],
        quiz_questions_fr=[
            {
                "unite": 1, "lecon": 1,
                "question": "Qu'est-ce qui déclenche l'arrêt automatique d'une séquence HubSpot ?",
                "options": [
                    "A) L'expiration du délai de 21 jours automatiquement",
                    "B) La réponse du prospect à n'importe quel email de la séquence",
                    "C) Quand le prospect visite votre site web",
                    "D) Quand vous désactivez manuellement la séquence"
                ],
                "correct": "B",
                "explanation": "Les séquences HubSpot s'arrêtent automatiquement dès qu'un prospect répond, évitant les relances maladroites."
            },
            {
                "unite": 1, "lecon": 2,
                "question": "Quelle est la différence principale entre une séquence et un workflow dans HubSpot ?",
                "options": [
                    "A) La séquence envoie des emails ; le workflow ne peut qu'envoyer des SMS",
                    "B) La séquence envoie des emails à intervalles fixes ; le workflow déclenche des actions selon le comportement du prospect",
                    "C) Les workflows sont réservés aux comptes Enterprise",
                    "D) Il n'y a pas de différence pratique entre les deux"
                ],
                "correct": "B",
                "explanation": "Les séquences suivent le temps (J+3, J+7...). Les workflows suivent le comportement (a ouvert, a cliqué...)."
            },
            {
                "unite": 2, "lecon": 1,
                "question": "Un prospect a un lead score de 85 dans HubSpot. Que faire ?",
                "options": [
                    "A) L'inscrire dans une séquence de 21 jours",
                    "B) Attendre qu'il vous contacte",
                    "C) Le contacter dans les 2 heures avec une proposition personnalisée",
                    "D) Lui envoyer automatiquement votre brochure complète"
                ],
                "correct": "C",
                "explanation": "Un score de 85 + visite tarifaire = fenêtre d'achat ouverte. Chaque heure perdue réduit la probabilité de conversion."
            },
            {
                "unite": 2, "lecon": 2,
                "question": "Vous avez un deal de 25 000 TND avec une probabilité AI de 40%. Quel est son poids dans votre CA prévisionnel ?",
                "options": ["A) 25 000 TND", "B) 40 000 TND", "C) 10 000 TND", "D) 15 000 TND"],
                "correct": "C",
                "explanation": "CA prévisionnel = Valeur deal × Probabilité AI = 25 000 × 40% = 10 000 TND."
            },
            {
                "unite": 3, "lecon": 1,
                "question": "Pour une campagne de 80 prospects en 3 secteurs, quel niveau de personnalisation est optimal ?",
                "options": [
                    "A) Niveau 4 — hyper-personnalisation individuelle",
                    "B) Niveau 1 — uniquement le prénom",
                    "C) Niveau 2 — 3 variantes contextuelles par secteur avec tokens HubSpot",
                    "D) Aucune personnalisation"
                ],
                "correct": "C",
                "explanation": "Pour 80 prospects en 3 secteurs, le Niveau 2 est le meilleur rapport efficacité/effort."
            },
            {
                "unite": 4, "lecon": 2,
                "question": "Quelle est la principale raison pour laquelle Zoho CRM est populaire parmi les PME MENA ?",
                "options": [
                    "A) Zoho a plus de fonctionnalités AI que HubSpot",
                    "B) Zoho propose une interface en arabe, un prix bas (14$/mois) et des serveurs régionaux MENA",
                    "C) Zoho est uniquement disponible en MENA",
                    "D) Zoho est gratuit pour les PME tunisiennes"
                ],
                "correct": "B",
                "explanation": "Zoho gagne sur trois critères décisifs : interface en arabe, prix accessible et conformité des données locales."
            },
            {
                "unite": 5, "lecon": 1,
                "question": "Une PME tunisienne qui prospecte des clients en France est-elle soumise au RGPD ?",
                "options": [
                    "A) Non — le RGPD ne s'applique qu'aux entreprises européennes",
                    "B) Oui — si elle collecte des données de personnes résidant en Europe, le RGPD s'applique",
                    "C) Uniquement si elle a un bureau en Europe",
                    "D) Uniquement si elle réalise plus de 1 million d'euros de CA"
                ],
                "correct": "B",
                "explanation": "Le RGPD s'applique selon le lieu de résidence des prospects, pas le lieu de l'entreprise."
            },
        ],
        quiz_questions_en=[
            {
                "unite": 1, "lecon": 1,
                "question": "What triggers the automatic stop of a HubSpot sequence?",
                "options": [
                    "A) The expiry of the 21-day delay automatically",
                    "B) The prospect replying to any email in the sequence",
                    "C) When the prospect visits your website",
                    "D) When you manually deactivate the sequence"
                ],
                "correct": "B",
                "explanation": "HubSpot sequences automatically stop when a prospect replies, avoiding awkward follow-ups."
            },
        ],
        prompt_examples_fr=[
            {
                "unite": 1,
                "lecon": 1,
                "titre": "Prompt séquence email complète (5 emails en une requête)",
                "prompt": (
                    "Tu es un expert en vente B2B pour les PME tunisiennes. Rédige une séquence de 5 emails "
                    "de prospection pour [POSTE DU PROSPECT] dans le secteur [SECTEUR] à [VILLE]. "
                    "Mon produit est [PRODUIT]. Le problème que je résous est [PROBLÈME].\n\n"
                    "Pour chaque email, précise :\n"
                    "- Jour d'envoi\n"
                    "- Objet de l'email\n"
                    "- Corps du message (80 à 150 mots max)\n"
                    "- Angle différent : Email 1 = accroche valeur, Email 2 = preuve sociale, "
                    "Email 3 = angle problème, Email 4 = rupture, Email 5 = ressource utile\n\n"
                    "Ton : professionnel, chaleureux, adapté à la culture MENA."
                ),
                "usage": "Générer une séquence de prospection complète en une seule requête ChatGPT"
            },
            {
                "unite": 3,
                "lecon": 1,
                "titre": "Prompt batch — 4 variantes par segment MENA",
                "prompt": (
                    "Tu es un expert commercial B2B pour les PME tunisiennes. "
                    "Rédige 4 variantes d'un email de prospection pour les 4 segments suivants, "
                    "en gardant le même message de base mais en adaptant l'accroche et le ton :\n\n"
                    "Segment 1 : PME industrielle (textile, agroalimentaire), 20-100 employés, Sfax ou Sousse\n"
                    "Segment 2 : PME de services (conseil, IT), 5-30 employés, Grand Tunis\n"
                    "Segment 3 : PME commerciale (distribution, import-export), 10-50 employés\n"
                    "Segment 4 : Cabinet professionnel (médical, juridique), 2-15 personnes\n\n"
                    "Mon produit : [PRODUIT]. Problème résolu : [PROBLÈME]. Bénéfice principal : [BÉNÉFICE].\n"
                    "Chaque variante : 120-140 mots, objet spécifique au segment, "
                    "tokens {{ contact.firstname }} et {{ contact.company }}."
                ),
                "usage": "Personnalisation de masse pour campagnes MENA multi-segments"
            },
            {
                "unite": 4,
                "lecon": 3,
                "titre": "Prompt Zapier — Score > 70 déclencheur",
                "prompt": (
                    "Rédige un email de prospection personnalisé pour {{ contact.firstname }} {{ contact.lastname }}, "
                    "{{ contact.jobtitle }} chez {{ contact.company }} dans le secteur {{ contact.industry }} "
                    "à {{ contact.city }}. Mon produit est [PRODUIT]. "
                    "Ce prospect a un score élevé dans notre CRM — il est probablement en train d'évaluer notre offre. "
                    "L'email doit être direct, professionnel, faire 130 mots et proposer un call de 20 minutes. "
                    "Ton adapté à la culture MENA. Intégrer les tokens HubSpot."
                ),
                "usage": "Template Zapier déclenché automatiquement quand le score dépasse 70"
            },
        ],
        prompt_examples_en=[
            {
                "unite": 1, "lecon": 1,
                "title": "Full email sequence prompt (5 emails in one request)",
                "prompt": (
                    "You are a B2B sales expert for Tunisian SMEs. Write a 5-email prospection sequence "
                    "for [PROSPECT JOB TITLE] in the [SECTOR] sector in [CITY]. "
                    "My product is [PRODUCT]. The problem I solve is [PROBLEM].\n\n"
                    "For each email: send day, email subject, message body (80-150 words max), "
                    "different angle: Email 1=value hook, Email 2=social proof, Email 3=problem angle, "
                    "Email 4=breakup, Email 5=pure value resource."
                ),
                "usage": "Generate a full prospection sequence in a single ChatGPT request"
            },
        ],
        practical_exercise_fr={
            "module": "Pratique",
            "exercises": [
                {
                    "unite": 1,
                    "lecon": 3,
                    "titre": "Ma première campagne automatisée (Projet noté)",
                    "consigne": (
                        "1. Définir la cible : segment précis de votre marché (ICP en 3 lignes)\n"
                        "2. Identifier 10 prospects dans HubSpot correspondant à votre ICP\n"
                        "3. Rédiger la séquence avec ChatGPT (prompt séquence complète)\n"
                        "4. Configurer la séquence dans HubSpot (5 emails, délais, condition arrêt)\n"
                        "5. Configurer le workflow comportemental (2 déclencheurs minimum)\n"
                        "6. Inscrire les 10 prospects dans la séquence\n"
                        "7. Soumettre : tableau de bord + captures d'écran"
                    ),
                    "livrable": "Séquence HubSpot activée + workflow + 10 prospects inscrits + tableau de bord",
                    "criteres": {
                        "pertinence_icp": "15%",
                        "qualite_5_emails": "25%",
                        "configuration_sequence": "20%",
                        "configuration_workflow": "20%",
                        "prospects_inscrits": "10%",
                        "tableau_bord": "10%"
                    },
                    "score_minimum": 70,
                    "duree_estimee": "60-90 minutes"
                },
                {
                    "unite": 3,
                    "lecon": 3,
                    "titre": "Ma campagne personnalisée MENA (Projet noté)",
                    "consigne": (
                        "1. Définir votre offre\n"
                        "2. Constituer une liste de 20 prospects sur 2 marchés MENA minimum\n"
                        "3. Segmenter en minimum 3 segments\n"
                        "4. Générer les variantes emails avec ChatGPT (prompt batch)\n"
                        "5. Configurer les tokens dans HubSpot\n"
                        "6. Planifier les envois selon le calendrier saisonnier MENA\n"
                        "7. Soumettre le dossier complet"
                    ),
                    "livrable": "Dossier : segmentation + 3 variantes emails + tokens + planning saisonnier + KPIs cibles",
                    "criteres": {
                        "qualite_segmentation": "20%",
                        "qualite_variantes_emails": "25%",
                        "adaptation_culturelle_mena": "20%",
                        "integration_tokens_hubspot": "15%",
                        "pertinence_planning": "10%",
                        "kpis_cibles": "10%"
                    },
                    "score_minimum": 70,
                    "duree_estimee": "90-120 minutes"
                },
            ]
        },
        practical_exercise_en={
            "module": "Practice",
            "exercises": [
                {
                    "unite": 1, "lecon": 3,
                    "title": "My first automated campaign (Graded project)",
                    "instructions": (
                        "1. Define the target: precise segment (3-line ICP)\n"
                        "2. Identify 10 prospects in HubSpot matching your ICP\n"
                        "3. Write the sequence with ChatGPT\n"
                        "4. Configure the sequence in HubSpot\n"
                        "5. Configure the behavioural workflow (min 2 triggers)\n"
                        "6. Enrol the 10 prospects\n"
                        "7. Submit: dashboard + screenshots"
                    ),
                    "minimum_score": 70,
                    "estimated_duration": "60-90 minutes"
                },
            ]
        },
        comparison_tables_fr={
            "sequence_vs_workflow": {
                "titre": "Séquence vs Workflow HubSpot",
                "colonnes": ["Critère", "Séquence", "Workflow"],
                "lignes": [
                    ["Déclencheur", "Temps (J+3, J+7...)", "Comportement (a ouvert, a cliqué, a visité...)"],
                    ["Flexibilité", "Linéaire — même chemin pour tous", "Conditionnel — chemin selon les actions"],
                    ["Utilisation principale", "Prospection froide initiale", "Relances comportementales, nurturing avancé"],
                    ["Complexité", "Simple à configurer", "Plus avancé — logique si/alors"],
                    ["Dans HubSpot", "Onglet 'Séquences'", "Onglet 'Workflows'"],
                ]
            },
            "hubspot_vs_zoho": {
                "titre": "HubSpot AI vs Zoho CRM AI — Comparaison MENA",
                "colonnes": ["Critère", "HubSpot AI", "Zoho CRM AI", "Recommandation"],
                "lignes": [
                    ["Prix de départ", "Gratuit / 90$/mois Pro", "14$/mois/utilisateur", "Zoho pour budgets serrés"],
                    ["Interface arabe", "Non (français/anglais)", "Oui — interface complète", "Zoho pour clients arabophones"],
                    ["Qualité de l'AI", "Très avancée — ChatSpot, Content Assistant", "Bonne — Zia solide", "HubSpot pour AI avancée"],
                    ["Facilité de prise en main", "Très intuitive", "Courbe d'apprentissage plus longue", "HubSpot pour débutants"],
                    ["Support MENA", "Français, pas en arabe", "Arabe disponible", "Zoho pour support local"],
                ]
            },
            "niveaux_personnalisation": {
                "titre": "4 niveaux de personnalisation",
                "colonnes": ["Niveau", "Ce qu'on personnalise", "Pour qui ?", "Effort AI"],
                "lignes": [
                    ["Niveau 1 — Basique", "Prénom et nom de l'entreprise", "Campagnes 200+ prospects", "Minimal — tokens simples"],
                    ["Niveau 2 — Contextuel", "Secteur, ville, taille de l'entreprise", "Campagnes 20-200 prospects", "Faible — segmentation par groupe"],
                    ["Niveau 3 — Comportemental", "Actions récentes du prospect", "Leads chauds score > 70", "Moyen — données CRM temps réel"],
                    ["Niveau 4 — Hyper-personnalisation", "Contexte individuel unique", "5-10 grands comptes", "Élevé — recherche individuelle"],
                ]
            }
        },
        comparison_tables_en={
            "sequence_vs_workflow": {
                "title": "HubSpot Sequence vs Workflow",
                "columns": ["Criterion", "Sequence", "Workflow"],
                "rows": [
                    ["Trigger", "Time (D+3, D+7...)", "Behaviour (opened, clicked, visited...)"],
                    ["Use", "Initial cold prospection", "Behavioural follow-ups"],
                ]
            }
        },
        role_based_example_fr=(
            "Cas TechServ Tunisie — Analyse prédictive (Unité 2) :\n"
            "TechServ Tunisie (services IT, 18 employés) utilise HubSpot AI depuis 4 mois. "
            "Le tableau de bord révèle : taux de conversion leads→opportunités à 8% (sous la cible de 10%), "
            "2 clients à risque de churn élevé dont Plastique Moderne (28 000 TND/an), "
            "et Groupe Bâtisseurs Nasr avec un score de 89 (intention d'achat imminente).\n\n"
            "Actions prioritaires : appel DG Plastique Moderne dans les 24h, "
            "contact Groupe Bâtisseurs aujourd'hui + proposition demain.\n\n"
            "Cas Amine — Prédiction churn :\n"
            "Amine, DC startup SaaS Tunis, a reçu 8 alertes churn en janvier. "
            "En appelant proactivement dans les 48h : 6 clients retenus sur 8. "
            "CA préservé estimé : 45 000 TND."
        ),
        role_based_example_en=(
            "TechServ Tunisia Case — Predictive Analysis:\n"
            "TechServ Tunisia (IT services, 18 employees) has been using HubSpot AI for 4 months. "
            "The dashboard reveals: lead→opportunity conversion rate at 8% (below 10% target), "
            "2 high churn risk clients including Plastique Moderne (28,000 TND/year), "
            "and Groupe Bâtisseurs Nasr with a score of 89 (imminent purchase intent).\n\n"
            "Priority actions: call Plastique Moderne CEO within 24h, "
            "contact Groupe Bâtisseurs today + proposal tomorrow."
        ),
        action_point_fr=(
            "1. Configurer une séquence de 5 emails dans HubSpot pour votre segment principal\n"
            "2. Créer un workflow comportemental avec 2 déclencheurs (ouverture sans réponse + clic)\n"
            "3. Lancer votre première campagne personnalisée pour 20 prospects MENA\n"
            "4. Créer le Zap Zapier : Score > 70 → email ChatGPT → note HubSpot\n"
            "5. Vérifier la conformité de vos listes (consentement + désinscriptions synchronisées)"
        ),
        action_point_en=(
            "1. Configure a 5-email sequence in HubSpot for your main segment\n"
            "2. Create a behavioural workflow with 2 triggers\n"
            "3. Launch your first personalised campaign for 20 MENA prospects\n"
            "4. Create the Zapier Zap: Score > 70 → ChatGPT email → HubSpot note\n"
            "5. Check your list compliance (consent + synchronised unsubscribes)"
        ),
        section_content_fr={
            "unite1": {
                "title": "Unité 1 — Automatiser sa prospection",
                "duration": "~34 minutes + projet noté",
                "lessons": [
                    {"id": "1.1", "title": "Les séquences d'emails automatiques", "format": "Vidéo 12 min + Démo HubSpot"},
                    {"id": "1.2", "title": "Automatiser les relances", "format": "Vidéo 10 min + Exercice"},
                    {"id": "1.3", "title": "Ma première campagne automatisée", "format": "Projet noté (70/100 minimum)"},
                ]
            },
            "unite2": {
                "title": "Unité 2 — Analyser les données clients",
                "duration": "~32 minutes + cas pratique",
                "lessons": [
                    {"id": "2.1", "title": "Lire les insights AI", "format": "Vidéo 10 min + Quiz", "framework": "DIAL (Détecter, Interpréter, Agir, Logger)"},
                    {"id": "2.2", "title": "Prédire les comportements d'achat", "format": "Vidéo 10 min + Exercice"},
                    {"id": "2.3", "title": "Décisions data-driven — Cas TechServ Tunisie", "format": "Cas pratique PME tunisienne"},
                ]
            },
            "unite3": {
                "title": "Unité 3 — Personnaliser à grande échelle",
                "duration": "~34 minutes + projet noté",
                "lessons": [
                    {"id": "3.1", "title": "La personnalisation de masse", "format": "Vidéo 12 min + Démo"},
                    {"id": "3.2", "title": "Adapter au contexte MENA", "format": "Vidéo 10 min + Exercice"},
                    {"id": "3.3", "title": "Ma campagne personnalisée MENA", "format": "Projet noté"},
                ]
            },
            "unite4": {
                "title": "Unité 4 — Outils AI avancés",
                "duration": "~36 minutes + exercices",
                "lessons": [
                    {"id": "4.1", "title": "HubSpot AI en profondeur", "format": "Tutoriel avancé + Exercice", "outils": ["ChatSpot", "Content Assistant", "Deal Intelligence", "Predictive Lead Scoring"]},
                    {"id": "4.2", "title": "Zoho AI pour le marché MENA", "format": "Tutoriel + Exercice comparatif", "outils": ["Zia AI", "Interface arabe", "Serveurs MENA"]},
                    {"id": "4.3", "title": "Intégrer ChatGPT dans son CRM", "format": "Tutoriel Zapier + Exercice", "niveaux": ["Niveau 1 manuel", "Niveau 2 Zapier", "Niveau 3 API"]},
                ]
            },
            "unite5": {
                "title": "Unité 5 — Éthique AI intermédiaire",
                "duration": "~24 minutes + cas pratiques",
                "lessons": [
                    {"id": "5.1", "title": "Gérer les données responsablement", "format": "Vidéo 12 min + Quiz", "lois": ["Loi tunisienne 2004-63", "RGPD (si clients européens)", "PDPL EAU 2022"]},
                    {"id": "5.2", "title": "Éviter la manipulation avec l'AI", "format": "Cas pratiques interactifs", "cas": ["Personnalisation trop précise", "Séquence sans fin", "Scoring discriminatoire", "Automatisation qui dépasse la vitesse humaine", "Données client détournées"]},
                ]
            },
            "test_final": {
                "title": "Test Final — Pratique",
                "format": "10 questions QCM + 1 Projet",
                "duration": "30 min (test) + 48h (projet)",
                "score_minimum": "8/10 + Projet 70/100",
                "acces_suivant": "Module 3 — Expert"
            }
        },
        section_content_en={
            "unite1": {
                "title": "Unit 1 — Automate Your Prospection",
                "lessons": [
                    {"id": "1.1", "title": "Automatic email sequences", "format": "12 min video + HubSpot demo"},
                    {"id": "1.2", "title": "Automate follow-ups", "format": "10 min video + Exercise"},
                    {"id": "1.3", "title": "My first automated campaign", "format": "Graded project"},
                ]
            },
            "unite2": {
                "title": "Unit 2 — Analyse Client Data",
                "lessons": [
                    {"id": "2.1", "title": "Reading AI insights", "format": "10 min video + Quiz"},
                    {"id": "2.2", "title": "Predict buying behaviours", "format": "10 min video + Exercise"},
                    {"id": "2.3", "title": "Data-driven decisions — TechServ case", "format": "Tunisian SME case study"},
                ]
            },
            "unite3": {
                "title": "Unit 3 — Personalise at Scale",
                "lessons": [
                    {"id": "3.1", "title": "Mass personalisation", "format": "12 min video + Demo"},
                    {"id": "3.2", "title": "Adapt to MENA context", "format": "10 min video + Exercise"},
                    {"id": "3.3", "title": "My personalised MENA campaign", "format": "Graded project"},
                ]
            },
            "unite4": {
                "title": "Unit 4 — Advanced AI Tools",
                "lessons": [
                    {"id": "4.1", "title": "HubSpot AI in depth", "format": "Advanced tutorial + Exercise"},
                    {"id": "4.2", "title": "Zoho AI for MENA market", "format": "Tutorial + Comparison exercise"},
                    {"id": "4.3", "title": "Integrate ChatGPT into your CRM", "format": "Zapier tutorial + Exercise"},
                ]
            },
            "unite5": {
                "title": "Unit 5 — Intermediate AI Ethics",
                "lessons": [
                    {"id": "5.1", "title": "Responsible data management", "format": "12 min video + Quiz"},
                    {"id": "5.2", "title": "Avoid manipulation with AI", "format": "Interactive case studies"},
                ]
            },
            "final_test": {
                "title": "Final Test — Practice",
                "format": "10 MCQ + 1 Project",
                "minimum_score": "8/10 + Project 70/100",
                "next_access": "Module 3 — Expert"
            }
        },
        takeaway_fr="Un AI Sales Specialist intermédiaire automatise sa prospection et prend des décisions basées sur les données.",
        takeaway_en="An intermediate AI Sales Specialist automates prospection and makes data-driven decisions.",
        recommended_when_fr="Recommandé quand votre score est 1/2 sur un ou plusieurs skills (niveau Intermédiaire).",
        recommended_when_en="Recommended when your score is 1/2 on one or more skills (Intermediate level).",
        why_this_module_fr="Ce module vous permet de passer de l'utilisation basique à une utilisation systématique et automatisée de l'AI dans la vente.",
        why_this_module_en="This module allows you to move from basic to systematic and automated AI use in sales.",
        next_recommended_module_fr="AI Sales Specialist — Expert",
        next_recommended_module_en="AI Sales Specialist — Expert",
        is_active=True,
    )
    db.add(module_pratique)
    db.flush()

    # =============================
    # MODULE 3 — Expert (Avancé)
    # =============================
    module_expert = Module(
        title_en="AI Sales Specialist — Expert",
        title_fr="AI Sales Specialist — Expert",
        description_en=(
            "Build and lead a complete AI Sales strategy. "
            "Train and manage an AI Sales team, measure ROI, "
            "handle complex B2B MENA cases, and create an AI governance policy. "
            "Leads to official Euklydia certification."
        ),
        description_fr=(
            "Construisez et pilotez une stratégie AI Sales complète. "
            "Formez et managez une équipe AI Sales, mesurez le ROI, "
            "gérez des cas complexes B2B MENA et créez une politique de gouvernance AI. "
            "Mène à la certification officielle Euklydia."
        ),
        learning_objective_en=(
            "Build and lead a complete AI Sales strategy, train and manage an AI Sales team, "
            "measure and present AI ROI, handle complex B2B MENA cases, "
            "create an AI governance policy."
        ),
        learning_objective_fr=(
            "Construire et piloter une stratégie AI Sales complète, former et manager une équipe AI Sales, "
            "mesurer et présenter le ROI de l'AI, gérer des cas complexes B2B MENA, "
            "créer une politique de gouvernance AI."
        ),
        level="Advanced",
        estimated_duration_min=300,
        format="video + strategic exercises + mentor feedback + certification",
        role="AI Sales Specialist",
        journey_stage="expert",
        display_order=3,
        expected_outcome_fr=(
            "À la fin de ce module, l'apprenant a une stratégie AI Sales documentée sur 12 mois, "
            "sait former et piloter une équipe commerciale AI, peut calculer et présenter le ROI "
            "de l'AI Sales, gère des cas B2B complexes en Tunisie et en Afrique du Nord, "
            "et détient la certification officielle Euklydia AI Sales Specialist."
        ),
        expected_outcome_en=(
            "By the end of this module, the learner has a documented 12-month AI Sales strategy, "
            "can train and lead an AI sales team, can calculate and present AI Sales ROI, "
            "handles complex B2B cases in Tunisia and North Africa, "
            "and holds the official Euklydia AI Sales Specialist certification."
        ),
        key_concepts_en=[
            "Building a complete AI Sales strategy (4-phase roadmap)",
            "Training and managing an AI Sales team (cascade model)",
            "Measuring and presenting AI ROI (formula + dashboard)",
            "Complex B2B cases in Tunisia and MENA",
            "B2B strategies for Maghreb and Gulf",
            "AI governance policy and advanced ethics",
        ],
        key_concepts_fr=[
            "Construire une stratégie AI Sales complète (feuille de route 4 phases)",
            "Former et manager une équipe AI Sales (modèle cascade)",
            "Mesurer et présenter le ROI de l'AI (formule + dashboard)",
            "Cas complexes B2B tunisiens et MENA",
            "Stratégies B2B Maghreb et Golfe",
            "Politique de gouvernance AI et éthique avancée",
        ],
        quiz_questions_fr=[
            {
                "unite": 1, "lecon": 1,
                "question": "Une organisation avec CRM AI actif et séquences déployées mais sans ROI mesuré ni gouvernance est à quel niveau de maturité ?",
                "options": [
                    "A) Niveau 1 — Initiation",
                    "B) Niveau 2 — Adoption",
                    "C) Niveau 3 — Optimisation",
                    "D) Niveau 4 — Transformation"
                ],
                "correct": "B",
                "explanation": "Niveau 2 = CRM AI actif, séquences déployées, mais ROI non mesuré et gouvernance absente."
            },
            {
                "unite": 2, "lecon": 1,
                "question": "Pourquoi le modèle de formation en cascade avec champions AI est-il efficace en MENA ?",
                "options": [
                    "A) Parce qu'il coûte moins cher",
                    "B) Parce que l'apprentissage par les pairs est culturellement plus efficace en MENA",
                    "C) Parce que les champions AI ont toujours raison",
                    "D) Parce que le management n'a pas à s'impliquer"
                ],
                "correct": "B",
                "explanation": "En MENA, un collègue qui montre ses résultats AI est 5x plus convaincant qu'une présentation PowerPoint du management."
            },
            {
                "unite": 3, "lecon": 1,
                "question": "Une PME investit 6 000 TND dans l'AI Sales et génère 72 000 TND de bénéfices. Quel est le ROI ?",
                "options": ["A) 72%", "B) 720%", "C) 1100%", "D) 600%"],
                "correct": "C",
                "explanation": "ROI = (72 000 - 6 000) / 6 000 × 100 = 66 000 / 6 000 × 100 = 1100%."
            },
            {
                "unite": 3, "lecon": 2,
                "question": "Quelle section du dashboard AI Sales est lue quotidiennement par les commerciaux ?",
                "options": [
                    "A) Section 4 — ROI et impact business",
                    "B) Section 1 — Performance pipeline",
                    "C) Section 3 — Productivité équipe",
                    "D) Section 2 — Efficacité campagnes"
                ],
                "correct": "B",
                "explanation": "La Section 1 (performance pipeline) est la vue quotidienne des commerciaux — deals actifs, probabilités, alertes."
            },
            {
                "unite": 4, "lecon": 1,
                "question": "Dans le cas Mzoughi (groupe familial 3 générations), quel est le principe le plus important ?",
                "options": [
                    "A) Contacter uniquement le DAF car il contrôle le budget",
                    "B) Respecter la hiérarchie familiale — le DG fondateur a le dernier mot, toujours",
                    "C) Éviter les rencontres physiques et tout gérer par email AI",
                    "D) Proposer une réduction de 30% pour accélérer la décision"
                ],
                "correct": "B",
                "explanation": "Dans un groupe familial tunisien, la hiérarchie familiale prime sur la hiérarchie fonctionnelle."
            },
            {
                "unite": 5, "lecon": 1,
                "question": "Pourquoi la politique AI Sales doit-elle être co-construite avec l'équipe ?",
                "options": [
                    "A) Parce que la direction n'a pas les compétences pour la rédiger",
                    "B) Parce qu'en MENA, une politique acceptée par l'équipe sera appliquée — une politique imposée sera contournée",
                    "C) Parce que la co-construction est obligatoire légalement",
                    "D) Parce que cela réduit les coûts"
                ],
                "correct": "B",
                "explanation": "En MENA, le changement accepté est 10x plus durable que le changement imposé. La co-construction garantit l'adoption."
            },
        ],
        quiz_questions_en=[
            {
                "unite": 1, "lecon": 1,
                "question": "What maturity level is an organisation with active CRM AI and sequences but no measured ROI or governance?",
                "options": [
                    "A) Level 1 — Initiation",
                    "B) Level 2 — Adoption",
                    "C) Level 3 — Optimisation",
                    "D) Level 4 — Transformation"
                ],
                "correct": "B",
                "explanation": "Level 2 = active AI CRM, deployed sequences, but no measured ROI and no governance in place."
            },
        ],
        prompt_examples_fr=[
            {
                "unite": 1,
                "lecon": 1,
                "titre": "Prompt OKRs AI Sales — PME tunisienne",
                "prompt": (
                    "Tu es un expert en stratégie AI Sales pour les PME tunisiennes. "
                    "Génère 3 OKRs (Objectives and Key Results) pour une PME de [SECTEUR] "
                    "à [VILLE] avec [N] commerciaux qui veut déployer l'AI Sales sur 12 mois. "
                    "Chaque OKR doit avoir : 1 objectif qualitatif ambitieux + 3 Key Results "
                    "mesurables et chiffrés. Contexte : actuellement niveau [NIVEAU] de maturité AI "
                    "(1=initiation, 2=adoption, 3=optimisation, 4=transformation)."
                ),
                "usage": "Définir des objectifs mesurables pour la stratégie AI Sales"
            },
            {
                "unite": 1,
                "lecon": 3,
                "titre": "Prompt présentation ROI direction — Structure SCORE",
                "prompt": (
                    "Tu es un directeur commercial expérimenté. Aide-moi à structurer une présentation "
                    "de 15-20 minutes pour convaincre mon DG d'investir dans l'AI Sales. "
                    "Utilise la structure SCORE :\n"
                    "S — Situation actuelle de notre processus commercial\n"
                    "C — Complication : pourquoi ne pas changer coûte plus cher\n"
                    "O — Opportunité : ce que l'AI Sales peut apporter concrètement\n"
                    "R — Recommandation : la stratégie proposée avec budget\n"
                    "E — Engagement : ce qu'on demande et ce que ça rapporte\n\n"
                    "Contexte : PME [SECTEUR], [N] commerciaux, CA [MONTANT] TND, "
                    "marché principal [MARCHÉ]. Inclure un calcul ROI conservateur."
                ),
                "usage": "Préparer la présentation stratégique à la direction"
            },
            {
                "unite": 4,
                "lecon": 1,
                "titre": "Prompt adaptation culturelle Maroc B2B",
                "prompt": (
                    "Adapte cet email commercial pour le marché marocain des PME. "
                    "Le prospect est [POSTE] dans une entreprise [SECTEUR] à Casablanca. "
                    "Assure-toi que :\n"
                    "- Le ton est professionnel et respectueux, typique des relations B2B marocaines\n"
                    "- L'accroche fait référence à un défi spécifique aux PME marocaines\n"
                    "- L'exemple de résultat cite un secteur marocain reconnaissable\n"
                    "- Le CTA propose un appel ou une rencontre physique\n\n"
                    "Voici l'email à adapter : [EMAIL]"
                ),
                "usage": "Adapter un email tunisien pour le marché marocain"
            },
            {
                "unite": 4,
                "lecon": 2,
                "titre": "Prompt prospection Golfe (EAU) — en anglais",
                "prompt": (
                    "You are a B2B sales expert for the UAE market (Dubai). "
                    "Write a cold outreach email in English for a CFO of a mid-size technology company in Dubai. "
                    "My product is [PRODUCT]. The email must:\n"
                    "- Open with a specific insight about the UAE tech market\n"
                    "- Present a clear ROI figure\n"
                    "- Reference a MENA region success story\n"
                    "- Propose a 20-minute virtual demo\n"
                    "- Formal but dynamic tone — no small talk\n"
                    "- 130 words maximum\n"
                    "Tokens: {{ contact.firstname }}, {{ contact.company }}"
                ),
                "usage": "Prospection B2B vers le marché EAU (Dubai/Abu Dhabi)"
            },
        ],
        prompt_examples_en=[
            {
                "unite": 1, "lecon": 3,
                "title": "ROI presentation prompt — SCORE structure",
                "prompt": (
                    "You are an experienced commercial director. Help me structure a 15-20 minute presentation "
                    "to convince my CEO to invest in AI Sales. Use the SCORE structure: "
                    "S=Situation, C=Complication, O=Opportunity, R=Recommendation, E=Engagement. "
                    "Context: [SECTOR] SME, [N] salespeople, [REVENUE] revenue, main market [MARKET]."
                ),
                "usage": "Prepare the strategic presentation to management"
            },
        ],
        practical_exercise_fr={
            "module": "Expert",
            "exercises": [
                {
                    "unite": 1,
                    "lecon": 1,
                    "titre": "Construire votre stratégie AI Sales 12 mois",
                    "consigne": (
                        "1. Évaluez le niveau de maturité AI actuel de votre organisation (1-4) avec justification\n"
                        "2. Définissez votre vision AI Sales en 3 phrases\n"
                        "3. Rédigez 2 OKRs complets (Objectif + 3 Key Results chacun)\n"
                        "4. Complétez la feuille de route en 4 phases adaptée à votre contexte\n"
                        "5. Identifiez 3 obstacles et proposez une solution pour chacun"
                    ),
                    "livrable": "Document stratégique de 3 à 5 pages",
                    "evaluation": "Feedback mentor Euklydia dans les 5 jours ouvrés",
                    "duree_estimee": "2-3 heures"
                },
                {
                    "unite": 3,
                    "lecon": 3,
                    "titre": "Présenter vos résultats AI Sales (Exercice filmé)",
                    "consigne": (
                        "1. Préparez une présentation de 20 minutes suivant les 5 actes\n"
                        "2. Intégrez minimum 3 visuels (before/after + ROI + un visuel de votre choix)\n"
                        "3. Basez-vous sur des données réelles ou sur les données TechServ Tunisie\n"
                        "4. Anticipez 3 questions difficiles et préparez vos réponses\n"
                        "5. Filmez votre présentation et soumettez sur la plateforme"
                    ),
                    "criteres": {
                        "structure_narrative_5_actes": "20%",
                        "qualite_visuels": "20%",
                        "rigueur_calcul_roi": "25%",
                        "pertinence_recommandations": "20%",
                        "conviction_presentation": "15%"
                    },
                    "score_minimum": 70,
                    "feedback": "Mentor Euklydia dans les 5 jours ouvrés"
                },
            ]
        },
        practical_exercise_en={
            "module": "Expert",
            "exercises": [
                {
                    "unite": 3, "lecon": 3,
                    "title": "Present your AI Sales results (Filmed exercise)",
                    "instructions": (
                        "1. Prepare a 20-minute presentation following the 5 acts\n"
                        "2. Include minimum 3 visuals\n"
                        "3. Based on real data or TechServ Tunisia case\n"
                        "4. Anticipate 3 difficult questions\n"
                        "5. Film your presentation and submit"
                    ),
                    "minimum_score": 70,
                    "feedback": "Euklydia mentor within 5 business days"
                }
            ]
        },
        comparison_tables_fr={
            "niveaux_maturite_ai": {
                "titre": "Modèle de maturité AI Sales — 4 niveaux",
                "colonnes": ["Niveau", "Nom", "Description", "Indicateurs clés"],
                "lignes": [
                    ["Niveau 1", "Initiation", "Quelques commerciaux utilisent ChatGPT ponctuellement, pas de CRM AI", "< 20% équipe utilise AI, pas de métriques"],
                    ["Niveau 2", "Adoption", "CRM AI configuré, séquences actives, métriques suivies", "CRM actif, séquences > 50% prospects"],
                    ["Niveau 3", "Optimisation", "Stack AI complet, scoring prédictif, campagnes multi-marchés MENA", "ROI AI mesuré, conversion > 25%"],
                    ["Niveau 4", "Transformation", "AI au cœur de toute la stratégie, équipe certifiée, gouvernance AI", "CA AI-driven > 60%, politique AI documentée"],
                ]
            },
            "profils_apprenants": {
                "titre": "4 profils d'apprenants — Équipe commerciale",
                "colonnes": ["Profil", "Comportement typique", "Approche de formation", "Levier de motivation"],
                "lignes": [
                    ["L'Enthousiaste", "Adopte immédiatement, expérimente, peut faire des erreurs", "Formation rapide + autonomie + défis avancés", "Reconnaissance comme 'champion AI'"],
                    ["Le Pragmatique", "Attend de voir les résultats avant d'adopter", "Démonstration de résultats concrets en premier", "Chiffres et gains de temps mesurables"],
                    ["Le Sceptique", "Doute de la valeur, perçoit une menace à son expertise", "Rassurer sur le rôle humain, amplifier l'expertise", "Valorisation expertise + preuve que l'AI ne remplace pas"],
                    ["Le Réfractaire", "Refuse activement ou passivement", "Accompagnement individuel + petites victoires", "Inclusion dans les décisions + reconnaissance progrès"],
                ]
            },
            "strategies_marches_mena": {
                "titre": "Stratégies B2B par marché MENA",
                "colonnes": ["Marché", "Langue principale", "Ton recommandé", "Facteur clé de succès"],
                "lignes": [
                    ["Tunisie", "Français (B2B)", "Direct, chaleureux, pragmatique", "Confiance personnelle, réseau, PME familiales"],
                    ["Maroc", "Français (B2B)", "Formel mais accessible", "Marché dynamique, forte francophonie"],
                    ["Algérie", "Français ou arabe", "Formel, institutionnel", "Secteur public dominant, cycles longs"],
                    ["EAU / Qatar", "Anglais ou arabe MSA", "Très formel, orienté ROI chiffré", "ROI immédiat, tech-friendly, délais courts"],
                    ["Arabie Saoudite", "Arabe MSA ou anglais", "Formel, respectueux des hiérarchies", "Wasta (réseau), Vision 2030, patience"],
                ]
            },
            "roi_categories_benefices": {
                "titre": "5 catégories de bénéfices ROI AI Sales",
                "colonnes": ["Catégorie", "Bénéfice", "Valeur type PME MENA (annuel)"],
                "lignes": [
                    ["CA additionnel", "+20 à +40% de CA sur la période AI", "20 000 - 50 000 TND"],
                    ["Rétention clients", "CA préservé via prédiction du churn", "5 000 - 15 000 TND"],
                    ["Productivité", "2-4h/semaine/commercial libérées", "3 000 - 6 000 TND"],
                    ["Cycle de vente réduit", "+2 à +4 deals/trimestre", "16 000 - 32 000 TND"],
                    ["Cross-sell / Up-sell", "Opportunités détectées par AI", "3 000 - 10 000 TND"],
                ]
            }
        },
        comparison_tables_en={
            "ai_maturity_levels": {
                "title": "AI Sales Maturity Model — 4 levels",
                "columns": ["Level", "Name", "Description", "Key indicators"],
                "rows": [
                    ["Level 1", "Initiation", "A few salespeople use ChatGPT occasionally, no AI CRM", "< 20% team uses AI"],
                    ["Level 2", "Adoption", "AI CRM configured, sequences active, metrics tracked", "Active CRM, sequences > 50%"],
                    ["Level 3", "Optimisation", "Complete AI stack, predictive scoring, multi-MENA campaigns", "Measured ROI, conversion > 25%"],
                    ["Level 4", "Transformation", "AI at core of strategy, certified team, governance in place", "AI-driven revenue > 60%"],
                ]
            }
        },
        role_based_example_fr=(
            "Cas Distribio Tunisie — Gestion de la résistance au changement :\n"
            "Distribution de matériel de bureau, 35 employés, 8 commerciaux, CA 2,4M TND. "
            "Déploiement HubSpot AI + ChatGPT annoncé. 4 profils de résistance identifiés :\n\n"
            "Amine (45 ans, 15 ans ancienneté) — Réfractaire : 'J'ai mes preuves sans AI'. "
            "Solution : reconnaître publiquement son expertise, reformuler l'outil comme amplificateur, "
            "accompagnement individuel sans témoin.\n\n"
            "Karim (28 ans) — Enthousiaste désorganisé : envoie des emails AI sans relecture. "
            "Solution : nommer 'champion qualité AI', lui donner une responsabilité.\n\n"
            "Leila (39 ans) — Sceptique constructive : 'Comment on s'assure que les clients savent ?' "
            "Solution : la nommer responsable de la politique éthique AI.\n\n"
            "Sonia (32 ans) — Abandon silencieux. "
            "Solution : entretien privé bienveillant + progression par petites victoires + suivi 48h.\n\n"
            "Cas TechServ ROI :\n"
            "Investissement 4 900 TND → Bénéfices 146 979 TND → ROI 2898% — Payback 1,2 mois."
        ),
        role_based_example_en=(
            "Distribio Tunisia Case — Managing resistance to change:\n"
            "Office supplies distribution, 35 employees, 8 salespeople. "
            "HubSpot AI + ChatGPT deployment announced. 4 resistance profiles identified: "
            "Amine (senior, refuser), Karim (enthusiastic but disorganised), "
            "Leila (constructive sceptic), Sonia (silent dropout).\n\n"
            "TechServ ROI Case: Investment 4,900 TND → Benefits 146,979 TND → ROI 2898%"
        ),
        action_point_fr=(
            "1. Évaluer honnêtement votre niveau de maturité AI (1-4) et documenter\n"
            "2. Rédiger votre stratégie AI Sales 12 mois avec OKRs mesurables\n"
            "3. Identifier vos 2 champions AI et lancer la formation en cascade\n"
            "4. Créer votre dashboard AI Sales avec les 4 sections dans HubSpot\n"
            "5. Rédiger et déployer votre politique AI Sales en co-construction avec l'équipe\n"
            "6. Préparer et soumettre votre projet de certification finale Euklydia"
        ),
        action_point_en=(
            "1. Honestly assess your AI maturity level (1-4) and document it\n"
            "2. Write your 12-month AI Sales strategy with measurable OKRs\n"
            "3. Identify your 2 AI champions and launch cascade training\n"
            "4. Create your AI Sales dashboard with 4 sections in HubSpot\n"
            "5. Write and deploy your AI Sales policy with team co-construction\n"
            "6. Prepare and submit your Euklydia final certification project"
        ),
        section_content_fr={
            "unite1": {
                "title": "Unité 1 — Stratégie AI Sales globale",
                "duration": "~39 minutes + exercice stratégique",
                "lessons": [
                    {"id": "1.1", "title": "Construire sa stratégie AI Sales", "format": "Vidéo 15 min + Exercice stratégique", "outils": ["Modèle maturité 4 niveaux", "5 piliers stratégie", "Feuille de route 4 phases", "OKRs AI Sales"]},
                    {"id": "1.2", "title": "Adapter au contexte MENA", "format": "Vidéo 12 min + Cas pratique", "focus": "Adaptation des 5 piliers, 3 profils PME MENA, 5 facteurs critiques succès"},
                    {"id": "1.3", "title": "Présenter sa stratégie à la direction", "format": "Exercice + Feedback mentor", "structure": "SCORE — calcul ROI exemple 1673% — 5 objections fréquentes"},
                ]
            },
            "unite2": {
                "title": "Unité 2 — Piloter une équipe AI Sales",
                "duration": "~34 minutes + simulation + cas Distribio",
                "lessons": [
                    {"id": "2.1", "title": "Former ses collègues à l'AI", "format": "Vidéo 12 min + Exercice", "modele": "Cascade avec champions AI — 4 profils d'apprenants"},
                    {"id": "2.2", "title": "Orchestrer humains et AI", "format": "Vidéo 10 min + Simulation", "outils": ["Matrice orchestration", "3 modes (automatisé/assisté/humain-led)", "AI Sales Review 45 min"]},
                    {"id": "2.3", "title": "Gérer la résistance au changement", "format": "Cas réel équipe tunisienne (Distribio)", "cas": ["Amine réfractaire", "Karim enthousiaste", "Leila sceptique", "Sonia abandon silencieux"]},
                ]
            },
            "unite3": {
                "title": "Unité 3 — Mesurer le ROI de l'AI",
                "duration": "~34 minutes + tutoriel dashboard + exercice noté",
                "lessons": [
                    {"id": "3.1", "title": "C'est quoi le ROI ?", "format": "Vidéo 12 min + Quiz", "formule": "ROI = (Bénéfices - Coûts) / Coûts × 100", "exemple": "TechServ : ROI 2898%, payback 1,2 mois"},
                    {"id": "3.2", "title": "Créer son dashboard AI Sales", "format": "Tutoriel HubSpot + Exercice", "sections": ["Performance pipeline", "Efficacité campagnes", "Productivité équipe", "ROI et impact business"]},
                    {"id": "3.3", "title": "Présenter les résultats", "format": "Exercice noté + Feedback mentor", "structure": "5 actes narratifs + tableau before/after + 5 questions difficiles"},
                ]
            },
            "unite4": {
                "title": "Unité 4 — AI Sales avancé MENA",
                "duration": "~36 minutes + 3 cas B2B + forum",
                "lessons": [
                    {"id": "4.1", "title": "Cas complexes B2B tunisiens", "format": "3 cas réels d'entreprises", "cas": ["Groupe Mzoughi (groupe familial, cycle 14 mois)", "Mutuelle AMINA (para-public, pilote)", "ShopTunisie (startup chaos commercial)"]},
                    {"id": "4.2", "title": "Stratégies B2B Maghreb et Golfe", "format": "Vidéo 12 min + Exercice", "marches": ["Maroc (dynamique, français)", "Algérie (institutionnel)", "EAU (ROI, anglais)", "Qatar (vision)", "Saudi (wasta, arabe)"]},
                    {"id": "4.3", "title": "L'avenir de l'AI Sales en MENA", "format": "Vidéo 12 min + Forum", "tendances": ["AI agentique", "Voix AI multilingue", "WhatsApp AI", "Vision 2030", "Arabe de qualité"]},
                ]
            },
            "unite5": {
                "title": "Unité 5 — Gouvernance et Éthique AI avancée",
                "duration": "~24 minutes + simulation 5 crises",
                "lessons": [
                    {"id": "5.1", "title": "Créer sa politique AI Sales", "format": "Vidéo 12 min + Exercice", "sections_politique": ["Objet et périmètre", "Principes directeurs", "Usages autorisés", "Usages interdits", "Gestion données", "Responsabilités", "Procédures contrôle"]},
                    {"id": "5.2", "title": "Gérer les crises éthiques AI", "format": "Simulation interactive — 5 crises", "crises": ["Email au mauvais client", "Contenu offensant Ramadan", "Violation RGPD", "Accusation publique concurrent", "Biais algorithmique discriminatoire"]},
                ]
            },
            "certification_finale": {
                "title": "Certification Finale — AI Sales Specialist",
                "format": "Test 20 questions + Projet complet + Présentation jury Euklydia",
                "score_minimum": "80% test + 75/100 projet",
                "delivrables_projet": [
                    "Diagnostic de maturité AI",
                    "Stratégie AI Sales 12 mois",
                    "Plan de formation équipe",
                    "Politique AI Sales",
                    "Dashboard ROI",
                    "Présentation direction"
                ],
                "jury": "2 membres Euklydia — 20 min présentation + 10 min questions",
                "certification": "Badge LinkedIn officiel + Certificat PDF + Annuaire Euklydia MENA",
                "validite": "2 ans"
            }
        },
        section_content_en={
            "unite1": {
                "title": "Unit 1 — Global AI Sales Strategy",
                "lessons": [
                    {"id": "1.1", "title": "Build your AI Sales strategy", "format": "15 min video + Strategic exercise"},
                    {"id": "1.2", "title": "Adapt to MENA context", "format": "12 min video + Case study"},
                    {"id": "1.3", "title": "Present your strategy to leadership", "format": "Exercise + Mentor feedback"},
                ]
            },
            "unite2": {
                "title": "Unit 2 — Lead an AI Sales Team",
                "lessons": [
                    {"id": "2.1", "title": "Train colleagues in AI", "format": "12 min video + Exercise"},
                    {"id": "2.2", "title": "Orchestrate humans and AI", "format": "10 min video + Simulation"},
                    {"id": "2.3", "title": "Manage resistance to change", "format": "Tunisian team case (Distribio)"},
                ]
            },
            "unite3": {
                "title": "Unit 3 — Measure AI ROI",
                "lessons": [
                    {"id": "3.1", "title": "What is ROI?", "format": "12 min video + Quiz"},
                    {"id": "3.2", "title": "Build your AI Sales dashboard", "format": "HubSpot tutorial + Exercise"},
                    {"id": "3.3", "title": "Present results", "format": "Graded exercise + Mentor feedback"},
                ]
            },
            "unite4": {
                "title": "Unit 4 — Advanced AI Sales MENA",
                "lessons": [
                    {"id": "4.1", "title": "Complex B2B Tunisian cases", "format": "3 real company cases"},
                    {"id": "4.2", "title": "B2B strategies Maghreb and Gulf", "format": "12 min video + Exercise"},
                    {"id": "4.3", "title": "Future of AI Sales in MENA", "format": "Video + Forum"},
                ]
            },
            "unite5": {
                "title": "Unit 5 — AI Governance and Advanced Ethics",
                "lessons": [
                    {"id": "5.1", "title": "Create your AI Sales policy", "format": "12 min video + Exercise"},
                    {"id": "5.2", "title": "Manage AI ethics crises", "format": "Interactive simulation — 5 crises"},
                ]
            },
            "final_certification": {
                "title": "Final Certification — AI Sales Specialist",
                "format": "20Q test + Complete project + Euklydia jury presentation",
                "minimum_score": "80% test + 75/100 project",
                "certification": "Official LinkedIn badge + PDF certificate + Euklydia MENA directory",
                "validity": "2 years"
            }
        },
        takeaway_fr="Un AI Sales Specialist certifié Euklydia pilote une stratégie AI complète, forme son équipe et mesure son ROI.",
        takeaway_en="An Euklydia certified AI Sales Specialist leads a complete AI strategy, trains their team and measures ROI.",
        recommended_when_fr="Recommandé quand votre score est 2/2 sur un ou plusieurs skills (niveau Avancé).",
        recommended_when_en="Recommended when your score is 2/2 on one or more skills (Advanced level).",
        why_this_module_fr="Ce module vous prépare à la certification officielle Euklydia AI Sales Specialist et fait de vous un leader AI reconnu en Afrique du Nord.",
        why_this_module_en="This module prepares you for the official Euklydia AI Sales Specialist certification and makes you a recognised AI leader in North Africa.",
        next_recommended_module_fr=None,
        next_recommended_module_en=None,
        is_active=True,
    )
    db.add(module_expert)
    db.flush()

    # =============================
    # MODULE SKILLS MAPPING
    # Score 0   → Beginner     → Module Fondations
    # Score 50  → Intermediate → Module Pratique
    # Score 100 → Advanced     → Module Expert
    # =============================
    for skill_id in skill_ids:
        db.add(ModuleSkill(module_id=module_fondations.id, skill_id=skill_id))
        db.add(ModuleSkill(module_id=module_pratique.id, skill_id=skill_id))
        db.add(ModuleSkill(module_id=module_expert.id, skill_id=skill_id))

    db.commit()
    print(f"✅ AI Sales Specialist — 3 modules enrichis créés et liés aux {len(skill_ids)} skills")
    print(f"   Module Fondations ID: {module_fondations.id}")
    print(f"   Module Pratique ID:   {module_pratique.id}")
    print(f"   Module Expert ID:     {module_expert.id}")