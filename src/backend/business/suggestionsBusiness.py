import sys
from services import genaiService, dbService
import json

def getAISuggestions(payload):
    suggestions = 'Something went wrong'
    requestText = payload['requestText']
    embeddings = genaiService.generateEmbeddings(requestText)
    knowledgebase = getRelevantDocs(embeddings)
    aiResponse = json.loads(genaiService.getPromptResponse(knowledgebase, requestText))
    if aiResponse['done']:
        suggestions = { 'suggestions' : aiResponse['response'] }
    return suggestions

def getRelevantDocs(embedding):
    conn = dbService.getConnection()
    cur = conn.cursor()
    cur.execute('')
