# Copyright (C) Siemens AG 2021. All Rights Reserved. Confidential.

"""
Common methods for handling image payload with different connectors.

"""

from urllib.request import urlopen
import base64
import cv2
import datetime
from itertools import chain
import json
import numpy
from pathlib import Path
from PIL import Image
import io
import uuid

IMAGE_WIDTH = 224
IMAGE_HEIGHT = 224
IMAGE_SIZE = (IMAGE_WIDTH, IMAGE_HEIGHT)
counter = 0
width = 0
height = 0

def create_mqtt_payload(filepath):
    """
    Packages an image file into Vision Connector payload format for testing.

    Args:
        filepath: Path to an image file.

    Returns:
        dict: The Vision Connector `Object`.
    """

    with open(filepath, "rb") as image_file:
        content = image_file.read()
    image = base64.b64encode(content).decode('ascii')

    extension = Path(filepath).suffix
    extension_lower = extension.lower()
    if extension_lower == ".png":
        image_prefix = "data:image/png;base64,"
    elif extension_lower in [".jpg", ".jpeg"]:
        image_prefix = "data:image/jpeg;base64,"
    else:
        assert False, f"Unsupported image file suffix {extension}"

    timestamp = datetime.datetime.now().isoformat()
    sensor_id = "a204dba4-274e-43ce-9a71-55de9e715e72"
    status = {"genicam_signal": {"code": 3}}

    vision_connector_data = json.dumps({
        "timestamp": timestamp,
        "sensor_id": sensor_id,
        "image": image_prefix + image,
        "status": status
    })

    return vision_connector_data


def get_image_from_vision_mqtt_payload(vision_payload):
    """
    Takes a Vision Connector JSON payload, decodes the image and returns it as PIL image object resized to the input shape of the network.

    Args:
        vision_payload: A Vision Payload `Object`.

    Returns:
        Image: The PIL Image extracted from the Vision Connector `Object`. Returns None if decoding fails.
    """
    from log_module import LogModule
    logger = LogModule()

    try:
        image_string = vision_payload['image']
        with urlopen(image_string) as response:
            assert response.headers["Content-type"] in ["image/png", "image/jpeg"]
            logger.debug("Verified image type is PNG or JPEG")
            image_bytes = response.read()
            pil_image = Image.open(io.BytesIO(image_bytes)).resize(IMAGE_SIZE)
            logger.debug(f"Image info: {pil_image}")
        return pil_image
    except BaseException:
        logger.debug("Error decoding image from vision payload")
    return None


def create_zmq_dict(file_path: Path):
    """
    Provides Vision Connector `Object` payload in a dictionary with key "image" that is specified as single input of inference node.

    Args:
        file_path (Path): The image file to be packaged.

    Returns:
        dict: The image formatted as a Vision Connector `Object` output.
    """

    image = Image.open(file_path)
    image = image.convert(mode='RGB', colors=256)

    payload = { "image":
                {
                    "resolutionWidth": image.width,
                    "resolutionHeight": image.height,
                    "mimeType": "image/raw",
                    "dataType": "uint8",
                    "channelsPerPixel": 3,
                    "image": _swap_bytes(image.tobytes())
                }
                }
    return payload


def create_image_output(image: Image):
    """
    Takes a PIL image and packages it into an `Object` payload format.

    Args:
        image (Image): The PIL Image to be packaged.

    Returns:
        dict: The image formatted as an `Object` output.
    """
    output_image = {
        "metadata": json.dumps( {
            "resolutionWidth": image.width,
            "resolutionHeight": image.height
        }
        ),
        "bytes": image.tobytes()
    }
    return output_image


def get_image_from_vision_zmq_dict(image_data: dict):
    """
    Takes a Vision Connector `Object` payload in a dictionary, decodes the image and returns it as PIL image object resized to the input shape of the network.

    Args:
        image_data (dict): A dictionary containing the Vision Connecto `Object`.

    Returns:
        Image: The PIL image extracted from a Vision Connector `Object`. Returns None if decoding fails.
    """
    from log_module import LogModule
    logger = LogModule()

    global counter, width, height
    counter = (counter + 1) % 10

    if image_data["dataType"] != "uint8" or image_data["channelsPerPixel"] != 3:
        logger.error("The image must be sent with data type uint8 and 3 channels per pixel.")
        return None

    try:
        width = image_data["resolutionWidth"]
        height = image_data["resolutionHeight"]

        # The image is received with 'BGR' byte order
        pil_image = Image.frombytes("RGB", (width, height), image_data["image"], "raw", 'BGR').resize(IMAGE_SIZE)
        logger.debug(f"Image info: {pil_image}")

        return pil_image
    except BaseException:
        logger.warning("Error decoding image from vision payload")
    return None


def _swap_bytes(image_bytes):
    """
    Takes raw image data in `bytes` format and converts RGB to BGR or vice versa.

    Args:
        image_bytes: Raw bytes of a PIL Image.

    Returns:
        bytes: Raw bytes of a PIL Imag.
    """

    number_of_pixels = int(len(image_bytes) / 3)
    list_of_bytes = [[image_bytes[3*i+2], image_bytes[3*i+1], image_bytes[3*i]] for i in range(number_of_pixels)]
    image_bytes = bytes(chain.from_iterable(list_of_bytes))

    return image_bytes


def create_binary_output(image):
    """
    Takes a PIL image and writes it as PNG into a memory buffer, then returns it as a `bytes` array.

    Args:
        image: The PIL image to be packaged.

    Returns:
        bytes: The raw bytes of the image in PNG format.
    """
    image = image.convert(mode='RGB', colors=256)

    membuf = io.BytesIO()
    image.save(membuf, format="png")

    return membuf.getvalue()


def create_binary_dict(file_path, name="image"):
    """
    Provides `Binary` payload in a dictionary with key "image" that is specified as single input of inference node.

    Args:
        file_path: The image file to be packaged.
        name (str): Key for the `Binary` data in the dictionary

    Returns:
        dict: The image formatted as a `Binary` output.
    """
    image = Image.open(file_path)

    return { f"{name}": create_binary_output(image) }


def get_image_from_binary_input(data: dict, name="image"):
    """
    Takes a `Binary` pipeline input and extracts a PIL image from it.

    Args:
        data (dict): Pipeline input dictionary
        name (str): Key for the `Binary` data in the dictionary

    Returns:
        Image: The extracted image as a PIL Image.
    """
    binary = data[name]

    if not isinstance(binary, bytes):
        from log_module import LogModule
        logger = LogModule()
        logger.error(f"The variable '{name}' is not a 'bytes' instance.")
        return None

    return ( Image
             .open(io.BytesIO(binary))
             .convert(mode='RGB', colors=256)
             .resize(IMAGE_SIZE) )


def create_imageset_dict(image_path, image_format="RAW"):
    timestamp = datetime.datetime.now().isoformat()

    if image_format == "RAW":
        image = Image.open(image_path)
        width, height = image.size
        with open(image_path, "rb") as fp:
            image_bytes = fp.read()
    elif image_format == "BGR8":
        image = Image.open(image_path)
        width, height = image.size
        image_bytes = image.convert(mode='RGB', colors=256)
    elif image_format == "BayerRG8":
        image_bytes, width, height = image_to_bayer(image_path)

    return {
        "version": "1",
        "count": 1,
        "timestamp": timestamp,
        "detail": [{
            "id": str(image_path),
            "timestamp": timestamp,
            "width": width,
            "height": height,
            "format": image_format,
            "image": bytes(image_bytes)
        }]
    }


def create_imageset_payload(file_path: Path):
    image = Image.open(file_path)
    image = image.convert(mode='RGB', colors=256)
    timestamp = datetime.datetime.now().isoformat()

    metadata = json.dumps({
        "version": "1",
        "count": 1,
        "timestamp": timestamp,
        "detail": [{
            "id": file_path,
            "timestamp": timestamp,
            "width": image.width,
            "height": image.height,
            "format": "BGR8",
        }]
    }).encode(encoding="utf-8")

    return [
        metadata,
        _swap_bytes(image.tobytes())
    ]

def image_to_bayer(image_path):
    im = cv2.imread(image_path)
    im = cv2.resize(im, (224, 224)) # RGB image 224x224x3
    (height, width) = im.shape[:2]
    (R,G,B) = cv2.split(im)

    bayerrg8 = numpy.zeros((height, width), numpy.uint8)

    # strided slicing for this pattern:
    #   R G
    #   G R
    bayerrg8[0::2, 0::2] = R[0::2, 1::2] # top left
    bayerrg8[0::2, 1::2] = G[0::2, 0::2] # top right
    bayerrg8[1::2, 0::2] = G[1::2, 1::2] # bottom left
    bayerrg8[1::2, 1::2] = B[1::2, 0::2] # bottom right

    return bayerrg8, width, height