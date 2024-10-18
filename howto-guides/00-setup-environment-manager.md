<!--
SPDX-FileCopyrightText: Copyright (C) 2020 - 2024 Siemens AG

SPDX-License-Identifier: MIT
-->

# Setting up an environment manager

When using multiple project templates and notebook editors, we recommend using an environment manager that can help you keeping those environments and the potentially conflicting requirements separate.\
Below you can find instructions for setting up two environment managers:

- [Setting up an environment manager](#setting-up-an-environment-manager)
  - [Setting up Conda](#setting-up-conda)
  - [Setting up Python venv](#setting-up-python-venv)

You can choose any of the above environment managers or your preferred environment manager.

## Setting up Conda

If you choose to install Python using Conda you need a Conda edition installed on your machine. The following page provides guidance on choosing between the [editions of Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html).\

With Conda, you can select the Python version when you create a new environment. The rest of the section assumes setting up your conda environment using [Miniconda installer](https://docs.conda.io/en/latest/miniconda.html#linux-installers)

> ⚠️ **Warning**\
Conda is dual licenced with a commercial and a free licence.\
Please study the license terms of Conda to determine whether you can use it for free or need to pay a license fee.

After the installer is downloaded, start it using a bash shell.

```bash
bash "~/Downloads/Miniconda3-py310_23.1.0-1-Linux-x86_64.sh"
```

After accepting the licence, the installer will ask for a destination folder. By default, it suggests

> /home/${USER}/miniconda3\

Press ENTER to confirm the location, or type in the desired folder path.

As the last step it will offer to put a conda setup script into your shell initializer script (`~/.bashrc`).

> Do you wish the installer to initialize Miniconda3
> by running conda init? [yes|no]

If you answer yes, conda will automatically activate the `base` environment when you start a new shell. This can be disabled while keeping the rest of the conda initializer script.

To disable the automatic activation of the base environment, run:

```bash
conda config --set auto_activate_base false
```

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
