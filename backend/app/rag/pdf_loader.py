from pathlib import Path
import fitz


class PDFLoader:

    def load_pdf(self, pdf_path):

        doc = fitz.open(pdf_path)

        text = ""

        for page in doc:
            text += page.get_text()

        return text


if __name__ == "__main__":

    BASE_DIR = Path(__file__).resolve().parents[2]

    pdf_path = BASE_DIR / "data" / "pdfs" / "consumer_protection_act_2019.pdf"

    loader = PDFLoader()

    text = loader.load_pdf(str(pdf_path))

    print(text[:3000])