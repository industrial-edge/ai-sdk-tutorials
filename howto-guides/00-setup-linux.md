# How to setup Linux to run AI SDK

## Setting up Python

Before installing anything, the Linux distribution's package list needs to be updated. It is advised to install the upgradeable packages as well. Ubuntu comes with Python version 2 as default, but there is a package which can switch the default to version 3. Also here we install the `zip` package, since we will need it to unpack the project templates and the AI SDK package.

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y zip python-is-python3
```

After the installation, you can check the current Python version with `python --version`. The output should show Python version 3.11.x.
