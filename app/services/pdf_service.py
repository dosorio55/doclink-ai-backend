import os
import uuid
from PyPDF2 import PdfReader, PdfWriter
from app.utils.paths import UPLOADS_DIR

def extract_page_range(input_path: str, start_page: int, end_page: int) -> str:
    reader = PdfReader(input_path)
    n = len(reader.pages)

    if start_page < 1 or end_page < start_page or end_page > n:
        raise ValueError("Invalid page range")
    writer = PdfWriter()

    for i in range(start_page - 1, end_page):
        writer.add_page(reader.pages[i])
    out_name = f"subset_{uuid.uuid4().hex}.pdf"
    out_path = os.path.join(UPLOADS_DIR, out_name)

    with open(out_path, "wb") as f:
        writer.write(f)
        
    return out_path
