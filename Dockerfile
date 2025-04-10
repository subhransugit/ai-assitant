# Start from official Python slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirement files first for layer caching
COPY requirements.txt .

# Install system dependencies (needed for chroma-hnswlib, PDFs)
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libffi-dev \
    libpoppler-cpp-dev \
    poppler-utils \
    && pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the full app
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Run the app using Streamlit
CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.enableCORS=false"]
