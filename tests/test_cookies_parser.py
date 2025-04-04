from datetime import datetime, timezone
from io import BytesIO
from struct import pack
from unittest.mock import ANY, patch

import pytest

from binary_cookies_parser import load
from binary_cookies_parser.models import Flag
from binary_cookies_parser.parser import (
    binary_cookies_reader,
    interpret_flag,
    mac_epoch_to_date,
    read_binary_cookies_file,
    read_cookie,
)


def test_interpret_flag():
    assert interpret_flag(0) == Flag.UNKNOWN
    assert interpret_flag(1) == Flag.SECURE
    assert interpret_flag(4) == Flag.HTTPONLY
    assert interpret_flag(5) == Flag.SECURE_HTTPONLY
    assert interpret_flag(6) == Flag.UNKNOWN


def test_mac_epoch_to_date():
    epoch = 0  # This corresponds to 2001-01-01 00:00:00
    expected_date = datetime(2001, 1, 1, 0, 0, tzinfo=timezone.utc)
    assert mac_epoch_to_date(epoch) == expected_date


def test_read_cookie():
    from io import BytesIO

    # Create a mock binary cookie data
    cookie_size = 81
    cookie_data = BytesIO()
    cookie_data.write(pack("<i", cookie_size))  # cookie size
    cookie_data.write(pack("<i", 0))  # unknown
    cookie_data.write(pack("<i", 1))  # flag (SECURE)
    cookie_data.write(pack("<i", 0))  # unknown
    cookie_data.write(pack("<i", 56))  # url offset
    cookie_data.write(pack("<i", 68))  # name offset
    cookie_data.write(pack("<i", 73))  # path offset
    cookie_data.write(pack("<i", 75))  # value offset
    cookie_data.write(b"\x00\x00\x00@\xe4'\xcdA")  # unknown (8 bytes)
    cookie_data.write(pack("<d", 978307200.0))  # expiry date offset = 56 - 8 bytes = 48
    cookie_data.write(pack("<d", 978307200.0))  # creation date
    cookie_data.write(b"example.com\0")  # url
    cookie_data.write(b"name\0")  # name
    cookie_data.write(b"/\0")  # path
    cookie_data.write(b"value\0")  # value
    cookie_data.seek(0)

    cookie = read_cookie(cookie_data, cookie_size)
    assert cookie.name == "name"
    assert cookie.value == "value"
    assert cookie.url == "example.com"
    assert cookie.path == "/"
    assert cookie.flag == Flag.SECURE
    assert cookie.create_datetime == datetime(2032, 1, 2, 0, 0, tzinfo=timezone.utc)
    assert cookie.expiry_datetime == datetime(2032, 1, 2, 0, 0, tzinfo=timezone.utc)


def test_binary_cookies_reader():
    with patch("binary_cookies_parser.parser.read_cookie") as mock_read_cookie:
        page_data = b"\x01\x00\x00\x00\x01\x00\x00\x00\x08\x00\x00\x00" + b"\x00" * 65
        binary_cookies_reader(BytesIO(page_data))
        assert mock_read_cookie.call_count == 1


def test_read_binary_cookies_file(tmp_path):
    with patch("binary_cookies_parser.parser.binary_cookies_reader") as mock_binary_cookies_reader:
        file_path = tmp_path / "Cookies.binarycookies"
        with open(file_path, "wb") as f:
            f.write(b"cook")  # File Magic String
            f.write(b"\x00\x00\x00\x01")  # number of pages
            f.write(b"\x00\x00\x00\x4d")  # page size
            f.write(b"\x01\x00\x00\x00\x04\x00\x00\x00\x4d\x00\x00\x00" + b"\x00" * 65)

        read_binary_cookies_file(str(file_path))
        mock_binary_cookies_reader.assert_called_with(ANY)


def test_read_binary_cookies_file_multiple_pages(tmp_path):
    with patch("binary_cookies_parser.parser.binary_cookies_reader") as mock_binary_cookies_reader:
        file_path = tmp_path / "Cookies.binarycookies"
        with open(file_path, "wb") as f:
            f.write(b"cook")  # File Magic String
            f.write(b"\x00\x00\x00\x02")  # number of pages
            f.write(b"\x00\x00\x00\x4d")  # page size for first page
            f.write(b"\x00\x00\x00\x4d")  # page size for second page
            f.write(b"\x01\x00\x00\x00\x04\x00\x00\x00\x4d\x00\x00\x00" + b"\x00" * 65)  # first page content
            f.write(b"\x01\x00\x00\x00\x04\x00\x00\x00\x4d\x00\x00\x00" + b"\x00" * 64)  # second page content

        read_binary_cookies_file(str(file_path))
        assert mock_binary_cookies_reader.call_count == 2
        assert (
            mock_binary_cookies_reader.call_args_list[0][0][0].read()
            == b"\x01\x00\x00\x00\x04\x00\x00\x00\x4d\x00\x00\x00" + b"\x00" * 65
        )
        assert (
            mock_binary_cookies_reader.call_args_list[1][0][0].read()
            == b"\x01\x00\x00\x00\x04\x00\x00\x00\x4d\x00\x00\x00" + b"\x00" * 64
        )


def test_read_binary_cookies_file_not_a_cookie_file(tmp_path):
    with patch("binary_cookies_parser.parser.binary_cookies_reader"):
        file_path = tmp_path / "Cookies.binarycookies"
        with open(file_path, "wb") as f:
            f.write(b"not a cookie file")

        with pytest.raises(SystemExit, match="Not a Cookies.binarycookies file"):
            read_binary_cookies_file(str(file_path))


def test_load(tmp_path):
    with patch("binary_cookies_parser.parser.binary_cookies_reader") as mock_binary_cookies_reader:
        file_path = tmp_path / "Cookies.binarycookies"
        with open(file_path, "wb") as f:
            f.write(b"cook")  # File Magic String
            f.write(b"\x00\x00\x00\x01")  # number of pages
            f.write(b"\x00\x00\x00\x4d")  # page size
            f.write(b"\x01\x00\x00\x00\x04\x00\x00\x00\x4d\x00\x00\x00" + b"\x00" * 65)

        load(str(file_path))
        mock_binary_cookies_reader.assert_called_with(ANY)
