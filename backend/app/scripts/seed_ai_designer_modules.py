"""
Seed Modules — AI Designer (career_path_id=81)
3 modules : Fondations / Pratique / Expert

Même structure que seed_ai_sales_specialist_modules.py
Inclut : section_content, key_concepts, learning_objective, expected_outcome,
         why_this_module, recommended_when, takeaway, ModuleSkill mapping

Ordre d'exécution :
  1. seed_ai_designer.py          (assessment skills + questions)
  2. seed_ai_designer_modules.py  ← ce fichier
  3. seed_ai_designer_units_lessons.py
"""

from app.models.module import Module
from app.models.module_skill import ModuleSkill
from app.models.skill import Skill


def seed_ai_designer_modules(db):

    # ── Anti-doublon ──────────────────────────────────────────────────────────
    existing = db.query(Module).filter_by(role="AI Designer").first()
    if existing:
        print("⚠️ AI Designer — modules déjà seedés, skip.")
        return

    # ── Récupérer les skills AI Designer (career_path_id = 81) ──────────────────────
    skills = db.query(Skill).filter(Skill.career_path_id == 81).order_by(Skill.id.asc()).all()
    if not skills:
        print("❌ Aucun skill trouvé pour AI Designer (career_path_id=81)")
        return

    skill_ids = [s.id for s in skills]
    print(f"✅ Skills trouvés : {[s.name for s in skills]}")

    # ════════════════════════════════════════════════════════════════════════
    # MODULE 1 — FONDATIONS (Débutant)
    # ════════════════════════════════════════════════════════════════════════
    module_fondations = Module(
        title_fr="AI Designer — Fondations",
        title_en="AI Designer — Foundations",
        description_fr=(
            "Vos premiers pas avec l'AI dans le design. Apprenez à générer vos premières images, "
            "créer vos premiers wireframes, construire des brand assets basiques "
            "et appliquer les règles éthiques fondamentales du design AI "
            "dans le contexte du marché Afrique du Nord."
        ),
        description_en=(
            "Your first steps with AI in design. Learn to generate your first images, "
            "create your first wireframes, build basic brand assets "
            "and apply the fundamental ethical rules of AI design "
            "in the context of the North Africa market."
        ),
        learning_objective_fr=(
            "Générer des images avec Midjourney et Adobe Firefly, "
            "créer des wireframes mobiles avec Figma AI, "
            "construire un logo et une palette de couleurs avec les outils AI, "
            "et respecter les droits d'auteur et règles éthiques de base du design AI."
        ),
        learning_objective_en=(
            "Generate images with Midjourney and Adobe Firefly, "
            "create mobile wireframes with Figma AI, "
            "build a logo and colour palette with AI tools, "
            "and respect basic copyright and ethical rules of AI design."
        ),
        level="Beginner",
        estimated_duration_min=180,
        format="vidéo + quiz + exercices pratiques",
        role="AI Designer",
        journey_stage="foundation",
        display_order=1,
        expected_outcome_fr=(
            "À la fin de ce module, l'apprenant génère des images professionnelles avec Midjourney, "
            "crée des wireframes mobiles RTL/LTR avec Figma AI, "
            "produit un premier logo et une palette de couleurs cohérente, "
            "et applique les règles éthiques de base (droits commerciaux, transparence client)."
        ),
        expected_outcome_en=(
            "By the end of this module, the learner generates professional images with Midjourney, "
            "creates RTL/LTR mobile wireframes with Figma AI, "
            "produces a first logo and coherent colour palette, "
            "and applies basic ethical rules (commercial rights, client transparency)."
        ),
        key_concepts_fr=[
            "Le design AI : révolution créative et outils essentiels",
            "Midjourney : génération d'images professionnelles",
            "Adobe Firefly : images avec droits commerciaux inclus",
            "Figma AI : wireframes et interfaces mobiles",
            "RTL vs LTR : design pour le marché Afrique du Nord",
            "Brand assets basiques : logo, palette, typographie",
            "Droits d'auteur et éthique du design AI",
        ],
        key_concepts_en=[
            "AI design: creative revolution and essential tools",
            "Midjourney: professional image generation",
            "Adobe Firefly: images with commercial rights included",
            "Figma AI: wireframes and mobile interfaces",
            "RTL vs LTR: design for the North Africa market",
            "Basic brand assets: logo, palette, typography",
            "Copyright and ethics in AI design",
        ],
        section_content_fr={
            "unite1": {
                "title": "Unité 1 — L'AI dans le design",
                "lessons": [
                    {"id": "1.1", "title": "C'est quoi le design AI ?", "format": "Vidéo 10 min + Quiz"},
                    {"id": "1.2", "title": "Les outils AI essentiels du designer", "format": "Vidéo 8 min + Tableau comparatif"},
                    {"id": "1.3", "title": "Le design AI dans le contexte Afrique du Nord", "format": "Vidéo 8 min + Forum de discussion"},
                ]
            },
            "unite2": {
                "title": "Unité 2 — Générer ses premières images AI",
                "lessons": [
                    {"id": "2.1", "title": "Introduction à Midjourney", "format": "Tutoriel guidé + Exercice pratique"},
                    {"id": "2.2", "title": "Créer des prompts visuels efficaces", "format": "Vidéo 12 min + Exercice pratique"},
                    {"id": "2.3", "title": "Générer des images adaptées au marché Afrique du Nord", "format": "Projet pratique noté"},
                ]
            },
            "unite3": {
                "title": "Unité 3 — Design UI/UX basique avec AI",
                "lessons": [
                    {"id": "3.1", "title": "C'est quoi l'UI/UX ?", "format": "Vidéo 10 min + Quiz"},
                    {"id": "3.2", "title": "Créer ses premiers wireframes avec Figma AI", "format": "Tutoriel guidé + Exercice"},
                    {"id": "3.3", "title": "Adapter le design au contexte Afrique du Nord", "format": "Vidéo 10 min + Exercice pratique"},
                ]
            },
            "unite4": {
                "title": "Unité 4 — Créer ses premiers brand assets",
                "lessons": [
                    {"id": "4.1", "title": "C'est quoi un système de brand assets ?", "format": "Vidéo 10 min + Quiz"},
                    {"id": "4.2", "title": "Créer un logo simple avec l'AI", "format": "Tutoriel guidé + Exercice pratique"},
                    {"id": "4.3", "title": "Créer une palette de couleurs avec Coolors AI", "format": "Vidéo 8 min + Exercice"},
                ]
            },
            "unite5": {
                "title": "Unité 5 — Éthique AI basique en design",
                "lessons": [
                    {"id": "5.1", "title": "Droits d'auteur et images générées par l'AI", "format": "Vidéo 10 min + Quiz"},
                    {"id": "5.2", "title": "Transparence avec les clients sur l'usage de l'AI", "format": "Cas pratiques interactifs"},
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
                "title": "Unit 1 — AI in Design",
                "lessons": [
                    {"id": "1.1", "title": "What is AI design?", "format": "10 min video + Quiz"},
                    {"id": "1.2", "title": "Essential AI tools for designers", "format": "8 min video + Comparison table"},
                    {"id": "1.3", "title": "AI design in the North Africa context", "format": "8 min video + Discussion forum"},
                ]
            },
            "unite2": {
                "title": "Unit 2 — Generate Your First AI Images",
                "lessons": [
                    {"id": "2.1", "title": "Introduction to Midjourney", "format": "Guided tutorial + Practical exercise"},
                    {"id": "2.2", "title": "Create effective visual prompts", "format": "12 min video + Practical exercise"},
                    {"id": "2.3", "title": "Generate images for the North Africa market", "format": "Graded practical project"},
                ]
            },
            "unite3": {
                "title": "Unit 3 — Basic UI/UX Design with AI",
                "lessons": [
                    {"id": "3.1", "title": "What is UI/UX?", "format": "10 min video + Quiz"},
                    {"id": "3.2", "title": "Create first wireframes with Figma AI", "format": "Guided tutorial + Exercise"},
                    {"id": "3.3", "title": "Adapt design to North Africa context", "format": "10 min video + Practical exercise"},
                ]
            },
            "unite4": {
                "title": "Unit 4 — Create Your First Brand Assets",
                "lessons": [
                    {"id": "4.1", "title": "What is a brand assets system?", "format": "10 min video + Quiz"},
                    {"id": "4.2", "title": "Create a simple logo with AI", "format": "Guided tutorial + Practical exercise"},
                    {"id": "4.3", "title": "Create a colour palette with Coolors AI", "format": "8 min video + Exercise"},
                ]
            },
            "unite5": {
                "title": "Unit 5 — Basic AI Ethics in Design",
                "lessons": [
                    {"id": "5.1", "title": "Copyright and AI-generated images", "format": "10 min video + Quiz"},
                    {"id": "5.2", "title": "Transparency with clients on AI usage", "format": "Interactive case studies"},
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
        takeaway_fr="L'AI ne remplace pas le designer — elle lui permet de créer plus vite, d'explorer plus d'options et de se concentrer sur la direction artistique.",
        takeaway_en="AI does not replace the designer — it allows them to create faster, explore more options and focus on art direction.",
        recommended_when_fr="Recommandé quand votre score est 0/2 sur un ou plusieurs skills (niveau Débutant).",
        recommended_when_en="Recommended when your score is 0/2 on one or more skills (Beginner level).",
        why_this_module_fr="Avant d'utiliser les outils AI design avancés, vous avez besoin de comprendre les fondamentaux, les droits d'auteur et le contexte visuel Afrique du Nord.",
        why_this_module_en="Before using advanced AI design tools, you need to understand the fundamentals, copyright rules and the North Africa visual context.",
        next_recommended_module_fr="AI Designer — Pratique",
        next_recommended_module_en="AI Designer — Practice",
        is_active=True,
    )
    db.add(module_fondations)
    db.flush()

    # ════════════════════════════════════════════════════════════════════════
    # MODULE 2 — PRATIQUE (Intermédiaire)
    # ════════════════════════════════════════════════════════════════════════
    module_pratique = Module(
        title_fr="AI Designer — Pratique",
        title_en="AI Designer — Practice",
        description_fr=(
            "Créez des visuels professionnels et maîtrisez les outils AI avancés. "
            "Développez vos compétences en prompting avancé, UI/UX bilingue AR/FR, "
            "création vidéo avec Runway ML et ElevenLabs, "
            "et systèmes de brand assets complets pour le marché Afrique du Nord."
        ),
        description_en=(
            "Create professional visuals and master advanced AI tools. "
            "Develop your advanced prompting, bilingual AR/FR UI/UX, "
            "video creation with Runway ML and ElevenLabs, "
            "and complete brand assets systems for the North Africa market."
        ),
        learning_objective_fr=(
            "Maîtriser les techniques avancées de prompting culturel MENA, "
            "créer des interfaces bilingues AR/FR complètes avec Figma AI, "
            "produire des vidéos publicitaires avec Runway ML et ElevenLabs, "
            "développer un système de brand assets complet et gérer les droits commerciaux."
        ),
        learning_objective_en=(
            "Master advanced MENA cultural prompting techniques, "
            "create complete bilingual AR/FR interfaces with Figma AI, "
            "produce advertising videos with Runway ML and ElevenLabs, "
            "develop a complete brand assets system and manage commercial rights."
        ),
        level="Intermediate",
        estimated_duration_min=240,
        format="vidéo + exercices pratiques + projets notés",
        role="AI Designer",
        journey_stage="practice",
        display_order=2,
        expected_outcome_fr=(
            "À la fin de ce module, l'apprenant maîtrise le prompting avancé adapté au marché Afrique du Nord, "
            "crée des interfaces mobiles bilingues RTL/LTR professionnelles, "
            "produit des vidéos publicitaires complètes avec voix off bilingue, "
            "et livre des systèmes de brand assets complets avec brand book."
        ),
        expected_outcome_en=(
            "By the end of this module, the learner masters advanced prompting adapted to the North Africa market, "
            "creates professional bilingual RTL/LTR mobile interfaces, "
            "produces complete advertising videos with bilingual voice-over, "
            "and delivers complete brand assets systems with brand book."
        ),
        key_concepts_fr=[
            "Techniques avancées de prompting : négatifs, pondération, référence image",
            "Prompting culturel pour le marché Afrique du Nord",
            "Itération et amélioration des résultats AI",
            "Design UI/UX avancé avec Figma AI — interfaces bilingues AR/FR",
            "Création vidéo AI : Runway ML + ElevenLabs + CapCut AI",
            "Système de brand assets complet et brand book professionnel",
            "Droits commerciaux par outil AI et propriété intellectuelle",
        ],
        key_concepts_en=[
            "Advanced prompting techniques: negatives, weighting, image reference",
            "Cultural prompting for the North Africa market",
            "AI result iteration and improvement",
            "Advanced UI/UX design with Figma AI — bilingual AR/FR interfaces",
            "AI video creation: Runway ML + ElevenLabs + CapCut AI",
            "Complete brand assets system and professional brand book",
            "Commercial rights by AI tool and intellectual property",
        ],
        section_content_fr={
            "unite1": {
                "title": "Unité 1 — Prompting visuel avancé",
                "lessons": [
                    {"id": "1.1", "title": "Les techniques avancées de prompting", "format": "Vidéo 12 min + Exercice pratique"},
                    {"id": "1.2", "title": "Prompting culturel pour le marché Afrique du Nord", "format": "Vidéo 10 min + Exercice pratique"},
                    {"id": "1.3", "title": "Itération et amélioration des résultats", "format": "Tutoriel guidé + Exercice pratique"},
                ]
            },
            "unite2": {
                "title": "Unité 2 — Design UI/UX avancé avec AI",
                "lessons": [
                    {"id": "2.1", "title": "Créer des interfaces complètes avec Figma AI", "format": "Tutoriel avancé + Exercice"},
                    {"id": "2.2", "title": "Intégrer l'AI dans le processus UX", "format": "Vidéo 12 min + Exercice pratique"},
                    {"id": "2.3", "title": "Interface bilingue arabe/français avec AI", "format": "Projet pratique noté"},
                ]
            },
            "unite3": {
                "title": "Unité 3 — Créer des vidéos avec l'AI",
                "lessons": [
                    {"id": "3.1", "title": "Introduction à Runway ML", "format": "Tutoriel guidé + Exercice pratique"},
                    {"id": "3.2", "title": "Voix off en arabe et français avec ElevenLabs", "format": "Tutoriel guidé + Exercice"},
                    {"id": "3.3", "title": "Ma première vidéo publicitaire AI complète", "format": "Projet pratique noté"},
                ]
            },
            "unite4": {
                "title": "Unité 4 — Système de brand assets complet",
                "lessons": [
                    {"id": "4.1", "title": "Créer une identité visuelle complète", "format": "Vidéo 12 min + Projet pratique"},
                    {"id": "4.2", "title": "Templates réseaux sociaux avec AI", "format": "Tutoriel guidé + Exercice pratique"},
                    {"id": "4.3", "title": "Guide d'utilisation de la marque (Brand Book)", "format": "Projet pratique noté"},
                ]
            },
            "unite5": {
                "title": "Unité 5 — Éthique AI intermédiaire",
                "lessons": [
                    {"id": "5.1", "title": "Droits commerciaux des images AI", "format": "Vidéo 12 min + Quiz éthique"},
                    {"id": "5.2", "title": "Propriété intellectuelle et design AI", "format": "Cas pratiques interactifs"},
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
                "title": "Unit 1 — Advanced Visual Prompting",
                "lessons": [
                    {"id": "1.1", "title": "Advanced prompting techniques", "format": "12 min video + Practical exercise"},
                    {"id": "1.2", "title": "Cultural prompting for North Africa market", "format": "10 min video + Practical exercise"},
                    {"id": "1.3", "title": "Iteration and result improvement", "format": "Guided tutorial + Practical exercise"},
                ]
            },
            "unite2": {
                "title": "Unit 2 — Advanced UI/UX Design with AI",
                "lessons": [
                    {"id": "2.1", "title": "Create complete interfaces with Figma AI", "format": "Advanced tutorial + Exercise"},
                    {"id": "2.2", "title": "Integrate AI into the UX process", "format": "12 min video + Practical exercise"},
                    {"id": "2.3", "title": "Bilingual Arabic/French interface with AI", "format": "Graded practical project"},
                ]
            },
            "unite3": {
                "title": "Unit 3 — Creating Videos with AI",
                "lessons": [
                    {"id": "3.1", "title": "Introduction to Runway ML", "format": "Guided tutorial + Practical exercise"},
                    {"id": "3.2", "title": "Voice-over in Arabic and French with ElevenLabs", "format": "Guided tutorial + Exercise"},
                    {"id": "3.3", "title": "My first complete AI advertising video", "format": "Graded practical project"},
                ]
            },
            "unite4": {
                "title": "Unit 4 — Complete Brand Assets System",
                "lessons": [
                    {"id": "4.1", "title": "Create a complete visual identity", "format": "12 min video + Practical project"},
                    {"id": "4.2", "title": "Social media templates with AI", "format": "Guided tutorial + Practical exercise"},
                    {"id": "4.3", "title": "Brand usage guide (Brand Book)", "format": "Graded practical project"},
                ]
            },
            "unite5": {
                "title": "Unit 5 — Intermediate AI Ethics",
                "lessons": [
                    {"id": "5.1", "title": "Commercial rights for AI images", "format": "12 min video + Ethics quiz"},
                    {"id": "5.2", "title": "Intellectual property and AI design", "format": "Interactive case studies"},
                ]
            },
            "final_test": {
                "title": "Final Test — Practice",
                "format": "10 MCQ + 1 Project",
                "minimum_score": "8/10 + Project 70/100",
                "next_access": "Module 3 — Expert"
            }
        },
        takeaway_fr="Un AI Designer intermédiaire produit des visuels professionnels complets, crée des interfaces bilingues et livre des systèmes de brand assets cohérents.",
        takeaway_en="An intermediate AI Designer produces complete professional visuals, creates bilingual interfaces and delivers coherent brand assets systems.",
        recommended_when_fr="Recommandé quand votre score est 1/2 sur un ou plusieurs skills (niveau Intermédiaire).",
        recommended_when_en="Recommended when your score is 1/2 on one or more skills (Intermediate level).",
        why_this_module_fr="Ce module vous permet de passer de la création d'images basiques à une maîtrise complète du design AI professionnel adapté au marché Afrique du Nord.",
        why_this_module_en="This module allows you to move from basic image creation to complete mastery of professional AI design adapted to the North Africa market.",
        next_recommended_module_fr="AI Designer — Expert",
        next_recommended_module_en="AI Designer — Expert",
        is_active=True,
    )
    db.add(module_pratique)
    db.flush()

    # ════════════════════════════════════════════════════════════════════════
    # MODULE 3 — EXPERT (Avancé)
    # ════════════════════════════════════════════════════════════════════════
    module_expert = Module(
        title_fr="AI Designer — Expert",
        title_en="AI Designer — Expert",
        description_fr=(
            "Pilotez une stratégie design AI complète et formez votre équipe. "
            "Maîtrisez la calligraphie arabe et le design moderne, "
            "mesurez le ROI de vos créations AI, "
            "gérez les enjeux éthiques avancés du design AI en Afrique du Nord "
            "et obtenez la certification officielle Euklydia AI Designer."
        ),
        description_en=(
            "Lead a complete AI design strategy and train your team. "
            "Master Arabic calligraphy and modern design, "
            "measure the ROI of your AI creations, "
            "manage advanced ethical issues of AI design in North Africa "
            "and obtain the official Euklydia AI Designer certification."
        ),
        learning_objective_fr=(
            "Construire et piloter un workflow design AI complet, "
            "former et manager une équipe design AI, "
            "créer des identités visuelles bilingues premium avec calligraphie arabe, "
            "mesurer et présenter le ROI du design AI, "
            "créer une politique design AI et gérer les crises éthiques créatives."
        ),
        learning_objective_en=(
            "Build and lead a complete AI design workflow, "
            "train and manage an AI design team, "
            "create premium bilingual visual identities with Arabic calligraphy, "
            "measure and present AI design ROI, "
            "create an AI design policy and manage creative ethical crises."
        ),
        level="Advanced",
        estimated_duration_min=300,
        format="vidéo + exercices stratégiques + feedback mentor + certification",
        role="AI Designer",
        journey_stage="expert",
        display_order=3,
        expected_outcome_fr=(
            "À la fin de ce module, l'apprenant pilote un workflow design AI complet avec productivité × 5, "
            "forme son équipe aux outils AI design, "
            "crée des identités visuelles bilingues premium fusionnant calligraphie arabe et design moderne, "
            "mesure et présente le ROI de ses créations AI, "
            "et détient la certification officielle Euklydia AI Designer."
        ),
        expected_outcome_en=(
            "By the end of this module, the learner leads a complete AI design workflow with 5× productivity, "
            "trains their team in AI design tools, "
            "creates premium bilingual visual identities fusing Arabic calligraphy and modern design, "
            "measures and presents AI design ROI, "
            "and holds the official Euklydia AI Designer certification."
        ),
        key_concepts_fr=[
            "Workflow design AI complet : productivité × 5",
            "Former et piloter une équipe design AI",
            "Orchestrer créativité humaine et AI",
            "Calligraphie arabe et design moderne — identités visuelles premium",
            "Identités visuelles bilingues AR/FR pour le marché Afrique du Nord",
            "Tendances du design AI en Afrique du Nord 2025-2027",
            "Mesurer le ROI du design AI et présenter aux clients",
            "Politique design AI et gestion des crises éthiques créatives",
        ],
        key_concepts_en=[
            "Complete AI design workflow: 5× productivity",
            "Train and lead an AI design team",
            "Orchestrate human creativity and AI",
            "Arabic calligraphy and modern design — premium visual identities",
            "Bilingual AR/FR visual identities for the North Africa market",
            "AI design trends in North Africa 2025-2027",
            "Measure AI design ROI and present to clients",
            "AI design policy and managing creative ethical crises",
        ],
        section_content_fr={
            "unite1": {
                "title": "Unité 1 — Stratégie design AI globale",
                "lessons": [
                    {"id": "1.1", "title": "Construire son workflow design AI complet", "format": "Vidéo 15 min + Exercice stratégique"},
                    {"id": "1.2", "title": "Intégrer l'AI dans tous les projets créatifs", "format": "Vidéo 12 min + Cas pratique"},
                    {"id": "1.3", "title": "Présenter sa stratégie AI aux clients", "format": "Exercice pratique + Feedback mentor"},
                ]
            },
            "unite2": {
                "title": "Unité 2 — Piloter une équipe design AI",
                "lessons": [
                    {"id": "2.1", "title": "Former son équipe aux outils AI design", "format": "Vidéo 12 min + Exercice pratique"},
                    {"id": "2.2", "title": "Orchestrer créativité humaine et AI", "format": "Vidéo 10 min + Simulation"},
                    {"id": "2.3", "title": "Maintenir l'authenticité de la marque avec l'AI", "format": "Cas réel agence tunisienne"},
                ]
            },
            "unite3": {
                "title": "Unité 3 — Design AI avancé Afrique du Nord",
                "lessons": [
                    {"id": "3.1", "title": "Calligraphie arabe et design moderne", "format": "Vidéo 15 min + Projet pratique"},
                    {"id": "3.2", "title": "Identités visuelles bilingues avec l'AI", "format": "Vidéo 12 min + Projet pratique"},
                    {"id": "3.3", "title": "Tendances du design AI en Afrique du Nord", "format": "Vidéo + Forum de discussion"},
                ]
            },
            "unite4": {
                "title": "Unité 4 — Mesurer le ROI du design AI",
                "lessons": [
                    {"id": "4.1", "title": "Calculer la valeur créée par l'AI", "format": "Vidéo 12 min + Exercice pratique"},
                    {"id": "4.2", "title": "Présenter les résultats à ses clients", "format": "Exercice + Feedback mentor"},
                    {"id": "4.3", "title": "Optimiser son workflow AI continuellement", "format": "Exercice stratégique + Forum"},
                ]
            },
            "unite5": {
                "title": "Unité 5 — Gouvernance et Éthique AI avancée",
                "lessons": [
                    {"id": "5.1", "title": "Créer sa politique design AI", "format": "Vidéo 12 min + Exercice pratique"},
                    {"id": "5.2", "title": "Gérer les crises éthiques créatives AI", "format": "Simulation interactive"},
                ]
            },
            "unite6": {
                "title": "Unité 6 — Certification Finale",
                "is_cert": True,
                "lessons": [
                    {"id": "6.1", "title": "Test final — 20 questions", "format": "30 minutes | Score minimum 80%"},
                    {"id": "6.2", "title": "Projet de certification — Dossier complet design AI", "format": "Évaluation jury Euklydia"},
                ]
            },
            "certification_finale": {
                "title": "Certification Finale — AI Designer",
                "format": "Test 20 questions + Projet complet + Présentation jury Euklydia",
                "score_minimum": "80% test + 75/100 projet",
                "livrables": [
                    "Portfolio design AI (10 créations)",
                    "Identité visuelle bilingue AR/FR complète",
                    "Interface mobile bilingue (5 écrans AR + 5 écrans FR)",
                    "Vidéo publicitaire AI complète bilingue",
                    "Politique design AI officielle",
                    "Présentation stratégique clients"
                ],
                "certification": "Badge LinkedIn officiel + Certificat PDF + Annuaire Euklydia Afrique du Nord",
                "validite": "2 ans"
            }
        },
        section_content_en={
            "unite1": {
                "title": "Unit 1 — Global AI Design Strategy",
                "lessons": [
                    {"id": "1.1", "title": "Build your complete AI design workflow", "format": "15 min video + Strategic exercise"},
                    {"id": "1.2", "title": "Integrate AI into all creative projects", "format": "12 min video + Case study"},
                    {"id": "1.3", "title": "Present your AI strategy to clients", "format": "Practical exercise + Mentor feedback"},
                ]
            },
            "unite2": {
                "title": "Unit 2 — Lead an AI Design Team",
                "lessons": [
                    {"id": "2.1", "title": "Train your team in AI design tools", "format": "12 min video + Practical exercise"},
                    {"id": "2.2", "title": "Orchestrate human creativity and AI", "format": "10 min video + Simulation"},
                    {"id": "2.3", "title": "Maintain brand authenticity with AI", "format": "Real Tunisian agency case"},
                ]
            },
            "unite3": {
                "title": "Unit 3 — Advanced AI Design North Africa",
                "lessons": [
                    {"id": "3.1", "title": "Arabic calligraphy and modern design", "format": "15 min video + Practical project"},
                    {"id": "3.2", "title": "Bilingual visual identities with AI", "format": "12 min video + Practical project"},
                    {"id": "3.3", "title": "AI design trends in North Africa", "format": "Video + Discussion forum"},
                ]
            },
            "unite4": {
                "title": "Unit 4 — Measuring AI Design ROI",
                "lessons": [
                    {"id": "4.1", "title": "Calculate the value created by AI", "format": "12 min video + Practical exercise"},
                    {"id": "4.2", "title": "Present results to clients", "format": "Exercise + Mentor feedback"},
                    {"id": "4.3", "title": "Continuously optimise your AI workflow", "format": "Strategic exercise + Forum"},
                ]
            },
            "unite5": {
                "title": "Unit 5 — AI Governance and Advanced Ethics",
                "lessons": [
                    {"id": "5.1", "title": "Create your AI design policy", "format": "12 min video + Practical exercise"},
                    {"id": "5.2", "title": "Manage creative AI ethical crises", "format": "Interactive simulation"},
                ]
            },
            "unite6": {
                "title": "Unit 6 — Final Certification",
                "is_cert": True,
                "lessons": [
                    {"id": "6.1", "title": "Final test — 20 questions", "format": "30 minutes | Minimum score 80%"},
                    {"id": "6.2", "title": "Certification project — Complete AI design portfolio", "format": "Euklydia jury evaluation"},
                ]
            },
            "final_certification": {
                "title": "Final Certification — AI Designer",
                "format": "20Q test + Complete project + Euklydia jury presentation",
                "minimum_score": "80% test + 75/100 project",
                "certification": "Official LinkedIn badge + PDF certificate + Euklydia North Africa directory",
                "validity": "2 years"
            }
        },
        takeaway_fr="Un AI Designer certifié Euklydia pilote une stratégie design AI complète, forme son équipe et maîtrise l'esthétique visuelle unique de l'Afrique du Nord.",
        takeaway_en="An Euklydia certified AI Designer leads a complete AI design strategy, trains their team and masters the unique visual aesthetic of North Africa.",
        recommended_when_fr="Recommandé quand votre score est 2/2 sur un ou plusieurs skills (niveau Avancé).",
        recommended_when_en="Recommended when your score is 2/2 on one or more skills (Advanced level).",
        why_this_module_fr="Ce module vous prépare à la certification officielle Euklydia AI Designer et fait de vous un expert reconnu du design AI en Afrique du Nord.",
        why_this_module_en="This module prepares you for the official Euklydia AI Designer certification and makes you a recognised AI design expert in North Africa.",
        next_recommended_module_fr=None,
        next_recommended_module_en=None,
        is_active=True,
    )
    db.add(module_expert)
    db.flush()

    # ── ModuleSkill Mapping ───────────────────────────────────────────────────
    for skill_id in skill_ids:
        db.add(ModuleSkill(module_id=module_fondations.id, skill_id=skill_id))
        db.add(ModuleSkill(module_id=module_pratique.id, skill_id=skill_id))
        db.add(ModuleSkill(module_id=module_expert.id, skill_id=skill_id))

    db.commit()
    print(f"✅ AI Designer — 3 modules complets créés et liés aux {len(skill_ids)} skills")
    print(f"   Module Fondations ID: {module_fondations.id}")
    print(f"   Module Pratique ID:   {module_pratique.id}")
    print(f"   Module Expert ID:     {module_expert.id}")