from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, Dict
from core.vectordb import VectorDB

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


@app.get("/health")
def health_check():
    return {"status": "ok"}
