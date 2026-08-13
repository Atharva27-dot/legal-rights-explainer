"""
Evaluation metrics for retrieval.
"""


def precision_at_k(results, expected_section):

    retrieved = [
        item["metadata"]["section"]
        for item in results
    ]

    correct = sum(
        1
        for section in retrieved
        if section == expected_section
    )

    return correct / len(results)


def recall(results, expected_section):

    retrieved = [
        item["metadata"]["section"]
        for item in results
    ]

    return 1 if expected_section in retrieved else 0


def reciprocal_rank(results, expected_section):

    for rank, item in enumerate(results, start=1):

        if item["metadata"]["section"] == expected_section:

            return 1 / rank

    return 0