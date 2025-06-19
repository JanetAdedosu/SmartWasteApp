from PIL import Image
import numpy as np
import tensorflow as tf

# Load your model
#interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter = tf.lite.Interpreter(model_path="/Users/janetadedosu/Desktop/Smart_Waste/backend/model.tflite")

interpreter.allocate_tensors()

# Preprocess the image
img = Image.open('dataset/DATASET/TEST/Organic/O_12568.jpg').resize((150, 150))
img_array = np.expand_dims(np.array(img) / 255.0, axis=0).astype(np.float32)  # Normalize and ensure FLOAT32

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

interpreter.set_tensor(input_details[0]['index'], img_array)  # Set input tensor
interpreter.invoke()

# Get the predicted class index
predicted_index = np.argmax(interpreter.get_tensor(output_details[0]['index']))

# Map the class index to the label
class_labels = {
    0: "Organic",
    1: "Recyclable",
    2: "Non-Recyclable"
}

# Output the full class name
print(f"Predicted Class: {class_labels[predicted_index]}")
