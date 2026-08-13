"""
intent_detector.py

Detects the legal intent of a user's question.
"""

import re


class IntentDetector:

    INTENT_PATTERNS = {
        "definition": [
            r"\bwhat is\b",
            r"\bwho is\b",
            r"\bdefine\b",
            r"\bmeaning\b"
        ],

        "rights": [
            r"\bright\b",
            r"\bentitled\b"
        ],

        "complaint": [
            r"\bcomplaint\b",
            r"\bfile\b",
            r"\breport\b"
        ],

        "documents": [
            r"\bdocument\b",
            r"\bproof\b",
            r"\brequired\b"
        ],

        "penalty": [
            r"\bpunishment\b",
            r"\bfine\b",
            r"\bpenalty\b"
        ]
    }

    def detect(self, query: str):

        query = query.lower()

        for intent, patterns in self.INTENT_PATTERNS.items():

            for pattern in patterns:

                if re.search(pattern, query):

                    return intent

        return "general"