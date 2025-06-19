# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy the backend folder (which includes your code and requirements.txt)
COPY backend/ ./backend/

# Install dependencies using the requirements.txt inside backend
RUN pip install --no-cache-dir -r backend/requirements.txt

# Expose the port your Flask app runs on (update this if you use a different port)
EXPOSE 5001

# Run the Flask app
CMD ["python", "backend/backend.py"]
