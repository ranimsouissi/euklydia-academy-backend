"""
patch_mena_ai_designer.py
=========================
Corrige les mentions "MENA" de positionnement plateforme dans les 2 fichiers
seed AI Designer + ajoute l'Unité 6 Certification au Module Expert.

Utilisation :
  python patch_mena_ai_designer.py
  Les backups .bak sont créés automatiquement.
"""

import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FILES = {
    "modules": os.path.join(BASE_DIR, "app", "scripts", "seed_ai_designer_modules.py"),
    "units":   os.path.join(BASE_DIR, "app", "scripts", "seed_ai_designer_units_lessons.py"),
}

# ── Corrections seed_ai_designer_modules.py ───────────────────────────────────
CORRECTIONS_MODULES = [
    # MODULE 2 — Pratique description_fr
    (
        "et création d'identités visuelles pour le marché MENA.",
        "et création d'identités visuelles pour le marché Afrique du Nord.",
    ),
    # MODULE 2 — Pratique description_en
    (
        "and visual identity creation skills for the MENA market.",
        "and visual identity creation skills for the North Africa market.",
    ),
    # MODULE 3 — Expert description_fr
    (
        "et gérez les enjeux éthiques avancés du design AI en MENA.",
        "et gérez les enjeux éthiques avancés du design AI en Afrique du Nord.",
    ),
    # MODULE 3 — Expert description_en
    (
        "and manage advanced ethical issues of AI design in MENA.",
        "and manage advanced ethical issues of AI design in North Africa.",
    ),
]

# ── Corrections seed_ai_designer_units_lessons.py ─────────────────────────────
CORRECTIONS_UNITS = [
    # u1_1 description_fr
    (
        'description_fr="Comprendre le design AI, ses outils essentiels et ses spécificités pour le marché MENA.",',
        'description_fr="Comprendre le design AI, ses outils essentiels et ses spécificités pour le marché Afrique du Nord.",',
    ),
    # u1_2 description_fr
    (
        'description_fr="Maîtriser Midjourney et Canva AI pour créer des images adaptées au marché MENA.",',
        'description_fr="Maîtriser Midjourney et Canva AI pour créer des images adaptées au marché Afrique du Nord.",',
    ),
    # u3_3 title_fr
    (
        'title_fr="Design AI avancé MENA",',
        'title_fr="Design AI avancé Afrique du Nord",',
    ),
    # u3_3 title_en
    (
        'title_en="Advanced AI Design MENA",',
        'title_en="Advanced AI Design North Africa",',
    ),
]

# ── Code Unité 6 Certification ─────────────────────────────────────────────────
CERTIFICATION_UNIT_CODE = '''
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
'''

ANCHOR_BEFORE_COMMIT = '''    db.commit()
    print("✅ AI Designer — units, lessons, activities insérées")'''

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

    if "Certification Finale — AI Designer" in content:
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
    print("PATCH — AI Designer")
    print("MENA → Afrique du Nord + Ajout Certification Finale")
    print("=" * 65)

    print(f"\n📄 Fichier 1 : seed_ai_designer_modules.py")
    apply_corrections(FILES["modules"], CORRECTIONS_MODULES,
                      "seed_ai_designer_modules.py")

    print(f"\n📄 Fichier 2 : seed_ai_designer_units_lessons.py")
    apply_corrections(FILES["units"], CORRECTIONS_UNITS,
                      "seed_ai_designer_units_lessons.py (MENA)")
    add_certification_unit(FILES["units"],
                           "seed_ai_designer_units_lessons.py (Certification)")

    print("\n" + "=" * 65)
    print("✅ Patch terminé.")
    print("   AI Designer — modules déjà en BDD (skip anti-doublon actif).")
    print("   Supprimez uniquement les units/lessons/activities AI Designer,")
    print("   puis relancez : python -m app.scripts.seed_all")
    print("=" * 65)


if __name__ == "__main__":
    main()