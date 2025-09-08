import os
from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import JSONResponse
import chromadb
from sentence_transformers import SentenceTransformer
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import requests 
from dotenv import load_dotenv

load_dotenv()
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE")
HF_API_URL = "https://api-inference.huggingface.co/models/openai/gpt-oss-120b"

app = FastAPI()
client = chromadb.PersistentClient(path='./chroma_db')
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
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


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def get_top_k_similar(question_embedding, embeddings, documents, k=3):
    similarities = [cosine_similarity(question_embedding, emb) for emb in embeddings]
    top_k_indices = np.argsort(similarities)[::-1][:k]
    top_docs = [documents[i] for i in top_k_indices]
    return top_docs

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    print('data from frontend', data)
    question = data.get("question", "")

    # Step 1: Embed the question
    question_emb = model.encode([question])[0]

    # Step 2: Fetch all documents and embeddings
    db_data = collection.get(include=['documents','embeddings'])
    documents = db_data['documents']
    embeddings = db_data['embeddings']

    # Step 3: Find top-K similar docs
    top_docs = get_top_k_similar(question_emb, embeddings, documents, k=3)
    print('similar data',top_docs)
    return {'answer': top_docs }
    
    # Step 4: Build context for LLM
    # context = "\n\n".join(top_docs)
    # prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"

    ## Step 5: Call Hugging Face Inference API
    # headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}
    # payload = {"inputs": prompt}
    # try:
    #     response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=60)
    #     print("Raw response:", response.text)
    #     if response.status_code == 200:
    #         result = response.json()
    #         # Hugging Face API returns 'generated_text' or similar, depends on model
    #         answer = result.get("generated_text") or (
    #             result[0]["generated_text"] if isinstance(result, list) and "generated_text" in result[0] else str(result)
    #         )
    #     else:
    #         # Print full error for debugging
    #         answer = f"HuggingFace Error: {response.status_code}: {response.text}"
    # except Exception as e:
    #     answer = f"HuggingFace Connection Error: {e}"
    # return {"answer": answer}

@app.get('/hello/')
def hello():
    return "hello"

