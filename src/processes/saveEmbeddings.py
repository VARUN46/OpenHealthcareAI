import http
import http.client
import json
import glob
import PyPDF2
import mariadb
import os

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


def readAllFilesInDir(dir):
    files = glob.glob(dir+"*.pdf")
    return files
    
def convertPdfToText(pdfPath):
    text = ''
    reader = PyPDF2.PdfReader(pdfPath)
    pagesLen = len(reader.pages)
    for pageNum in range(pagesLen):
        text = text + reader.pages[pageNum].extract_text()
    return text
    
def splitFileText(text, size):
    currentPos = 0
    chunk = []
    lastPos = len(text)
    while currentPos < lastPos:
        chunk.append(text[currentPos : currentPos + size])
        currentPos = currentPos + size
    return chunk


def getConnection():
    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user="root",
            password = "",
            host="127.0.0.1",
            port=3306,
            database="openhealthcareai"
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
      
    return conn


def saveEmbeddings(pdfPath):
    pdftext = convertPdfToText(pdfPath)
    splitText = splitFileText(pdftext, 200)
    
    for text in splitText:
        conn = getConnection()
        embedding = generateEmbeddingsOllama(text)
        embeddingjsontxt = json.dumps(embedding)
        cur = conn.cursor() 
        cur.execute("INSERT INTO document_vector (vector) VALUES (?) RETURNING id", [embeddingjsontxt])
        conn.commit()
        for docid in cur: 
            cur = conn.cursor() 
            cur.execute("INSERT INTO document (document_vector_id,document_text) VALUES (?,?)", (docid[0],text))    
            conn.commit()
        conn.close()
 


files = readAllFilesInDir('datasource/')
for file in files:
    saveEmbeddings(file)
