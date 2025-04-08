from typing import List

from typing_extensions import deprecated

from binarycookies._deserialize import load
from binarycookies.models import Cookie


@deprecated("read_binary_cookies_file is deprecated, use binarycookies.load instead.")
def read_binary_cookies_file(file_path: str) -> List[Cookie]:
    with open(file_path, "rb") as f:
        return load(f)
