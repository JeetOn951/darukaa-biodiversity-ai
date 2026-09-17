from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer
from app.data.knowledge import KNOWLEDGE

DB_PATH = Path(__file__).resolve().parents[2] / "chroma_db"

class KnowledgeStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=str(DB_PATH))
        self.collection = self.client.get_or_create_collection(
            name="environmental_knowledge",
            metadata={"description": "Darukaa biodiversity scientific knowledge base"}
        )
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self._seed()

    def _seed(self):
        existing = self.collection.count()
        if existing >= len(KNOWLEDGE):
            return
        ids = [f"doc_{i}" for i in range(len(KNOWLEDGE))]
        texts = [x["text"] for x in KNOWLEDGE]
        embeddings = self.model.encode(texts, normalize_embeddings=True).tolist()
        self.collection.upsert(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=[
                {"title": x["title"], "source": x["source"], "url": x["url"], "topics": ", ".join(x["topics"])}
                for x in KNOWLEDGE
            ],
        )

    def search(self, query: str, k: int = 5):
        emb = self.model.encode([query], normalize_embeddings=True).tolist()
        result = self.collection.query(query_embeddings=emb, n_results=k)
        docs = result.get("documents", [[]])[0]
        metas = result.get("metadatas", [[]])[0]
        distances = result.get("distances", [[]])[0]
        return [
            {"text": d, "title": m["title"], "source": m["source"], "url": m["url"], "distance": float(distances[i])}
            for i, (d, m) in enumerate(zip(docs, metas))
        ]
