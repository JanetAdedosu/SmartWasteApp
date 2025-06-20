import os
from flask import Flask, jsonify
from tensorflow.keras.models import load_model

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

# Start Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
