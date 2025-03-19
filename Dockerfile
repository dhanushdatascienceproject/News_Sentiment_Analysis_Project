# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Hugging Face's Transformers & Torch
RUN pip install --no-cache-dir transformers torch

# Create necessary directories and set permissions
RUN mkdir -p /app/static/audio && chmod -R 777 /app/static

# Copy FastAPI app files
COPY . .

# Set environment variables
ENV NLTK_DATA=/tmp/nltk_data \
    HF_HOME=/tmp/huggingface

# Expose the correct port
EXPOSE 7860

# Run FastAPI server
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "7860"]
