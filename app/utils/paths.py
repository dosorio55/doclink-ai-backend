import os
import sys


def get_application_path() -> str:
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

BASE_PATH = (
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
    )
)
UPLOADS_DIR = os.path.join(BASE_PATH, 'uploads')
PROCESSED_DIR = os.path.join(BASE_PATH, 'processed')
CACHE_DIR = os.path.join(BASE_PATH, 'docling_cache')

os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)
