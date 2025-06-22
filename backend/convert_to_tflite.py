import tensorflow as tf

# Load the retrained Keras model
model = tf.keras.models.load_model('best_model.h5')

# Convert the Keras model to TFLite format
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the TFLite model to file
with open('model.tflite', 'wb') as f:
    f.write(tflite_model)

print("Model converted to model.tflite successfully!")




