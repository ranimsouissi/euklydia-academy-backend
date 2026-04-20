import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import app.models.unit
import app.models.lesson
import app.models.activity
import app.models.learner_activity_log
import app.models.learner_skill_mastery
import app.models.learner_path_log

from app.db.session import SessionLocal
from app.scripts.seed_ai_sales_units_lessons import seed_ai_sales_units_lessons

db = SessionLocal()
try:
    seed_ai_sales_units_lessons(db)
    print("Done")
except Exception as e:
    db.rollback()
    print(f"Erreur : {e}")
    raise
finally:
    db.close()
