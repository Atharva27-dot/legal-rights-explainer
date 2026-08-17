"""
chunker.py

Creates LegalDocument objects using LegalParser.

Chunk IDs are unique per source PDF so multiple
legal Acts can coexist in ChromaDB.
"""

from pathlib import Path

from app.models.legal_document import LegalDocument
from app.rag.legal_parser import LegalParser


class LegalChunker:

    def __init__(self):

        self.parser = LegalParser()

    # ============================================================
    # SPLIT DOCUMENT INTO LEGAL CHUNKS
    # ============================================================

    def split_into_chunks(
        self,
        text: str,
        source_file: str
    ):

        parsed_sections = (
            self.parser.extract_metadata(
                text,
                source_file
            )
        )

        chunks = []

        # Remove extension and make a safe ID
        source_stem = Path(
            source_file
        ).stem

        safe_source = (
            source_stem
            .lower()
            .replace(" ", "_")
            .replace("-", "_")
        )

        for i, section in enumerate(
            parsed_sections,
            start=1
        ):

            # ====================================================
            # UNIQUE CHUNK ID
            # ====================================================

            chunk_id = (
                f"{safe_source}_chunk_{i}"
            )

            chunk = LegalDocument(

                id=chunk_id,

                page_content=
                    section["content"],

                metadata={

                    "source":
                        source_file,

                    "chunk_number":
                        i,

                    "act":
                        section["act"],

                    "domain":
                        section["domain"],

                    "chapter":
                        section["chapter"],

                    "section":
                        section["section"],

                    "title":
                        section["title"]

                }

            )

            chunks.append(chunk)

        print(
            f"{len(chunks)} chunks created "
            f"from {source_file}"
        )

        return chunks