from sqlalchemy import create_engine, text

LOCAL_URL = "postgresql+psycopg2://postgres:postgres20@localhost:5432/euklydia_prod"
import os
from dotenv import load_dotenv
load_dotenv()
SUPA_URL = os.getenv("DATABASE_URL")

def cols(url, label):
    e = create_engine(url)
    with e.connect() as c:
        rows = c.execute(text("""
            select column_name, data_type, is_nullable, column_default
            from information_schema.columns
            where table_name = 'coaching_sessions'
            order by ordinal_position
        """)).fetchall()
    print(f"\n=== coaching_sessions ({label}) — {len(rows)} colonnes ===")
    return {r[0]: r for r in rows}

local = cols(LOCAL_URL, "LOCAL")
for name, r in local.items():
    print(f"  {name:20s} {r[1]:25s} null={r[2]} default={r[3]}")

supa = cols(SUPA_URL, "SUPABASE")
for name, r in supa.items():
    print(f"  {name:20s} {r[1]:25s} null={r[2]} default={r[3]}")

print("\n=== Colonnes présentes en LOCAL mais ABSENTES sur SUPABASE ===")
for name in local:
    if name not in supa:
        print("  MANQUANTE :", name, "->", local[name][1], "null=", local[name][2], "default=", local[name][3])
