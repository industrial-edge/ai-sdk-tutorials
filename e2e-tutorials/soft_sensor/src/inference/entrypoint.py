# Copyright (C) Siemens AG 2024. All Rights Reserved. Confidential.

import joblib
import pandas
import numpy as np

with open("./model.joblib", 'rb') as rpl:
    linear_reg = joblib.load(rpl)

phC_mean = 9.0

def process_input(payload: list):
    """
    Entry point function for AI Inference Server.

    Args:
        data (dict): Dictionary that should contain the following keys: "temperature_A", "temperature_B", "temperature_C", "valve_position_A", "valve_position_B"
    Returns:
        dict: new values of velocity_A and velocity_B
    """
    
    phC_predictions = []
    for record in payload:
        df = pandas.DataFrame(record, index=[0])
        phC_predictions.append(linear_reg.predict(df))

    phC_predictions = np.array(phC_predictions).flatten()  # create a 1D numpy array
    flow_control_ratio = phC_predictions.mean() / phC_mean  # calculate the flow control ratio

    valve_position_A_values = np.array(df['valve_position_A']).flatten()
    valve_position_A = valve_position_A_values.mean() * flow_control_ratio  # adjust the valve position A

    valve_position_B_values = np.array(df['valve_position_B']).flatten()
    valve_position_B = valve_position_B_values.mean() / flow_control_ratio  # adjust the valve position B

    return {
        "valve_control_A": valve_position_A, 
        "valve_control_B": valve_position_B, 
        "predicted_phC": phC_predictions.mean()
    }
