# Copyright (C) Siemens AG 2021. All Rights Reserved. Confidential.
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List
from enum import Enum
import uuid

import cv2
import numpy

DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

class ImageFormat(Enum):
    RGB8 = "RGB8"
    BGR8 = "BGR8"
    YUV422Packed = "YUV422Packed"
    YUV422_YUYV_Packed = "YUV422_YUYV_Packed"
    Mono8 = "Mono8"
    BayerRG8 = "BayerRG8"
    BayerGR8 = "BayerGR8"
    BayerBG8 = "BayerBG8"
    BayerGB8 = "BayerGB8"

@dataclass
class ImageDetails:
    id: str
    width: int
    height: int

    seq: int = field(default=0)
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)

    format: ImageFormat = field(default=ImageFormat.RGB8)
    image: bytes = field(default=b"")

    def __post_init__(self):
        assert isinstance(self.id, str)
        assert isinstance(self.timestamp, datetime)
        assert isinstance(self.width, int) and self.width > 0
        assert isinstance(self.height, int) and self.height > 0
        assert isinstance(self.format, ImageFormat) and self.format in ImageFormat.__members__.values()
        assert isinstance(self.image, bytes) and len(self.image) > 0

    @staticmethod
    def from_dict(data: dict):
        try:
            details = ImageDetails(
                id          =   data.get("id", f"simaticai-image-{datetime.now().timestamp()}"),
                seq         =    data.get("seq", 0),
                timestamp   =   datetime.strptime(data.get("timestamp"), DATE_TIME_FORMAT),
                format      =   ImageFormat[data.get("format", "RGB8")],
                width       =   data.get("width", 0),
                height      =   data.get("height", 0),
                metadata    =   data.get("metadata", {}),
                image       =   data.get("image", b"")
            )
        except Exception as e:
            raise ValueError(f"Error parsing image details: {repr(e)}")
        return details

    def to_dict(self):
        return {
            "id": self.id,
            "seq": self.seq,
            "timestamp": self.timestamp.isoformat(timespec='milliseconds') + "Z",
            "format": self.format.value,
            "width": self.width,
            "height": self.height,
            "metadata": self.metadata,
            "image": self.image
        }

    @staticmethod
    def from_image(image_path: Path) -> "ImageDetails":
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError(f"Image file {image_path} not found")

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return ImageDetails(
            id=image_path.name,
            timestamp=datetime.now(),
            width=image.shape[1],
            height=image.shape[0],
            format=ImageFormat.RGB8,
            image=bytes(image.ravel())
        )
    
    def update_image(self, image: numpy.ndarray, image_format: ImageFormat):
        self.format = image_format
        self.height = image.shape[0]
        self.width = image.shape[1]
        self.image = image.ravel().tobytes()
    
    def get_image_array(self) -> numpy.ndarray:
        
        image = self.image
        image = numpy.frombuffer(image, dtype=numpy.uint8)
        match self.format:
            case ImageFormat.RGB8 | ImageFormat.BGR8:
                image = image.reshape(self.height, self.width, 3)
            case ImageFormat.Mono8 | ImageFormat.BayerRG8 | ImageFormat.BayerGR8 | ImageFormat.BayerBG8 | ImageFormat.BayerGB8:
                image = image.reshape(self.height, self.width)
            case ImageFormat.YUV422Packed | ImageFormat.YUV422_YUYV_Packed:
                image = image.reshape(self.height, self.width, 2)
            case _:
                raise ValueError(f"Unsupported image format: {self.format}")
        return image
    
    def get_image_rgb(self) -> numpy.ndarray:
        """OpenCV uses following conversion constants for Bayer patterns when using 2-letter notations:

        'There are several modifications of the above pattern that can be achieved by shifting the pattern one pixel left and/or one pixel up.
        The two letters C_1 and C_2 in the conversion constants CV_Bayer{C_1 C_2}2BGR and CV_Bayer{C_1 C_2}2RGB indicate the particular pattern type.
        These are components from the second row, second and third columns, respectively.'
    
        Source: https://docs.opencv.org/4.12.0/de/d25/imgproc_color_conversions.html

        It is possible to use the more common 'classical' naming scheme for the various Bayer patterns with OpenCV, for example,
        cv2.COLOR_BayerBG2RGB == cv2.COLOR_BayerRGGB2RGB

        For this reason, when converting from Bayer, one should use the 4-letter notation function call of OpenCV,
        to avoid confusion.
        """
        image = self.get_image_array()
        match self.format:
            case ImageFormat.Mono8:
                return cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            case ImageFormat.RGB8:
                return image
            case ImageFormat.BGR8:
                return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            case ImageFormat.BayerRG8:
                return cv2.cvtColor(image, cv2.COLOR_BayerRGGB2RGB)
            case ImageFormat.BayerGR8:
                return cv2.cvtColor(image, cv2.COLOR_BayerGRBG2RGB)
            case ImageFormat.BayerBG8:
                return cv2.cvtColor(image, cv2.COLOR_BayerBGGR2RGB)
            case ImageFormat.BayerGB8:
                return cv2.cvtColor(image, cv2.COLOR_BayerGBRG2RGB)
            case ImageFormat.YUV422Packed:
                return cv2.cvtColor(image, cv2.COLOR_YUV2RGB_Y422)
            case ImageFormat.YUV422_YUYV_Packed:
                return cv2.cvtColor(image, cv2.COLOR_YUV2RGB_YUYV)
            case _:
                raise ValueError(f"Unsupported image format: {self.format}")


@dataclass
class ImageSet:
    version: str = field(default="1.0")
    cameraid: str = field(default_factory=uuid.uuid4)
    timestamp: datetime = field(default_factory=datetime.now)
    count: int = field(default=0)

    detail: List[ImageDetails] = field(default_factory=list)

    def add_image(self, image: ImageDetails):
        self.detail.append(image)
        self.count += 1

    def get_image_array(self, index: int = 0) -> numpy.ndarray:
        if index < 0 or index >= len(self.detail):
            raise IndexError("Index out of range")
        
        image = self.detail[index].get_image_array()

        return image
    
    def get_image_rgb(self, index: int = 0) -> numpy.ndarray:
        if index < 0 or index >= len(self.detail):
            raise IndexError("Index out of range")
        
        return self.detail[index].get_image_rgb()

    def to_dict(self):
        return {
            "version": self.version,
            "count": self.count,
            "cameraid": str(self.cameraid),
            "timestamp": self.timestamp.isoformat(timespec='milliseconds') + "Z",
            "detail": [image.to_dict() for image in self.detail]
        }
    
    @staticmethod
    def from_dict(data: dict):
        return ImageSet(
            version=data.get("version", "1.0"),
            count=data.get("count", 0),
            cameraid=uuid.UUID(data.get("cameraid", str(uuid.uuid4()))),
            timestamp=datetime.strptime(data.get("timestamp"), DATE_TIME_FORMAT),
            detail=[ImageDetails.from_dict(image) for image in data.get("detail", [])]
        )
