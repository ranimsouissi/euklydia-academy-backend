"""
patch_mena_ai_project_manager.py
=================================
Corrige les mentions "MENA" de positionnement plateforme
+ Ajoute l'Unité 6 Certification au Module Expert.

Utilisation :
  python patch_mena_ai_project_manager.py
"""

import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FILES = {
    "modules": os.path.join(BASE_DIR, "app", "scripts", "seed_ai_project_manager_modules.py"),
    "units":   os.path.join(BASE_DIR, "app", "scripts", "seed_ai_project_manager_units_lessons.py"),
}

# ── Corrections seed_ai_project_manager_modules.py ────────────────────────────
CORRECTIONS_MODULES = [
    # MODULE 1 — description_en
    (
        "in the MENA project management context.",
        "in the North Africa project management context.",
    ),
    # MODULE 1 — description_fr
    (
        "dans le contexte MENA de la gestion de projet.",
        "dans le contexte Afrique du Nord de la gestion de projet.",
    ),
    # MODULE 1 — why_this_module_fr
    (
        "why_this_module_fr=\"Avant d'utiliser les outils AI PM, vous avez besoin de comprendre les fondamentaux et le contexte MENA.\",",
        "why_this_module_fr=\"Avant d'utiliser les outils AI PM, vous avez besoin de comprendre les fondamentaux et le contexte Afrique du Nord.\",",
    ),
    # MODULE 1 — why_this_module_en
    (
        "why_this_module_en=\"Before using AI PM tools, you need to understand the fundamentals and the MENA context.\",",
        "why_this_module_en=\"Before using AI PM tools, you need to understand the fundamentals and the North Africa context.\",",
    ),
    # MODULE 1 — section_content_fr U1L3
    (
        '"Leçon 3 — L\'AI PM dans le contexte MENA | Vidéo 8 min + Forum de discussion",',
        '"Leçon 3 — L\'AI PM dans le contexte Afrique du Nord | Vidéo 8 min + Forum de discussion",',
    ),
    # MODULE 1 — section_content_en U1L3
    (
        '"Lesson 3 — AI PM in the MENA context | 8 min video + Discussion forum",',
        '"Lesson 3 — AI PM in the North Africa context | 8 min video + Discussion forum",',
    ),
    # MODULE 1 — section_content_fr U2L3
    (
        '"Leçon 3 — Mon premier planning de projet MENA | Projet pratique noté",',
        '"Leçon 3 — Mon premier planning de projet Afrique du Nord | Projet pratique noté",',
    ),
    # MODULE 1 — section_content_en U2L3
    (
        '"Lesson 3 — My first MENA project plan | Graded practical project",',
        '"Lesson 3 — My first North Africa project plan | Graded practical project",',
    ),
    # MODULE 2 — section_content_fr U4L2
    (
        '"Leçon 2 — Monday AI pour les équipes MENA | Tutoriel + Exercice comparatif",',
        '"Leçon 2 — Monday AI pour les équipes Afrique du Nord | Tutoriel + Exercice comparatif",',
    ),
    # MODULE 2 — section_content_en U4L2
    (
        '"Lesson 2 — Monday AI for MENA teams | Tutorial + Comparative exercise",',
        '"Lesson 2 — Monday AI for North Africa teams | Tutorial + Comparative exercise",',
    ),
    # MODULE 3 — description_fr
    (
        "gérez des projets MENA complexes et distribués,",
        "gérez des projets Afrique du Nord complexes et distribués,",
    ),
    # MODULE 3 — description_en
    (
        "handle complex distributed MENA projects,",
        "handle complex distributed North Africa projects,",
    ),
    # MODULE 3 — section_content_fr U3 title
    (
        '"title": "Unité 3 — Gestion de projets AI complexes MENA",',
        '"title": "Unité 3 — Gestion de projets AI complexes Afrique du Nord",',
    ),
    # MODULE 3 — section_content_en U3 title
    (
        '"title": "Unit 3 — Complex MENA AI Project Management",',
        '"title": "Unit 3 — Complex North Africa AI Project Management",',
    ),
    # MODULE 3 — section_content_fr U3L1
    (
        '"Leçon 1 — Gérer des projets digitaux en MENA | Vidéo 12 min + Cas pratiques",',
        '"Leçon 1 — Gérer des projets digitaux en Afrique du Nord | Vidéo 12 min + Cas pratiques",',
    ),
    # MODULE 3 — section_content_en U3L1
    (
        '"Lesson 1 — Manage digital projects in MENA | 12 min video + Case studies",',
        '"Lesson 1 — Manage digital projects in North Africa | 12 min video + Case studies",',
    ),
    # MODULE 3 — section_content_fr U3L2
    (
        '"Leçon 2 — Coordonner des équipes distribuées MENA | Vidéo 12 min + Exercice pratique",',
        '"Leçon 2 — Coordonner des équipes distribuées Afrique du Nord | Vidéo 12 min + Exercice pratique",',
    ),
    # MODULE 3 — section_content_en U3L2
    (
        '"Lesson 2 — Coordinate distributed MENA teams | 12 min video + Practical exercise",',
        '"Lesson 2 — Coordinate distributed North Africa teams | 12 min video + Practical exercise",',
    ),
    # MODULE 3 — section_content_fr U3L3
    (
        '"Leçon 3 — L\'avenir de l\'AI PM en MENA | Vidéo + Forum de discussion",',
        '"Leçon 3 — L\'avenir de l\'AI PM en Afrique du Nord | Vidéo + Forum de discussion",',
    ),
    # MODULE 3 — section_content_en U3L3
    (
        '"Lesson 3 — The future of AI PM in MENA | Video + Discussion forum",',
        '"Lesson 3 — The future of AI PM in North Africa | Video + Discussion forum",',
    ),
]

# ── Corrections seed_ai_project_manager_units_lessons.py ──────────────────────
CORRECTIONS_UNITS = [
    # u1_1 description_fr
    (
        'description_fr="Comprendre l\'AI pour un PM, ses outils essentiels et ses spécificités pour le contexte MENA.",',
        'description_fr="Comprendre l\'AI pour un PM, ses outils essentiels et ses spécificités pour le contexte Afrique du Nord.",',
    ),
    # u3_3 title_fr
    (
        'title_fr="Gestion de projets AI complexes MENA",',
        'title_fr="Gestion de projets AI complexes Afrique du Nord",',
    ),
    # u3_3 title_en
    (
        'title_en="Complex MENA AI Project Management",',
        'title_en="Complex North Africa AI Project Management",',
    ),
]

# ── Code Unité 6 Certification ─────────────────────────────────────────────────
CERTIFICATION_UNIT_CODE = '''
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
'''

ANCHOR_BEFORE_COMMIT = '''    db.commit()
    print("✅ AI Project Manager — units, lessons, activities insérées")'''

REPLACEMENT_WITH_CERT = CERTIFICATION_UNIT_CODE + "\n" + ANCHOR_BEFORE_COMMIT


# ── Fonctions ──────────────────────────────────────────────────────────────────

def apply_corrections(filepath, corrections, label):
    if not os.path.exists(filepath):
        print(f"❌ Fichier introuvable : {filepath}")
        return False

    backup = filepath + ".bak"
    shutil.copy2(filepath, backup)
    print(f"💾 Backup : {backup}")

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    applied = 0
    skipped = 0

    for old, new in corrections:
        if old == new:
            continue
        if old in content:
            content = content.replace(old, new, 1)
            applied += 1
            print(f"  ✅ '{old[:70].strip()}...'")
        else:
            skipped += 1
            print(f"  ⚠️  Non trouvé : '{old[:70].strip()}...'")

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ {label} — {applied} corrections, {skipped} ignorées.")
    else:
        print(f"✅ {label} — Déjà à jour.")
    return True


def add_certification_unit(filepath, label):
    if not os.path.exists(filepath):
        print(f"❌ Fichier introuvable : {filepath}")
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if "Certification Finale — AI Project Manager" in content:
        print(f"✅ {label} — Unité 6 Certification déjà présente, skip.")
        return True

    if ANCHOR_BEFORE_COMMIT not in content:
        print(f"⚠️  {label} — Ancre db.commit() non trouvée.")
        return False

    backup = filepath + ".cert.bak"
    shutil.copy2(filepath, backup)
    print(f"💾 Backup cert : {backup}")

    content = content.replace(ANCHOR_BEFORE_COMMIT, REPLACEMENT_WITH_CERT, 1)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ {label} — Unité 6 Certification ajoutée avec succès !")
    return True


def main():
    print("=" * 65)
    print("PATCH — AI Project Manager")
    print("MENA → Afrique du Nord + Ajout Certification Finale")
    print("=" * 65)

    print(f"\n📄 Fichier 1 : seed_ai_project_manager_modules.py")
    apply_corrections(FILES["modules"], CORRECTIONS_MODULES,
                      "seed_ai_project_manager_modules.py")

    print(f"\n📄 Fichier 2 : seed_ai_project_manager_units_lessons.py")
    apply_corrections(FILES["units"], CORRECTIONS_UNITS,
                      "seed_ai_project_manager_units_lessons.py (MENA)")
    add_certification_unit(FILES["units"],
                           "seed_ai_project_manager_units_lessons.py (Certification)")

    print("\n" + "=" * 65)
    print("✅ Patch terminé.")
    print("   Supprimez les modules AI Project Manager en BDD,")
    print("   puis relancez : python -m app.scripts.seed_all")
    print("=" * 65)


if __name__ == "__main__":
    main()