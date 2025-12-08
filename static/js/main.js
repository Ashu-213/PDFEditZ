const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileName = document.getElementById('fileName');
const uploadForm = document.getElementById('uploadForm');
const uploadSection = document.getElementById('uploadSection');
const successSection = document.getElementById('successSection');
const convertText = document.getElementById('convertText');
const convertingText = document.getElementById('convertingText');
const downloadBtn = document.getElementById('downloadBtn');
const convertAnotherBtn = document.getElementById('convertAnotherBtn');

let convertedFileUrl = '';
let convertedFileName = '';

uploadArea.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        fileName.textContent = `Selected: ${e.target.files[0].name}`;
    }
});

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '#764ba2';
    uploadArea.style.background = '#f8f9fa';
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.style.borderColor = '#667eea';
    uploadArea.style.background = '';
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '#667eea';
    uploadArea.style.background = '';
    
    if (e.dataTransfer.files.length > 0) {
        fileInput.files = e.dataTransfer.files;
        fileName.textContent = `Selected: ${e.dataTransfer.files[0].name}`;
    }
});

// Handle form submission
uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const file = fileInput.files[0];
    if (!file) {
        alert('Please select a file');
        return;
    }
    
    // Show converting state
    convertText.classList.add('hidden');
    convertingText.classList.remove('hidden');
    uploadForm.querySelector('button').disabled = true;
    
    // Create form data
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        // Send conversion request
        const response = await fetch('/convert', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            // Get the blob and create download URL
            const blob = await response.blob();
            convertedFileUrl = window.URL.createObjectURL(blob);
            
            // Get filename from response header or use default
            const contentDisposition = response.headers.get('Content-Disposition');
            if (contentDisposition) {
                const match = contentDisposition.match(/filename="(.+)"/);
                convertedFileName = match ? match[1] : 'converted.pdf';
            } else {
                convertedFileName = file.name.replace(/\.[^/.]+$/, '') + '.pdf';
            }
            
            // Show success section
            uploadSection.classList.add('hidden');
            successSection.classList.remove('hidden');
        } else {
            const text = await response.text();
            alert('Conversion failed: ' + text);
            resetForm();
        }
    } catch (error) {
        alert('Error during conversion: ' + error.message);
        resetForm();
    }
});

// Handle download button
downloadBtn.addEventListener('click', () => {
    const a = document.createElement('a');
    a.href = convertedFileUrl;
    a.download = convertedFileName;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    
    // Clean up and redirect to converter page after download
    setTimeout(() => {
        if (convertedFileUrl) {
            window.URL.revokeObjectURL(convertedFileUrl);
            convertedFileUrl = '';
        }
        
        resetForm();
        successSection.classList.add('hidden');
        uploadSection.classList.remove('hidden');
    }, 500);
});

// Handle convert another button
convertAnotherBtn.addEventListener('click', () => {
    // Clean up the blob URL
    if (convertedFileUrl) {
        window.URL.revokeObjectURL(convertedFileUrl);
        convertedFileUrl = '';
    }
    
    // Reset and show upload section
    resetForm();
    successSection.classList.add('hidden');
    uploadSection.classList.remove('hidden');
});

function resetForm() {
    uploadForm.reset();
    fileName.textContent = '';
    convertText.classList.remove('hidden');
    convertingText.classList.add('hidden');
    uploadForm.querySelector('button').disabled = false;
}
