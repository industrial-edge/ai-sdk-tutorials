# How to handle Python dependencies

## Processing data

The main part of your Python script is the logic for calculating the output from the input. This is done by your Python code, which can use configuration files and persistent ML models in a well-defined Python environment. To define these resources, the `PythonComponent` class of the `simaticai.deployment` module is used to add dependencies or additional files.
These files are included in the configuration package and extracted in the AI Inference Server as follows:

- Dependencies are installed on the server via pip.
- Additional files are copied into the component directory.

## Python dependencies

The AI Inference Server executes every component of a pipeline in an isolated Python virtual environment. For each component, you must specify which Python packages are required by the Python scripts in that component, including the Python packages required to load persistent Python objects.

### Adding Python dependencies

The Python dependencies of a component can be added in several ways:

- As a standard wheel file or a zip/tar.gz file that contains standard wheel files.\
  In both cases, the packages, which can be precompiled wheel files or pure Python source distributions, are added to the `component.dependencies` dictionary and binaries are zipped into the configuration package. AI Inference server supports only installing source distributions that contain only Python source code.

```python
component.add_python_packages('../packages/my_module-0.0.1-py3-anyany.whl')
component.add_python_packages('../packages/MyPackages.zip')
component.add_python_packages('../packages/my_source_module-0.0.2.tar.gz')
```

> **Recommendations and limitations for using source distributions**\
>  Prefer using wheel files instead of source distributions where possible.\
>  Transitive dependencies of a source distribution must be added to the requirements.txt specifying explicitly the version that matches the targeted Python runtime.\
>  Should there be any unidentified dependencies left, AI SDK will raise an error, which will guide you through resolution.

- Using a standard `requirements.txt`\
  This way, the `component.dependencies` dictionary contains only the dependencies defined in the file. The required wheel files are downloaded while converting the edge configuration package to an edge configuration package using `pip`.

```python
component.set_requirements('./requirements.txt')
```

- By name using a list that contains the names of the Python modules \
  In this case, the method searches for the module in the current Python environment and adds the package with its version and all of its transitive dependencies.

```python
component.add_dependencies(['numpy', 'scikit-learn'])
```

Dependencies can be added by name and version using a list that contains corresponding tuples. When the component is saved, it will perform a check if all specified dependencies can be installed together. Transitive dependencies will also be downloaded.

```python
component.add_dependencies([('pandas', '1.3.0'), ('pyarrow', '3.0.0')])
```

Dependencies added to a component will be installed on the AI Inference Server with the defined version and can be imported into your Python code during execution.

```python
# entrypoint.py or data_processor.py
import numpy as np
import pandas as pd
[...]
```

### Download from non-public repository

Dependencies from non-public repositories can be downloaded by specifying an extra index URL at the beginning of the `requirements.txt` file.

```bash
--extra-index-url https://<API_KEY>@your/private/repository
simaticai
```

Please be aware that if a package is also available in a public repository, `pip` may download it from there and not look for it in the private repository, which may pose a cybersecurity risk.
It is recommended to only use trusted private repositories, pin the version of the package, and check if a package with the same properties already exists on [https://pypi.org/simple](https://pypi.org/simple).

If you want to change the default [https://pypi.org/simple](https://pypi.org/simple) package index, you can do it by using an index URL at the beginning of the `requirements.txt` file. This allows you to download dependencies exclusively from a private repository.

```bash
--index-url https://<API_KEY>@your/private/repository
simaticai
```
