"""Command-line interface for procmount."""

import argparse
import random

from .color import parse_color
from .png import write_png
from .render import generate


def build_parser():
    p = argparse.ArgumentParser(
        prog="procmount",
        description="Procedurally generate a mountain landscape image.",
    )
    p.add_argument("-o", "--output", default="mountain.png", help="output PNG path")

    dim = p.add_argument_group("dimensions")
    dim.add_argument("-W", "--width", type=int, default=2048, help="image width (px)")
    dim.add_argument("-H", "--height", type=int, default=768, help="image height (px)")

    gen = p.add_argument_group("generation")
    gen.add_argument("-l", "--layers", type=int, default=5, help="number of mountain ranges")
    gen.add_argument(
        "-r", "--roughness", type=float, default=1.0,
        help="ridge jaggedness; higher is rougher (~0.4-1.4)",
    )
    gen.add_argument("-s", "--seed", type=int, default=None, help="random seed (default: random)")
    gen.add_argument(
        "--fade", type=float, default=0.6,
        help="atmospheric fade of distant ranges into the background (0-1)",
    )
    gen.add_argument(
        "--moon", action=argparse.BooleanOptionalAction, default=True, help="draw a moon",
    )
    gen.add_argument("--moon-size", type=int, default=None, help="moon radius in px")
    gen.add_argument("--stars", type=int, default=120, help="number of stars")
    gen.add_argument(
        "--contour", action="store_true", help="stroke ridgelines only (line art) instead of filling",
    )
    gen.add_argument("--line-width", type=int, default=2, help="contour stroke width in px")

    col = p.add_argument_group("color")
    col.add_argument("--fg", type=parse_color, default="white", help="landscape color")
    col.add_argument("--bg", type=parse_color, default="black", help="background color")

    return p


def main(argv=None):
    args = build_parser().parse_args(argv)

    seed = args.seed if args.seed is not None else random.randrange(2**32)

    canvas = generate(
        width=args.width,
        height=args.height,
        layers=args.layers,
        roughness=args.roughness,
        seed=seed,
        fg=args.fg,
        bg=args.bg,
        fade=args.fade,
        moon=args.moon,
        moon_size=args.moon_size,
        stars=args.stars,
        contour=args.contour,
        line_width=args.line_width,
    )
    write_png(args.output, canvas.w, canvas.h, canvas.buf)
    print(f"wrote {args.output} ({canvas.w}x{canvas.h}, seed {seed})")


if __name__ == "__main__":
    main()
