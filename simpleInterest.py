"""Simple Interest Calculator.

Supported domain boundaries (derived from the original source):
  - principle (float): any numeric value convertible to float  [line 1]
  - time (int):        any numeric value convertible to int     [line 2]
  - rate (float):      any numeric value convertible to float   [line 3]
  - formula:           (principle * time * rate) / 100          [line 4]

The smallest valid inputs are zero for each parameter.
No rejection guards are added for behavior the source leaves undefined
(e.g., negative values produce mathematically correct negative interest).
"""


def simpleInterest(principle, time, rate):
    """Calculate simple interest.

    Args:
        principle: The principal amount (float-compatible numeric).
        time: The time period in years (int-compatible numeric).
        rate: The annual interest rate (float-compatible numeric).

    Returns:
        float: The simple interest = (principle * time * rate) / 100.

    Boundary contract (source line citations):
        - Line 1: principle is accepted as float.
        - Line 2: time is accepted as int.
        - Line 3: rate is accepted as float.
        - Line 4: formula (principle * time * rate) / 100.
    """
    return (principle * time * rate) / 100


if __name__ == "__main__":
    principle = float(input("Enter the principle amount:"))
    time = int(input("Enter the time(years):"))
    rate = float(input("Enter the rate:"))
    simple_interest = simpleInterest(principle, time, rate)
    print("The simple interest is:", simple_interest)
