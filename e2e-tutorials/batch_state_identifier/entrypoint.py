# SPDX-FileCopyrightText: Copyright (C) Siemens AG 2021. All Rights Reserved. Confidential.
#
# SPDX-License-Identifier: MIT

import sys
import json
import numpy
import joblib

from pathlib import Path

models_dir = Path(__file__).parent.absolute() / 'models'
models_dir = models_dir.resolve()

sys.path.insert(0, str(Path('./src').resolve()))

with open(models_dir / 'bsi-model.joblib', 'rb') as rpl:
    model = joblib.load(rpl)

def process_input(data: dict):
    json_data = json.loads(data['json_data'])
    measurements = json_data['measurements']
    input_data = numpy.array([[[item['ph1'], item['ph2'], item['ph3']] for item in measurements]])
    prediction =  model.predict(input_data)
    output = {"prediction": prediction[0]}
    return output