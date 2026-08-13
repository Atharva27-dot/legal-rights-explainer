"""
pipeline.py

Complete Legal Document Ingestion Pipeline
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

        self.preprocessor = TextPreprocessor()

        self.chunker = LegalChunker()

        self.embedder = EmbeddingGenerator()

        self.vector_store = LegalVectorStore()


    def ingest(self, pdf_path):

        pdf_path = Path(pdf_path)

        print("\nLoading PDF...")

        raw_text = self.loader.load_pdf(str(pdf_path))

        print("Cleaning Text...")

        clean_text = self.preprocessor.clean_text(raw_text)

        print("Creating Chunks...")

        chunks = self.chunker.split_into_chunks(
            clean_text,
            pdf_path.name
        )

        print("Generating Embeddings...")

        texts = [chunk.page_content for chunk in chunks]

        embeddings = self.embedder.generate_embeddings(texts)

        print("Saving into ChromaDB...")

        self.vector_store.add_chunks(
            chunks,
            embeddings
        )

        print()

        print("Pipeline Finished Successfully.")

        print(f"Stored {len(chunks)} chunks.")


if __name__ == "__main__":

    BASE_DIR = Path(__file__).resolve().parents[2]

    pdf = BASE_DIR / "data" / "pdfs" / "consumer_protection_act_2019.pdf"

    pipeline = LegalRAGPipeline()

    pipeline.ingest(pdf)