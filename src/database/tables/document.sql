CREATE TABLE document(
document_vector_id BIGINT,
document_text TEXT 
)
ALTER TABLE document 
MODIFY COLUMN document_text TEXT
CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
