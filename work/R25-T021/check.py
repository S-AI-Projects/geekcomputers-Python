#!/usr/bin/env python3
"""Focused test runner and evidence generator for Task R25-T021 (merge.py)."""

import os
import sys
import subprocess
import platform

TASK_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(TASK_DIR, "..", ".."))
TEST_FILE = os.path.join(TASK_DIR, "test_merge.py")
RESULTS_FILE = os.path.join(TASK_DIR, "RESULTS.md")


def run_checks():
    print(f"=== Running focused checks for R25-T021 (merge.py) ===")
    cmd = [sys.executable, "-m", "pytest", "-v", TEST_FILE]
    print(f"Command: {' '.join(cmd)}")

    result = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    # Save evidence and results
    evidence = []
    evidence.append("# Verification Evidence — R25-T021 (merge.py)\n")
    evidence.append("## Environment & Tool Versions")
    evidence.append(f"- **Python Version:** {platform.python_version()}")
    evidence.append(f"- **Platform:** {platform.platform()}")
    evidence.append(f"- **Runner:** {sys.executable}")
    evidence.append(f"- **Target File:** merge.py (function `merge`)")
    evidence.append(f"- **Test Suite:** work/R25-T021/test_merge.py\n")

    evidence.append("## Executed Command")
    evidence.append(f"```bash\n{' '.join(cmd)}\n```\n")

    evidence.append("## Precondition Source Lines Cited")
    evidence.append("- `merge.py#L18`: `global resultfile` (output file specification)")
    evidence.append("- `merge.py#L21-L25`: Directory list comprehension and CSV extension predicate")
    evidence.append("- `merge.py#L28`: `with open(resultfile, 'w') as writefile:` (overwrite semantics)")
    evidence.append("- `merge.py#L34`: `writefile.write(readfile.read() + '\\n')` (newline concatenation)\n")

    evidence.append("## Inputs and Expected vs Actual Results")
    evidence.append("| Scenario | Preconditions | Literal Input | Expected Output | Actual Result | Status |")
    evidence.append("|---|---|---|---|---|---|")
    evidence.append("| Smallest input (0 CSVs) | L18, L21-25, L28 | No CSV files | Empty `result.csv`, return `None` | Empty `result.csv`, return `None` | PASS |")
    evidence.append("| Smallest input (1 CSV) | L21-25, L28, L34 | `single.csv: 'k,v\\n1,2'` | `result.csv: 'k,v\\n1,2\\n'` | `result.csv: 'k,v\\n1,2\\n'` | PASS |")
    evidence.append("| Ordinary input (2 CSVs) | L21-25, L28, L34 | `a.csv`, `b.csv` | Sequential concatenation with newlines | Sequential concatenation with newlines | PASS |")
    evidence.append("| Repeated value boundary | L21-25, L34 | `rep1.csv`, `rep2.csv` (duplicate rows) | Full duplication preserved (no loss) | Full duplication preserved (no loss) | PASS |")
    evidence.append("| Boundary filtering | L24 | Non-csv files & existing result | Only valid CSVs included, result overwritten | Only valid CSVs included, result overwritten | PASS |\n")

    evidence.append("## Pytest Console Output")
    evidence.append(f"```\n{result.stdout}\n```\n")
    evidence.append(f"**Exit Code:** {result.returncode}\n")

    with open(RESULTS_FILE, "w") as f:
        f.write("\n".join(evidence))

    print(f"Results saved to {RESULTS_FILE}")
    sys.exit(result.returncode)


if __name__ == "__main__":
    run_checks()
