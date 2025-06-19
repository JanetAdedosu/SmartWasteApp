from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import requests

import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np
from io import BytesIO

app = Flask(__name__)
CORS(app)

# Model setup
MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "waste_classification_model.h5")
MODEL_URL = "https://drive.google.com/uc?export=download&id=1mtsvwzWIwbdbYYWJ4KOCTkWx_lfQfKyM"

# Download the model if it doesn't exist
if not os.path.exists(MODEL_PATH):
    os.makedirs(MODEL_DIR, exist_ok=True)
    print("📥 Downloading model from Google Drive...")
    response = requests.get(MODEL_URL)
    with open(MODEL_PATH, 'wb') as f:
        f.write(response.content)
    print("✅ Model downloaded!")

# Load model
model = load_model(MODEL_PATH)

# Constants
IMG_HEIGHT = 150
IMG_WIDTH = 150
CLASS_NAMES = ["Organic", "Recyclable", "Plastic"]

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
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)
