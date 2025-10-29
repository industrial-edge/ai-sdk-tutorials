<!--
    SPDX-FileCopyrightText: 2021 Siemens AG. All Rights Reserved.
    SPDX-License-Identifier: MIT
-->

# AI SDK Segmentation Tutorial

This is an AI SDK tutorial intended to create a segmentation pipeline running on AI Inference Server using the Ultralytics python package with a pretrained YOLO segmentation model.
The project example is designed to explain the workflow of creating a Pipeline Package through the guidance of the interactive IPython Notebooks in the `notebook` folder.

The main goal of this example is introducing a way to use Ultralytics in such a pipeline. At the time of writing of this tutorial, AI Inference Server does not support opencv-python, one of the dependencies of Ultralytics. However, we can still use Ultralytics on an AI Inference Server, if we can swap opencv-python to opencv-python-headless, a version of OpenCV with no GUI implementation.

_Important!_ This feature is only supported on AI SDK 2.6.0 and higher, and AI Inference Server 2.6.0 or higher.

The example demonstrates the stages of deploying a YOLO segmentation model to an AI Inference Server, such as

- Explaining the usage of the Ultralytics YOLO segmentation model
- Creating an inference wrapper (a Python step, and eventually, the pipeline) that uses the model
- Demonstrating how to prepare the package dependencies, replacing opencv-python with its headless version
- Packaging the model into a Pipeline Package
- Testing the package in local Python environment

_Hint: This readme is available both as HTML and Markdown. The HTML version you can use with any browser, even if you have no software with Markdown rendering capabilities installed. We recommend using the Markdown version if you have a notebook editor, as most of these let you navigate the links to the notebooks of the template directly._

# Setup environment for running the notebooks

We assume that Jupyter Lab or another notebook editor is already installed on your machine.

We recommend that you run the notebooks using the `segmentation` ipython kernel from the `segmentation` Python environment.

The following commands show how to set up such an environment on Linux.
If you are using Windows, please find the minor differences in the comments.

You can choose your preferred Python environment manager to create the separated Python environment.
We show example for `venv`.

```bash
# via venv assuming Python 3.12 is installed on path {PYTHON_HOME_3.12}
{PYTHON_HOME_3.12}/bin/python -m venv {ENV_DIR}/object_detection
{ENV_DIR}/object_detection/bin/activate  # on Windows, 'activate.bat' can be found in folder 'Scripts' instead of 'bin'

```

Once the environment is created and activated you need to install required packages including AI SDK and ipykernel.
These packages must be installed at the same time for pip's dependency resolution to work correctly.

Finally, register an ipykernel for running the notebooks.

```bash
pip install ipykernel -r requirements.txt

python -m ipykernel install --user --name segmentation --display-name "(Python) Segmentation"
```

# Execute the notebooks to package your model

Now the notebooks can be explored and executed in your notebook editor.
Please make sure that you select the `segmentation` kernel to execute the AI SDK Segmentation notebooks.

### 1. Introducing the Ultralytics YOLO segmentation model.

The notebook [10-UltralyticsYoloModel](./notebooks/10-UltralyticsYoloModel.ipynb) explains how you can download and use a pretrained segmentation model using Ultralytics, how to load and run an image on the model, and how to extract and interpret the results.

### 2. Create an Inference Wrapper

The notebook [20-CreateInferenceWrapper.ipynb](./notebooks/20-CreateInferenceWrapper.ipynb) shows you how to create an inference wrapper that serves as an entrypoint to the model. It also shows how you can swap the opencv-python package to opencv-python-headless, so that an AI Inference Server can use the Ultralytics package with no issue.

### 3. Package for deployment

Before you can bring the model to the shopfloor, a Pipeline Package must be created with all of the content necessary for executing the model on an AI Inference Server.
This package can be created with the notebook [30-CreatePipeline.ipynb](./notebooks/30-CreatePipeline.ipynb).

### 4. Test your packaged pipeline locally in Python

Test the created Pipeline Package in a local simulated runtime environment to eliminate as many problems as possible without leaving your Python development environment. This is shown in [40-TestPipelineLocally.ipynb](./notebooks/40-TestPipelineLocally.ipynb).

# Directory structure

The directory structure is based on [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/).

```text
├── README.md             <- The top-level README for developers using this project.
├── images
│   └── bus.jpg           <- An example image for segmentation.
│
├── models                <- The folder for the YOLO segmentation model downloaded by executing the notebooks.
│
├── notebooks             <- Jupyter notebooks. The naming convention is a number (for ordering),
│                            and a short `-` delimited description.
│
├── packages              <- This is where the Pipeline Package is created.
│                            The folder also contains the PythonPackages.zip which collects the wheel
│                            files that are officially not available in the proper format to deploy.
│
├── src                   <- Source code for use in this project.
│   │
│   ├── requirements.txt  <- The list of required Python packages for the pipeline.
│   └── segmentation.py   <- The entrypoint for the inference wrapper.
│
├── test                  <- This is where the local pipeline runner creates the local test environment.
│
└── requirements.txt      <- The list of required Python packages to execute the notebooks.
```
