FROM python:3.9-buster



WORKDIR /app

# Copy only the model file explicitly
#COPY backend/models/waste_classification_model.h5 ./backend/models/waste_classification_model.h5

# Copy backend.py to /app for testing (optional)
COPY backend/backend.py ./backend.py

# Install Flask and tensorflow just to avoid runtime errors
RUN pip install --upgrade pip
RUN pip install flask tensorflow

# Expose port for flask app (optional)
EXPOSE 5003

# For testing: list the model file then run flask app
CMD ls -l /app/backend/models/ && python backend.py
