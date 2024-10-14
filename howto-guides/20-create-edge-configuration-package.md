<!--
SPDX-FileCopyrightText: Copyright (C) 2020-2024 Siemens AG

SPDX-License-Identifier: MIT
-->

# How to convert and deploy the packaged inference pipeline to AI@Edge

> **Note**\
> In the future only edge package generation will be supported.
> You can use `pipeline.export('../packages')` to create an edge package directly.

After you create and test your pipeline configuration package, you have to convert it to an edge configuration package before you deploy it to AI Inference Server. To do, you have to

1. Use AI SDK to convert the pipeline configuration package created by AI SDK to an edge configuration package.
2. Deploy the edge configuration package on an Industrial Edge device by uploading it using the AI Inference Server application or use AI Model Manager to deploy packages to multiple AI Inference Server at once.

The rationale for the required conversion is that although a pipeline configuration package defines the inputs, outputs and inner working of an inference pipeline entirely, it does not contain all the ingredients that are necessary for executing it in AI Inference Server. To make it complete for deployment on AI Inference Server, the pipeline configuration package has to be converted to an edge configuration package.

The conversion involves, amongst others, ensuring that all required Python packages are included for the target platform. If any of the required packages, including transitive dependencies, are not included in the pipeline configuration package for the target platform, they will be downloaded from pypi.org.

The conversion function is available in AI SDK both as Python function and CLI command. Please refer to the details of function `convert_package` in module `simaticai.deployment` in the SDK API reference manual.

```python
from simaticai import deployment

[...] #component and pipeline creation

pipeline_package_path = pipeline.export('../packages')
```
