import test_background


def main():
    tests = [
        test_background.test_all_supported_colors,
        test_background.test_unknown_color_uses_pink_fallback,
        test_background.test_twenty_argument_combinations,
    ]

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print(f"\nAll {len(tests)} background test groups passed!")


if __name__ == "__main__":
    main()