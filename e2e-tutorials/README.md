# End-to-end tutorials

These Machine Learning tutorials walks you through the entire ML workflow from creating and training models to packaging them for AI Inference Server and testing them in your local environment.

The project example is designed to be extracted into a folder and the example notebooks executed in an interactive Python notebook editor such as Jupyter lab or Visual Studio Code.

## AI SDK Image Classification

This is a machine learning tutorial intended to create an image classification pipeline running on AI Inference Server.
This tutorial uses a pre-trained `MobilNet` classifier network which we will extend with layers and train to be able to classify example images of the following SIMATIC automation products:

- ET 200AL
- ET 200eco PN
- ET 200SP
- S7-1200
- S7-1500

## AI SDK State Identifier

This is a machine learning tutorial showing how to package a clustering model into a state identifier pipeline running on AI Inference Server.

The tutorial provides an example of identifying the operation state of an equipment based on its electrical consumption.\
The consumption is measured on three phases.\
These input signals are preprocessed by extracting basic statistical features from time windows. The features are then consumed by a clustering or classification model.

## AI SDK Batch State Identifier

This is a machine learning tutorial intended to create a state identifier pipeline running on AI@Edge.
The example demonstrates how to train, package and test a Machine Learning pipeline using time series data.

This tutorial is a variant of the State Identifier tutorial which works with batches of data instead of continuous signals.\
It was derived from State Identifier with the intent of having something simpler, with less entry barrier to get it running:

- No need for S7 Connector and wrapping in S7 Data Format.
- No need for inter-signal alignment.
- No need for accumulating windows in the inference wrapper.
- No need for bridging the MQTT Connector to the IE Databus to drive the pipeline from a notebook on a PC.

> **Note**\
> In this tutorial, we are assuming that the data is collected, aggregated and compiled into a json by another service.

## AI SDK Object Detection

This machine learning tutorial helps you create an object detection pipeline running on AI Inference Server with GPU extension.
The tutorial is designed to explain the workflow of creating a Pipeline with step `gpuruntime` through the guidance of the interactive IPython Notebooks in the notebook folder. The example demonstrates the stages of deploying an ONNX model to an AI Inference Server with GPU support, such as

- Creating test set for the workflow
- Studying and fixing the supported ONNX model formats
- Creating Pre- and Postprocessing steps to support the `gpuruntime`
- Packaging the model into an Edge Configuration Package
- Testing the Edge Configuration Package in local Python environment
