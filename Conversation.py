# imports modules
import sys
import time
from getpass import getuser


def conversation(input_fn=input, print_fn=print, sleep_fn=time.sleep, exit_fn=sys.exit, default_user=None):
    """
    Run interactive conversation dialogue.

    Failure-Path Contract:
      Preconditions:
        - Line 8: `name = getuser()` retrieves default local username.
        - Line 9: `name_check = input(...)` prompts for name confirmation.
        - Line 23: `response = input(...)` prompts for friendly response.
        - Line 31: `else:` branch handles unexpected responses (not starting with 'y' or 'n').
                   Outputs error message and invokes exit handler.
        - Line 41: Second `else:` branch handles invalid robot justification responses.
    """
    name = default_user if default_user is not None else getuser()
    name_check = input_fn("Is your name " + name + "? → ")
    if name_check.lower().startswith("y"):
        print_fn("Okay.")
        sleep_fn(1)

    if name_check.lower().startswith("n"):
        name = input_fn("Then what is it? → ")

    userList = name

    print_fn("Hello", name + ", my name is Python.")
    sleep_fn(0.8)
    first_letter = userList[0] if userList else "?"
    print_fn("The first letter of your name is", first_letter + ".")
    sleep_fn(0.8)
    print_fn("Nice to meet you. :)")
    sleep_fn(0.8)
    response = input_fn("Would you say it's nice to meet me? → ")

    if response.lower().startswith("y"):
        print_fn("Nice :)")
        exit_fn(0)
        return "nice"

    elif response.lower().startswith("n"):
        response2 = input_fn("Is it because I am a robot? → ")
    else:
        print_fn("You may have made an input error. Please restart and try again.")
        exit_fn(1)
        return "input_error_1"

    if response2.lower().startswith("y"):
        print_fn("Aw :(")
        return "robot_sad"

    elif response2.lower().startswith("n"):
        response3 = input_fn("Then why? → ")
        sleep_fn(1)
        print_fn("Oh.")
        return "why_explained"

    else:
        print_fn("You may have made an input error. Please restart and try again.")
        exit_fn(1)
        return "input_error_2"


def main():
    conversation()


if __name__ == "__main__":
    main()
