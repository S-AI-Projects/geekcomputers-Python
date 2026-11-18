# Script Name		: pscheck.py
# Author				: Craig Richards
# Created				: 19th December 2011
# Last Modified		: 17th June 2013
# Version				: 1.1

# Modifications		: 1.1 - 17/06/13 - CR - Changed to functions, and check os before running the program

# Description			: Process check on Nix boxes, diplsay formatted output from ps command

import os
import string

try:
    import commands
except ImportError:
    import subprocess as commands

if not hasattr(string, "split"):
    string.split = str.split

try:
    input = raw_input
except NameError:
    pass


def ps():
    """Check a running process on POSIX systems and display formatted process info.

    Preconditions:
      - Line 41 (input): User input provides process query string (program name).
      - Line 45 (getoutput): Shell execution (commands.getoutput) yields space-delimited ps line.
      - Line 46 (split): Whitespace split generates field list 'proginfo' with >= 6 tokens.
      - Lines 49-65 (format): Positional field mappings (Owner=0, PID=1, PPID=2, Time=4, Path=5).
      - Line 66 (except): Failure boundary catches exceptions (e.g. IndexError on < 6 tokens).

    Protected condition:
      - Field indexing and positional mapping integrity across stdout formatting.
    """
    program = input("Enter the name of the program to check: ")

    try:
        # perform a ps command and assign results to a list
        output = commands.getoutput("ps -f|grep " + program)
        proginfo = string.split(output)

        # display results
        print(
            "\n\
    Full path:\t\t",
            proginfo[5],
            "\n\
    Owner:\t\t\t",
            proginfo[0],
            "\n\
    Process ID:\t\t",
            proginfo[1],
            "\n\
    Parent process ID:\t",
            proginfo[2],
            "\n\
    Time started:\t\t",
            proginfo[4],
        )
    except:
        print("There was a problem with the program.")


def main():
    if os.name == "posix":  # Unix/Linux/MacOS/BSD/etc
        ps()  # Call the function
    elif os.name in ("nt", "dos", "ce"):  # if the OS is windows
        print("You need to be on Linux or Unix to run this")


if __name__ == "__main__":
    main()
