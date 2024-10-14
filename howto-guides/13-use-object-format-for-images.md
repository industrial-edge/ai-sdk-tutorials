# How to use `Object` format for images

Instead of sending image data over MQTT as a `String`, you can use ZMQ to feed the running pipeline with images using the `Object` format.
You have to create and configure a ZMQ connector, and configure your pipeline variables accordingly in AI Inference Server.

> ⚠️ Note
The preferred way of transferring images is the `ImageSet` format and ZMQ. Only use the `Object` format if `ImageSet` is not available.

## `Object` Input

```python
# component.add_input('vision_payload', 'String')
# Use this instead:
component.add_input('vision_payload', 'Object')
```

In `entrypoint.py` in `process_input`:

```python
# vision_payload = json.loads(data['vision_payload'])
# pil_image = payload.get_image_from_vision_mqtt_payload(vision_payload)

# Use this instead:
pil_image = payload.get_image_from_vision_zmq_dict(data["vision_payload"])
```

## `Object` Output

If you want to return the thumbnail, add the appropriate output.

```python
component.add_input('vision_payload', 'Object')
component.add_output('prediction', 'String')
# Add this line:
component.add_output('thumbnail', 'Object')
```

In `entrypoint.py` in `process_input`:

```python
return {
    "prediction": str(prediction),
    "ic_probability": metric_output(probability),
    # Add this line:
    "thumbnail": payload.create_image_output(pil_image),
}
```

## Restrictions on `Object` format

AI Inference Server version 1.6 imposes restrictions on the dictionaries returned by the inference wrappers for output variables of type `Object`. The returned dictionary must contain a metadata string and a binary sequence. The metadata and the binary sequence can have any key in the `dict`, but must be of type `str` and `bytes` respectively.\
For details, refer to the [Returning results](./06-return-processing-results.md) howto guide.

> ⚠️ Note
The structure of dictionaries that is received as pipeline input is different from the dictionary
structure that is required as component output. For details, see the section [Processing Images](./11-process-images.md).
