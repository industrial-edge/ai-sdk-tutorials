# Copyright (C) Siemens AG 2021. All Rights Reserved. Confidential.

"""
This module contains two methods for executing a scikit-learn pipeline on the AI Inference Server.
The pipeline is stored as a pickle file and contains preprocessing steps to form windowed data and to extract features from these data.

When the module is loaded, it reads the pickle file and gets some information from it, such as:
    - window_size
    - window_step
    - input_columns
    - output_name

The AI Inference Server will call the 'run(..)' method with the values for one datapoint in JSON format.
The 'run' method collects these data until the window_size is reached.
Once a sufficient amount of data has been collected, the 'predict(..)' method will be called.
This method will produce a prediction which will be forwarded to the Runtime as a JSON.

"""

from pathlib import Path
import json
import numpy
import joblib

from log_module import LogModule
logger = LogModule()

models_dir = Path(__file__).parent.absolute() / '../../models'
models_dir = models_dir.resolve()

logger.info(f"Loading model {Path(models_dir / 'clustering-model.joblib').resolve()}")
with open(models_dir / 'clustering-model.joblib', 'rb') as rpl:
    pipe = joblib.load(rpl)
logger.info("Model loaded")

window_size = pipe.get_params().get('preprocessing__windowing__window_size')
step_size = pipe.get_params().get('preprocessing__windowing__window_step')

input_columns = ["ph1", "ph2", "ph3"]

output_name = "prediction"

aggregated_data = numpy.empty((0, len(input_columns)), int)


def update_parameters(params: dict):
    """
    This method is triggered by the AI Inference Server on the Edge ecosystem.
    The method updates the value of a given parameter.

    Args:
        params (dict): Names and values of parameters to update given in this format:
        {"parameter_name": parameter_value}
    """
    global step_size

    step_size = params.get("step_size", step_size)


def process_data(input_dict: dict):
    """
    This method is triggered by AI Inference Server.
    The caller method pushes the aggregated values for the input columns as a dictionary and reads the output columns from a dictionary.
    The dictionary keys and values come from the name of the input columns and from the record data.

    Args:
        input_dict (dict): Input data collected in a dictionary like:
        {"ph1": 10000.0, "ph2": 9879.2, "ph3": 7514.3}  # in this case 'input_columns' = ['ph1','ph2','ph3']

    Returns:
        [int]: The index of the predicted class if the input completes a window and an inference was made.
               None if the input was accumulated but the windows size was not reached.
    """
    global aggregated_data, logger
    values = [[numpy.nan if input_dict[variable] is None else input_dict[variable] for variable in input_columns]]
    aggregated_data = numpy.append(aggregated_data, values, axis=0)

    if len(aggregated_data) >= window_size:
        output = {output_name: predict(pipe, aggregated_data)}
        features = pipe["preprocessing"].transform(aggregated_data)[0]
        output["model_input_max"]  = metric_output(features[0].item())
        output["model_input_min"]  = metric_output(features[1].item())
        output["model_input_mean"] = metric_output(features[2].item())
        aggregated_data = aggregated_data[step_size:]
        return output

    return None


def predict(pipe: dict, model_input: numpy.array):
    """
    Called by 'process_data(..)'. This method gets the scikit-learn Pipeline and the aggregated data for the window, then predicts the class.

    Args:
        pipe (sklearn.pipeline.Pipeline): The trained scikit-learn Pipeline
        model_input (numpy.array): The aggregated data for the data window

    Returns:
        [int]: The index of the predicted class
    """

    prediction = pipe.predict(model_input)

    return prediction[0]

def metric_output(v: int or float):
    return json.dumps({"value": v})
