from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
import chromadb
from sentence_transformers import SentenceTransformer

app = FastAPI()
client = chromadb.PersistentClient(path='./chroma_db')
model = SentenceTransformer()
collection = client.get_or_create_collection(name="documents")
model = SentenceTransformer("all-MiniLM-L6-v2")

@app.post('/upload_text/')
async def upload_text(file: UploadFile):
    text = (await file.read()).decode('utf-8')
    #print('data received on server:', text)
    embedding = model.encode([text])[0].tolist()
    #print('data converted into vectors:',embedding)
    collection.add(
        documents=[text],
        embeddings=[embedding],
        ids=[file.filename]
    )

    return { "status" : "Successfully Stored" }

@app.get('/fetch_embeddings')
def fetch_embeddings():
    data = collection.get(include=['documents','embeddings','metadatas'])
    return JSONResponse(content={
        'ids' : data['ids'],
        'documents': data['documents'],
        'embeddings': [list(map(float, emb)) for emb in data['embeddings']]
    })

@app.get('/hello/')
def hello():
    return "hello"

