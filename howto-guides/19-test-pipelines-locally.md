<!--
SPDX-FileCopyrightText: Copyright (C) 2020 - 2025 Siemens AG

SPDX-License-Identifier: MIT
-->

# How to test edge configuration package locally

​Once you have created your pipeline configuration, you can export it as an Edge configuration package and deploy it directly to the AI Inference Server.
**However, we strongly recommend that you test the edge configuration package before deploying it.**
The benefits of local testing are the following:

- You can figure out many potential problems quicker, as you don't have to go through a deployment cycle.
- You can diagnose and troubleshoot problems much easier, as you can inspect artifacts in your development environment.
- You can validate your fixes quicker and move on to further issues that could not surface yet due to earlier problems.
- You can easily include the local pipeline tests into the test automation in your build process.

In general, we encourage you to apply state-of-the-art software engineering practices, such as unit testing and test driven development.
This means that ideally you have already in place automated unit or even integration tests that make sure that the Python code and the
saved models work according to expectations in isolation. This helps you localize errors when you put these pieces together and integrate them as an edge configuration package.

AI SDK package `simaticai.testing` provides two tools for local testing:

- A pipeline validator, that performs a static validation of the package concerning the availability of required
  Python packages.
- A pipeline runner, that lets you simulate the execution of your pipeline in your Python environment.

## Dependency validation of a pipeline configuration

When the pipeline is exported as an edge package, the following checks are automatically performed:

- Verifying that the Python version required in the package is supported by a known version of AI Inference Server.
- Verifying that all the required Python packages exist for the target platform and are included in the edge package.

For concrete programming details, please refer to the SDK API reference manual.

## Local execution of a packaged pipeline

Class `LocalPipelineRunner` in submodule `simaticai.testing.pipeline_runner` can be used to locally mimic the behavior of the AI Inference Server concerning loading and running inference pipelines. This is a quick and easy way to find programming or configuration errors before deploying the package.

The local pipeline runner performs the simulation of the server environment as follows.

1. It unpacks the pipeline components into a test folder, similar to how it would happen on the inference server.
2. It creates for each component an own Python virtual environment.
3. It installs required Python packages from the wheels if provided in the package or from `pypi.org`.
4. It installs a mock of the `log_module` (see [Mocking the logger of AI Inference Server](17-mock-inference-server-logging.md))
5. It updates pipeline parameters if applicable
6. It feeds the pipeline with input data by triggering the entrypoints of the components accordingly.
7. It collects the sequence of pipeline outputs for a given sequence of pipeline inputs.

The local pipeline runner also lets you exercise your pipeline component by component. In other words, you can feed single components with inputs and verify the output produced.

If the pipeline has parameters, they will be supplied with their default values. You can also change parameter values using the `update_parameters()` method. This way you can test your pipeline with different parameters. You can use this method before calling `run_component()` or `run_pipeline()` but you cannot change pipeline parameters while these methods
are running.

From a test strategy and risk based testing point of view, we suggest that you verify the business logic within the pipeline components in unit tests as with any ordinary Python program, and use the local pipeline runner to cover test risks such as:

- Mismatch between pipeline and component input and output variable names.
- Required Python packages not covered by `requirements.txt`.
- Source or other files missing from the package.
- Interface mismatch between subsequent pipeline components.
- Entrypoint cannot consume input data due to data format mismatch.
- Entrypoint produces output data in wrong format.
- For some reason, the pipeline doesn't work end-to-end as intended.

One crucial point for making the local test faithful concerning data input and output formats is understanding how data connections in AI Inference
Server work. The following data connection types are straightforward:

- Databus
- External Databus
- IE Vision Connector

For these data connection types, AI Inference Server passes the MQTT payload string directly as the value of the connected pipeline input variable. In many use cases where you use this data connection type, your pipeline has a single input variable of type string. This means that you must pass local pipeline runner a Python dictionary with a single element.

Taking the pipeline from the Image Classification project template for example, you have a single input variable `vision_payload`. To run your
pipeline for two consecutive input images, you must invoke the pipeline runner like this:

```python
pipeline_input1 = { 'vision_payload': mqtt_payload1 }
pipeline_input2 = { 'vision_payload': mqtt_payload2 }
pipeline_output = runner.run_pipeline([pipeline_input1, pipeline_input2])
```

For a complete code example that shows how to feed a pipeline with a single string input variable in a local test, see the Local Pipeline Test Notebook in the Image Classification project template.

​The SIMATIC S7 Connector data connection type requires more attention. This connector is typically used in time series use cases. Using this connection, the AI Inference Server processes the MQTT payload used by the S7 Connector and only passes on the values of the PLC variables, but not the metadata. So, if you intend to use your pipeline with the S7 connector, you need to feed it with dictionaries holding the PLC tag values.

Taking the pipeline from the State Identifier project template for example, you have input variables `ph1`, `ph2` and `ph3`, which are meant to
be used with the SIMATIC S7 Connector data connection type. To mimic how AI Inference Server feeds the pipeline, you must call the pipeline
runner like this:

```python
pipeline_input1 = {'ph1': 4732.89, 'ph2': 4654.44, 'ph3': 4835.02}
pipeline_input2 = {'ph1': 4909.13, 'ph2': 4775.16, 'ph3': 4996.67}
pipeline_output = runner.run_pipeline([pipeline_input1, pipeline_input2])
```

For a complete code example that shows how to feed a pipeline with an input line of PLC tag values in a local test, see the Local Pipeline Test Notebook in the State Identifier project template.

## Restrictions of local pipeline execution

The local runner works with batches of input data and processes the whole input batch component by component. In other words, given a sequence
of pipeline inputs, the entire sequence is first processed by the first components, and only then is the output of the first component processed
by the second component. This is different from the runtime environment on AI Inference Server, where the components in the pipeline potentially
start consuming input as soon as the preceding component has produced output.

You cannot fully test input and output data formats, as these depend on the data connection settings in AI Inference Server, and you have to provide
the local runner the input data in the representation that matches the output side of the connector. This means that if your assumptions
on the data connection settings or the resulting data formats are wrong, your tests will provide misleading results, too.

The local runner can only simulate linear pipelines, where the pipeline input variables are only used by one component, each component uses only the outputs of the previous components, and the pipeline output only consists of variables from the last component.

Furthermore, the results obtained in local tests are not fully representative for AI Inference Server, including but not limited to the following aspects:

- The local version of Python might differ from that in the Inference Server.
- The local architecture might differ, resulting in different builds of imported Python packages being used.
- The local runner executes only one instance of the Python code, regardless of the parallelism setting in the configuration.

Despite all these limitations, we would like to highlight again our recommendation to test your pipeline locally before deploying it.
Most likely it will save you more time and trouble compared to skipping this step.
