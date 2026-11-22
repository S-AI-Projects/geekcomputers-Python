"""Focused failure-path coverage tests for conversation in Conversation.py.

Precondition citations:
    - Line 8: `name = getuser()` default identity anchor.
    - Line 9: `name_check = input(...)` confirmation check.
    - Line 23: `response = input(...)` greeting response.
    - Line 31-33: Line 31 `else:` branch handles unexpected response (input error fallback).
    - Line 41-43: Line 41 `else:` branch handles second input error fallback.
"""

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import Conversation as conv


class TestConversationFailurePath(unittest.TestCase):
    """Tests verifying failure branches, error messages, and caller recovery."""

    def test_smallest_input_reaching_failure_branch_line_31(self):
        """Smallest invalid input: empty string '' reaching Line 31 error fallback.
        
        Preconditions:
            - Line 9: name_check = 'y'
            - Line 23: response = '' (empty string)
            - Line 31: ''.lower().startswith('y') is False, ''.lower().startswith('n') is False
        Literal input:
            inputs = ['y', '']
        Independently calculated expected output:
            Prints "You may have made an input error. Please restart and try again."
            Calls exit handler with code 1.
        """
        inputs = iter(["y", ""])
        printed = []
        exits = []

        ret = conv.conversation(
            input_fn=lambda prompt: next(inputs),
            print_fn=lambda *args: printed.append(" ".join(str(a) for a in args)),
            sleep_fn=lambda t: None,
            exit_fn=lambda code: exits.append(code),
            default_user="Alice"
        )

        self.assertEqual(ret, "input_error_1")
        self.assertEqual(exits, [1])
        self.assertIn("You may have made an input error. Please restart and try again.", printed)

    def test_ordinary_valid_call_line_26(self):
        """Ordinary valid input: 'y' to name check and 'y' to meeting response.
        
        Preconditions:
            - Line 9: name_check starts with 'y'
            - Line 23: response starts with 'y'
            - Line 26: prints 'Nice :)' and exits 0
        Literal input:
            inputs = ['yes', 'yes']
        Independently calculated expected output:
            Prints 'Nice :)' and exit_code == 0
        """
        inputs = iter(["yes", "yes"])
        printed = []
        exits = []

        ret = conv.conversation(
            input_fn=lambda prompt: next(inputs),
            print_fn=lambda *args: printed.append(" ".join(str(a) for a in args)),
            sleep_fn=lambda t: None,
            exit_fn=lambda code: exits.append(code),
            default_user="Bob"
        )

        self.assertEqual(ret, "nice")
        self.assertEqual(exits, [0])
        self.assertIn("Nice :)", printed)

    def test_caller_recovery_success_after_failure(self):
        """Verify that caller state is clean and an ordinary valid call succeeds immediately after failure."""
        caller_state = {"runs": 0}

        # Step 1: Execute failure case
        fail_inputs = iter(["y", "invalid_choice"])
        fail_exits = []
        ret_fail = conv.conversation(
            input_fn=lambda p: next(fail_inputs),
            print_fn=lambda *a: None,
            sleep_fn=lambda t: None,
            exit_fn=lambda code: fail_exits.append(code),
            default_user="Charlie"
        )
        caller_state["runs"] += 1
        self.assertEqual(ret_fail, "input_error_1")
        self.assertEqual(fail_exits, [1])

        # Step 2: Execute success case immediately after
        success_inputs = iter(["y", "yes"])
        success_exits = []
        ret_success = conv.conversation(
            input_fn=lambda p: next(success_inputs),
            print_fn=lambda *a: None,
            sleep_fn=lambda t: None,
            exit_fn=lambda code: success_exits.append(code),
            default_user="Charlie"
        )
        caller_state["runs"] += 1
        self.assertEqual(ret_success, "nice")
        self.assertEqual(success_exits, [0])
        self.assertEqual(caller_state["runs"], 2)

    def test_second_failure_branch_line_41(self):
        """Test reaching second error fallback on Line 41 when robot justification is invalid."""
        inputs = iter(["y", "n", "maybe"])
        printed = []
        exits = []

        ret = conv.conversation(
            input_fn=lambda p: next(inputs),
            print_fn=lambda *args: printed.append(" ".join(str(a) for a in args)),
            sleep_fn=lambda t: None,
            exit_fn=lambda code: exits.append(code),
            default_user="Dana"
        )

        self.assertEqual(ret, "input_error_2")
        self.assertEqual(exits, [1])
        self.assertIn("You may have made an input error. Please restart and try again.", printed)


if __name__ == "__main__":
    unittest.main()
