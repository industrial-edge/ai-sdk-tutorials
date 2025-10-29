# SPDX-FileCopyrightText: 2025 Siemens AG
#
# SPDX-License-Identifier: MIT

import numpy

from imageset import ImageSet

try:
    from log_module import LogModule
    logger = LogModule()
except: 
    import logging
    logger = logging.getLogger(__name__)
    logger.setLevel('DEBUG')

WIDTH = 224
HEIGHT = 224

def process_input(data:dict):
    try:
        payload = {}
        image_set = ImageSet.from_dict(data.get("vision_payload", {}))
        iuid = None

        inputs = []
        for image_detail in image_set.detail:
            iuid = image_detail.id
            width = image_detail.width
            height = image_detail.height

            if width != WIDTH or height != HEIGHT:
                logger.warning(f"Image {iuid} was dropped because of wrong size {width} X {height}")
                return None
            
            image_data = image_detail.get_image_rgb()              # RGB, (height, width, 3)
            image_data = image_data.transpose(2,1,0)               # RGB, (3, width, height)
            image_data = image_data.astype(numpy.float32) / 255.0  # RGB, (3, width, height)

            inputs.append(image_data.ravel())

        inputs = numpy.array(inputs).ravel()
        logger.debug(f"inputs shape and length: {inputs.shape} {len(inputs)}")

        if inputs is not None:
            payload["input"] = inputs
            payload["vision_payload"] = data.get("vision_payload", {})
            if iuid is not None:
                payload["iuid"] = iuid
            return payload
        else:
            return None

    except Exception as e:
        logger.error("exception [process_input]:"+str(e))
        return None

def update_parameters(parameters: dict):
    # To avoid warning about missing update_parameters implementation
    pass
