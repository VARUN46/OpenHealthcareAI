-- Table: public.document_vector

-- DROP TABLE IF EXISTS public.document_vector;

CREATE TABLE IF NOT EXISTS public.document_vector
(
    document_id bigint NOT NULL,
    vector_position integer NOT NULL,
    dimension point NOT NULL
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.document_vector
    OWNER to postgres;