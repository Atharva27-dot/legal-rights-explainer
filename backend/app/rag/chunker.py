"""
chunker.py

Creates LegalDocument objects using LegalParser.
"""

from app.models.legal_document import LegalDocument
from app.rag.legal_parser import LegalParser


class LegalChunker:

    def __init__(self):
        self.parser = LegalParser()
       

    def split_into_chunks(self, text: str, source_file: str):

        parsed_sections = self.parser.extract_metadata(text)

        chunks = []

        for i, section in enumerate(parsed_sections, start=1):

            chunk = LegalDocument(

                id=f"chunk_{i}",

                page_content=section["content"],

                metadata={
                    "source": source_file,
                    "chunk_number": i,
                    "act": section["act"],
                    "chapter": section["chapter"],
                    "section": section["section"],
                    "title": section["title"],
                    
                    
                }

            )

            chunks.append(chunk)

        return chunks