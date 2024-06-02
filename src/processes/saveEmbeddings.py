import http
import http.client
import json


def generateEmbeddingsOllama(text):
    conn = http.client.HTTPConnection("localhost", 11434)
    payload = json.dumps({ 
                'model': 'snowflake-arctic-embed',
                'prompt': text
               })
    
    headers = {
        'Content-Type': 'text/plain'
    }
    conn.request("POST", "/api/embeddings", payload, headers)
    res = conn.getresponse()
    data = res.read()
    vector = json.loads(data.decode("utf-8"))
    return vector['embedding']



def readAllFiles():
    pass

def saveEmbeddings(embeddings):
    pass    

embeddings = generateEmbeddingsOllama('hello')
print(embeddings)