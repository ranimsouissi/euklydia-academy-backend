from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
e = create_engine(os.getenv("DATABASE_URL"))
with e.connect() as c:
    r = c.execute(text("select extname, extversion from pg_extension where extname = 'vector'")).fetchone()
    print("vector active :", r)
