# Use an official Python 3.10 base image (TensorFlow 2.12 supports <=3.10)
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy everything into the container
COPY . .

# Install system dependencies (for image processing + TF)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set environment variable to tell Flask to run in production
ENV FLASK_ENV=production

# Expose port 5000
EXPOSE 5000

# Run the Flask app
CMD ["python", "backend/backend.py"]
