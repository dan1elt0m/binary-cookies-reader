from io import BytesIO
from struct import pack

from binary_cookies_reader.models import Flag
from binary_cookies_reader.reader import (
    interpret_flag,
    read_next_date,
    read_next_int,
    read_next_string,
)


def test_interpret_flag():
    assert interpret_flag(0) == ""
    assert interpret_flag(1) == Flag.SECURE
    assert interpret_flag(4) == Flag.HTTPONLY
    assert interpret_flag(5) == Flag.SECURE_HTTPONLY
    assert interpret_flag(6) == Flag.UNKNOWN


def test_read_string():
    cookie = BytesIO(b"test\0")
    assert read_next_string(cookie, 4) == "test"


def test_read_int():
    cookie = BytesIO(pack("<i", 123))
    assert read_next_int(cookie) == 123


def test_read_date():
    cookie = BytesIO(pack("<d", 978307200.0))
    assert read_next_date(cookie) == 978307200.0
