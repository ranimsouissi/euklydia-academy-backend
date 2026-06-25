from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
e = create_engine(os.getenv("DATABASE_URL"))
with e.connect() as c:
    rows = c.execute(text(
        "select table_name from information_schema.tables "
        "where table_schema = 'public' order by table_name"
    )).fetchall()
    print("Nombre de tables :", len(rows))
    for r in rows:
        print(" -", r[0])
