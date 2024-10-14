import numpy as np
import json

from log_module import LogModule
logger = LogModule()

LABELS = ['DAMAGED', 'EXTRA_HOLE', 'MISSING_HOLE', 'VALID']

data_aggregator = {}

"""
Main function that gets called by AIIS
"""
def process_input(data:dict):
    logger.debug(f"Payload data: {data}")
    
    try:
        iuid = data.get("iuid", None)
        image_input = data.get("input", None)
        boxes = data.get("boxes", None)
        labels = data.get("labels", None)
        scores = data.get("scores", None)

        holes = 0
        scratches = 0
        for i in range(len(scores)):
            if scores[i] > 0.8:
                if labels[i] == 1:
                    holes += 1
                if labels[i] == 2:
                    scratches +=1

        print(f"The board contains {holes} holes and {scratches} scratches.")
        prediction = "OK" if holes == 8 and scratches == 0 else "DAMAGED"

        return {
            "prediction": prediction,
            "result": json.dumps({
                    "prediction": prediction,
                    "holes": holes,
                    "scratces": scratches,
                    "message": f"The board with id '{iuid}' contains {holes} holes and {scratches} scratches."
                })
        }
    except Exception as e:
        logger.error("exception when processing input"+str(e))
        return None
   
