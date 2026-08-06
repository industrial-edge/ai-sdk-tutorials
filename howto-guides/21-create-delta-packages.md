<!--
SPDX-FileCopyrightText: 2025 Siemens AG

SPDX-License-Identifier: MIT
-->

# How to create delta packages

Data scientists often realize that edge configuration packages can be large, and consequently, deployment time scales accordingly.

Currently AI SDK provides two different methods for generating delta packages:

1. Automatic delta package creation

    Let's assume you would like to hand over a package to production where you plan to reuse the previous Python environment, but keep everything else in the package in a traceable way.
    You can rely on AI SDK's internal logic whether a full package (referred to as 'base' afterwards) or a delta package is created [automatically](#generate-delta-automatically) in a given scenario. Naturally, you have the possibility to [override](#override-automatic-delta-generation) this logic as well at pipeline export.  
    A base package is a self-contained, deployable inference pipeline that comprises not only the python scripts, configuration files, ML model, but also the wheel files that are required for a successful execution. When you install a new edge device or share a package with someone, always create a self-contained base package, as deltas are rather for small upgrades.

2. Fine-grained delta package creation

    Let's say you would like to verify that package works on AI Inference Server in a rapid fashion and even introduce a chain of dependency regarding delta packages, while keep the size of the new versions low.
    [Fine-grained delta packaging](#fine-grained-delta-packaging) allows you to manually generate a delta package comparing two different versions of edge configuration packages that results in a package that contains solely the changed files (no other source).

!!! info "NOTICE"
    The delta configuration package can be deployed in the same way as the Edge configuration package. The original ('base') Edge configuration package must be deployed before the delta configuration package.

## Generate delta automatically

AI SDK recommends and will automatically generate a delta package if there is already an existing base package that:

- requires the same python version and dependency list as the package to be exported
- is larger in size than a pre-configured threshold (configurable; 300MB by default)

If you wish to change the size threshold for automatic delta package generation, update the `delta_threshold_mb` parameter of the `pipeline.export()` function.

The delta package will contain all file resources, but no python dependencies. If more than one new version is created of the pipeline and all are valid candidates for a delta package, these subsequently generated pipeline packages will be delta packages if possible, and they will always be compared to the latest base package in the export directory.

The generated delta pipeline's version will be automatically incremented, while its name and package ID remains the same.

!!! info "NOTICE"
    The default value of `package_type` is `auto`, which means that SDK will create a delta when possible.

### Override automatic delta generation

Even if the above defined requirements hold for the base package (used as a foundation for generating a delta), you can force the generation of a base package instead of a delta. Set the `package_type` parameter of the `pipeline.export()` function to `base` in order to enforce a base package.

Similarly, delta package generation can be requested by setting the same parameter to `delta`, however only if:

- there is an already existing package that AI SDK can use as base package at delta generation
- the newly exported pipeline does not require a different python version or dependency list than the base package

In case the above requirements are not fulfilled, AI SDK returns with an error, and no package will be generated.

## Fine-grained delta packaging

In case you have two Edge configuration base packages, AI SDK also lets you create a so called 'fine-grained' delta configuration package using function `create_delta_package` in module `simaticai.deployment` or the corresponding CLI command. The difference between a 'fine-grained' delta and the delta package mentioned above is that a 'fine-grained' delta includes only the changed files in the zip file, while the other incorporates all the components, models, scripts and configurations that are needed, except the Python dependencies. For more details, please visit our publicly available [SDK API documentation](https://developer.siemens.com/industrial-ai-suite/sdk/overview.html).

```python
old_package_path = Path('../packages/MyPipeline-edge_1.zip')
new_package_path = Path('../packages/MyPipeline-edge_2.zip')

delta_package_path = deployment.create_delta_package(old_package_path, new_package_path)
print(delta_package_path)
```
