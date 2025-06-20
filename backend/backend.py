from flask import Flask, jsonify, request
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image
import logging
import io
import os
import traceback

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)

# Load TFLite model
MODEL_PATH = "model.tflite"  # Adjust path if needed

logging.info(f"Starting model load check...")
logging.info(f"Current working directory: {os.getcwd()}")
logging.info(f"Looking for model file at: {MODEL_PATH}")

if not os.path.isfile(MODEL_PATH):
    logging.error(f"Model file NOT found at {MODEL_PATH}")

interpreter = None
model_loaded = False
load_error = None

try:
    interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    model_loaded = True
    logging.info("TFLite model loaded successfully.")
except Exception as e:
    load_error = str(e) + "\n" + traceback.format_exc()
    logging.error(f"Failed to load TFLite model:\n{load_error}")

# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    if model_loaded:
        return jsonify({"model_loaded": True, "status": "ok"})
    else:
        return jsonify({"model_loaded": False, "status": "error", "error": load_error})

# Classify endpoint
@app.route('/classify', methods=['POST'])
def classify():
    if not model_loaded:
        return jsonify({"error": "Model not loaded"}), 500

    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    try:
        # Preprocess image
        img = Image.open(io.BytesIO(file.read())).convert('RGB')
        img = img.resize((150, 150))  # Match your model input size
        img_array = np.expand_dims(np.array(img) / 255.0, axis=0).astype(np.float32)

        # Run inference
        interpreter.set_tensor(input_details[0]['index'], img_array)
        interpreter.invoke()
        predictions = interpreter.get_tensor(output_details[0]['index'])

        class_idx = int(np.argmax(predictions[0]))
        confidence = float(predictions[0][class_idx])

        class_labels = {
            0: "Organic",
            1: "Recyclable",
            2: "Non-Recyclable",
            3: "Plastic"
        }

        predicted_class = class_labels.get(class_idx, "Unknown")

        return jsonify({
            "class": predicted_class,
            "confidence": confidence
        })

    except Exception as e:
        logging.error(f"Error during classification: {e}", exc_info=True)
        return jsonify({"error": f"Error during classification: {e}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5003))
    app.run(host="0.0.0.0", port=port)
