import os
import json
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models, optimizers, callbacks

# --- Paths ---
train_dir = os.path.join(os.path.dirname(__file__), "dataset", "DATASET", "TRAIN")
if not os.path.exists(train_dir):
    raise FileNotFoundError(f"Train dataset directory not found: {train_dir}")

# --- Params ---
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 25             # Slightly longer training
FINE_TUNE_EPOCHS = 15   # More fine-tuning
LEARNING_RATE = 1e-4

# --- Data augmentation ---
train_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    rotation_range=30,           # stronger augmentation
    width_shift_range=0.3,
    height_shift_range=0.3,
    shear_range=0.2,
    zoom_range=0.3,
    horizontal_flip=True,
    brightness_range=[0.7, 1.3],
    fill_mode="nearest"
)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    shuffle=True
)

val_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    shuffle=True
)

# --- Compute class weights to handle imbalance ---
from sklearn.utils.class_weight import compute_class_weight
import numpy as np

classes = list(train_generator.class_indices.values())
labels = train_generator.classes
class_weights = compute_class_weight(
    class_weight='balanced',
    classes=np.unique(labels),
    y=labels
)
class_weights = {i: w for i, w in enumerate(class_weights)}
print("✅ Class weights:", class_weights)

# --- Load MobileNetV2 ---
base_model = MobileNetV2(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False

# --- Build model ---
model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.4),           # Slightly higher dropout
    layers.Dense(256, activation="relu"),  # More neurons
    layers.Dense(train_generator.num_classes, activation="softmax")
])

# --- Compile model ---
model.compile(
    optimizer=optimizers.Adam(learning_rate=LEARNING_RATE),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# --- Callbacks ---
checkpoint = callbacks.ModelCheckpoint("best_model_v2.keras", monitor="val_accuracy", save_best_only=True, verbose=1)
early_stop = callbacks.EarlyStopping(monitor="val_accuracy", patience=6, restore_best_weights=True)
reduce_lr = callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=3, verbose=1)

# --- Stage 1 Training (frozen base) ---
history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=EPOCHS,
    class_weight=class_weights,
    callbacks=[checkpoint, early_stop, reduce_lr]
)

# --- Fine-tuning: unfreeze more layers ---
base_model.trainable = True
fine_tune_at = len(base_model.layers) // 3  # unfreeze last 2/3 for better learning
for layer in base_model.layers[:fine_tune_at]:
    layer.trainable = False

model.compile(
    optimizer=optimizers.Adam(learning_rate=1e-5),  # smaller LR for fine-tuning
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# --- Stage 2 Training (fine-tuning) ---
history_fine = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=FINE_TUNE_EPOCHS,
    class_weight=class_weights,
    callbacks=[checkpoint, early_stop, reduce_lr]
)

# --- Save class indices ---
with open("class_indices.json", "w") as f:
    json.dump(train_generator.class_indices, f)

print("✅ Training complete. Best model and class indices saved.")
