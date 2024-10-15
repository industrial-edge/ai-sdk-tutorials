# AI SDK, Tutorials and guides

## Introduction to AI SDK

The AI Software Development Kit, or AI SDK for short, is a set of Python libraries. These libraries provide building blocks for automating the creation, packaging, and testing of inference pipelines for the AI Inference Server.

You can consider AI SDK to be the entry point into Siemens' Industrial AI portfolio.
AI SDK helps you in a number of steps in a machine learning workflow, like packaging the models and its depenedencies, verifying and testing the package locally, and creating the inference pipeline package to run your model on AI Inference Server.

## Tutorials and guides

This collection of guidelines, howto examples, and use case specific solutions contain all the necessary information and dependencies for a quick and smooth start of using AI SDK.

We recommend studying the [End-to-end tutorials](./e2e-tutorials/README.md) first.\
The tutorials will guide you through a notebook-based ML workflow starting with training an example model and show you the recommended way to use the AI SDK for packaging a trained model for deployment and to test such packages.\
The End-to-End tutorials cover the following machine learning workflow steps:

- Training data preparation
- Training models
- Packaging models as an inference pipeline
- Testing of packaged inference pipelines
- Generating the inference pipeline for AI@Edge

You can also use these tutorials as a starting point for packaging and testing your own models.

> **Hint**\
> If you want to run these end-to-end tutorials, you need to setup your environment with appropriate dependencies. Each tutorial explains how to setup the environment in their README.md file

Our [Howto guides](./howto-guides/README.md) provide tips and tricks on specific aspect of packaging your ML model for running on AI Inference Server.

And lastly, the [Howto notebooks](./howto-notebooks/README.MD) serves you runnable examples for various steps in the ML workflow that you help you master pipeline creation.


## Contribution

Thank you for your interest in contributing. Anybody is free to report bugs, unclear documentation, and other problems regarding this repository in the Issues section.
Additionally everybody is free to propose any changes to this repository using Pull Requests.

If you haven't previously signed the [Siemens Contributor License Agreement](https://cla-assistant.io/industrial-edge/) (CLA), the system will automatically prompt you to do so when you submit your Pull Request. This can be conveniently done through the CLA Assistant's online platform. Once the CLA is signed, your Pull Request will automatically be cleared and made ready for merging if all other test stages succeed.

## License and Legal Information

Please read the [Legal information](LICENSE.md).
