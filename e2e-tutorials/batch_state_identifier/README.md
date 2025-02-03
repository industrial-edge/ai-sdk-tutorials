<!--
SPDX-FileCopyrightText: Copyright (C) Siemens AG 2021. All Rights Reserved.

SPDX-License-Identifier: MIT
-->

# AI SDK Batch State Identifier example

This is a machine learning project intended to create a state identifier pipeline running on AI@Edge.
The project example is designed to be extracted into a folder, renamed to your needs and the example notebooks executed in Jupyter Lab.
The example demonstrates how to train, package and test a time series ML pipeline.

**This is a proof of concept variant of State Identifier that works on batches of data instead of continuous signals.** It was derived from
State Identifier with the intent of having something simpler, with less entry barrier to get it running:

- No need for S7 Connector and wrapping in S7 Data Format.
- No need for inter-signal alignment.
- No need for accumulating windows in the inference wrapper.
- No need for bridging the MQTT Connector to the IE Databus to drive the pipeline from a notebook on a PC.

In this case the data is collected, aggregated and compiled into a json by another service.
Simply said, we assume that data arrives already in batch, one window per databus input.

**Please note that the code and the explanations are not fully adapted and cleaned up.** But there is:

- Training data.
- A training notebook.
- A packaging notebook.
- A notebook to test the package locally.

There is no notebook to test the package on an Edge device but notebook #50 from Image Classification should work with minimum adaptation
(feed the JSONs instead of the images, adapt input and output variable and topic names, adapt package name).

# Directory structure

The directory structure is based on [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/).

```commandLine
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

# Environment for running the notebooks

We assume that Jupyter Notebooks or Jupyter Lab is already installed on your machine.
It is recommended that notebooks are run using the `state_identifier` ipython kernel from the `state_identifier` Python environment.
The following commands show how to set up such an environment.

```commandline
# You can choose your preferred Python environment manager to create the separated Python environment.
# We show example for `venv`.

# via venv assuming Python 3.11.10 is installed on path {PYTHON_HOME_3.11.10}
{PYTHON_HOME_3.11.10}/bin/python -m venv {ENV_DIR}/state_identifier
{ENV_DIR}/state_identifier/bin/activate  # on Windows, 'activate.bat' can be found in folder 'Scripts' instead of 'bin'

# Once the environment is created and activated you need to register as an ipykernel.
pip install ipykernel
python -m ipykernel install --user --name state_identifier --display-name "Python (state_identifier)"

# Install required packages including AI SDK.
pip install -r requirements.txt -f <directory path containing simaticai sdk wheel>
```

Once the required packages are installed the notebooks can be explored and executed in Jupyter Lab.
Please make sure that you select the `state_identifier` kernel to execute the notebooks.
