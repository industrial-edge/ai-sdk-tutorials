# SPDX-FileCopyrightText: Siemens AG 2021.
# SPDX-License-Identifier: MIT

import sys
import json
from pathlib import Path
import cv2
import numpy as np

try:
    from log_module import LogModule
    logger = LogModule()
except ImportError:
    # Fallback for local testing without log_module
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

sys.path.insert(0, str(Path('./src').resolve()))
import vision_classifier as classifier
from imageset import ImageSet, ImageFormat

IMAGE_WIDTH:  int = 224
IMAGE_HEIGHT: int = 224
IMAGE_SIZE: tuple = (IMAGE_WIDTH, IMAGE_HEIGHT)

CLASS_LABELS: list = ['ET200AL', 'ET200ecoPN', 'ET200sp', 'S7_1200', 'S7_1500']

VISUALIZATION_IS_SET: bool = False

def update_parameters(params: dict):
    """
    Update parameters for the image classifier.

    Args:
        params (dict): Dictionary containing parameters to update.
    """
    global VISUALIZATION_IS_SET
    VISUALIZATION_IS_SET = params.get("__AI_IS_IMAGE_SET_VISUALIZATION", VISUALIZATION_IS_SET)
    
    logger.info(f"Updated parameters: {VISUALIZATION_IS_SET = }")
    
def update_image(imageset: ImageSet, restored_image: np.ndarray, text_to_show: str):
    """
    Updates the imageset with the processed image and additional details.
    Args:
        imageset (ImageSet): The imageset dictionary to update.
        restored_image (np.ndarray): The processed image in RGB format.
        text_to_show (str): The text to overlay on the image.
    Returns:
        dict: The updated imageset with the processed image and details."""

    image_with_label = cv2.putText(restored_image.copy(), text_to_show, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, .4, (0, 0, 0), 2)
    image_with_label = cv2.putText(image_with_label.copy(), text_to_show, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, .4, (255, 255, 255), 1)
    imageset.detail[0].update_image(image_with_label, ImageFormat.BGR8)

    return imageset.to_dict()

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


    imageset:ImageSet = ImageSet.from_dict(data.get("vision_payload", {}))

    for image_detail in imageset.detail:
        try:
            restored_image = image_detail.get_image_rgb()
            restored_image = cv2.resize(restored_image, IMAGE_SIZE)
            prediction, confidence = classifier.predict_from_image(restored_image)
            logger.debug(f"Predicted class: {prediction} (probability: {confidence})")
            result = {
                "prediction": CLASS_LABELS[prediction],
                "ic_probability": metric_output(confidence),
            }
            if VISUALIZATION_IS_SET:
                text_to_show = f"Predicted: {CLASS_LABELS[prediction]} ({confidence:.4f})"
                result["image_to_show"] = update_image(imageset, restored_image, text_to_show)
            return result
        except BaseException as e:
            logger.warning(f"Error decoding image from vision payload. Image ID: '{image_detail.id}' Exception:{e}")

    return None

def metric_output(v: float):
    return json.dumps({"value": v})
