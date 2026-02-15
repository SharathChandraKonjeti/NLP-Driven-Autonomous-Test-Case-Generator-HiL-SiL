# src/rag/vector_store.py

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class VectorStore:
    def __init__(self, embedding_model="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(embedding_model)
        self.index = None
        self.documents = []

    def add_documents(self, docs):
        """
        docs = list of {"text": "...", "source": "..."}
        """
        self.documents.extend(docs)

        embeddings = self.model.encode([d["text"] for d in docs], convert_to_numpy=True)

        dim = embeddings.shape[1]

        if self.index is None:
            self.index = faiss.IndexFlatL2(dim)

        self.index.add(embeddings)

    def search(self, query, top_k=5):
        query_emb = self.model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_emb, top_k)

        results = []
        for idx in indices[0]:
            if idx < len(self.documents):
                results.append(self.documents[idx])

        return results
