# src/rag/rag_engine.py

from .document_loader import DocumentLoader
from .vector_store import VectorStore


class RAGEngine:
    def __init__(self):
        self.loader = DocumentLoader()
        self.store = VectorStore()

    def build_index(self):
        docs = self.loader.load_all_documents()
        self.store.add_documents(docs)

    def retrieve(self, query, top_k=5):
        return self.store.search(query, top_k)
