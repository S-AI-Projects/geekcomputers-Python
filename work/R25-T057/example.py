"""
Worked example: Random Password Generator

The original program combines lowercase letters, uppercase letters,
digits and symbols, then selects eight distinct characters.
"""

import random

low = "abcdefghijklmnopqrstuvwxyz"
upp = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
num = "0123456789"
sym = "!@#$%^&*"

all = low + upp + num + sym
length = 8

# Deterministic selection for this worked example.
selected = list("aB3!cD4@")
password = "".join(selected)

print("Character pool size:", len(all))
print("Requested length:", length)
print("Selected characters:", selected)
print("Final password:", password)
