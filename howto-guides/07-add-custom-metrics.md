<!--
SPDX-FileCopyrightText: Copyright (C) 2020-2024 Siemens AG

SPDX-License-Identifier: MIT
-->

# How to add custom metrics

You can implement any model metrics as component metrics that you can use to evaluate the performance of the model in the AI Model Monitor. The pipeline automatically generates the metrics as outputs that are automatically mapped to the required Databus topics. In the AI Inference Server, you only need to select Databus as the data connection for these metric outputs.

A custom metric must be defined for the component as follows:

```python
component.add_metric("ic_probability")
```

Note that the metric name must be prefixed and must contain an underscore (_) because the prefix is used to group custom metrics on the dashboard.

An output with the same name can be returned from the inference wrapper as follows:

```python
def process_input(data: dict):
    prediction, metric_value = predict(data)
    return {
        "prediction": prediction,
        "ic_probability": json.dumps({"values": metric_value})
    }
```

Once the pipeline is created, it collects the metrics from all components and delivers them as pipeline outputs. The AI Inference Server can continue to use them as output. The custom metric is displayed in the AI Inference Server as output with a pre-configured topic that needs to be connected to the Databus.

>*Note*\
You can also add custom metrics to a monitoring component provided by the AI SDK Monitoring Extension.
