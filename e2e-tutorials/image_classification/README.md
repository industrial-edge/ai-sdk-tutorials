<!-- Copyright (C) Siemens AG 2021. All Rights Reserved. -->

# AI SDK Image Classification project template

This is a machine learning project intended to create an image classification pipeline running on AI Inference Server.
The project example is designed to be extracted into a folder and the example notebooks executed in an interactive Python notebook editor such as Jupyter lab or Visual Studio Code.

The example demonstrates the three stages of deploying a model to AI Inference Server, such as

- Creating a model embedded in inference wrapper
- Packaging the model into an Edge Configuration Package
- Testing the Edge Configuration Package in local Python environment

_Hint: This readme is available both as HTML and Markdown. The HTML version you can use with any browser, even if you have no software with Markdown rendering capabilities installed. We recommend using the Markdown version if you have a notebook editor, as most of these let you navigate the links to the notebooks of the template directly._

# Setup environment for running the notebooks

We assume that Jupyter Lab or another notebook editor is already installed on your machine.

We recommend that you run the notebooks using the `image_classification` ipython kernel from the `image_classification` Python environment.

The following commands show how to set up such an environment on Linux.
If you are using Windows, please refer [WINDOWS_SETUP.md](docs/WINDOWS_SETUP.md).

You can choose your preferred Python environment manager to create the separated Python environment.
We show examples for `conda` and `venv`.

```bash
# via conda
conda create -n image_classification python=3.11.9
conda activate image_classification
```

```bash
# via venv assuming Python 3.11.9 is installed on path {PYTHON_HOME_3.11.9}
{PYTHON_HOME_3.11.9}/bin/python -m venv {ENV_DIR}/image_classification
{ENV_DIR}/image_classification/Scripts/activate

```

Once the environment is created and activated you need to install required packages including AI SDK and ipykernel.
These packages must be installed at the same time for pip's dependency resolution to work correctly.
_Note:_ `$DOWNLOAD_PATH` is the _directory path containing simaticai sdk wheel_, which can be set in environment variables or replaced in the command below.

Finally, register an ipykernel for running the notebooks.

```bash
pip install ipykernel ipython==8.12.0 -r requirements.txt -f $DOWNLOAD_PATH

python -m ipykernel install --user --name image_classification --display-name "Python (image_classification)"
```

# Execute the notebooks to package your model

Now the notebooks can be explored and executed in your notebook editor.
Please make sure that you select the `image_classification` kernel to execute the AI SDK Image Classification notebooks.

### 1. Build and train a classification model

The notebook [10-CreateClassificationModel.ipynb](notebooks/10-CreateClassificationModel.ipynb) helps you to create a training set from your image set, build a classification model based on a pre-trained Tensorflow model and train the model with the created training set.

### 2. Create an Inference Wrapper

The notebook [20-CreateInferenceWrapper.ipynb](notebooks/20-CreateInferenceWrapper.ipynb) shows you how to create an inference wrapper that serves as an entrypoint to your model.

### 3. Package for deployment

Before you can bring the model to the shopfloor, an edge package must be created with all of the content necessary for executing the model on an Industrial Edge device.
This package can be created with the notebook [30-CreatePipelinePackage.ipynb](notebooks/30-CreatePipelinePackage.ipynb).

### 4. Test your packaged pipeline locally in Python

Test the created edge config package in a local simulated runtime environment to eliminate as many problems as possible without leaving your Python development environment. This is shown in [40-TestPipelineLocally.ipynb](notebooks/40-TestPipelineLocally.ipynb).

### 5. Test your packaged pipeline on an Industrial Edge device

The how-to guide [22-test-on-edge-device](../../howto-guides/22-test-on-edge-device.md) provides means to exercise your pipeline on an AI Inference Server running on an Industrial Edge device.

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
│                         The folder also contains the PythonPackages.zip which collects the wheel
│                         files that are officially not available in the proper format to deploy
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
├── runtime_requirements.txt   <- The list of required Python packages to include in the deployment package
│                                        when deploying the model with TensorFlow Lite.
└── entrypoint.py      <- An entrypoint file to be used in example notebook 30-CreatePipelinePackage.ipynb.
```
