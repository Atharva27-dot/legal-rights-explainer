"""
pipeline.py

Multi-document Legal RAG ingestion pipeline.

Automatically processes every PDF present in:

backend/data/pdfs/

Example:

consumer_protection_act_2019.pdf
information_technology_act_2000.pdf
"""

from pathlib import Path

from app.rag.pdf_loader import PDFLoader
from app.rag.preprocessor import TextPreprocessor
from app.rag.chunker import LegalChunker
from app.rag.embedder import EmbeddingGenerator
from app.rag.vector_store import LegalVectorStore


class LegalRAGPipeline:

    def __init__(self):

        self.loader = PDFLoader()

        self.preprocessor = (
            TextPreprocessor()
        )

        self.chunker = LegalChunker()

        self.embedder = (
            EmbeddingGenerator()
        )

        self.vector_store = (
            LegalVectorStore()
        )

    # ============================================================
    # INGEST SINGLE PDF
    # ============================================================

    def ingest(self, pdf_path):

        pdf_path = Path(pdf_path)

        print()
        print("=" * 60)
        print(
            f"INGESTING: {pdf_path.name}"
        )
        print("=" * 60)

        # --------------------------------------------------------
        # LOAD PDF
        # --------------------------------------------------------

        print("\nLoading PDF...")

        raw_text = (
            self.loader.load_pdf(
                str(pdf_path)
            )
        )

        # --------------------------------------------------------
        # CLEAN TEXT
        # --------------------------------------------------------

        print("Cleaning Text...")

        clean_text = (
            self.preprocessor.clean_text(
                raw_text
            )
        )

        # --------------------------------------------------------
        # CREATE LEGAL CHUNKS
        # --------------------------------------------------------

        print("Creating Legal Chunks...")

        chunks = (
            self.chunker.split_into_chunks(
                clean_text,
                pdf_path.name
            )
        )

        if not chunks:

            print(
                "WARNING: No legal sections "
                "were extracted."
            )

            return 0

        # --------------------------------------------------------
        # GENERATE EMBEDDINGS
        # --------------------------------------------------------

        print(
            f"Generating embeddings for "
            f"{len(chunks)} chunks..."
        )

        texts = [
            chunk.page_content
            for chunk in chunks
        ]

        embeddings = (
            self.embedder.generate_embeddings(
                texts
            )
        )

        # --------------------------------------------------------
        # STORE IN CHROMADB
        # --------------------------------------------------------

        print("Saving into ChromaDB...")

        self.vector_store.add_chunks(
            chunks,
            embeddings
        )

        print()
        print(
            f"Successfully stored "
            f"{len(chunks)} chunks."
        )

        return len(chunks)

    # ============================================================
    # INGEST ALL PDF FILES
    # ============================================================

    def ingest_all(self, pdf_directory):

        pdf_directory = Path(
            pdf_directory
        )

        pdf_files = sorted(
            pdf_directory.glob("*.pdf")
        )

        if not pdf_files:

            print(
                "ERROR: No PDF files found in:"
            )

            print(
                pdf_directory
            )

            return

        print()
        print("=" * 60)
        print("MULTI-DOMAIN LEGAL RAG INGESTION")
        print("=" * 60)

        print(
            f"PDF directory: {pdf_directory}"
        )

        print(
            f"Documents found: {len(pdf_files)}"
        )

        for pdf in pdf_files:

            print(
                f"  - {pdf.name}"
            )

        print("=" * 60)

        total_chunks = 0

        # --------------------------------------------------------
        # PROCESS EACH PDF
        # --------------------------------------------------------

        for pdf_path in pdf_files:

            try:

                count = self.ingest(
                    pdf_path
                )

                total_chunks += count

            except Exception as e:

                print()
                print(
                    f"ERROR processing "
                    f"{pdf_path.name}:"
                )

                print(e)

        # --------------------------------------------------------
        # FINAL SUMMARY
        # --------------------------------------------------------

        print()
        print("=" * 60)
        print("INGESTION COMPLETE")
        print("=" * 60)

        print(
            f"Documents processed: "
            f"{len(pdf_files)}"
        )

        print(
            f"Total chunks stored: "
            f"{total_chunks}"
        )

        print(
            f"ChromaDB count: "
            f"{self.vector_store.count()}"
        )

        print("=" * 60)


# ================================================================
# MAIN
# ================================================================

if __name__ == "__main__":

    BASE_DIR = (
        Path(__file__)
        .resolve()
        .parents[2]
    )

    PDF_DIRECTORY = (
        BASE_DIR /
        "data" /
        "pdfs"
    )

    pipeline = LegalRAGPipeline()

    pipeline.ingest_all(
        PDF_DIRECTORY
    )