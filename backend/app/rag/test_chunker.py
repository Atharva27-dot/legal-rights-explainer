from pathlib import Path

from app.rag.pdf_loader import PDFLoader
from app.rag.preprocessor import TextPreprocessor
from app.rag.chunker import LegalChunker

BASE_DIR = Path(__file__).resolve().parents[2]

pdf_file = "consumer_protection_act_2019.pdf"

pdf_path = BASE_DIR / "data" / "pdfs" / pdf_file

loader = PDFLoader()

preprocessor = TextPreprocessor()

chunker = LegalChunker()

raw_text = loader.load_pdf(str(pdf_path))

clean_text = preprocessor.clean_text(raw_text)

chunks = chunker.split_into_chunks(clean_text, pdf_file)

print(f"\nTotal Chunks: {len(chunks)}\n")

print("=" * 100)

print(chunks[0])