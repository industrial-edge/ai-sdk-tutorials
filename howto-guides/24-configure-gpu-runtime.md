<!--
SPDX-FileCopyrightText: Copyright (C) 2020 - 2024 Siemens AG
SPDX-FileCopyrightText: Copyright (C) 2020-2024 Siemens AG

SPDX-License-Identifier: MIT
-->

# How to configure the GPU Runtime component

AI Inference Server supports GPU acceleration for executing pipelines that include a GPU Runtime component. This component is specifically designed to execute ONNX models on the GPU, as ONNX models are the only supported model type in AI Inference Server. Additionally, the GPU Runtime component offers various configuration options to optimize the model's performance on the GPU. 

Besides specifying a model, the edge package must contain a model configuration file, that defines specific behavior of the model execution, like

- batching
- model warmup

AI SDK allows you to configure both batching and model warm-up during pipeline creation.

## Configure batching

Batching information is extracted from the model, but a `max_batch_size` value between 0 and the maximum supported by the model must be provided.

```python
    from simaticai.deployment import GPURuntimeComponent
    from simaticai.helpers import model_config
    component = GPURuntimeComponent()
    component.use_model(path_to_model, max_batch_size)
```

Additional knowhow is available in guide [26 - Parallel Execution and Batch Processing](./26-parallel-execution-and-batch-processing.md)

## Configure model warmup

Model warmup is disabled by default. If enabled, the strategy can be zero data or random data.

```python
    from simaticai.deployment import GPURuntimeComponent
    from simaticai.helpers import model_config
    component = GPURuntimeComponent()
    # No warmup
    component.use_model(path_to_model, max_batch_size)
    component.use_model(path_to_model, max_batch_size, model_config.Warmup.DISABLED)
    # Warmup with zero data
    component.use_model(path_to_model, max_batch_size, model_config.Warmup.ZERO_DATA)
    # Warmup with random data
    component.use_model(path_to_model, max_batch_size, model_config.Warmup.RANDOM_DATA)
```

Alternatively, AI SDK allows you to replace the AI SDK generated configuration file with a handwritten one.

## Handwritten configuration file

For detailed configuration options consult the [model configuration instructions](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_configuration.html)

To attache a model configuration file to the `component` use the `use_config()` method

```python
    from simaticai.deployment import GPURuntimeComponent
    from simaticai.helpers import model_config
    component = GPURuntimeComponent()
    component.use_model(path_to_model, max_batch_size)
    component.use_config(path_to_config_file)
```
