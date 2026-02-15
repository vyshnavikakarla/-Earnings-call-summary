import fitz
import pytesseract
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(path):
    text = ""

    # Try normal extraction
    doc = fitz.open(path)
    for page in doc:
        text += page.get_text("text")
    doc.close()

    # If very little text → use OCR
    if len(text.strip()) < 500:
        print("Switching to OCR...")
        text = ""
        pages = convert_from_path(
            path,
            poppler_path=r"C:\Release-25.12.0-0\poppler-25.12.0\Library\bin"
        )

        for page in pages:
            text += pytesseract.image_to_string(page)

    return text
