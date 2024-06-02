-- Table: public.document

-- DROP TABLE IF EXISTS public.document;

CREATE TABLE IF NOT EXISTS public.document
(
    "Id" bigint NOT NULL DEFAULT nextval('"document_Id_seq"'::regclass),
    docchunktext text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT document_pkey PRIMARY KEY ("Id")
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.document
    OWNER to postgres;