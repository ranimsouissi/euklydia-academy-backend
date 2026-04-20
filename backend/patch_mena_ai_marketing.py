"""
patch_mena_ai_marketing.py
==========================
Corrige les mentions "MENA" de positionnement plateforme dans les 2 fichiers
seed AI Marketing Strategist + ajoute l'Unité 6 Certification au Module Expert.

Corrections appliquées :
  ✅ MENA → Afrique du Nord dans les champs de positionnement plateforme
  ✅ Ajout Unité 6 — Certification Finale dans seed_ai_marketing_units_lessons.py

Utilisation :
  python patch_mena_ai_marketing.py
  Les backups .bak sont créés automatiquement.
"""

import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FILES = {
    "modules": os.path.join(BASE_DIR, "app", "scripts", "seed_ai_marketing_strategist_modules.py"),
    "units":   os.path.join(BASE_DIR, "app", "scripts", "seed_ai_marketing_units_lessons.py"),
}

# ── Corrections seed_ai_marketing_strategist_modules.py ───────────────────────
CORRECTIONS_MODULES = [

    # MODULE 1 — Fondations
    (
        "in the MENA market context.",
        "in the North Africa market context.",
    ),
    (
        "appliquer les principes éthiques dans le contexte MENA.",
        "appliquer les principes éthiques dans le contexte Afrique du Nord.",
    ),
    (
        "why_this_module_fr=\"Avant d'utiliser les outils AI marketing, vous avez besoin de comprendre les fondamentaux et le contexte MENA.\",",
        "why_this_module_fr=\"Avant d'utiliser les outils AI marketing, vous avez besoin de comprendre les fondamentaux et le contexte Afrique du Nord.\",",
    ),
    (
        "why_this_module_en=\"Before using marketing AI tools, you need to understand the fundamentals and the MENA context.\",",
        "why_this_module_en=\"Before using marketing AI tools, you need to understand the fundamentals and the North Africa context.\",",
    ),
    # section_content M1
    (
        '"Leçon 3 — Le marketing AI dans le contexte MENA | Vidéo 8 min + Forum discussion",',
        '"Leçon 3 — Le marketing AI dans le contexte Afrique du Nord | Vidéo 8 min + Forum discussion",',
    ),
    (
        '"Lesson 3 — AI marketing in the MENA context | 8 min video + Discussion forum",',
        '"Lesson 3 — AI marketing in the North Africa context | 8 min video + Discussion forum",',
    ),
    (
        '"Leçon 3 — Adapter le contenu au contexte MENA | Vidéo 10 min + Exercice pratique",',
        '"Leçon 3 — Adapter le contenu au contexte Afrique du Nord | Vidéo 10 min + Exercice pratique",',
    ),
    (
        '"Lesson 3 — Adapt content to MENA context | 10 min video + Practical exercise",',
        '"Lesson 3 — Adapt content to North Africa context | 10 min video + Practical exercise",',
    ),

    # MODULE 2 — Pratique
    (
        "master Google Analytics AI, "
        "build high-performing ads with AI, and develop an advanced AI content strategy "
        "for the MENA market.",
        "master Google Analytics AI, "
        "build high-performing ads with AI, and develop an advanced AI content strategy "
        "for the North Africa market.",
    ),
    (
        "créez des publicités performantes avec l'AI et développez une stratégie de contenu "
        "AI avancée pour le marché MENA.",
        "créez des publicités performantes avec l'AI et développez une stratégie de contenu "
        "AI avancée pour le marché Afrique du Nord.",
    ),
    # section_content M2
    (
        '"Leçon 3 — Ma campagne publicitaire MENA complète | Projet pratique noté",',
        '"Leçon 3 — Ma campagne publicitaire Afrique du Nord complète | Projet pratique noté",',
    ),
    (
        '"Lesson 3 — My complete MENA ad campaign | Graded practical project",',
        '"Lesson 3 — My complete North Africa ad campaign | Graded practical project",',
    ),
    (
        '"Leçon 1 — SEO avec l\'AI pour le marché MENA | Vidéo 12 min + Exercice",',
        '"Leçon 1 — SEO avec l\'AI pour le marché Afrique du Nord | Vidéo 12 min + Exercice",',
    ),
    (
        '"Lesson 1 — SEO with AI for the MENA market | 12 min video + Exercise",',
        '"Lesson 1 — SEO with AI for the North Africa market | 12 min video + Exercise",',
    ),
    (
        '"Leçon 1 — Protection des données clients MENA | Vidéo 12 min + Quiz éthique",',
        '"Leçon 1 — Protection des données clients Afrique du Nord | Vidéo 12 min + Quiz éthique",',
    ),
    (
        '"Lesson 1 — MENA client data protection | 12 min video + Ethics quiz",',
        '"Lesson 1 — North Africa client data protection | 12 min video + Ethics quiz",',
    ),

    # MODULE 3 — Expert
    (
        "handle complex MENA cultural campaigns,",
        "handle complex North Africa cultural campaigns,",
    ),
    # section_content M3 U4
    (
        '"title": "Unité 4 — Marketing AI avancé MENA",',
        '"title": "Unité 4 — Marketing AI avancé Afrique du Nord",',
    ),
    (
        '"title": "Unit 4 — Advanced AI Marketing MENA",',
        '"title": "Unit 4 — Advanced AI Marketing North Africa",',
    ),
    (
        '"Leçon 3 — L\'avenir du marketing AI en MENA | Vidéo + Forum discussion",',
        '"Leçon 3 — L\'avenir du marketing AI en Afrique du Nord | Vidéo + Forum discussion",',
    ),
    (
        '"Lesson 3 — The future of AI marketing in MENA | Video + Discussion forum",',
        '"Lesson 3 — The future of AI marketing in North Africa | Video + Discussion forum",',
    ),
]

# ── Corrections seed_ai_marketing_units_lessons.py ────────────────────────────
CORRECTIONS_UNITS = [
    # u1_1 descriptions
    (
        'description_fr="Comprendre le marketing AI, ses outils essentiels et son contexte MENA.",',
        'description_fr="Comprendre le marketing AI, ses outils essentiels et son contexte en Afrique du Nord.",',
    ),
    (
        'description_en="Understand AI marketing, its essential tools and the MENA context.",',
        'description_en="Understand AI marketing, its essential tools and the North Africa context.",',
    ),
    # u1_2 description
    (
        'description_fr="Maîtriser ChatGPT et Canva AI pour créer du contenu marketing bilingue adapté au marché MENA.",',
        'description_fr="Maîtriser ChatGPT et Canva AI pour créer du contenu marketing bilingue adapté au marché Afrique du Nord.",',
    ),
    # u3_4 titre et description
    (
        "title_fr=\"Marketing AI avancé MENA\",",
        "title_fr=\"Marketing AI avancé Afrique du Nord\",",
    ),
    (
        "title_en=\"Advanced AI Marketing MENA\",",
        "title_en=\"Advanced AI Marketing North Africa\",",
    ),
]

# ── Code à ajouter à la fin de seed_ai_marketing_units_lessons.py ─────────────
CERTIFICATION_UNIT_CODE = '''
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
'''

# ── Ancre de recherche pour insérer le code de certification ──────────────────
# On insère AVANT le db.commit() final du fichier units
ANCHOR_BEFORE_COMMIT = '''    db.commit()
    print("✅ AI Marketing Strategist — units, lessons, activities insérées")'''

REPLACEMENT_WITH_CERT = CERTIFICATION_UNIT_CODE + "\n" + ANCHOR_BEFORE_COMMIT


# ── Fonction de patch ─────────────────────────────────────────────────────────

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

    if "Certification Finale — AI Marketing Strategist" in content:
        print(f"✅ {label} — Unité 6 Certification déjà présente, skip.")
        return True

    if ANCHOR_BEFORE_COMMIT not in content:
        print(f"⚠️  {label} — Ancre db.commit() non trouvée. Ajout manuel nécessaire.")
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
    print("PATCH — AI Marketing Strategist")
    print("MENA → Afrique du Nord + Ajout Certification Finale")
    print("=" * 65)

    print(f"\n📄 Fichier 1 : seed_ai_marketing_strategist_modules.py")
    apply_corrections(FILES["modules"], CORRECTIONS_MODULES,
                      "seed_ai_marketing_strategist_modules.py")

    print(f"\n📄 Fichier 2 : seed_ai_marketing_units_lessons.py")
    apply_corrections(FILES["units"], CORRECTIONS_UNITS,
                      "seed_ai_marketing_units_lessons.py (MENA)")
    add_certification_unit(FILES["units"],
                           "seed_ai_marketing_units_lessons.py (Certification)")

    print("\n" + "=" * 65)
    print("✅ Patch terminé.")
    print("   Backups .bak disponibles si annulation nécessaire.")
    print("   Supprimez les modules AI Marketing en BDD, puis relancez")
    print("   python -m app.scripts.seed_all")
    print("=" * 65)


if __name__ == "__main__":
    main()