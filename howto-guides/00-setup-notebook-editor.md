<!--
SPDX-FileCopyrightText: Copyright (C) 2020 - 2024 Siemens AG

SPDX-License-Identifier: MIT
-->

# How to setup up a notebook editor

There are many notebook editor and executor software. This guide shows how to set up two of them: Jupyter Lab and Visual Studio Code.

## Jupyter Lab

It is strongly recommended to create a separated environment for installing and running Jupyter Lab, to avoid version collisions with the dependencies of AI SDK or the project template.

First, deactivate the `image_classification` environment. Then create `jupyter_env`, activate it, and install the `jupyterlab` package.

```bash
deactivate
python -m venv ~/venv/jupyter_env
source ~/venv/jupyter_env/bin/activate
python -m pip install --upgrade pip
pip install jupyterlab
```

You can simply start Jupyter Lab from this environment. When the server initializes, it prints out the URLs with which it can be accessed from your browser. Just copy the address pointing to `localhost`, and open it in a browser.\
To start the server, run:

```bash
cd ~/image_classification
jupyter lab --no-browser
```

When the Jupyter server is not running in a virtual machine, it can open the browser automatically. To make this work from WSL2, it requires the following command alias to be created:

```bash
echo -ne "\nalias jupyter-lab='(source ~/venv/jupyter_env/bin/activate && jupyter lab --ServerApp.use_redirect_file=False --browser=\"cmd.exe /c start %s\")'\n\n" >> ~/.bashrc
```

With this alias, you don't need to activate the `jupyter_env` before starting the server. Just step into the project template directory, and invoke the `jupyter-lab` command.

```bash
cd ~/image_classification
jupyter-lab
```

## Visual Studio Code

Visual Studio Code is a versatile code editor, and with the right extensions, it can connect to the virtual Python environments on WSL2, and use the registered kernels to run Jupyter notebooks.\
Download the [VSCode installer](https://code.visualstudio.com/docs/?dv=win64user), and install it on Windows.

If your WSL2 environment is already set up, it will prompt you to install the WSL extension.

> You have Windows Subsystem for Linux (WSL) installed on your system.\
> Do you want to install the recommended extensions for it?

Alternatively, you can manually install the extension with the following command:

```bash
cmd.exe /v /c "set HTTP_PROXY=${HTTP_PROXY}&& set HTTPS_PROXY=${HTTP_PROXY}&& code --install-extension ms-vscode-remote.remote-wsl --disable-telemetry"
```

After the extension is installed, restart VSCode, and on the bottom left, click on the green `><` button, then select `Connect to WSL using Distro...`. Next, open the `image_classification` folder on your virtual Linux machine.\
Alternatively, you can start VSCode from a shell, also specifying the folder to open.

```bash
code ~/image_classification
```

At first start, it will show a popup message:

> Do you trust the authors of the files in this folder?

Select `Yes, I trust the authors`.

When you first open a Jupyter notebook, you will be prompted to install the necessary extensions.

> Do you want to install the recommended extension for Python?

Answer `Yes`, then wait for the extensions to install, then restart VSCode.\
Reopen the Jupyter notebook, and try to run it or click on `select kernels` in the top right corner. Select the `Python environments` option, then choose the `Python (image_classification)` kernel to run the notebook.

### Known issue with updates

The proxy settings configured in your `~/.bashrc` will not take effect when VSCode is started from Windows, and it tries to download its updates. The simple workaround is to first start a Linux shell, so the environment variables are initialized, then start VSCode from this shell.

> ⚠️ Note\
> If VSCode is stuck downloading updates on startup, try to start it from a Linux shell with the command `code`.

### VSCode Extensions

To manually install the notebook extensions for Python and Jupyter, run the following script:

```bash
code --disable-telemetry --install-extension ms-python.python
code --disable-telemetry --install-extension ms-python.vscode-pylance
code --disable-telemetry --install-extension ms-toolsai.jupyter
code --disable-telemetry --install-extension ms-toolsai.jupyter-keymap
code --disable-telemetry --install-extension ms-toolsai.jupyter-renderers
code --disable-telemetry --install-extension ms-toolsai.vscode-jupyter-cell-tags
code --disable-telemetry --install-extension ms-toolsai.vscode-jupyter-slideshow
```
