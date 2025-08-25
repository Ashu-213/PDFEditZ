# 🎯 PDFEditZ - Professional PDF Management Tool

[![Flask](https://img.shields.io/badge/Flask-2.3.3-blue.svg)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

**PDFEditZ** is a modern, professional web application for comprehensive PDF management. Built with Flask and featuring a sleek gradient design, it provides powerful tools for merging and compressing PDF documents with ease.

## ✨ Features

### 📄 **PDF Merger**
- Upload multiple PDF files simultaneously
- Merge PDFs in upload order with drag-and-drop reordering
- Preserve document quality and formatting
- Support for various page sizes and orientations

### 🗜️ **PDF Compression** 
- **4 Compression Levels**: High, Medium, Low, and Extreme
- Guaranteed file size reduction using advanced algorithms
- Individual file processing for upload limit compliance
- Smart compression with fallback methods

### 📐 **Page Resizing**
- Standardize PDF pages to common formats:
  - **A-Series**: A3, A4, A5
  - **US Letter Sizes**: Letter, Legal, Tabloid
- Maintain aspect ratio during resizing
- Batch processing support

### 🎨 **Professional Interface**
- Modern gradient design with PDFEditZ branding
- Responsive layout for desktop and mobile
- Tabbed navigation between features
- Real-time file size display
- Progress indicators and status updates

## 🚀 Quick Start

### Prerequisites
- Python 3.6 or higher
- 50MB free disk space
- Modern web browser

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/pdfeditz.git
   cd pdfeditz
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and set your own SECRET_KEY
   # Generate a new key with: python -c "import secrets; print(secrets.token_hex(32))"
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```

5. **Open your browser:**
   ```
   http://localhost:5000
   ```

## 📋 Dependencies

```
Flask==2.3.3
PyPDF2==3.0.1
PyMuPDF==1.23.8
Werkzeug==2.3.7
```

## 🔧 Configuration

### Environment Variables
- `FLASK_ENV`: Set to `development` for debug mode
- `SECRET_KEY`: Change the secret key for production deployment
- `MAX_CONTENT_LENGTH`: Adjust maximum file upload size (default: 16MB)

### File Upload Limits
- Maximum file size: 16MB per PDF
- Supported formats: PDF only
- Concurrent uploads: Up to 10 files

## 📁 Project Structure

```
pdfeditz/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/            # HTML templates
│   ├── index.html        # PDF merger interface
│   ├── compress.html     # PDF compression interface
│   └── terms.html        # Terms of service & privacy
├── uploads/              # Temporary file storage
└── .venv/               # Virtual environment (not in repo)
```

## 🛡️ Security Features

- Secure filename handling with Werkzeug
- File type validation (PDF only)
- Automatic cleanup of temporary files
- Size limits to prevent abuse
- Input sanitization for all uploads

## 🔄 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main merger interface |
| `/compress` | GET | Compression interface |
| `/terms` | GET | Terms of service |
| `/merge` | POST | Process PDF merger |
| `/compress_file` | POST | Process PDF compression |

## 🎯 Use Cases

- **Document Management**: Combine multiple reports into single PDFs
- **File Size Optimization**: Reduce PDFs for email or upload limits
- **Standardization**: Convert documents to uniform page sizes
- **Archive Preparation**: Organize and compress document collections

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏆 Credits

**Created by Ashu** - 2025

- Flask framework for web application
- PyPDF2 for PDF manipulation
- PyMuPDF for advanced PDF processing
- Modern gradient design inspiration

## 📞 Support

For support, questions, or feature requests:
- Email: support@pdfeditz.com
- Create an issue on GitHub
- Visit our website: [PDFEditZ.com](https://pdfeditz.com)

## 🔮 Roadmap

- [ ] Batch processing for multiple files
- [ ] Cloud storage integration
- [ ] Advanced PDF editing features
- [ ] API for developers
- [ ] Docker containerization

---

**© 2025 PDFEditZ - Professional PDF Management Made Simple**

## Usage

### 📄 PDF Merger (Multi-file):
1. Open the web application in your browser
2. Stay on the "PDF Merger" tab
3. Click "Choose PDF Files" and select multiple PDF files (minimum 2)
4. **🆕 Optionally select a target page size for resizing:**
   - **Keep Original**: No resizing (default)
   - **A4**: 210×297mm (most common)
   - **A3**: 297×420mm (larger format)
   - **A5**: 148×210mm (smaller format)
   - **Letter**: 8.5×11 inches (US standard)
   - **Legal**: 8.5×14 inches (US legal)
   - **Tabloid**: 11×17 inches (large format)
5. The files will be listed in the order you selected them
6. Click "Merge PDFs" (or "Resize to [Size] & Merge PDFs") to process
7. The merged PDF will be downloaded as `merged.pdf`

### 📦 PDF Compressor (Single file):
1. Click on the "PDF Compressor" tab
2. Upload a single PDF file
3. **Choose compression level based on your needs:**
   - **Light Compression**: Minimal compression, high quality (95% image quality, 150 DPI)
   - **Balanced Compression**: Good balance of size and quality (85% image quality, 120 DPI) - **Recommended**
   - **High Compression**: Small file size, good quality (70% image quality, 96 DPI)
   - **Maximum Compression**: Smallest file size, lower quality (50% image quality, 72 DPI)
4. Click "Apply [Level] Compression" to process
5. Download the compressed PDF with reduced file size
6. **Perfect for meeting website upload limits!**

## File Structure

```
pdfmerger/
├── app.py              # Main Flask application
├── templates/
│   └── index.html      # Upload form template
├── uploads/            # Temporary storage for uploaded files
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Technical Details

- **Backend**: Flask (Python web framework)
- **PDF Processing**: PyPDF2 library
- **File Upload**: HTML5 multiple file input
- **Security**: Secure filename handling with Werkzeug
- **Storage**: Temporary files stored in `uploads/` folder
- **Cleanup**: Automatic cleanup of uploaded files after each merge

## Configuration

You can modify the following settings in `app.py`:

- `MAX_CONTENT_LENGTH`: Maximum file size (default: 16MB)
- `UPLOAD_FOLDER`: Temporary storage folder (default: 'uploads')
- `app.secret_key`: Change this for production use

## Limitations

- Maximum file size: 16MB per PDF
- Minimum 2 PDF files required for merging
- Files are merged in upload order
- Temporary files are cleaned after each operation

## Production Notes

For production deployment:

1. Change the secret key in `app.py`
2. Set `debug=False` in the app.run() call
3. Use a proper WSGI server like Gunicorn
4. Configure proper error handling and logging
5. Add authentication if needed
6. Consider using cloud storage for file handling

## Error Handling

The app handles common errors:
- Invalid file types (only PDF allowed)
- File size too large
- Insufficient number of files
- PDF processing errors
- File system errors

## License

This project is open source and available under the MIT License.
