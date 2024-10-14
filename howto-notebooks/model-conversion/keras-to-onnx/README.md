<!-- Copyright (C) Siemens AG 2021. All Rights Reserved. -->

# Model Conversions

## Keras to ONNX model conversion

This tutorial explains how to convert a Keras Model stored in tensorflow's 'h5' format to a standardized ONNX format through the following steps:

* load a model stored in 'h5' format
* convert and save the loaded model into 'ONNX' format
* verify the input and output shape of the model

The tutorial will also give you ways to execute your model on your local machine.

## Using conda

If you are using conda as your virtual environment manager, you can easily create an environment with all the necessary dependencies installed using the below command in your terminal

```bash
conda env create -f keras-to-onnx.conda.yml
```
