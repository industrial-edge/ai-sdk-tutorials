<!--
SPDX-FileCopyrightText: Copyright (C) 2020 - 2024 Siemens AG

SPDX-License-Identifier: MIT
-->

### Using Databus connection with type `String`

For use cases with small images and low input rates, you can use Databus. In this case, you need to define the type of component input variable for passing the image as a String that corresponds to a Python str in the input dictionary.  

> ⚠️ Note
The preferred way of transferring images is the `ImageSet` format and ZMQ. Only transfer images over Databus as a last resort, as it is not designed for large volumes of data.

```python
# define input
component.add_input('vision_payload', 'String')
```

AI Inference Server passes the payload provided by the `Vision Connector` directly as a string.
This string is a JSON file that contains metadata and the image itself in data URL-encoded form as follows:

```python
# example image in Vision Connector MQTT JSON format
{
    'timestamp': '2022-02-23T09:29:45.276338',
    'sensor_id': 'a204dba4-274e-43ce-9a71-55de9e715e72',
    'image': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAASwAAAGQCAI...QmCC',
    # note the above URL encoded string is truncated
    'status':
        {
            'genicam_signal': {'code': 3}
        }
}
```

You can extract the URL-encoded image into a PIL image object as follows:

```python
# extract payload
from urllib.request import urlopen
from PIL import Image

def process_input(data: dict):
    payload = json.loads(data['vision_payload'])
    url_encoded_image = payload['image']
    with urlopen(url_encoded_image) as response:
        assert response.headers['Content-type'] in ['image/png', 'image/jpeg']
        image_bytes = response.read()
        return Image.open(io.BytesIO(image_bytes))
```

Refer to the Image Classification project template for a complete example of MQTT and ZMQ
connection variants.

For more details, refer to the [Vision Connector User Guide](https://support.industry.siemens.com/cs/document/109963116/vision-connector?dti=0&lc=en-WW).
