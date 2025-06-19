import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np
from io import BytesIO  # ✅ Added to handle file upload

app = Flask(__name__)
CORS(app)  # ✅ Allow cross-origin requests (Flutter -> Flask)

# Load model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "waste_classification_model.h5")
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
model = load_model(MODEL_PATH)

# Image input dimensions and class labels
IMG_HEIGHT = 150
IMG_WIDTH = 150
CLASS_NAMES = ["Organic", "Recyclable","Plastic"]

@app.route('/')
def home():
    return jsonify({"message": "Smart Waste Backend is running!"})

@app.route('/classify', methods=['POST'])
def classify_image():
    try:
        print("📥 Request received")
        print("📥 Files received:", request.files)

        if 'image' not in request.files:
            print("❌ No image found in request.files")
            return jsonify({"error": "No image file provided"}), 400

        image_file = request.files['image']
        print("✅ Image filename:", image_file.filename)

        # ✅ FIX: Read image from memory stream
        img = load_img(BytesIO(image_file.read()), target_size=(IMG_HEIGHT, IMG_WIDTH))
        img_array = img_to_array(img)
        print("✅ Image shape after loading:", img_array.shape)

        img_array = np.expand_dims(img_array, axis=0) / 255.0
        print("✅ Final input shape to model:", img_array.shape)

        predictions = model.predict(img_array)
        print("✅ Model output:", predictions)

        predicted_class_index = np.argmax(predictions, axis=1)[0]
        confidence = float(predictions[0][predicted_class_index])
        result = {
            "class": CLASS_NAMES[predicted_class_index],
            "confidence": round(confidence, 2)
        }

        print("✅ Classification result:", result)
        return jsonify(result), 200

    except Exception as e:
        print("❌ Error occurred:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
