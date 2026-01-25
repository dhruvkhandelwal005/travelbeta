import pytesseract
from PIL import Image
import pdfplumber
import docx
import io

async def extract_text(file):
    content = await file.read()
    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        text = ""
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    elif filename.endswith((".png", ".jpg", ".jpeg")):
        image = Image.open(io.BytesIO(content))
        return pytesseract.image_to_string(image)

    elif filename.endswith(".docx"):
        doc = docx.Document(io.BytesIO(content))
        return "\n".join(p.text for p in doc.paragraphs)

    else:
        raise ValueError("Unsupported file format")
