# How to create the entrypoint

AI Inference Server itself receives the data payload from the input data connection. With each input, the AI Inference Server triggers the `process_input(data: dict) -> dict` function in the entrypoint module. After `process_input()` returns, the server forwards the output to the next pipeline component, or emits it as pipeline output over the output data connection.

## Example

```python
# entrypoint.py
import sys
from pathlib import Path

# when you import from source, the parent folder of the module ('./src') must be added to the system path
sys.path.insert(0, str(Path('./src').resolve()))

from my_module import data_processor # should be adapted to your code

def process_input(data: dict) -> dict:

return data_processor.process_data(data["input_1"], data["input_2"])
```

In this case, it is assumed that business logic is encapsulated in
`data_processor.process_data()`. You can place the code into your package and modify only the reference to your data processor.
