# T053 — Cross-check change_background

## Source inspected

File: `Pomodoro (tkinter).py`

- Lines 11–17: Define five supported background color names and their hex values.
- Line 30: Defines `change_background(*args)`.
- Line 31: Reads the selected color from `bg_color_var.get()`.
- Line 32: Uses `bg_colors.get(selected, PINK)`, establishing the pink fallback.
- Lines 33–38: Applies the chosen color to six widgets.
- Lines 170–244: Build the Tkinter interface and call `window.mainloop()`.

## Observed behavior

- The function returns `None`.
- It reads the selection from the global `bg_color_var`.
- It applies the same background color to window, canvas, label, tick_label, work_label and break_label.
- Unknown selections use the PINK fallback.
- The function does not modify `bg_colors`.
- The function accepts arbitrary callback arguments through `*args` and does not use them.

## Independent expected-result table

| Selection | Expected result |
|---|---|
| Pink | #e2979c |
| Green | #9bdeac |
| Blue | #1f75fe |
| Yellow | #ffcc00 |
| Purple | #b19cd9 |
| Unknown | #e2979c |

Expected values are independently copied from the source fixture and fallback contract.

## Test coverage

1. All five supported color selections.
2. Unknown selection fallback.
3. Twenty distinct callback argument combinations while the selected color is Blue.
4. Six widget configuration calls per test case.
5. Return value is None.
6. The original color dictionary remains unchanged.

Tkinter is mocked because the source creates a window and calls mainloop at import time.

## Test execution

Command:

`python3 work/R25-T053/check.py`

Result: 3 test groups passed.

## Tool versions

- Python: 3.12.16
- requests: 2.34.2
- pytest: 9.2.0

## Implementation changes

No changes were made to `Pomodoro (tkinter).py`.