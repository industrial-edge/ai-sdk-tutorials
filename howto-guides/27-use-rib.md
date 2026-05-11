<!--
SPDX-FileCopyrightText: 2025 Siemens AG

SPDX-License-Identifier: MIT
-->
# How to use RIB

RIB, or Real-time Information Backbone, is a high-performance communication protocol developed by Siemens. Its primary goal is to enable fast, low-latency, and low-jitter data exchange between applications running on the same device, especially when interacting with PLCs.

The RIB cycle time is a crucial setting that defines the expected frequency at which data is updated or read within the RIB system. It's measured in milliseconds and acts as a vital parameter for managing real-time data flow and ensuring optimal system performance.

For Data Providers (e.g., AI Inference Server sending data to a PLC), the cycle time specifies how often the provider should publish new data. Adhering to this helps maintain data consistency for consumers.

For Data Consumers (e.g., AI Inference Server receiving data from a PLC), the cycle time dictates how often the consumer should attempt to read new data. This ensures that AI Inference Server processes information promptly.

!!! info "Cycle time of PLCs"
    PLCs have their own cycle time. If AI Inference Server is used as a data consumer, it is recommended to set the cycle time to half the PLC's cycle time, ensuring that no data sent by the PLC is lost.

## How to preconfigure AI SDK pipeline with RIB

For more information on pipeline preconfiguration, refer to the [Pipeline Mapping Preconfiguration tutorial](https://github.com/industrial-edge/ai-sdk-tutorials/blob/main/howto-notebooks/pipeline-mapping-preconfiguration/pipeline-mapping.ipynb).

Starting from version 2.8.0, AI SDK supports preconfiguration of RIB connections on pipeline input and output variables.

```python
from simaticai.deployment import PythonComponent, Pipeline
from simaticai.payloads import Connection, ConnectionTypeAndPayloadFormat as CPT

component = PythonComponent(name="python_component")
# Setting various attributes of the component: resources, entrypoint, dependencies, etc.
# ...
component.add_input("rib_input", _type="Double")
component.add_input("rib_output", _type="Double")
# ...
pipeline = Pipeline.from_components([component], name="my_pipeline")

# preconfiguring RIB connection
rib_connection = Connection(name="RIB connection", cptype=CPT.Realtime_Information_Backbone)

pipeline.inputs[0].add_mapping_with_connection(rib_connection, tagName="RIB_input_tagname")
pipeline.outputs[0].add_mapping_with_connection(rib_connection, tagName="RIB_output_tagname")
```

Note that each pipeline needs this specific setting of cycle time that defines in which interval the RIB symbols will be updated.

## How to set RIB cycle time in AI SDK

AI SDK provides a straightforward way to configure the RIB cycle time for your pipelines using the `set_rib_cycle_time` function:

```python
pipeline.set_rib_cycle_time(cycle_time_msec=100)  # Sets the cycle time to 100 milliseconds
```

The recommended range for RIB cycle time is between 1 and 1000 milliseconds. Values outside this range will trigger a warning, as short cycle time can lead to high utilization of the CPU, while high cycle time can potentially lead to data loss.

Lower than 0.001 milliseconds triggers an error message, and the pipeline creation fails.

!!! info "Stored unit in generated configuration"
    Although the set_rib_cycle_time() function accepts integers and floats in milliseconds, the pipeline config file stores this value for AI Inference Server in microseconds, rounded to the nearest integer. AI Inference Server expects to receive this value in microseconds, thus no action is needed from user perspective.

## Choosing an initial cycle time

!!! info "Cycle time of PLCs"
    PLCs have their own cycle time. If AI Inference Server is used as a data consumer, it is recommended to set the cycle time to half the PLC's cycle time, ensuring that no data sent by the PLC is lost.

Use this baseline when tuning cycle time:

- Start with `50` ms for first integration tests.
- Reduce stepwise only if your use case needs lower latency.
- Increase stepwise if CPU load rises or unstable processing appears.
- Validate throughput, CPU utilization, and missed data indications after each change.

## Verifying your setup

After deployment, check the following:

- Pipeline starts without cycle-time validation errors.
- CPU load on AI Inference Server remains stable.
- Expected data update frequency is achieved.
- No signs of dropped or stale values in downstream processing.

If you observe high CPU load, increase cycle time. If you observe stale or skipped data, reduce cycle time within the recommended range and retest.
