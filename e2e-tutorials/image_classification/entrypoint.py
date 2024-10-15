# SPDX-FileCopyrightText: Copyright (C) Siemens AG 2021. All Rights Reserved. Confidential.
#
# SPDX-License-Identifier: MIT

import sys
import json
from pathlib import Path
from PIL import Image
import cv2
import numpy

from log_module import LogModule
logger = LogModule()


sys.path.insert(0, str(Path('./src').resolve()))
import vision_classifier as classifier
from payload import create_image_output


IMAGE_WIDTH = 224
IMAGE_HEIGHT = 224
IMAGE_SIZE = (IMAGE_WIDTH, IMAGE_HEIGHT)

def process_input(data: dict):
    """
    Entry point function for AI Inference Server.
    First, this method creates PIL image object, resized to the input shape of the network.
    Then returns a prediction from the created pillow image.

    Args:
        data (dict): Dictionary that should contain the key 'vision_payload' that holds the Vision Connector payload.
    Returns:
        dict: A dictionary with the key 'prediction' that holds the index of the predicted class as an integer string.
    """

    image_set = data["vision_payload"]["detail"]

    for image in image_set:
        width = image["width"]
        height = image["height"]
        image_bytes = image["image"]
        image_id = image['id']
        try:
            if "BayerRG8" != image["format"]:
                logger.warning(f"Unsupported image format: {image['format']}")
                return None
            
            converted_image = numpy.frombuffer(image_bytes, dtype=numpy.uint8) 
            converted_image = converted_image.reshape(height, width)
            converted_image = cv2.resize(converted_image, IMAGE_SIZE)          
            converted_image = cv2.cvtColor(converted_image, cv2.COLOR_BayerRG2RGB)
            
            prediction, probability = classifier.predict_from_image(converted_image)
            logger.debug(f"Predicted class: {prediction} (probability: {probability})")
            return {
                "prediction": str(prediction),
                "ic_probability": metric_output(probability),
            }
        except BaseException as e:
            logger.warning(f"Error decoding image from vision payload. Image ID: '{image_id}' Exception:{e}")

    return None

def metric_output(v: float):
    return json.dumps({"value": v})
