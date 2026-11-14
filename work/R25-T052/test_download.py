import builtins
import contextlib
import io
import runpy
from unittest.mock import mock_open, patch

import requests


def run_download(url, filename, chunks):
    output = io.StringIO()
    fake_file = mock_open()

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def raise_for_status(self):
            pass

        def iter_content(self, chunk_size):
            assert chunk_size == 8192
            return iter(chunks)

    with (
        patch("requests.get", return_value=FakeResponse()),
        patch.object(builtins, "open", fake_file),
        contextlib.redirect_stdout(output),
    ):
        namespace = runpy.run_path("scrap_file.py")

        # Ignore writes from the example download at the bottom of scrap_file.py
        fake_file.return_value.write.reset_mock()

        result = namespace["download"](url, filename)
        fake_file.assert_called_with(filename, "wb")

    written = b"".join(
    call.args[0]
    for call in fake_file.return_value.write.call_args_list
    )
    return result, written, output.getvalue()


def test_smallest_nonempty_download():
    result, written, _ = run_download(
        "https://example.test/a",
        "a",
        [b"x"],
    )
    assert result is None
    assert written == b"x"


def test_ordinary_download_skips_empty_chunks():
    result, written, _ = run_download(
        "https://example.test/files/report.bin",
        "report.bin",
        [b"hello ", b"", b"world"],
    )
    assert result is None
    assert written == b"hello world"


def test_empty_response_creates_empty_file():
    result, written, _ = run_download(
        "https://example.test/empty",
        "empty.bin",
        [],
    )
    assert result is None
    assert written == b""

def test_request_error_is_handled():
    output = io.StringIO()

    with (
        patch(
            "requests.get",
            side_effect=requests.exceptions.ConnectionError("test error"),
        ),
        contextlib.redirect_stdout(output),
    ):
        namespace = runpy.run_path("scrap_file.py")

    assert "Download failed:" in output.getvalue()

if __name__ == "__main__":
    test_smallest_nonempty_download()
    test_ordinary_download_skips_empty_chunks()
    test_empty_response_creates_empty_file()
    print("All 3 download tests passed!")