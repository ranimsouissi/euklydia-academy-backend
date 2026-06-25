import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.db.session import SessionLocal
from app.models.skill import Skill
from app.models.question import Question
from app.models.module import Module
from app.models.unit import Unit
from app.models.lesson import Lesson
from app.models.module_skill import ModuleSkill

db = SessionLocal()
try:
    print("\n📊 État de la DB Euklydia Academy")
    print("=" * 50)
    
    # Skills par career path
    print("\n🎯 Skills par career_path :")
    for cp_id in [79, 80, 81, 82]:
        count = db.query(Skill).filter(Skill.career_path_id == cp_id).count()
        print(f"   career_path_id={cp_id} : {count} skills")
    
    # Questions totales
    nb_questions = db.query(Question).count()
    print(f"\n❓ Questions totales : {nb_questions}")
    
    # Modules par role
    print("\n📚 Modules par role :")
    for role in ["AI Sales Specialist", "AI Marketing Strategist", 
                 "AI Designer", "AI Project Manager"]:
        count = db.query(Module).filter(Module.role == role).count()
        print(f"   {role} : {count} modules")
    
    # Totaux units / lessons / links
    print(f"\n📐 Units totales   : {db.query(Unit).count()}")
    print(f"📐 Lessons totales : {db.query(Lesson).count()}")
    print(f"📐 Module_skills   : {db.query(ModuleSkill).count()}")
    
    print("\n" + "=" * 50)
finally:
    db.close()