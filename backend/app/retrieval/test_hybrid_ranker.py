from app.rag.retriever import LegalRetriever
from app.retrieval.hybrid_ranker import HybridRanker

retriever = LegalRetriever()
ranker = HybridRanker()

while True:

    question = input("Question: ")

    if question.lower() == "exit":
        break

    results = retriever.search(question)

    ranked = ranker.rank(question, results)

    print("\n")

    for i, item in enumerate(ranked, start=1):

        print("=" * 70)

        print(f"Rank {i}")

        print("=" * 70)

        print("Score:", item["score"])

        print("Metadata:", item["metadata"])

        print()

        print(item["document"][:400])

        print()