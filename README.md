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
pip install binary-cookies-parser
```
If you want to use the parser as CLI, it's recommended to use pipx to install the package in an isolated environment.

## Usage
After installation, you can use the command-line interface to read a binary cookies file:

```bash
bcparser <path_to_binary_cookies_file>
```
Replace <path_to_binary_cookies_file> with the path to the binary cookie file you want to read.

Or use it in Python:

```python
from binary_cookies_parser.parser import read_binary_cookies_file

cookies = read_binary_cookies_file("path/to/cookies.binarycookies")
```