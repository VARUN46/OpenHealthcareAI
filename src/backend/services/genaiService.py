import http.client
import json

def getPromptResponse(systemPrompt,userPrompt):
    conn = http.client.HTTPConnection("localhost", 11434)
    payload = json.dumps({
        "model": "tinyllama",
        "stream": False,
        "system": systemPrompt,
        "prompt": userPrompt
    })
    headers = {
    'Content-Type': 'application/json'
    }
    conn.request("POST", "/api/generate", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")