# Use a slim version of Python 3.9
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy all backend files into the container
COPY backend/ ./backend/

# Install system-level dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install required Python packages
RUN pip install --upgrade pip
RUN pip install flask flask-cors gunicorn tensorflow-cpu

# Expose the port the app will run on
EXPOSE 5003

# Start the app using Gunicorn on port 5003
CMD ["gunicorn", "backend.backend:app", "-b", "0.0.0.0:5003"]
