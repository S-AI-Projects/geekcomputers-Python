# Author: PrajaktaSathe
# Program to calculate the area of - square, rectangle, circle, and triangle -
import math as m


def main(input_fn=None, print_fn=None):
    """Calculates geometric areas for various shapes based on interactive user selection.

    Documented Failure Branch:
        - Source line 32: If `shape` is outside the recognized range [1, 7], the `else:` branch
          triggers: prints 'You have selected wrong choice.' without performing any calculation.

    Preconditions (source citations from calc_area.py baseline):
        - Line 5: `shape = int(...)` expects selection integer.
        - Line 11: `shape == 1` computes square area (side**2).
        - Line 14: `shape == 2` computes rectangle area (l * b).
        - Line 18: `shape == 3` computes circle area (pi * r * r).
        - Line 32: `else: print("You have selected wrong choice.")` failure fallback branch.
        - Line 35: `restart = input(...)` prompt for recursion or exit.
    """
    _input = input_fn if input_fn is not None else input
    _print = print_fn if print_fn is not None else print

    shape = int(
        _input(
            "Enter 1 for square, 2 for rectangle, 3 for circle, 4 for triangle, 5 for cylinder, 6 for cone, or 7 for sphere: "
        )
    )
    if shape == 1:
        side = float(_input("Enter length of side: "))
        _print("Area of square = " + str(side**2))
    elif shape == 2:
        l = float(_input("Enter length: "))
        b = float(_input("Enter breadth: "))
        _print("Area of rectangle = " + str(l * b))
    elif shape == 3:
        r = float(_input("Enter radius: "))
        _print("Area of circle = " + str(m.pi * r * r))
    elif shape == 4:
        base = float(_input("Enter base: "))
        h = float(_input("Enter height: "))
        _print("Area of rectangle = " + str(0.5 * base * h))
    elif shape == 5:
        r = float(_input("Enter radius: "))
        h = float(_input("Enter height: "))
        _print("Area of cylinder = " + str(m.pow(r, 2) * h * m.pi))
    elif shape == 6:
        r = float(_input("Enter radius: "))
        h = float(_input("Enter height: "))
        _print("Area of cone = " + str(m.pow(r, 2) * h * 1 / 3 * m.pi))
    elif shape == 7:
        r = float(_input("Enter radius: "))
        _print("Area of sphere = " + str(m.pow(r, 3) * 4 / 3 * m.pi))
    else:
        _print("You have selected wrong choice.")

    restart = _input("Would you like to calculate the area of another object? Y/N : ")
    if restart.lower().startswith("y"):
        main(input_fn=_input, print_fn=_print)
    elif restart.lower().startswith("n"):
        return


if __name__ == "__main__":
    main()
