"""
preprocessor.py

Cleans extracted legal text before chunking.
"""

import re
import unicodedata


class TextPreprocessor:

    def clean_text(self, text: str) -> str:
        """
        Clean extracted PDF text.
        """

        # Normalize Unicode
        text = unicodedata.normalize("NFKC", text)

        # Remove page numbers (lines containing only digits)
        text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)

        # Remove tabs
        text = text.replace("\t", " ")

        # Remove multiple spaces
        text = re.sub(r' +', ' ', text)

        # Remove excessive blank lines
        text = re.sub(r'\n{3,}', '\n\n', text)

        # Remove leading/trailing whitespace
        text = text.strip()

        return text

    def clean(self, text: str) -> str:
        """
        Wrapper for backward compatibility.
        """
        return self.clean_text(text)