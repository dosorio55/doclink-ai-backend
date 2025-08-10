from flask import Blueprint, request, jsonify
from app.services.storage_service import allowed_file, save_upload, write_processed
from app.services.docling_service import convert_to_markdown
from app.config import Config
import os
from app.services.pdf_service import extract_page_range

uploads_bp = Blueprint('uploads', __name__)

@uploads_bp.route('/upload', methods=['POST'])
def upload_file():
    custom_name = request.args.get('new-filename')
    start = request.args.get('start-page', type=int)
    end = request.args.get('end-page', type=int)
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    if not allowed_file(file.filename, Config.ALLOWED_EXTENSIONS):
        return jsonify({'error': 'Invalid file type. Only PDF files are allowed.'}), 400
        
    try:

        print('Saving upload...')
        meta = save_upload(file)
        source_path = meta['path']
        subset_path = None
        if start is not None and end is not None:
            print(f'Extracting page range from pages {start} to {end}')
            subset_path = extract_page_range(source_path, start, end)

            print(f'Extracted page range to {subset_path}')
            source_path = subset_path

        print('Converting to markdown...')
        markdown = convert_to_markdown(source_path)

        print('Writing processed file...')
        processed = write_processed(markdown, meta, base_name=custom_name, page_range=f'{start}-{end}' if start and end else None)

        if subset_path and os.path.exists(subset_path):
            os.remove(subset_path)

        if os.path.exists(meta['path']):
            os.remove(meta['path'])

        print('Cleanup complete')
            
        return jsonify({
            'success': True,
            'processed_file_id': meta['uuid'],
            'original_filename': meta['original'],
            'processed_filename': processed['filename']
        })
    except Exception as e:
        print(f'Processing failed: {str(e)}')
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500
