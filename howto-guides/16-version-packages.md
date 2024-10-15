<!--
SPDX-FileCopyrightText: Copyright (C) 2020 - 2024 Siemens AG
SPDX-FileCopyrightText: Copyright (C) 2020-2024 Siemens AG

SPDX-License-Identifier: MIT
-->

# How to version packages and how to use Package ID

Edge packages are identified by their package ID and version attributes, and are grouped by package ID in [AI Inference Server](https://support.industry.siemens.com/cs/document/109825687/industrial-ai-ai-inference-server?dti=0&lc=en-US) and in other Edge applications.

When saving a pipeline – with the `pipeline.export()` method – you can specify a package ID in a UUID 4 compliant format or an automatically generated one is assigned.

If no package ID is defined in the `pipeline.export()` method, and AI SDK finds an already assigned package ID in a previously generated and similarly named package, the package ID found in the latest package is used.

AI SDK automatically assigns and increments the version number of a pipeline each time a package is saved unless a new package ID is assigned in the `pipeline.export()` method, or an explicit version number without a package ID is defined in the `pipeline.export()` method, or in the pipeline constructor.

Restrictions:

- You cannot overwrite a previously saved package with the same package ID if the package ID is explicitly assigned in the `pipeline.export()` method
- Existing packages without a package ID will be overwritten
- If a new package ID is assigned to an existing version of the package, the old one will be overwritten
- If no predecessor of a package is found, AI SDK assigns version 1 to the created package
- The version defined in the `pipeline.export()` method takes precedence over the version assigned at the constructor level

The `pipeline.export()` method automatically generates a Package ID when you first save your package.
It will also automatically assign a version number. The version number will be increased if you save the package again.

If you need to manually provide a Package ID or a version number, you can specify them in the arguments of the save method.

```python
import uuid
edge_package_path = pipeline.export('../packages', version="1")
edge_package_path = pipeline.export('../packages', package_id=uuid.uuid4())
edge_package_path = pipeline.export('../packages', package_id=uuid.uuid4(), version="1")
```

## Using semantic versioning

AI SDK does not use semantic versioning to auto-increment version numbers.
If you plan to use semantic versioning for your packages and want to maintaing package ID across different versions of your package, you need to provide a UUID4 compliant package ID explicitly in the `pipeline.export()` method.

```python
edge_package_path = pipeline.export('../packages', package_id='385e930a-063d-44b4-9aa5-d804fa8304a0', version="1.0.2")
```

This way the package ID provided will be kept consistent across all package versions.
