# SPDX-FileCopyrightText: 2025 Siemens AG
#
# SPDX-License-Identifier: MIT

import json
from ultralytics import YOLO, __version__ as ultralytics_version
import cv2
import torch

from imageset import ImageSet, ImageFormat

__AI_IS_IMAGE_SET_VISUALIZATION = False


try:
    from log_module import LogModule
    logger = LogModule()
except: 
    import logging
    logger = logging.getLogger(__name__)
    logger.setLevel('DEBUG')

model_name = "yolo11n-seg.pt"
model = YOLO(model_name)

try:
    logger.info(f"Ultralytics version: {ultralytics_version}")
    logger.info(f"PyTorch version: {torch.__version__}")
    logger.info(f"Built with CUDA: {torch.version.cuda}")
    if torch.cuda.is_available():
        device_names = [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())]
        logger.info(f"PyTorch GPU reachable: True. Devices: {device_names}")
    else:
        logger.info("PyTorch GPU reachable: False. No GPU devices detected.")
except Exception as ex:
    logger.warning(f"PyTorch GPU check failed: {ex}")

def calculate_areas(result):
    areas = []

    class_ids = result.boxes.cls.int().tolist()
    masks = result.masks.data

    for class_id, mask in zip(class_ids, masks):
        class_label = result.names[class_id]
        mask_area = mask.sum().item()
        total_area = mask.numel()
        relative_area = mask_area / total_area
        areas.append({"class": class_label,
                      "relative_area": relative_area,
                      "text": f"Detected {class_label} occupying {relative_area * 100.0:.1f}% of the image."})
    return areas


def process_input(input_payload: dict):
    try:
        # Load the image from the input payload
        image_set = ImageSet.from_dict(input_payload.get("vision_payload", {}))
        image = image_set.get_image_rgb()
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        logger.debug(f"Image shape: {image.shape}")

        # Run the model on the input image
        result = model(image)
        result = result[0]  # Get the first (and only) result from the list

        # Prepare the output payload
        output_payload = {}
        output_payload["iuid"] = str(image_set.detail[0].id)
        output_payload["areas"] = json.dumps(calculate_areas(result))

        if __AI_IS_IMAGE_SET_VISUALIZATION:
            logger.info("Image set visualization is enabled.")
            result_img = result.plot()
            result_img = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
            # Replace the original image with the result image in ImageSet
            image_set.detail[0].update_image(result_img, ImageFormat.RGB8)
            output_payload["result_image_set"] = image_set.to_dict()

        return output_payload

    except Exception as e:
        logger.error("exception [process_input]:" + str(e))
        return None


def update_parameters(parameters: dict):
    global __AI_IS_IMAGE_SET_VISUALIZATION 
    __AI_IS_IMAGE_SET_VISUALIZATION = parameters.get("__AI_IS_IMAGE_SET_VISUALIZATION", __AI_IS_IMAGE_SET_VISUALIZATION)
    logger.debug(f"__AI_IS_IMAGE_SET_VISUALIZATION has been changed to {__AI_IS_IMAGE_SET_VISUALIZATION}")
