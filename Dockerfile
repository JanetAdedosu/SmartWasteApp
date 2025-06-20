# Use a slim version of Python 3.9
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt first
COPY requirements.txt .

# Install system-level dependencies needed to build packages (e.g., Pillow)
RUN apt-get update && apt-get install -y \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install required Python packages from requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy backend code after dependencies to leverage Docker cache
COPY backend/ ./backend/

# Copy the model file into the working directory
COPY model.tflite .

# Expose the port the app will run on
EXPOSE 5003

# Start the app using Gunicorn on port 5003
CMD ["gunicorn", "backend.backend:app", "-b", "0.0.0.0:5003"]

