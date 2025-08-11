import os
from typing import Dict, List, Tuple

# Grid-based pixel-art to SVG generator

SPRITES_OUT_DIR = "/workspace/assets/sprites"
SCALE = 8  # multiplier for crisp pixels

Color = Tuple[int, int, int, int]

PALETTE: Dict[str, str] = {
    # General
    "_": "none",  # transparent / skip
    "O": "#1e1428",  # outline dark purple
    # Skin / hair
    "S": "#ffd9b3",  # skin
    "H": "#3a2a24",  # hair dark brown/black mix
    "h": "#6c4a3b",  # hair highlight
    # Eyes / glasses
    "E": "#2aa84a",  # green eye
    "G": "#202225",  # glasses frame / dark
    # Clothing - shared style similar to reference
    "T": "#55c146",  # shirt primary green
    "t": "#3aa133",  # shirt shade
    "J": "#2a2e44",  # hijab dark
    "j": "#515777",  # hijab light
    "P": "#355bd6",  # pants primary blue
    "p": "#243f9e",  # pants shade
    "W": "#ffffff",  # shoes
    "w": "#d8d8d8",  # shoe shade
}


def write_svg(filename: str, grid: List[str]) -> None:
    height = len(grid)
    width = max(len(row) for row in grid)
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(
            f"<svg xmlns='http://www.w3.org/2000/svg' width='{width * SCALE}' height='{height * SCALE}' viewBox='0 0 {width * SCALE} {height * SCALE}' shape-rendering='crispEdges'>\n"
        )
        # background is transparent; draw pixels as rectangles
        for y, row in enumerate(grid):
            for x, key in enumerate(row):
                if key == "_":
                    continue
                color = PALETTE.get(key, None)
                if not color:
                    continue
                f.write(
                    f"  <rect x='{x * SCALE}' y='{y * SCALE}' width='{SCALE}' height='{SCALE}' fill='{color}' />\n"
                )
        f.write("</svg>\n")


def mirror_h(grid: List[str]) -> List[str]:
    return [row[::-1] for row in grid]


# The following grids are handcrafted 22x24 pixel sprites inspired by the provided style.
# Keys:
#   _ none, O outline, S skin, H/h hair, E eye, G glasses, T/t shirt, J/j hijab, P/p pants, W/w shoes


def guy_right() -> List[str]:
    return [
        "______________________",
        "________OOOHHHOO______",
        "_______OHhHHHHHHO_____",
        "______OHhHHSSHHHOO____",
        "______OHSSSSSSSHO_____",
        "______OHSS_E_SSHO_____",
        "_______OOSSSSSOO______",
        "_________OTTTTO_______",
        "________OTTTTTTO______",
        "_______OTTTtTTTTO_____",
        "______OTTTTTTTTTTO____",
        "_____OTTTTTTTTTTTTO___",
        "_____OTTTTTTTTTTTTO___",
        "______OPPPppPPPPPO____",
        "______OPPPPPPPPPPO____",
        "______OPPP__PPPPPO____",
        "______OPPP__PPPPPO____",
        "_______OWWW__WWW0_____".replace('0', 'O'),
        "_______OWw____wWO_____",
        "______________________",
    ]


def girl_right() -> List[str]:
    return [
        "______________________",
        "________OOOOOOOO______",
        "_______OJjJJJJJOO_____",
        "______OJjJJJJJJJOO____",
        "______OJjJHSSJJJJO____",
        "______OJjJSGSJJJJO____",  # G for glasses bridge
        "______OJjJSSSJJJJO____",
        "_______OJJJJJJJJO_____",
        "________OJJJJJJO______",
        "________OTTTtTTO______",
        "_______OTTTTTTTTO_____",
        "______OTTTTTTTTTTO____",
        "______OTTTTTTTTTTO____",
        "______OPPPppPPPPPO____",
        "______OPPPPPPPPPPO____",
        "______OPPP__PPPPPO____",
        "______OPPP__PPPPPO____",
        "_______OWWW__WWW0_____".replace('0', 'O'),
        "_______OWw____wWO_____",
        "______________________",
    ]


def add_face_details_guy(grid: List[str]) -> List[str]:
    # Add eye pixel facing right and jaw outline; already encoded in the grid
    return grid


def add_glasses_to_girl(grid: List[str]) -> List[str]:
    # Draw glasses frames around eyes using G key; simple 3x1 bars on each side
    g = grid[:]
    row = list(g[5])
    # left lens frame
    for x in range(10, 12):
        row[x] = 'G'
    # bridge already in template
    # right lens frame
    for x in range(13, 15):
        row[x] = 'G'
    g[5] = ''.join(row)

    # add verticals below lenses
    r6 = list(g[6])
    r6[10] = 'G'
    r6[14] = 'G'
    g[6] = ''.join(r6)
    return g


def main() -> None:
    guy_r = add_face_details_guy(guy_right())
    girl_r = add_glasses_to_girl(girl_right())

    guy_l = mirror_h(guy_r)
    girl_l = mirror_h(girl_r)

    write_svg(os.path.join(SPRITES_OUT_DIR, "guy_right.svg"), guy_r)
    write_svg(os.path.join(SPRITES_OUT_DIR, "guy_left.svg"), guy_l)
    write_svg(os.path.join(SPRITES_OUT_DIR, "girl_right.svg"), girl_r)
    write_svg(os.path.join(SPRITES_OUT_DIR, "girl_left.svg"), girl_l)


if __name__ == "__main__":
    main()