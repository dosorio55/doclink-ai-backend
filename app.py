from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from docling.document_converter import DocumentConverter
import os
import sys
import uuid
from werkzeug.utils import secure_filename
from pathlib import Path
import easyocr

app = Flask(__name__)
CORS(app)

def get_application_path():
    """Get the base path for the application in both dev and executable environments"""
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle (PyInstaller)
        return os.path.dirname(sys.executable)
    else:
        # If running in development mode
        return os.path.dirname(os.path.abspath(__file__))

# Set up paths relative to the application base path
BASE_PATH = get_application_path()
UPLOAD_FOLDER = os.path.join(BASE_PATH, 'uploads')
PROCESSED_FOLDER = os.path.join(BASE_PATH, 'processed')
ALLOWED_EXTENSIONS = {'pdf'}

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            unique_id = str(uuid.uuid4())
            file_path = os.path.join(UPLOAD_FOLDER, f"{unique_id}_{filename}")
            file.save(file_path)
            
            # Configure Docling to use a cache directory within our application path
            os.environ['DOCLING_CACHE_DIR'] = os.path.join(BASE_PATH, 'docling_cache')
            
            converter = DocumentConverter()
            result = converter.convert(file_path)
            markdown_content = result.document.export_to_markdown()
            
            processed_filename = f"{unique_id}_{filename.rsplit('.', 1)[0]}.md"
            processed_path = os.path.join(PROCESSED_FOLDER, processed_filename)
            
            with open(processed_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            os.remove(file_path)
            
            return jsonify({
                'success': True,
                'processed_file_id': unique_id,
                'original_filename': filename,
                'processed_filename': processed_filename
            })
            
        except Exception as e:
            print(f"Error processing file: {str(e)}")
            return jsonify({'error': f'Processing failed: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file type. Only PDF files are allowed.'}), 400

@app.route('/files', methods=['GET'])
def list_files():
    try:
        files = []
        for filename in os.listdir(PROCESSED_FOLDER):
            if filename.endswith('.md'):
                file_id = filename.split('_')[0]
                original_name = '_'.join(filename.split('_')[1:]).rsplit('.', 1)[0]
                files.append({
                    'id': file_id,
                    'filename': filename,
                    'original_name': original_name
                })
        return jsonify({'files': files})
    except Exception as e:
        print(f"Error listing files: {str(e)}")
        return jsonify({'error': f'Failed to list files: {str(e)}'}), 500

@app.route('/download/<file_id>', methods=['GET'])
def download_file(file_id):
    try:
        for filename in os.listdir(PROCESSED_FOLDER):
            if filename.startswith(file_id):
                file_path = os.path.join(PROCESSED_FOLDER, filename)
                return send_file(
                    file_path,
                    as_attachment=True,
                    download_name=filename,
                    mimetype='text/markdown'
                )
        
        return jsonify({'error': 'File not found'}), 404
    
    except Exception as e:
        print(f"Error downloading file: {str(e)}")
        return jsonify({'error': f'Download failed: {str(e)}'}), 500

if __name__ == '__main__':
    # Create cache directory for Docling models
    docling_cache_dir = os.path.join(BASE_PATH, 'docling_cache')
    os.makedirs(docling_cache_dir, exist_ok=True)
    os.environ['DOCLING_CACHE_DIR'] = docling_cache_dir
    
    # Log paths for debugging
    print(f"Application base path: {BASE_PATH}")
    print(f"Upload folder: {UPLOAD_FOLDER}")
    print(f"Processed folder: {PROCESSED_FOLDER}")
    print(f"Docling cache: {docling_cache_dir}")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
