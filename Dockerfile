FROM python:3.10


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory to /app (one level above backend)
WORKDIR /app

# Copy requirements and install them
COPY backend/requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend folder including your models folder and all code
COPY backend/ ./backend/

# Expose port 5003
EXPOSE 5003

# Run the app with gunicorn, specifying the module as backend.backend:app
CMD ["gunicorn", "--bind", "0.0.0.0:5003", "backend.backend:app"]
