from app.retrieval.hybrid_ranker import HybridRanker
from app.rag.retriever import LegalRetriever

from app.evaluation.metrics import (
    precision_at_k,
    recall,
    reciprocal_rank
)

from app.evaluation.test_queries import TEST_QUERIES


retriever = LegalRetriever()
ranker = HybridRanker()

precision_scores = []
recall_scores = []
mrr_scores = []

for test in TEST_QUERIES:

    print("=" * 70)
    print("Question:", test["query"])

    results = retriever.search(test["query"])

    ranked = ranker.rank(test["query"], results)

    p = precision_at_k(
        ranked,
        test["expected_section"]
    )

    r = recall(
        ranked,
        test["expected_section"]
    )

    mrr = reciprocal_rank(
        ranked,
        test["expected_section"]
    )

    precision_scores.append(p)
    recall_scores.append(r)
    mrr_scores.append(mrr)

    print("Precision:", p)
    print("Recall:", r)
    print("MRR:", mrr)

print()

print("=" * 70)

print("Average Precision:", sum(precision_scores)/len(precision_scores))

print("Average Recall:", sum(recall_scores)/len(recall_scores))

print("Average MRR:", sum(mrr_scores)/len(mrr_scores))