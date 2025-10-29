# SPDX-FileCopyrightText: 2025 Siemens AG
#
# SPDX-License-Identifier: MIT

import numpy
from PIL import ImageDraw, ImageFont

CLASSES = [ '__background__', 'hole', 'scratch' ]
COLORS = list(tuple(x) for x in numpy.random.randint(low=0, high=255, size=(len(CLASSES), 3)))
_font = ImageFont.load_default(size=11)

_GREEN = (16, 255, 16)  # color for hole boxes
_RED = (255, 16, 16)  # color for scratch boxes

def draw_prediction(image, boxes, labels, scores, threshold = 0.8):
	canvas = ImageDraw.Draw(image)
	boxes = boxes.reshape(-1, 4)  # on AI Inference Server, the output of GPURuntime is flattened into a one-dimensional array; we should reshape it to two-dimensional
	for i in range(0, len(boxes)):
		_class = labels[i]
		confidence = scores[i]
		if confidence > threshold:
			box = boxes[i]
			(startY, startX, endY, endX) = box.astype("int")
			label = "{}: {:.2f}%".format(CLASSES[_class], confidence * 100)

			COLOR = _GREEN if _class == 1 else _RED
			canvas.rectangle([(startX, startY), (endX, endY)], outline=COLOR, width=2)

			y = startY - 4 if startY - 4 > 4 else startY + 4
			canvas.text(xy=(startX+4, y), text=label, font=_font)
