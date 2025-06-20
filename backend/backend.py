import os
import requests
import numpy as np
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image
import io

app = Flask(__name__)

# === Model Config ===
MODEL_DIR = './backend/models'
MODEL_FILENAME = 'waste_classification_model.h5'
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_FILENAME)
MODEL_URL = 'https://drive.google.com/uc?export=download&id=1mtsvwzWIwbdbYYWJ4KOCTkWx_lfQfKyM'

# === Download the model if not found ===
def download_model():
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
    if not os.path.exists(MODEL_PATH):
        print("🔽 Downloading model from Google Drive...")
        response = requests.get(MODEL_URL)
        if response.status_code == 200:
            with open(MODEL_PATH, 'wb') as f:
                f.write(response.content)
            print("✅ Model downloaded to", MODEL_PATH)
        else:
            raise RuntimeError(f"❌ Failed to download model: {response.status_code}")

# === Load the model ===
print(f"🔄 Checking model at {MODEL_PATH} ...")
try:
    download_model()
    model = load_model(MODEL_PATH)
    print("✅ Model loaded successfully!")
    model_loaded = True
except Exception as e:
    print(f"❌ Failed to load model: {e}")
    model_loaded = False

# === Routes ===
@app.route('/')
def home():
    return "Model is loaded and app is running."

@app.route('/health')
def health():
    return jsonify({
        "status": "ok" if model_loaded else "error",
        "model_loaded": model_loaded
    })

@app.route('/classify', methods=['POST'])
def classify():
    if not model_loaded:
        return jsonify({"error": "Model is not loaded"}), 500

    if 'image' not in request.files:
        return jsonify({"error": "No image part in the request"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        img = Image.open(io.BytesIO(file.read()))
        img = img.resize((224, 224))  # Adjust to match model input
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        predictions = model.predict(img_array)
        class_idx = np.argmax(predictions)
        confidence = float(predictions[0][class_idx])

        class_labels = ["Organic", "Plastic", "Paper", "Glass", "Other"]
        predicted_class = class_labels[class_idx]

        return jsonify({
            "class": predicted_class,
            "confidence": confidence
        })
    except Exception as e:
        return jsonify({"error": f"Error during classification: {e}"}), 500

# === Run the app ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5003))  # Use environment port (for Render)
    app.run(host="0.0.0.0", port=port)
