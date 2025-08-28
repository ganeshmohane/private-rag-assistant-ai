## 1. What is a Vector Database (Vector DB)?
A **Vector DB** is a database optimized to store and search high-dimensional vectors (embeddings).  
These vectors represent text, documents, or other data in numerical form.  
Examples: **FAISS, ChromaDB, Weaviate, Milvus**.

## 2. What is an Embedding?
An **embedding** is a numerical representation of text (or other data) in a multi-dimensional space.  
It captures **semantic meaning** — so words/phrases with similar meanings have vectors that are close to each other.  
Example: "car" and "automobile" → embeddings will be very close.

## 3. How does an Embedding look?
An embedding is typically a long list of floating-point numbers (vector).  
Example (shortened):  
```

\[0.124, -0.876, 0.452, 0.001, -0.239, ...]

```
For models like `sentence-transformers`, an embedding might have **768 dimensions**.


## 4. Why do we need a Vector DB instead of SQL?
- SQL databases are good for structured queries.  
- But embeddings are **high-dimensional numeric vectors** (not rows/columns).  
- A vector DB allows **fast similarity search** (finding nearest neighbors in vector space).  


## 5. What is Cosine Similarity?
Cosine similarity measures **how similar two vectors are**, based on the angle between them.  
Formula:  
```

cos(θ) = (A · B) / (||A|| \* ||B||)

```
Where:  
- `A · B` = dot product of vectors A and B  
- `||A||` and `||B||` = magnitudes of vectors  

Values range from:  
- **1 → very similar**  
- **0 → no similarity**  
- **-1 → completely opposite**

## 6. Example of Cosine Similarity
Vector A = [1, 2, 3]  
Vector B = [2, 4, 6]  

- Dot product = 1\*2 + 2\*4 + 3\*6 = 28  
- Magnitude(A) = √(1²+2²+3²) = √14  
- Magnitude(B) = √(2²+4²+6²) = √56  
- Cosine similarity = 28 / (√14 * √56) = 1 (perfect similarity)

## 7. What is RAG (Retrieval-Augmented Generation)?
RAG is an approach where:  
1. Query is embedded.  
2. Vector DB retrieves the most relevant documents.  
3. The retrieved documents are passed as **context** to a language model.  
4. The LLM generates an answer backed by the documents.

## 8. Difference between TF-IDF and Embeddings
- **TF-IDF**: Counts word frequency, good for keyword-based search.  
- **Embeddings**: Capture meaning and context, better for semantic search.  

## 9. What is Euclidean Distance vs Cosine Similarity?
- **Euclidean Distance**: Measures straight-line distance between vectors.  
- **Cosine Similarity**: Measures angle between vectors.  
- In text retrieval, **cosine similarity** is preferred because vector magnitude (document length) is less important than direction (meaning).

## 10. What is an Open-Source LLM (Large Language Model)?
A model trained on large datasets to understand and generate human-like text.  
Examples: **BERT, LLaMA 2, Mistral, Phi-2**.  
We use them with RAG to generate **document-backed answers**.
