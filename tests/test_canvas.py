import unittest

from procmount.canvas import Canvas

WHITE = (255, 255, 255)


def _lit_rows(canvas, x):
    return [y for y in range(canvas.h) if canvas.buf[(y * canvas.w + x) * 3] > 0]


class TestCanvas(unittest.TestCase):
    def test_init_fills_background(self):
        c = Canvas(3, 2, (10, 20, 30))
        self.assertEqual(bytes(c.buf), bytes((10, 20, 30)) * 6)

    def test_fill_column_to_bottom(self):
        c = Canvas(4, 10, (0, 0, 0))
        c.fill_column(1, 4.0, WHITE)
        self.assertEqual(_lit_rows(c, 1), list(range(4, 10)))

    def test_draw_vspan_solid_middle(self):
        c = Canvas(4, 10, (0, 0, 0))
        c.draw_vspan(2, 3.0, 6.0, WHITE)
        self.assertEqual(_lit_rows(c, 2), [3, 4, 5])

    def test_draw_vspan_antialiases_ends(self):
        c = Canvas(4, 10, (0, 0, 0))
        c.draw_vspan(0, 2.5, 5.5, WHITE)
        i = lambda y: c.buf[(y * c.w + 0) * 3]
        self.assertTrue(0 < i(2) < 255)  # top edge partial
        self.assertEqual(i(3), 255)
        self.assertTrue(0 < i(5) < 255)  # bottom edge partial

    def test_out_of_bounds_safe(self):
        c = Canvas(4, 4, (0, 0, 0))
        c.fill_column(99, 0.0, WHITE)
        c.draw_vspan(-1, 0.0, 4.0, WHITE)
        c.ring(2, 2, 10, WHITE, 2)  # extends past edges
        self.assertEqual(len(c.buf), 4 * 4 * 3)

    def test_ring_hollow_center(self):
        c = Canvas(40, 40, (0, 0, 0))
        c.ring(20, 20, 12, WHITE, 2)
        center = c.buf[(20 * 40 + 20) * 3]
        edge = max(c.buf[(20 * 40 + x) * 3] for x in range(40))
        self.assertEqual(center, 0)
        self.assertGreater(edge, 0)


if __name__ == "__main__":
    unittest.main()
