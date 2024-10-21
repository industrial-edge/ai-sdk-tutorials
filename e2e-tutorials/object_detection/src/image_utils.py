# SPDX-FileCopyrightText": "Copyright (C) Siemens AG 2021. All Rights Reserved."
#
# SPDX-License-Identifier: MIT

import numpy as np
from PIL import ImageDraw, ImageFont

CLASSES = [ '__background__', 'hole', 'scratch' ]
COLORS = list(tuple(x) for x in np.random.randint(low=0, high=255, size=(len(CLASSES), 3)))
_font = ImageFont.load_default(size=11)

_GREEN = (16, 255, 16)  # color for hole boxes
_RED = (255, 16, 16)  # color for scratch boxes

def draw_prediction(image, boxes, labels, scores, threshold = 0.8):
	canvas = ImageDraw.Draw(image)
	for i in range(0, len(boxes)):
		_class = labels[i]
		confidence = scores[i]
		if confidence > threshold:
			box = boxes[i]
			# (startX, startY, endX, endY) = box.astype("int")
			(startY, startX, endY, endX) = box.astype("int")
			label = "{}: {:.2f}%".format(CLASSES[_class], confidence * 100)
			print("[INFO] {} ({})".format(label, box))
			COLOR = _GREEN if _class == 1 else _RED
			canvas.rectangle([(startX, startY), (endX, endY)], outline=COLOR, width=2)

			y = startY - 4 if startY - 4 > 4 else startY + 4
			canvas.text(xy=(startX+4, y), text=label, font=_font)
