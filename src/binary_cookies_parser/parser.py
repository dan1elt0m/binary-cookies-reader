from datetime import datetime, timezone
from io import BytesIO
from struct import unpack
from typing import List

from binary_cookies_parser.models import BcField, Cookie, CookieFields, FileFields, Flag, Format

FLAGS = {
    0: Flag.UNKNOWN,
    1: Flag.SECURE,
    4: Flag.HTTPONLY,
    5: Flag.SECURE_HTTPONLY,
}


def interpret_flag(flags: int) -> str:
    """Interprets the flags of a cookie and returns a human-readable string."""
    return FLAGS.get(flags, Flag.UNKNOWN)


def mac_epoch_to_date(epoch: int) -> datetime:
    """Converts a mac epoch time to a datetime object."""
    return datetime.fromtimestamp(epoch + 978307200, tz=timezone.utc)


def read_string(data: BytesIO, size: int) -> str:
    """Reads a string from binary file."""
    result = ""
    count = 0
    c = data.read(1)
    while unpack("<b", c)[0] != 0:
        count += 1
        if count > size:
            break
        result += str(c.decode())
        c = data.read(1)
    return result


def read_field(data: BytesIO, field: BcField) -> int:
    """Reads a field from binary data."""
    data.seek(field.offset)
    if field.format == Format.string:
        return read_string(data, field.size)
    return unpack(field.format, data.read(field.size))[0]


def read_cookie(cookie: BytesIO, cookie_size: int) -> Cookie:
    """Reads a cookie from the given offset in the page."""

    cookie_fields = CookieFields()
    flag = interpret_flag(read_field(cookie, cookie_fields.flag))

    url_offset = read_field(cookie, cookie_fields.url_offset)
    name_offset = read_field(cookie, cookie_fields.name_offset)
    path_offset = read_field(cookie, cookie_fields.path_offset)
    value_offset = read_field(cookie, cookie_fields.value_offset)

    expiry_datetime = mac_epoch_to_date(read_field(cookie, cookie_fields.expiry_date))
    create_datetime = mac_epoch_to_date(read_field(cookie, cookie_fields.create_date))

    url = read_field(cookie, BcField(offset=url_offset, size=name_offset - url_offset, format=Format.string))
    name = read_field(cookie, BcField(offset=name_offset, size=path_offset - name_offset, format=Format.string))
    path = read_field(cookie, BcField(offset=path_offset, size=value_offset - path_offset, format=Format.string))
    value = read_field(cookie, BcField(offset=value_offset, size=cookie_size - value_offset, format=Format.string))

    return Cookie(
        name=name,
        value=value,
        url=url,
        path=path,
        create_datetime=create_datetime,
        expiry_datetime=expiry_datetime,
        flag=flag,
    )


def get_cookie_offsets(page: BytesIO, num_cookies: int) -> List[int]:
    """Reads the offsets of the cookies in the page."""
    return [read_field(page, BcField(offset=8 + (4 * i), size=4, format=Format.integer)) for i in range(num_cookies)]


def get_file_pages(binary_file: BytesIO, num_pages: int) -> List[int]:
    return [
        read_field(binary_file, BcField(offset=8 + (i * 4), size=4, format=Format.integer_be)) for i in range(num_pages)
    ]


def binary_cookies_reader(page: BytesIO) -> List[Cookie]:
    """Reads a binary cookie file and returns a list of cookies."""
    num_cookies = read_field(page, BcField(offset=4, size=4, format=Format.integer))
    cookie_offsets = get_cookie_offsets(page, num_cookies)
    cookies = []
    for offset in cookie_offsets:
        cookie_size = read_field(page, BcField(offset=offset, size=4, format=Format.integer))
        page.seek(offset)
        cookie = page.read(cookie_size)
        cookies.append(read_cookie(BytesIO(cookie), cookie_size))
    return cookies


def read_binary_cookies_file(file_path: str) -> List[Cookie]:
    """Reads a binary cookie file and returns a list of cookies."""
    all_cookies = []
    with open(file_path, "rb") as binary_file:
        data: BytesIO = BytesIO(binary_file.read())
        file_fields = FileFields()
        file_header = read_field(data, field=file_fields.header)  # File Magic String:cook

        if str(file_header) != "cook":
            raise SystemExit("Not a Cookies.binarycookies file")

        # Number of pages in the binary file: 4 bytes
        num_pages = read_field(data, field=file_fields.num_pages)
        page_sizes = get_file_pages(data, num_pages)

        pages = []
        data.seek(8 + (num_pages * 4))
        for ps in page_sizes:
            # Grab individual pages and each page will contain >= one cookie
            pages.append(data.read(ps))

        for page in pages:
            cookies = binary_cookies_reader(BytesIO(page))
            all_cookies.extend(cookies)

    return all_cookies
