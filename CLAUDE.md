# procmount

CLI that procedurally generates mountain landscape PNGs. Pure Python stdlib, **zero dependencies**.

## Commands

```sh
python3 -m procmount                    # render → mountain.png
python3 -m unittest discover -s tests   # run tests (19)
```

No build step. No package install needed to run (`python -m procmount`); `pip install -e .` adds a `procmount` command.

## Hard constraint: no third-party deps

The local Homebrew Python 3.14 has a broken `pyexpat` (libexpat symbol mismatch) that
breaks pip/ensurepip, so Pillow/numpy **cannot be installed here**. The tool deliberately
ships its own PNG writer (`png.py`, via `zlib`) and uses only the stdlib. Keep it that way —
do not add imports outside the standard library.

## Layout

- `png.py` — PNG encoder (IHDR/IDAT/IEND chunks, zlib, CRC). 8-bit truecolor RGB.
- `terrain.py` — `ridge()`: 1-D midpoint displacement → normalized heights, resampled to width. Lower `hurst` = jaggedier.
- `canvas.py` — `Canvas` RGB buffer. `fill_column` uses strided slice assignment (fast) + anti-aliased top edge; `disc` for the moon.
- `render.py` — `generate()`: draws sky (stars, moon) then mountain layers back-to-front, blending each layer's color from `bg`→`fg` by depth (atmospheric fade). Tunables: `BASE_Y`, `AMPLITUDE`.
- `color.py` — `parse_color` (name / hex / `r,g,b`), `blend`.
- `cli.py` — argparse entry point; maps user `roughness` → `hurst` as `2.0 - roughness`.

## Conventions

- New features need tests (`tests/`, stdlib `unittest`).
- Run tests before committing. Validate rendered PNGs with `sips -g pixelWidth -g pixelHeight <file>`.
- `demo/*.png` are committed showcase images; root-level `*.png` are gitignored.
