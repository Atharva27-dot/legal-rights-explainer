"""
legal_document.py

Defines the data structure for a legal document chunk.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class LegalDocument:
    """
    Represents one legal chunk.
    """

    id: str

    page_content: str

    metadata: Dict

    embedding: Optional[List[float]] = field(default=None)

    score: Optional[float] = None