"""
patch_mena_ai_sales.py
======================
Corrige les mentions "MENA" de positionnement plateforme dans les 2 fichiers
seed AI Sales Specialist.

Règle appliquée :
  ✅ Remplacé  → champs visibles par l'apprenant comme positionnement plateforme
                 (description, expected_outcome, why_this_module, action_point,
                  recommended_when, next_recommended_module, takeaway)
  ✅ Conservé  → contenu pédagogique enseigné
                 (titres leçons, quiz, cas pratiques, prompts, tableaux comparatifs,
                  stratégies B2B MENA = contenu du cours)

Utilisation :
  Placez ce fichier à la racine du projet, puis exécutez :
  python patch_mena_ai_sales.py

  Les fichiers sont modifiés en place. Un backup .bak est créé automatiquement.
"""

import os
import re
import shutil

# ── Chemins vers les fichiers à corriger ──────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FILES = {
    "modules": os.path.join(BASE_DIR, "app", "scripts", "seed_ai_sales_specialist_modules.py"),
    "units":   os.path.join(BASE_DIR, "app", "scripts", "seed_ai_sales_units_lessons.py"),
}

# ── Corrections ciblées par fichier ──────────────────────────────────────────
# Format : (texte_exact_à_remplacer, texte_de_remplacement)
# Les chaînes doivent correspondre EXACTEMENT au fichier source.

CORRECTIONS_MODULES = [

    # ── MODULE 1 — Fondations ─────────────────────────────────────────────────

    # description_en
    (
        "understand the fundamentals and the context of the MENA market.",
        "understand the fundamentals and the context of the North Africa market.",
    ),
    # description_fr
    (
        "les principes éthiques dans le contexte du marché MENA.",
        "les principes éthiques dans le contexte du marché Afrique du Nord.",
    ),
    # expected_outcome_fr
    (
        "a configuré HubSpot AI avec son pipeline MENA,",
        "a configuré HubSpot AI avec son pipeline Afrique du Nord,",
    ),
    # expected_outcome_en
    (
        "has configured HubSpot AI with their MENA pipeline,",
        "has configured HubSpot AI with their North Africa pipeline,",
    ),
    # action_point_fr — module 1
    (
        "2. Configurer votre pipeline en 6 étapes adaptées au marché MENA\n",
        "2. Configurer votre pipeline en 6 étapes adaptées au marché Afrique du Nord\n",
    ),
    # action_point_en — module 1
    (
        "2. Configure your pipeline with 6 MENA-adapted stages\n",
        "2. Configure your pipeline with 6 North Africa-adapted stages\n",
    ),
    # why_this_module_fr — module 1
    (
        "why_this_module_fr=\"Before using sales AI tools, you need to understand the fundamentals and the MENA context.\",",
        "why_this_module_fr=\"Before using sales AI tools, you need to understand the fundamentals and the North Africa context.\",",
    ),
    (
        "why_this_module_fr=\"Avant d'utiliser les outils AI de vente, vous avez besoin de comprendre les fondamentaux et le contexte MENA.\",",
        "why_this_module_fr=\"Avant d'utiliser les outils AI de vente, vous avez besoin de comprendre les fondamentaux et le contexte Afrique du Nord.\",",
    ),
    # why_this_module_en — module 1
    (
        "why_this_module_en=\"Before using sales AI tools, you need to understand the fundamentals and the MENA context.\",",
        "why_this_module_en=\"Before using sales AI tools, you need to understand the fundamentals and the North Africa context.\",",
    ),

    # ── MODULE 2 — Pratique ───────────────────────────────────────────────────

    # description_fr
    (
        "personnalisez à grande échelle pour le marché MENA.",
        "personnalisez à grande échelle pour le marché Afrique du Nord.",
    ),
    # description_en
    (
        "personalise at scale for the MENA market.",
        "personalise at scale for the North Africa market.",
    ),
    # expected_outcome_fr
    (
        "personnalise ses messages pour plusieurs "
        "marchés MENA simultanément,",
        "personnalise ses messages pour plusieurs "
        "marchés d'Afrique du Nord simultanément,",
    ),
    # expected_outcome_en
    (
        "personalises messages for multiple "
        "MENA markets simultaneously,",
        "personalises messages for multiple "
        "North Africa markets simultaneously,",
    ),

    # ── MODULE 3 — Expert ─────────────────────────────────────────────────────

    # description_fr
    (
        "Mène à la certification officielle Euklydia.",
        "Mène à la certification officielle Euklydia.",   # inchangé — pas de MENA ici
    ),
    # why_this_module_fr
    (
        "fait de vous un leader AI reconnu en MENA.",
        "fait de vous un leader AI reconnu en Afrique du Nord.",
    ),
    # why_this_module_en
    (
        "makes you a recognised AI leader in MENA.",
        "makes you a recognised AI leader in North Africa.",
    ),
    # expected_outcome_fr — module 3
    (
        "gère des cas B2B complexes en Tunisie et en MENA,",
        "gère des cas B2B complexes en Tunisie et en Afrique du Nord,",
    ),
    # expected_outcome_en — module 3
    (
        "handles complex B2B cases in Tunisia and MENA,",
        "handles complex B2B cases in Tunisia and North Africa,",
    ),
]

# ── Pour seed_ai_sales_units_lessons.py ──────────────────────────────────────
# Analyse : les mentions MENA sont quasi-exclusivement pédagogiques
# (titres leçons, quiz, cas pratiques, prompts, exercices).
# Seules quelques descriptions d'unités sont du positionnement plateforme.

CORRECTIONS_UNITS = [

    # u1_1 — description de l'unité (vue apprenant — positionnement)
    (
        "description_fr=\"Comprendre ce qu'est l'AI, ses outils et son contexte MENA.\",",
        "description_fr=\"Comprendre ce qu'est l'AI, ses outils et son contexte en Afrique du Nord.\",",
    ),
    (
        "description_en=\"Understand what AI is, its tools and the MENA context.\",",
        "description_en=\"Understand what AI is, its tools and the North Africa context.\",",
    ),

    # u2_3 — description de l'unité
    (
        "description_fr=\"Personnalisation de masse avec l'AI, adaptation au contexte MENA, campagnes multi-segments.\",",
        "description_fr=\"Personnalisation de masse avec l'AI, adaptation au contexte Afrique du Nord, campagnes multi-segments.\",",
    ),
    (
        "description_en=\"Mass personalisation with AI, MENA context adaptation, multi-segment campaigns.\",",
        "description_en=\"Mass personalisation with AI, North Africa context adaptation, multi-segment campaigns.\",",
    ),
]


# ── Fonction de patch ─────────────────────────────────────────────────────────

def apply_corrections(filepath: str, corrections: list, label: str):
    if not os.path.exists(filepath):
        print(f"❌ Fichier introuvable : {filepath}")
        return False

    # Créer un backup
    backup = filepath + ".bak"
    shutil.copy2(filepath, backup)
    print(f"💾 Backup créé : {backup}")

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    applied = 0
    skipped = 0

    for old, new in corrections:
        if old == new:
            # Correction identique = pas de changement à faire (ligne commentaire)
            continue
        if old in content:
            content = content.replace(old, new, 1)
            applied += 1
            print(f"  ✅ Remplacé : '{old[:60]}...'")
        else:
            skipped += 1
            print(f"  ⚠️  Non trouvé (déjà corrigé ?) : '{old[:60]}...'")

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"\n✅ {label} — {applied} corrections appliquées, {skipped} ignorées.")
    else:
        print(f"\n✅ {label} — Aucune modification nécessaire (déjà à jour).")

    return True


# ── Exécution ─────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("PATCH — MENA → Afrique du Nord (positionnement plateforme)")
    print("Fichiers AI Sales Specialist")
    print("=" * 60)

    print(f"\n📄 Fichier 1 : seed_ai_sales_specialist_modules.py")
    apply_corrections(
        FILES["modules"],
        CORRECTIONS_MODULES,
        "seed_ai_sales_specialist_modules.py"
    )

    print(f"\n📄 Fichier 2 : seed_ai_sales_units_lessons.py")
    apply_corrections(
        FILES["units"],
        CORRECTIONS_UNITS,
        "seed_ai_sales_units_lessons.py"
    )

    print("\n" + "=" * 60)
    print("✅ Patch terminé.")
    print("   Les backups .bak sont disponibles si vous voulez annuler.")
    print("   Relancez seed_all.py pour intégrer les corrections en BDD.")
    print("=" * 60)


if __name__ == "__main__":
    main()