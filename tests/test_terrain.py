import random
import unittest

from procmount.terrain import ridge


class TestRidge(unittest.TestCase):
    def test_length_matches_width(self):
        for w in (2, 3, 100, 513, 2048):
            self.assertEqual(len(ridge(w, random.Random(1))), w)

    def test_values_normalized(self):
        h = ridge(500, random.Random(7))
        self.assertGreaterEqual(min(h), 0.0)
        self.assertLessEqual(max(h), 1.0)
        self.assertGreater(max(h) - min(h), 0.5)  # spans a meaningful range

    def test_deterministic_with_seed(self):
        self.assertEqual(ridge(256, random.Random(42)), ridge(256, random.Random(42)))

    def test_seed_changes_output(self):
        self.assertNotEqual(ridge(256, random.Random(1)), ridge(256, random.Random(2)))

    def test_width_one(self):
        self.assertEqual(len(ridge(1, random.Random(1))), 1)


if __name__ == "__main__":
    unittest.main()
