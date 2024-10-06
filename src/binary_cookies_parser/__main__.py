import typer
from rich import print

from binary_cookies_parser.parser import read_binary_cookies_file


def cli(file_path: str):
    cookies = read_binary_cookies_file(file_path)
    [print(cookie.json()) for cookie in cookies]


def main():
    """CLI entrypoint for reading binarycookies files"""
    typer.run(cli)


if __name__ == "__main__":
    main()
