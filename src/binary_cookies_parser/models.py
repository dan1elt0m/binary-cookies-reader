from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class Flag(str, Enum):
    SECURE = "Secure"
    HTTPONLY = "HttpOnly"
    UNKNOWN = "Unknown"
    SECURE_HTTPONLY = "Secure; HttpOnly"


class Cookie(BaseModel):
    name: str
    value: str
    url: str
    path: str
    create_datetime: datetime
    expiry_datetime: datetime
    flag: Flag


class Format(str, Enum):
    integer = "<i"  # Integer format is a 4 byte integer
    integer_be = ">i"  # Integer format is a 4 byte integer big endian
    string = "<b"  # String format is a byte
    date = "<d"  # Date format is a double (epoch mac)


class BcField(BaseModel):
    offset: int
    size: int
    format: Format


class CookieFields(BaseModel):
    flag: BcField = BcField(offset=8, size=4, format=Format.integer)
    url_offset: BcField = BcField(offset=16, size=4, format=Format.integer)
    name_offset: BcField = BcField(offset=20, size=4, format=Format.integer)
    path_offset: BcField = BcField(offset=24, size=4, format=Format.integer)
    value_offset: BcField = BcField(offset=28, size=4, format=Format.integer)
    expiry_date: BcField = BcField(offset=32, size=8, format=Format.date)
    create_date: BcField = BcField(offset=40, size=8, format=Format.date)


class FileFields(BaseModel):
    header: BcField = BcField(offset=0, size=4, format=Format.string)
    num_pages: BcField = BcField(offset=4, size=4, format=Format.integer_be)
