import os
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, Dict
from core.vectordb import VectorDB
from core.loaders import load_pdf, load_txt, load_md
from core.chunker import chunk_text
from fastapi import UploadFile, File, Query
import shutil


app = FastAPI(
    title="Vector DB API",
    description="Hardened API wrapper over custom Vector Database",
    version="1.1"
)

db = VectorDB()


# Request Models (validated)


class InsertRequest(BaseModel):
    text: str = Field(..., min_length=3, description="Text to embed")
    metadata: Optional[Dict] = Field(default_factory=dict)

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = Field(default=3, ge=1, le=20)

class DeleteRequest(BaseModel):
    id: str = Field(..., min_length=5)


# Routes


@app.post("/insert", status_code=status.HTTP_201_CREATED)
def insert_vector(req: InsertRequest):
    try:
        record_id = db.insert(req.text, req.metadata)
        return {
            "status": "success",
            "id": record_id
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Insert failed: {str(e)}"
        )


@app.post("/search")
def search_vector(req: SearchRequest):
    try:
        results = db.search(req.query, top_k=req.top_k)

        return {
            "query": req.query,
            "count": len(results),
            "results": [
                {
                    "score": score,
                    "id": record["id"],
                    "text": record["text"],
                    "metadata": record["metadata"]
                }
                for score, record in results
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )


@app.delete("/delete", status_code=status.HTTP_200_OK)
def delete_vector(req: DeleteRequest):
    try:
        db.delete(req.id)
        return {
            "status": "delete attempted",
            "id": req.id
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Delete failed: {str(e)}"
        )

@app.post("/ingest-file")
def ingest_file(
    file: UploadFile = File(...),
    save: bool = Query(default=False, description="Save file for re-indexing")
):
    ext = os.path.splitext(file.filename)[1].lower()
    raw = file.file.read()

    # decide storage path
    if save:
        os.makedirs("data/uploads", exist_ok=True)
        stored_path = f"data/uploads/{file.filename}"
        with open(stored_path, "wb") as f:
            f.write(raw)
        path_for_processing = stored_path
    else:
        path_for_processing = None  # temp / memory

    # load text
    if ext == ".txt":
        text = raw.decode("utf-8", errors="ignore")

    elif ext == ".md":
        text = raw.decode("utf-8", errors="ignore")
        from markdown import markdown
        import re
        text = re.sub("<[^<]+?>", "", markdown(text))

    elif ext == ".pdf":
        temp = path_for_processing or f"/tmp/{file.filename}"
        if not path_for_processing:
            with open(temp, "wb") as f:
                f.write(raw)
        text = load_pdf(temp)

    else:
        raise HTTPException(400, "Unsupported file type")

    chunks = chunk_text(text)

    for i, chunk in enumerate(chunks):
        db.insert(chunk, {
            "source": file.filename,
            "stored": save,
            "chunk_id": i
        })

    return {
        "status": "success",
        "chunks_added": len(chunks),
        "stored": save
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}
