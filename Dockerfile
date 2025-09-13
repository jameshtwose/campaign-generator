# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and source code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose FastAPI port
EXPOSE 8080

# Set environment variables (optional, for production)
ENV PYTHONUNBUFFERED=1

# Start the FastAPI app using Uvicorn
CMD ["python", "main.py"]