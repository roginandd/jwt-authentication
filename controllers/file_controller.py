import uuid
import logging
from flask import Blueprint, request, jsonify, send_file, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.file_service import save_file, update_file, delete_file
from models.uploaded_file import UploadedFile

file_bp = Blueprint('file_bp', __name__)

# 🟢 POST — Upload file (JWT required)
@file_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    try:
        current_user = get_jwt_identity()  # retrieve username from token
        if 'file' not in request.files:
            return jsonify({'message': 'No file uploaded'}), 400
        
        file = request.files['file']
        folder = f"{current_app.config['UPLOAD_FOLDER']}/{uuid.uuid4().hex}"
        uploaded = save_file(file, folder)

        return jsonify({
            'message': 'Upload successful',
            'id': uploaded.id,
            'path': uploaded.file_path,
            'uploaded_by': current_user
        }), 201
    
    except Exception as e:
        logging.error(f"Upload error: {e}")
        return jsonify({'message': str(e)}), 400


# 🟡 GET — Retrieve file info or download (JWT required)
@file_bp.route('/file/<int:file_id>', methods=['GET'])
@jwt_required()
def get_file(file_id):
    try:
        current_user = get_jwt_identity()
        file = UploadedFile.query.get(file_id)
        if not file:
            return jsonify({'message': 'File not found'}), 404
        return send_file(file.file_path, as_attachment=True)
    except Exception as e:
        logging.error(f"Get error: {e}")
        return jsonify({'message': str(e)}), 400


# 🟠 PUT — Update file (JWT required)
@file_bp.route('/file/<int:file_id>', methods=['PUT'])
@jwt_required()
def update_existing_file(file_id):
    try:
        current_user = get_jwt_identity()
        if 'file' not in request.files:
            return jsonify({'message': 'No file provided'}), 400

        file = request.files['file']
        updated = update_file(file_id, file, current_app.config['UPLOAD_FOLDER'])

        return jsonify({
            'message': 'File updated successfully',
            'path': updated.file_path,
            'updated_by': current_user
        }), 200

    except Exception as e:
        logging.error(f"Update error: {e}")
        return jsonify({'message': str(e)}), 400


# 🔴 DELETE — Delete file (JWT required)
@file_bp.route('/file/<int:file_id>', methods=['DELETE'])
@jwt_required()
def delete_existing_file(file_id):
    try:
        current_user = get_jwt_identity()
        delete_file(file_id)
        return jsonify({
            'message': 'File deleted successfully',
            'deleted_by': current_user
        }), 200
    
    except Exception as e:
        logging.error(f"Delete error: {e}")
        return jsonify({'message': str(e)}), 400
