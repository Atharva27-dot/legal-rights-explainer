from app.rag.pdf_loader import PDFLoader
from app.rag.preprocessor import TextPreprocessor
from app.rag.chunker import LegalChunker
from pathlib import Path

loader = PDFLoader()
preprocessor = TextPreprocessor()
chunker = LegalChunker()

pdf_folder = Path("data")

# Search recursively in all subfolders
pdf_files = list(pdf_folder.rglob("*.pdf"))

if not pdf_files:
    raise FileNotFoundError("No PDF found inside data folder.")

print("Found PDF:", pdf_files[0])

text = loader.load_pdf(str(pdf_files[0]))

if not pdf_files:
    raise FileNotFoundError("No PDF found inside data folder.")

text = loader.load_pdf(str(pdf_files[0]))
text = preprocessor.clean_text(text)

chunks = chunker.split_into_chunks(
    text,
    "Consumer_Protection_Act_2019"
)

print("Total Chunks:", len(chunks))

print("\nFirst Chunk Metadata:\n")

for chunk in chunks[:5]:

    print("=" * 80)

    from pprint import pprint

    pprint(chunk.metadata)

    print()

    print(chunk.page_content[:300])

    print("\n")