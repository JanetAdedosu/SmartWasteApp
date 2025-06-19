import os
import requests
from tensorflow.keras.models import load_model
from flask import Flask

app = Flask(__name__)

MODEL_DIR = './backend/models'
MODEL_FILENAME = 'waste_classification_model.h5'
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_FILENAME)
FILE_ID = '1mtsvwzWIwbdbYYWJ4KOCTkWx_lfQfKyM'  # your file ID from the Drive link

def download_file_from_google_drive(file_id, destination):
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()

    response = session.get(URL, params={'id': file_id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    os.makedirs(os.path.dirname(destination), exist_ok=True)

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                f.write(chunk)

# Download model if it doesn't exist yet
if not os.path.exists(MODEL_PATH):
    print("📥 Downloading model from Google Drive...")
    download_file_from_google_drive(FILE_ID, MODEL_PATH)
    print("✅ Model downloaded!")

print(f"🔄 Loading model from {MODEL_PATH} ...")
model = load_model(MODEL_PATH)
print("✅ Model loaded successfully!")

# Your Flask app routes and logic here
@app.route('/')
def home():
    return "Model is loaded and app is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
