from flask import Blueprint, jsonify, send_file
from app.services.storage_service import list_processed_files, find_processed_by_id

files_bp = Blueprint('files', __name__)

@files_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

@files_bp.route('/files', methods=['GET'])
def list_files():
    try:
        return jsonify({'files': list_processed_files()})
    except Exception as e:
        return jsonify({'error': f'Failed to list files: {str(e)}'}), 500

@files_bp.route('/download/<file_id>', methods=['GET'])
def download_file(file_id):
    try:
        path, filename = find_processed_by_id(file_id)
        if not path:
            return jsonify({'error': 'File not found'}), 404
        return send_file(path, as_attachment=True, download_name=filename, mimetype='text/markdown')
    except Exception as e:
        return jsonify({'error': f'Download failed: {str(e)}'}), 500
