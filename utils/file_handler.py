import os
from werkzeug.utils import secure_filename

def allowed_file(filename, allowed_extensions):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def get_output_filename(input_filename, new_extension='pdf'):
    """Generate output filename with new extension"""
    return secure_filename(input_filename.rsplit('.', 1)[0] + f'.{new_extension}')

def cleanup_files(*file_paths):
    """Delete multiple files safely"""
    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {str(e)}")
