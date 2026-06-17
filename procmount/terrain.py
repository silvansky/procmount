"""Fractal ridgelines via 1-D midpoint displacement."""


def _resample(values, width):
    n = len(values)
    if n == width:
        return list(values)
    if width == 1:
        return [values[0]]
    out = []
    for x in range(width):
        t = x * (n - 1) / (width - 1)
        i = int(t)
        if i + 1 < n:
            out.append(values[i] * (1 - (t - i)) + values[i + 1] * (t - i))
        else:
            out.append(values[i])
    return out


def ridge(width, rng, hurst=1.0):
    """Return `width` heights in [0, 1].

    Lower `hurst` yields a more jagged ridge (slower displacement decay).
    """
    size = 2
    while size + 1 < width:
        size *= 2
    size += 1

    h = [0.0] * size
    h[0] = rng.random()
    h[-1] = rng.random()

    step = size - 1
    disp = 0.5
    decay = 2.0 ** (-hurst)
    while step > 1:
        half = step // 2
        for i in range(half, size - 1, step):
            h[i] = (h[i - half] + h[i + half]) / 2 + rng.uniform(-disp, disp)
        step = half
        disp *= decay

    lo, hi = min(h), max(h)
    span = (hi - lo) or 1.0
    h = [(v - lo) / span for v in h]
    return _resample(h, width)
