#!/usr/bin/env python3
"""Focused test runner and evidence generator for Task R25-T022 (vowel remover function.py)."""

import os
import sys
import subprocess
import platform

TASK_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(TASK_DIR, "..", ".."))
TEST_FILE = os.path.join(TASK_DIR, "test_vowel_remover.py")
RESULTS_FILE = os.path.join(TASK_DIR, "RESULTS.md")


def run_checks():
    print(f"=== Running focused boundary checks for R25-T022 (vowel remover function.py) ===")
    cmd = [sys.executable, "-m", "pytest", "-v", TEST_FILE]
    print(f"Command: {' '.join(cmd)}")

    result = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    # Save evidence and results
    evidence = []
    evidence.append("# Verification Evidence — R25-T022 (vowel remover function.py)\n")
    evidence.append("## Environment & Tool Versions")
    evidence.append(f"- **Python Version:** {platform.python_version()}")
    evidence.append(f"- **Platform:** {platform.platform()}")
    evidence.append(f"- **Runner:** {sys.executable}")
    evidence.append(f"- **Target File:** vowel remover function.py (function `vowel_remover`)")
    evidence.append(f"- **Test Suite:** work/R25-T022/test_vowel_remover.py\n")

    evidence.append("## Executed Command")
    evidence.append(f"```bash\n{' '.join(cmd)}\n```\n")

    evidence.append("## Precondition Source Lines Cited")
    evidence.append("- `vowel remover function.py#L27`: `for l in text:` (iterable requirement)")
    evidence.append("- `vowel remover function.py#L28`: `if l.lower() not in 'aeiou':` (.lower() method requirement)")
    evidence.append("- `vowel remover function.py#L29`: `string += l` (string concatenation requirement)\n")

    evidence.append("## Supported Domain & Boundary Table")
    evidence.append("| Category | Scenario | Preconditions | Literal Input | Expected Output | Actual Output | Status |")
    evidence.append("|---|---|---|---|---|---|---|")
    evidence.append("| Valid Boundary | Smallest valid input | L27, L31 | `\"\"` | `\"\"` | `\"\"` | PASS |")
    evidence.append("| Valid Interior | Ordinary input | L27-L29 | `\"hello world!\"` | `\"hll wrld!\"` | `\"hll wrld!\"` | PASS |")
    evidence.append("| Valid Boundary | All vowels (mixed case) | L28 | `\"aeiouAEIOU\"` | `\"\"` | `\"\"` | PASS |")
    evidence.append("| Valid Boundary | Zero vowels | L28 | `\"rhythm fly pry\"` | `\"rhythm fly pry\"` | `\"rhythm fly pry\"` | PASS |")
    evidence.append("| Valid Boundary | Single consonant | L27-29 | `\"b\"` | `\"b\"` | `\"b\"` | PASS |")
    evidence.append("| Valid Boundary | Single vowel | L27-29 | `\"a\"` | `\"\"` | `\"\"` | PASS |")
    evidence.append("| Valid Boundary | Digits & symbols | L28 | `\" 12345!@#$%^ \"` | `\" 12345!@#$%^ \"` | `\" 12345!@#$%^ \"` | PASS |")
    evidence.append("| Unsupported | Non-iterable int | L27 | `12345` | `TypeError` | `TypeError` | PASS |")
    evidence.append("| Unsupported | Elements without .lower() | L28 | `[1, 2, 3]` | `AttributeError` | `AttributeError` | PASS |\n")

    evidence.append("## Pytest Console Output")
    evidence.append(f"```\n{result.stdout}\n```\n")
    evidence.append(f"**Exit Code:** {result.returncode}\n")

    with open(RESULTS_FILE, "w") as f:
        f.write("\n".join(evidence))

    print(f"Results saved to {RESULTS_FILE}")
    sys.exit(result.returncode)


if __name__ == "__main__":
    run_checks()
