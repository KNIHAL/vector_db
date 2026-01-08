import uuid
import math
from core.storage import Storage
from core.tfidf import TFIDFEmbedding


class VectorDB:
    def __init__(self, path="data/vectors.json"):
        self.storage = Storage(path)
        self.embedder = TFIDFEmbedding()
        self._rebuild_embeddings()

    # -----------------------------
    # Similarity
    # -----------------------------
    def _cosine_similarity(self, v1, v2):
        common = set(v1.keys()) & set(v2.keys())
        dot = sum(v1[x] * v2[x] for x in common)

        mag1 = math.sqrt(sum(v ** 2 for v in v1.values()))
        mag2 = math.sqrt(sum(v ** 2 for v in v2.values()))

        if mag1 == 0 or mag2 == 0:
            return 0.0

        return dot / (mag1 * mag2)

    # -----------------------------
    # Insert
    # -----------------------------
    def insert(self, text, metadata=None):
        records = self.storage.read_all()

        # TF-IDF needs full corpus
        texts = [r["text"] for r in records] + [text]
        self.embedder.fit(texts)

        record = {
            "id": str(uuid.uuid4()),
            "text": text,
            "vector": self.embedder.embed(text),
            "metadata": metadata or {}
        }

        records.append(record)
        self.storage.write_all(records)
        return record["id"]

    # -----------------------------
    # Search
    # -----------------------------
    def search(self, query, top_k=3):
        records = self.storage.read_all()

        # Fit again to current corpus
        texts = [r["text"] for r in records]
        if texts:
            self.embedder.fit(texts)

        query_vec = self.embedder.embed(query)

        scored = []
        for r in records:
            score = self._cosine_similarity(query_vec, r["vector"])
            scored.append((score, r))

        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[:top_k]

    # -----------------------------
    # Rebuild embeddings on startup
    # -----------------------------
    def _rebuild_embeddings(self):
        records = self.storage.read_all()
        texts = [r["text"] for r in records]
        if texts:
            self.embedder.fit(texts)

    # -----------------------------
    # Delete
    # -----------------------------
    def delete(self, record_id):
        records = self.storage.read_all()
        new_records = [r for r in records if r["id"] != record_id]
        self.storage.write_all(new_records)
