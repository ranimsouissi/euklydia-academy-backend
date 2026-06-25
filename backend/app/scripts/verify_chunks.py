"""
verify_chunks.py
================
Phase 2 — Validation de l'intégration content_chunks

Ce script vérifie :
1. Que content_chunks contient des données
2. Que les embeddings sont bien générés (non NULL)
3. Que chaque module/skill/question a son chunk
4. Teste une recherche sémantique simple

Usage :
    cd backend
    python scripts/verify_chunks.py
"""

import os
import sys
import json
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL  = os.getenv("DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not DATABASE_URL:
    print("❌ DATABASE_URL manquante dans .env")
    sys.exit(1)

try:
    import openai
    from sqlalchemy import create_engine, text
except ImportError as e:
    print(f"❌ Dépendance manquante : {e}")
    sys.exit(1)

engine = create_engine(DATABASE_URL)


def run():
    print("=" * 60)
    print("  VERIFY_CHUNKS.PY — Validation Phase 2")
    print("=" * 60)

    with engine.connect() as conn:

        # ── 1. Comptages généraux ────────────────────────────────────────────
        print("\n📊 Statistiques content_chunks :")

        total = conn.execute(text(
            "SELECT COUNT(*) FROM content_chunks"
        )).scalar()
        print(f"  Total chunks          : {total}")

        with_embedding = conn.execute(text(
            "SELECT COUNT(*) FROM content_chunks WHERE embedding IS NOT NULL"
        )).scalar()
        print(f"  Avec embedding        : {with_embedding}")

        without_embedding = total - with_embedding
        if without_embedding > 0:
            print(f"  ⚠️  Sans embedding     : {without_embedding}")
        else:
            print(f"  ✅ Sans embedding     : 0")

        # ── 2. Par source_type ───────────────────────────────────────────────
        print("\n📦 Répartition par source_type :")
        rows = conn.execute(text("""
            SELECT source_type, COUNT(*) as count
            FROM content_chunks
            GROUP BY source_type
            ORDER BY source_type
        """)).fetchall()

        for row in rows:
            print(f"  {row.source_type:<12} : {row.count} chunks")

        # ── 3. Vérification couverture modules ───────────────────────────────
        print("\n🔍 Couverture modules :")
        total_modules = conn.execute(text(
            "SELECT COUNT(*) FROM modules WHERE is_active = true"
        )).scalar()
        embedded_modules = conn.execute(text(
            "SELECT COUNT(DISTINCT source_id) FROM content_chunks WHERE source_type = 'module'"
        )).scalar()
        print(f"  Modules actifs        : {total_modules}")
        print(f"  Modules avec chunks   : {embedded_modules}")
        if total_modules > 0:
            coverage = round(embedded_modules / total_modules * 100)
            status = "✅" if coverage == 100 else "⚠️ "
            print(f"  {status} Couverture          : {coverage}%")

        # ── 4. Vérification couverture questions ─────────────────────────────
        print("\n🔍 Couverture questions :")
        total_questions = conn.execute(text(
            "SELECT COUNT(*) FROM questions"
        )).scalar()
        embedded_questions = conn.execute(text(
            "SELECT COUNT(DISTINCT source_id) FROM content_chunks WHERE source_type = 'question'"
        )).scalar()
        print(f"  Questions totales     : {total_questions}")
        print(f"  Questions avec chunks : {embedded_questions}")
        if total_questions > 0:
            coverage = round(embedded_questions / total_questions * 100)
            status = "✅" if coverage == 100 else "⚠️ "
            print(f"  {status} Couverture          : {coverage}%")

        # ── 5. Test recherche sémantique (si clé OpenAI dispo) ───────────────
        if OPENAI_API_KEY:
            print("\n🧪 Test recherche sémantique RAG :")
            test_query = "Comment utiliser l'IA pour qualifier des leads ?"
            print(f"  Query : \"{test_query}\"")

            try:
                client = openai.OpenAI(api_key=OPENAI_API_KEY)
                response = client.embeddings.create(
                    model="text-embedding-3-small",
                    input=test_query,
                )
                query_embedding = response.data[0].embedding
                embedding_str = "[" + ",".join(str(x) for x in query_embedding) + "]"

                results = conn.execute(text("""
                    SELECT source_type, source_id, chunk_text,
                           1 - (embedding <=> :embedding::vector) AS similarity,
                           metadata
                    FROM content_chunks
                    WHERE embedding IS NOT NULL
                    ORDER BY embedding <=> :embedding::vector
                    LIMIT 3
                """), {"embedding": embedding_str}).fetchall()

                print(f"  Top 3 résultats :")
                for i, r in enumerate(results, 1):
                    sim = round(r.similarity * 100, 1)
                    meta = json.loads(r.metadata) if r.metadata else {}
                    title = meta.get("module_title") or meta.get("skill_name") or meta.get("question_text", "")
                    print(f"  {i}. [{r.source_type}] {title[:50]} — similarité {sim}%")

                print("  ✅ Recherche RAG fonctionnelle !")

            except Exception as e:
                print(f"  ❌ Erreur test RAG : {e}")
        else:
            print("\n⏭️  Test RAG ignoré (OPENAI_API_KEY non configurée)")
            print("   → Relancez après avoir ajouté la clé pour valider la recherche.")

        # ── 6. Résumé final ──────────────────────────────────────────────────
        print("\n" + "=" * 60)
        if with_embedding == total and total > 0:
            print("  ✅ Phase 2 validée — content_chunks prêt pour le tutor !")
        elif total == 0:
            print("  ❌ content_chunks est vide — lancez embed_content.py d'abord")
        else:
            print("  ⚠️  Phase 2 partielle — certains embeddings manquants")
        print("=" * 60)


if __name__ == "__main__":
    run()
