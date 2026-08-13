from pathlib import Path

from app.rag.pdf_loader import PDFLoader
from app.rag.preprocessor import TextPreprocessor

BASE_DIR = Path(__file__).resolve().parents[2]

pdf_path = BASE_DIR / "data" / "pdfs" / "consumer_protection_act_2019.pdf"

loader = PDFLoader()
preprocessor = TextPreprocessor()

raw_text = loader.load_pdf(str(pdf_path))

clean_text = preprocessor.clean_text(raw_text)

print("=" * 80)
print("RAW TEXT")
print("=" * 80)
print(raw_text[:1500])

print("\n\n")

print("=" * 80)
print("CLEANED TEXT")
print("=" * 80)
print(clean_text[:1500])