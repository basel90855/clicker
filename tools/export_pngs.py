import os
from pathlib import Path

from cairosvg import svg2png

ROOT = Path("/workspace")
SRC = ROOT / "assets" / "sprites"
OUT = SRC / "png"

SPRITES = [
    "guy_right.svg",
    "guy_left.svg",
    "girl_right.svg",
    "girl_left.svg",
]

SCALES = [1, 2, 4]


def export():
    OUT.mkdir(parents=True, exist_ok=True)
    for name in SPRITES:
        svg_path = SRC / name
        if not svg_path.exists():
            continue
        for scale in SCALES:
            out_name = f"{svg_path.stem}@{scale}x.png" if scale != 1 else f"{svg_path.stem}.png"
            out_path = OUT / out_name
            with open(svg_path, "rb") as f:
                svg2png(file_obj=f, write_to=str(out_path), scale=scale)
            print(f"Wrote {out_path}")


if __name__ == "__main__":
    export()