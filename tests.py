import unittest
import pandas as pd
import numpy as np


class TestLeastSquares(unittest.TestCase):

    def test_least_squares_zero(self):
        y1 = np.array([1, 2, 3])
        y2 = np.array([1, 2, 3])
        self.assertEqual(((y1 - y2) ** 2).sum(), 0)


class TestDeviation(unittest.TestCase):

    def test_deviation_positive(self):
        self.assertTrue(abs(5 - 3) > 0)


if __name__ == "__main__":
    unittest.main()
