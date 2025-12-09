from docx2pdf import convert
import os

class DocumentConverter:
    """Handle document conversion operations"""
    
    @staticmethod
    def word_to_pdf(input_path, output_path):
        """Convert Word document to PDF"""
        try:
            if not os.path.exists(input_path):
                raise FileNotFoundError(f"Input file not found: {input_path}")
            
            convert(input_path, output_path)
            
            if not os.path.exists(output_path):
                raise Exception("PDF file was not created by docx2pdf")
                
            return True
            
        except Exception as e:
            error_msg = str(e)
            
            if "com_error" in error_msg.lower():
                raise Exception("Microsoft Word encountered an error. Please ensure Word is installed and the document is not corrupted.")
            
            if input_path.lower().endswith('.doc'):
                raise Exception("Old .doc format not supported. Save your file as .docx in Word first.")
            
            raise Exception(f"Conversion failed: {error_msg}")
