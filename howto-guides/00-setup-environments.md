<!--
SPDX-FileCopyrightText: 2025 Siemens AG

SPDX-License-Identifier: MIT
-->

# How to setup environment manager environments

You can use your preferred Python environment manager to create the Python environment. We show here the commands for Python `venv`, taking project template Image Classification as an example. For other project templates, you have to substitute the name `image_classification` as described in the template's README.

> **Note**\
> It is strongly recommended to create independent environments for project templates, and also for Jupyter Lab.

## Create a Python virtual environment and activate it

This method requires a preinstalled Python 3.12 runtime.

```bash
python -m venv ~/.venv/image_classification
. ~/.venv/image_classification/bin/activate
```

## Separate Jupyter Lab environment

We recommend creating an environment for installing and running Jupyter Lab, to avoid dependency version collisions with AI SDK.

```bash
python -m venv ~/.venv/jupyter
. ~/.venv/jupyter/bin/activate
pip install jupyterlab
```

## Environment for a project template

Download the Image Classification project template. Choose your Downloads folder in your Windows home directory. Unpack the zip files into the `image_classification` folder in your home folder of the virtual Linux machine with the following command.

```bash
unzip "~/mnt/c/Users/YOUR USER/Downloads/AI_SDK_Tutorials-2.9.0.zip"
```

Next, step into the `image_classification` folder and install the ipykernel package along with the project template's dependencies and with AI SDK. The requirements.txt contains the `simaticai` dependency, which will be downloaded from PyPi.org.

These packages must be installed at the same time for pip's dependency resolution to work correctly.

```bash
cd e2e-tutorials/image_classification
pip install ipykernel -r requirements.txt
```

Once the environment is created and activated, you need to register it as an interactive Python kernel so that it becomes available in your notebook editor. This is can be achieved with the following command:

```bash
python -m ipykernel install --user --name image_classification --display-name "Python (image_classification)"
```
