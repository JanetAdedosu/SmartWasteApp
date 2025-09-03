# import os
# import json
# import numpy as np
# from keras_preprocessing.image import ImageDataGenerator
# from tensorflow.keras.preprocessing import image
# from tensorflow.keras.models import load_model

# # --- Paths ---
# BASE_DIR = os.path.dirname(__file__)
# MODEL_PATH = os.path.join(BASE_DIR, "models", "best_model_v2.keras")
# CLASS_INDICES_PATH = os.path.join(BASE_DIR, "models", "class_indices.json")
# DATASET_DIR = os.path.join(BASE_DIR, "dataset", "DATASET", "TRAIN")  # your current TRAIN folder
# TEST_IMAGE_PATH = os.path.join(DATASET_DIR, "Paper", "R_10736.jpg")   # example single image

# # --- Check files ---
# if not os.path.exists(MODEL_PATH):
#     raise FileNotFoundError(f"❌ Could not find 'best_model_v2.keras' at {MODEL_PATH}")
# if not os.path.exists(CLASS_INDICES_PATH):
#     raise FileNotFoundError(f"❌ Could not find 'class_indices.json' at {CLASS_INDICES_PATH}")
# if not os.path.exists(DATASET_DIR):
#     raise FileNotFoundError(f"❌ Dataset folder not found at {DATASET_DIR}")

# print(f"✅ Model found at: {MODEL_PATH}")
# print(f"✅ Class indices found at: {CLASS_INDICES_PATH}")
# print(f"✅ Dataset folder found at: {DATASET_DIR}")

# # --- Load model ---
# model = load_model(MODEL_PATH)
# print("✅ Model loaded successfully.")

# # --- Load class indices ---
# with open(CLASS_INDICES_PATH, "r") as f:
#     class_indices = json.load(f)
# idx_to_class = {v: k for k, v in class_indices.items()}

# # --- Single image prediction ---
# def preprocess_image(img_path, target_size=(224, 224)):
#     img = image.load_img(img_path, target_size=target_size)
#     img_array = image.img_to_array(img)
#     img_array = np.expand_dims(img_array, axis=0)
#     img_array = img_array / 255.0
#     return img_array

# def predict_image(img_path):
#     img_array = preprocess_image(img_path)
#     preds = model.predict(img_array)
#     class_idx = np.argmax(preds[0])
#     class_label = idx_to_class[class_idx]
#     confidence = preds[0][class_idx] * 100
#     return class_label, confidence

# if os.path.exists(TEST_IMAGE_PATH):
#     label, conf = predict_image(TEST_IMAGE_PATH)
#     print(f"🔍 Single Image Prediction: {label} ({conf:.2f}% confidence)")
# else:
#     print(f"⚠️ Test image not found at {TEST_IMAGE_PATH}")

# # --- Full dataset evaluation ---
# def evaluate_dataset(dataset_dir, target_size=(224, 224), batch_size=32):
#     test_datagen = ImageDataGenerator(rescale=1./255)
#     test_generator = test_datagen.flow_from_directory(
#         dataset_dir,
#         target_size=target_size,
#         batch_size=batch_size,
#         class_mode="categorical",  # must match your training
#         shuffle=False
#     )

#     loss, acc = model.evaluate(test_generator)
#     print(f"📊 Dataset Accuracy: {acc*100:.2f}% | Loss: {loss:.4f}")

# evaluate_dataset(DATASET_DIR)



# import os
# import json
# import numpy as np
# from keras_preprocessing.image import ImageDataGenerator
# from tensorflow.keras.preprocessing import image
# from tensorflow.keras.models import load_model

# # --- Paths ---
# BASE_DIR = os.path.dirname(__file__)
# MODEL_PATH = os.path.join(BASE_DIR,  "best_model_v2.keras")
# CLASS_INDICES_PATH = os.path.join(BASE_DIR,  "class_indices.json")
# DATASET_DIR = os.path.join(BASE_DIR, "dataset", "DATASET", "TRAIN")  # your current dataset
# TEST_IMAGE_PATH = os.path.join(DATASET_DIR, "Plastic", "R_7.jpg")   # example single image

# # --- Check existence ---
# if not os.path.exists(MODEL_PATH):
#     raise FileNotFoundError(f"❌ Model not found at {MODEL_PATH}")
# if not os.path.exists(CLASS_INDICES_PATH):
#     raise FileNotFoundError(f"❌ Class indices not found at {CLASS_INDICES_PATH}")
# if not os.path.exists(DATASET_DIR):
#     raise FileNotFoundError(f"❌ Dataset folder not found at {DATASET_DIR}")

# print(f"✅ Model found at: {MODEL_PATH}")
# print(f"✅ Class indices found at: {CLASS_INDICES_PATH}")
# print(f"✅ Dataset folder found at: {DATASET_DIR}")

# # --- Load model ---
# model = load_model(MODEL_PATH)
# print("✅ Model loaded successfully.")

# # --- Load class indices ---
# with open(CLASS_INDICES_PATH, "r") as f:
#     class_indices = json.load(f)
# idx_to_class = {v: k for k, v in class_indices.items()}

# # --- Single image prediction ---
# def preprocess_image(img_path, target_size=(224, 224)):
#     img = image.load_img(img_path, target_size=target_size)
#     img_array = image.img_to_array(img)
#     img_array = np.expand_dims(img_array, axis=0)
#     img_array = img_array / 255.0
#     return img_array

# def predict_image(img_path):
#     img_array = preprocess_image(img_path)
#     preds = model.predict(img_array)
#     class_idx = np.argmax(preds[0])
#     class_label = idx_to_class[class_idx]
#     confidence = preds[0][class_idx] * 100
#     return class_label, confidence

# if os.path.exists(TEST_IMAGE_PATH):
#     label, conf = predict_image(TEST_IMAGE_PATH)
#     print(f"🔍 Single Image Prediction: {label} ({conf:.2f}% confidence)")
# else:
#     print(f"⚠️ Test image not found at {TEST_IMAGE_PATH}")

# # --- Full dataset evaluation ---
# def evaluate_dataset(dataset_dir, target_size=(224, 224), batch_size=32):
#     test_datagen = ImageDataGenerator(rescale=1./255)
#     test_generator = test_datagen.flow_from_directory(
#         dataset_dir,
#         target_size=target_size,
#         batch_size=batch_size,
#         class_mode="categorical",  # must match training
#         shuffle=False
#     )

#     loss, acc = model.evaluate(test_generator, verbose=1)
#     print(f"📊 Dataset Accuracy: {acc*100:.2f}% | Loss: {loss:.4f}")

# evaluate_dataset(DATASET_DIR)


from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image

model = load_model("best_model_v2.keras")

img = Image.open("dataset/DATASET/TRAIN/Paper/R_10734.jpg").resize((224,224))
img_array = np.expand_dims(np.array(img)/255.0, axis=0)

pred = model.predict(img_array)
print(pred, np.argmax(pred))
