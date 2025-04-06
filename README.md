[![Github Actions Status](https://github.com/dan1elt0m/binary-cookies-reader/workflows/test/badge.svg)](https://github.com/dan1elt0m/binary-cookies-reader/actions/workflows/test.yml)

# Binary Cookies Reader

This project provides a CLI tool to read and interpret binary cookie files.
The project is based on the cookie reader written by Satishb3 

## Requirements

- Python 3.8 or higher

## Installation
```bash 
pip install binary-cookies-parser
```
If you want to use the parser as CLI, it's recommended to use pipx to install the package in an isolated environment.

## Basic Usage CLI
After installation, you can use the command-line interface to read a binary cookies file:

```bash
bcparser <path_to_binary_cookies_file>
```
Replace <path_to_binary_cookies_file> with the path to the binary cookie file you want to read.

### Basic Usage Python

#### Deserialization
```python
import binary_cookies_parser as bcp 

with open("path/to/cookies.binarycookies", "rb") as f:
    cookies = bcp.load(f)
```

#### Serialization

```python
import binary_cookies_parser as bcp

cookie = {
    "name": "session_id",
    "value": "abc123",
    "url": "https://example.com",
    "path": "/",
    "create_datetime": "2023-10-01T12:34:56+00:00",
    "expiry_datetime": "2023-12-31T23:59:59+00:00",
    "flag": "Secure"
}

with open("path/to/cookies.binarycookies", "wb") as f:
    bcp.dumps(cookie, f)
```

## Output Types

The `bcparser` CLI supports two output types: `json` (default) and `ascii`.

### JSON Output

The `json` output type formats the cookies as a JSON array, making it easy to parse and manipulate programmatically.

Example usage:
```sh
bcparser path/to/cookies.binarycookies --output json
```

Example output JSON:
```json
[
  {
    "name": "session_id",
    "value": "abc123",
    "url": "https://example.com",
    "path": "/",
    "create_datetime": "2023-10-01T12:34:56+00:00",
    "expiry_datetime": "2023-12-31T23:59:59+00:00",
    "flag": "Secure"
  },
  {
    "name": "user_token",
    "value": "xyz789",
    "url": "https://example.com",
    "path": "/account",
    "create_datetime": "2023-10-01T12:34:56+00:00",
    "expiry_datetime": "2023-12-31T23:59:59+00:00",
    "flag": "HttpOnly"
  }
]
```

### ASCII Output
The ascii output type formats the cookies in a simple, line-by-line text format, making it easy to read and pipe to other command-line tools.

Example usage:
```sh
bcparser path/to/cookies.binarycookies --output ascii
```

Example output ASCII:
```text
Name: session_id
Value: abc123
URL: https://example.com
Path: /
Created: 2023-10-01T12:34:56+00:00
Expires: 2023-12-31T23:59:59+00:00
Flag: Secure
----------------------------------------
Name: user_token
Value: xyz789
URL: https://example.com
Path: /account
Created: 2023-10-01T12:34:56+00:00
Expires: 2023-12-31T23:59:59+00:00
Flag: HttpOnly
----------------------------------------
```

### License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Contributing
Contributions are welcome! If you find a bug or have a feature request, please open an issue on GitHub. Pull requests are also welcome.