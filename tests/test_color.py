import unittest

from procmount.color import blend, parse_color


class TestColor(unittest.TestCase):
    def test_names(self):
        self.assertEqual(parse_color("white"), (255, 255, 255))
        self.assertEqual(parse_color(" Black "), (0, 0, 0))

    def test_hex(self):
        self.assertEqual(parse_color("#ffffff"), (255, 255, 255))
        self.assertEqual(parse_color("f00"), (255, 0, 0))
        self.assertEqual(parse_color("#0a142f"), (10, 20, 47))

    def test_rgb_triplet(self):
        self.assertEqual(parse_color("12,34,56"), (12, 34, 56))

    def test_invalid(self):
        for bad in ("", "#12", "300,0,0", "nope", "1,2"):
            with self.assertRaises(ValueError):
                parse_color(bad)

    def test_blend_endpoints(self):
        self.assertEqual(blend((0, 0, 0), (255, 255, 255), 0), (0, 0, 0))
        self.assertEqual(blend((0, 0, 0), (255, 255, 255), 1), (255, 255, 255))
        self.assertEqual(blend((0, 0, 0), (100, 100, 100), 0.5), (50, 50, 50))

    def test_blend_clamps(self):
        self.assertEqual(blend((0, 0, 0), (10, 10, 10), 5), (10, 10, 10))


if __name__ == "__main__":
    unittest.main()
