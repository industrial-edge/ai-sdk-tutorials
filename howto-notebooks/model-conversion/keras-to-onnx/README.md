<!--
SPDX-FileCopyrightText: Copyright (C) Siemens AG 2021. All Rights Reserved.

SPDX-License-Identifier: MIT
-->

# Model Conversions

## Keras to ONNX model conversion

This tutorial explains how to convert a Keras Model stored in tensorflow's 'h5' format to a standardized ONNX format through the following steps:

* load a model stored in 'h5' format
* convert and save the loaded model into 'ONNX' format
* verify the input and output shape of the model

The tutorial will also give you ways to execute your model on your local machine.

## Using Virtual Python Environment
 
If you are using a virtual python environment manager, you can easily install all the necessary dependencies from requirements.txt
 
```bash
python -m pip install -r requirements.txt
```
