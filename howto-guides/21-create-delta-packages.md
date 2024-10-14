<!--
SPDX-FileCopyrightText: Copyright (C) 2020-2024 Siemens AG

SPDX-License-Identifier: MIT
-->

# How to create Delta packages

An edge configuration package can be large in size, and the time of deployment strongly correlates with this size. To reduce this time, AI Inference Server is able to create a new version of a pipeline form an original version and a delta package.
A delta package only contains the files which are updated or newly added compared to the original version.

AI SDK lets you create a delta configuration package using function `create_delta_package` in module `simaticai.deployment` or the corresponding CLI command. Please refer to the details in the SDK API reference manual.

The deployment of a delta configuration package works similarly to the upload of an edge configuration package. The only prerequisite is that the original version of the pipeline must be imported on AI Inference Server before the delta.

```python
old_package_path = Path('../packages/MyPipeline-edge_1.zip')
new_package_path = Path('../packages/MyPipeline-edge_2.zip')

delta_package_path = deployment.create_delta_package(old_package_path, new_package_path)
print(delta_package_path)
```

The delta configuration package can be deployed in the same way as the Edge configuration package. However, the original Edge configuration package must be deployed before the delta configuration package.
