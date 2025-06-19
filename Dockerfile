# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set working directory in the container
WORKDIR /app/backend

# Copy backend folder contents into the container
COPY backend/ /app/backend/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your Flask app will run on
EXPOSE 5001

# Set environment variables to avoid Python buffering output
ENV PYTHONUNBUFFERED=1

# Command to run your Flask app
CMD ["python", "backend.py"]
