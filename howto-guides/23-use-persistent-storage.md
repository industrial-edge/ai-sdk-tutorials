<!--
SPDX-FileCopyrightText: Copyright (C) 2020-2024 Siemens AG

SPDX-License-Identifier: MIT
-->

# How to use persistent storage on AI Inference Server

AI Inference Server (v1.6.0+) allows the use of persistent storage.

You can create and process directories and files in the current working directory, directly from Python.
Folders and files are persisted as long as the pipeline is running. Once the pipeline stopped all files and folders will be deleted.

However, it is possible to store temporary data on AI Inference Server that persists after the pipeline is stopped or even after the edge device is rebooted. These files and folders are accessible for all steps in the pipeline and remain available until the pipeline gets deleted.
​All steps can access this pipeline store from the `​./_pipeline_storage​` folder.\
Any file (folder) created in the ​./_pipeline_storage​ folder will be placed in pipeline storage.

```python
    # store data in persistent storage
    filepath = './_pipeline_storage/sample.txt'
    f = open(filepath, 'w')
    f.write(”example”)
    f.close()
```

>**Restriction**\
The step that originally contains a file or folder named ​_pipeline_storage​ cannot use the pipeline storage.
