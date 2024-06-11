import sys
from services import genaiService
import json

def getAISuggestions(payload):
    suggestions = 'Something went wrong'
    aiResponse = json.loads(genaiService.getPromptResponse("ToDo: Empty", payload['requestText']))
    if aiResponse['done']:
        suggestions = { 'suggestions' : aiResponse['response'] }
    return suggestions