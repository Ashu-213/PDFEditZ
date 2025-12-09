#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install LibreOffice (Render has sudo access)
sudo apt-get update
sudo apt-get install -y libreoffice

# Verify installation
which soffice && echo "LibreOffice installed successfully" || echo "Warning: LibreOffice not found"
