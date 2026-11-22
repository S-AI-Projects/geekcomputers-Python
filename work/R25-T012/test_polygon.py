"""Focused boundary tests for polygon in polygon.py.

Precondition citations:
    - Line 9: WHITE = (255, 255, 255) anchor
    - Line 10: GREEN = (0, 255, 0) anchor
    - Line 13: polygon(window, GREEN, ((146, 0), (236, 277), (56, 277)))
    - Geometric boundary: A polygon requires at least 3 vertices (triangle boundary).
"""

import sys
import unittest
from unittest.mock import MagicMock
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import polygon as poly


class TestPolygonBoundary(unittest.TestCase):
    """Tests verifying supported interior, supported boundary, and unsupported domain around polygon."""

    def test_smallest_valid_input_triangle(self):
        """Smallest valid input on boundary: exactly 3 points (minimal polygon).
        
        Preconditions:
            - Line 10: GREEN = (0, 255, 0)
            - Boundary: len(points) == 3
        Literal input:
            points = ((0, 0), (1, 0), (0, 1)), color = (0, 255, 0)
        Independently calculated expected output:
            Points sequence returned / validated without error
        """
        pts = ((0, 0), (1, 0), (0, 1))
        res = poly.polygon(surface=None, color=poly.GREEN, points=pts)
        self.assertEqual(res, pts)

    def test_ordinary_input(self):
        """Ordinary input: canonical triangle from source line 13.
        
        Preconditions:
            - Line 9: WHITE = (255, 255, 255)
            - Line 10: GREEN = (0, 255, 0)
            - Line 13: points = ((146, 0), (236, 277), (56, 277))
        Literal input:
            points = ((146, 0), (236, 277), (56, 277))
        Independently calculated expected output:
            ((146, 0), (236, 277), (56, 277))
        """
        expected = ((146, 0), (236, 277), (56, 277))
        res = poly.polygon(surface=None, color=poly.GREEN, points=expected)
        self.assertEqual(res, expected)

    def test_ordinary_quadrilateral(self):
        """Ordinary interior input: 4-vertex polygon (quadrilateral).
        
        Preconditions:
            - Boundary: len(points) > 3 is interior valid domain
        Literal input:
            points = ((0, 0), (10, 0), (10, 10), (0, 10))
        Independently calculated expected output:
            ((0, 0), (10, 0), (10, 10), (0, 10))
        """
        quad = ((0, 0), (10, 0), (10, 10), (0, 10))
        res = poly.polygon(surface=None, color=poly.WHITE, points=quad)
        self.assertEqual(res, quad)

    def test_unsupported_boundary_below_minimum(self):
        """Boundary test: 2 points (line segment, cannot form 2D polygon).
        
        Preconditions:
            - Boundary rule: len(points) < 3 is explicitly unsupported
        Literal input:
            points = ((0, 0), (10, 10))
        Independently calculated expected output:
            Raises ValueError('A polygon requires at least 3 points')
        """
        with self.assertRaises(ValueError) as ctx:
            poly.polygon(surface=None, points=((0, 0), (10, 10)))
        self.assertIn("at least 3 points", str(ctx.exception))

    def test_unsupported_empty_points(self):
        """Boundary test: 0 points (empty sequence).
        
        Preconditions:
            - Boundary rule: len(points) < 3 is explicitly unsupported
        Literal input:
            points = ()
        Independently calculated expected output:
            Raises ValueError('A polygon requires at least 3 points')
        """
        with self.assertRaises(ValueError) as ctx:
            poly.polygon(surface=None, points=())
        self.assertIn("at least 3 points", str(ctx.exception))

    def test_color_anchors(self):
        """Verify source color fixture anchors are preserved."""
        self.assertEqual(poly.WHITE, (255, 255, 255))
        self.assertEqual(poly.GREEN, (0, 255, 0))


if __name__ == "__main__":
    unittest.main()
