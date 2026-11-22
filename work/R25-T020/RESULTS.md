# Verification Evidence — R25-T020

## Target
- **Script:** date-timeclient.py
- **Function:** `date_timeclient`
- **Python Version:** 3.14.7
- **Command:** `/Library/Frameworks/Python.framework/Versions/3.14/bin/python3 -m unittest /Users/nevilmaru009/.gemini/antigravity/scratch/geekcomputers-Python/work/R25-T020/test_datetimeclient.py -v`

## Precondition Citations
- Line 3: `soc = socket.socket(...)` socket initialization.
- Line 4: `soc.connect((..., 2905))` connects to destination port 2905.
- Line 5: `recmsg = soc.recv(1024)` reads up to 1024 bytes.
- Line 6: `soc.close()` socket teardown.
- Line 7: `"The time got from the server is %s" % recmsg.decode("ascii")` formatting normalization.

## Mutation Analysis
- **Mutant 1 (Off-by-one port):** Connecting to port 2906 instead of 2905. Proven caught by `mock_soc.connect.assert_called_once_with((host, 2905))`.
- **Mutant 2 (Altered format prefix):** String modified to `"Time got from server is %s"`. Proven caught by strict return assertion.
- **Mutant 3 (Altered buffer size):** Changing `recv(1024)` to `recv(512)`. Proven caught by `mock_soc.recv.assert_called_once_with(1024)`.
- **Production Cleanliness:** The final implementation in `date-timeclient.py` contains zero mutant code or test hooks.

## Test Results
| Scenario | Preconditions | Literal Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|---|
| Smallest valid input (empty) | L5, L7 | Payload `b""` | `"The time got from the server is "` | Matches expected | PASS |
| Ordinary input | L4, L5, L7 | `b"2026-11-23 00:00:00"` | Formatted string with ISO timestamp | Matches expected | PASS |
| Mutant 1: Port 2906 | L4 | Connect to 2906 | Fails port assertion | Caught by test | PASS |
| Mutant 2: Altered prefix | L7 | Changed string template | Fails string equality | Caught by test | PASS |
| Mutant 3: Buffer 512 | L5 | `recv(512)` | Fails buffer assertion | Caught by test | PASS |

## Test Runner Output
```
test_mutation_resistance_altered_format_string (work.R25-T020.test_datetimeclient.TestDateTimeClientMutationResistance.test_mutation_resistance_altered_format_string)
Mutation resistance: catch plausible one-line bug altering format prefix. ... ok
test_mutation_resistance_wrong_buffer_size (work.R25-T020.test_datetimeclient.TestDateTimeClientMutationResistance.test_mutation_resistance_wrong_buffer_size)
Mutation resistance: catch plausible one-line bug changing recv buffer from 1024 to 512. ... ok
test_mutation_resistance_wrong_port (work.R25-T020.test_datetimeclient.TestDateTimeClientMutationResistance.test_mutation_resistance_wrong_port)
Mutation resistance: catch plausible one-line mutation altering default port to 2906. ... ok
test_ordinary_input_datetime_string (work.R25-T020.test_datetimeclient.TestDateTimeClientMutationResistance.test_ordinary_input_datetime_string)
Ordinary input: timestamp payload "2026-11-23 00:00:00". ... ok
test_smallest_valid_input_empty_payload (work.R25-T020.test_datetimeclient.TestDateTimeClientMutationResistance.test_smallest_valid_input_empty_payload)
Smallest valid input: empty byte stream b"". ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.001s

OK
```

**Exit Code:** 0
