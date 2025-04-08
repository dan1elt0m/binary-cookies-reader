import json
from datetime import datetime
from enum import Enum
from sys import stdout
from typing import Type

import typer
from rich import print

from binarycookies import load


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj: Type) -> str:
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class OutputType(str, Enum):
    json = "json"
    ascii = "ascii"


def cli(file_path: str, output: str = "json"):
    """CLI entrypoint for reading Binary Cookies"""
    with open(file_path, "rb") as f:
        cookies = load(f)
    if output == OutputType.json:
        json.dump([cookie.model_dump() for cookie in cookies], indent=2, cls=DateTimeEncoder, fp=stdout)
    elif output == OutputType.ascii:
        for cookie in cookies:
            print(f"Name: {cookie.name}")
            print(f"Value: {cookie.value}")
            print(f"URL: {cookie.url}")
            print(f"Path: {cookie.path}")
            print(f"Created: {cookie.create_datetime.isoformat()}")
            print(f"Expires: {cookie.expiry_datetime.isoformat()}")
            print(f"Flag: {cookie.flag.value}")
            print("-" * 40)


def main():
    """CLI entrypoint for reading Binary Cookies"""
    typer.run(cli)


if __name__ == "__main__":
    main()
