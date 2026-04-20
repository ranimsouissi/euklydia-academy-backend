from sqlalchemy import create_engine, text
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)

with engine.connect() as conn:
    print("DATABASE_URL:", settings.DATABASE_URL)
    print("DB:", conn.execute(text("SELECT current_database()")).scalar())
    print("USER:", conn.execute(text("SELECT current_user")).scalar())
    print("search_path:", conn.execute(text("SHOW search_path")).scalar())
    print("current_schema:", conn.execute(text("SELECT current_schema()")).scalar())

    rows = conn.execute(text("""
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_name = 'diagnostic_sessions'
        ORDER BY table_schema;
    """)).all()
    print("diagnostic_sessions tables:", rows)