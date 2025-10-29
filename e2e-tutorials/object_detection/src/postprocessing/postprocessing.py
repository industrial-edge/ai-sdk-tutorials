# SPDX-FileCopyrightText: 2025 Siemens AG
#
# SPDX-License-Identifier: MIT

from image_utils import draw_prediction
from imageset import ImageSet, ImageFormat

import json
import numpy
from PIL import Image

from log_module import LogModule
logger = LogModule()

LABELS = ['DAMAGED', 'EXTRA_HOLE', 'MISSING_HOLE', 'VALID']
SCORE_THRESHOLD = 0.8

__AI_IS_IMAGE_SET_VISUALIZATION = False

"""
Main function that gets called by AIIS
"""
def process_input(data:dict):
    logger.debug(f"Payload data: {data}")
    
    try:
        iuid = data.get("iuid", None)
        boxes = data.get("boxes", None)
        labels = data.get("labels", None)
        scores = data.get("scores", None)
        input_image_set = ImageSet.from_dict(data.get("vision_payload", {}))

        holes = 0
        scratches = 0
        for i in range(len(scores)):
            if scores[i] > SCORE_THRESHOLD:
                if labels[i] == 1:
                    holes += 1
                if labels[i] == 2:
                    scratches += 1

        logger.info(f"The board with id {iuid} contains {holes} holes and {scratches} scratches.")
        prediction = "OK" if holes == 8 and scratches == 0 else "DAMAGED"

        output_payload = {}
        output_payload["prediction"] = prediction
        output_payload["result"] = json.dumps({
            "prediction": prediction,
            "holes": holes,
            "scratches": scratches,
            "message": f"The board with id '{iuid}' contains {holes} holes and {scratches} scratches."
        })

        if __AI_IS_IMAGE_SET_VISUALIZATION and input_image_set:
            # if visualization is enabled, draw the predictions on the images
            for image_detail in input_image_set.detail:
                image = image_detail.get_image_rgb()
                pil_image = Image.fromarray(image)
                draw_prediction(pil_image, boxes, labels, scores, threshold=SCORE_THRESHOLD)
                image_detail.update_image(numpy.array(pil_image), ImageFormat.RGB8)
            output_payload["visualization"] = input_image_set.to_dict()

        return output_payload

    except Exception as e:
        logger.error("exception when processing input " + str(e))
        return None

def update_parameters(parameters: dict):
    global __AI_IS_IMAGE_SET_VISUALIZATION 
    __AI_IS_IMAGE_SET_VISUALIZATION = parameters.get("__AI_IS_IMAGE_SET_VISUALIZATION", __AI_IS_IMAGE_SET_VISUALIZATION)
    logger.debug(f"__AI_IS_IMAGE_SET_VISUALIZATION has been changed to {__AI_IS_IMAGE_SET_VISUALIZATION}")
