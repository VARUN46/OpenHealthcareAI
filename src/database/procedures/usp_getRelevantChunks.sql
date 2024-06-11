CREATE PROCEDURE `usp_getRelevantChunks`(
	IN `embeddingVector` JSON
)
LANGUAGE SQL
NOT DETERMINISTIC
CONTAINS SQL
SQL SECURITY DEFINER
COMMENT ''
BEGIN
	SELECT * FROM JSON_TABLE(
         embeddingVector,
         "$[*]"
         COLUMNS(
           Pos FOR ORDINALITY,
           Value FLOAT PATH "$"
         )
       ) data;

	CREATE TEMPORARY TABLE relevant_docs(
		similarity_score FLOAT,
		document_text TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
	);
	
	
	SELECT * FROM relevant_docs;
	
END