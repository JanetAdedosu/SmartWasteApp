from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import numpy as np
from io import BytesIO

import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img

import requests

app = Flask(__name__)
CORS(app)

# Constants
MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "waste_classification_model.h5")
FILE_ID = "1mtsvwzWIwbdbYYWJ4KOCTkWx_lfQfKyM"  # Your Google Drive file ID here

IMG_HEIGHT = 150
IMG_WIDTH = 150
CLASS_NAMES = ["Organic", "Recyclable", "Plastic"]


def download_file_from_google_drive(id, destination):
    """Downloads file from Google Drive handling confirmation tokens."""

    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    """Extracts Google Drive download warning token."""
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None


def save_response_content(response, destination):
    """Save the content of the response to a file."""
    CHUNK_SIZE = 32768

    os.makedirs(os.path.dirname(destination), exist_ok=True)
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                f.write(chunk)


# Download model if not exists or file size suspiciously small
if not os.path.exists(MODEL_PATH) or os.path.getsize(MODEL_PATH) < 1000000:
    print("📥 Downloading model from Google Drive...")
    download_file_from_google_drive(FILE_ID, MODEL_PATH)
    print("✅ Model downloaded!")


# Load the model
print(f"🔄 Loading model from {MODEL_PATH} ...")
model = load_model(MODEL_PATH)
print("✅ Model loaded successfully!")


@app.route('/')
def home():
    return jsonify({"message": "Smart Waste Backend is running!"})


@app.route('/classify', methods=['POST'])
def classify_image():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400

        image_file = request.files['image']
        img = load_img(BytesIO(image_file.read()), target_size=(IMG_HEIGHT, IMG_WIDTH))
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        predictions = model.predict(img_array)
        predicted_class_index = np.argmax(predictions, axis=1)[0]
        confidence = float(predictions[0][predicted_class_index])

        result = {
            "class": CLASS_NAMES[predicted_class_index],
            "confidence": round(confidence, 2)
        }

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    app.run(host="0.0.0.0", port=port, debug=True)
