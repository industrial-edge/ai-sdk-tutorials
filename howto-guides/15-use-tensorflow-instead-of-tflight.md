<!--
SPDX-FileCopyrightText: Copyright (C) 2020 - 2025 Siemens AG

SPDX-License-Identifier: MIT
-->

# How to use `TensorFlow` instead of `TensorFlow Light`

On IPC427 or newer Edge Devices you can use the full TensorFlow package instead of the TFlite version.

In the [Image Classification](../e2e-tutorials/image_classification/README.md) end to end tutorial we are providing the necessary resources to try using it with TensorFlow.

In the pipeline creation you need to add the TensorFlow related resources

```python
# component.add_resources('..', ['src/payload.py', 'src/vision_classifier.py'])
# Use this instead:
component.add_resources('..', ['src/payload.py', 'src/vision_classifier_tf.py'])
```

```python
# component.add_resources('..', 'models/classification_mobilnet.tflite')
# Use this instead:
component.add_resources('..', 'models/classification_mobilnet.h5')
```

In `entrypoint.py` you need to import the TensorFlow related dependency

```python
# import vision_classifier as classifier
# Use this instead:
import vision_classifier_tf as classifier
```
