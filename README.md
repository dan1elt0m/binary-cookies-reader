[![Python package](https://github.com/godatadriven/pydantic-avro/actions/workflows/python-package.yml/badge.svg)](https://github.com/binary-cookies-reader/actions/workflows/python-package.yml)
[![PyPI version](https://badge.fury.io/py/binary-cookies-reader.svg)](https://badge.fury.io/py/binary-cookies-reader)
[![CodeQL](https://github.com/godatadriven/pydantic-avro/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/dan1elt0m/binary-cookies-reader/actions/workflows/codeql-analysis.yml)

# Binary Cookies Reader

This project provides a Python script to read and interpret binary cookie files.
The project is based on the cookie reader written by Satishb3 

## Requirements

- Python 3.8 or higher

## Installation
```bash 
pip install binary-cookies-reader
```
If you want to use the bcr CLI, it's recommended to use pipx to install the package in an isolated environment.

## Usage
After installation, you can use the command-line interface to read a binary cookie file:

```bash
bcr <path_to_binary_cookie_file>
```
Replace <path_to_binary_cookie_file> with the path to the binary cookie file you want to read.

Or use it in Python:

```python
from binary_cookies_reader.reader import read_binary_cookies_file

cookies = read_binary_cookies_file("path/to/cookies.binarycookies")
```