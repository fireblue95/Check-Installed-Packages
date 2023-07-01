# Check-Installed-Packages
Simple tool for checking the installed packages.

This repository supports checking whether the packages are installed.

Supports checking the types of packages
===
* ### Dpkg
* ### PyPI

Installation
===

```bash
pip3 install PyYAML
```

```bash
git clone https://github.com/fireblue95/Check-Installed-Packages.git
```

Usage
===

Check Dpkg and PyPI
---
```bash
python3 check_packages.py 
```

Check Dpkg only
---
```bash
python3 check_packages.py --no-check-pypi
```

Check PyPI only
---
```bash
python3 check_packages.py --no-check-dpkg
```

Note
=
Please check if the name of the PyPI package in `config.yml` is correct.  
You can verify it by using the `pip3 freeze` command to get the correct name.

## Correct
```bash
opencv-python
PyYAML
pyyaml
```

## Incorrect
```bash
opencvpython
```