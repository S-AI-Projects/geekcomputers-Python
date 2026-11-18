# patch-1
# import os
# The OS module in python provides functions for interacting with the operating system

# patch-3
# function to check if 'binod' is present in the file.
# def checkBinod(file):
# =======

# def checkBinod(file):       #this function will check there is any 'Binod' text in file or not
#     with open(file, "r") as f: #we are opening file in read mode and using 'with' so need to take care of close()
# =======
import time
import os

# Importing our Bindoer
print("To Kaise Hai Ap Log!")
time.sleep(1)
print("Chaliye Binod Karte Hai!")


def checkBinod(file):  # Trying to find Binod In File Insted Of Manohar Ka Kotha
    """Check if the keyword 'binod' (case-insensitive) is present in the specified file.

    Contract & Preconditions:
        - Precondition Source Line 38: `with open(file, "r") as f:` requires readable file path.
        - Precondition Source Line 40: `fileContent = f.read()` reads file as text.
        - Precondition Source Line 42: `has_binod = "binod" in fileContent.lower()` checks case-insensitively.
        - Precondition Source Line 44: prints congratulatory message if found.

    Returns:
        bool: True if 'binod' is in file, False otherwise.
    """
    with open(file, "r") as f:
        fileContent = f.read()

    # Responsibility simplified: extract explicit boolean flag for keyword detection
    has_binod = "binod" in fileContent.lower()
    if has_binod:
        print(f"**************Congratulations Binod found in {f}********************")
        return True
    return False


if __name__ == "__main__":
    print("************binod Detector********************")
    dir_contents = os.listdir()
    for item in dir_contents:
        if item.endswith("txt"):
            ans = checkBinod(item)
            if ans is False:
                print("Binod not found Try Looking In Manohar Ka Kotha!!")
