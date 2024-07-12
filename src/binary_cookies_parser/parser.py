from datetime import datetime
from io import BytesIO
from struct import unpack
from typing import List

from binary_cookies_parser.models import Cookie, Flag

FLAGS = {
    0: "",
    1: Flag.SECURE,
    4: Flag.HTTPONLY,
    5: Flag.SECURE_HTTPONLY,
}


def interpret_flag(flags: int) -> str:
    """Interprets the flags of a cookie and returns a human-readable string."""
    return FLAGS.get(flags, Flag.UNKNOWN)


def mac_epoch_to_date(epoch: int) -> datetime:
    """Converts a mac epoch time to a datetime object."""
    return datetime.fromtimestamp(epoch + 978307200)


def read_next_string(cookie: BytesIO, offset: int) -> str:
    """Reads a string from the given offset in the cookie."""
    result = ""
    cookie.seek(offset - 4)
    c = cookie.read(1)
    while unpack("<b", c)[0] != 0:
        result += str(c.decode())
        c = cookie.read(1)
    return result


def read_next_int(cookie: BytesIO) -> int:
    return unpack("<i", cookie.read(4))[0]


def read_next_date(cookie: BytesIO) -> int:
    return unpack("<d", cookie.read(8))[0]


def read_cookie(page: BytesIO, offset: int) -> Cookie:
    """Reads a cookie from the given offset in the page."""
    page.seek(offset)
    cookiesize = read_next_int(page)
    cookie = BytesIO(page.read(cookiesize))

    cookie.read(4)  # unknown
    flag = interpret_flag(read_next_int(cookie))
    cookie.read(4)  # unknown

    urloffset = read_next_int(cookie)
    nameoffset = read_next_int(cookie)
    pathoffset = read_next_int(cookie)
    valueoffset = read_next_int(cookie)

    cookie.read(8)

    expiry_datetime = mac_epoch_to_date(read_next_date(cookie))
    create_datetime = mac_epoch_to_date(read_next_date(cookie))

    url = read_next_string(cookie, urloffset)
    name = read_next_string(cookie, nameoffset)
    path = read_next_string(cookie, pathoffset)
    value = read_next_string(cookie, valueoffset)

    return Cookie(
        name=name,
        value=value,
        url=url,
        path=path,
        create_datetime=create_datetime,
        expiry_datetime=expiry_datetime,
        flag=flag,
    )


def binary_cookies_reader(page: bytes) -> List[Cookie]:
    """Reads a binary cookie file and returns a list of cookies."""
    page = BytesIO(page)
    page.read(4)
    num_cookies = read_next_int(page)

    cookie_offsets = [unpack("<i", page.read(4))[0] for _ in range(num_cookies)]
    page.read(4)

    return [read_cookie(page, offset) for offset in cookie_offsets]


def read_binary_cookies_file(file_path: str) -> List[Cookie]:
    """Reads a binary cookie file and returns a list of cookies."""
    all_cookies = []
    with open(file_path, "rb") as binary_file:
        file_header = binary_file.read(4).decode()  # File Magic String:cook

        if str(file_header) != "cook":
            raise SystemExit("Not a Cookies.binarycookies file")

        # Number of pages in the binary file: 4 bytes
        num_pages = unpack(">i", binary_file.read(4))[0]

        page_sizes = []
        for np in range(num_pages):
            # Each page size: 4 bytes*number of pages
            page_sizes.append(unpack(">i", binary_file.read(4))[0])

        pages = []
        for ps in page_sizes:
            # Grab individual pages and each page will contain >= one cookie
            pages.append(binary_file.read(ps))

        for page in pages:
            cookies = binary_cookies_reader(page)
            all_cookies.extend(cookies)

    return all_cookies
