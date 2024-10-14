# How to mock AI Inference Server logger locally

The Python environment on AI Inference Server injects a Python module named `log_module`, which the Python scripts can use for logging on the
server. To be able to run the same code in a local development environment on a PC, the AI SDK provides a mock of `log_module` in a wheel,
which you can install, import and use in the same way. 

> **Warning**\
> This wheel file must not be included in the pipeline package's dependencies.
