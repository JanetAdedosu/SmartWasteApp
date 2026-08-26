# SmartWasteApp
A waste sorting app with computer vision

# ♻️ Smart Sorting Waste App

A mobile application powered by machine learning that helps users **identify and sort waste** into categories like *Plastic*, *Organic*, *Recyclable*, and *Non-Recyclable* using camera . Designed to promote sustainable waste management through intelligent classification.

---

## 📱 Features

- ✅ Real-time waste classification using image recognition
- 📷 Support for camera capture 
- 🧠 Deep learning model integrated with TensorFlow/Keras
- 🌐 Flutter-based cross-platform UI (iOS support)
- 🔤 Label mapping and confidence display
- 📊 Lightweight and optimized for mobile deployment

---

## 🚀 How It Works

1. User captures  an image of a waste item.
2. Image is processed and passed to a trained machine learning model.
3. Model predicts the waste category (e.g., Organic, Plastic, etc.).
4. The app displays the prediction and sorting guidance.

---

## 🛠️ Tech Stack

- **Frontend**: Flutter
- **Backend / ML**: Python, TensorFlow, Keras, Flask
- **Model Format**: `.h5` and `TFLite` for mobile deployment
- Tools:

PIL – Image loading and preprocessing

NumPy – Numerical operations on image arrays

JSON – For handling label mappings and config files

absl-py – Logging and CLI utility used with TensorFlow

SciPy – Scientific computing (e.g., image filtering, distance metrics)

Xcode – Required for building and running iOS apps

Visual Studio Code (VS Code) – Source code editor

---

## 📂 Project Structure

smart_sorting_waste_app/
│
├── backend/                             # Python backend
│   ├── dataset/                         # Dataset for training/testing
│   │   └── DATASET/TRAIN/...            # Organized training images
│   ├── models/                          # Saved training models (if not root)
│   ├── best_model.h5                    # Trained Keras model
│   ├── model.tflite                     # Converted TFLite model for mobile
│   ├── class_indices.json               # Mapping of class labels to indices
│   ├── convert_to_tflite.py             # Script to convert .h5 to .tflite
│   ├── train_model.py                   # Model training script
│   ├── test_model.py                    # Model test script
│   ├── requirements.txt                 # Python dependencies
│   └── app.py or backend.py             # Optional backend API (Flask/FastAPI)
│
├── smart_sorting_waste_app/            # Flutter app (main frontend)
│   ├── lib/
│   │   └── main.dart                    # Flutter entry point
│   ├── ios/                             # iOS-specific code
│   ├── android/                         # Android-specific code
│   ├── assets/                          # Image assets, .tflite model, labels
│   │   ├── model.tflite
│   │   └── labels.txt
│   ├── pubspec.yaml                     # Flutter dependencies and metadata
│   └── build/                           # Auto-generated build files
│
├── README.md                            # Project overview and instructions
└── .gitignore                           # Files and folders to ignore in Git

#janetadeola the red one