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
