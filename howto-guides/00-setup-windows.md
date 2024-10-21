<!--
SPDX-FileCopyrightText: Copyright (C) 2020 - 2024 Siemens AG

SPDX-License-Identifier: MIT
-->

# How to setup Windows to run AI SDK

## Prerequisites

You will need a 64 bit Windows version to run AI SDK and the notebooks in the templates.

Before you begin, make sure that you have internet access. If you access the internet through a proxy, e.g. because you are working in a corporate network directly or via VPN, please make sure that you have configured `pip` and, if you plan to use it, `conda` to use the correct proxy. Setting the environment variables `http_proxy` and `https_proxy` covers both. A detailed explanation about alternative solutions is provided here:

- https://pip.pypa.io/en/stable/user_guide/#using-a-proxy-server
- https://docs.anaconda.com/anaconda/user-guide/tasks/proxy/

If you have no `USERPROFILE` environment variable set, please set it so that it contains the path to a directory that belongs personally to you. You can check the variable by echoing it on Windows Command Prompt.

```dosbatch
echo %USERPROFILE%
```

## Setting up WSL2 on Windows

There are multiple solution for running Linux on a virtual machine. We recommend using WSL2 as it is a builtin feature of Windows. This creates a Linux environment that is tightly integrated with Windows, and it is capable of running Python packages that have binary parts compiled only for POSIX type operating systems.
For activating and setting up this feature, please follow the official [Microsoft guideline](https://learn.microsoft.com/en-us/windows/wsl/install-manual).
At the end of this official guide, you can find instructions on how to download a Linux distribution manually in case the Microsoft Store is not accessible on your computer.
Alternatively, you can install a distribution directly with `wsl.exe`.

If you are using Visual Studio Code, you can install the WSL extension, which enables you to run Jupyter Notebooks in the virtual Linux environment and work in the WSL2 environment just as if you would work natively on Windows.

Once you have WSL2 activated, you can list the distributions you can install by typing the following into a Windows Command Prompt (`cmd.exe`) or PowerShell:

```dosbatch
wsl.exe -l -o
```

### Installing Ubuntu 22.04

AI SDK was tested on Ubuntu Linux 22.04, and the rest of this guide will provide guidance on installing it under a Windows virtual environment and using it to run the project templates.

The easiest way to download and install it is to type the following command into a Windows Command Prompt:

```dosbatch
wsl.exe --install --web-download -d Ubuntu-22.04
```

When the installer finishes, it will ask for a user name and a password. The user name can not contain whitespace characters. If your Windows user name does not contain whitespaces, we recommend to set the Linux user name to the same.

### Starting a Linux shell

1. Search for the Ubuntu App in Start Menu, and launch it. This will open a separate terminal window.

1. Start a Windows Command Prompt with `cmd.exe`. In the terminal, list the installed distributions with

    ```dosbatch
    wsl.exe -l -v --all
    ```

    Start the Linux shell with the desired distribution name.

    ```dosbatch
    wsl.exe -d Ubuntu-22.04
    ```

    This will run the shell in the same window.

1. Alternatively, you can try using [Windows Terminal](https://apps.microsoft.com/detail/windows-terminal/9N0DX20HK701?hl=en-us&gl=AT). It is a tabbed window, where you can easily launch new tabs using Linux distributions, PowerShell or the Command Prompt.

> ⚠️ Note\
> From this point on, this guide assumes that commands are executed in a Linux shell.

### Configuring network proxy

If you access the internet through a proxy, you need to set up the following environment variables inside the virtual environment.
To make sure every software finds the variables, both upper and lowercase names are needed. In `http_proxy` specify your company proxy's URL, and in `no_proxy` the domains or IP addresses which don't need to go through the proxy server. Consult with your company's IT department which proxy servers can you use. The following command will put these variables with example values into your shell initializer script.

```bash
cat >> ~/.bashrc <<'EOF'
export http_proxy=http://proxy.mycompany.com:9400
export https_proxy=$http_proxy
export HTTP_PROXY=$http_proxy
export HTTPS_PROXY=$http_proxy
export no_proxy=127.0.0.1,localhost,mycompany.com
export NO_PROXY=$no_proxy
EOF
```

To be able to access these environment variables when you are running commands with administrative privileges, run the following command to append your `sudoers` configuration. The command `sudo` will ask for the password you have set up at the end of Linux installation.

```bash
echo -ne "\nDefaults:%sudo env_keep += \"http_proxy https_proxy HTTP_PROXY HTTPS_PROXY no_proxy NO_PROXY\"\n" | sudo tee -a /etc/sudoers
```

> ⚠️ Note\
> These changes will only take effect after the Linux shell is restarted.

### Accessing files from WSL2

From the virtual Linux you can access your files on Windows using the path prefix `"/mnt/c/Users/*<Windows Username>*/"`. As a rule of thumb, always use double quotes around paths, this way whitespaces in file or folder names will not cause problems.

To simplify accessing the files downloaded on Windows, you can create a symlink to your `Downloads` folder.

> ⚠️ Note\
> Later steps assume that you have created this symlink. If not, you will need to substitute the file paths manually.

```bash
WINUSER=$(cmd.exe /c echo %username% 2>/dev/null | tr -d "\n\r")
ln -s "/mnt/c/Users/$WINUSER/Downloads/" ~/Downloads
```

## Known issues

### Issue with DNS resolution

In some networks, usually when a VPN connection is used, the default domain name resolution strategy of WSL2 does not work.
If a command that uses the network, gives the following error, the name servers must be manually configured.

> Temporary failure in name resolution.

This is an example list of name server IP addresses. Consult with your company's IT department which nameservers can you use.

```bash
NAMESERVERS="555.123.456.100, 555.123.456.101, 8.8.8.8"
```

The following script disables the automatic generation of `/etc/resolv.conf`, and replaces it with a list using the IP addresses in the `NAMESERVERS` variable.

```bash
echo -ne "[network]\ngenerateResolvConf = false\n" | sudo tee /etc/wsl.conf

sudo rm -rf /etc/resolv.conf

sed -E "s/^|, */\nnameserver /g" <<<"${NAMESERVERS}" | sudo tee /etc/resolv.conf
```

The script recreates the `/etc/resolv.conf` file, and prints it's content to the screen as well.

> nameserver 555.123.456.100\
 nameserver 555.123.456.101\
 nameserver 8.8.8.8

In order for these changes to take effect, the virtual Linux machine needs to be restarted.

> ⚠️ Note\
> In this step, restarting just the Linux shell is not enough.

The following command will shut down all running Linux distributions.

```bash
wsl.exe --shutdown
```

### Issue with WSLg

WSLg is an extension of WSL2 which allows to run Linux applications which require a graphical user interface. Every time the WSL subsystem is restarted, it will create a popup with the following message:

> The identity of the remote computer cannot be verified.\
> Do you want to connect anyway?

Answering yes is not a security risk, and the popup will disappear until the next restart. Currently, there is no official fix for this issue.\
However, WSLg is not required to run AI SDK and the project templates, so it can be disabled by adding `guiApplications=false` under the `[wsl2]` section of the config file `.wslconfig` in your Windows home folder.

The following script adds the section to the config file to disable WSLg.

```bash
WINUSER=$(cmd.exe /c echo %username% 2>/dev/null | tr -d "\n\r")
echo -ne "[wsl2]\nguiApplications=false\n" >> "/mnt/c/Users/${WINUSER}/.wslconfig"
```

### Path length issue

Sometimes the path of project files can be too long. On Windows by default paths have a 256 character length limitation, which we recommend to change. It can be changed via the Group Policy in `Computer Configuration > Administrative Templates > System > Filesystem > Enable NTFS long paths`. Or when you install Python for Windows, the installer has an extra step at the end to disable the path length limitation. You will need administrator privileges in both cases.

### TensorFlow Lite issue

Some of our notebooks suggests to use TFLite instead of the full TensorFlow package. This is a smaller and faster runtime for TensorFlow models. It is possible to use either on AI Inference Server, but less powerful Edge Devices can only run TFLite models.
However, if you want to test your model locally, currently there is no official TFLite runtime for Windows.
You can either use the full TensorFlow package, or you can build your TFLite models in a virtual Linux environment.

> **Note**\
To complete setup, follow the steps described in the [Linux setup](#linux-setup) section.
