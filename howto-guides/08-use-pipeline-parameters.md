<!--
SPDX-FileCopyrightText: Copyright (C) 2020 - 2024 Siemens AG

SPDX-License-Identifier: MIT
-->

# How to use pipeline parameters

If a component is used in a pipeline with parameters, the component must provide an `update_parameters()` function to handle parameter updates. AI Inference Server calls `update_parameters()` at least once after the pipeline has been started. However, before passing the first input to the `update_parameters()` component, it can be called again if pipeline parameters are changed while the pipeline is running. AI Inference Server ensures that calls to update_parameters()` and `process_input()` do not occur at the same time.

## Parameters to be changed on the user interface

Use individual parameters if you intend to let the operator change pipeline parameters interactively in the AI Inference Server user interface. For each parameter, you must define the name, default value, and type.

```python
# define individual parameters for the pipeline
pipeline.add_parameter('windowSize', 300, 'Integer')
pipeline.add_parameter('windowStepSize', 75, 'Integer')
```

In this way, the AI Inference Server provides individual input fields for each parameter on its user interface. In the handler function, the parameters can be retrieved as individual dictionary elements from the function parameters.

```python
# entrypoint.py
def update_parameters(params: dict):
    windowSize = params['windowSize']
    windowStepSize = params['windowStepSize']
```

## Parameters to be changed via MQTT

If you need to change pipeline parameters programmatically by sending MQTT messages, use a single composite parameter of type String and combine multiple parameters into JSON.
For the AI Inference Server to provide parameter values from an MQTT topic, you must enable this function by passing True as an additional, fourth argument.

```python
# define compound JSON parameter for the pipeline
pipeline.add_parameter('windowing', json.dumps({'windowSize': 300, 'stepSize': 75}), 'String', True)
```

Therefore, the AI Inference Server allows you to map this parameter to an MQTT topic, which is similar to the method of mapping input and output variables. In the handler function, the parameters can be retrieved by first unfolding the JSON in the individual formal pipeline parameter into a dictionary, then they can be accessed individually.

```python
def update_parameters(params: dict):
    windowing = json.loads(params['windowing'])
    windowSize = windowing['windowSize']
    windowStepSize = windowing['stepSize']
```
