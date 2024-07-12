import typer
from binary_cookies_reader.reader import read_binary_cookies_file
from rich import print


def cli(file_path: str):
    cookies = read_binary_cookies_file(file_path)
    [print(cookie.json()) for cookie in cookies]


def main():
    """CLI entrypoint for reading binarycookies files"""
    typer.run(cli)


if __name__ == "__main__":
    typer.run(main)
