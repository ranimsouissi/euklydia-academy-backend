from app.models.module import Module
from app.models.module_skill import ModuleSkill
from app.models.skill import Skill


def seed_ai_project_manager_modules(db):
    # =============================
    # Récupérer les skills AI Project Manager (career_path_id = 82)
    # =============================
    skills = db.query(Skill).filter(Skill.career_path_id == 82).order_by(Skill.id.desc()).limit(5).all()
    skills = list(reversed(skills))  # remettre dans l'ordre
    if not skills:
        print("❌ Aucun skill trouvé pour AI Project Manager (career_path_id=82)")
        return

    skill_ids = [s.id for s in skills]
    print(f"✅ Skills trouvés : {[s.name for s in skills]}")

    # =============================
    # Supprimer les anciens modules de ce rôle
    # =============================
    existing_modules = db.query(Module).filter(Module.role == "AI Project Manager").all()
    for m in existing_modules:
        db.query(ModuleSkill).filter(ModuleSkill.module_id == m.id).delete()
        db.delete(m)
    db.flush()

    # =============================
    # MODULE 1 — Fondations (Débutant)
    # =============================
    module_fondations = Module(
        title_en="AI Project Manager — Foundations",
        title_fr="AI Project Manager — Fondations",
        description_en=(
            "Your first steps with AI in project management. Learn to plan with AI, "
            "use ClickUp AI to manage your first dashboard, communicate with your team "
            "using ChatGPT in Arabic and French, and apply ethical principles "
            "in the North Africa project management context."
        ),
        description_fr=(
            "Vos premiers pas avec l'AI dans la gestion de projet. Apprenez à planifier avec l'AI, "
            "utiliser ClickUp AI pour gérer votre premier tableau de bord, communiquer avec votre équipe "
            "via ChatGPT en arabe et français, et appliquer les principes éthiques "
            "dans le contexte Afrique du Nord de la gestion de projet."
        ),
        learning_objective_en=(
            "Generate a first project plan with AI, create tasks and sub-tasks automatically, "
            "use ClickUp AI to manage a dashboard, generate reports and meeting minutes with ChatGPT, "
            "and respect basic AI ethics in project decisions."
        ),
        learning_objective_fr=(
            "Générer un premier planning de projet avec l'AI, créer des tâches et sous-tâches automatiquement, "
            "utiliser ClickUp AI pour gérer un tableau de bord, générer des rapports et comptes-rendus avec ChatGPT, "
            "et respecter les règles éthiques AI de base dans les décisions de projet."
        ),
        level="Beginner",
        estimated_duration_min=180,
        format="vidéo + quiz + exercices pratiques",
        role="AI Project Manager",
        journey_stage="foundation",
        display_order=1,
        key_concepts_en=[
            "AI in project management: what it changes today",
            "Essential PM AI tools (ClickUp AI, Monday AI, ChatGPT)",
            "AI PM in the MENA context",
            "Planning with AI: tasks and sub-tasks",
            "First AI project dashboard",
            "Team communication with AI in Arabic and French",
            "Basic AI ethics: decisions AI can and cannot make",
        ],
        key_concepts_fr=[
            "L'AI dans la gestion de projet : ce qu'elle change aujourd'hui",
            "Outils AI essentiels du PM (ClickUp AI, Monday AI, ChatGPT)",
            "L'AI PM dans le contexte MENA",
            "Planifier avec l'AI : tâches et sous-tâches",
            "Premier tableau de bord de projet AI",
            "Communiquer avec son équipe avec l'AI en arabe et français",
            "Éthique AI basique : décisions que l'AI peut et ne doit pas prendre",
        ],
        section_content_fr={
            "unite1": {
                "title": "Unité 1 — L'AI dans la gestion de projet",
                "lessons": [
                    "Leçon 1 — C'est quoi l'AI pour un PM ? | Vidéo 10 min + Quiz 5 questions",
                    "Leçon 2 — Les outils AI essentiels du PM | Vidéo 8 min + Tableau comparatif",
                    "Leçon 3 — L'AI PM dans le contexte Afrique du Nord | Vidéo 8 min + Forum de discussion",
                ]
            },
            "unite2": {
                "title": "Unité 2 — Planifier avec l'AI",
                "lessons": [
                    "Leçon 1 — Générer son premier planning avec l'AI | Tutoriel guidé + Exercice pratique",
                    "Leçon 2 — Créer des tâches et sous-tâches automatiquement | Vidéo 10 min + Exercice",
                    "Leçon 3 — Mon premier planning de projet Afrique du Nord | Projet pratique noté",
                ]
            },
            "unite3": {
                "title": "Unité 3 — Mon premier outil de gestion AI",
                "lessons": [
                    "Leçon 1 — Introduction à ClickUp AI | Tutoriel guidé pas à pas",
                    "Leçon 2 — Créer son premier tableau de bord AI | Tutoriel guidé + Exercice",
                    "Leçon 3 — Gérer son équipe avec l'AI | Vidéo 10 min + Exercice pratique",
                ]
            },
            "unite4": {
                "title": "Unité 4 — Communiquer avec son équipe avec l'AI",
                "lessons": [
                    "Leçon 1 — Générer des rapports automatiquement | Vidéo 10 min + Exercice",
                    "Leçon 2 — Rédiger des comptes-rendus avec ChatGPT en arabe et français | Tutoriel + Exercice",
                    "Leçon 3 — Communiquer avec les parties prenantes | Vidéo 8 min + Exercice pratique",
                ]
            },
            "unite5": {
                "title": "Unité 5 — Éthique AI basique en gestion de projet",
                "lessons": [
                    "Leçon 1 — Les décisions que l'AI peut et ne doit pas prendre | Vidéo 10 min + Quiz",
                    "Leçon 2 — Transparence avec son équipe sur l'usage de l'AI | Cas pratiques interactifs",
                ]
            },
        },
        section_content_en={
            "unite1": {
                "title": "Unit 1 — AI in Project Management",
                "lessons": [
                    "Lesson 1 — What is AI for a PM? | 10 min video + 5-question quiz",
                    "Lesson 2 — Essential PM AI tools | 8 min video + Comparison table",
                    "Lesson 3 — AI PM in the North Africa context | 8 min video + Discussion forum",
                ]
            },
            "unite2": {
                "title": "Unit 2 — Planning with AI",
                "lessons": [
                    "Lesson 1 — Generate your first project plan with AI | Guided tutorial + Practical exercise",
                    "Lesson 2 — Create tasks and sub-tasks automatically | 10 min video + Exercise",
                    "Lesson 3 — My first North Africa project plan | Graded practical project",
                ]
            },
            "unite3": {
                "title": "Unit 3 — My First AI Management Tool",
                "lessons": [
                    "Lesson 1 — Introduction to ClickUp AI | Step-by-step guided tutorial",
                    "Lesson 2 — Create your first AI dashboard | Guided tutorial + Exercise",
                    "Lesson 3 — Manage your team with AI | 10 min video + Practical exercise",
                ]
            },
            "unite4": {
                "title": "Unit 4 — Communicate with Your Team Using AI",
                "lessons": [
                    "Lesson 1 — Generate reports automatically | 10 min video + Exercise",
                    "Lesson 2 — Write meeting minutes with ChatGPT in Arabic and French | Tutorial + Exercise",
                    "Lesson 3 — Communicate with stakeholders | 8 min video + Practical exercise",
                ]
            },
            "unite5": {
                "title": "Unit 5 — Basic AI Ethics in Project Management",
                "lessons": [
                    "Lesson 1 — Decisions AI can and cannot make | 10 min video + Quiz",
                    "Lesson 2 — Transparency with your team on AI usage | Interactive case studies",
                ]
            },
        },
        takeaway_fr="L'AI ne remplace pas le chef de projet — elle lui permet de se concentrer sur les décisions stratégiques et humaines.",
        takeaway_en="AI does not replace the project manager — it allows them to focus on strategic and human decisions.",
        recommended_when_fr="Recommandé quand votre score est 0/2 sur un ou plusieurs skills (niveau Débutant).",
        recommended_when_en="Recommended when your score is 0/2 on one or more skills (Beginner level).",
        why_this_module_fr="Avant d'utiliser les outils AI PM, vous avez besoin de comprendre les fondamentaux et le contexte Afrique du Nord.",
        why_this_module_en="Before using AI PM tools, you need to understand the fundamentals and the North Africa context.",
        next_recommended_module_fr="AI Project Manager — Pratique",
        next_recommended_module_en="AI Project Manager — Practice",
        is_active=True,
    )
    db.add(module_fondations)
    db.flush()

    # =============================
    # MODULE 2 — Pratique (Intermédiaire)
    # =============================
    module_pratique = Module(
        title_en="AI Project Manager — Practice",
        title_fr="AI Project Manager — Pratique",
        description_en=(
            "Automate your project management and predict risks with AI. "
            "Create automatic workflows with ClickUp AI, analyse dashboards, "
            "predict delays and risks, manage workload across multiple simultaneous projects, "
            "and master advanced AI PM tools for the MENA market."
        ),
        description_fr=(
            "Automatisez votre gestion de projet et prédisez les risques avec l'AI. "
            "Créez des workflows automatiques avec ClickUp AI, analysez les tableaux de bord, "
            "prédisez les retards et risques, gérez la charge de travail sur plusieurs projets simultanés "
            "et maîtrisez les outils AI PM avancés pour le marché MENA."
        ),
        learning_objective_en=(
            "Create automatic project workflows with ClickUp AI, read and interpret AI dashboards, "
            "predict delays and risks with AI, detect workload overloads automatically, "
            "manage 3 projects simultaneously with AI, master Monday AI for MENA teams, "
            "and use team data responsibly."
        ),
        learning_objective_fr=(
            "Créer des workflows de projet automatiques avec ClickUp AI, lire et interpréter les tableaux de bord AI, "
            "prédire les retards et risques avec l'AI, détecter les surcharges de travail automatiquement, "
            "gérer 3 projets simultanément avec l'AI, maîtriser Monday AI pour les équipes MENA "
            "et utiliser les données de l'équipe de manière responsable."
        ),
        level="Intermediate",
        estimated_duration_min=240,
        format="vidéo + exercices pratiques + projet noté",
        role="AI Project Manager",
        journey_stage="practice",
        display_order=2,
        key_concepts_en=[
            "Automatic workflows with ClickUp AI",
            "Automated reminders and notifications",
            "Reading and interpreting AI dashboards",
            "Predicting delays and risks with AI",
            "Workload detection and redistribution with AI",
            "Managing 3 simultaneous projects with AI",
            "ClickUp AI in depth",
            "Monday AI for MENA teams",
            "Integrating ChatGPT into management tools",
            "Responsible use of team data",
        ],
        key_concepts_fr=[
            "Workflows automatiques avec ClickUp AI",
            "Rappels et notifications automatisés",
            "Lire et interpréter les tableaux de bord AI",
            "Prédire les retards et risques avec l'AI",
            "Détection et redistribution de la charge de travail avec l'AI",
            "Gérer 3 projets simultanément avec l'AI",
            "ClickUp AI en profondeur",
            "Monday AI pour les équipes MENA",
            "Intégrer ChatGPT dans ses outils de gestion",
            "Utilisation responsable des données de l'équipe",
        ],
        section_content_fr={
            "unite1": {
                "title": "Unité 1 — Automatiser la gestion de projet",
                "lessons": [
                    "Leçon 1 — Créer des workflows automatiques avec ClickUp AI | Vidéo 12 min + Exercice",
                    "Leçon 2 — Automatiser les rappels et notifications | Tutoriel guidé + Exercice pratique",
                    "Leçon 3 — Mon projet entièrement automatisé | Projet pratique noté",
                ]
            },
            "unite2": {
                "title": "Unité 2 — Analyser et prédire avec l'AI",
                "lessons": [
                    "Leçon 1 — Lire et interpréter les tableaux de bord AI | Vidéo 12 min + Exercice",
                    "Leçon 2 — Prédire les retards et risques avec l'AI | Vidéo 10 min + Exercice pratique",
                    "Leçon 3 — Agir avant que le problème survienne | Cas pratique noté",
                ]
            },
            "unite3": {
                "title": "Unité 3 — Gérer la charge de travail avec l'AI",
                "lessons": [
                    "Leçon 1 — Détecter les surcharges automatiquement | Vidéo 10 min + Exercice pratique",
                    "Leçon 2 — Redistribuer les tâches avec l'AI | Tutoriel guidé + Exercice pratique",
                    "Leçon 3 — Gérer 3 projets simultanément avec l'AI | Projet pratique noté",
                ]
            },
            "unite4": {
                "title": "Unité 4 — Outils AI avancés pour PM",
                "lessons": [
                    "Leçon 1 — ClickUp AI en profondeur | Tutoriel avancé + Exercice pratique",
                    "Leçon 2 — Monday AI pour les équipes Afrique du Nord | Tutoriel + Exercice comparatif",
                    "Leçon 3 — Intégrer ChatGPT dans ses outils de gestion | Tutoriel guidé + Exercice",
                ]
            },
            "unite5": {
                "title": "Unité 5 — Éthique AI intermédiaire",
                "lessons": [
                    "Leçon 1 — Utiliser les données de l'équipe responsablement | Vidéo 12 min + Quiz",
                    "Leçon 2 — Biais AI dans la gestion de projet | Cas pratiques interactifs",
                ]
            },
        },
        section_content_en={
            "unite1": {
                "title": "Unit 1 — Automate Project Management",
                "lessons": [
                    "Lesson 1 — Create automatic workflows with ClickUp AI | 12 min video + Exercise",
                    "Lesson 2 — Automate reminders and notifications | Guided tutorial + Practical exercise",
                    "Lesson 3 — My fully automated project | Graded practical project",
                ]
            },
            "unite2": {
                "title": "Unit 2 — Analyse and Predict with AI",
                "lessons": [
                    "Lesson 1 — Read and interpret AI dashboards | 12 min video + Exercise",
                    "Lesson 2 — Predict delays and risks with AI | 10 min video + Practical exercise",
                    "Lesson 3 — Act before the problem occurs | Graded case study",
                ]
            },
            "unite3": {
                "title": "Unit 3 — Manage Workload with AI",
                "lessons": [
                    "Lesson 1 — Detect overloads automatically | 10 min video + Practical exercise",
                    "Lesson 2 — Redistribute tasks with AI | Guided tutorial + Practical exercise",
                    "Lesson 3 — Manage 3 simultaneous projects with AI | Graded practical project",
                ]
            },
            "unite4": {
                "title": "Unit 4 — Advanced AI Tools for PM",
                "lessons": [
                    "Lesson 1 — ClickUp AI in depth | Advanced tutorial + Practical exercise",
                    "Lesson 2 — Monday AI for North Africa teams | Tutorial + Comparative exercise",
                    "Lesson 3 — Integrate ChatGPT into management tools | Guided tutorial + Exercise",
                ]
            },
            "unite5": {
                "title": "Unit 5 — Intermediate AI Ethics",
                "lessons": [
                    "Lesson 1 — Use team data responsibly | 12 min video + Quiz",
                    "Lesson 2 — AI bias in project management | Interactive case studies",
                ]
            },
        },
        takeaway_fr="Un AI Project Manager intermédiaire automatise sa gestion de projet et anticipe les risques avant qu'ils surviennent.",
        takeaway_en="An intermediate AI Project Manager automates their project management and anticipates risks before they occur.",
        recommended_when_fr="Recommandé quand votre score est 1/2 sur un ou plusieurs skills (niveau Intermédiaire).",
        recommended_when_en="Recommended when your score is 1/2 on one or more skills (Intermediate level).",
        why_this_module_fr="Ce module vous permet de passer d'une gestion de projet basique à une gestion automatisée et prédictive avec l'AI.",
        why_this_module_en="This module allows you to move from basic project management to automated and predictive AI-driven management.",
        next_recommended_module_fr="AI Project Manager — Expert",
        next_recommended_module_en="AI Project Manager — Expert",
        is_active=True,
    )
    db.add(module_pratique)
    db.flush()

    # =============================
    # MODULE 3 — Expert (Avancé)
    # =============================
    module_expert = Module(
        title_en="AI Project Manager — Expert",
        title_fr="AI Project Manager — Expert",
        description_en=(
            "Build and lead a complete AI PM strategy and transform your organisation. "
            "Train and manage an AI PM team, measure ROI, "
            "handle complex distributed North Africa projects, manage AI project crises, "
            "and create an AI governance policy. "
            "Leads to official Euklydia AI Project Manager certification."
        ),
        description_fr=(
            "Construisez et pilotez une stratégie AI PM complète et transformez votre organisation. "
            "Formez et managez une équipe AI PM, mesurez le ROI, "
            "gérez des projets Afrique du Nord complexes et distribués, gérez les crises liées à l'AI dans les projets "
            "et créez une politique de gouvernance AI PM. "
            "Mène à la certification officielle Euklydia AI Project Manager."
        ),
        learning_objective_en=(
            "Build and present a complete AI PM strategy, train and manage an AI PM team, "
            "orchestrate humans and AI in projects, manage complex distributed MENA digital projects, "
            "measure and present AI PM ROI to the CEO, "
            "create an AI PM governance policy, and manage AI-related project crises."
        ),
        learning_objective_fr=(
            "Construire et présenter une stratégie AI PM complète, former et manager une équipe AI PM, "
            "orchestrer humains et AI dans les projets, gérer des projets digitaux MENA complexes et distribués, "
            "mesurer et présenter le ROI de l'AI PM au CEO, "
            "créer une politique de gouvernance AI PM et gérer les crises liées à l'AI dans les projets."
        ),
        level="Advanced",
        estimated_duration_min=300,
        format="vidéo + exercices stratégiques + feedback mentor + certification",
        role="AI Project Manager",
        journey_stage="expert",
        display_order=3,
        key_concepts_en=[
            "Building a complete AI PM strategy",
            "Adapting AI PM strategy to the MENA context",
            "Training and managing an AI PM team",
            "Orchestrating humans and AI in projects",
            "Managing resistance to AI change",
            "Managing complex digital projects in MENA",
            "Coordinating distributed MENA teams",
            "Calculating value created by AI PM",
            "Building executive AI PM dashboards",
            "AI PM governance and project crisis management",
        ],
        key_concepts_fr=[
            "Construire une stratégie AI PM complète",
            "Adapter la stratégie AI PM au contexte MENA",
            "Former et manager une équipe AI PM",
            "Orchestrer humains et AI dans les projets",
            "Gérer la résistance au changement AI",
            "Gérer des projets digitaux complexes en MENA",
            "Coordonner des équipes distribuées MENA",
            "Calculer la valeur créée par l'AI PM",
            "Construire des tableaux de bord exécutifs AI PM",
            "Gouvernance AI PM et gestion des crises de projet",
        ],
        section_content_fr={
            "unite1": {
                "title": "Unité 1 — Stratégie AI PM globale",
                "lessons": [
                    "Leçon 1 — Construire sa stratégie AI PM complète | Vidéo 15 min + Exercice stratégique",
                    "Leçon 2 — Adapter la stratégie au contexte MENA | Vidéo 12 min + Cas pratique",
                    "Leçon 3 — Présenter sa stratégie à la direction | Exercice pratique + Feedback mentor",
                ]
            },
            "unite2": {
                "title": "Unité 2 — Piloter une organisation AI",
                "lessons": [
                    "Leçon 1 — Former son équipe aux outils AI PM | Vidéo 12 min + Exercice pratique",
                    "Leçon 2 — Orchestrer humains et AI dans les projets | Vidéo 10 min + Simulation interactive",
                    "Leçon 3 — Gérer la résistance au changement AI | Cas réel entreprise tunisienne",
                ]
            },
            "unite3": {
                "title": "Unité 3 — Gestion de projets AI complexes Afrique du Nord",
                "lessons": [
                    "Leçon 1 — Gérer des projets digitaux en Afrique du Nord | Vidéo 12 min + Cas pratiques",
                    "Leçon 2 — Coordonner des équipes distribuées Afrique du Nord | Vidéo 12 min + Exercice pratique",
                    "Leçon 3 — L'avenir de l'AI PM en Afrique du Nord | Vidéo + Forum de discussion",
                ]
            },
            "unite4": {
                "title": "Unité 4 — Mesurer le ROI de l'AI PM",
                "lessons": [
                    "Leçon 1 — Calculer la valeur créée par l'AI PM | Vidéo 12 min + Exercice pratique",
                    "Leçon 2 — Créer des tableaux de bord exécutifs | Tutoriel guidé + Exercice pratique",
                    "Leçon 3 — Présenter les résultats au CEO | Exercice pratique + Feedback mentor",
                ]
            },
            "unite5": {
                "title": "Unité 5 — Gouvernance et Éthique AI avancée",
                "lessons": [
                    "Leçon 1 — Créer sa politique de gouvernance AI PM | Vidéo 12 min + Exercice pratique",
                    "Leçon 2 — Gérer les crises liées à l'AI dans les projets | Simulation interactive",
                ]
            },
        },
        section_content_en={
            "unite1": {
                "title": "Unit 1 — Global AI PM Strategy",
                "lessons": [
                    "Lesson 1 — Build your complete AI PM strategy | 15 min video + Strategic exercise",
                    "Lesson 2 — Adapt strategy to MENA context | 12 min video + Case study",
                    "Lesson 3 — Present your strategy to leadership | Practical exercise + Mentor feedback",
                ]
            },
            "unite2": {
                "title": "Unit 2 — Lead an AI Organisation",
                "lessons": [
                    "Lesson 1 — Train your team in AI PM tools | 12 min video + Practical exercise",
                    "Lesson 2 — Orchestrate humans and AI in projects | 10 min video + Interactive simulation",
                    "Lesson 3 — Manage resistance to AI change | Real Tunisian company case",
                ]
            },
            "unite3": {
                "title": "Unit 3 — Complex North Africa AI Project Management",
                "lessons": [
                    "Lesson 1 — Manage digital projects in North Africa | 12 min video + Case studies",
                    "Lesson 2 — Coordinate distributed North Africa teams | 12 min video + Practical exercise",
                    "Lesson 3 — The future of AI PM in North Africa | Video + Discussion forum",
                ]
            },
            "unite4": {
                "title": "Unit 4 — Measure AI PM ROI",
                "lessons": [
                    "Lesson 1 — Calculate value created by AI PM | 12 min video + Practical exercise",
                    "Lesson 2 — Build executive dashboards | Guided tutorial + Practical exercise",
                    "Lesson 3 — Present results to the CEO | Practical exercise + Mentor feedback",
                ]
            },
            "unite5": {
                "title": "Unit 5 — AI Governance and Advanced Ethics",
                "lessons": [
                    "Lesson 1 — Create your AI PM governance policy | 12 min video + Practical exercise",
                    "Lesson 2 — Manage AI-related project crises | Interactive simulation",
                ]
            },
        },
        takeaway_fr="Un AI Project Manager certifié Euklydia pilote une stratégie AI PM complète, transforme son organisation et forme son équipe.",
        takeaway_en="An Euklydia certified AI Project Manager leads a complete AI PM strategy, transforms their organisation, and trains their team.",
        recommended_when_fr="Recommandé quand votre score est 2/2 sur un ou plusieurs skills (niveau Avancé).",
        recommended_when_en="Recommended when your score is 2/2 on one or more skills (Advanced level).",
        why_this_module_fr="Ce module vous prépare à la certification officielle Euklydia AI Project Manager.",
        why_this_module_en="This module prepares you for the official Euklydia AI Project Manager certification.",
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
    print(f"✅ AI Project Manager — 3 modules créés et liés aux {len(skill_ids)} skills")
    print(f"   Module Fondations ID: {module_fondations.id}")
    print(f"   Module Pratique ID:   {module_pratique.id}")
    print(f"   Module Expert ID:     {module_expert.id}")