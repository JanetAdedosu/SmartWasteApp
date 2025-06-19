import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# Define dataset paths
dataset_dir = "dataset/DATASET"
train_dir = "dataset/DATASET/TRAIN"
test_dir = "dataset/DATASET/TEST"

#train_dir = os.path.join(dataset_dir, "TRAIN")
#test_dir = os.path.join(dataset_dir, "TEST")

# Check if dataset directories exist
if not os.path.exists(train_dir) or not os.path.exists(test_dir):
    raise FileNotFoundError(f"Dataset directories not found. Please check: {train_dir} and {test_dir}")

# Image parameters
img_height, img_width = 150, 150
batch_size = 32

# Data preprocessing and augmentation
datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    validation_split=0.2
)

# Training and validation data generators
train_generator = datagen.flow_from_directory(
    train_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode="categorical",
    subset="training"
)

val_generator = datagen.flow_from_directory(
    train_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode="categorical",
    subset="validation"
)

# Define the CNN model
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(train_generator.num_classes, activation='softmax')
])

# Compile the model
model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# Print model summary
model.summary()

# Create models/ directory if it doesn't exist
os.makedirs("models", exist_ok=True)

# Callbacks
callbacks = [
    EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True),
    ModelCheckpoint('models/best_model.h5', save_best_only=True, monitor='val_loss')
]

# Train the model
epochs = 10
model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=epochs,
    callbacks=callbacks,
    verbose=1
)

# Save final model
model.save("models/waste_classification_model.h5")

# Test data generator
test_generator = datagen.flow_from_directory(
    test_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode="categorical",
    shuffle=False
)

# Evaluate model
test_loss, test_acc = model.evaluate(test_generator, verbose=1)
print(f"\n✅ Test Loss: {test_loss:.4f}")
print(f"✅ Test Accuracy: {test_acc:.2%}")
