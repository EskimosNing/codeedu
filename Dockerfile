# Base image with Python
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Set environment variables
ENV PROJECT_ROOT=/app/src/codeedu
ENV PYTHONUNBUFFERED=1

# Run your Flask app (adjust path if needed)
CMD ["python", "src/codeedu/app.py"]
