import os
from flask import Flask, jsonify
from tensorflow.keras.models import load_model

app = Flask(__name__)

MODEL_DIR = './backend/models'
MODEL_FILENAME = 'waste_classification_model.h5'
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_FILENAME)



print(f"🔄 Loading model from {MODEL_PATH} ...")

if not os.path.exists(MODEL_PATH):
    raise RuntimeError(f"Model file {MODEL_PATH} not found. Please add it manually before running.")

model = load_model(MODEL_PATH)
print("✅ Model loaded successfully!")

@app.route('/')
def home():
    return "Model is loaded and app is running."

@app.route('/health')
def health():
    return jsonify({"status": "ok", "model_loaded": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
