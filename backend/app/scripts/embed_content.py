"""
embed_content.py â€” fixed
========================
Correction : utilisation de CAST() explicite au lieu de ::jsonb et ::vector
pour Ã©viter le conflit de syntaxe entre placeholders psycopg2 et SQLAlchemy.
"""

import os
import sys
import time
import json
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY  = os.getenv("OPENAI_API_KEY")
DATABASE_URL    = os.getenv("DATABASE_URL")
EMBEDDING_MODEL = "text-embedding-3-small"
BATCH_SIZE      = 20
LANG            = "fr"

if not OPENAI_API_KEY:
    print("âŒ OPENAI_API_KEY manquante dans .env")
    sys.exit(1)

if not DATABASE_URL:
    print("âŒ DATABASE_URL manquante dans .env")
    sys.exit(1)

try:
    import openai
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker
except ImportError as e:
    print(f"âŒ DÃ©pendance manquante : {e}")
    sys.exit(1)

openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
engine        = create_engine(DATABASE_URL)
Session       = sessionmaker(bind=engine)


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# HELPERS
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def get_embeddings_batch(texts: list[str]) -> list[list[float]]:
    response = openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts,
    )
    return [item.embedding for item in response.data]


def upsert_chunk(session, source_type, source_id, lang, chunk_text, metadata, embedding):
    """
    FIX : on utilise CAST(%(param)s AS jsonb) et CAST(%(param)s AS vector)
    au lieu de :param::jsonb pour Ã©viter le conflit de syntaxe psycopg2/SQLAlchemy.
    """
    embedding_str = "[" + ",".join(str(x) for x in embedding) + "]"
    metadata_str  = json.dumps(metadata, ensure_ascii=False)

    session.execute(text("""
        INSERT INTO content_chunks
            (source_type, source_id, lang, chunk_text, metadata, embedding)
        VALUES
            (:source_type, :source_id, :lang, :chunk_text,
             CAST(:metadata AS jsonb),
             CAST(:embedding AS vector))
        ON CONFLICT (source_type, source_id, lang, md5(chunk_text))
        DO UPDATE SET
            embedding  = EXCLUDED.embedding,
            metadata   = EXCLUDED.metadata,
            created_at = NOW()
    """), {
        "source_type": source_type,
        "source_id":   source_id,
        "lang":        lang,
        "chunk_text":  chunk_text,
        "metadata":    metadata_str,
        "embedding":   embedding_str,
    })


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# BUILDERS â€” identiques Ã  l'original
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def build_module_chunks(session):
    rows = session.execute(text("""
        SELECT id, title_fr, description_fr, learning_objective_fr,
               expected_outcome_fr, key_concepts_fr, takeaway_fr,
               action_point_fr, level, role
        FROM modules
        WHERE is_active = true
    """)).fetchall()

    chunks = []
    for row in rows:
        parts = []
        if row.title_fr:            parts.append(f"Module : {row.title_fr}")
        if row.description_fr:      parts.append(f"Description : {row.description_fr}")
        if row.learning_objective_fr: parts.append(f"Objectif : {row.learning_objective_fr}")
        if row.expected_outcome_fr: parts.append(f"RÃ©sultat attendu : {row.expected_outcome_fr}")
        if row.takeaway_fr:         parts.append(f"Ã€ retenir : {row.takeaway_fr}")
        if row.action_point_fr:     parts.append(f"Action : {row.action_point_fr}")
        if not parts:
            continue
        chunks.append({
            "source_type": "module",
            "source_id":   row.id,
            "lang":        LANG,
            "chunk_text":  "\n".join(parts),
            "metadata":    {"module_title": row.title_fr, "level": row.level, "role": row.role},
        })

    print(f"  â†’ {len(chunks)} chunks modules construits")
    return chunks


def build_skill_chunks(session):
    rows = session.execute(text("""
        SELECT s.id, s.name, s.description,
               s.use_case_name, s.kpi_before, s.kpi_after,
               cp.name as career_path_name
        FROM skills s
        LEFT JOIN career_paths cp ON cp.id = s.career_path_id
    """)).fetchall()

    chunks = []
    for row in rows:
        parts = [f"Skill : {row.name}"]
        if row.description:    parts.append(f"Description : {row.description}")
        if row.use_case_name:  parts.append(f"Use case : {row.use_case_name}")
        if row.kpi_before:     parts.append(f"Avant IA : {row.kpi_before}")
        if row.kpi_after:      parts.append(f"AprÃ¨s IA : {row.kpi_after}")
        chunks.append({
            "source_type": "skill",
            "source_id":   row.id,
            "lang":        LANG,
            "chunk_text":  "\n".join(parts),
            "metadata":    {"skill_name": row.name, "career_path": row.career_path_name},
        })

    print(f"  â†’ {len(chunks)} chunks skills construits")
    return chunks


def build_question_chunks(session):
    rows = session.execute(text("""
        SELECT q.id, q.text, q.option_a, q.option_b, q.option_c, q.option_d,
               q.correct_answer, q.explanation, s.name as skill_name
        FROM questions q
        LEFT JOIN skills s ON s.id = q.skill_id
    """)).fetchall()

    chunks = []
    correct_map = {"A": "option_a", "B": "option_b", "C": "option_c", "D": "option_d"}
    for row in rows:
        correct_text = getattr(row, correct_map.get(row.correct_answer, "option_a"), "")
        parts = [f"Question : {row.text}", f"Bonne rÃ©ponse : {correct_text}"]
        if row.explanation: parts.append(f"Explication : {row.explanation}")
        if row.skill_name:  parts.append(f"Skill associÃ© : {row.skill_name}")
        chunks.append({
            "source_type": "question",
            "source_id":   row.id,
            "lang":        LANG,
            "chunk_text":  "\n".join(parts),
            "metadata":    {"skill_name": row.skill_name, "correct": row.correct_answer},
        })

    print(f"  â†’ {len(chunks)} chunks questions construits")
    return chunks

def build_tutorial_chunks(session):
    rows = session.execute(text("""
        SELECT id, title_fr, role, tutorials_fr
        FROM modules
        WHERE is_active = true
          AND tutorials_fr IS NOT NULL
    """)).fetchall()

    chunks = []
    for row in rows:
        tutorials = row.tutorials_fr
        if not tutorials:
            continue
        for tuto in tutorials:
            parts = [f"Tutoriel : {tuto.get('title', '')}"]
            if tuto.get("tool"):
                parts.append(f"Outil : {tuto['tool']}")
            if tuto.get("steps"):
                steps_text = "\n".join(
                    f"Étape {i+1} : {step}"
                    for i, step in enumerate(tuto["steps"])
                )
                parts.append(f"Étapes :\n{steps_text}")
            if not parts:
                continue
            chunks.append({
                "source_type": "module",
                "source_id":   row.id,
                "lang":        LANG,
                "chunk_text":  "\n".join(parts),
                "metadata":    {
                    "module_title": row.title_fr,
                    "role": row.role,
                    "section": "tutorials",
                    "tutorial_id": tuto.get("id", ""),
                },
            })

    print(f"  → {len(chunks)} chunks tutoriels construits")
    return chunks

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# PIPELINE
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def run():
    print("=" * 60)
    print("  EMBED_CONTENT.PY â€” Phase 2 Euklydia (fixed)")
    print("=" * 60)

    session = Session()
    try:
        print("\nðŸ“¦ Construction des chunks...")
        all_chunks = []
        all_chunks.extend(build_module_chunks(session))
        all_chunks.extend(build_skill_chunks(session))
        all_chunks.extend(build_question_chunks(session))
        all_chunks.extend(build_tutorial_chunks(session))

        total = len(all_chunks)
        print(f"\nâœ… Total : {total} chunks Ã  embedder")

        if total == 0:
            print("âš ï¸  Aucun chunk â€” vÃ©rifiez que les seeds ont Ã©tÃ© exÃ©cutÃ©s.")
            return

        print(f"\nðŸ”„ Embedding en cours (batch={BATCH_SIZE})...")
        embedded = 0
        errors   = 0

        for i in range(0, total, BATCH_SIZE):
            batch  = all_chunks[i : i + BATCH_SIZE]
            texts  = [c["chunk_text"] for c in batch]

            try:
                embeddings = get_embeddings_batch(texts)

                for chunk, embedding in zip(batch, embeddings):
                    upsert_chunk(
                        session,
                        source_type = chunk["source_type"],
                        source_id   = chunk["source_id"],
                        lang        = chunk["lang"],
                        chunk_text  = chunk["chunk_text"],
                        metadata    = chunk["metadata"],
                        embedding   = embedding,
                    )
                    embedded += 1

                session.commit()
                pct = round((i + len(batch)) / total * 100)
                print(f"  [{pct:3d}%] {embedded}/{total} chunks insÃ©rÃ©s...")
                time.sleep(0.1)

            except Exception as e:
                print(f"  âŒ Erreur batch {i}-{i+BATCH_SIZE} : {e}")
                session.rollback()
                errors += 1

        print("\n" + "=" * 60)
        print(f"  âœ… Embedding terminÃ© !")
        print(f"  â†’ {embedded} chunks insÃ©rÃ©s dans content_chunks")
        if errors:
            print(f"  âš ï¸  {errors} batches en erreur")
        print("=" * 60)

    except Exception as e:
        session.rollback()
        print(f"\nâŒ Erreur fatale : {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    run()
