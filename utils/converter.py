import os
import subprocess
import platform

class DocumentConverter:
    """Handle document conversion operations"""
    
    @staticmethod
    def word_to_pdf(input_path, output_path):
        """Convert Word document to PDF using LibreOffice (cross-platform)"""
        try:
            if not os.path.exists(input_path):
                raise FileNotFoundError(f"Input file not found: {input_path}")
            
            # Detect platform and use appropriate conversion method
            system = platform.system()
            
            if system == "Windows":
                # Try docx2pdf on Windows (if available)
                try:
                    from docx2pdf import convert
                    convert(input_path, output_path)
                except ImportError:
                    # Fall back to LibreOffice
                    DocumentConverter._convert_with_libreoffice(input_path, output_path)
            else:
                # Use LibreOffice on Linux/Mac
                DocumentConverter._convert_with_libreoffice(input_path, output_path)
            
            if not os.path.exists(output_path):
                raise Exception("PDF file was not created")
                
            return True
            
        except Exception as e:
            error_msg = str(e)
            
            if "libreoffice" in error_msg.lower() or "soffice" in error_msg.lower():
                raise Exception("LibreOffice is required for conversion. Please ensure it's installed on the server.")
            
            if input_path.lower().endswith('.doc'):
                raise Exception("Old .doc format not supported. Save your file as .docx in Word first.")
            
            raise Exception(f"Conversion failed: {error_msg}")
    
    @staticmethod
    def _convert_with_libreoffice(input_path, output_path):
        """Convert using LibreOffice command line"""
        output_dir = os.path.dirname(output_path)
        
        # LibreOffice command
        cmd = [
            'soffice',
            '--headless',
            '--convert-to',
            'pdf',
            '--outdir',
            output_dir,
            input_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            raise Exception(f"LibreOffice conversion failed: {result.stderr}")
        
        # LibreOffice creates file with same name but .pdf extension
        expected_output = os.path.join(output_dir, os.path.splitext(os.path.basename(input_path))[0] + '.pdf')
        
        # Rename if needed
        if expected_output != output_path and os.path.exists(expected_output):
            os.rename(expected_output, output_path)
