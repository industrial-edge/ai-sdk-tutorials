<!--
SPDX-FileCopyrightText: 2025 Siemens AG

SPDX-License-Identifier: MIT
-->

# How to process images

The preferred solution to receive images in your Inference Pipeline is to have an installed [Vision Connector](https://support.industry.siemens.com/cs/document/109963116/vision-connector?dti=0&lc=en-WW) and connected to cameras. `Vision Connector` is capable to receive images from the cameras and provides them in 'ImageSet' format for AI Inference Server. This way the images can be received together with their metadata in a standardized format.

## Using `Vision Connector` with type `ImageSet`

This payload format is designed to send images in any format (e.g.: monochrome, or RGB) along with their metadata. This payload also supports sending multiple images in one message.

```json
{
    "version": "1", # version of the Metadata format
    "count": 1,     # Number of images on message
    "timestamp": "2024-06-18T13:00:37.189219",  # Camera acquisition time
    "detail": [     # list of images with detailed information
        {    
            "id": "camera-024581",              # unique image identifier. 
            "timestamp": "1718708437.189219",   # Timestamp provided by the camera
            "width": 600,                       # image width
            "height": 400,                      # image height
            "format": "BayerRG8",               # image format
            "metadata": "",                     # optional extra information on image
            "image": image_bytes                # image binary with the given 'format'
        }
    ]
}

```

As observed, the JSON format is capable of encapsulating a collection of images along with related metadata for both the payload and individual images.  
In this case, the `detail[0].image` field will be a one-dimensional byte array, regardless of whether it is in a monochrome or RGB format, which is defined in the `detail[0].format` field of the payload. When working with this payload in your pipeline, the first step is to convert the byte array to the format required by the model or the next step in the pipeline.

Vision use cases often involve GPU Runtime in the AI Inference Server. When targeting AI Inference Server 2.8.0 or later with ONNX model inputs, keep the tensor dimensions created during pre-processing. AI Inference Server now forwards the dimensional metadata to GPU Runtime and validates it against the model input automatically.

Flattening the input tensor is no longer required and is no longer recommended for AI Inference Server 2.8.0 or later. Flattened input is still accepted for backward compatibility, so existing pipelines continue to work. However, if your model input has multiple dynamic dimensions, do not flatten the tensor because the original shape cannot be reconstructed reliably.

GPU output remains flattened for compatibility reasons. In post-processing, reshape the returned output to the tensor shape expected by your logic before you interpret the values.

The following example demonstrates a solution using the OpenCV and ``Numpy`` libraries.

```python
# build_package.py
# assuming the first step in our Pipeline is 'preprocessing' 
# and we define the ImageSet input with the name 'vision_payload'

preprocessing.add_input('vision_payload', 'ImageSet')

[..]
```

```python
# entrypoint.py
# imports ..

WIDTH = HEIGHT = 224     # expected image size

# assuming the image arrives in the payload above with pixel format BayerRG8
def process_input(payload: dict):
    # extracting image details from the payload
    extracted = payload['vision_payload']
    image_detail = extracted["detail"][0]

    # extracting image metadata
    iuid = image_detail['id']
    width = image_detail.get("width", None)
    height = image_detail.get("height", None)

    if (width, height) != (WIDTH, HEIGHT):
        logger.warn("Image is dropped because of unexpected image size")
        return None

    # reading the byte-array into numpy array with one dimension, 
    image_data = numpy.frombuffer(image_detail['image'], dtype=numpy.uint8)  # BayerRG8, (width x height, )
    
    # forming two-dimensional numpy array with dimensions width and height
    image_data = image_data.reshape(width, height)                           # BayerRG8, (width, height)
    
    # converting from BayerRG8 format to 3-dimensional RGB image
    image_data = cv2.cvtColor(image_data, cv2.COLOR_BayerRG2RGB)             # RGB, (width, height, 3)
    
    # normalizing into [0,1) range and converting to float32
    image_array = image_data.astype(numpy.float32) / 255.  # numpy.float32, (width, height, 3)

    # keeping the tensor dimensions for AI Inference Server 2.8.0 or later GPU Runtime
    inputs = image_array   # numpy.float32, (width, height, 3)
    # for older versions, you should flatten the 3 dimensional array and adding to an empty batch:
    # inputs = numpy.array(image_array.ravel())

    return {
        'input': inputs    # assuming that our ML Model has an input with name 'input'
    }

```

<!-- from VCA user manual, section Accessing camera data via ZeroMQ -->
`Vision Connector` supports mainly the standardized GenICam pixel formats, as the most common `Mono8`, `RGB8` formats or `BayerXX8` formats to reduce network traffic while the color information is still recorded.
For different pixel format it is also recommended to use the GenICam naming convention as described in section 4.35 of the [GenICam_PFNC_2_7.pdf](https://www.emva.org/wp-content/uploads/GenICam_SFNC_v2_7.pdf) document.

### `ImageSet` as Output

As `ImageSet` is designed to be received from `Vision Connector`, this variable type is only allowed as input or between Pipeline steps, but not as output.  
In this case you need to follow and provide the payload format as described above.  
For more details, refer to the [Vision Connector User Guide](https://support.industry.siemens.com/cs/document/109963116/vision-connector?dti=0&lc=en-WW).

### `ImageSet` for previewing images on AI Inference Server

While an ImageSet cannot be part of the pipeline's output variables, it can be an output of a component. In this case the output does not need to be connected anywhere. On the AI Inference Server it is possible to visualize any `ImageSet` input or output variable. It is not recommended to use this feature in production as it can slow down the pipeline. It is useful for testing and validating the model's inference. It is advised to turn off generating `ImageSet` outputs when they are not needed. This is the default state of the AI Inference Server. When the user turns on or off the visualization, the pipeline receives a parameter update call with the boolean `__AI_IS_IMAGE_SET_VISUALIZATION` internal variable. This variable must not be declared explicitly as a pipeline parameter, but the update handler method should be implemented.
The returned result object should not contain the `ImageSet` variable name when preview generation is turned off, otherwise the pipeline fails.

As a safeguard, every Python component of the Pipeline must implement `update_parameters()`, even if the Pipeline does not define any parameter. In that case, provide an empty implementation:

```python
def update_parameters(params: dict):
    pass
```

Entrypoint example for generating an image preview

```python

GENERATE_PREVIEW = False

def update_parameters(params: dict):
    global GENERATE_PREVIEW
    GENERATE_PREVIEW = params.get("__AI_IS_IMAGE_SET_VISUALIZATION", GENERATE_PREVIEW)

def process_input(data: dict):
    # inferencing and output generation code here
    # ...
    result = {
        "output_1": "...",
        "output_2": "...",
        # "preview": None  ## The presence of this key would result in a failing pipeline
    }
    if GENERATE_PREVIEW:
        # this code simply returns the received ImageSet
        result["preview"] = data["vision_payload"]
    return result
```

### Other formats

There are other options to use different payload formats to receive images from sources that do not support `ImageSet`. We recommend a ZMQ connection to receive images, over which you can receive image information in `Binary` or `Object` format.  

A short description on their capabilities can be found in documents:

- [12-use-binary-format-for-images.md](12-use-binary-format-for-images.md)
- [13-use-object-format-for-images.md](13-use-object-format-for-images.md)
- [14-use-string-format-for-images.md](14-use-string-format-for-images.md)
