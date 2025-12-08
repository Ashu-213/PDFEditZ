from flask import Blueprint, render_template, request, send_file, current_app
from io import BytesIO
import os
import time
from werkzeug.utils import secure_filename
from utils import allowed_file, get_output_filename, cleanup_files, DocumentConverter

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/convert', methods=['POST'])
def convert_file():
    input_path = output_path = None
    
    try:
        if 'file' not in request.files or request.files['file'].filename == '':
            return 'No file selected', 400
        
        file = request.files['file']
        
        if not allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
            return 'Invalid file type. Please upload a .docx file.', 400
        
        # Create temporary files
        timestamp = str(int(time.time() * 1000))
        filename = secure_filename(file.filename)
        input_path = os.path.join(current_app.config['UPLOAD_FOLDER'], f"temp_{timestamp}_{filename}")
        output_path = os.path.join(current_app.config['UPLOAD_FOLDER'], f"temp_{timestamp}_{get_output_filename(filename, 'pdf')}")
        
        # Save and convert
        file.save(input_path)
        DocumentConverter.word_to_pdf(input_path, output_path)
        
        # Read to memory and cleanup
        with open(output_path, 'rb') as pdf_file:
            pdf_data = pdf_file.read()
        
        cleanup_files(input_path, output_path)
        
        # Send from memory
        return send_file(
            BytesIO(pdf_data),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=get_output_filename(filename, 'pdf')
        )
        
    except Exception as e:
        cleanup_files(input_path, output_path)
        return f'Error: {str(e)}', 500
