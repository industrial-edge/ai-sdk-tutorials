<!--
SPDX-FileCopyrightText: 2025 Siemens AG

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

#### ImageSet

ImageSet data type allows receiving multiple images, along with their format, dimension information, and metadata. This is the image format supported by [Vision Connector](https://support.industry.siemens.com/cs/document/109822712/vision-connector?dti=0&lc=en-WW) application.
Example of processing an incoming ImageSet in Python:

```python
# Define input

component.add_input("image_set", "ImageSet")

# Handle incoming image(s)

def process_input(data: dict):
    image_set = data['image_set']
    for image_data in image_set['detail']:
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
        "version": "1",  # version of the Metadata format
        "count": 1,  # Number of images on message
        "timestamp": timestamp.isoformat(),  # Camera acquisition time
        "detail": [{  # list of images with detailed information
            "id": str(image_path),  # unique image identifier. this case we use the filename of the original image
            "timestamp": str(timestamp.timestamp()),  # Timestamp provided by the camera
            "width": width,  # image width
            "height": height,  # image height
            "format": "BayerRG8",  # image format configure
            "metadata": "",  # optional extra information on image
            "image": image_bytes  # image binary with the given 'format'
        }]
    }

    return {
        "image_set": image_set
    }
```

See details in [How to use `ImageSet` format for images.md](14-use-imageset-format-for-images.md)