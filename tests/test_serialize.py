from datetime import datetime, timezone

from binary_cookies_parser import dump, load


def test_dump(tmp_path):
    data = [
        {
            "name": "name",
            "value": "value",
            "url": "example.com",
            "path": "/",
            "flag": "Secure",
            "create_datetime": "2032-01-02T00:00:00Z",
            "expiry_datetime": "2032-01-02T00:00:00Z",
        }
    ]

    # Define the file path
    file_path = tmp_path / "Cookies.binarycookies"

    # Call the dump method
    dump(data, str(file_path))

    # Read the file back and verify its contents
    cookies = load(str(file_path))
    assert len(cookies) == 1
    cookie = cookies[0]
    assert cookie.name == "name"
    assert cookie.value == "value"
    assert cookie.url == "example.com"
    assert cookie.path == "/"
    assert cookie.flag == "Secure"
    assert cookie.create_datetime == datetime(2032, 1, 2, 0, 0, tzinfo=timezone.utc)
    assert cookie.expiry_datetime == datetime(2032, 1, 2, 0, 0, tzinfo=timezone.utc)


def test_dump_multiple_cookies(tmp_path):
    data = [
        {
            "name": "name1",
            "value": "value1",
            "url": "example1.com",
            "path": "/",
            "flag": "Secure",
            "create_datetime": "2032-01-02T00:00:00Z",
            "expiry_datetime": "2032-01-02T00:00:00Z",
        },
        {
            "name": "name2",
            "value": "value2",
            "url": "example2.com",
            "path": "/",
            "flag": "HttpOnly",
            "create_datetime": "2033-01-02T00:00:00Z",
            "expiry_datetime": "2033-01-02T00:00:00Z",
        },
    ]

    # Define the file path
    file_path = tmp_path / "Cookies.binarycookies"

    # Call the dump method
    dump(data, str(file_path))

    # Read the file back and verify its contents
    cookies = load(str(file_path))
    assert len(cookies) == 2

    cookie1 = cookies[0]
    assert cookie1.name == "name1"
    assert cookie1.value == "value1"
    assert cookie1.url == "example1.com"
    assert cookie1.path == "/"
    assert cookie1.flag == "Secure"
    assert cookie1.create_datetime == datetime(2032, 1, 2, 0, 0, tzinfo=timezone.utc)
    assert cookie1.expiry_datetime == datetime(2032, 1, 2, 0, 0, tzinfo=timezone.utc)

    cookie2 = cookies[1]
    assert cookie2.name == "name2"
    assert cookie2.value == "value2"
    assert cookie2.url == "example2.com"
    assert cookie2.path == "/"
    assert cookie2.flag == "HttpOnly"
    assert cookie2.create_datetime == datetime(2033, 1, 2, 0, 0, tzinfo=timezone.utc)
    assert cookie2.expiry_datetime == datetime(2033, 1, 2, 0, 0, tzinfo=timezone.utc)
