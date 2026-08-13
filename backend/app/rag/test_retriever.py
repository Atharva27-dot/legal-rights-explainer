from app.rag.retriever import LegalRetriever

retriever = LegalRetriever()

question = input("Ask a legal question: ")

results = retriever.search(question)

print("\n")

for i in range(len(results["documents"][0])):

    print("=" * 80)

    print(f"Result {i+1}")

    print("=" * 80)

    print()

    print(results["documents"][0][i][:800])

    print()

    print("Metadata:")

    print(results["metadatas"][0][i])

    print()