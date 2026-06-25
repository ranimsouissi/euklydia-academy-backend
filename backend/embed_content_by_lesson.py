"""
embed_content_by_lesson.py
==========================
Re-embedde le contenu de chaque module par section (unitÃ©),
en associant chaque chunk au lesson_id de la premiÃ¨re leÃ§on de l'unitÃ©.

Structure :
  Unit 1 (Use Case + KPI)    â†’ lesson_id = premiÃ¨re leÃ§on unit 1
  Unit 2 (Skills)            â†’ lesson_id = premiÃ¨re leÃ§on unit 2
  Unit 3 (Execution Content) â†’ lesson_id = premiÃ¨re leÃ§on unit 3
  Unit 4 (Mission)           â†’ lesson_id = premiÃ¨re leÃ§on unit 4
  Unit 5 (KPI Measurement)   â†’ lesson_id = premiÃ¨re leÃ§on unit 5

Usage :
    cd backend
    python embed_content_by_lesson.py
"""

import os
import sys
import json
import time
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL   = os.getenv("DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not DATABASE_URL or not OPENAI_API_KEY:
    print("âŒ DATABASE_URL ou OPENAI_API_KEY manquant dans .env")
    sys.exit(1)

import openai
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

engine  = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
client  = openai.OpenAI(api_key=OPENAI_API_KEY)


def get_embedding(text_input: str) -> list[float]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text_input
    )
    return response.data[0].embedding


def upsert_chunk(session, lesson_id, source_type, chunk_text, citation_ref, metadata):
    embedding = get_embedding(chunk_text)
    embedding_str = "[" + ",".join(str(x) for x in embedding) + "]"
    metadata_str  = json.dumps(metadata, ensure_ascii=False)

    session.execute(text("""
        INSERT INTO content_chunks
            (source_type, source_id, lang, chunk_text, metadata, embedding, citation_ref)
        VALUES
            (:source_type, :source_id, 'fr', :chunk_text,
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
        "source_id":    lesson_id,
        "chunk_text":   chunk_text,
        "metadata":     metadata_str,
        "embedding":    embedding_str,
        "citation_ref": citation_ref,
    })


def build_chunks_for_module(module, unit_lesson_map):
    """
    Construit les chunks par section (unitÃ©) pour un module.
    Retourne une liste de (lesson_id, source_type, chunk_text, citation_ref, metadata).
    """
    chunks = []
    section_content = module.get("section_content_fr") or {}
    comparison_tables = module.get("comparison_tables_fr") or {}
    prompt_examples = module.get("prompt_examples_fr") or []
    practical_exercise = module.get("practical_exercise_fr") or {}
    key_concepts = module.get("key_concepts_fr") or []
    tutorials_fr = module.get("tutorials_fr") or []
    module_id = module["id"]
    title = module.get("title_fr", "")

    # â”€â”€ UNIT 1 : Use Case + KPI â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    lesson_id_1 = unit_lesson_map.get(module_id, {}).get(1)
    if lesson_id_1:
        use_case = section_content.get("use_case_detail") or {}
        if use_case.get("narrative"):
            chunks.append((lesson_id_1, "lesson",
                f"Use Case â€” {title}\n{use_case['narrative']}",
                f"UC.{module_id}.narrative",
                {"module": title, "section": "use_case"}))
        if use_case.get("pain_points"):
            text_pp = "\n".join(f"- {p}" for p in use_case["pain_points"])
            chunks.append((lesson_id_1, "lesson",
                f"Pain points â€” {title}\n{text_pp}",
                f"UC.{module_id}.pain_points",
                {"module": title, "section": "pain_points"}))
        kpi = comparison_tables.get("kpi_targets") or {}
        if kpi.get("rows"):
            rows_text = "\n".join(" | ".join(str(c) for c in row) for row in kpi["rows"])
            chunks.append((lesson_id_1, "lesson",
                f"KPI cibles â€” {title}\n{rows_text}",
                f"KPI.{module_id}.targets",
                {"module": title, "section": "kpi"}))

    # â”€â”€ UNIT 2 : Skills mapped â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    lesson_id_2 = unit_lesson_map.get(module_id, {}).get(2)
    if lesson_id_2 and key_concepts:
        concepts = key_concepts if isinstance(key_concepts, list) else [key_concepts]
        text_concepts = "\n".join(f"- {c}" for c in concepts)
        chunks.append((lesson_id_2, "lesson",
            f"CompÃ©tences clÃ©s â€” {title}\n{text_concepts}",
            f"SK.{module_id}.concepts",
            {"module": title, "section": "skills"}))

    # â”€â”€ UNIT 3 : Execution Content â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    lesson_id_3 = unit_lesson_map.get(module_id, {}).get(3)
    if lesson_id_3:
        for i, prompt in enumerate(prompt_examples):
            text_prompt = f"Prompt {i+1} â€” {prompt.get('title', '')}\n{prompt.get('content', '')}"
            chunks.append((lesson_id_3, "lesson",
                text_prompt,
                f"PR.{module_id}.{i+1}",
                {"module": title, "section": "templates", "prompt_id": prompt.get("id")}))
        tools = comparison_tables.get("tools") or {}
        if tools.get("rows"):
            rows_text = "\n".join(" | ".join(str(c) for c in row) for row in tools["rows"])
            chunks.append((lesson_id_3, "lesson",
                f"Outils â€” {title}\n{rows_text}",
                f"TL.{module_id}.tools",
                {"module": title, "section": "tools"}))
        workflows = comparison_tables.get("workflows") or {}
        if workflows.get("rows"):
            rows_text = "\n".join(" | ".join(str(c) for c in row) for row in workflows["rows"])
            chunks.append((lesson_id_3, "lesson",
                f"Workflows â€” {title}\n{rows_text}",
                f"WF.{module_id}.workflows",
                {"module": title, "section": "workflows"}))
        tutorials = tutorials_fr or section_content.get("tutorials") or []
        for i, tuto in enumerate(tutorials):
            chunks.append((lesson_id_3, "lesson",
                f"Tutoriel â€” {tuto.get('title', '')}\nFormat: {tuto.get('format', '')} â€” {tuto.get('duration_min', '')} min",
                f"TU.{module_id}.{i+1}",
                {"module": title, "section": "tutorials"}))

    # â”€â”€ UNIT 4 : Mission terrain â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    lesson_id_4 = unit_lesson_map.get(module_id, {}).get(4)
    if lesson_id_4 and practical_exercise:
        mission_text = f"Mission terrain â€” {practical_exercise.get('title', '')}\n"
        if practical_exercise.get("objective"):
            mission_text += f"Objectif: {practical_exercise['objective']}\n"
        if practical_exercise.get("steps"):
            for step in practical_exercise["steps"]:
                mission_text += f"- {step.get('title', '')}: {step.get('description', '')}\n"
        if practical_exercise.get("success_criteria"):
            mission_text += "CritÃ¨res de rÃ©ussite:\n"
            for c in practical_exercise["success_criteria"]:
                mission_text += f"âœ“ {c}\n"
        chunks.append((lesson_id_4, "lesson",
            mission_text.strip(),
            f"MI.{module_id}.mission",
            {"module": title, "section": "mission"}))

    # â”€â”€ UNIT 5 : KPI Measurement + Progress â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    lesson_id_5 = unit_lesson_map.get(module_id, {}).get(5)
    if lesson_id_5:
        kpi_m = section_content.get("kpi_targets") or {}
        if kpi_m.get("rows"):
            rows_text = "\n".join(" | ".join(str(c) for c in row) for row in kpi_m["rows"])
            chunks.append((lesson_id_5, "lesson",
                f"KPI Measurement â€” {title}\n{rows_text}",
                f"KM.{module_id}.measurement",
                {"module": title, "section": "kpi_measurement"}))

    return chunks


def run():
    print("=" * 60)
    print("  EMBED_CONTENT_BY_LESSON.PY â€” Euklydia")
    print("=" * 60)

    session = Session()
    try:
        # 1. RÃ©cupÃ©rer le mapping module_id â†’ unit_order â†’ first_lesson_id
        rows = session.execute(text("""
            SELECT m.id as module_id, u.order as unit_order, MIN(l.id) as lesson_id
            FROM modules m
            JOIN units u ON u.module_id = m.id
            JOIN lessons l ON l.unit_id = u.id
            WHERE m.is_active = true
            GROUP BY m.id, u.order
            ORDER BY m.id, u.order
        """)).fetchall()

        unit_lesson_map = {}
        for row in rows:
            mid, uord, lid = row.module_id, row.unit_order, row.lesson_id
            if mid not in unit_lesson_map:
                unit_lesson_map[mid] = {}
            unit_lesson_map[mid][uord] = lid

        print(f"âœ… {len(unit_lesson_map)} modules trouvÃ©s avec mapping unitÃ© â†’ leÃ§on")

        # 2. RÃ©cupÃ©rer tous les modules
        modules = session.execute(text("""
            SELECT id, title_fr, key_concepts_fr, tutorials_fr,
                   prompt_examples_fr, comparison_tables_fr,
                   practical_exercise_fr, section_content_fr,
                   progress_update_fr
            FROM modules
            WHERE is_active = true
            ORDER BY id
        """)).fetchall()

        all_chunks = []
        for module_row in modules:
            module = dict(module_row._mapping)
            # Parse JSON fields
            for field in ["key_concepts_fr", "tutorials_fr", "prompt_examples_fr",
                          "comparison_tables_fr", "practical_exercise_fr",
                          "section_content_fr", "progress_update_fr"]:
                val = module.get(field)
                if isinstance(val, str):
                    try: module[field] = json.loads(val)
                    except: module[field] = None

            chunks = build_chunks_for_module(module, unit_lesson_map)
            all_chunks.extend(chunks)
            print(f"  Module {module['id']} â€” {module['title_fr'][:40]}: {len(chunks)} chunks")

        total = len(all_chunks)
        print(f"\nðŸ“¦ Total: {total} chunks Ã  embedder")

        # 3. Embedder et insÃ©rer
        embedded = 0
        errors = 0
        for lesson_id, source_type, chunk_text, citation_ref, metadata in all_chunks:
            try:
                upsert_chunk(session, lesson_id, source_type, chunk_text, citation_ref, metadata)
                embedded += 1
                if embedded % 10 == 0:
                    session.commit()
                    print(f"  [{embedded}/{total}] chunks insÃ©rÃ©s...")
                time.sleep(0.05)
            except Exception as e:
                print(f"  âŒ Erreur chunk '{citation_ref}': {e}")
                session.rollback()
                errors += 1

        session.commit()
        print(f"\n{'=' * 60}")
        print(f"  âœ… Embedding terminÃ© !")
        print(f"  â†’ {embedded} chunks insÃ©rÃ©s avec lesson_id contextuel")
        if errors:
            print(f"  âš ï¸  {errors} erreurs")
        print(f"{'=' * 60}")

    except Exception as e:
        session.rollback()
        print(f"\nâŒ Erreur fatale: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    run()
