<!--
SPDX-FileCopyrightText: Copyright (C) 2020 - 2024 Siemens AG
SPDX-FileCopyrightText: Copyright (C) 2020-2024 Siemens AG

SPDX-License-Identifier: MIT
-->

# How to handle file resources

File resources can be of any file type required to execute the Python code, including the Python sources themselves, such as configuration files, static data, or trained AI models stored
in `joblib` or `pickle` format

## Adding resources

For the configuration package to transfer these files to the server environment, you must specify them using the `add_resources(base_dir, resources)` method, as shown below:

```python
# the method adds 'prediction_model.joblib' from the '../models' directory file to the component

# and the file will be extracted on the server into the component folder under the 'models' directory
component.add_resources(base_dir="..", resources="models/prediction_model.joblib")

# same way we define a file 'model-config.yml' to bring into the 'config' directory
component.add_resources(base_dir="..", resources="config/modelconfig.yml")
```

Once the pipeline is imported into the AI Inference Server and the component is installed, the files in the server file system are available in the component directory and can be accessed
by the Python scripts:

```python
# data_processor.py
import yaml
import joblib
from pathlib import Path

# Our goal is to have an identical relative path to the resources in the source repository and on the server.
base_dir = Path(__file__).parents[1]

# file 'model-config.yml' is extracted into the 'config' directory
config_path = base_dir / "config/model-config.yml"
model_config = yaml.load(config_path)

# file 'prediction_model.joblib' is extracted into the 'models' directory
model_path = base_dir / "models/prediction_model.joblib"
with open(model_path, "rb") as model_file:
    model = joblib.load(model_file)
```

As loading files can be time-consuming, it is recommended to load files and ML models into memory at the initialization time of your Python code and not during the call to `process_input()`. The entry point `process_input()` should focus on processing the
incoming data as quickly as possible. We highly suggest initializing the objects that are used in this code at the beginning of the script and then using them in the functions invoked by process_input.

Please be aware that this approach can result in a massive memory load, so you have to make a trade-off between memory consumption or CPU load and response time.

After loading, the model is ready to be used to process the input data. In simple cases, this can be done directly in the entrypoint script. In the given example, we have factored this out into a module to illustrate how another module can be called from the entrypoint.

```python
# data_processor.py
def process_data(width, height):
    data=[width, height]
        class_label, confidence = model.predict(data)
        return{
            "class_label": class_label,
            "confidence": confidence
        }
```
