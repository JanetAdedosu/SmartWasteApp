FROM python:3.9-slim


WORKDIR /app


COPY requirements.txt .


RUN apt-get update && apt-get install -y \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY backend/ ./backend/
COPY backend/model.tflite backend/  



EXPOSE 5003


CMD ["gunicorn", "backend.backend:app", "-b", "0.0.0.0:5003"]

