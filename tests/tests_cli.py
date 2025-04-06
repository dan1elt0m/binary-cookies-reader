import json

from binary_cookies_parser import dump
from binary_cookies_parser.__main__ import cli


def test_cli_json_output(tmp_path, capsys):
    file_path = tmp_path / "Cookies.binarycookies"
    with open(file_path, "wb") as f:
        f.write(b"cook")  # File Magic String
        f.write(b"\x00\x00\x00\x01")  # number of pages
        f.write(b"\x00\x00\x00\x4d")  # page size
        f.write(b"\x01\x00\x00\x00\x04\x00\x00\x00\x4d\x00\x00\x00" + b"\x00" * 65)
    cli(str(file_path), output="json")
    captured = capsys.readouterr()
    output = json.loads(captured)
    assert isinstance(output, list)
    assert len(output) > 0
    assert "name" in output[0]
    assert "value" in output[0]
    assert "url" in output[0]
    assert "path" in output[0]
    assert "create_datetime" in output[0]
    assert "expiry_datetime" in output[0]
    assert "flag" in output[0]


def test_cli_ascii_output(tmp_path, capsys):
    file_path = tmp_path / "Cookies.binarycookies"
    data = {
        "name": "name",
        "value": "value",
        "url": "example.com",
        "path": "/",
        "create_datetime": 2032,
        "expiry_datetime": 2032,
        "flag": "Secure",
    }
    dump(data, str(file_path))
    cli(str(file_path), output="ascii")
    output = capsys.readouterr().out

    assert "Name:" in output
    assert "Value:" in output
    assert "URL:" in output
    assert "Path:" in output
    assert "Created:" in output
    assert "Expires:" in output
    assert "Flag:" in output
    assert "-" * 40 in output
    assert "Flag.SECURE" not in output
    assert "Secure" in output
