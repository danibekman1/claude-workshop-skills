"""Shared matplotlib style + brand palette for slide figures.

Import as:
    from _common import setup, save, parse_output, BRAND, ROLE
    from _common import box, arrow, band   # for diagram-style plots

The BRAND dict is the SINGLE SOURCE OF TRUTH for figure colors. The HTML hex
values here must match the \\definecolor lines in theme-overrides.tex. To
adopt a different brand palette, change the hex values in both files (keep
the key/variable names the same).

Never hard-code hex colors in individual plot scripts. Use ROLE for semantic
choices (baseline/proposed/highlight/...). If you genuinely need a brand color
without a semantic role, reach for BRAND["..."], not a literal #...
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


# --- Brand palette. Mirror of theme-overrides.tex. ---
# Defaults: a neutral Tailwind-inspired palette. Swap hex values to rebrand.
BRAND = {
    "primary":      "#1E3A8A",
    "primary_alt":  "#1E40AF",
    "accent":       "#3B82F6",
    "secondary":    "#60A5FA",
    "success":      "#10B981",
    "light_grey":   "#F3F4F6",
    "grey":         "#6B7280",
    "black":        "#000000",
    "white":        "#FFFFFF",
}

# --- Semantic roles. Prefer these over raw BRAND in plot scripts. ---
ROLE = {
    "baseline":    BRAND["primary"],         # the thing being compared against
    "proposed":    BRAND["accent"],          # the new approach
    "highlight":   BRAND["success"],         # call attention to this
    "secondary":   BRAND["secondary"],       # supporting / less-important
    "neutral_bg":  BRAND["light_grey"],      # backgrounds, bands
    "muted_text":  BRAND["grey"],            # axis labels, secondary annotations
    "warning":     BRAND["primary_alt"],     # bad-path arrows, deprecated, etc.
}


def setup(figsize=(10, 5)):
    """Configure matplotlib defaults and return (fig, ax)."""
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.labelsize": 11,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "figure.dpi": 130,
        "savefig.dpi": 160,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.15,
        "text.color":       BRAND["primary"],
        "axes.labelcolor":  BRAND["primary"],
        "xtick.color":      BRAND["grey"],
        "ytick.color":      BRAND["grey"],
    })
    fig, ax = plt.subplots(figsize=figsize)
    return fig, ax


def parse_output() -> Path:
    """Standard CLI: -o path/to/output.png."""
    p = argparse.ArgumentParser()
    p.add_argument("-o", "--output", type=Path, required=True)
    args = p.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    return args.output


def save(fig, output: Path) -> None:
    fig.savefig(output)
    print(f"wrote {output} ({output.stat().st_size} bytes)")


# --- Diagram primitives (boxes, arrows, layer bands) ---

def box(ax, x, y, w, h, label, *,
        face=ROLE["proposed"], text_color="white", fontsize=11, weight="bold"):
    """Rounded rectangular box centered on (x+w/2, y+h/2) with a centered label."""
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.05",
        linewidth=1.2, facecolor=face, edgecolor=face,
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, label,
            ha="center", va="center",
            color=text_color, fontsize=fontsize, weight=weight)


def band(ax, y, h, label, *, face=ROLE["neutral_bg"], x=0.2, w=11.6):
    """Horizontal band used as a layer background. Label sits at the top-left."""
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        linewidth=1.0, facecolor=face, edgecolor=ROLE["muted_text"], alpha=0.35,
    ))
    ax.text(x + 0.15, y + h - 0.18, label,
            ha="left", va="top",
            color=BRAND["primary"], fontsize=10.5, weight="bold", style="italic")


def arrow(ax, x1, y1, x2, y2, *,
          color=BRAND["primary"], label=None, label_xy=None,
          label_ha="center", label_va="center"):
    """Arrow from (x1,y1) to (x2,y2) with optional label on the arrow line.

    The label always gets a white-background bbox so it reads as anchored to
    the arrow rather than floating. This is lesson #3 - do not change the
    bbox default without a strong reason.
    """
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle="-|>", mutation_scale=14,
        color=color, linewidth=1.6, shrinkA=2, shrinkB=2,
    ))
    if label:
        if label_xy is None:
            label_xy = ((x1 + x2) / 2, (y1 + y2) / 2)
        ax.text(label_xy[0], label_xy[1], label,
                ha=label_ha, va=label_va,
                color=color, fontsize=9, style="italic",
                bbox=dict(facecolor="white", edgecolor="none", pad=2.5, alpha=0.95))
