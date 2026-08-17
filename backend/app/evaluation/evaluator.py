"""
Legal Retrieval Evaluation

Compares:

BASELINE
    Original query
    -> Embedding
    -> ChromaDB
    -> Top-K

PROPOSED
    Domain
    -> Issue
    -> Issue-aware query expansion
    -> Semantic retrieval
    -> Hybrid ranking
    -> Top-K

Metrics:
    Precision@3
    Recall@3
    Hit@3
    MRR
"""

import json
import time
import chromadb

from app.rag.embedder import EmbeddingGenerator
from app.rag.retriever import LegalRetriever
from app.retrieval.hybrid_ranker import HybridRanker

from app.evaluation.metrics import (
    precision_at_k,
    recall_at_k,
    hit_at_k,
    reciprocal_rank,
    average
)

from app.evaluation.test_queries import TEST_QUERIES


# ================================================================
# INITIALIZATION
# ================================================================

print()
print("=" * 75)
print("INITIALIZING LEGAL RETRIEVAL EVALUATION")
print("=" * 75)

embedder = EmbeddingGenerator()
retriever = LegalRetriever()
ranker = HybridRanker()

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_collection(
    "legal_documents"
)


# ================================================================
# BASELINE SEARCH
# ================================================================

def baseline_search(query, top_k=10):
    """
    Pure semantic baseline.

    Original query
        -> embedding
        -> ChromaDB
        -> Top-K
    """

    query_embedding = embedder.generate_embedding(
        query
    )

    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=top_k
    )

    formatted = []

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    distances = results.get(
        "distances",
        [[]]
    )[0]

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        formatted.append({
            "document": document,
            "metadata": metadata,
            "distance": distance,
            "semantic_score": round(
                1 / (1 + distance),
                3
            )
        })

    return formatted


# ================================================================
# RESULT STORAGE
# ================================================================

baseline_results = []
proposed_results = []


# ================================================================
# RUN EXPERIMENT
# ================================================================

for test in TEST_QUERIES:

    print()
    print("=" * 75)

    print(
        "TEST:",
        test["id"]
    )

    print(
        "Domain:",
        test["domain"]
    )

    print(
        "Issue:",
        test["issue_type"]
    )

    print(
        "Query:",
        test["query"]
    )

    print(
        "Expected:",
        test["expected_sections"]
    )

    expected_sections = test[
        "expected_sections"
    ]


    # ============================================================
    # BASELINE
    # ============================================================

    baseline_start = time.perf_counter()

    baseline = baseline_search(
        test["query"],
        top_k=10
    )

    baseline_time = (
        time.perf_counter()
        -
        baseline_start
    )


    # ============================================================
    # PROPOSED
    # ============================================================

    proposed_start = time.perf_counter()

    raw_results = retriever.search(
        test["query"],
        top_k=10,
        domain=test["domain"],
        issue_type=test["issue_type"]
    )

    proposed = ranker.rank(
    test["query"],
    raw_results,
    requested_domain=test["domain"],
    issue_type=test["issue_type"]
)

    proposed_time = (
        time.perf_counter()
        -
        proposed_start
    )


    # ============================================================
    # BASELINE METRICS
    # ============================================================

    baseline_precision = precision_at_k(
        baseline,
        expected_sections,
        k=3
    )

    baseline_recall = recall_at_k(
        baseline,
        expected_sections,
        k=3
    )

    baseline_hit = hit_at_k(
        baseline,
        expected_sections,
        k=3
    )

    baseline_rr = reciprocal_rank(
        baseline,
        expected_sections
    )


    # ============================================================
    # PROPOSED METRICS
    # ============================================================

    proposed_precision = precision_at_k(
        proposed,
        expected_sections,
        k=3
    )

    proposed_recall = recall_at_k(
        proposed,
        expected_sections,
        k=3
    )

    proposed_hit = hit_at_k(
        proposed,
        expected_sections,
        k=3
    )

    proposed_rr = reciprocal_rank(
        proposed,
        expected_sections
    )


    # ============================================================
    # STORE BASELINE
    # ============================================================

    baseline_results.append({
        "id": test["id"],
        "domain": test["domain"],
        "issue_type": test["issue_type"],
        "precision_at_3": baseline_precision,
        "recall_at_3": baseline_recall,
        "hit_at_3": baseline_hit,
        "reciprocal_rank": baseline_rr,
        "time_seconds": baseline_time
    })


    # ============================================================
    # STORE PROPOSED
    # ============================================================

    proposed_results.append({
        "id": test["id"],
        "domain": test["domain"],
        "issue_type": test["issue_type"],
        "precision_at_3": proposed_precision,
        "recall_at_3": proposed_recall,
        "hit_at_3": proposed_hit,
        "reciprocal_rank": proposed_rr,
        "time_seconds": proposed_time
    })


    # ============================================================
    # DISPLAY BASELINE TOP 3
    # ============================================================

    print()
    print("-" * 75)
    print("BASELINE TOP 3")
    print("-" * 75)

    for rank_number, item in enumerate(
        baseline[:3],
        start=1
    ):

        metadata = item.get(
            "metadata",
            {}
        )

        print(
            f"{rank_number}. "
            f"{metadata.get('section', '')} | "
            f"{metadata.get('title', '')}"
        )


    # ============================================================
    # DISPLAY PROPOSED TOP 3
    # ============================================================

    print()
    print("-" * 75)
    print("PROPOSED TOP 3")
    print("-" * 75)

    for rank_number, item in enumerate(
        proposed[:3],
        start=1
    ):

        metadata = item.get(
            "metadata",
            {}
        )

        print(
            f"{rank_number}. "
            f"{metadata.get('section', '')} | "
            f"{metadata.get('title', '')} | "
            f"Score: {item.get('final_score', 0)}"
        )


    # ============================================================
    # DISPLAY TEST METRICS
    # ============================================================

    print()
    print(
        "Baseline Precision@3:",
        round(baseline_precision, 3)
    )

    print(
        "Proposed Precision@3:",
        round(proposed_precision, 3)
    )

    print(
        "Baseline Recall@3:",
        round(baseline_recall, 3)
    )

    print(
        "Proposed Recall@3:",
        round(proposed_recall, 3)
    )

    print(
        "Baseline MRR:",
        round(baseline_rr, 3)
    )

    print(
        "Proposed MRR:",
        round(proposed_rr, 3)
    )


# ================================================================
# OVERALL METRICS
# ================================================================

baseline_precision_overall = average([
    item["precision_at_3"]
    for item in baseline_results
])

proposed_precision_overall = average([
    item["precision_at_3"]
    for item in proposed_results
])


baseline_recall_overall = average([
    item["recall_at_3"]
    for item in baseline_results
])

proposed_recall_overall = average([
    item["recall_at_3"]
    for item in proposed_results
])


baseline_hit_overall = average([
    item["hit_at_3"]
    for item in baseline_results
])

proposed_hit_overall = average([
    item["hit_at_3"]
    for item in proposed_results
])


baseline_mrr_overall = average([
    item["reciprocal_rank"]
    for item in baseline_results
])

proposed_mrr_overall = average([
    item["reciprocal_rank"]
    for item in proposed_results
])


# ================================================================
# IMPROVEMENT
# ================================================================

def percentage_improvement(
    baseline,
    proposed
):

    if baseline == 0:

        return None

    return (
        (
            proposed - baseline
        )
        /
        baseline
    ) * 100


# ================================================================
# DOMAIN-WISE RESULTS
# ================================================================

domains = sorted({
    test["domain"]
    for test in TEST_QUERIES
})

domain_results = {}


for domain in domains:

    domain_baseline = [
        item
        for item in baseline_results
        if item["domain"] == domain
    ]

    domain_proposed = [
        item
        for item in proposed_results
        if item["domain"] == domain
    ]

    domain_results[domain] = {

        "baseline": {

            "precision_at_3": average([
                item["precision_at_3"]
                for item in domain_baseline
            ]),

            "recall_at_3": average([
                item["recall_at_3"]
                for item in domain_baseline
            ]),

            "hit_at_3": average([
                item["hit_at_3"]
                for item in domain_baseline
            ]),

            "mrr": average([
                item["reciprocal_rank"]
                for item in domain_baseline
            ])

        },

        "proposed": {

            "precision_at_3": average([
                item["precision_at_3"]
                for item in domain_proposed
            ]),

            "recall_at_3": average([
                item["recall_at_3"]
                for item in domain_proposed
            ]),

            "hit_at_3": average([
                item["hit_at_3"]
                for item in domain_proposed
            ]),

            "mrr": average([
                item["reciprocal_rank"]
                for item in domain_proposed
            ])

        }

    }


# ================================================================
# FINAL RESULTS
# ================================================================

print()
print()
print("=" * 75)
print("FINAL EVALUATION RESULTS")
print("=" * 75)


print()
print("BASELINE — PURE SEMANTIC RETRIEVAL")

print(
    "Precision@3:",
    round(
        baseline_precision_overall,
        3
    )
)

print(
    "Recall@3:",
    round(
        baseline_recall_overall,
        3
    )
)

print(
    "Hit@3:",
    round(
        baseline_hit_overall,
        3
    )
)

print(
    "MRR:",
    round(
        baseline_mrr_overall,
        3
    )
)


print()
print(
    "PROPOSED — DOMAIN + ISSUE-AWARE HYBRID"
)

print(
    "Precision@3:",
    round(
        proposed_precision_overall,
        3
    )
)

print(
    "Recall@3:",
    round(
        proposed_recall_overall,
        3
    )
)

print(
    "Hit@3:",
    round(
        proposed_hit_overall,
        3
    )
)

print(
    "MRR:",
    round(
        proposed_mrr_overall,
        3
    )
)


# ================================================================
# IMPROVEMENT REPORT
# ================================================================

print()
print("IMPROVEMENT")

metrics = [

    (
        "Precision@3",
        baseline_precision_overall,
        proposed_precision_overall
    ),

    (
        "Recall@3",
        baseline_recall_overall,
        proposed_recall_overall
    ),

    (
        "Hit@3",
        baseline_hit_overall,
        proposed_hit_overall
    ),

    (
        "MRR",
        baseline_mrr_overall,
        proposed_mrr_overall
    )

]


for name, baseline_value, proposed_value in metrics:

    improvement = percentage_improvement(
        baseline_value,
        proposed_value
    )

    if improvement is None:

        print(
            f"{name}: N/A "
            "(baseline = 0)"
        )

    else:

        print(
            f"{name}: "
            f"{improvement:.2f}%"
        )


# ================================================================
# DOMAIN RESULTS
# ================================================================

print()
print("=" * 75)
print("DOMAIN-WISE RESULTS")
print("=" * 75)


for domain, values in domain_results.items():

    print()
    print(
        "DOMAIN:",
        domain
    )

    print(
        "Baseline Precision@3:",
        round(
            values["baseline"][
                "precision_at_3"
            ],
            3
        )
    )

    print(
        "Proposed Precision@3:",
        round(
            values["proposed"][
                "precision_at_3"
            ],
            3
        )
    )

    print(
        "Baseline Recall@3:",
        round(
            values["baseline"][
                "recall_at_3"
            ],
            3
        )
    )

    print(
        "Proposed Recall@3:",
        round(
            values["proposed"][
                "recall_at_3"
            ],
            3
        )
    )

    print(
        "Baseline Hit@3:",
        round(
            values["baseline"][
                "hit_at_3"
            ],
            3
        )
    )

    print(
        "Proposed Hit@3:",
        round(
            values["proposed"][
                "hit_at_3"
            ],
            3
        )
    )

    print(
        "Baseline MRR:",
        round(
            values["baseline"]["mrr"],
            3
        )
    )

    print(
        "Proposed MRR:",
        round(
            values["proposed"]["mrr"],
            3
        )
    )


# ================================================================
# SAVE JSON
# ================================================================

evaluation_output = {

    "experiment": {

        "baseline":
            "Pure semantic retrieval",

        "proposed":
            "Domain + issue-aware hybrid retrieval",

        "metrics": [
            "Precision@3",
            "Recall@3",
            "Hit@3",
            "MRR"
        ]

    },

    "overall": {

        "baseline": {

            "precision_at_3":
                baseline_precision_overall,

            "recall_at_3":
                baseline_recall_overall,

            "hit_at_3":
                baseline_hit_overall,

            "mrr":
                baseline_mrr_overall

        },

        "proposed": {

            "precision_at_3":
                proposed_precision_overall,

            "recall_at_3":
                proposed_recall_overall,

            "hit_at_3":
                proposed_hit_overall,

            "mrr":
                proposed_mrr_overall

        }

    },

    "domain_results":
        domain_results,

    "baseline_details":
        baseline_results,

    "proposed_details":
        proposed_results

}


with open(
    "evaluation_results.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        evaluation_output,
        file,
        indent=4
    )


# ================================================================
# COMPLETE
# ================================================================

print()
print(
    "Results saved to: evaluation_results.json"
)

print()
print("=" * 75)
print("EVALUATION COMPLETE")
print("=" * 75)