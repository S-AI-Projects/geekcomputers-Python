import os
import argparse


def generate_unique_name(directory: str, name: str) -> str:
    """Generate a unique name for a file or folder in the specified directory.

    Contract & Preconditions:
        - Precondition Source Line 46: `base_name, extension = os.path.splitext(name)`
          splits name into stem and suffix.
        - Precondition Source Line 47: `index = 1` starts suffix indexing at 1.
        - Precondition Source Line 48: `while os.path.exists(...)` queries filesystem for collision.
        - Precondition Source Line 49: `index += 1` increments on collision.
        - Precondition Source Line 50: Returns first non-colliding formatted filename.

    Decisive State Transition:
        The loop guard `os.path.exists(os.path.join(directory, f"{base_name}_{index}{extension}"))`
        is the decisive transition: while True, `index` advances; the moment it evaluates to
        False (free filename slot detected), iteration halts and the unique name is returned.

    Worked Example:
        >>> import os, tempfile
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     # Simulate pre-existing files causing index collision:
        ...     open(os.path.join(tmpdir, "report_1.txt"), "w").close()
        ...     open(os.path.join(tmpdir, "report_2.txt"), "w").close()
        ...     # Execution trace:
        ...     # - index=1: "report_1.txt" exists (collision -> index=2)
        ...     # - index=2: "report_2.txt" exists (collision -> index=3)
        ...     # - index=3: "report_3.txt" does not exist (decisive exit)
        ...     generate_unique_name(tmpdir, "report.txt")
        'report_3.txt'

    Parameters:
    ----------
    directory : str
        The path to the directory.
    name : str
        The name of the file or folder.

    Returns:
    -------
    str
        The unique name with an index.
    """
    base_name, extension = os.path.splitext(name)
    index = 1
    while os.path.exists(os.path.join(directory, f"{base_name}_{index}{extension}")):
        index += 1
    return f"{base_name}_{index}{extension}"


def rename_files_and_folders(directory: str) -> None:
    """
    Rename files and folders in the specified directory to lowercase with underscores.

    Parameters:
    ----------
    directory : str
        The path to the directory containing the files and folders to be renamed.

    Returns:
    -------
    None
    """
    if not os.path.isdir(directory):
        raise ValueError("Invalid directory path.")

    for name in os.listdir(directory):
        old_path = os.path.join(directory, name)
        new_name = name.lower().replace(" ", "_")
        new_path = os.path.join(directory, new_name)

        # Check if the new filename is different from the old filename
        if new_name != name:
            # Check if the new filename already exists in the directory
            if os.path.exists(new_path):
                # If the new filename exists, generate a unique name with an index
                new_path = generate_unique_name(directory, new_name)

            os.rename(old_path, new_path)


def main() -> None:
    """
    Main function to handle command-line arguments and call the renaming function.

    Usage:
    ------
    python script_name.py <directory_path>

    Example:
    --------
    python rename_files_script.py /path/to/directory

    """
    # Create a parser for command-line arguments
    parser = argparse.ArgumentParser(
        description="Rename files and folders to lowercase with underscores."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="Path to the directory containing the files and folders to be renamed.",
    )
    args = parser.parse_args()

    # Call the rename_files_and_folders function with the provided directory path
    rename_files_and_folders(args.directory)


if __name__ == "__main__":
    main()
