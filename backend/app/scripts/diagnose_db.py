"""
Diagnostic détaillé de l'état de la DB Euklydia.
À lancer depuis backend/ avec : python app/scripts/diagnose_db.py
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy import func
from app.db.session import SessionLocal
from app.models.skill import Skill
from app.models.module import Module
from app.models.unit import Unit
from app.models.lesson import Lesson
from app.models.module_skill import ModuleSkill

db = SessionLocal()
try:
    print("\n🔍 Diagnostic détaillé — Euklydia Academy")
    print("=" * 70)

    # ─────────────────────────────────────────────────────────────────────
    # 1. Détail par module : units count + lessons count + skill linked ?
    # ─────────────────────────────────────────────────────────────────────
    print("\n📋 Détail par module (units / lessons / skill liée) :")
    print("-" * 70)

    modules = db.query(Module).order_by(Module.role, Module.display_order).all()
    for m in modules:
        units_count = db.query(Unit).filter(Unit.module_id == m.id).count()
        lessons_count = (
            db.query(Lesson)
            .join(Unit, Lesson.unit_id == Unit.id)
            .filter(Unit.module_id == m.id)
            .count()
        )
        ms_link = db.query(ModuleSkill).filter(ModuleSkill.module_id == m.id).first()
        skill_name = "❌ AUCUNE" if not ms_link else (
            db.query(Skill).filter(Skill.id == ms_link.skill_id).first().name
        )

        flag = "✅" if (units_count == 5 and ms_link) else "⚠️ "
        print(f"\n{flag} [{m.role}] Module #{m.display_order} (id={m.id}) : {m.title_fr}")
        print(f"     Units  : {units_count} (attendu 5)")
        print(f"     Lessons: {lessons_count}")
        print(f"     Skill  : {skill_name}")

    # ─────────────────────────────────────────────────────────────────────
    # 2. Modules sans jointure module_skills
    # ─────────────────────────────────────────────────────────────────────
    print("\n\n⚠️  Modules SANS skill liée (anomalie module_skills) :")
    print("-" * 70)
    modules_with_link = db.query(ModuleSkill.module_id).distinct().all()
    linked_ids = {m[0] for m in modules_with_link}
    orphan_modules = [m for m in modules if m.id not in linked_ids]
    if not orphan_modules:
        print("   Aucun module orphelin ✅")
    else:
        for m in orphan_modules:
            print(f"   ❌ [{m.role}] {m.title_fr} (module_id={m.id})")

    # ─────────────────────────────────────────────────────────────────────
    # 3. Units orphelines (sans module parent valide) ou en doublon
    # ─────────────────────────────────────────────────────────────────────
    print("\n\n🔎 Recherche d'units en doublon ou orphelines :")
    print("-" * 70)

    # Units par module avec leur ordre — détecter doublons d'ordre
    print("\n   Units groupées par module et order :")
    duplicate_query = (
        db.query(Unit.module_id, Unit.order, func.count(Unit.id).label("nb"))
        .group_by(Unit.module_id, Unit.order)
        .having(func.count(Unit.id) > 1)
        .all()
    )
    if not duplicate_query:
        print("   Aucun doublon d'order détecté ✅")
    else:
        for module_id, order, nb in duplicate_query:
            module = db.query(Module).filter(Module.id == module_id).first()
            module_title = module.title_fr if module else f"module_id={module_id} (introuvable)"
            print(f"   ⚠️  [{module_title}] order={order} apparaît {nb} fois")

    # Units sans module parent
    orphan_units = (
        db.query(Unit)
        .outerjoin(Module, Unit.module_id == Module.id)
        .filter(Module.id.is_(None))
        .all()
    )
    if orphan_units:
        print(f"\n   ⚠️  {len(orphan_units)} units sans module parent !")
        for u in orphan_units:
            print(f"      - unit_id={u.id} '{u.title_fr}' (module_id={u.module_id} manquant)")

    # ─────────────────────────────────────────────────────────────────────
    # 4. Skills par career_path avec leurs noms
    # ─────────────────────────────────────────────────────────────────────
    print("\n\n🎯 Skills par career_path (avec noms) :")
    print("-" * 70)
    for cp_id in [79, 80, 81, 82]:
        skills = db.query(Skill).filter(Skill.career_path_id == cp_id).all()
        print(f"\n   career_path_id={cp_id} :")
        for s in skills:
            print(f"      - skill_id={s.id} : {s.name}")

    print("\n" + "=" * 70)

finally:
    db.close()