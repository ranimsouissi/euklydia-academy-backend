"""
Correction rapide - ajoute title_en et description_en manquants
dans les fichiers seed qui ont des Lesson() sans champ _en.

Usage:
  python fix_null_title_en_v2.py backend\app\scripts\seed_ai_marketing_units_lessons.py
"""

import sys
import re
import shutil


def fix(filepath):
    shutil.copy2(filepath, filepath + ".bak_en")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    count_title = 0
    count_desc = 0

    # Correction 1 : title_fr="X",\n        format= -> ajouter title_en
    def insert_title_en(m):
        nonlocal count_title
        title_fr = m.group(1)
        count_title += 1
        return 'title_fr="' + title_fr + '",\n        title_en="' + title_fr + '",\n        format='

    new_content = re.sub(r'title_fr="([^"]+)",\n        format=', insert_title_en, content)

    # Correction 2 : description_fr="X",\n        format= -> ajouter description_en
    def insert_desc_en(m):
        nonlocal count_desc
        desc_fr = m.group(1)
        count_desc += 1
        return 'description_fr="' + desc_fr + '",\n        description_en="' + desc_fr + '",\n        format='

    new_content = re.sub(r'description_fr="([^"]+)",\n        format=', insert_desc_en, new_content)

    # Correction 3 : description_fr="X",\n        prerequisite -> ajouter description_en
    def insert_desc_en2(m):
        nonlocal count_desc
        desc_fr = m.group(1)
        count_desc += 1
        return 'description_fr="' + desc_fr + '",\n        description_en="' + desc_fr + '",\n        prerequisite_lesson_id='

    new_content = re.sub(r'description_fr="([^"]+)",\n        prerequisite_lesson_id=', insert_desc_en2, new_content)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    changed = new_content != original
    print("=" * 50)
    print("Fichier : " + filepath)
    if changed:
        print("OK - Corrections appliquees")
    else:
        print("Aucun changement necessaire")
    print("   title_en ajoutes       : " + str(count_title))
    print("   description_en ajoutes : " + str(count_desc))
    print("   Backup                 : " + filepath + ".bak_en")
    print("=" * 50)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fix_null_title_en_v2.py <fichier1> [fichier2] ...")
        sys.exit(1)

    for filepath in sys.argv[1:]:
        fix(filepath)

    print("Termine ! Relancez : python app\\scripts\\seed_all.py")
