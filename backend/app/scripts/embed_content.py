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


def upsert_chunk(session, source_type, source_id, lang, chunk_text, metadata, embedding, citation_ref=None):
    """
    FIX : on utilise CAST(%(param)s AS jsonb) et CAST(%(param)s AS vector)
    au lieu de :param::jsonb pour éviter le conflit de syntaxe psycopg2/SQLAlchemy.
    """
    embedding_str = "[" + ",".join(str(x) for x in embedding) + "]"
    metadata_str  = json.dumps(metadata, ensure_ascii=False)

    session.execute(text("""
        INSERT INTO content_chunks
            (source_type, source_id, lang, chunk_text, metadata, embedding, citation_ref)
        VALUES
            (:source_type, :source_id, :lang, :chunk_text,
             CAST(:metadata AS jsonb),
             CAST(:embedding AS vector),
             :citation_ref)
        ON CONFLICT (source_type, source_id, lang, md5(chunk_text))
        DO UPDATE SET
            embedding    = EXCLUDED.embedding,
            metadata     = EXCLUDED.metadata,
            citation_ref = EXCLUDED.citation_ref,
            created_at   = NOW()
    """), {
        "source_type":  source_type,
        "source_id":    source_id,
        "lang":         lang,
        "chunk_text":   chunk_text,
        "metadata":     metadata_str,
        "embedding":    embedding_str,
        "citation_ref": citation_ref,
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
            "metadata":    {"module_title": row.title_fr, "level": row.level, "role": row.role, "section_type": "use_case"},
            "citation_ref": f"{row.id}.module",
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
    "section_type": "execution_content",
    "chunk_subtype": "tutorial",
    "tutorial_id": tuto.get("id", ""),
},
"citation_ref": f"{row.id}.tutorial.{tuto.get('id', '')}",
            })

    print(f"  → {len(chunks)} chunks tutoriels construits")
    return chunks
def build_prompt_chunks(session):
    rows = session.execute(text("""
        SELECT id, title_fr, role, prompt_examples_fr
        FROM modules
        WHERE is_active = true
          AND prompt_examples_fr IS NOT NULL
    """)).fetchall()

    chunks = []
    for row in rows:
        prompts = row.prompt_examples_fr
        if not prompts:
            continue
        for prompt in prompts:
            parts = [f"Template : {prompt.get('title', '')}"]
            if prompt.get("use_case"):
                parts.append(f"Cas d'usage : {prompt['use_case']}")
            if prompt.get("content"):
                parts.append(f"Contenu du prompt :\n{prompt['content']}")
            if prompt.get("expected_output"):
                parts.append(f"Résultat attendu : {prompt['expected_output']}")
            if prompt.get("tools"):
                parts.append(f"Outils : {', '.join(prompt['tools'])}")
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
                    "section_type": "execution_content",
                    "chunk_subtype": "template",
                    "prompt_id": prompt.get("id", ""),
                },
                "citation_ref": f"{row.id}.template.{prompt.get('id', '')}",
            })

    print(f"  → {len(chunks)} chunks templates construits")
    return chunks
def build_tools_workflows_chunks(session):
    rows = session.execute(text("""
        SELECT id, title_fr, role, comparison_tables_fr
        FROM modules
        WHERE is_active = true
          AND comparison_tables_fr IS NOT NULL
    """)).fetchall()

    chunks = []
    for row in rows:
        tables = row.comparison_tables_fr
        if not tables:
            continue

        for table_key in ["tools", "workflows"]:
            table = tables.get(table_key)
            if not table or not table.get("rows"):
                continue

            headers = table.get("headers", [])
            for i, table_row in enumerate(table["rows"]):
                line_parts = [
                    f"{headers[j]} : {table_row[j]}"
                    for j in range(min(len(headers), len(table_row)))
                ]
                chunk_text = f"{table.get('title', table_key)}\n" + "\n".join(line_parts)

                chunks.append({
                    "source_type": "module",
                    "source_id":   row.id,
                    "lang":        LANG,
                    "chunk_text":  chunk_text,
                    "metadata":    {
                        "module_title": row.title_fr,
                        "role": row.role,
                        "section_type": "execution_content",
                        "chunk_subtype": table_key,
                        "row_index": i,
                    },
                    "citation_ref": f"{row.id}.{table_key}.{i}",
                })

    print(f"  → {len(chunks)} chunks tools/workflows construits")
    return chunks
def build_resource_chunks(session):
    rows = session.execute(text("""
        SELECT id, title_fr, role, section_content_fr
        FROM modules
        WHERE is_active = true
          AND section_content_fr IS NOT NULL
    """)).fetchall()

    chunks = []
    for row in rows:
        section_content = row.section_content_fr
        if not section_content:
            continue

        resources = section_content.get("resources", [])
        if not resources:
            continue

        for resource in resources:
            parts = [f"Ressource : {resource.get('title', '')}"]
            if resource.get("type"):
                parts.append(f"Type : {resource['type']}")
            if resource.get("description"):
                parts.append(f"Description : {resource['description']}")
            if resource.get("url"):
                parts.append(f"URL : {resource['url']}")
            if resource.get("tags"):
                parts.append(f"Tags : {', '.join(resource['tags'])}")

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
    "section_type": "execution_content",
    "chunk_subtype": "resource",
    "resource_id": resource.get("id", ""),
    "resource_url": resource.get("url", ""),
},
"citation_ref": f"{row.id}.resource.{resource.get('id', '')}",
            })

    print(f"  → {len(chunks)} chunks resources construits")
    return chunks
def build_use_case_chunks(session):
    rows = session.execute(text("""
        SELECT id, title_fr, role, section_content_fr
        FROM modules
        WHERE is_active = true
          AND section_content_fr IS NOT NULL
    """)).fetchall()

    chunks = []
    for row in rows:
        section_content = row.section_content_fr
        if not section_content:
            continue

        use_case = section_content.get("use_case_detail")
        if not use_case:
            continue

        parts = []
        if use_case.get("title"):
            parts.append(f"Use Case : {use_case['title']}")
        if use_case.get("narrative"):
            parts.append(f"Problème business : {use_case['narrative']}")
        if use_case.get("pain_points"):
            pain_points_text = "\n".join(
                f"- {p}" for p in use_case["pain_points"]
            )
            parts.append(f"Points de friction rencontrés :\n{pain_points_text}")

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
                "section_type": "use_case",
            },
            "citation_ref": f"{row.id}.use_case",
        })

    print(f"  → {len(chunks)} chunks use_case construits")
    return chunks
def build_kpi_chunks(session):
    rows = session.execute(text("""
        SELECT id, title_fr, role, section_content_fr, comparison_tables_fr
        FROM modules
        WHERE is_active = true
    """)).fetchall()

    chunks = []
    for row in rows:
        section_content = row.section_content_fr or {}
        tables = row.comparison_tables_fr or {}

        parts = []

        kpi_pattern = section_content.get("kpi_pattern")
        if kpi_pattern:
            if kpi_pattern.get("description"):
                parts.append(f"Méthode KPI : {kpi_pattern['description']}")
            for level in kpi_pattern.get("levels", []):
                parts.append(
                    f"{level.get('level', '')} ({level.get('horizon', '')}) — "
                    f"{level.get('type', '')} : {level.get('examples', '')}"
                )

        kpi_targets = tables.get("kpi_targets")
        if kpi_targets and kpi_targets.get("rows"):
            headers = kpi_targets.get("headers", [])
            for kpi_row in kpi_targets["rows"]:
                line = ", ".join(
                    f"{headers[j]} : {kpi_row[j]}"
                    for j in range(min(len(headers), len(kpi_row)))
                )
                parts.append(f"Objectif KPI — {line}")

        # ── Milestone J0 (déclaration baseline) — appartient à la section KPI ──
        method = section_content.get("kpi_measurement_method")
        if method:
            for milestone in method.get("milestones", []):
                if milestone.get("when") == "J0":
                    parts.append(f"J0 : {milestone.get('what', '')}")

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
                "section_type": "kpi",
            },
            "citation_ref": f"{row.id}.kpi",
        })

    print(f"  → {len(chunks)} chunks kpi construits")
    return chunks
def build_kpi_measurement_chunks(session):
    rows = session.execute(text("""
        SELECT id, title_fr, role, section_content_fr
        FROM modules
        WHERE is_active = true
          AND section_content_fr IS NOT NULL
    """)).fetchall()

    chunks = []
    for row in rows:
        section_content = row.section_content_fr
        if not section_content:
            continue

        method = section_content.get("kpi_measurement_method")
        if not method:
            continue

        parts = []
        if method.get("title"):
            parts.append(f"Méthode de mesure : {method['title']}")
        for milestone in method.get("milestones", []):
            if milestone.get("when") == "J0":
                continue  # J0 appartient à la section KPI, pas KPI Measurement
            parts.append(f"{milestone.get('when', '')} : {milestone.get('what', '')}")

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
                "section_type": "kpi_measurement",
            },
            "citation_ref": f"{row.id}.kpi_measurement",
        })

    print(f"  → {len(chunks)} chunks kpi_measurement construits")
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
        all_chunks.extend(build_prompt_chunks(session)) 
        all_chunks.extend(build_tools_workflows_chunks(session))
        all_chunks.extend(build_resource_chunks(session))
        all_chunks.extend(build_use_case_chunks(session))
        all_chunks.extend(build_kpi_chunks(session))
        all_chunks.extend(build_kpi_measurement_chunks(session))

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
                        citation_ref = chunk.get("citation_ref"),
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
