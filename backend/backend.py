import os
import gdown
from tensorflow.keras.models import load_model
from flask import Flask

app = Flask(__name__)

MODEL_DIR = './backend/models'
MODEL_FILENAME = 'waste_classification_model.h5'
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_FILENAME)

# Google Drive file link (replace if needed)
GDRIVE_URL = 'https://drive.google.com/uc?id=1mtsvwzWIwbdbYYWJ4KOCTkWx_lfQfKyM'


# Download the model if it doesn't already exist
if not os.path.exists(MODEL_PATH):
    print("📥 Downloading model from Google Drive...")
    os.makedirs(MODEL_DIR, exist_ok=True)
    gdown.download(GDRIVE_URL, MODEL_PATH, quiet=False)
    print("✅ Model downloaded!")

# Sanity check: read the first few bytes of the file
with open(MODEL_PATH, 'rb') as f:
    magic = f.read(4)
    print(f"🔍 File header: {magic}")
    if magic != b'\x89HDF':
        raise ValueError("❌ ERROR: File does not appear to be a valid .h5 model. Check your Google Drive file!")

# Load the model
print(f"🔄 Loading model from {MODEL_PATH} ...")
model = load_model(MODEL_PATH)
print("✅ Model loaded successfully!")

# Define a basic route
@app.route('/')
def home():
    return "✅ Model is loaded and app is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
