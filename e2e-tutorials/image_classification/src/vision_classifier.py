# Copyright (C) Siemens AG 2021. All Rights Reserved. Confidential.

"""
Experimental inference wrapper for standard AI Inference Server that feeds Vision Connector payload into a TensorFlow image classification model

"""

import numpy as np
import tflite_runtime.interpreter as tflite

from log_module import LogModule
logger = LogModule()

# Load the TFLite model and allocate tensors.
interpreter = tflite.Interpreter(model_path="models/classification_mobilnet.tflite")
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

IMAGE_WIDTH = 224
IMAGE_HEIGHT = 224
IMAGE_SIZE = (IMAGE_WIDTH, IMAGE_HEIGHT)
SCALE = 255


def predict_from_image(pil_image):
    """
    Takes a PIL image, scales pixel values to range [0,1] and returns the index and the probability of the predicted class.
    """

    input_arr = np.array(pil_image)*1/SCALE
    assert input_arr.shape == (IMAGE_WIDTH, IMAGE_HEIGHT, 3), "The input image must contain RGB channels but no alpha."
    input_arr = np.array([input_arr], dtype=np.float32)  # Convert single image to a batch.

    interpreter.set_tensor(input_details[0]['index'], input_arr)
    interpreter.invoke()
    predictions = interpreter.get_tensor(output_details[0]['index'])

    logger.info(f"Predicted class probabilities: {predictions}")

    index = np.argmax(predictions, axis=-1).item()
    return index, float(predictions[0][index].item())
