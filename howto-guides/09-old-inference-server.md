<!--
SPDX-FileCopyrightText: Copyright (C) 2020-2024 Siemens AG

SPDX-License-Identifier: MIT
-->

# How to write components for earlier versions (<1.2) of the AI Inference Server

AI Inference Server versions up to 1.1 require the entrypoint to define a function named `run()` instead of `process_input()`. Not only is the function name different, but the component inputs and outputs are passed differently too.

AI Inference Server version 1.1 passes the input variables as a JSON string, which you must convert to a dictionary. On the output side, you must also pass the outputs as a JSON string and embed it into a dictionary with a ready flag.

The following code example shows how to wrap `process_input()` into a `run()` function compatible with AI Inference Server 1.1.

```python
# entrypoint.py
...
# compatibility run() wrapper for process_input()
def run(data: str) -> dict:
    input_data = json.loads(data)
    result = process_input(input_data)
    if result is None:
        answer = {"ready": False, "output": None}
    else:
        answer = {"ready": True, "output": json.dumps(result)}
    return answer
```
