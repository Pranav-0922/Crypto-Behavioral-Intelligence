# -*- coding: utf-8 -*-
"""
config.py — Global constants, plot theme, and sentiment settings.
"""

import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")

# ── File paths ──────────────────────────────────────────────────────────────
FEAR_GREED_CSV   = "fear_greed_index.csv"
HISTORICAL_CSV   = "historical_data.csv"

# ── Sentiment ordering & colours ────────────────────────────────────────────
SENTIMENT_ORDER = ["Extreme Fear", "Fear", "Neutral", "Greed", "Extreme Greed"]

SENTIMENT_COLORS = {
    "Extreme Fear":  "#ff4d4f",
    "Fear":          "#ff7a45",
    "Neutral":       "#ffd666",
    "Greed":         "#73d13d",
    "Extreme Greed": "#36cfc9",
}

# ── Matplotlib dark theme ────────────────────────────────────────────────────
def apply_plot_theme():
    """Apply the global dark GitHub-style matplotlib theme."""
    plt.rcParams.update({
        "figure.facecolor":  "#0d1117",
        "axes.facecolor":    "#161b22",
        "axes.edgecolor":    "#30363d",
        "axes.labelcolor":   "#c9d1d9",
        "axes.titlecolor":   "#f0f6fc",
        "xtick.color":       "#8b949e",
        "ytick.color":       "#8b949e",
        "text.color":        "#c9d1d9",
        "grid.color":        "#21262d",
        "grid.linestyle":    "--",
        "grid.linewidth":    0.6,
        "font.family":       "monospace",
        "axes.titlesize":    13,
        "axes.labelsize":    11,
    })
