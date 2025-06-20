import os
import gdown
from tensorflow.keras.models import load_model
from flask import Flask

app = Flask(__name__)

MODEL_DIR = './backend/models'
MODEL_FILENAME = 'waste_classification_model.h5'
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_FILENAME)
FILE_ID = "1mtsvwzWIwbdbYYWJ4KOCTkWx_lfQfKyM"
GDRIVE_URL = f"https://drive.google.com/uc?id={FILE_ID}"

def download_model():
    os.makedirs(MODEL_DIR, exist_ok=True)
    if not os.path.exists(MODEL_PATH):
        print(f"📥 Downloading model from Google Drive...")
        gdown.download(GDRIVE_URL, MODEL_PATH, quiet=False)
        print(f"✅ Model downloaded!")

print(f"🔄 Loading model from {MODEL_PATH} ...")
download_model()
model = load_model(MODEL_PATH)
print("✅ Model loaded successfully!")

@app.route('/')
def home():
    return "Model is loaded and app is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
