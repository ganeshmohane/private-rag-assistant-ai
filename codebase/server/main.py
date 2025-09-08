import os
from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import JSONResponse
import chromadb
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import re
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


def chunk_text(text, chunk_size=200):
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks, current = [], ""
    for sent in sentences:
        if len(current) + len(sent) <= chunk_size:
            current += " " + sent
        else:
            chunks.append(current.strip())
            current = sent
    if current:
        chunks.append(current.strip())
    return chunks

@app.post('/upload_text/')
async def upload_text(file: UploadFile):
    text = (await file.read()).decode('utf-8')
    chunks = chunk_text(text, chunk_size=300)
    
    for i, chunk in enumerate(chunks):
        embedding = model.encode([chunk])[0].tolist()
        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            ids=[f"{file.filename}_{i}"]
        )

    return { "status": f"Stored {len(chunks)} chunks from {file.filename}" }


@app.get('/fetch_embeddings')
def fetch_embeddings():
    data = collection.get(
        include=['documents','embeddings','metadatas'],
        limit=10000
    )
    print(data)
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
    top_docs = [(documents[i], float(similarities[i])) for i in top_k_indices]
    return top_docs

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
llm_model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")
generator = pipeline("text2text-generation", model=llm_model, tokenizer=tokenizer)

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    question = data.get("question", "")
    print(question)
    # Step 1: Embed question (your existing embedding model)
    question_emb = model.encode([question])[0]  # assumes your embedding model is loaded as 'model'

    # Step 2: Fetch all documents and embeddings
    db_data = collection.get(include=['documents','embeddings'])
    documents = db_data['documents']
    embeddings = db_data['embeddings']

    # Step 3: Find top-K similar docs
    top_docs = get_top_k_similar(question_emb, embeddings, documents, k=3)
    context = "\n\n".join([doc for doc, _ in top_docs])

    # Step 4: Build prompt for LLM
    prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer concisely:"

    # Step 5: Generate answer using local LLM
    try:
        output = generator(prompt, max_length=150, do_sample=True)
        answer = output[0]['generated_text']
        print(answer)
    except Exception as e:
        answer = f"Local LLM Error: {e}"

    return {"answer": answer}


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

