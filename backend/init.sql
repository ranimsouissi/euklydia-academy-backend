-- 1. Extension pgvector (doit exister AVANT la table)
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Sequence pour l'id
CREATE SEQUENCE IF NOT EXISTS content_chunks_id_seq;

-- 3. Table content_chunks (citation_ref sera ajoutee par Alembic 85187baf525c)
CREATE TABLE IF NOT EXISTS public.content_chunks
(
    id integer NOT NULL DEFAULT nextval('content_chunks_id_seq'::regclass),
    source_type character varying(20) NOT NULL,
    source_id integer NOT NULL,
    lang character varying(5) NOT NULL DEFAULT 'fr',
    chunk_text text NOT NULL,
    metadata jsonb,
    embedding vector(1536),
    created_at timestamp without time zone NOT NULL DEFAULT now(),
    CONSTRAINT content_chunks_pkey PRIMARY KEY (id)
);

-- 4. Index (sauf citation_ref, ajoute par Alembic)
CREATE INDEX IF NOT EXISTS idx_content_chunks_embedding
    ON public.content_chunks USING hnsw (embedding vector_cosine_ops);

CREATE INDEX IF NOT EXISTS idx_content_chunks_lang
    ON public.content_chunks USING btree (lang);

CREATE INDEX IF NOT EXISTS idx_content_chunks_source
    ON public.content_chunks USING btree (source_type, source_id);

CREATE UNIQUE INDEX IF NOT EXISTS uq_chunk_source_lang_idx
    ON public.content_chunks USING btree (source_type, source_id, lang, md5(chunk_text));