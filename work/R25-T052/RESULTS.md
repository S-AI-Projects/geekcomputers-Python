# T052 — Download Boundary Tests

## Source inspected

File: `scrap_file.py`

- Line 9: `download(url, filename)` defines the function inputs.
- Line 11: Sends the URL using `requests.get` with streaming enabled and a 10-second timeout.
- Line 12: Raises an exception for unsuccessful HTTP responses.
- Line 14: Opens the destination filename in binary write mode.
- Lines 15–17: Iterates over response chunks and writes only non-empty chunks.
- Lines 21–22: Catches `requests.exceptions.RequestException` and prints a failure message.
- Lines 26–27: The module calls `download()` at top level when executed or imported.

## Observed behavior

The function has no explicit return statement, so successful downloads return `None`.

The source defines a chunk boundary:
- Empty chunks (`b""`) are skipped.
- Non-empty chunks are written to the file.

The destination file is opened even if the response contains no chunks.

The source does not define URL or filename validation rules. No additional rejection rules have been introduced.

## Boundary test table

| Input case | Expected behavior | Test |
|---|---|---|
| One non-empty chunk: `b"x"` | Writes `b"x"` | `test_smallest_nonempty_download` |
| Multiple chunks including `b""` | Skips the empty chunk and writes the others | `test_ordinary_download_skips_empty_chunks` |
| No response chunks | Creates or opens an empty file and writes no bytes | `test_empty_response_creates_empty_file` |
| Connection error | Prints a download failure message; does not propagate the request exception | `test_request_error_is_handled` |

## Test execution

Command:

`python3 work/R25-T052/check.py`

Result: 4 tests passed.

Network requests and file operations were mocked during testing.

## Tool versions

- Python: 3.12.16
- requests: 2.34.2
- pytest: 9.2.0

## Implementation changes

No changes were made to the original `scrap_file.py`.