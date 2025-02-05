<!--
SPDX-FileCopyrightText: Copyright (C) 2020 - 2025 Siemens AG

SPDX-License-Identifier: MIT
-->

# How to return the processing results

If you want to return the results after processing the input data, you must return them in a dictionary. The keys should be the variable names of the component's outputs. In the [handling file resources](05-handle-file-resources.md) howto guide, the `process_data()` function returns a such dictionary.\
It can be directly returned from process_inputs() as well. The dictionary contains an integer for class_label and a floating-point value that represents the confidence of the prediction.

If there is no output for a particular call to process_input(), you should return None. As a result, the AI Inference Server does not trigger the next component in the pipeline, or if it is the last component of the pipeline, the pipeline does not emit any output from that component.

## Returning Object

AI Inference Server version 1.6 restricts what kind of dictionary a pipeline component can return in an output variable of type `Object`. The dictionary must hold a metadata string and a binary sequence. The metadata and the binary sequence can have an arbitrary key in the `dict`, but must be of type `str` and `bytes` respectively. In other words, any dictionary with two elements will do if one of the elements is of type `str` and the other is `bytes`.

For example, if you want to pass a processed version of the input image to a later component or ZMQ, you can do it as follows:

```python
# define output
component.add_output("processed_image", "Object")

# Object output format
return {
    "processed_image": {
        "metadata": json.dumps({
                "mode": image.mode,
                "width": image.width,
                "height": image.height
            }),
        "bytes": image.tobytes()
    }
}
```

> *Note*\
You cannot pass a dictionary received as pipeline input as component output because the structures of these dictionaries are different.

In the receiver pipeline component, you can decode the image as follows:

```python
# define input
component.add_input("processed_image", "Object")

# construct PIL Object from metadata and binary data
def process_input(data: dict):
    metadata = json.loads(data['processed_image']['metadata'])
    image_data = data['processed_image']['bytes']
    mode = metadata['mode']
    width = metadata['width']
    height = metadata['height']
    image = Image.frombytes(mode, (width, height), image_data)
```

## Returning Binary data

AI Inference Server version 1.5.0 allows data to be returned in "Byte" format as an output variable, which is defined as "Binary" in the pipeline configuration.
To pass binary data, such as an image, between components or as pipeline output, you can do the following:

```python
# definition of outputs
component.add_output("prediction", "String")
component.add_output("processed_image", "Binary")

# Binary output format from a PIL image
membuf = io.BytesIO()
image.save(membuf, format="png")
return {
    "prediction": str(prediction),
    "processed_image": membuf.getvalue()
}
```

In the receiver pipeline component, you can decode the image as follows:

```python
# definition of input
component.add_input("processed_image", "Binary")

# construct PIL object from metadata and binary data
def process_input(data: dict):
    image_data = data['processed_image']
    image = Image.open(io.BytesIO(image_data))
```
