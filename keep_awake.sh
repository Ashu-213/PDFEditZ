#!/bin/bash
# Keep Render app awake by pinging it every 10 minutes

while true; do
    echo "Pinging PDFEditZ to keep it awake..."
    curl -s https://pdfeditz-1.onrender.com > /dev/null
    echo "Ping sent at $(date)"
    sleep 600  # Wait 10 minutes (600 seconds)
done
