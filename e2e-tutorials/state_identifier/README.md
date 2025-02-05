<!--
SPDX-FileCopyrightText: Copyright (C) Siemens AG 2021. All Rights Reserved.

SPDX-License-Identifier: MIT
-->

# AI SDK State Identifier project template

This is a machine learning project showing how to package a clustering model into a state identifier pipeline running on AI Inference Server.
The project example is designed to be extracted into a folder and the example notebooks executed in an interactive Python notebook editor such as Jupyter lab or Visual Studio Code.

The example demonstrates the three stages of deploying a model to AI Inference Server, such as

- Creating a model embedded in inference wrapper
- Packaging the model into an Edge Configuration Package
- Testing the Edge Configuration Package in local Python environment

The use case itself deals with identifying the operation state of an equipment based on its electrical consumption. The consumption is measured on three phases. These input signals are preprocessed by extracting basic statistical features from time windows. The features are then consumed by a clustering or classification model.

_Hint: This readme is available both as HTML and Markdown. The HTML version you can use with any browser, even if you have no software with Markdown rendering capabilities installed. We recommend using the Markdown version if you have a notebook editor, as most of these let you navigate the links to the notebooks of the template directly._

# Setup environment for running the notebooks

We assume that Jupyter Notebooks or Jupyter Lab is already installed on your machine.
It is recommended that notebooks are run using the `state_identifier` ipython kernel from the `state_identifier` Python environment.
The following commands show how to set up such an environment on Linux.
If you are using Windows, please find the minor differences in the comments.

You can choose your preferred Python environment manager to create the separated Python environment.

We show example for `venv`.

```bash
# via venv assuming Python 3.11.10 is installed on path {PYTHON_HOME_3.11.10}
{PYTHON_HOME_3.11.10}/bin/python -m venv {ENV_DIR}/state_identifier
{ENV_DIR}/state_identifier/bin/activate  # on Windows, 'activate.bat' can be found in folder 'Scripts' instead of 'bin'
```

Once the environment is created and activated you need to install required packages including AI SDK and ipykernel.
These packages must be installed at the same time for pip's dependency resolution to work correctly.

> _Note:_ `$DOWNLOAD_PATH` is the _directory path containing simaticai sdk wheel_, which can be set in environment variables or replaced in the command below.

Finally, register an ipykernel for running the notebooks.

```bash
pip install ipykernel ipython==8.12.0 -r requirements.txt -f $DOWNLOAD_PATH

python -m ipykernel install --user --name state_identifier --display-name "Python (state_identifier)"
```

# Execute the notebooks to package your model

Now the notebooks can be explored and executed in your notebook editor.
Please make sure that you select the `state_identifier` kernel to execute the AI SDK State Identifier notebooks.

### 1. Build and train a clustering model

The notebook [10-CreateClusteringModel.ipynb](notebooks/10-CreateClusteringModel.ipynb) shows you how to train a simple unsupervised model on an example dataset in case you don't already have a model.

### 2. Create an Inference Wrapper

The notebook [20-CreateInferenceWrapper.ipynb](notebooks/20-CreateInferenceWrapper.ipynb) creates an inference wrapper that serves as an entrypoint to your model.

### 3. Package for deployment

Before you can bring the model to the shopfloor, an edge package must be created with all of the content necessary for executing the model on an Industrial Edge device. This job is done by notebook [30-CreatePipelinePackage.ipynb](notebooks/30-CreatePipelinePackage.ipynb).
The notebook [35-CreateDeltaPackage.ipynb](notebooks/35-CreateDeltaPackage.ipynb) helps you to create a smaller Edge Configuration package for a Pipeline update. This is practical if the edge configuration package is large and you want to save time during deploying a small update.

### 4. Test your packaged pipeline locally in Python

Test the created edge config package in a local simulated runtime environment to eliminate as many problems as possible without leaving your Python development environment. This is shown in [40-TestPipelineLocally.ipynb](notebooks/40-TestPipelineLocally.ipynb).

# Directory structure

The directory structure is based on [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/).

```text
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default Sphinx project; see sphinx-doc.org for details.
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. The naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description.
├── packages           <- This is where the edge config package is created.
│
├── reports            <- Analysis generated as HTML, PDF, LaTeX, etc.
│   └── figures        <- Graphics and figures generated for use in `reports`.
│
├── src                <- Source code for use in this project.
│
├── test               <- This is where the local pipeline runner creates the local test environment.
│
├── CHANGELOG.md       <- The top-level CHANGELOG for developers using this project.
├── requirements.txt   <- The list of required Python packages to execute the notebooks.
└── entrypoint.py      <- An entrypoint file to be used in example notebook 30-CreatePipelinePackage.ipynb.
```
