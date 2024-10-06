import json
from datetime import datetime
from enum import Enum
from typing import Type

import typer
from rich import print

from binary_cookies_parser.parser import read_binary_cookies_file


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj: Type) -> str:
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class OutputType(str, Enum):
    json = "json"
    ascii = "ascii"


def cli(file_path: str, output: OutputType = "json"):
    cookies = read_binary_cookies_file(file_path)
    if output == OutputType.json:
        print(json.dumps([cookie.model_dump() for cookie in cookies], indent=2, cls=DateTimeEncoder))
    elif output == OutputType.ascii:
        for cookie in cookies:
            print(f"Name: {cookie.name}")
            print(f"Value: {cookie.value}")
            print(f"URL: {cookie.url}")
            print(f"Path: {cookie.path}")
            print(f"Created: {cookie.create_datetime.isoformat()}")
            print(f"Expires: {cookie.expiry_datetime.isoformat()}")
            print(f"Flag: {cookie.flag}")
            print("-" * 40)


def main():
    """CLI entrypoint for reading binarycookies files"""
    typer.run(cli)


if __name__ == "__main__":
    main()
