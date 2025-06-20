# Use an official Python runtime as a parent image
FROM python:3.9-buster

# Set working directory in the container
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY backend/requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend/ ./backend/

# Copy the model file explicitly (if not already copied by previous COPY)
# If your COPY backend/ already includes models/, you can omit this line
COPY backend/models/waste_classification_model.h5 ./backend/models/waste_classification_model.h5

# Expose the port your app runs on
EXPOSE 5003

# Command to run your app with Gunicorn or whatever you use
CMD ["gunicorn", "--bind", "0.0.0.0:5003", "backend.backend:app"]
