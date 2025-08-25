"""
PDFEditZ - Professional PDF Merger & Compressor
RENDER-OPTIMIZED VERSION for Cloud Deployment
Copyright © 2024 Ashu. All rights reserved.
"""

import os
import PyPDF2
from flask import Flask, request, render_template, send_file, jsonify, redirect, url_for
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
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def compress_pdf_render_optimized(input_path, output_path, quality='medium'):
    """RENDER-OPTIMIZED compression - Maximum speed for cloud deployment."""
    try:
        original_size = os.path.getsize(input_path)
        print(f"🚀 Render-optimized compression: {original_size / (1024*1024):.2f} MB")
        
        # ULTRA-FAST compression settings optimized for Render free tier
        render_configs = {
            'minimal': {'scale': 0.95, 'remove_images': False},   # Minimal compression
            'high': {'scale': 0.92, 'remove_images': False},     # Light compression, fastest
            'medium': {'scale': 0.78, 'remove_images': False},   # Balanced compression, fast
            'low': {'scale': 0.62, 'remove_images': True},      # Good compression, moderate
            'extreme': {'scale': 0.48, 'remove_images': True}    # Maximum compression
        }
        
        config = render_configs.get(quality, render_configs['medium'])
        
        # SINGLE-PASS processing for maximum speed
        with open(input_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            writer = PyPDF2.PdfWriter()
            
            total_pages = len(reader.pages)
            print(f"⚡ Processing {total_pages} pages ({config['scale']*100:.0f}% scale)...")
            
            for i, page in enumerate(reader.pages):
                # Minimal logging for speed
                if i == 0:
                    print(f"📄 Fast processing mode active...")
                
                # Quick annotation removal
                if '/Annots' in page:
                    del page['/Annots']
                
                # Remove images only if needed (saves time)
                if config['remove_images'] and '/Resources' in page:
                    resources = page['/Resources']
                    if '/XObject' in resources:
                        del resources['/XObject']
                
                # Single scaling operation
                page.scale(config['scale'], config['scale'])
                writer.add_page(page)
            
            # Minimal metadata for fastest write
            writer.add_metadata({'/Title': 'PDFEditZ Compressed'})
            
            # Single write operation
            print(f"💾 Writing compressed file...")
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
        
        # Quick final stats
        final_size = os.path.getsize(output_path)
        reduction = ((original_size - final_size) / original_size) * 100
        
        print(f"✅ Compression complete in Render-optimized mode!")
        print(f"📊 {original_size / (1024*1024):.2f} MB → {final_size / (1024*1024):.2f} MB ({reduction:.1f}% reduction)")
        
        return True
        
    except Exception as e:
        print(f"❌ Compression failed: {e}")
        return False

def merge_pdfs_fast(file_paths, output_path):
    """FAST PDF merging optimized for Render."""
    try:
        print(f"🚀 Fast merging {len(file_paths)} PDFs...")
        
        writer = PyPDF2.PdfWriter()
        total_pages = 0
        
        for i, file_path in enumerate(file_paths):
            print(f"📄 Adding file {i+1}/{len(file_paths)}...")
            
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                pages_count = len(reader.pages)
                total_pages += pages_count
                
                # Add all pages quickly
                for page in reader.pages:
                    writer.add_page(page)
        
        # Minimal metadata
        writer.add_metadata({
            '/Title': 'PDFEditZ Merged Document',
            '/Creator': 'PDFEditZ by Ashu'
        })
        
        # Single write operation
        print(f"💾 Writing merged file ({total_pages} total pages)...")
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        final_size = os.path.getsize(output_path)
        print(f"✅ Merge complete: {final_size / (1024*1024):.2f} MB")
        
        return True
        
    except Exception as e:
        print(f"❌ Merge failed: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress')
def compress_page():
    return render_template('compress.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/merge', methods=['POST'])
def merge_pdfs_route():
    if 'files' not in request.files:
        return jsonify({'success': False, 'error': 'No files provided'})
    
    files = request.files.getlist('files')
    
    if len(files) < 2:
        return jsonify({'success': False, 'error': 'Please select at least 2 PDF files'})
    
    try:
        # Save uploaded files
        file_paths = []
        for file in files:
            if file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4()}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(file_path)
                file_paths.append(file_path)
        
        if not file_paths:
            return jsonify({'success': False, 'error': 'No valid PDF files found'})
        
        # Generate output filename
        output_filename = f"merged_{uuid.uuid4()}.pdf"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        # Fast merge
        success = merge_pdfs_fast(file_paths, output_path)
        
        # Cleanup input files
        for file_path in file_paths:
            try:
                os.remove(file_path)
            except:
                pass
        
        if success:
            return jsonify({'success': True, 'filename': output_filename})
        else:
            return jsonify({'success': False, 'error': 'Merge failed'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/compress-pdf', methods=['POST'])
def compress_pdf_route():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'})
    
    file = request.files['file']
    quality = request.form.get('compression_level', 'medium')  # Fixed: use compression_level from form
    
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Please select a valid PDF file'})
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(input_path)
        
        # Generate output filename
        output_filename = f"compressed_{uuid.uuid4()}.pdf"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        # Render-optimized compression
        success = compress_pdf_render_optimized(input_path, output_path, quality)
        
        # Cleanup input file
        try:
            os.remove(input_path)
        except:
            pass
        
        if success:
            return jsonify({'success': True, 'filename': output_filename})
        else:
            return jsonify({'success': False, 'error': 'Compression failed'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "File not found", 404

# Health check endpoints for Render monitoring
@app.route('/health')
def health_check():
    """Detailed health check with timestamp for monitoring."""
    return jsonify({
        'status': 'healthy',
        'service': 'PDFEditZ',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0-render-optimized'
    })

@app.route('/ping')
def ping():
    """Quick ping endpoint for keep-alive services."""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    # Render uses PORT environment variable
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
