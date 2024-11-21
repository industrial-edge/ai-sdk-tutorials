<!--
SPDX-FileCopyrightText: Copyright (C) 2020 - 2024 Siemens AG

SPDX-License-Identifier: MIT
-->

# Setting up an environment manager

When using multiple project templates and notebook editors, we recommend using an environment manager that can help you keeping those environments and the potentially conflicting requirements separate.\
Below you can find instructions for setting up two environment managers:

- [Setting up an environment manager](#setting-up-an-environment-manager)
  - [Setting up Python venv](#setting-up-python-venv)

You can choose any of the above environment managers or your preferred environment manager.

## Setting up Python venv

The builtin environment manager for Python requires the desired runtime version preinstalled on the system. You can invoke the environment creation and activation commands by explicitly specifying the path of the Python executable, or you can set up the most frequently used version as the system default.

First you need to add an extra package source to the system.

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
```

Then you can install Python 3.8 and the `venv` environment manager. After that, you need to add the Python versions to the alternatives, with version 3.8 having a higher priority.

```bash
sudo apt install python3.8 python3.8-venv
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 2
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1
```

If you want to switch to an alternative version later, you can change the configuration with

```bash
sudo update-alternatives --config python
```

You can confirm whether the correct version is selected with `python --version`. The output should show:

> Python 3.8.18
