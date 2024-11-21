<!--
SPDX-FileCopyrightText: Copyright (C) Siemens AG 2023
SPDX-License-Identifier: MIT
-->

# Version History

Tutorials for AI Software Development Kit

Known issues:

- Python 3.8.10 is the final regular bugfix release of Python 3.8 with binary installers. We recommend you to use the most recent bugfix release of Python 3.8 for productive use. You can build it from the sources.
- The project templates have only been tested on 64-bit platforms. We do not recommend using them on 32-bit platforms.
- Python Package: Pillow ≤ 9.4.0 - Multiple Vulnerabilities
- As no TensorFlow Lite 2.7.0 installer was published for Windows systems, you cannot use the local pipeline runner on Windows to execute the TensorFlow Lite based pipeline packages, like the one provided in the Image Classification project template.
- Rust Crate: flatbuffers ≤ 2.0.0 - Remote Denial of Service Vulnerability - RUSTSEC-2021-0122

# 2.2.0

New features:

- Python 3.11 support

Fixed issues:

# 2.1.0

New features:

- Azure - Model Manager connection howto notebook
- Howto guides for model config
- Howto guides for batch processing
- Updated Object Detection and Image Classification tutorial to use BayerRG8 format

Fixed issues:

- Python Package: Pillow ≤ 10.2.0 - Remote Denial of Service Vulnerability - 10.3.0
- Python Package: cryptography 38.0.0 < 42.0.4 - Local Denial of Service Vulnerability Vulnerability - GHSA-6vqw-3v5j-54x4
- Python Package: tqdm 4.4.x < 4.66.3 - Local Arbitrary Code Execution Vulnerability - GHSA-g7vv-2v7x-gj9p
- Python Package: Werkzeug < 3.0.3 - Remote Code Execution Vulnerability - GHSA-2g68-c3qc-8985

# 2.0.1

Fixed issues:

- Python 3.10 support

# 2.0.0

New features:

- Support Triton inferencing
- Image Classification tutorial uses ImageSet data type
- New Tutorial Structure: Project templates are merged into single package
- Object Detection tutorial
- Keras to ONNX conversion howto
- Pytorch to ONNX conversion howto

Fixed issues:

- Rust Crate: flatbuffers ≤ 2.0.0 - Remote Denial of Service Vulnerability - RUSTSEC-2021-0122
- Python Package: cryptography 0.5 < 41.0.0 - openssl Remote Denial of Service Vulnerability - GHSA-5cpq-8wj7-hf2v
- Python Package: scipy ≤ 1.10rc2 - Multiple Vulnerabilities - 1.10

# 1.7.0

New features:

- Mathilda packages pipeline with image input and output
- Documentation revamp

# 1.6.0

New features:

- Recommended folder structure for organizing data, code, notebooks and other artifacts.
- Specification of required Python packages.
- Notebook for training a state identifier model.
- Notebook explaining the Inference wrapper code for running the trained model on AI Inference Server.
- Notebook for packaging the trained model and the inference wrapper.
- Notebook for driving the pipeline with test data locally or remotely.

Fixed issues:

- Endpoint and username for creating MQTT config file is not valid for the Chinese version of Azure
- Incorrect instructions in notebook 60-ConnectModelManager

## 1.5.2

Fixed issues:

- Typo in README.md at installing project requirements
- Version limitation for statsmodels
- Notebooks 40a-TestPipelineLocally, 40b-TestZmqPipelineLocally and 50-TestOnIED referenced a non existing labels.txt
- Notebook 40a-TestPipelineLocally displayed predictions incorrectly
- The file packaging.conda.yml referenced AI SDK version in an incompatible way

## 1.5.1

New features:

- Define custom metrics for a pipeline.
- Added description for the pipeline and its elements.
- Example provided for binary output from a pipeline.
- Merged Welcome.ipynb and README.md.
- README is provided in both HTML and md format for convenience.
- Improved installation guide for Windows environment.
- Merged and simplified multiple notebooks dealing with training the example model.

Fixed issues:

- Python 3.8.x ≤ 3.8.15 - Remote Denial of Service Vulnerability - CVE-2022-45061
- Python Package: certifi 2017.11.05 ≤ 2022.9.24 - Remote Improper Input Validation Vulnerability - GHSA-43fp-rhv2-5gv8
- Python Package: Pillow ≤ 9.3.0 - Multiple Vulnerabilities
- Python Package: wheel ≤ 0.37.1 - Remote Regular Expression Denial of Service Vulnerability

## 1.4.1

New features:

- Notebook for explaining and testing inference wrapper
- Four notebooks that demonstrate how the cloud delivery mechanism of AI Model Manager can be connected to a training and packaging MLOps pipeline in Azure ML Studio

Fixed issues:

- Python 3.8.x ≤ 3.8.13 - Multiple Vulnerabilities - 3.8.14
- Python 3.8.x ≤ 3.8.14 - Multiple Vulnerabilities - 3.8.15
- Python 3.8.x ≤ 3.8.15 - Remote Denial of Service Vulnerability - CVE-2022-45061
- Python Package: Pillow 2.0.0 ≤ 9.2.0 - Multiple Local Denial of Service Vulnerabilities - 9.3.0
- Python Package: Pillow ≤ 9.3.0 - Multiple Vulnerabilities - 9.4.0
- Python Package: protobuf ≤ 3.21.6 - Remote Denial of Service Vulnerability - 3.21.7 - the suggested security upgrade cannot be done, as even TensorFlow 2.11.0 requires protobuf < 3.20.
- Python Package: oauthlib 3.1.1 < 3.2.1 - Remote Denial of Service Vulnerability - GHSA-3pgj-pg6c-r5p7
- Python Package: tensorflow 2.7.x < 2.7.4 - Multiple Vulnerabilities - TFSA-2022-085, TFSA-2022-086, TFSA-2022-087 and more
- Python Package: wheel ≤ 0.37.1 - Remote Regular Expression Denial of Service Vulnerability - 0.38.0
- Python Package: certifi 2017.11.05 ≤ 2022.9.24 - Remote Improper Input Validation Vulnerability - GHSA-43fp-rhv2-5gv

## 1.4.0

New features:

- Notebook for explaining and testing inference wrapper

Fixed issues:

- Python 3.8.x ≤ 3.8.13 - Multiple Vulnerabilities - 3.8.14
- Python 3.8.x ≤ 3.8.14 - Multiple Vulnerabilities - 3.8.15
- Python 3.8.x ≤ 3.8.15 - Remote Denial of Service Vulnerability - CVE-2022-45061
- Python Package: Pillow 2.0.0 ≤ 9.2.0 - Multiple Local Denial of Service Vulnerabilities - 9.3.0
- Python Package: Pillow ≤ 9.3.0 - Multiple Vulnerabilities - 9.4.0
- Protocol Buffers for C++ < 3.18.3, 3.19.x < 3.19.5, 3.20.x < 3.20.2, 3.21.x < 3.21.6 - Remote Denial of Service Vulnerability - GHSA-8gq9-2x98-w8hf
- Python Package: certifi 2017.11.05 ≤ 2022.9.24 - Remote Improper Input Validation Vulnerability - GHSA-43fp-rhv2-5gv8

## 1.2.0

New features:

- Inference wrapper code for consuming Industrial Edge Vision Connector output via ZMQ.
- Notebook for creating and testing pipeline package for image ingest via ZMQ.
- Notebook for creating delta pipeline package.
- Adjust window step size using a pipeline parameter.

Fixed issues, fixed bugs and improvements:

- Replaced deprecated `run(data: str)` with `process_input(data: dict)` in entrypoints.
- Separated image payload decoding and prediction code in inference wrapper scripts.
- Improved naming and wording across notebooks.
- Security upgrade open source component Pillow to version 9.2.0.

## 1.1.0

New features:

- Conversion to Edge configuration package included in package creation.
- Notebook to test drive pipeline package on Edge device via External Databus.

Fixed issues:

- Upgraded required TensorFlow version to 2.7.2 as it fixes a critical security issue (CVE-2022-29216).

## 1.0.1

Updated README_OSS.html and constraints.txt.

## 1.0.0

Initial released version.

Main features include:

- Recommended folder structure for organizing data, code, notebooks and other artifacts.
- Specification of required Python packages.
- Notebook for downloading example training data set.
- Notebook for training of an image classification model.
- Notebook for unsupervised training of a state identifier model.
- Training notebook variants for supervised training and parameter search.
- Inference wrapper code for running trained model on AI Inference Server.
- Inference wrapper and packaging variant employing TensorFlow instead of TensorFlow Lite for inference.
- Notebook for packaging trained model and inference wrapper into a pipeline configuration.
- Notebook for driving the pipeline configuration package with test data.
- Notebook for driving the pipeline loaded into AI Inference Server via MQTT.
