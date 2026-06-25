from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
LOCAL_URL = "postgresql+psycopg2://postgres:postgres20@localhost:5432/euklydia_prod"
SUPA_URL = os.getenv("DATABASE_URL")

missing_tables = ["events", "performance_insights", "cohort_insights", "interventions"]

le = create_engine(LOCAL_URL)

def col_ddl(col, dt, udt, nul, dflt, maxlen):
    # type
    if dt == "character varying":
        t = f"varchar({maxlen})" if maxlen else "varchar"
    elif dt == "USER-DEFINED" and udt == "vector":
        t = "extensions.vector(1536)"
    elif dt == "ARRAY":
        t = udt.lstrip("_") + "[]"
    else:
        t = dt
    line = f"    {col} {t}"
    if dflt is not None:
        # nextval => SERIAL handled separately; keep simple defaults
        if "nextval" not in str(dflt):
            line += f" DEFAULT {dflt}"
    if nul == "NO":
        line += " NOT NULL"
    return line

print("-- DDL généré depuis LOCAL --\n")
ddls = []
with le.connect() as c:
    for t in missing_tables:
        cols = c.execute(text("""
            select column_name, data_type, udt_name, is_nullable, column_default, character_maximum_length
            from information_schema.columns
            where table_name = :t order by ordinal_position
        """), {"t": t}).fetchall()
        if not cols:
            print(f"-- ⚠️ {t} introuvable en local, skip")
            continue
        # detect serial PK
        lines = []
        for col, dt, udt, nul, dflt, maxlen in cols:
            if dflt and "nextval" in str(dflt):
                lines.append(f"    {col} SERIAL PRIMARY KEY")
            else:
                lines.append(col_ddl(col, dt, udt, nul, dflt, maxlen))
        ddl = f"CREATE TABLE IF NOT EXISTS public.{t} (\n" + ",\n".join(lines) + "\n);"
        ddls.append(ddl)
        print(ddl, "\n")

print("\n=== Application sur SUPABASE ===")
se = create_engine(SUPA_URL)
with se.begin() as c:
    for ddl in ddls:
        c.execute(text(ddl))
    c.execute(text("ALTER TABLE pain_points ADD COLUMN IF NOT EXISTS severity smallint"))
    c.execute(text("ALTER TABLE pain_points ADD COLUMN IF NOT EXISTS source text DEFAULT 'coaching_agent'"))
print("✅ Tables manquantes créées + colonnes pain_points ajoutées")
