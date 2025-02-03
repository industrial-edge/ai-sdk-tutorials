<!--
SPDX-FileCopyrightText: Copyright (C) 2020 - 2025 Siemens AG

SPDX-License-Identifier: MIT
-->

# Howto guides

 These guides take you through the steps required to solve real-world problems.
 These guides assumes some level of understanding and working knowledge on the general ML workflow as well as the concepts of packaging ML models to run on AI Inference Server, which can be acquired by studying the [End-to-End tutorials](../e2e-tutorials/README.md)

 These tutorials provide answers to the following questions:

* [How to setup your environment to be able to run tutorials?](./00-prepare-environment.md)
  * [How to setup Windows](00-setup-windows.md)
  * [How to setup Linux](00-setup-linux.md)
  * [How to setup environment manager](00-setup-environment-manager.md)
  * [How to setup a notebook editor](00-setup-notebook-editor.md)
  * [How to setup setup environment manager environments](00-setup-environments)
* [How to define pipeline components?](01-define-components.md)
* [How to create entrypoints for AI Inference Server to be able to feed the model with data?](02-create-entrypoint.md)
* [How to use variables in pipelines?](03-use-variable-types.md)
* [How to add and handle Python dependencies?](04-handle-python-dependencies.md)
* [How to handle file resources?](05-handle-file-resources.md)
* [How to return the result of the Ml model execution?](06-return-processing-results.md)
* [How to create metrics out of processing results and how to add it to your pipeline output?](07-add-custom-metrics.md)
* [How to use pipeline parameters?](08-use-pipeline-parameters.md)
* [How to write components for older versions of AI Inference Server?](./09-old-inference-server.md)
* [How to time series signals?](10-process-timeseries-data.md)
* [How to process images?](11-process-images.md)
  * [How to use Binary format for images](./12-use-binary-format-for-images.md)
  * [How to use Object format for images](./13-use-object-format-for-images.md)
  * [How to use ImageSet format for images](./14-use-imageset-format-for-images.md)
* [How to use Tensorflow instead of Tensorflow Light](./15-use-tensorflow-instead-of-tflight.md)
* [How to version pacakges and use Pacakge ID](./16-version-packages.md)
* [How to mock AI Inference Server logger locally](./17-mock-inference-server-logging.md)
* [How to package models into an inference pipeline](./18-package-inference-pipelines.md)
* [How to test pipeline configuration package locally](./19-test-pipelines-locally.md)
* [How to convert and deploy the packaged inference pipeline to AI@Edge](./20-create-edge-configuration-package.md)
* [How to create delta packages](./21-create-delta-packages.md)
* [How to configure the GPU Runtime component](./24-configure-gpu-runtime.md)
* [How to use Azure MLOps](./25-azure-mlops.md)
