# Contributing to PDFEditZ

First off, thank you for considering contributing to PDFEditZ! It's people like you that make PDFEditZ such a great tool.

## Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct. Please report unacceptable behavior to support@pdfeditz.com.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps which reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed after following the steps**
- **Explain which behavior you expected to see instead and why**
- **Include screenshots if possible**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior and explain which behavior you expected to see instead**
- **Explain why this enhancement would be useful**

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code lints
6. Issue that pull request!

## Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/yourusername/pdfeditz.git
   cd pdfeditz
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

## Style Guidelines

### Python Code Style

- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions small and focused
- Use type hints where appropriate

### HTML/CSS Style

- Use semantic HTML5 elements
- Follow consistent indentation (2 spaces)
- Use CSS classes instead of inline styles
- Keep CSS organized and commented

### Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

## Project Structure

```
pdfeditz/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── index.html        # PDF merger interface
│   ├── compress.html     # PDF compression interface
│   └── terms.html        # Terms of service
├── uploads/              # Temporary file storage
└── tests/               # Test files (if you add them)
```

## Testing

Currently, the project doesn't have automated tests, but we welcome contributions to add them! When adding tests:

- Use pytest as the testing framework
- Write unit tests for individual functions
- Write integration tests for API endpoints
- Ensure all tests pass before submitting a PR

## Questions?

Don't hesitate to contact us at support@pdfeditz.com if you have any questions!
