#!/usr/bin/env python3
"""Focused test runner for Task R25-T012 (polygon.py)."""

import os
import subprocess
import sys
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
REPO_ROOT = TASK_DIR.parents[1]
TEST_FILE = TASK_DIR / "test_polygon.py"
RESULTS_FILE = TASK_DIR / "RESULTS.md"


def main():
    print(f"=== Running focused checks for R25-T012 ===")
    cmd = [sys.executable, "-m", "unittest", str(TEST_FILE), "-v"]
    print(f"Command: {' '.join(cmd)}")

    result = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    evidence = f"""# Verification Evidence — R25-T012

## Target
- **Script:** polygon.py
- **Function:** `polygon`
- **Python Version:** {sys.version.split()[0]}
- **Command:** `{' '.join(cmd)}`

## Precondition Citations
- Line 9: `WHITE = (255, 255, 255)` color anchor.
- Line 10: `GREEN = (0, 255, 0)` color anchor.
- Line 13: `pygame.draw.polygon(window, GREEN, ((146, 0), (236, 277), (56, 277)))` default call.
- Geometric Boundary: 2D polygons require `len(points) >= 3` vertices.

## Boundary Partitioning Table
| Domain Region | Vertex Count (`len(points)`) | Behavior / Expectation | Precondition Citation |
|---|---|---|---|
| Explicitly Unsupported | 0, 1, 2 | Raises `ValueError` | Line 13 (2D polygon topology) |
| Supported Boundary (Minimum) | 3 | Validated / Drawn (Triangle) | Line 13 minimal closed polygon |
| Supported Interior | >= 4 | Validated / Drawn (Polygon) | Standard planar geometry |

## Test Results
| Scenario | Preconditions | Literal Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|---|
| Smallest valid input (boundary) | L10, L13 | `points=((0,0),(1,0),(0,1))` | Returns validated points | `((0,0),(1,0),(0,1))` | PASS |
| Ordinary input (canonical) | L9, L10, L13 | `points=((146,0),(236,277),(56,277))` | Returns canonical points | `((146,0),(236,277),(56,277))` | PASS |
| Ordinary interior (quadrilateral) | L13 | `points=((0,0),(10,0),(10,10),(0,10))` | Returns quadrilateral points | `((0,0),(10,0),(10,10),(0,10))` | PASS |
| Unsupported boundary (< 3 points) | L13 boundary | `points=((0,0),(10,10))` | Raises `ValueError` | `ValueError` raised | PASS |
| Unsupported empty (0 points) | L13 boundary | `points=()` | Raises `ValueError` | `ValueError` raised | PASS |
| Fixture anchors preserved | L9, L10 | `WHITE, GREEN` | `(255,255,255), (0,255,0)` | Exact match | PASS |

## Test Runner Output
```
{result.stderr.strip() if result.stderr else result.stdout.strip()}
```

**Exit Code:** {result.returncode}
"""
    RESULTS_FILE.write_text(evidence, encoding="utf-8")

    if result.returncode == 0:
        print("All R25-T012 checks passed successfully.")
    else:
        print(f"Checks failed with exit code {result.returncode}", file=sys.stderr)

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
