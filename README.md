# 🧠 Vector DB — Local Vector Database with API (Python)

A **lightweight, local-first Vector Database built from scratch in pure Python**, with a **FastAPI wrapper**, designed for **semantic search, RAG pipelines, and GenAI systems** — without paid APIs or heavy frameworks.

This project focuses on **fundamentals, explainability, and reusability**, making it ideal for:
- RAG systems
- Backend + GenAI portfolios
- Interviews & system design discussions

---

## 🚀 Why This Project Exists

Most vector databases hide the internals behind complex abstractions.  
This project answers a simple but powerful question:

> **“How does a vector database actually work under the hood?”**

By building everything from scratch, this project demonstrates:
- How text is converted into vectors
- How similarity search works (cosine similarity)
- How embeddings evolve dynamically
- How a vector DB is exposed safely via an API
- How it plugs directly into RAG systems

---

## 🎯 Project Goals

- Build a **true vector database engine**, not a wrapper
- Keep everything **local, free, and framework-light**
- Maintain **clear separation of concerns**
- Make the system **RAG-ready out of the box**
- Ensure **interview-ready explanations**

---

## 🧱 High-Level Architecture

```text
Client / RAG System / Scraper
↓
FastAPI API
↓
Vector DB Engine
↓
TF-IDF Embeddings + Similarity
↓
vectors.json
```


---

## 📂 Project Structure

```yaml
vector_db/
│
├── core/
│ ├── storage.py # Disk persistence (JSON)
│ ├── tfidf.py # TF-IDF embedding engine
│ └── vectordb.py # Vector DB core logic
│
├── data/
│ └── vectors.json # Stored vectors
│
├── cli.py # CLI wrapper (manual testing)
├── api.py # FastAPI wrapper (production use)
└── README.md
```


---

## 🧩 Core Components

### 1️⃣ Vector DB Engine (`vectordb.py`)
- Inserts text + metadata
- Converts text → TF-IDF vectors
- Performs cosine similarity search
- Supports delete operations
- Automatically adapts to new data

**Responsibility:**  
Semantic retrieval (Retriever in RAG).

---

### 2️⃣ Embedding Layer (`tfidf.py`)
- Pure-Python TF-IDF implementation
- Corpus-aware embeddings
- Dynamically re-fits on new inserts

**Why TF-IDF?**
- Fully local
- Explainable
- Interview-friendly
- Strong baseline before neural embeddings

---

### 3️⃣ Storage Layer (`storage.py`)
- JSON-based persistence
- Human-readable & debuggable
- No database magic

---

### 4️⃣ API Layer (`api.py`)
- FastAPI wrapper
- Input validation
- Proper HTTP status codes
- Swagger UI support

**Responsibility:**  
Expose Vector DB safely to other systems.

---

## ✅ Features

### Vector DB Core
- Text → Vector (TF-IDF)
- Cosine similarity search
- Top-K retrieval
- Metadata support
- Persistent storage

### API
- `POST /insert` → add new text
- `POST /search` → semantic search
- `DELETE /delete` → remove record
- `GET /health` → health check
- Input validation & error handling

---

## ❌ Intentionally Not Included

To keep the system clean and reusable:

- No SQL
- No joins or schemas
- No neural embeddings (yet)
- No cloud services
- No paid APIs
- No RAG generation logic

> **This project is the Retriever, not the Generator.**

---

## ▶️ How to Run (WSL / Linux)

```bash
python3 -m venv env
source env/bin/activate
pip install fastapi uvicorn
uvicorn api:app --reload
```
Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## 🔌 How This Is Used in RAG

This Vector DB fits directly into a RAG pipeline:

1️⃣ Ingestion

- Chunk documents (PDF, web, text)
- Call POST /insert for each chunk

2️⃣ Retrieval
- User query → POST /search
- Get top-K relevant chunks

## 3️⃣ Generation (External)

- Pass retrieved chunks to any LLM
- Generate final answer
- RAG Flow:
  - User Query → Vector DB (/search) → Context → LLM → Answer
- 👉 No changes needed in this DB to support RAG.

## 🧪 Testing

- CLI testing via cli.py
- API testing via Swagger UI
- Dynamic insert/search/delete
- Corpus-aware TF-IDF validation

## 🧠 Key Learnings

- Vector DBs are about math + similarity, not tables
- Embeddings can be built incrementally
- API and engine must stay separate
- TF-IDF is a powerful, explainable baseline
- A clean Retriever is enough for RAG

## 📌 Project Status

✅ Vector DB Engine — Complete
✅ CLI Wrapper — Complete
✅ API Wrapper — Complete
✅ RAG-Ready — Yes

## 🔜 Future (Optional):

- Neural embeddings
- Scraper integration
- Full RAG demo

## 📄 License

MIT — free to use, learn, and extend.