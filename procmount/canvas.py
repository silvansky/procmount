"""RGB pixel buffer with the few drawing primitives the scene needs."""


class Canvas:
    def __init__(self, width, height, bg):
        self.w = width
        self.h = height
        self.buf = bytearray(bytes(bg) * (width * height))

    def set_pixel(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.buf[i : i + 3] = bytes(color)

    def blend_pixel(self, x, y, color, a):
        if a <= 0 or not (0 <= x < self.w and 0 <= y < self.h):
            return
        if a >= 1:
            return self.set_pixel(x, y, color)
        i = (y * self.w + x) * 3
        b = self.buf
        for c in range(3):
            b[i + c] = round(b[i + c] * (1 - a) + color[c] * a)

    def fill_column(self, x, top, color):
        """Fill column x from float `top` down to the bottom, anti-aliasing the top edge."""
        if not 0 <= x < self.w:
            return
        if top < 0:
            top = 0.0
        ti = int(top)
        if ti >= self.h:
            return
        frac = top - ti
        ystart = ti
        if frac > 0:
            self.blend_pixel(x, ti, color, 1 - frac)
            ystart = ti + 1
        if ystart >= self.h:
            return
        count = self.h - ystart
        stride = self.w * 3
        base = (ystart * self.w + x) * 3
        end = base + count * stride
        r, g, bl = color
        self.buf[base : end : stride] = bytes((r,)) * count
        self.buf[base + 1 : end + 1 : stride] = bytes((g,)) * count
        self.buf[base + 2 : end + 2 : stride] = bytes((bl,)) * count

    def disc(self, cx, cy, radius, color):
        """Filled circle with a 1px anti-aliased rim."""
        r = radius
        for y in range(int(cy - r) - 1, int(cy + r) + 2):
            dy = y - cy
            if abs(dy) > r:
                continue
            for x in range(int(cx - r) - 1, int(cx + r) + 2):
                d = ((x - cx) ** 2 + dy * dy) ** 0.5
                if d <= r - 1:
                    self.set_pixel(x, y, color)
                elif d < r:
                    self.blend_pixel(x, y, color, r - d)

    def ring(self, cx, cy, radius, color, width):
        """Circle outline of the given stroke width, anti-aliased."""
        half = width / 2
        reach = radius + half + 1
        for y in range(int(cy - reach), int(cy + reach) + 1):
            dy = y - cy
            for x in range(int(cx - reach), int(cx + reach) + 1):
                d = ((x - cx) ** 2 + dy * dy) ** 0.5
                self.blend_pixel(x, y, color, half + 0.5 - abs(d - radius))

    def draw_vspan(self, x, top, bottom, color):
        """Fill column x between floats `top` and `bottom`, anti-aliasing both ends."""
        if not 0 <= x < self.w:
            return
        top = max(0.0, top)
        bottom = min(float(self.h), bottom)
        if bottom <= top:
            return
        ti, bi = int(top), int(bottom)
        if ti == bi:
            return self.blend_pixel(x, ti, color, bottom - top)
        self.blend_pixel(x, ti, color, (ti + 1) - top)
        for y in range(ti + 1, bi):
            self.set_pixel(x, y, color)
        if bi < self.h:
            self.blend_pixel(x, bi, color, bottom - bi)
