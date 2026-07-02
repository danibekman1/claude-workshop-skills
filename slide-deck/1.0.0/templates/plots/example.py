"""Exemplar plot - delete or replace once you have real figures.

Demonstrates: brand palette import, setup(), parse_output(), save() pattern,
and the box/arrow helpers for diagram-style figures.

Run via Makefile:
    cd plots && python3 example.py -o ../figs/example.png
"""

from __future__ import annotations

from _common import BRAND, ROLE, arrow, box, parse_output, save, setup


def main() -> None:
    output = parse_output()
    fig, ax = setup(figsize=(8, 4))
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 4)
    ax.set_aspect("equal")
    ax.axis("off")

    box(ax, 0.5, 1.5, 2.0, 1.0, "Before",  face=ROLE["baseline"])
    box(ax, 5.5, 1.5, 2.0, 1.0, "After",   face=ROLE["highlight"], text_color=BRAND["primary"])
    arrow(ax, 2.6, 2.0, 5.4, 2.0, label="change", label_xy=(4.0, 2.05))

    save(fig, output)


if __name__ == "__main__":
    main()
