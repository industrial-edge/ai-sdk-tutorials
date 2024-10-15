<!--
SPDX-FileCopyrightText: Copyright (C) 2020 - 2024 Siemens AG
SPDX-FileCopyrightText: Copyright (C) 2020-2024 Siemens AG

SPDX-License-Identifier: MIT
-->

# How to use `Binary` format for images

Instead of sending image data over MQTT as a `String`, you can use the `Binary` format.

> ⚠️ Note
The preferred way of transferring images is the `ImageSet` format and ZMQ.  Only use the `Binary` format if `ImageSet` is not available.

## `Binary` Input

You need to define a `Binary` type copmonent input

```python
# component.add_input('vision_payload', 'String')
# Use this instead:
component.add_input('vision_payload', 'Binary')
```

In the `process_input` in the `entrypoint.py` you need to process the payload as binary input:

```python
# vision_payload = json.loads(data['vision_payload'])
# pil_image = payload.get_image_from_vision_mqtt_payload(vision_payload)

# Use this instead:
pil_image = payload.get_image_from_binary_input(data, "vision_payload")
```

## `Binary` Output

If you want to return the thumbnail, add the appropriate output.

```python
component.add_input('vision_payload', 'Binary')
component.add_output('prediction', 'String')
# Add this line:
component.add_output('thumbnail', 'Binary')
```

In `process_input` in the `entrypoint.py` you need to return the thumbnail:

```python
return {
    "prediction": str(prediction),
    "ic_probability": metric_output(probability),
    # Add this line:
    "thumbnail": payload.create_binary_output(pil_image),
}
```

## Restrictions on `Binary` format

Currently, the `Binary` data format can only be used as pipeline input and output with the ZMQ connector.

However, it can be used as an intermediate format between pipeline steps without any limitations.
