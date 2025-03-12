import tensorflow as tf
import numpy as np
from PIL import Image
import io

# Path to your Keras model file
MODEL_PATH = "model/fine_tuned_model.h5"

# Load the Keras model
model = tf.keras.models.load_model(MODEL_PATH)

# Updated class names based on your provided classes:
class_names = [
    "asd_mild_coloring_3-6",
    "asd_moderate_coloring_3-6",
    "asd_severe_coloring_3-6",
    "asdwithcd_mild_coloring_3-6",
    "asdwithcd_moderate_coloring_3-6",
    "asdwithcd_severe_coloring_3-6",
    "non_asd_normal_coloring_3-6"
]

def preprocess_image(image_bytes: bytes, target_size=(128, 128)):
    """
    Preprocess the input image bytes into a format acceptable by the model.
    """
    image = Image.open(io.BytesIO(image_bytes))
    image = image.convert("RGB")
    image = image.resize(target_size)
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    return image_array

def predict_image(image_bytes: bytes):
    """
    Perform a prediction on the given image bytes.
    Returns the predicted label and confidence.
    """
    processed = preprocess_image(image_bytes)
    predictions = model.predict(processed)
    predicted_index = np.argmax(predictions, axis=1)[0]
    confidence = float(np.max(predictions))
    predicted_label = class_names[predicted_index] if predicted_index < len(class_names) else f"class_{predicted_index}"
    return predicted_label, confidence
