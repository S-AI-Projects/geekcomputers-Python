"""Focused complexity scaling and correctness tests for webcam in webcam.py.

Precondition citations:
    - Line 11-12: `frames_width`, `frames_height` resolution anchors.
    - Line 34: `gray = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)` frame processing anchor.
    - Complexity invariant: Work scales linearly O(N) where N = width * height * frames.
"""

import random
import sys
import time
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import webcam


class TestWebcamComplexity(unittest.TestCase):
    """Tests verifying correctness and measuring scaling across increasing input dimensions."""

    def test_smallest_valid_input_single_pixel(self):
        """Smallest valid input: 1 frame of 1x1 pixel.
        
        Preconditions:
            - Line 11-12: width=1, height=1
            - Line 34: BGR -> BGRA adds alpha channel 255
        Literal input:
            frames = [[[[10, 20, 30]]]]
        Independently calculated expected output:
            [[[[10, 20, 30, 255]]]]
        """
        frame = [[[10, 20, 30]]]
        out = webcam.webcam([frame])
        expected = [[[10, 20, 30, 255]]]
        self.assertEqual(out, [expected])

    def test_ordinary_input_2x2_frame(self):
        """Ordinary input: 1 frame of 2x2 pixels.
        
        Preconditions:
            - Line 11-12: width=2, height=2
            - Line 34: all 4 pixels converted to BGRA
        Literal input:
            frame with 4 known RGB triples
        Independently calculated expected output:
            all 4 pixels have alpha 255 added
        """
        frame = [
            [[1, 2, 3], [4, 5, 6]],
            [[7, 8, 9], [10, 11, 12]]
        ]
        out = webcam.webcam([frame])
        expected = [
            [[1, 2, 3, 255], [4, 5, 6, 255]],
            [[7, 8, 9, 255], [10, 11, 12, 255]]
        ]
        self.assertEqual(out, [expected])

    def test_complexity_scaling_experiment(self):
        """Measure execution time across 3 increasing pixel dimensions with 5 repetitions each."""
        rng = random.Random(42)
        sizes = [10, 25, 50]  # Corresponding to 100, 625, and 2500 pixels per frame
        repetitions = 5
        timings = {}

        for dim in sizes:
            dim_timings = []
            for rep in range(repetitions):
                # Generate fresh frame of shape (dim, dim, 3)
                frame = [
                    [[rng.randint(0, 255) for _ in range(3)] for _ in range(dim)]
                    for _ in range(dim)
                ]

                # Measure pure algorithm conversion without I/O
                start_t = time.perf_counter()
                out = webcam.webcam([frame])
                elapsed = time.perf_counter() - start_t
                dim_timings.append(elapsed)

                # Correctness assertions outside timed interval
                self.assertEqual(len(out), 1)
                self.assertEqual(len(out[0]), dim)
                self.assertEqual(len(out[0][0]), dim)
                self.assertEqual(len(out[0][0][0]), 4)
                self.assertEqual(out[0][0][0][3], 255)

            dim_timings.sort()
            median_t = dim_timings[len(dim_timings) // 2]
            spread = dim_timings[-1] - dim_timings[0]
            timings[dim * dim] = {"median": median_t, "range": spread, "all": dim_timings}

        # Store timings on class for check.py receipt generation
        TestWebcamComplexity.recorded_timings = timings
        # Ensure measurements were collected
        self.assertEqual(len(timings), 3)


if __name__ == "__main__":
    unittest.main()
