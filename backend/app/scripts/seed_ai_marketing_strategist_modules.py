from app.models.module import Module
from app.models.module_skill import ModuleSkill
from app.models.skill import Skill


def seed_ai_marketing_strategist_modules(db):
    # =============================
    # Récupérer les skills AI Marketing Strategist (career_path_id = 80)
    # =============================
    skills = db.query(Skill).filter(Skill.career_path_id == 80).order_by(Skill.id.desc()).limit(5).all()
    skills = list(reversed(skills))  # remettre dans l'ordre
    if not skills:
        print("❌ Aucun skill trouvé pour AI Marketing Strategist (career_path_id=80)")
        return

    skill_ids = [s.id for s in skills]
    print(f"✅ Skills trouvés : {[s.name for s in skills]}")

    # =============================
    # Supprimer les anciens modules de ce rôle
    # =============================
    existing_modules = db.query(Module).filter(Module.role == "AI Marketing Strategist").all()
    for m in existing_modules:
        db.query(ModuleSkill).filter(ModuleSkill.module_id == m.id).delete()
        db.delete(m)
    db.flush()

    # =============================
    # MODULE 1 — Fondations (Débutant)
    # =============================
    module_fondations = Module(
        title_en="AI Marketing Strategist — Foundations",
        title_fr="AI Marketing Strategist — Fondations",
        description_en=(
            "Your first steps with AI in marketing. Learn to use ChatGPT for content creation, "
            "understand AI marketing tools, manage social media with AI, launch your first "
            "email campaign, and apply ethical principles in the North Africa market context."
        ),
        description_fr=(
            "Vos premiers pas avec l'AI dans le marketing. Apprenez à utiliser ChatGPT pour la création "
            "de contenu, comprendre les outils AI marketing, gérer les réseaux sociaux avec l'AI, "
            "lancer votre première campagne email et appliquer les principes éthiques dans le contexte Afrique du Nord."
        ),
        learning_objective_en=(
            "Use ChatGPT to create content in Arabic and French, manage social media with AI, "
            "launch a first email campaign with Mailchimp AI, create simple visuals with Canva AI, "
            "and respect basic ethical and copyright rules."
        ),
        learning_objective_fr=(
            "Utiliser ChatGPT pour créer du contenu en arabe et français, gérer les réseaux sociaux avec l'AI, "
            "lancer une première campagne email avec Mailchimp AI, créer des visuels simples avec Canva AI "
            "et respecter les règles éthiques et droits d'auteur de base."
        ),
        level="Beginner",
        estimated_duration_min=180,
        format="video + quiz + exercices pratiques",
        role="AI Marketing Strategist",
        journey_stage="foundation",
        display_order=1,
        key_concepts_en=[
            "AI in marketing: what it changes today",
            "Essential marketing AI tools (ChatGPT, Canva AI, Mailchimp AI, Buffer AI)",
            "Content creation with ChatGPT in Arabic and French",
            "Social media management with AI",
            "First AI email marketing campaign",
            "Basic AI ethics: copyright and transparency",
        ],
        key_concepts_fr=[
            "L'AI dans le marketing : ce qu'elle change aujourd'hui",
            "Outils AI essentiels du marketeur (ChatGPT, Canva AI, Mailchimp AI, Buffer AI)",
            "Créer du contenu avec ChatGPT en arabe et français",
            "Gérer les réseaux sociaux avec l'AI",
            "Première campagne email marketing AI",
            "Éthique AI basique : droits d'auteur et transparence",
        ],
        section_content_fr={
            "unite1": {
                "title": "Unité 1 — L'AI dans le marketing",
                "lessons": [
                    "Leçon 1 — C'est quoi le marketing AI ? | Vidéo 10 min + Quiz",
                    "Leçon 2 — Les outils AI essentiels du marketeur | Vidéo 8 min + Tableau comparatif",
                    "Leçon 3 — Le marketing AI dans le contexte Afrique du Nord | Vidéo 8 min + Forum discussion",
                ]
            },
            "unite2": {
                "title": "Unité 2 — Créer du contenu avec l'AI",
                "lessons": [
                    "Leçon 1 — Rédiger avec ChatGPT en arabe et français | Vidéo 12 min + Exercice",
                    "Leçon 2 — Créer des visuels avec Canva AI | Tutoriel guidé + Exercice pratique",
                    "Leçon 3 — Adapter le contenu au contexte Afrique du Nord | Vidéo 10 min + Exercice pratique",
                ]
            },
            "unite3": {
                "title": "Unité 3 — Les réseaux sociaux avec l'AI",
                "lessons": [
                    "Leçon 1 — Gérer ses réseaux avec l'AI | Vidéo 10 min + Quiz",
                    "Leçon 2 — Planifier ses publications automatiquement | Tutoriel Buffer AI + Exercice",
                    "Leçon 3 — Mon premier calendrier de contenu AI | Projet pratique noté",
                ]
            },
            "unite4": {
                "title": "Unité 4 — Mon premier email marketing AI",
                "lessons": [
                    "Leçon 1 — C'est quoi une campagne email ? | Vidéo 8 min + Quiz",
                    "Leçon 2 — Créer sa première campagne avec Mailchimp AI | Tutoriel guidé",
                    "Leçon 3 — Analyser les résultats basiques | Vidéo 10 min + Exercice pratique",
                ]
            },
            "unite5": {
                "title": "Unité 5 — Éthique AI marketing basique",
                "lessons": [
                    "Leçon 1 — Droits d'auteur et contenu AI | Vidéo 10 min + Quiz éthique",
                    "Leçon 2 — Transparence et responsabilité | Cas pratiques interactifs",
                ]
            },
        },
        section_content_en={
            "unite1": {
                "title": "Unit 1 — AI in Marketing",
                "lessons": [
                    "Lesson 1 — What is AI marketing? | 10 min video + Quiz",
                    "Lesson 2 — Essential marketing AI tools | 8 min video + Comparison table",
                    "Lesson 3 — AI marketing in the North Africa context | 8 min video + Discussion forum",
                ]
            },
            "unite2": {
                "title": "Unit 2 — Create Content with AI",
                "lessons": [
                    "Lesson 1 — Writing with ChatGPT in Arabic and French | 12 min video + Exercise",
                    "Lesson 2 — Create visuals with Canva AI | Guided tutorial + Practical exercise",
                    "Lesson 3 — Adapt content to North Africa context | 10 min video + Practical exercise",
                ]
            },
            "unite3": {
                "title": "Unit 3 — Social Media with AI",
                "lessons": [
                    "Lesson 1 — Manage your social media with AI | 10 min video + Quiz",
                    "Lesson 2 — Schedule publications automatically | Buffer AI tutorial + Exercise",
                    "Lesson 3 — My first AI content calendar | Graded practical project",
                ]
            },
            "unite4": {
                "title": "Unit 4 — My First AI Email Marketing",
                "lessons": [
                    "Lesson 1 — What is an email campaign? | 8 min video + Quiz",
                    "Lesson 2 — Create your first campaign with Mailchimp AI | Guided tutorial",
                    "Lesson 3 — Analyse basic results | 10 min video + Practical exercise",
                ]
            },
            "unite5": {
                "title": "Unit 5 — Basic AI Marketing Ethics",
                "lessons": [
                    "Lesson 1 — Copyright and AI content | 10 min video + Ethics quiz",
                    "Lesson 2 — Transparency and accountability | Interactive case studies",
                ]
            },
        },
        takeaway_fr="L'AI ne remplace pas le marketeur — elle lui permet de créer plus vite et de mieux cibler son audience.",
        takeaway_en="AI does not replace the marketer — it allows them to create faster and better target their audience.",
        recommended_when_fr="Recommandé quand votre score est 0/2 sur un ou plusieurs skills (niveau Débutant).",
        recommended_when_en="Recommended when your score is 0/2 on one or more skills (Beginner level).",
        why_this_module_fr="Avant d'utiliser les outils AI marketing, vous avez besoin de comprendre les fondamentaux et le contexte Afrique du Nord.",
        why_this_module_en="Before using marketing AI tools, you need to understand the fundamentals and the North Africa context.",
        next_recommended_module_fr="AI Marketing Strategist — Pratique",
        next_recommended_module_en="AI Marketing Strategist — Practice",
        is_active=True,
    )
    db.add(module_fondations)
    db.flush()

    # =============================
    # MODULE 2 — Pratique (Intermédiaire)
    # =============================
    module_pratique = Module(
        title_en="AI Marketing Strategist — Practice",
        title_fr="AI Marketing Strategist — Pratique",
        description_en=(
            "Automate your campaigns and analyse marketing data with AI. "
            "Create automated content sequences, master Google Analytics AI, "
            "build high-performing ads with AI, and develop an advanced AI content strategy "
            "for the MENA market."
        ),
        description_fr=(
            "Automatisez vos campagnes et analysez les données marketing avec l'AI. "
            "Créez des séquences de contenu automatisées, maîtrisez Google Analytics AI, "
            "créez des publicités performantes avec l'AI et développez une stratégie de contenu "
            "AI avancée pour le marché MENA."
        ),
        learning_objective_en=(
            "Create automated content sequences, plan 1 month of content in 1 hour, "
            "analyse marketing data with AI, build high-performing Facebook/Google ads, "
            "develop an advanced multichannel AI content strategy, and manage data ethically."
        ),
        learning_objective_fr=(
            "Créer des séquences de contenu automatisées, planifier 1 mois de contenu en 1 heure, "
            "analyser les données marketing avec l'AI, créer des publicités Facebook/Google performantes, "
            "développer une stratégie de contenu AI multicanale avancée et gérer les données éthiquement."
        ),
        level="Intermediate",
        estimated_duration_min=240,
        format="video + exercices pratiques + projet noté",
        role="AI Marketing Strategist",
        journey_stage="practice",
        display_order=2,
        key_concepts_en=[
            "Automated content sequences (Buffer AI + Hootsuite AI)",
            "Analysing marketing data with Google Analytics AI",
            "High-performing Facebook and Instagram Ads with AI",
            "Google Ads with AI",
            "SEO with AI for the MENA market",
            "Video marketing with AI (Runway ML + ElevenLabs)",
            "Multichannel AI content strategy",
            "Responsible data management (MENA client data protection)",
        ],
        key_concepts_fr=[
            "Séquences de contenu automatisées (Buffer AI + Hootsuite AI)",
            "Analyser les données marketing avec Google Analytics AI",
            "Publicités Facebook et Instagram performantes avec l'AI",
            "Google Ads avec l'AI",
            "SEO avec l'AI pour le marché MENA",
            "Vidéos marketing avec l'AI (Runway ML + ElevenLabs)",
            "Stratégie de contenu AI multicanale",
            "Gestion responsable des données (protection des données clients MENA)",
        ],
        section_content_fr={
            "unite1": {
                "title": "Unité 1 — Automatiser ses campagnes",
                "lessons": [
                    "Leçon 1 — Créer des séquences de contenu automatisées | Vidéo 12 min + Exercice",
                    "Leçon 2 — Planifier 1 mois de contenu en 1 heure | Tutoriel + Projet pratique noté",
                    "Leçon 3 — Automatiser les publications | Buffer AI + Hootsuite AI + Exercice",
                ]
            },
            "unite2": {
                "title": "Unité 2 — Analyser les données marketing AI",
                "lessons": [
                    "Leçon 1 — Comprendre Google Analytics AI | Vidéo 12 min + Quiz",
                    "Leçon 2 — Lire et interpréter les insights | Vidéo 10 min + Exercice pratique",
                    "Leçon 3 — Prendre des décisions basées sur les données | Cas pratique PME tunisienne",
                ]
            },
            "unite3": {
                "title": "Unité 3 — Créer des publicités AI performantes",
                "lessons": [
                    "Leçon 1 — Facebook et Instagram Ads avec AI | Tutoriel guidé + Exercice",
                    "Leçon 2 — Google Ads avec AI | Vidéo 12 min + Exercice pratique",
                    "Leçon 3 — Ma campagne publicitaire Afrique du Nord complète | Projet pratique noté",
                ]
            },
            "unite4": {
                "title": "Unité 4 — Stratégie contenu AI avancée",
                "lessons": [
                    "Leçon 1 — SEO avec l'AI pour le marché Afrique du Nord | Vidéo 12 min + Exercice",
                    "Leçon 2 — Créer des vidéos marketing avec l'AI | Runway ML + ElevenLabs + Exercice",
                    "Leçon 3 — Stratégie multicanale AI | Projet pratique noté",
                ]
            },
            "unite5": {
                "title": "Unité 5 — Éthique AI intermédiaire",
                "lessons": [
                    "Leçon 1 — Protection des données clients Afrique du Nord | Vidéo 12 min + Quiz éthique",
                    "Leçon 2 — Publicité responsable avec l'AI | Cas pratiques interactifs",
                ]
            },
        },
        section_content_en={
            "unite1": {
                "title": "Unit 1 — Automate Your Campaigns",
                "lessons": [
                    "Lesson 1 — Create automated content sequences | 12 min video + Exercise",
                    "Lesson 2 — Plan 1 month of content in 1 hour | Tutorial + Graded practical project",
                    "Lesson 3 — Automate publications | Buffer AI + Hootsuite AI + Exercise",
                ]
            },
            "unite2": {
                "title": "Unit 2 — Analyse Marketing Data with AI",
                "lessons": [
                    "Lesson 1 — Understanding Google Analytics AI | 12 min video + Quiz",
                    "Lesson 2 — Read and interpret insights | 10 min video + Practical exercise",
                    "Lesson 3 — Data-driven decisions | Tunisian SME case study",
                ]
            },
            "unite3": {
                "title": "Unit 3 — Create High-Performing AI Ads",
                "lessons": [
                    "Lesson 1 — Facebook and Instagram Ads with AI | Guided tutorial + Exercise",
                    "Lesson 2 — Google Ads with AI | 12 min video + Practical exercise",
                    "Lesson 3 — My complete North Africa ad campaign | Graded practical project",
                ]
            },
            "unite4": {
                "title": "Unit 4 — Advanced AI Content Strategy",
                "lessons": [
                    "Lesson 1 — SEO with AI for the North Africa market | 12 min video + Exercise",
                    "Lesson 2 — Create marketing videos with AI | Runway ML + ElevenLabs + Exercise",
                    "Lesson 3 — Multichannel AI strategy | Graded practical project",
                ]
            },
            "unite5": {
                "title": "Unit 5 — Intermediate AI Ethics",
                "lessons": [
                    "Lesson 1 — North Africa client data protection | 12 min video + Ethics quiz",
                    "Lesson 2 — Responsible advertising with AI | Interactive case studies",
                ]
            },
        },
        takeaway_fr="Un AI Marketing Strategist intermédiaire automatise ses campagnes et prend des décisions basées sur les données.",
        takeaway_en="An intermediate AI Marketing Strategist automates campaigns and makes data-driven decisions.",
        recommended_when_fr="Recommandé quand votre score est 1/2 sur un ou plusieurs skills (niveau Intermédiaire).",
        recommended_when_en="Recommended when your score is 1/2 on one or more skills (Intermediate level).",
        why_this_module_fr="Ce module vous permet de passer de la création de contenu basique à une stratégie marketing AI systématique et automatisée.",
        why_this_module_en="This module allows you to move from basic content creation to a systematic and automated AI marketing strategy.",
        next_recommended_module_fr="AI Marketing Strategist — Expert",
        next_recommended_module_en="AI Marketing Strategist — Expert",
        is_active=True,
    )
    db.add(module_pratique)
    db.flush()

    # =============================
    # MODULE 3 — Expert (Avancé)
    # =============================
    module_expert = Module(
        title_en="AI Marketing Strategist — Expert",
        title_fr="AI Marketing Strategist — Expert",
        description_en=(
            "Build and lead a complete AI marketing strategy. "
            "Train and manage an AI marketing team, measure ROI, "
            "handle complex North Africa cultural campaigns, manage AI reputation crises, "
            "and create an AI governance policy. "
            "Leads to official Euklydia AI Marketing Strategist certification."
        ),
        description_fr=(
            "Construisez et pilotez une stratégie AI marketing complète. "
            "Formez et managez une équipe marketing AI, mesurez le ROI, "
            "gérez des campagnes culturelles MENA complexes, gérez les crises de réputation AI "
            "et créez une politique de gouvernance AI. "
            "Mène à la certification officielle Euklydia AI Marketing Strategist."
        ),
        learning_objective_en=(
            "Build and lead a complete AI marketing strategy, train and manage an AI marketing team, "
            "measure and present AI marketing ROI, manage complex cultural MENA campaigns, "
            "handle AI reputation crises, create an AI governance policy."
        ),
        learning_objective_fr=(
            "Construire et piloter une stratégie AI marketing complète, former et manager une équipe marketing AI, "
            "mesurer et présenter le ROI du marketing AI, gérer des campagnes culturelles MENA complexes, "
            "gérer les crises de réputation AI, créer une politique de gouvernance AI."
        ),
        level="Advanced",
        estimated_duration_min=300,
        format="video + exercices stratégiques + feedback mentor + certification",
        role="AI Marketing Strategist",
        journey_stage="expert",
        display_order=3,
        key_concepts_en=[
            "Building a complete AI marketing strategy",
            "Aligning AI marketing with business objectives",
            "Training and managing an AI marketing team",
            "Orchestrating humans and AI in marketing",
            "Measuring and presenting AI marketing ROI",
            "Cultural MENA campaigns with AI",
            "Marketing in dialectal Arabic with AI",
            "AI governance and reputation crisis management",
        ],
        key_concepts_fr=[
            "Construire une stratégie AI marketing complète",
            "Aligner le marketing AI avec les objectifs business",
            "Former et manager une équipe marketing AI",
            "Orchestrer humains et AI dans le marketing",
            "Mesurer et présenter le ROI du marketing AI",
            "Campagnes culturelles MENA avec l'AI",
            "Marketing en arabe dialectal avec l'AI",
            "Gouvernance AI et gestion des crises de réputation",
        ],
        section_content_fr={
            "unite1": {
                "title": "Unité 1 — Stratégie AI marketing globale",
                "lessons": [
                    "Leçon 1 — Construire sa stratégie AI marketing | Vidéo 15 min + Exercice stratégique",
                    "Leçon 2 — Aligner marketing AI et objectifs business | Vidéo 12 min + Cas pratique",
                    "Leçon 3 — Présenter sa stratégie à la direction | Exercice + Feedback mentor",
                ]
            },
            "unite2": {
                "title": "Unité 2 — Piloter une équipe marketing AI",
                "lessons": [
                    "Leçon 1 — Former son équipe aux outils AI | Vidéo 12 min + Exercice pratique",
                    "Leçon 2 — Orchestrer humains et AI dans le marketing | Vidéo 10 min + Simulation",
                    "Leçon 3 — Gérer la créativité humaine et AI | Cas réel agence marketing tunisienne",
                ]
            },
            "unite3": {
                "title": "Unité 3 — Mesurer le ROI du marketing AI",
                "lessons": [
                    "Leçon 1 — C'est quoi le ROI en marketing ? | Vidéo 12 min + Quiz",
                    "Leçon 2 — Créer son dashboard marketing AI | Tutoriel guidé + Exercice",
                    "Leçon 3 — Présenter les résultats à la direction | Exercice + Feedback mentor",
                ]
            },
            "unite4": {
                "title": "Unité 4 — Marketing AI avancé Afrique du Nord",
                "lessons": [
                    "Leçon 1 — Campagnes culturelles MENA avec l'AI | Vidéo 15 min + Projet pratique",
                    "Leçon 2 — Marketing en arabe dialectal avec l'AI | Vidéo 12 min + Exercice",
                    "Leçon 3 — L'avenir du marketing AI en Afrique du Nord | Vidéo + Forum discussion",
                ]
            },
            "unite5": {
                "title": "Unité 5 — Gouvernance et Éthique AI avancée",
                "lessons": [
                    "Leçon 1 — Créer sa politique marketing AI | Vidéo 12 min + Exercice pratique",
                    "Leçon 2 — Gérer les crises de réputation AI | Simulation interactive",
                ]
            },
        },
        section_content_en={
            "unite1": {
                "title": "Unit 1 — Global AI Marketing Strategy",
                "lessons": [
                    "Lesson 1 — Build your AI marketing strategy | 15 min video + Strategic exercise",
                    "Lesson 2 — Align AI marketing with business objectives | 12 min video + Case study",
                    "Lesson 3 — Present your strategy to leadership | Exercise + Mentor feedback",
                ]
            },
            "unite2": {
                "title": "Unit 2 — Lead an AI Marketing Team",
                "lessons": [
                    "Lesson 1 — Train your team in AI tools | 12 min video + Practical exercise",
                    "Lesson 2 — Orchestrate humans and AI in marketing | 10 min video + Simulation",
                    "Lesson 3 — Manage human and AI creativity | Real Tunisian marketing agency case",
                ]
            },
            "unite3": {
                "title": "Unit 3 — Measure AI Marketing ROI",
                "lessons": [
                    "Lesson 1 — What is ROI in marketing? | 12 min video + Quiz",
                    "Lesson 2 — Build your AI marketing dashboard | Guided tutorial + Exercise",
                    "Lesson 3 — Present results to leadership | Exercise + Mentor feedback",
                ]
            },
            "unite4": {
                "title": "Unit 4 — Advanced AI Marketing North Africa",
                "lessons": [
                    "Lesson 1 — Cultural MENA campaigns with AI | 15 min video + Practical project",
                    "Lesson 2 — Marketing in dialectal Arabic with AI | 12 min video + Exercise",
                    "Lesson 3 — The future of AI marketing in North Africa | Video + Discussion forum",
                ]
            },
            "unite5": {
                "title": "Unit 5 — AI Governance and Advanced Ethics",
                "lessons": [
                    "Lesson 1 — Create your AI marketing policy | 12 min video + Practical exercise",
                    "Lesson 2 — Manage AI reputation crises | Interactive simulation",
                ]
            },
        },
        takeaway_fr="Un AI Marketing Strategist certifié Euklydia pilote une stratégie AI complète et forme son équipe.",
        takeaway_en="An Euklydia certified AI Marketing Strategist leads a complete AI strategy and trains their team.",
        recommended_when_fr="Recommandé quand votre score est 2/2 sur un ou plusieurs skills (niveau Avancé).",
        recommended_when_en="Recommended when your score is 2/2 on one or more skills (Advanced level).",
        why_this_module_fr="Ce module vous prépare à la certification officielle Euklydia AI Marketing Strategist.",
        why_this_module_en="This module prepares you for the official Euklydia AI Marketing Strategist certification.",
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
    print(f"✅ AI Marketing Strategist — 3 modules créés et liés aux {len(skill_ids)} skills")
    print(f"   Module Fondations ID: {module_fondations.id}")
    print(f"   Module Pratique ID:   {module_pratique.id}")
    print(f"   Module Expert ID:     {module_expert.id}")