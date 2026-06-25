"""
rechunk_modules.py — V3 (psycopg2 direct)
==========================================
Rechunking sémantique des modules — 7 chunks par module.
Utilise psycopg2 directement pour éviter les conflits SQLAlchemy/pgvector.
"""

import os
import sys
import json
import time
import re
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL   = os.getenv("DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not DATABASE_URL:
    print("❌ DATABASE_URL manquante dans .env")
    sys.exit(1)
if not OPENAI_API_KEY:
    print("❌ OPENAI_API_KEY manquante dans .env")
    sys.exit(1)

try:
    import psycopg2
    import psycopg2.extras
    import openai
except ImportError as e:
    print(f"❌ Dépendance manquante : {e}")
    sys.exit(1)

# Convertir DATABASE_URL SQLAlchemy → psycopg2
# postgresql+psycopg2://user:pass@host/db  →  host=... dbname=...
def parse_db_url(url):
    url = url.replace("postgresql+psycopg2://", "postgresql://")
    url = url.replace("postgresql://", "")
    pattern = r"(?:([^:]+):([^@]*)@)?([^/:]+)(?::(\d+))?/(.+)"
    m = re.match(pattern, url)
    if not m:
        raise ValueError(f"Impossible de parser DATABASE_URL : {url}")
    user, password, host, port, dbname = m.groups()
    params = {"host": host, "dbname": dbname}
    if user:     params["user"]     = user
    if password: params["password"] = password
    if port:     params["port"]     = int(port)
    return params

client = openai.OpenAI(api_key=OPENAI_API_KEY)

def get_embedding(text_input: str) -> list:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text_input,
    )
    return response.data[0].embedding

def embedding_to_pg(vec: list) -> str:
    return "[" + ",".join(str(x) for x in vec) + "]"

def safe_str(val) -> str:
    if val is None:
        return ""
    if isinstance(val, str):
        return val.strip()
    return json.dumps(val, ensure_ascii=False)

def build_chunks_for_module(module: dict) -> list:
    mid   = module["id"]
    title = safe_str(module.get("title_fr")) or safe_str(module.get("title_en"))
    role  = safe_str(module.get("role"))
    level = safe_str(module.get("level"))
    chunks = []

    # Chunk 1 — Description + Objectif
    t = f"Module : {title}\nRôle : {role} | Niveau : {level}\n\n"
    desc = safe_str(module.get("description_fr"))
    obj  = safe_str(module.get("learning_objective_fr"))
    out  = safe_str(module.get("expected_outcome_fr"))
    if desc: t += f"Description :\n{desc}\n\n"
    if obj:  t += f"Objectif :\n{obj}\n\n"
    if out:  t += f"Résultat attendu :\n{out}"
    if t.strip():
        chunks.append({"text": t.strip(), "type": "desc",     "ref": f"m{mid}_desc"})

    # Chunk 2 — Concepts clés
    kc  = safe_str(module.get("key_concepts_fr"))
    why = safe_str(module.get("why_this_module_fr"))
    t2  = f"Module : {title} — Concepts clés\n\n"
    if kc:  t2 += f"Concepts :\n{kc}\n\n"
    if why: t2 += f"Pourquoi :\n{why}"
    if kc or why:
        chunks.append({"text": t2.strip(), "type": "concepts", "ref": f"m{mid}_concepts"})

    # Chunk 3 — Section content (tronqué à 600 chars pour limite index btree)
    sc = safe_str(module.get("section_content_fr"))
    if sc:
        # Extraire les 600 premiers chars du JSON/texte pour rester sous la limite btree
        sc_short = sc[:600] + ("..." if len(sc) > 600 else "")
        chunks.append({"text": f"Module : {title} — Use Case\n\n{sc_short}", "type": "section", "ref": f"m{mid}_section"})

    # Chunk 4 — Prompts (tronqué à 600 chars pour limite index btree)
    pe = safe_str(module.get("prompt_examples_fr"))
    if pe:
        pe_short = pe[:600] + ("..." if len(pe) > 600 else "")
        chunks.append({"text": f"Module : {title} — Prompts\n\n{pe_short}", "type": "prompts", "ref": f"m{mid}_prompts"})

    # Chunk 5 — Execution Task
    ex  = safe_str(module.get("practical_exercise_fr"))
    act = safe_str(module.get("action_point_fr"))
    t5  = f"Module : {title} — Mission terrain\n\n"
    if ex:  t5 += f"Exercice :\n{ex}\n\n"
    if act: t5 += f"Action :\n{act}"
    if ex or act:
        chunks.append({"text": t5.strip(), "type": "exercise", "ref": f"m{mid}_exercise"})

    # Chunk 6 — Takeaway
    pa  = safe_str(module.get("practical_application_fr"))
    tak = safe_str(module.get("takeaway_fr"))
    t6  = f"Module : {title} — Takeaway\n\n"
    if pa:  t6 += f"Application :\n{pa}\n\n"
    if tak: t6 += f"Takeaway :\n{tak}"
    if pa or tak:
        chunks.append({"text": t6.strip(), "type": "takeaway", "ref": f"m{mid}_takeaway"})

    # Chunk 7 — Tableaux
    ct = safe_str(module.get("comparison_tables_fr"))
    if ct:
        chunks.append({"text": f"Module : {title} — Outils & KPIs\n\n{ct}", "type": "tools", "ref": f"m{mid}_tools"})

    return chunks


def run():
    print("=" * 60)
    print("  RECHUNK_MODULES V3 — psycopg2 direct")
    print("=" * 60)

    db_params = parse_db_url(DATABASE_URL)
    conn = psycopg2.connect(**db_params)
    conn.autocommit = False
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        # 1. Charger les modules
        cur.execute("""
            SELECT id, role, level, title_fr, title_en,
                   description_fr, learning_objective_fr, expected_outcome_fr,
                   key_concepts_fr, why_this_module_fr, section_content_fr,
                   prompt_examples_fr, practical_exercise_fr, action_point_fr,
                   practical_application_fr, takeaway_fr, comparison_tables_fr
            FROM modules WHERE is_active = true ORDER BY id
        """)
        modules = cur.fetchall()
        print(f"\n✅ {len(modules)} modules chargés")

        # 2. Supprimer anciens chunks module
        cur.execute("SELECT COUNT(*) as n FROM content_chunks WHERE source_type = 'module'")
        old = cur.fetchone()["n"]
        cur.execute("DELETE FROM content_chunks WHERE source_type = 'module'")
        conn.commit()
        print(f"🗑️  {old} anciens chunks supprimés")

        # 3. Générer et insérer
        total_ok  = 0
        total_err = 0

        for module in modules:
            mid    = module["id"]
            title  = module.get("title_fr") or module.get("title_en") or f"Module {mid}"
            chunks = build_chunks_for_module(dict(module))

            print(f"\n📦 Module {mid} — {title}")
            print(f"   → {len(chunks)} chunks")

            for i, chunk in enumerate(chunks, 1):
                try:
                    emb     = get_embedding(chunk["text"])
                    emb_str = embedding_to_pg(emb)
                    meta    = json.dumps({
                        "module_title": title,
                        "role":  module.get("role", ""),
                        "level": module.get("level", ""),
                        "chunk_type": chunk["type"]
                    }, ensure_ascii=False)

                    cur.execute("""
                        INSERT INTO content_chunks
                            (source_type, source_id, lang, chunk_text, metadata, embedding, citation_ref)
                        VALUES (%s, %s, %s, %s, %s::jsonb, %s::vector, %s)
                    """, (
                        'module', mid, 'fr',
                        chunk["text"], meta, emb_str, chunk["ref"]
                    ))
                    conn.commit()

                    print(f"   ✅ [{i}/{len(chunks)}] {chunk['type']}")
                    total_ok += 1
                    time.sleep(0.3)

                except Exception as e:
                    conn.rollback()
                    print(f"   ❌ [{i}/{len(chunks)}] {chunk['type']} — {e}")
                    total_err += 1

        # 4. Résumé
        cur.execute("SELECT COUNT(*) as n FROM content_chunks WHERE source_type = 'module'")
        new_mod = cur.fetchone()["n"]
        cur.execute("SELECT COUNT(*) as n FROM content_chunks")
        grand   = cur.fetchone()["n"]

        print("\n" + "=" * 60)
        print(f"  ✅ Rechunking terminé")
        print(f"  • Chunks créés   : {total_ok}")
        print(f"  • Erreurs        : {total_err}")
        print(f"  • Chunks module  : {new_mod}")
        print(f"  • Total chunks   : {grand}")
        print("=" * 60)

        if total_err == 0:
            print("\n  🚀 RAG prêt — lance verify_chunks.py pour valider")
        else:
            print(f"\n  ⚠️  {total_err} erreur(s) — relance le script")

    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    run()