"""Compose a layered mountain scene."""

import random

from .canvas import Canvas
from .color import blend
from .terrain import ridge

# Per-layer placement as a fraction of image height, from back (t=0) to front (t=1).
BASE_Y = (0.42, 1.05)  # y of the valley floor
AMPLITUDE = (0.16, 0.40)  # peak height above the floor


def _lerp(pair, t):
    return pair[0] + (pair[1] - pair[0]) * t


def generate(
    width=2048,
    height=768,
    *,
    layers=5,
    roughness=1.0,
    seed=None,
    fg=(255, 255, 255),
    bg=(0, 0, 0),
    fade=0.6,
    moon=True,
    moon_size=None,
    stars=120,
):
    """Render a procedural mountain landscape and return a Canvas."""
    if width < 2 or height < 2:
        raise ValueError("width and height must be >= 2")
    if layers < 1:
        raise ValueError("layers must be >= 1")

    rng = random.Random(seed)
    canvas = Canvas(width, height, bg)

    _draw_sky(canvas, rng, fg, bg, moon, moon_size, stars)

    hurst = max(0.2, min(1.8, 2.0 - roughness))
    for i in range(layers):
        t = i / (layers - 1) if layers > 1 else 1.0
        color = blend(bg, fg, (1 - fade) + fade * t)
        base = height * _lerp(BASE_Y, t)
        amp = height * _lerp(AMPLITUDE, t)
        heights = ridge(width, rng, hurst)
        for x in range(width):
            canvas.fill_column(x, base - amp * heights[x], color)

    return canvas


def _draw_sky(canvas, rng, fg, bg, moon, moon_size, stars):
    sky_h = int(canvas.h * 0.7)
    for _ in range(stars):
        x = rng.randrange(canvas.w)
        y = rng.randrange(sky_h)
        canvas.blend_pixel(x, y, fg, rng.uniform(0.25, 1.0))

    if moon:
        r = moon_size if moon_size is not None else max(6, int(canvas.h * 0.09))
        cx = rng.uniform(canvas.w * 0.12, canvas.w * 0.88)
        cy = rng.uniform(r + 4, canvas.h * 0.38)
        canvas.disc(cx, cy, r, blend(bg, fg, 0.92))
