from sys import argv


def print_all(f):
    """
    Read and print the entire contents of a file-like object to stdout.

    Contract:
      Preconditions:
        - Line 6: `f` must be a readable stream supporting `.read()` and `.tell()`.
        - Line 7: `print(f.read())` reads remaining stream content to EOF and prints with newline.
      Representative Result:
        - Input: StringIO("Hello World")
        - Output printed: "Hello World\\n"
        - Stream mutation: stream position advances from 0 to EOF (position 11).
    """
    print(f.read())


# seek(n) to read a file's content from byte-n
def rewind(f):
    """Rewind the file pointer to the beginning (byte 0)."""
    f.seek(0)


def print_a_line(line_count, f):
    """Print the 1-based line number followed by the next line read from the file."""
    print(line_count, f.readline())


def main():
    if len(argv) < 2:
        print("Usage: python ex20.py <input_file>")
        return
    input_file = argv[1]
    current_file = open(input_file)

    print("First let's print the whole file:\n")
    print_all(current_file)

    print("Now let's rewind, kind of like a tape.")
    rewind(current_file)

    print("Let's print three lines:")
    current_line = 1
    print_a_line(current_line, current_file)

    current_line = current_line + 1
    print_a_line(current_line, current_file)

    current_line = current_line + 1
    print_a_line(current_line, current_file)

    current_file.close()


if __name__ == "__main__":
    main()
