# Use a lightweight Python 2026 image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies for Neo4j/Qdrant clients
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Default command (can be overridden in docker-compose)
CMD ["python", "main.py"]