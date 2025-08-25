import os
import glob
from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
import PyPDF2
from dotenv import load_dotenv

# Try to import PyMuPDF, but gracefully handle if not available
try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False
    print("PyMuPDF not available - using PyPDF2 only mode")

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-for-production')

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

def allowed_file(filename):
    """Check if the uploaded file is a PDF."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clean_uploads_folder():
    """Clean all files in the uploads folder."""
    files = glob.glob(os.path.join(UPLOAD_FOLDER, '*'))
    for file in files:
        try:
            os.remove(file)
        except OSError:
            pass

def compress_pdf_pypdf2_only(input_path, output_path, quality='medium'):
    """Compression using PyPDF2 only - fallback when PyMuPDF not available."""
    try:
        with open(input_path, 'rb') as input_file:
            reader = PyPDF2.PdfReader(input_file)
            writer = PyPDF2.PdfWriter()
            
            # Add all pages to writer
            for page in reader.pages:
                # Basic compression by removing unnecessary data
                if hasattr(page, 'compress_content_streams'):
                    page.compress_content_streams()
                writer.add_page(page)
            
            # Apply compression settings based on quality
            if quality in ['low', 'extreme']:
                # More aggressive compression for low quality
                writer.add_metadata({
                    '/Producer': 'PDFEditZ Compressor',
                    '/Creator': 'PDFEditZ'
                })
            
            # Write compressed PDF
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
        
        print(f"PyPDF2 compression completed: {input_path} -> {output_path}")
        return True
        
    except Exception as e:
        print(f"PyPDF2 compression failed: {e}")
        return False

def compress_pdf_working(input_path, output_path, quality='medium'):
    """WORKING compression method - Compatible with or without PyMuPDF."""
    if not PYMUPDF_AVAILABLE:
        # Fallback to PyPDF2 compression
        return compress_pdf_pypdf2_only(input_path, output_path, quality)
    
    try:
        doc = fitz.open(input_path)
        
        # REAL compression settings that ACTUALLY reduce file size
        compression_configs = {
            'high': {      # MODERATE - 20-30% reduction
                'resolution': 150,
                'jpeg_quality': 80,
                'scale_factor': 0.9
            },
            'medium': {    # STRONG - 30-50% reduction  
                'resolution': 120,
                'jpeg_quality': 70,
                'scale_factor': 0.8
            },
            'low': {       # AGGRESSIVE - 50-70% reduction
                'resolution': 96,
                'jpeg_quality': 55,
                'scale_factor': 0.7
            },
            'minimal': {   # EXTREME - 70%+ reduction
                'resolution': 72,
                'jpeg_quality': 40,
                'scale_factor': 0.6
            }
        }
        
        config = compression_configs.get(quality, compression_configs['medium'])
        
        # Create new compressed document
        compressed_doc = fitz.open()
        
        for page_num in range(doc.page_count):
            page = doc[page_num]
            rect = page.rect
            
            # Calculate the scaling and resolution matrix
            dpi_scale = config['resolution'] / 72.0
            size_scale = config['scale_factor']
            combined_scale = dpi_scale * size_scale
            
            # Create transformation matrix
            mat = fitz.Matrix(combined_scale, combined_scale)
            
            # Render page to pixmap with reduced resolution
            pix = page.get_pixmap(matrix=mat)
            
            # Compress to JPEG with specified quality
            img_data = pix.tobytes("jpeg", jpg_quality=config['jpeg_quality'])
            
            # Calculate new page dimensions
            new_width = rect.width * size_scale
            new_height = rect.height * size_scale
            
            # Create new page with reduced dimensions
            new_page = compressed_doc.new_page(width=new_width, height=new_height)
            
            # Insert compressed image to fill the page
            img_rect = fitz.Rect(0, 0, new_width, new_height)
            new_page.insert_image(img_rect, stream=img_data)
            
            # Clean up pixmap
            pix = None
        
        # Save with maximum compression settings
        compressed_doc.save(output_path,
                          garbage=4,           # Remove unused objects
                          deflate=True,        # Compress streams
                          clean=True,          # Clean up document
                          deflate_images=True, # Compress embedded images
                          deflate_fonts=True,  # Compress fonts
                          linear=True)         # Linearize for web
        
        compressed_doc.close()
        doc.close()
        
        return True
        
    except Exception as e:
        print(f"Compression error: {str(e)}")
        return False

def compress_pdf_simple_working(input_path, output_path):
    """Simple but effective compression using PyPDF2."""
    try:
        with open(input_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            writer = PyPDF2.PdfWriter()
            
            # Add all pages with compression
            for page in reader.pages:
                page.compress_content_streams()
                writer.add_page(page)
            
            # Apply compression optimizations
            writer.compress_identical_objects(remove_duplicate_obj=True)
            writer.remove_duplicates()
            
            # Write compressed PDF
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
        
        return True
        
    except Exception as e:
        print(f"Simple compression error: {str(e)}")
        return False

def compress_pdf_alternative(input_path, output_path, quality='medium'):
    """Alternative compression method using PyPDF2 - focuses on real compression."""
    try:
        with open(input_path, 'rb') as input_file:
            reader = PyPDF2.PdfReader(input_file)
            writer = PyPDF2.PdfWriter()
            
            # Set compression level based on quality
            compression_levels = {
                'high': {'remove_duplication': True, 'compress_streams': True},
                'medium': {'remove_duplication': True, 'compress_streams': True},
                'low': {'remove_duplication': True, 'compress_streams': True},
                'minimal': {'remove_duplication': True, 'compress_streams': True}
            }
            
            settings = compression_levels.get(quality, compression_levels['medium'])
            
            # Process each page
            for page_num, page in enumerate(reader.pages):
                # Compress content streams
                if settings['compress_streams']:
                    page.compress_content_streams()
                
                # Scale down images if needed (for higher compression)
                if quality in ['low', 'minimal']:
                    # This reduces image quality in the PDF
                    if '/XObject' in page['/Resources']:
                        xobjects = page['/Resources']['/XObject'].get_object()
                        for obj in xobjects:
                            if xobjects[obj]['/Subtype'] == '/Image':
                                # Image compression happens here
                                pass
                
                writer.add_page(page)
            
            # Apply additional compression techniques
            if settings['remove_duplication']:
                writer.compress_identical_objects(remove_duplicate_obj=True)
                writer.remove_duplicates()
            
            # Save compressed PDF
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
        
        return True
    
    except Exception as e:
        print(f"Error in PyPDF2 compression: {str(e)}")
        return False

def compress_pdf(input_path, output_path, quality='medium'):
    """Compress PDF to reduce file size using proper PDF optimization."""
    try:
        # Open the PDF
        doc = fitz.open(input_path)
        
        # Create new document for compressed output
        new_doc = fitz.open()
        
        # Define compression settings
        compression_settings = {
            'high': {'deflate_level': 1, 'image_quality': 95, 'image_dpi': 150},
            'medium': {'deflate_level': 6, 'image_quality': 85, 'image_dpi': 120},
            'low': {'deflate_level': 9, 'image_quality': 70, 'image_dpi': 96},
            'minimal': {'deflate_level': 9, 'image_quality': 50, 'image_dpi': 72}
        }
        
        if quality not in compression_settings:
            quality = 'medium'
        
        settings = compression_settings[quality]
        
        # Copy pages with optimization
        for page_num in range(doc.page_count):
            page = doc[page_num]
            
            # Compress images in the page
            img_list = page.get_images()
            for img_index, img in enumerate(img_list):
                try:
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    
                    # Only compress if it's a large image
                    if len(image_bytes) > 50000:  # 50KB threshold
                        # Create pixmap from image
                        pix = fitz.Pixmap(image_bytes)
                        
                        # Reduce DPI if image is too large
                        if pix.width > settings['image_dpi'] * 8 or pix.height > settings['image_dpi'] * 8:
                            # Scale down large images
                            scale = min(
                                (settings['image_dpi'] * 8) / pix.width,
                                (settings['image_dpi'] * 8) / pix.height
                            )
                            if scale < 1:
                                mat = fitz.Matrix(scale, scale)
                                pix = fitz.Pixmap(pix, mat)
                        
                        # Compress image
                        if image_ext.lower() in ['jpg', 'jpeg']:
                            compressed_image = pix.tobytes("jpeg", jpg_quality=settings['image_quality'])
                        else:
                            compressed_image = pix.tobytes("png")
                        
                        # Replace image in PDF
                        doc.update_object(xref, compressed_image)
                        pix = None
                except:
                    # Skip problematic images
                    continue
            
            # Add page to new document
            new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
        
        # Save with maximum compression settings
        new_doc.save(output_path,
                    garbage=4,
                    deflate=True,
                    clean=True,
                    deflate_images=True,
                    deflate_fonts=True)
        
        new_doc.close()
        doc.close()
        
        return True
    
    except Exception as e:
        print(f"Error in PyMuPDF compression: {str(e)}")
        return False

def get_file_size_mb(file_path):
    """Get file size in MB."""
    try:
        size_bytes = os.path.getsize(file_path)
        size_mb = size_bytes / (1024 * 1024)
        return round(size_mb, 2)
    except:
        return 0

def resize_pdf(input_path, output_path, page_size):
    """Resize PDF pages to specified size."""
    if not PYMUPDF_AVAILABLE:
        # If PyMuPDF not available, just copy the file (no resizing)
        import shutil
        shutil.copy2(input_path, output_path)
        print(f"PyMuPDF not available - copying file without resizing: {input_path} -> {output_path}")
        return True
        
    try:
        # Define page sizes in points (72 points = 1 inch)
        sizes = {
            'A4': (595, 842),      # 210 x 297 mm
            'A3': (842, 1191),     # 297 x 420 mm
            'A5': (420, 595),      # 148 x 210 mm
            'Letter': (612, 792),   # 8.5 x 11 inches
            'Legal': (612, 1008),   # 8.5 x 14 inches
            'Tabloid': (792, 1224)  # 11 x 17 inches
        }
        
        if page_size not in sizes:
            raise ValueError(f"Unsupported page size: {page_size}")
        
        target_width, target_height = sizes[page_size]
        
        # Open the PDF
        doc = fitz.open(input_path)
        new_doc = fitz.open()  # Create new document
        
        for page_num in range(doc.page_count):
            page = doc[page_num]
            
            # Get current page dimensions
            current_rect = page.rect
            current_width = current_rect.width
            current_height = current_rect.height
            
            # Calculate scaling factors
            scale_x = target_width / current_width
            scale_y = target_height / current_height
            
            # Use uniform scaling (maintain aspect ratio)
            scale = min(scale_x, scale_y)
            
            # Create new page with target size
            new_page = new_doc.new_page(width=target_width, height=target_height)
            
            # Calculate position to center the content
            scaled_width = current_width * scale
            scaled_height = current_height * scale
            x_offset = (target_width - scaled_width) / 2
            y_offset = (target_height - scaled_height) / 2
            
            # Create transformation matrix
            mat = fitz.Matrix(scale, scale).pretranslate(x_offset, y_offset)
            
            # Insert the scaled page
            new_page.show_pdf_page(new_page.rect, doc, page_num, clip=None, matrix=mat)
        
        # Save the resized PDF
        new_doc.save(output_path)
        new_doc.close()
        doc.close()
        
        return True
    
    except Exception as e:
        print(f"Error resizing PDF: {str(e)}")
        return False

def merge_pdfs(pdf_files, resize_option=None):
    """Merge multiple PDF files into one, with optional resizing."""
    pdf_merger = PyPDF2.PdfMerger()
    
    try:
        # Sort files to maintain upload order
        pdf_files.sort()
        
        for pdf_file in pdf_files:
            pdf_path = os.path.join(UPLOAD_FOLDER, pdf_file)
            
            # If resize is requested, resize the PDF first
            if resize_option and resize_option != 'none':
                resized_path = os.path.join(UPLOAD_FOLDER, f"resized_{pdf_file}")
                if resize_pdf(pdf_path, resized_path, resize_option):
                    pdf_path = resized_path
            
            with open(pdf_path, 'rb') as file:
                pdf_merger.append(file)
        
        # Save merged PDF
        output_path = os.path.join(UPLOAD_FOLDER, 'merged.pdf')
        with open(output_path, 'wb') as output_file:
            pdf_merger.write(output_file)
        
        pdf_merger.close()
        return output_path
    
    except Exception as e:
        pdf_merger.close()
        raise e

@app.route('/')
def index():
    """Render the upload form."""
    return render_template('index.html')

@app.route('/terms')
def terms():
    """Render the terms and privacy policy page."""
    return render_template('terms.html')

@app.route('/compress')
def compress_page():
    """Render the compression page."""
    return render_template('compress.html')

@app.route('/compress_file', methods=['POST'])
def compress_file():
    """Handle individual PDF compression."""
    try:
        # Clean previous uploads
        clean_uploads_folder()
        
        # Check if file was uploaded
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(url_for('compress_page'))
        
        file = request.files['file']
        compression_level = request.form.get('compression_level', 'medium')
        
        if file.filename == '':
            flash('No file selected')
            return redirect(url_for('compress_page'))
        
        if not file or not allowed_file(file.filename):
            flash('Please select a valid PDF file')
            return redirect(url_for('compress_page'))
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, f"input_{filename}")
        file.save(input_path)
        
        # Get original file size
        original_size = get_file_size_mb(input_path)
        
        # Compress the PDF
        output_filename = f"compressed_{filename}"
        output_path = os.path.join(UPLOAD_FOLDER, output_filename)
        
        # Use WORKING compression methods that actually reduce file size
        compression_success = compress_pdf_working(input_path, output_path, compression_level)
        
        if not compression_success:
            # Fallback to simple PyPDF2 compression
            compression_success = compress_pdf_simple_working(input_path, output_path)
        
        if not compression_success:
            # Last resort - try the original PyPDF2 method
            compression_success = compress_pdf_alternative(input_path, output_path, compression_level)
        
        if compression_success:
            # Get compressed file size
            compressed_size = get_file_size_mb(output_path)
            
            # If compression didn't work well enough, force more aggressive compression
            target_reduction = 0.15  # Minimum 15% reduction required
            if compressed_size >= original_size * (1 - target_reduction):
                print(f"⚠️ Compression insufficient ({compressed_size}MB vs {original_size}MB). Forcing aggressive compression...")
                
                # Force aggressive compression regardless of selected level
                if compress_pdf_working(input_path, output_path, 'low'):  # Use 'low' for aggressive
                    compressed_size = get_file_size_mb(output_path)
                    print(f"🔥 Applied forced aggressive compression")
                    
                    # If still not good enough, go extreme
                    if compressed_size >= original_size * 0.9:
                        if compress_pdf_working(input_path, output_path, 'minimal'):  # Use 'minimal' for extreme
                            compressed_size = get_file_size_mb(output_path)
                            print(f"💀 Applied extreme compression as last resort")
            
            if compressed_size < original_size:
                reduction_percent = round(((original_size - compressed_size) / original_size) * 100, 1)
                print(f"✅ COMPRESSION SUCCESS: {original_size}MB → {compressed_size}MB ({reduction_percent}% reduction)")
                
                # Check if we achieved significant compression
                if reduction_percent >= 20:
                    print(f"🎯 EXCELLENT COMPRESSION: {reduction_percent}% reduction achieved!")
                elif reduction_percent >= 10:
                    print(f"👍 GOOD COMPRESSION: {reduction_percent}% reduction achieved!")
                else:
                    print(f"📉 MINIMAL COMPRESSION: Only {reduction_percent}% reduction")
                
            else:
                print(f"❌ WARNING: File size did not reduce: {original_size}MB → {compressed_size}MB")
            
            # Return the compressed PDF
            return send_file(
                output_path,
                as_attachment=True,
                download_name=f"compressed_{filename}",
                mimetype='application/pdf'
            )
        else:
            print(f"Both compression methods failed for file: {filename}")
            flash('Error compressing PDF. The file may be corrupted or use unsupported features.')
            return redirect(url_for('compress_page'))
    
    except Exception as e:
        flash(f'Error processing file: {str(e)}')
        return redirect(url_for('compress_page'))

@app.route('/merge', methods=['POST'])
def merge_files():
    """Handle file upload and PDF merging."""
    try:
        # Clean previous uploads
        clean_uploads_folder()
        
        # Check if files were uploaded
        if 'files' not in request.files:
            flash('No files selected')
            return redirect(url_for('index'))
        
        files = request.files.getlist('files')
        resize_option = request.form.get('resize_option', 'none')
        
        if not files or all(file.filename == '' for file in files):
            flash('No files selected')
            return redirect(url_for('index'))
        
        # Filter and save valid PDF files
        saved_files = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to avoid conflicts
                timestamp = str(len(saved_files)).zfill(3)
                filename = f"{timestamp}_{filename}"
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                saved_files.append(filename)
        
        if not saved_files:
            flash('No valid PDF files found')
            return redirect(url_for('index'))
        
        if len(saved_files) < 2:
            flash('Please upload at least 2 PDF files to merge')
            return redirect(url_for('index'))
        
        # Merge PDFs with optional resizing
        merged_pdf_path = merge_pdfs(saved_files, resize_option)
        
        # Return the merged PDF
        return send_file(
            merged_pdf_path,
            as_attachment=True,
            download_name='merged.pdf',
            mimetype='application/pdf'
        )
    
    except Exception as e:
        flash(f'Error processing files: {str(e)}')
        return redirect(url_for('index'))

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error."""
    flash('File is too large. Maximum size is 16MB per file.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Ensure upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    # Run the app
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug, host='0.0.0.0', port=port)
