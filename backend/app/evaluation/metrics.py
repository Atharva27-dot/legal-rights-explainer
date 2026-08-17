"""
Evaluation metrics for legal retrieval.

Supports:
- multiple relevant sections
- subsection-aware matching
- Precision@K
- Recall@K
- Hit@K
- Reciprocal Rank
- MRR
"""

import re


# ================================================================
# NORMALIZATION
# ================================================================

def normalize_section(section):
    """
    Normalize section strings.

    Example:

        Section 2(7)
        section 2(7)

    both become:

        section 2(7)
    """

    if not section:
        return ""

    return re.sub(
        r"\s+",
        " ",
        str(section).strip().lower()
    )


# ================================================================
# SECTION MATCHING
# ================================================================

def section_matches(
    retrieved_section,
    expected_section
):
    """
    Determine whether a retrieved legal section matches
    an expected legal provision.

    Exact match:
        Section 43 == Section 43

    Parent-section match:
        Section 2(7) belongs to Section 2

    We intentionally DO NOT allow:
        Section 2(7) == Section 2(25)
    """

    retrieved = normalize_section(
        retrieved_section
    )

    expected = normalize_section(
        expected_section
    )

    if not retrieved or not expected:
        return False

    # Exact match
    if retrieved == expected:
        return True

    # Parent section relationship.
    #
    # Example:
    # expected = section 2
    # retrieved = section 2(7)
    #
    # This is relevant because Section 2 is the parent
    # section containing the subsection.
    if re.fullmatch(
        r"section\s+\d+[a-z]?",
        expected
    ):

        if retrieved.startswith(
            expected + "("
        ):

            return True

    return False


# ================================================================
# EXTRACT RETRIEVED SECTIONS
# ================================================================

def get_retrieved_sections(
    results,
    k=None
):

    if k is not None:

        results = results[:k]

    sections = []

    for item in results:

        metadata = item.get(
            "metadata",
            {}
        )

        section = metadata.get(
            "section",
            ""
        )

        if section:

            sections.append(
                section
            )

    return sections


# ================================================================
# RELEVANCE CHECK
# ================================================================

def is_relevant(
    retrieved_section,
    expected_sections
):

    for expected in expected_sections:

        if section_matches(
            retrieved_section,
            expected
        ):

            return True

    return False


# ================================================================
# PRECISION @ K
# ================================================================

def precision_at_k(
    results,
    expected_sections,
    k=3
):

    retrieved_sections = (
        get_retrieved_sections(
            results,
            k
        )
    )

    if not retrieved_sections:

        return 0.0

    relevant_count = sum(

        1

        for section in retrieved_sections

        if is_relevant(
            section,
            expected_sections
        )

    )

    return (
        relevant_count
        /
        len(retrieved_sections)
    )


# ================================================================
# RECALL @ K
# ================================================================

def recall_at_k(
    results,
    expected_sections,
    k=3
):

    retrieved_sections = (
        get_retrieved_sections(
            results,
            k
        )
    )

    if not expected_sections:

        return 0.0

    matched_expected = set()

    for expected in expected_sections:

        for retrieved in retrieved_sections:

            if section_matches(
                retrieved,
                expected
            ):

                matched_expected.add(
                    expected
                )

                break

    return (
        len(matched_expected)
        /
        len(expected_sections)
    )


# ================================================================
# HIT @ K
# ================================================================

def hit_at_k(
    results,
    expected_sections,
    k=3
):

    return int(

        recall_at_k(
            results,
            expected_sections,
            k
        ) > 0

    )


# ================================================================
# RECIPROCAL RANK
# ================================================================

def reciprocal_rank(
    results,
    expected_sections
):

    for rank, item in enumerate(
        results,
        start=1
    ):

        section = item.get(
            "metadata",
            {}
        ).get(
            "section",
            ""
        )

        if is_relevant(
            section,
            expected_sections
        ):

            return 1 / rank

    return 0.0


# ================================================================
# MEAN RECIPROCAL RANK
# ================================================================

def mean_reciprocal_rank(
    values
):

    if not values:

        return 0.0

    return (
        sum(values)
        /
        len(values)
    )


# ================================================================
# AVERAGE
# ================================================================

def average(values):

    if not values:

        return 0.0

    return (
        sum(values)
        /
        len(values)
    )