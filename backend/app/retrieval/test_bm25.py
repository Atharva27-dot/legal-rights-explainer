from app.rag.retriever import LegalRetriever
from app.retrieval.bm25_retriever import BM25Retriever

retriever = LegalRetriever()

results = retriever.search("consumer", top_k=50)

documents = results["documents"][0]

bm25 = BM25Retriever(documents)

query = input("Question: ")

ranked = bm25.search(query)

for index, score in ranked:

    print("=" * 60)
    print("Score:", score)
    print(documents[index][:500])