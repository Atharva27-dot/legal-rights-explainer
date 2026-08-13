from pathlib import Path

from pdf_loader import PDFLoader
from preprocessor import TextPreprocessor
from chunker import LegalChunker
from embedder import EmbeddingGenerator
from vector_store import LegalVectorStore

BASE_DIR = Path(__file__).resolve().parents[2]

pdf_name = "consumer_protection_act_2019.pdf"

pdf_path = BASE_DIR / "data" / "pdfs" / pdf_name

loader = PDFLoader()
preprocessor = TextPreprocessor()
chunker = LegalChunker()
embedder = EmbeddingGenerator()
vector_store = LegalVectorStore()

print("Loading PDF...")
raw_text = loader.load_pdf(str(pdf_path))

print("Cleaning...")
clean_text = preprocessor.clean_text(raw_text)

print("Chunking...")
chunks = chunker.split_into_chunks(clean_text, pdf_name)

print("Generating embeddings...")
texts = [chunk["text"] for chunk in chunks]

embeddings = embedder.generate_embeddings(texts)

print("Saving to ChromaDB...")
vector_store.add_chunks(chunks, embeddings)

print()

print("Total Documents in Database:")

print(vector_store.count())