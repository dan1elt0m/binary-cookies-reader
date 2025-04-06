from typing import List

from typing_extensions import deprecated

from binary_cookies_parser._deserialize import load
from binary_cookies_parser.models import Cookie


@deprecated("read_binary_cookies_file is deprecated, use binary_cookies_parser.load instead.")
def read_binary_cookies_file(file_path: str) -> List[Cookie]:
    with open(file_path, "rb") as f:
        return load(f)
