import os
import numpy as np
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image
import io

app = Flask(__name__)

# Define model path
MODEL_DIR = './backend/models'
MODEL_FILENAME = 'waste_classification_model.h5'
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_FILENAME)

print(f"🔄 Loading model from {MODEL_PATH} ...")

# Load the model (with error handling)
try:
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    model = load_model(MODEL_PATH)
    print("✅ Model loaded successfully!")
    model_loaded = True
except Exception as e:
    print(f"❌ Failed to load model: {e}")
    model_loaded = False

# Root route
@app.route('/')
def home():
    return "Model is loaded and app is running."

# Health check
@app.route('/health')
def health():
    return jsonify({
        "status": "ok" if model_loaded else "error",
        "model_loaded": model_loaded
    })

# Image classification route
@app.route('/classify', methods=['POST'])
def classify():
    if not model_loaded:
        return jsonify({"error": "Model is not loaded"}), 500
    
    # Check if the image is part of the request
    if 'image' not in request.files:
        return jsonify({"error": "No image part in the request"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Open image file
        img = Image.open(io.BytesIO(file.read()))
        img = img.resize((224, 224))  # Adjust based on your model's expected input size
        img_array = np.array(img) / 255.0  # Normalize the image
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

        # Predict with the model
        predictions = model.predict(img_array)
        class_idx = np.argmax(predictions)  # Get index of the highest probability
        confidence = predictions[0][class_idx]

        # Mapping class indices to human-readable labels (Adjust these according to your model)
        class_labels = ["Organic", "Plastic", "Paper", "Glass", "Other"]
        predicted_class = class_labels[class_idx]

        # Prepare and return response
        return jsonify({
            "class": predicted_class,
            "confidence": confidence
        })
    except Exception as e:
        return jsonify({"error": f"Error during classification: {e}"}), 500

# Start Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
