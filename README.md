# 🧠 Vector DB — Local Vector Database with CLI & API (Python)

A **production-style, local-first Vector Database built from scratch in pure Python**, with **CLI and FastAPI wrappers**, designed for **semantic search, document ingestion, and RAG pipelines** — without paid APIs, cloud services, or heavy frameworks.

This project focuses on **fundamentals, explainability, and real-world usability**, making it suitable for:
- RAG backends
- GenAI / Backend portfolios
- System design & interview discussions

---

## 🚀 Why This Project Exists

Most vector databases abstract away the internals behind black-box tooling.  
This project was built to answer one core question:

> **“How does a vector database actually work under the hood?”**

By implementing everything from scratch, this project demonstrates:
- How documents are converted into vectors
- How similarity search works using cosine similarity
- How embeddings evolve dynamically with new data
- How document ingestion (PDF / MD / TXT) works in practice
- How a vector database plugs directly into RAG systems

---

## 🎯 Project Goals

- Build a **real vector database engine**, not a wrapper
- Keep everything **local, free, and framework-light**
- Maintain **clean separation of concerns**
- Support **document ingestion (not just toy text input)**
- Be **RAG-ready out of the box**
- Stay **interview-explainable**

---

## 🧱 High-Level Architecture

```text
CLI / API / RAG System
↓
Ingestion Layer
(PDF / MD / TXT → Chunks)
↓
Vector DB Engine
(TF-IDF + Similarity)
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
│ ├── vectordb.py # Vector DB core logic
│ ├── loaders.py # PDF / MD / TXT loaders
│ └── chunker.py # Text chunking logic
│
├── data/
│ ├── vectors.json # Stored vectors
│ └── uploads/ # Optional persisted source files
│
├── cli.py # CLI interface
├── api.py # FastAPI wrapper
└── README.md
```


---

## 🧩 Core Components

### 1️⃣ Vector DB Engine (`vectordb.py`)
- Inserts text + metadata
- Converts text → TF-IDF vectors
- Performs cosine similarity search
- Supports delete operations
- Automatically adapts when new data is added

**Role:** Retriever (RAG terminology)

---

### 2️⃣ Embedding Layer (`tfidf.py`)
- Pure-Python TF-IDF implementation
- Corpus-aware embeddings
- Re-fits dynamically on ingestion

**Why TF-IDF?**
- Fully local
- Explainable
- Lightweight
- Strong baseline before neural embeddings

---

### 3️⃣ Storage Layer (`storage.py`)
- JSON-based persistence
- Human-readable & debuggable
- No hidden magic

---

### 4️⃣ Ingestion Layer (`loaders.py`, `chunker.py`)
- Supports **PDF, Markdown, and Text files**
- Extracts text
- Splits into overlapping chunks
- Each chunk stored as an independent vector

This is what makes the project **non-toy** and production-relevant.

---

### 5️⃣ API Layer (`api.py`)
- FastAPI-based wrapper
- Input validation & proper status codes
- File ingestion endpoint
- Swagger UI for testing

---

## ✅ Features

### Vector DB Core
- Text → Vector (TF-IDF)
- Cosine similarity search
- Top-K retrieval
- Metadata support
- Persistent storage

### CLI
- Insert text
- Search vectors
- Delete by ID
- Ingest PDF / MD / TXT files
- Optional file persistence (`data/uploads/`)

### API
- `POST /insert` → insert raw text
- `POST /search` → semantic search
- `POST /ingest-file` → document ingestion
- `DELETE /delete` → remove vector
- `GET /health` → health check

---

## ❌ Intentionally Not Included

To keep the system focused and explainable:

- No SQL
- No joins or schemas
- No cloud services
- No paid APIs
- No neural embeddings (yet)
- No LLM generation logic

> **This project is the Retriever, not the Generator.**

---

## ▶️ How to Run (WSL / Linux)

```bash
python3 -m venv env
source env/bin/activate
pip requirements.txt
uvicorn api:app --reload
```
Swagger UI:

```text
http://127.0.0.1:8000/docs
```

### 🧪 Testing

**CLI**

```text
python cli.py
```

- Ingest PDF / MD / TXT using local paths
- Search content semantically
- Verify chunk metadata

**API**

- Test /ingest-file via Swagger
- Search ingested documents
- Restart server → data persists


## 🔌 How This Is Used in RAG

This Vector DB plugs directly into a RAG pipeline:

1️⃣ Ingestion

- Chunk documents
- Store via CLI or /ingest-file

2️⃣ Retrieval

- User query → /search
- Top-K relevant chunks returned

3️⃣ Generation (External)

- Retrieved chunks passed to an LLM
- Answer generated outside this system

**Flow:**

```text
User Query → Vector DB → Context → LLM → Answer

```
👉 No changes required in this DB to support RAG.

## 🧠 Key Learnings

- Vector databases are about math + similarity, not tables
- Document ingestion is essential for real RAG systems
- Chunking is as important as embeddings
- Clean separation of engine, CLI, and API matters
- TF-IDF is a strong, explainable foundation


## Status: FROZEN (v1.0)
 🔜 Future (Optional, Not Required)
- Neural embeddings
- Scraper-based ingestion
- Full RAG demo

## 📄 License

MIT — free to use, learn, and extend.
