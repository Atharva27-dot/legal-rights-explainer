"""
Ground-truth evaluation dataset for the Legal Rights Explainer.

The dataset contains multiple legal domains and allows multiple
relevant provisions for questions where more than one provision
can reasonably answer the query.
"""

TEST_QUERIES = [

    # ============================================================
    # CONSUMER PROTECTION
    # ============================================================

    {
        "id": "consumer_01",
        "query": "What is a consumer?",
        "domain": "Consumer Protection",
        "issue_type": "Consumer Definition",

        # Section 2 contains multiple definitions.
        # Section 2(7) is the definition of consumer.
        "expected_sections": [
            "Section 2(7)"
        ]
    },

    {
        "id": "consumer_02",
        "query": "Who can file a consumer complaint?",
        "domain": "Consumer Protection",
        "issue_type": "Filing Complaint",

        "expected_sections": [
            "Section 35"
        ]
    },

    {
        "id": "consumer_03",
        "query": "What is mediation under consumer protection law?",
        "domain": "Consumer Protection",
        "issue_type": "Mediation",

        # Section 2(25) defines mediation.
        # Section 79 deals with mediation proceedings/cell.
        "expected_sections": [
            "Section 2(25)",
            "Section 79"
        ]
    },

    {
        "id": "consumer_04",
        "query": "What are consumer rights?",
        "domain": "Consumer Protection",
        "issue_type": "Consumer Rights",

        # Section 2 contains definitions, while Section 17
        # concerns complaints relating to violation of consumer
        # rights. We allow both relevant areas.
        "expected_sections": [
            "Section 2",
            "Section 17"
        ]
    },

    {
        "id": "consumer_05",
        "query": (
            "I purchased a defective phone and the seller "
            "is refusing to replace it or refund my money."
        ),
        "domain": "Consumer Protection",
        "issue_type": "Defective Product",

        "expected_sections": [
            "Section 39",
            "Section 2(10)"
        ]
    },

    # ============================================================
    # CYBER / IT
    # ============================================================

    {
        "id": "cyber_01",
        "query": (
            "Someone accessed my Google Pay account and "
            "transferred money without my permission."
        ),
        "domain": "Cyber / IT",
        "issue_type": "UPI Fraud",

        "expected_sections": [
            "Section 43"
        ]
    },

    {
        "id": "cyber_02",
        "query": (
            "Someone accessed my computer system without "
            "my permission and caused loss."
        ),
        "domain": "Cyber / IT",
        "issue_type": "Unauthorized Access",

        "expected_sections": [
            "Section 43"
        ]
    },

    {
        "id": "cyber_03",
        "query": (
            "Someone fraudulently used my password and "
            "identity information."
        ),
        "domain": "Cyber / IT",
        "issue_type": "Identity Theft",

        "expected_sections": [
            "Section 66C"
        ]
    },

    {
        "id": "cyber_04",
        "query": (
            "I became a victim of online fraud involving "
            "unauthorized electronic transactions."
        ),
        "domain": "Cyber / IT",
        "issue_type": "Online Payment Fraud",

        "expected_sections": [
            "Section 43",
            "Section 66C",
            "Section 66D"
        ]
    }
]


if __name__ == "__main__":

    print("=" * 70)
    print("LEGAL RETRIEVAL EVALUATION DATASET")
    print("=" * 70)

    print(
        "Total test cases:",
        len(TEST_QUERIES)
    )

    print()

    for test in TEST_QUERIES:

        print(
            test["id"],
            "|",
            test["domain"],
            "|",
            test["issue_type"]
        )

        print(
            "Expected:",
            ", ".join(
                test["expected_sections"]
            )
        )