# SPDX-FileCopyrightText: 2025 Siemens AG
# SPDX-License-Identifier: MIT

import sys
import json
from pathlib import Path
import cv2
import numpy as np

from log_module import LogModule
logger = LogModule()

sys.path.insert(0, str(Path('./src').resolve()))
import vision_classifier as classifier

IMAGE_WIDTH = 224
IMAGE_HEIGHT = 224
IMAGE_SIZE = (IMAGE_WIDTH, IMAGE_HEIGHT)

CLASS_LABELS = ['ET200AL', 'ET200ecoPN', 'ET200sp', 'S7_1200', 'S7_1500']


def restore_image_from_bytes(image_bytes, width, height, format):
    """
    Converts image bytes to a numpy array and reshapes it based on the specified format.

    Args:
        image_bytes (bytes): The raw image data in bytes.
        width (int): The width of the image.
        height (int): The height of the image.
        format (str): The format of the image: 'Mono8', 'BayerRG8', 'BayerGR8', 'BayerBG8', 'BayerGB8',
            'RGB', 'RGB8', 'BGR', 'BGR8', 'YUV422Packed', or 'YUV422_YUYV_Packed'.
    Returns:
        np.ndarray: The converted image as a numpy array in RGB format, or None if the format is unsupported.
    """

    restored_image = np.frombuffer(image_bytes, dtype=np.uint8)

    # Reshape the image data based on the height and width
    match format:
        case "Mono8" | "BayerRG8" | "BayerGR8" | "BayerBG8" | "BayerGB8":
            restored_image = restored_image.reshape(height, width)
        case "RGB" | "RGB8" | "BGR" | "BGR8":
            restored_image = restored_image.reshape(height, width, 3)
        case "YUV422Packed" | "YUV422_YUYV_Packed":
            restored_image = restored_image.reshape(height, width, 2)
        case _:
            logger.warning(f"Unsupported image format: {format}")
            return None

    # Convert the image to RGB format.
    match format:
        case "BGR" | "BGR8":
            restored_image = cv2.cvtColor(restored_image, cv2.COLOR_BGR2RGB)
        case "Mono8":
            restored_image = cv2.cvtColor(restored_image, cv2.COLOR_GRAY2RGB)
        case "BayerRG8":
            restored_image = cv2.cvtColor(restored_image, cv2.COLOR_BayerRG2RGB)
        case "BayerGR8":
            restored_image = cv2.cvtColor(restored_image, cv2.COLOR_BayerGR2RGB)
        case "BayerBG8":
            restored_image = cv2.cvtColor(restored_image, cv2.COLOR_BayerBG2RGB)
        case "BayerGB8":
            restored_image = cv2.cvtColor(restored_image, cv2.COLOR_BayerGB2RGB)
        case "YUV422Packed":
            restored_image = cv2.cvtColor(restored_image, cv2.COLOR_YUV2RGB_Y422)
        case "YUV422_YUYV_Packed":
            restored_image = cv2.cvtColor(restored_image, cv2.COLOR_YUV2RGB_YUYV)
    
    return restored_image

def process_input(data: dict):
    """
    Entry point function for AI Inference Server.
    First, this method creates an image object, converted to RGB and resized to the input shape of the network.
    Then returns a prediction from the created image.

    Args:
        data (dict): Dictionary that should contain the key 'vision_payload' that holds the Vision Connector payload.
    Returns:
        dict: A dictionary with the key 'prediction' that holds the index of the predicted class as an integer string.
    """

    image_detail = data["vision_payload"]["detail"]

    for image in image_detail:
        width = image["width"]
        height = image["height"]
        image_bytes = image["image"]
        image_id = image['id']
        try:
            restored_image = restore_image_from_bytes(image_bytes, width, height, image["format"])
            restored_image = cv2.resize(restored_image, IMAGE_SIZE)
            prediction, probability = classifier.predict_from_image(restored_image)
            logger.debug(f"Predicted class: {prediction} (probability: {probability})")
            return {
                "prediction": CLASS_LABELS[prediction],
                "ic_probability": metric_output(probability),
            }
        except BaseException as e:
            logger.warning(f"Error decoding image from vision payload. Image ID: '{image_id}' Exception:{e}")

    return None

def metric_output(v: float):
    return json.dumps({"value": v})
