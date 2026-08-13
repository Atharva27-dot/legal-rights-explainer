"""
keyword_extractor.py

Lightweight keyword extractor for legal queries.
Uses only Python's standard library.
"""

import re


class KeywordExtractor:

    # Common English stop words
    STOP_WORDS = {
        "the", "is", "a", "an", "to", "of", "and", "or",
        "in", "on", "at", "for", "with", "by", "from",
        "what", "who", "how", "when", "where", "which",
        "can", "could", "should", "would", "may", "might",
        "do", "does", "did", "are", "was", "were", "be",
        "been", "being", "i", "you", "he", "she", "it",
        "we", "they", "this", "that", "these", "those",
        "my", "your", "our", "their", "me", "him", "her"
    }

    def extract(self, query: str):

        query = query.lower()

        # Keep only letters and numbers
        words = re.findall(r"\b[a-zA-Z0-9]+\b", query)

        keywords = [
            word
            for word in words
            if word not in self.STOP_WORDS and len(word) > 2
        ]

        return keywords