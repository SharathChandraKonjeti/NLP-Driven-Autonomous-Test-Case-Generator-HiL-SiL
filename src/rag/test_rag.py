from src.rag.rag_engine import RAGEngine

rag = RAGEngine()
rag.build_index()

query = "ACC must be enabled above what speed?"
results = rag.retrieve(query, top_k=3)

for r in results:
    print("\nSOURCE:", r["source"])
    print("TEXT:", r["text"])
