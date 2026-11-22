from __future__ import print_function

import os

try:
    from winreg import OpenKey, HKEY_LOCAL_MACHINE, QueryValueEx
except ImportError:
    try:
        from _winreg import OpenKey, HKEY_LOCAL_MACHINE, QueryValueEx
    except ImportError:
        OpenKey = None
        HKEY_LOCAL_MACHINE = None
        QueryValueEx = None


def sid2user(sid, key_opener=None, value_querier=None):
    """Converts a Windows Security Identifier (SID) into an associated username.

    Complexity Analysis:
        - Input size variable: n = length of the resolved ProfileImagePath string.
        - Worst-case time complexity: O(n) due to string splitting across path separators.
        - Space complexity: O(n) to allocate path segments from the split operation.
        - Observed behavior: Performs 1 registry key open, 1 value query, and 1 string split.

    Preconditions (source citations from recyclebin.py baseline):
        - Line 20: Input is an SID string (e.g., 'S-1-5-...').
        - Line 21: Opens HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\ProfileList\\<sid>.
        - Line 25: Queries 'ProfileImagePath' value.
        - Line 26: Splits path on '\\' and takes the trailing element as the username.
        - Line 28: Fallback on exception returns original `sid`.
        - Line 32: Anchor dirs = ["c:\\Recycler\\", "C:\\Recycled\\", "C:\\$RECYCLE.BIN\\"].
    """
    opener = key_opener if key_opener is not None else OpenKey
    querier = value_querier if value_querier is not None else QueryValueEx

    try:
        if opener is None or querier is None:
            raise RuntimeError("Registry access not available on this platform")

        key = opener(
            HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList" + "\\" + sid,
        )
        (value, type_) = querier(key, "ProfileImagePath")
        user = value.split("\\")[-1]
        return user
    except Exception:
        return sid


def returnDir():
    dirs = ["c:\\Recycler\\", "C:\\Recycled\\", "C:\\$RECYCLE.BIN\\"]
    for recycleDir in dirs:
        if os.path.isdir(recycleDir):
            return recycleDir
    return None


def findRecycled(recycleDir):
    if not recycleDir or not os.path.isdir(recycleDir):
        return
    dirList = os.listdir(recycleDir)
    for sid in dirList:
        userPath = os.path.join(recycleDir, sid)
        if os.path.isdir(userPath):
            files = os.listdir(userPath)
            user = sid2user(sid)

            print("\n[*] Listing Files for User: " + str(user))
            for file in files:
                print("[+] Found File: " + str(file))


def main():
    recycleDir = returnDir()
    if recycleDir:
        findRecycled(recycleDir)


if __name__ == "__main__":
    main()
