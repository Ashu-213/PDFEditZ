# Word to PDF Converter

A lightweight Flask web application to convert Word documents (.docx) to PDF format instantly.

## Features

- 📄 Upload Word documents (.docx only)
- ⚡ Fast conversion to PDF
- 🎨 Clean, minimal Bootstrap UI
- 🖱️ Drag and drop support
- 🔄 2-step process (Convert → Download)
- 🧹 Automatic cleanup (no files stored)
- 🔐 Secure with environment variables
- 📦 Modular architecture

## Project Structure

```
PDFEditZ/
├── app.py                 # Application entry point
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── routes/                # Route handlers (blueprints)
│   ├── __init__.py
│   └── main.py           # Main routes
├── utils/                 # Utility functions
│   ├── __init__.py
│   ├── converter.py      # Conversion logic
│   └── file_handler.py   # File operations
├── static/                # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── templates/             # HTML templates
│   └── index.html
└── uploads/               # Temporary file storage
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Ashu-213/PDFEditZ.git
cd PDFEditZ
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Copy the example file
copy .env.example .env

# Edit .env and add your SECRET_KEY
# Generate a secure key: python -c "import os; print(os.urandom(24).hex())"
```

## Usage

1. Run the application:
```bash
python app.py
```

2. Open your browser and go to `http://localhost:5000`

3. Upload a .docx file, convert, and download

**Note**: Old .doc format is not supported. Save your file as .docx in Word first.

## Configuration

Edit `.env` file to customize:
- `SECRET_KEY`: Flask secret key (generate using: `python -c "import os; print(os.urandom(24).hex())"`)
- `MAX_CONTENT_LENGTH`: Maximum file size in bytes (default: 16MB)
- `UPLOAD_FOLDER`: Folder for temporary file storage
- `ALLOWED_EXTENSIONS`: Supported file extensions (default: docx)

**Important**: Never commit your `.env` file to version control. Use `.env.example` as a template.

## Requirements

- Python 3.7+
- Flask 3.0+
- docx2pdf
- Microsoft Word (required for docx2pdf on Windows)

## How It Works

1. User uploads a .docx file
2. File is temporarily saved with unique timestamp
3. Conversion happens using Microsoft Word automation
4. PDF is loaded into memory
5. Temporary files are immediately deleted
6. User downloads PDF from memory

No files are permanently stored on the server!

## Adding New Features

The modular structure makes it easy to extend:

- **New routes**: Add blueprints to `routes/` folder
- **New converters**: Extend `DocumentConverter` class in `utils/`
- **New file types**: Update `ALLOWED_EXTENSIONS` and converter logic
- **New UI**: Modify templates in `templates/` and styles in `static/`

## License

MIT License - feel free to use for any project!

1. User uploads a .docx file
2. File is temporarily saved with unique timestamp
3. Conversion happens using Microsoft Word automation
4. PDF is loaded into memory
5. Temporary files are immediately deleted
6. User downloads PDF from memory

No files are permanently stored on the server!.7+
- Flask
- docx2pdf
- Microsoft Word (required for docx2pdf on Windows)

## Note

The `docx2pdf` library requires Microsoft Word to be installed on Windows systems.
