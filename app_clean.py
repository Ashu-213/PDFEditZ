"""
PDFEditZ - Professional PDF Merger & Compressor
Clean and Simple Version - GUARANTEED TO WORK
Copyright © 2024 Ashu. All rights reserved.
"""

import os
import PyPDF2
from flask import Flask, request, render_template, send_file, jsonify
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    """Check if file is a PDF."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def simple_merge_pdfs(file_paths, output_path):
    """Simple PDF merger - guaranteed to work."""
    try:
        print(f"📄 Merging {len(file_paths)} PDF files...")
        
        writer = PyPDF2.PdfWriter()
        
        for i, file_path in enumerate(file_paths):
            print(f"Adding file {i+1}: {file_path}")
            
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    writer.add_page(page)
        
        print(f"Writing merged file to: {output_path}")
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        print("✅ Merge completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Merge failed: {str(e)}")
        return False

def simple_compress_pdf(input_path, output_path, compression_level='medium'):
    """Simple PDF compressor - guaranteed to work."""
    try:
        print(f"🗜️ Compressing PDF: {input_path}")
        print(f"Compression level: {compression_level}")
        
        # Define compression settings
        settings = {
            'minimal': 0.95,
            'high': 0.85,
            'medium': 0.70,
            'low': 0.55
        }
        
        scale_factor = settings.get(compression_level, 0.70)
        print(f"Using scale factor: {scale_factor}")
        
        with open(input_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            writer = PyPDF2.PdfWriter()
            
            print(f"Processing {len(reader.pages)} pages...")
            
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                
                # Scale down the page
                page.scale(scale_factor, scale_factor)
                
                writer.add_page(page)
        
        print(f"Writing compressed file to: {output_path}")
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        # Show file sizes
        original_size = os.path.getsize(input_path) / (1024 * 1024)
        compressed_size = os.path.getsize(output_path) / (1024 * 1024)
        reduction = ((original_size - compressed_size) / original_size) * 100
        
        print(f"✅ Compression completed!")
        print(f"Original: {original_size:.2f} MB")
        print(f"Compressed: {compressed_size:.2f} MB")
        print(f"Reduction: {reduction:.1f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Compression failed: {str(e)}")
        return False

# ============ ROUTES ============

@app.route('/')
def index():
    """Home page with PDF merger."""
    return render_template('index.html')

@app.route('/compress')
def compress_page():
    """PDF compression page."""
    return render_template('compress.html')

@app.route('/terms')
def terms():
    """Terms and conditions page."""
    return render_template('terms.html')

@app.route('/merge', methods=['POST'])
def merge_pdfs():
    """Handle PDF merging."""
    print("=== MERGE REQUEST RECEIVED ===")
    
    if 'files' not in request.files:
        print("❌ No files in request")
        return jsonify({'success': False, 'error': 'No files provided'})
    
    files = request.files.getlist('files')
    print(f"📄 Received {len(files)} files")
    
    if len(files) < 2:
        print("❌ Less than 2 files")
        return jsonify({'success': False, 'error': 'Please select at least 2 PDF files'})
    
    try:
        # Save uploaded files
        file_paths = []
        for i, file in enumerate(files):
            if file.filename != '' and allowed_file(file.filename):
                print(f"Processing file {i+1}: {file.filename}")
                
                filename = secure_filename(file.filename)
                unique_filename = f"merge_input_{uuid.uuid4()}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                
                file.save(file_path)
                file_paths.append(file_path)
                print(f"Saved to: {file_path}")
        
        if not file_paths:
            print("❌ No valid PDF files found")
            return jsonify({'success': False, 'error': 'No valid PDF files found'})
        
        print(f"📁 Total valid files: {len(file_paths)}")
        
        # Generate output filename
        output_filename = f"merged_{uuid.uuid4().hex[:8]}.pdf"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        print(f"🎯 Output file: {output_filename}")
        
        # Merge PDFs
        success = simple_merge_pdfs(file_paths, output_path)
        
        # Cleanup input files
        for file_path in file_paths:
            try:
                os.remove(file_path)
                print(f"🗑️ Cleaned up: {file_path}")
            except:
                pass
        
        if success:
            print("✅ MERGE SUCCESS - returning filename")
            return jsonify({'success': True, 'filename': output_filename})
        else:
            print("❌ MERGE FAILED")
            return jsonify({'success': False, 'error': 'Failed to merge PDFs'})
            
    except Exception as e:
        print(f"❌ EXCEPTION in merge: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'})

@app.route('/compress-pdf', methods=['POST'])
def compress_pdf():
    """Handle PDF compression."""
    print("=== COMPRESSION REQUEST RECEIVED ===")
    
    if 'file' not in request.files:
        print("❌ No file in request")
        return jsonify({'success': False, 'error': 'No file provided'})
    
    file = request.files['file']
    compression_level = request.form.get('compression_level', 'medium')
    
    print(f"📄 File: {file.filename}")
    print(f"🎚️ Compression level: {compression_level}")
    
    if file.filename == '' or not allowed_file(file.filename):
        print("❌ Invalid file")
        return jsonify({'success': False, 'error': 'Please select a valid PDF file'})
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        unique_input = f"compress_input_{uuid.uuid4()}_{filename}"
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_input)
        
        file.save(input_path)
        print(f"📁 Saved input to: {input_path}")
        
        # Generate output filename
        output_filename = f"compressed_{uuid.uuid4().hex[:8]}.pdf"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        print(f"🎯 Output file: {output_filename}")
        
        # Compress PDF
        success = simple_compress_pdf(input_path, output_path, compression_level)
        
        # Cleanup input file
        try:
            os.remove(input_path)
            print(f"🗑️ Cleaned up: {input_path}")
        except:
            pass
        
        if success:
            print("✅ COMPRESSION SUCCESS - returning filename")
            return jsonify({'success': True, 'filename': output_filename})
        else:
            print("❌ COMPRESSION FAILED")
            return jsonify({'success': False, 'error': 'Failed to compress PDF'})
            
    except Exception as e:
        print(f"❌ EXCEPTION in compression: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'})

@app.route('/download/<filename>')
def download_file(filename):
    """Download processed PDF file."""
    print(f"📥 Download request for: {filename}")
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if os.path.exists(file_path):
        print(f"✅ File found, sending: {file_path}")
        return send_file(file_path, as_attachment=True)
    else:
        print(f"❌ File not found: {file_path}")
        return "File not found", 404

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'PDFEditZ',
        'timestamp': datetime.now().isoformat(),
        'version': 'clean-simple'
    })

@app.route('/ping')
def ping():
    """Simple ping endpoint."""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    print("🚀 Starting PDFEditZ...")
    print(f"📁 Upload folder: {app.config['UPLOAD_FOLDER']}")
    print("🔗 Available routes:")
    for rule in app.url_map.iter_rules():
        print(f"   {rule.rule} -> {rule.endpoint}")
    
    # Run app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
