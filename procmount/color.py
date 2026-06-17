"""Color parsing and blending."""

_NAMES = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 128, 0),
    "blue": (0, 0, 255),
    "navy": (10, 20, 48),
    "midnight": (8, 12, 28),
    "slate": (40, 48, 66),
    "gray": (128, 128, 128),
    "grey": (128, 128, 128),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "yellow": (255, 255, 0),
    "orange": (255, 140, 0),
    "amber": (255, 191, 64),
    "pink": (255, 120, 160),
    "teal": (0, 128, 128),
    "cream": (245, 240, 225),
}

_HEX = set("0123456789abcdef")


def parse_color(s):
    """Accept a name, #rgb, #rrggbb, or 'r,g,b' and return an (r,g,b) tuple."""
    s = s.strip().lower()
    if s in _NAMES:
        return _NAMES[s]
    if "," in s:
        parts = s.split(",")
        if len(parts) == 3:
            try:
                rgb = tuple(int(p) for p in parts)
            except ValueError:
                rgb = None
            if rgb and all(0 <= v <= 255 for v in rgb):
                return rgb
        raise ValueError(f"invalid color: {s!r}")
    h = s[1:] if s.startswith("#") else s
    if h and all(c in _HEX for c in h):
        if len(h) == 3:
            return tuple(int(c * 2, 16) for c in h)
        if len(h) == 6:
            return tuple(int(h[i : i + 2], 16) for i in range(0, 6, 2))
    raise ValueError(f"invalid color: {s!r}")


def blend(c0, c1, t):
    """Linear interpolate from c0 (t=0) to c1 (t=1)."""
    t = 0.0 if t < 0 else 1.0 if t > 1 else t
    return tuple(round(a * (1 - t) + b * t) for a, b in zip(c0, c1))
