# SPDX-FileCopyrightText: Siemens AG 2021.
# SPDX-License-Identifier: MIT

"""
Experimental inference wrapper for standard AI Inference Server that feeds Vision Connector payload into a TensorFlow image classification model

"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing import image as imglib

try:
    from log_module import LogModule
    logger = LogModule()
except ImportError:
    # Fallback for local testing without log_module
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

from pathlib import Path


def _resolve_model_path() -> Path:
    file_dir = Path(__file__).resolve().parent
    # We check two folders on purpose because this script runs in two layouts:
    # 1) From source code: model is usually in ../models
    # 2) From packaged AIIS runtime: model can be in ./models
    candidates = [
        file_dir / 'models' / 'classification_mobilnet.h5',
        file_dir / '..' / 'models' / 'classification_mobilnet.h5',
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        f"classification_mobilnet.h5 not found. Checked: {[str(p.resolve()) for p in candidates]}"
    )


model = keras.models.load_model(_resolve_model_path())

# Log GPU visibility at startup so users can filter AIIS logs for "TensorFlow GPU reachable".
try:
    gpu_devices = tf.config.list_physical_devices('GPU')
    if gpu_devices:
        logger.info(f"TensorFlow GPU reachable: True. Devices: {[gpu.name for gpu in gpu_devices]}")
    else:
        logger.info("TensorFlow GPU reachable: False. No GPU devices detected.")
except Exception as ex:
    logger.warning(f"TensorFlow GPU check failed: {ex}")

IMAGE_WIDTH = 224
IMAGE_HEIGHT = 224
SCALE = 255


def predict_from_image(pil_image):
    """
    Takes an image and returns the index and the probability of the predicted class.
    """
    global IMAGE_WIDTH, IMAGE_HEIGHT, SCALE

    input_arr = imglib.img_to_array(pil_image)*1/SCALE
    assert input_arr.shape == (IMAGE_HEIGHT, IMAGE_WIDTH, 3), "The input image must contain RGB channels but no alpha."
    input_arr = np.array([input_arr], dtype=np.float32)  # Convert single image to a batch.

    predictions = model(input_arr, training=False)
    logger.info(f"Predicted class probabilities: {predictions}")

    index = np.argmax(predictions, axis=-1).item()
    return index, float(predictions[0][index])
