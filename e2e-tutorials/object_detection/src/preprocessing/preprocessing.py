import numpy
import cv2

try:
    from log_module import LogModule
    logger = LogModule()
except: 
    import logging
    logger = logging.getLogger(__name__)
    logger.setLevel('DEBUG')

COLORS = 1
WIDTH = 224
HEIGHT = 224

def process_input(data:dict):
    try:
        payload = {}
        image_set = data["vision_payload"]
        
        image_details = image_set['detail']
        iuid = None
        inputs = []

        for image_detail in image_details:
            payload["iuid"] = image_detail.get('id', 'no-id')
            width = image_detail.get("width", WIDTH)
            height = image_detail.get("height", HEIGHT)

            if width != WIDTH or height != HEIGHT:
                logger.warn(f"Image {payload['iuid']} was dropped because of wrong size {width} X {height}")
                return None

            image_data = numpy.frombuffer(image_detail['image'], dtype=numpy.uint8)  # BayerRG8, (height x width, )
            image_data = image_data.reshape(height, width)                           # BayerRG8, (height, width)
            image_data = cv2.cvtColor(image_data, cv2.COLOR_BayerRG2RGB)             # RGB, (width, height, 3)
            image_data = image_data.transpose(2,0,1)                                 # RGB, (3, width, height)
            image_data = image_data.astype(numpy.float32) / 255.0                    # RGB, (3, width, height)

            inputs.append(image_data.ravel())

        inputs = numpy.array(inputs).ravel()
        logger.debug(f"inputs shape and length: {inputs.shape} {len(inputs)}")

        if inputs is not None:
            payload["input"] = inputs
            if iuid is not None:
                payload["iuid"] = iuid
            return payload
        else:
            return None
    except Exception as e:
        logger.error("exception [process_input]:"+str(e))
        return None
