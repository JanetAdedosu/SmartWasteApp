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


