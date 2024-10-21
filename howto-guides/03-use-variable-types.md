<!--
SPDX-FileCopyrightText: Copyright (C) 2020 - 2024 Siemens AG

SPDX-License-Identifier: MIT
-->

# How to use variable types

Let's take another look and check how you defined the input variable `input_1`

```python
# defining input variable
component.add_input(name= 'input_1', _type='Double')
```

You defined it as `Double`, which is a data type of AI Inference Server.

The `process_input()` function receives the inputs converted to a Python data type, which is a float for the AI Inference Server type Double.

AI SDK allows custom datatypes for input/output variables, but it will raise a warning message. Also, it is then the user's responsibility to handle these variables correctly. Defining a custom datatype, e.g. NumpyArray can be useful between a GPU component and a Python component.

In general, you need to define the types of input and output variables as AI Inference Server types, but the Python script should use the appropriate Python type.\
The match between AI Inference Server data types and Python data types is shown in the following table.\
The table also shows AI Inference Server 1.6 connection support for each data type.

A complete list of supported datatypes can be found in [AI Inference Server documentation](https://support.industry.siemens.com/cs/mdm/109825687?c=173477346315&lc=en-US) in the `Introduction` > `Software and hardware restrictions` section.\
This documentation is also available from the home screen of AI Inference Server by clicking the `(?)` icon

| AI Inference Server | Python   | Databus | S7 Connector | Vision Connector |  ZMQ   |
| ------------------- | -------- | :-----: | :----------: | :--------------: | :----: |
| Bool                | bool     |         |     I/O      |                  |        |
| Integer             | int      |         |     I/O      |                  |        |
| Double              | float    |         |     I/O      |                  |        |
| String              | str      |   I/O   |     I/O      |      input       |        |
| Object              | dict     |         |              |      input       | output |
| Binary              | bytes    |         |              |                  |  I/O   |
| ImageSet            | dict     |         |              |      I/O         |        |
| StringArray         | [string] |   I/O   |              |                  |        |

External Databus connections support the same data types as Databus.

## Custom data formats

To connect your pipeline to a custom application with its own data format, you can take one of the following methods:

- Use `String` and connect input or output through Databus or External Databus. In this case, you can use any text data format, such as JSON, XML, CSV, or any combination of these.
- Use `Object` and connect output via ZMQ. In this case, the AI Inference Server converts the metadata dictionary into a JSON string and passes it to the receiver together with the binary contents in a multi-part ZMQ message. For more details, refer to the AI Inference Server Function Manual (<https://support.industry.siemens.com/cs/ww/en/view/109822331>).

### Specific variable types for images

#### String

AI Inference Server supports receiving URL-encoded images via MQTT as `String`. The payload type is str and can be extracted into a PIL image as follows:

```python
# define input

component.add_input("image", "String")

# extract payload

def process_input(payload: dict):
    url_encoded_image = payload["image"]
    with urlopen(url_encoded_image) as response:
        assert response.headers["Content-type"] in ["image/png", "image/jpeg"]
    image_bytes = response.read()
    pil_image = Image.open(io.BytesIO(image_bytes)).resize(IMAGE_SIZE)
```

#### Object

Another supported type for images is `Object` which can be used to receive or send images via ZMQ.

If the input variable is defined with type Object, the AI Inference Server takes the image from ZMQ and creates a specific payload format. In your code, this format can be processed and extracted into a PIL Image. A specific code example can be found in the [Image Classification pipeline](01-define-components.md#image-classification-pipeline) section of the [define components](01-define-components.md) howto guide.

```python
# define input

component.add_input("image", "Object")

# Object input format

payload = { "image":
            {
            "resolutionWidth": image.width,
            "resolutionHeight": image.height,
            "mimeType": ["image/raw"],
            "dataType": "uint8",
            "channelsPerPixel": 3,
            "image": _swap_bytes(image.tobytes())
            }
          }
```

When the output variable is defined with type Object, the output must be provided in a specific format. In your code, a dictionary must be created with a string and a bytes field.
They must contain the width and height information in a JSON string and the UINT8 bytes of the raw image.

```python
# define output

component.add_input("image_with_filter", "Object")

# Object output format

return {
    "image_with_filter": {
        "metadata": json.dumps( {
            "resolutionWidth": image.width,
            "resolutionHeight": image.height
        }),
        "bytes": image.tobytes()
    }
}
```
See details in [How to use `Object` format for images.md](13-use-object-format-for-images.md)

#### Binary

The most commonly supported data format is "Binary" that is used to receive or send a byte array over ZMQ.

If an `input_variable` is defined as "Binary", the AI Inference Server provides it as a Python dictionary, where the variable name is the key, and the value is the binary data provided as the Python type "bytes".

A specific code example can be found in the [Image Classification pipeline](01-define-components.md#image-classification-pipeline) section of the [define components](01-define-components.md) howto guide..

```python
# definition of input

component.add_input("image", "Binary")

# Binary input format

with open('image.png', 'rb') as f:
    binary = f.read()
    payload = { "image": binary }
...

# Decode a PIL image from Binary data

image = Image.open(io.BytesIO(binary))
...
```

If an `output_variable` is defined with type "Binary" the output must be provided as a "bytes" value in the returned dictionary.

```python

# output definition

component.add_input("processed_image", "Binary")

# Binary output format from a PIL image

membuf = io.BytesIO()
image.save(membuf, format="png")
return {
    "processed_image": membuf.getvalue()
}
```

See details in [How to use `Binary` format for images.md](13-use-object-format-for-images.md)

#### ImageSet

ImageSet data type allows receiving multiple images, along with their format, dimension information, and metadata. This is the image format supported by [Vision Connector](https://support.industry.siemens.com/cs/document/109822712/vision-connector?dti=0&lc=en-WW) application.
Example of processing an incoming ImageSet in Python:

```python
# Define input

component.add_input("image_set", "ImageSet")

# Handle incoming image(s)

def process_input(data: dict):
    image_set = data['image_set']
    for image_data in image_set['image_list']:
        process_image_data(image_data['image'])
        # ...
```

Example of producing an ImageSet output in `python`:

```python
# Define output

component.add_output("image_set", "ImageSet")

# Assemble an ImageSet object

import json

def process_input(data):
    # ...

    image_set: {
        "version": "1",
        "camera_id": "...",
        "timestamp": "2023-08-08T09:11:12.000Z",
        "metadata": json.dumps({
            "key1": "value1",
            "key2": "value2",
            # ...
        }),
        "image_list": [{
            "id": "...",
            "width": 640,
            "height": 480,
            "format": "<GeniCam image format>",
            "timestamp": "2023-08-08T09:11:12.000Z",
            "metadata": json.dumps({
                "key1": "value1",
                "key2": "value2",
                # ...
            }),
            "image": b"..."
        }, {
            # ...
        }]
    }

    return {
        "image_set": image_set
    }
```

See details in [How to use `ImageSet` format for images.md](14-use-imageset-format-for-images.md)