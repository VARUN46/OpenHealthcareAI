CREATE PROCEDURE `usp_getRelevantChunks`(
	IN `embeddingVector` JSON
)
LANGUAGE SQL
NOT DETERMINISTIC
CONTAINS SQL
SQL SECURITY DEFINER
COMMENT ''
BEGIN

	CREATE TEMPORARY TABLE embeddingVector_spread(
	Id INT,
	embeddingVal FLOAT
	);
	
	CREATE TEMPORARY TABLE currentEmbeddingVector_spread(
	Id INT,
	embeddingVal FLOAT
	);


	INSERT INTO embeddingVector_spread SELECT Pos,Value FROM JSON_TABLE(
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
	
	SET @similarDocsCount = 0;
	SET @currIndex = (SELECT MIN(id) FROM document_vector);
	SET @maxIndex = (SELECT MAX(id) FROM document_vector);
	SET @documentText = '';
	SET @vectorVal = '[]';
	
	FindCosineSimilarDocs:
	WHILE @similarDocsCount < 3 AND @currIndex <= @maxIndex
	DO
		
		SELECT d.document_text,dv.vector INTO @documentText,@vectorVal FROM document d JOIN document_vector dv 
		ON d.document_vector_id = dv.id
		WHERE d.document_vector_id = @currIndex
		LIMIT 1;

		INSERT INTO currentEmbeddingVector_spread SELECT Pos,Value FROM JSON_TABLE(
         @vectorVal,
         "$[*]"
         COLUMNS(
           Pos FOR ORDINALITY,
           Value FLOAT PATH "$"
         )
       ) data;
		
		
		SET @currentScore = (SELECT 
    		SUM(a.embeddingVal * b.embeddingVal) / (  
        		SQRT(SUM(a.embeddingVal * a.embeddingVal)) * SQRT(SUM(b.embeddingVal * b.embeddingVal))   
    	)
		FROM embeddingVector_spread a JOIN currentEmbeddingVector_spread b
		ON a.Id = b.Id
		LIMIT 1);
    	
    	IF @currentScore > 0.8
    	THEN
    	
    		INSERT INTO relevant_docs VALUES (@currentScore,@documentText);
    		
    	END IF;
		
		SET @currIndex = @currIndex + 1;
		SET @similarDocsCount = @similarDocsCount + 1;
	
	END WHILE FindCosineSimilarDocs;
	
	
	
	SELECT * FROM relevant_docs;
	
	DROP TABLE relevant_docs;
	DROP TABLE embeddingVector_spread;
	DROP TABLE currentEmbeddingVector_spread;
	
END