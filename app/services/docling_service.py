from docling.document_converter import DocumentConverter
import os
from app.utils.paths import CACHE_DIR

def convert_to_markdown(file_path: str) -> str:
    try:
        os.environ['DOCLING_CACHE_DIR'] = CACHE_DIR
        converter = DocumentConverter()
        result = converter.convert(file_path)
        return result.document.export_to_markdown()
    except Exception as e:
        print(f'Conversion failed: {str(e)}')
        raise e
