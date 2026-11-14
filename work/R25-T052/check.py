import test_download


def main():
    tests = [
        test_download.test_smallest_nonempty_download,
        test_download.test_ordinary_download_skips_empty_chunks,
        test_download.test_empty_response_creates_empty_file,
        test_download.test_request_error_is_handled,
    ]

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print(f"\nAll {len(tests)} download tests passed!")


if __name__ == "__main__":
    main()