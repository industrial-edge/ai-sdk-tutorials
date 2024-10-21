# SPDX-FileCopyrightText: Copyright (C) Siemens AG 2021. All Rights Reserved. Confidential.
#
# SPDX-License-Identifier: MIT

"""
Experimental inference wrapper for standard AI Inference Server that feeds Vision Connector payload into a TensorFlow image classification model

"""

import numpy as np
from tensorflow import keras
from tensorflow.keras.preprocessing import image as imglib

from log_module import LogModule
logger = LogModule()

model = keras.models.load_model('models/classification_mobilnet.h5')

IMAGE_WIDTH = 224
IMAGE_HEIGHT = 224
IMAGE_SIZE = (IMAGE_WIDTH, IMAGE_HEIGHT)
SCALE = 255


def predict_from_image(pil_image):
    """
    Takes a PIL image and returns the index and the probability of the predicted class.
    """
    global IMAGE_WIDTH, IMAGE_HEIGHT, SCALE

    input_arr = imglib.img_to_array(pil_image)*1/SCALE
    assert input_arr.shape == (IMAGE_WIDTH, IMAGE_HEIGHT, 3), "The input image must contain RGB channels but no alpha."
    input_arr = np.array([input_arr], dtype=np.float32)  # Convert single image to a batch.

    predictions = model(input_arr, training=False)
    logger.info(f"Predicted class probabilities: {predictions}")

    index = np.argmax(predictions, axis=-1).item()
    return index, float(predictions[0][index])
