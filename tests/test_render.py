import unittest

from procmount.render import generate


class TestRender(unittest.TestCase):
    def test_dimensions(self):
        c = generate(width=128, height=64, seed=1)
        self.assertEqual((c.w, c.h), (128, 64))
        self.assertEqual(len(c.buf), 128 * 64 * 3)

    def test_not_blank(self):
        bg = (0, 0, 0)
        c = generate(width=128, height=64, seed=1, bg=bg, fg=(255, 255, 255))
        self.assertTrue(any(c.buf[i : i + 3] != bytes(bg) for i in range(0, len(c.buf), 3)))

    def test_deterministic(self):
        a = generate(width=96, height=48, seed=5)
        b = generate(width=96, height=48, seed=5)
        self.assertEqual(a.buf, b.buf)

    def test_seed_varies(self):
        a = generate(width=96, height=48, seed=1)
        b = generate(width=96, height=48, seed=2)
        self.assertNotEqual(a.buf, b.buf)

    def test_invalid_dims(self):
        with self.assertRaises(ValueError):
            generate(width=1, height=64)

    def test_single_layer_no_moon(self):
        c = generate(width=64, height=64, seed=3, layers=1, moon=False, stars=0)
        self.assertEqual(len(c.buf), 64 * 64 * 3)


if __name__ == "__main__":
    unittest.main()
