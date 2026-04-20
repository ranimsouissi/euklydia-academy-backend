"""
Script d'application du patch — seed_ai_sales_units_lessons.py
Applique les 12 corrections (ajout des unités manquantes) automatiquement.

Usage :
  python apply_patch_sales.py <chemin_vers_le_fichier>

Exemple :
  python apply_patch_sales.py backend/app/scripts/seed_ai_sales_units_lessons.py
"""

import sys
import os
import shutil

CORRECTIONS = [
    # ── CORRECTION 1 — u1_4 ──────────────────────────────────────────────────
    (
        """    # ════════════════════════════════════════════════════════════════════════
    # UNITÉ 4 — MON PREMIER EMAIL AI
    # ════════════════════════════════════════════════════════════════════════

    # ── Leçon 4.1 — Rédiger avec ChatGPT ────────────────────────────────────
    l1_4_1 = Lesson(""",
        """    # ════════════════════════════════════════════════════════════════════════
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
    db.add(u1_4); db.flush()

    # ── Leçon 4.1 — Rédiger avec ChatGPT ────────────────────────────────────
    l1_4_1 = Lesson(""",
    ),

    # ── CORRECTION 2 — u1_5 ──────────────────────────────────────────────────
    (
        """    # ════════════════════════════════════════════════════════════════════════
    # UNITÉ 5 — ÉTHIQUE AI BASIQUE
    # ════════════════════════════════════════════════════════════════════════

    # ── Leçon 5.1 — Les règles fondamentales ────────────────────────────────
    l1_5_1 = Lesson(""",
        """    # ════════════════════════════════════════════════════════════════════════
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

    # ── Leçon 5.1 — Les règles fondamentales ────────────────────────────────
    l1_5_1 = Lesson(""",
    ),

    # ── CORRECTION 3 — u2_1 ──────────────────────────────────────────────────
    (
        """    # ════════════════════════════════════════════════════════════════════════
    # UNITÉ 1 — AUTOMATISER SA PROSPECTION
    # ════════════════════════════════════════════════════════════════════════

    # ── Leçon 1.1 — Les séquences d'emails automatiques ─────────────────────
    l2_1_1 = Lesson(""",
        """    # ════════════════════════════════════════════════════════════════════════
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

    # ── Leçon 1.1 — Les séquences d'emails automatiques ─────────────────────
    l2_1_1 = Lesson(""",
    ),

    # ── CORRECTION 4 — u2_2 ──────────────────────────────────────────────────
    (
        """    # ════════════════════════════════════════════════════════════════════════
    # UNITÉ 2 — ANALYSER LES DONNÉES CLIENTS
    # ════════════════════════════════════════════════════════════════════════

    # ── Leçon 2.1 — Lire et interpréter les insights AI ─────────────────────
    l2_2_1 = Lesson(""",
        """    # ════════════════════════════════════════════════════════════════════════
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

    # ── Leçon 2.1 — Lire et interpréter les insights AI ─────────────────────
    l2_2_1 = Lesson(""",
    ),

    # ── CORRECTION 5 — u2_3 ──────────────────────────────────────────────────
    (
        """    # ════════════════════════════════════════════════════════════════════════
    # UNITÉ 3 — PERSONNALISER À GRANDE ÉCHELLE
    # ════════════════════════════════════════════════════════════════════════

    # ── Leçon 3.1 — La personnalisation de masse ─────────────────────────────
    l2_3_1 = Lesson(""",
        """    # ════════════════════════════════════════════════════════════════════════
    # UNITÉ 3 — PERSONNALISER À GRANDE ÉCHELLE
    # ════════════════════════════════════════════════════════════════════════

    u2_3 = Unit(
        module_id=m2.id, order=3,
        title_fr="Personnaliser à grande échelle",
        title_en="Personalising at Scale",
        description_fr="Personnalisation de masse avec l'AI, adaptation au contexte MENA, campagnes multi-segments.",
        description_en="Mass personalisation with AI, MENA context adaptation, multi-segment campaigns.",
        estimated_duration_min=112,
    )
    db.add(u2_3); db.flush()

    # ── Leçon 3.1 — La personnalisation de masse ─────────────────────────────
    l2_3_1 = Lesson(""",
    ),

    # ── CORRECTION 6 — u2_4 ──────────────────────────────────────────────────
    (
        """    # ════════════════════════════════════════════════════════════════════════
    # UNITÉ 4 — OUTILS AI AVANCÉS
    # ════════════════════════════════════════════════════════════════════════

    # ── Leçon 4.1 — HubSpot AI en profondeur ────────────────────────────────
    l2_4_1 = Lesson(""",
        """    # ════════════════════════════════════════════════════════════════════════
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

    # ── Leçon 4.1 — HubSpot AI en profondeur ────────────────────────────────
    l2_4_1 = Lesson(""",
    ),

    # ── CORRECTION 7 — u2_5 ──────────────────────────────────────────────────
    (
        """    # ════════════════════════════════════════════════════════════════════════
    # UNITÉ 5 — ÉTHIQUE AI INTERMÉDIAIRE
    # ════════════════════════════════════════════════════════════════════════

    # ── Leçon 5.1 — Gérer les données clients responsablement ───────────────
    l2_5_1 = Lesson(""",
        """    # ════════════════════════════════════════════════════════════════════════
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

    # ── Leçon 5.1 — Gérer les données clients responsablement ───────────────
    l2_5_1 = Lesson(""",
    ),

    # ── CORRECTION 8 — u3_1 ──────────────────────────────────────────────────
    (
        """    # ════════════════════════════════════════════════════════════════════════
    # UNITÉ 1 — STRATÉGIE AI SALES GLOBALE
    # ════════════════════════════════════════════════════════════════════════

    # ── Leçon 1.1 — Construire sa stratégie AI Sales ─────────────────────────
    l3_1_1 = Lesson(""",
        """    # ════════════════════════════════════════════════════════════════════════
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

    # ── Leçon 1.1 — Construire sa stratégie AI Sales ─────────────────────────
    l3_1_1 = Lesson(""",
    ),

    # ── CORRECTION 9 — u3_2 ──────────────────────────────────────────────────
    (
        """    # ════════════════════════════════════════════════════════════════════════
    # UNITÉ 2 — PILOTER UNE ÉQUIPE AI SALES
    # ════════════════════════════════════════════════════════════════════════

    # ── Leçon 2.1 — Former ses collègues à l'AI ─────────────────────────────
    l3_2_1 = Lesson(""",
        """    # ════════════════════════════════════════════════════════════════════════
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

    # ── Leçon 2.1 — Former ses collègues à l'AI ─────────────────────────────
    l3_2_1 = Lesson(""",
    ),

    # ── CORRECTION 10 — u3_3 ─────────────────────────────────────────────────
    (
        """    # ════════════════════════════════════════════════════════════════════════
    # UNITÉ 3 — MESURER LE ROI DE L'AI
    # ════════════════════════════════════════════════════════════════════════

    # ── Leçon 3.1 — Calculer le retour sur investissement AI ────────────────
    l3_3_1 = Lesson(""",
        """    # ════════════════════════════════════════════════════════════════════════
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

    # ── Leçon 3.1 — Calculer le retour sur investissement AI ────────────────
    l3_3_1 = Lesson(""",
    ),

    # ── CORRECTION 11 — u3_4 ─────────────────────────────────────────────────
    (
        """    # ════════════════════════════════════════════════════════════════════════
    # UNITÉ 4 — AI SALES AVANCÉ MENA
    # ════════════════════════════════════════════════════════════════════════

    # ── Leçon 4.1 — Cas complexes B2B tunisiens ─────────────────────────────
    l3_4_1 = Lesson(""",
        """    # ════════════════════════════════════════════════════════════════════════
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

    # ── Leçon 4.1 — Cas complexes B2B tunisiens ─────────────────────────────
    l3_4_1 = Lesson(""",
    ),

    # ── CORRECTION 12 — u3_5 ─────────────────────────────────────────────────
    (
        """    # ════════════════════════════════════════════════════════════════════════
    # UNITÉ 5 — GOUVERNANCE ET ÉTHIQUE AI AVANCÉE
    # ════════════════════════════════════════════════════════════════════════

    # ── Leçon 5.1 — Créer sa politique AI Sales ──────────────────────────────
    l3_5_1 = Lesson(""",
        """    # ════════════════════════════════════════════════════════════════════════
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

    # ── Leçon 5.1 — Créer sa politique AI Sales ──────────────────────────────
    l3_5_1 = Lesson(""",
    ),
]


def apply_patch(filepath):
    if not os.path.exists(filepath):
        print(f"❌ Fichier introuvable : {filepath}")
        sys.exit(1)

    # Backup
    backup = filepath + ".backup"
    shutil.copy2(filepath, backup)
    print(f"✅ Backup créé : {backup}")

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    applied = 0
    already_ok = 0
    not_found = 0

    for i, (old, new) in enumerate(CORRECTIONS, 1):
        unit_name = f"u{'1' if i <= 2 else '2' if i <= 7 else '3'}_{i if i <= 2 else i - 2 if i <= 7 else i - 7}"

        if old in content:
            content = content.replace(old, new, 1)
            print(f"  ✅ Correction {i:2d} appliquée")
            applied += 1
        elif new in content:
            print(f"  ⏭️  Correction {i:2d} déjà appliquée (skip)")
            already_ok += 1
        else:
            print(f"  ⚠️  Correction {i:2d} — texte non trouvé (vérifier manuellement)")
            not_found += 1

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\n{'='*50}")
    print(f"✅ Patch terminé")
    print(f"   {applied} correction(s) appliquée(s)")
    print(f"   {already_ok} déjà en place")
    print(f"   {not_found} non trouvée(s)")

    if not_found > 0:
        print(f"\n⚠️  {not_found} correction(s) non appliquée(s).")
        print(f"   Restaurez le backup si nécessaire : {backup}")
    else:
        print(f"\n🎉 Toutes les unités sont maintenant en place !")
        print(f"   Relancez : python app/scripts/seed_all.py")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python apply_patch_sales.py <chemin_vers_seed_ai_sales_units_lessons.py>")
        print("Ex:    python apply_patch_sales.py backend/app/scripts/seed_ai_sales_units_lessons.py")
        sys.exit(1)

    apply_patch(sys.argv[1])
