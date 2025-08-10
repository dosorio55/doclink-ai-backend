import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from app.utils.paths import UPLOADS_DIR, PROCESSED_DIR

def allowed_file(filename: str, allowed_exts) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_exts

def save_upload(file_storage):
    original = secure_filename(file_storage.filename)

    date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    uid = str(uuid.uuid4())
    save_name = f"{uid}_{date}_{original}"
    save_path = os.path.join(UPLOADS_DIR, save_name)
    file_storage.save(save_path)

    return {'path': save_path, 'uuid': uid, 'date': date, 'original': original}

def write_processed(markdown_content: str, meta: dict, base_name: str | None = None):
    base_original = base_name if base_name else meta['original'].rsplit('.', 1)[0]
    base_original = secure_filename(base_original)

    filename = f"{base_original}_{meta['date']}.md"

    path = os.path.join(PROCESSED_DIR, filename)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    return {'path': path, 'filename': filename}

def list_processed_files():
    items = []
    for filename in os.listdir(PROCESSED_DIR):
        if not filename.endswith('.md'):
            continue
        parts = filename.split('_', 2)
        if len(parts) < 3:
            continue
        file_id = parts[0]
        remainder = parts[2]
        original_name = remainder.rsplit('.', 1)[0]
        items.append({'id': file_id, 'filename': filename, 'original_name': original_name})
    return items

def find_processed_by_id(file_id: str):
    for filename in os.listdir(PROCESSED_DIR):
        if filename.startswith(f"{file_id}_") and filename.endswith('.md'):
            return os.path.join(PROCESSED_DIR, filename), filename
    return None, None
