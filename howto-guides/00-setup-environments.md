<!--
SPDX-FileCopyrightText: Copyright (C) 2020 - 2024 Siemens AG

SPDX-License-Identifier: MIT
-->

# How to setup environment manager environments

You can use your preferred Python environment manager to create the Python environment. We show here the commands for `Conda` and Python `venv`, taking project template Image Classification as an example. For other project templates, you have to substitute the name `image_classification` as described in the template's README.

> **Note**\
> It is strongly recommended to create independent environments for project templates, and also for Jupyter Lab.

## Create Conda environment including Python and activate it

```dosbatch
conda create -n image_classification python=3.11.9
conda activate image_classification
```

## Create a Python virtual environment and activate it

This method requires a preinstalled Python 3.11 runtime.

```dosbatch
python -m venv %USERPROFILE%\venv\image_classification
%USERPROFILE%\venv\image_classification\Scripts\activate.bat
```

## Separate Jupyter Lab environment

We recommend creating an environment for installing and running Jupyter Lab, to avoid dependency version collisions with AI SDK.

```dosbatch
conda create -n jupyter_env python=3.11.9
conda activate jupyter_env
pip install jupyterlab
```

## Environment for a project template

Download the AI SDK distribution package and the Image Classification project template. Choose your Downloads folder in your Windows home directory. Unpack the zip files into `ai_sdk_core` and `image_classification` folders in your home folder of the virtual Linux machine with the following commands.

```bash
unzip "~/Downloads/ai_sdk_core-1.6.0.zip" -d ~/ai_sdk_core
unzip "~/Downloads/ai_sdk_image_classification-1.7.0.zip" -d ~/image_classification
```

Next, step into the `image_classification` folder and install the ipykernel package along with the project template's dependencies and with AI SDK.

These packages must be installed at the same time for pip's dependency resolution to work correctly.

```bash
cd ~/image_classification
pip install ipykernel -r requirements.txt -f ~/ai_sdk_core
```

Please note that by default, `pip` will install the newest available version of required packages that are compatible with the SDK and the project template. If you want to make sure to use the versions that are listed in Readme_OSS, you can apply the appropriate constraint during installation as follows:

```bash
cd ~/image_classification
pip install ipykernel -r requirements.txt -c constraints.txt -f ~/ai_sdk_core
```

Once the environment is created and activated, you need to register it as an interactive Python kernel so that it becomes available in your notebook editor. This is can be achieved with the following command:

```bash
python -m ipykernel install --user --name image_classification --display-name "Python (image_classification)"
```
