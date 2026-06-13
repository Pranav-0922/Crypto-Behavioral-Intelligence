# -*- coding: utf-8 -*-
"""
visualizations.py — One function per figure; each saves a PNG and returns
                    the output filename.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors as mcolors

from config import SENTIMENT_ORDER, SENTIMENT_COLORS
from preprocessing import (
    sentiment_grouped,
    monthly_pnl,
    monthly_fear_greed,
    assign_trader_tiers,
    compute_trader_stats,
    compute_coin_stats,
)

_COLORS = [SENTIMENT_COLORS[s] for s in SENTIMENT_ORDER]


# ── Figure 1 — Overview dashboard ────────────────────────────────────────────

def fig1_overview_dashboard(fg: pd.DataFrame, closed: pd.DataFrame,
                             out: str = "fig1_overview_dashboard.png") -> str:
    print("🎨  Figure 1 — Overview Dashboard...")

    fig = plt.figure(figsize=(18, 13))
    fig.suptitle(
        "Bitcoin Market Sentiment  ×  Trader Performance\n"
        "Are traders actually smarter in Fear or in Greed?",
        fontsize=17, fontweight="bold", color="#f0f6fc", y=0.97,
    )
    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.45, wspace=0.35)

    # — Days per sentiment state
    ax1 = fig.add_subplot(gs[0, 0])
    day_counts = fg["classification"].value_counts().reindex(SENTIMENT_ORDER)
    bars = ax1.bar(SENTIMENT_ORDER, day_counts.values, color=_COLORS,
                   edgecolor="#0d1117", linewidth=0.8)
    ax1.set_title("How many days was the market in each state?")
    ax1.set_ylabel("Days")
    ax1.set_xticklabels(SENTIMENT_ORDER, rotation=20, ha="right", fontsize=9)
    ax1.yaxis.grid(True); ax1.set_axisbelow(True)
    for bar, val in zip(bars, day_counts.values):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 8,
                 f"{val:,}", ha="center", va="bottom", fontsize=9, color="#f0f6fc")

    # — Total PnL by sentiment
    ax2 = fig.add_subplot(gs[0, 1])
    total_pnl = sentiment_grouped(closed, "Closed PnL", "sum") / 1e6
    bars2 = ax2.bar(SENTIMENT_ORDER, total_pnl.values, color=_COLORS,
                    edgecolor="#0d1117", linewidth=0.8)
    ax2.set_title("Total Closed PnL by Sentiment ($M)")
    ax2.set_ylabel("PnL ($ millions)")
    ax2.set_xticklabels(SENTIMENT_ORDER, rotation=20, ha="right", fontsize=9)
    ax2.yaxis.grid(True); ax2.set_axisbelow(True)
    for bar, val in zip(bars2, total_pnl.values):
        ax2.text(bar.get_x() + bar.get_width() / 2, val + 0.04,
                 f"${val:.2f}M", ha="center", va="bottom", fontsize=9, color="#f0f6fc")

    # — Win rate
    ax3 = fig.add_subplot(gs[1, 0])
    win_rate = sentiment_grouped(closed, "profitable", "mean") * 100
    ax3.bar(SENTIMENT_ORDER, win_rate.values, color=_COLORS,
            edgecolor="#0d1117", linewidth=0.8)
    ax3.axhline(50, color="#8b949e", linestyle="--", linewidth=1, label="50% baseline")
    ax3.set_title("Win Rate (% profitable trades) by Sentiment")
    ax3.set_ylabel("Win Rate (%)")
    ax3.set_xticklabels(SENTIMENT_ORDER, rotation=20, ha="right", fontsize=9)
    ax3.set_ylim(0, 105)
    ax3.yaxis.grid(True); ax3.set_axisbelow(True)
    ax3.legend(fontsize=9)
    for i, val in enumerate(win_rate.values):
        ax3.text(i, val + 0.8, f"{val:.1f}%", ha="center", fontsize=9, color="#f0f6fc")

    # — Average PnL per trade
    ax4 = fig.add_subplot(gs[1, 1])
    avg_pnl = sentiment_grouped(closed, "Closed PnL", "mean")
    ax4.bar(SENTIMENT_ORDER, avg_pnl.values, color=_COLORS,
            edgecolor="#0d1117", linewidth=0.8)
    ax4.axhline(0, color="#8b949e", linestyle="-", linewidth=0.8)
    ax4.set_title("Average PnL Per Trade by Sentiment ($)")
    ax4.set_ylabel("Avg PnL ($)")
    ax4.set_xticklabels(SENTIMENT_ORDER, rotation=20, ha="right", fontsize=9)
    ax4.yaxis.grid(True); ax4.set_axisbelow(True)
    for i, val in enumerate(avg_pnl.values):
        ax4.text(i, val + 1.5, f"${val:.1f}", ha="center", fontsize=9, color="#f0f6fc")

    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"   saved → {out}")
    return out


# ── Figure 2 — BUY vs SELL behaviour ─────────────────────────────────────────

def fig2_buy_vs_sell(closed: pd.DataFrame,
                     out: str = "fig2_buy_vs_sell.png") -> str:
    print("🎨  Figure 2 — BUY vs SELL behaviour...")

    side_data = (
        closed.groupby(["classification", "Side"])["Closed PnL"]
        .agg(["mean", "count"])
        .reset_index()
    )

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    fig.patch.set_facecolor("#0d1117")
    fig.suptitle(
        "BUY vs SELL — Who's actually making money, and when?",
        fontsize=15, fontweight="bold", color="#f0f6fc", y=1.01,
    )

    for ax, (metric, ylabel, title) in zip(
        axes,
        [("mean",  "Avg PnL ($)",      "Avg PnL per Trade"),
         ("count", "Number of Trades", "Trade Volume")],
    ):
        buys  = (side_data[side_data["Side"] == "BUY"]
                 .set_index("classification").reindex(SENTIMENT_ORDER)[metric])
        sells = (side_data[side_data["Side"] == "SELL"]
                 .set_index("classification").reindex(SENTIMENT_ORDER)[metric])

        x, w = np.arange(len(SENTIMENT_ORDER)), 0.35
        ax.bar(x - w / 2, buys.values,  w, label="BUY",
               color="#58a6ff", edgecolor="#0d1117", linewidth=0.7)
        ax.bar(x + w / 2, sells.values, w, label="SELL",
               color="#ff7b72", edgecolor="#0d1117", linewidth=0.7)

        ax.set_title(title, fontsize=12)
        ax.set_ylabel(ylabel)
        ax.set_xticks(x)
        ax.set_xticklabels(SENTIMENT_ORDER, rotation=20, ha="right", fontsize=9)
        ax.yaxis.grid(True); ax.set_axisbelow(True)
        ax.legend(fontsize=10)
        ax.set_facecolor("#161b22")

    plt.tight_layout()
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"   saved → {out}")
    return out


# ── Figure 3 — Monthly PnL trend ─────────────────────────────────────────────

def fig3_monthly_trend(merged: pd.DataFrame, closed: pd.DataFrame,
                       out: str = "fig3_monthly_trend.png") -> str:
    print("🎨  Figure 3 — Monthly PnL trend...")

    m_pnl = monthly_pnl(closed)
    m_fg  = monthly_fear_greed(merged)

    fig, ax1 = plt.subplots(figsize=(16, 7))
    fig.patch.set_facecolor("#0d1117")
    ax1.set_facecolor("#161b22")

    ax1.fill_between(m_pnl.index, m_pnl.values / 1e6, alpha=0.3, color="#58a6ff")
    ax1.plot(m_pnl.index, m_pnl.values / 1e6, color="#58a6ff",
             linewidth=2.5, marker="o", markersize=5, label="Monthly PnL ($M)")
    ax1.set_ylabel("Monthly Closed PnL ($M)", color="#58a6ff")
    ax1.tick_params(axis="y", labelcolor="#58a6ff")
    ax1.yaxis.grid(True); ax1.set_axisbelow(True)

    ax2 = ax1.twinx()
    ax2.set_facecolor("#161b22")
    ax2.plot(m_fg.index, m_fg.values, color="#ffd666",
             linewidth=1.8, linestyle="--", alpha=0.85, label="Avg Fear/Greed Index")
    ax2.set_ylabel("Avg Fear/Greed Index (0–100)", color="#ffd666")
    ax2.tick_params(axis="y", labelcolor="#ffd666")
    ax2.set_ylim(0, 100)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=10,
               facecolor="#21262d", edgecolor="#30363d", labelcolor="#c9d1d9")

    ax1.set_title(
        "Monthly PnL vs Fear/Greed Index — the Dec 2024 rally was wild 👀",
        fontsize=14, fontweight="bold", color="#f0f6fc",
    )
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"   saved → {out}")
    return out


# ── Figure 4 — Top traders analysis ──────────────────────────────────────────

def fig4_top_traders(closed: pd.DataFrame,
                     out: str = "fig4_top_traders.png") -> str:
    print("🎨  Figure 4 — Top traders analysis...")

    trader_stats = compute_trader_stats(closed)
    top10 = trader_stats.head(10).copy()
    top10["label"]   = [f"Trader {i+1}" for i in range(len(top10))]
    top10["win_pct"] = top10["win_rate"] * 100

    fig, axes = plt.subplots(1, 3, figsize=(20, 7))
    fig.patch.set_facecolor("#0d1117")
    fig.suptitle("Top 10 Traders — What makes them different?",
                 fontsize=15, fontweight="bold", color="#f0f6fc")

    palette = plt.cm.plasma(np.linspace(0.2, 0.9, 10))

    axes[0].barh(top10["label"][::-1], top10["total_pnl"][::-1] / 1e6,
                 color=palette[::-1], edgecolor="#0d1117")
    axes[0].set_xlabel("Total PnL ($M)")
    axes[0].set_title("Total PnL")
    axes[0].xaxis.grid(True); axes[0].set_axisbelow(True)

    axes[1].barh(top10["label"][::-1], top10["win_pct"][::-1],
                 color=palette[::-1], edgecolor="#0d1117")
    axes[1].axvline(50, color="#8b949e", linestyle="--", linewidth=1)
    axes[1].set_xlabel("Win Rate (%)")
    axes[1].set_title("Win Rate")
    axes[1].xaxis.grid(True); axes[1].set_axisbelow(True)

    sc = axes[2].scatter(
        top10["trade_count"], top10["win_pct"],
        s=top10["total_pnl"] / 5000,
        c=top10["total_pnl"] / 1e6,
        cmap="plasma", edgecolors="#f0f6fc", linewidth=0.5, alpha=0.85,
    )
    for _, row in top10.iterrows():
        axes[2].annotate(row["label"],
                         (row["trade_count"], row["win_pct"]),
                         textcoords="offset points", xytext=(5, 3),
                         fontsize=7.5, color="#c9d1d9")
    plt.colorbar(sc, ax=axes[2], label="Total PnL ($M)")
    axes[2].set_xlabel("Trade Count")
    axes[2].set_ylabel("Win Rate (%)")
    axes[2].set_title("Volume vs Win Rate\n(bubble = PnL size)")
    axes[2].xaxis.grid(True); axes[2].yaxis.grid(True)
    axes[2].set_axisbelow(True)

    for ax in axes:
        ax.set_facecolor("#161b22")

    plt.tight_layout()
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"   saved → {out}")
    return out


# ── Figure 5 — Trader tier × Sentiment heatmap ───────────────────────────────

def fig5_tier_sentiment_heatmap(closed: pd.DataFrame,
                                out: str = "fig5_tier_sentiment_heatmap.png") -> str:
    print("🎨  Figure 5 — Trader tier × Sentiment heatmap...")

    closed = assign_trader_tiers(closed, top_n=20)
    heatmap_data = (
        closed[closed["Tier"] != "Rest"]
        .groupby(["Tier", "classification"])["Closed PnL"]
        .mean()
        .unstack("classification")
        .reindex(columns=SENTIMENT_ORDER)
    )

    fig, ax = plt.subplots(figsize=(12, 5))
    fig.patch.set_facecolor("#0d1117")
    ax.set_facecolor("#161b22")

    cmap = plt.cm.RdYlGn
    norm = mcolors.TwoSlopeNorm(
        vmin=heatmap_data.values.min(), vcenter=0,
        vmax=heatmap_data.values.max(),
    )
    im = ax.imshow(heatmap_data.values, cmap=cmap, norm=norm, aspect="auto")

    ax.set_xticks(range(len(SENTIMENT_ORDER)))
    ax.set_xticklabels(SENTIMENT_ORDER, fontsize=11)
    ax.set_yticks(range(len(heatmap_data.index)))
    ax.set_yticklabels(heatmap_data.index, fontsize=11)

    for i in range(heatmap_data.shape[0]):
        for j in range(heatmap_data.shape[1]):
            val = heatmap_data.values[i, j]
            if not np.isnan(val):
                ax.text(j, i, f"${val:.0f}", ha="center", va="center",
                        fontsize=11, fontweight="bold",
                        color="black" if abs(val) < heatmap_data.values.max() * 0.6
                        else "white")

    plt.colorbar(im, ax=ax, label="Avg PnL per Trade ($)")
    ax.set_title(
        "Avg PnL per Trade — Top vs Bottom Traders across each Sentiment State\n"
        "(are top traders better at picking *when* to trade?)",
        fontsize=13, fontweight="bold", color="#f0f6fc",
    )
    plt.tight_layout()
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"   saved → {out}")
    return out


# ── Figure 6 — PnL distribution boxplots ─────────────────────────────────────

def fig6_pnl_distribution(closed: pd.DataFrame,
                           out: str = "fig6_pnl_distribution.png") -> str:
    print("🎨  Figure 6 — PnL distribution boxplots...")

    plot_data = [
        closed.loc[closed["classification"] == s, "Closed PnL"]
        .clip(-2000, 2000).values
        for s in SENTIMENT_ORDER
    ]

    fig, ax = plt.subplots(figsize=(14, 7))
    fig.patch.set_facecolor("#0d1117")
    ax.set_facecolor("#161b22")

    bp = ax.boxplot(
        plot_data,
        patch_artist=True,
        medianprops=dict(color="#f0f6fc", linewidth=2),
        whiskerprops=dict(color="#8b949e"),
        capprops=dict(color="#8b949e"),
        flierprops=dict(marker=".", color="#8b949e", alpha=0.3, markersize=3),
        widths=0.5,
    )
    for patch, color in zip(bp["boxes"], _COLORS):
        patch.set_facecolor(color)
        patch.set_alpha(0.75)

    ax.axhline(0, color="#ff7b72", linestyle="--", linewidth=1, alpha=0.7, label="Break-even")
    ax.set_xticks(range(1, 6))
    ax.set_xticklabels(SENTIMENT_ORDER, fontsize=11)
    ax.set_ylabel("Closed PnL per Trade (clipped ±$2,000)")
    ax.set_title(
        "PnL Distribution per Trade — how spread out are outcomes across sentiment?\n"
        "(clipped at ±$2k to reduce outlier distortion)",
        fontsize=13, fontweight="bold", color="#f0f6fc",
    )
    ax.yaxis.grid(True); ax.set_axisbelow(True)
    ax.legend(fontsize=10)

    plt.tight_layout()
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"   saved → {out}")
    return out


# ── Figure 7 — Top coins by PnL ──────────────────────────────────────────────

def fig7_top_coins(closed: pd.DataFrame,
                   out: str = "fig7_top_coins.png") -> str:
    print("🎨  Figure 7 — Top coins by PnL...")

    top_coins   = compute_coin_stats(closed, top_n=10)
    coin_palette = plt.cm.viridis(np.linspace(0.2, 0.9, 10))

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    fig.patch.set_facecolor("#0d1117")
    fig.suptitle("Top 10 Coins — Which assets printed the most?",
                 fontsize=14, fontweight="bold", color="#f0f6fc")

    axes[0].barh(top_coins.index[::-1], top_coins["total_pnl"][::-1] / 1e6,
                 color=coin_palette[::-1], edgecolor="#0d1117")
    axes[0].set_xlabel("Total PnL ($M)")
    axes[0].set_title("Total PnL by Coin")
    axes[0].xaxis.grid(True); axes[0].set_axisbelow(True)

    axes[1].barh(top_coins.index[::-1], top_coins["win_rate"][::-1] * 100,
                 color=coin_palette[::-1], edgecolor="#0d1117")
    axes[1].axvline(50, color="#ff7b72", linestyle="--", linewidth=1)
    axes[1].set_xlabel("Win Rate (%)")
    axes[1].set_title("Win Rate by Coin")
    axes[1].xaxis.grid(True); axes[1].set_axisbelow(True)

    for ax in axes:
        ax.set_facecolor("#161b22")

    plt.tight_layout()
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"   saved → {out}")
    return out


# ── Figure 8 — Contrarian trading insight ────────────────────────────────────

def fig8_contrarian_insight(closed: pd.DataFrame,
                             out: str = "fig8_contrarian_insight.png") -> str:
    print("🎨  Figure 8 — Contrarian trading insight...")

    direction_sentiment = (
        closed[closed["classification"].isin(["Extreme Fear", "Extreme Greed"])]
        .groupby(["classification", "Direction"])["Closed PnL"]
        .agg(["mean", "count"])
        .reset_index()
        .rename(columns={"mean": "avg_pnl", "count": "trades"})
    )
    direction_sentiment = direction_sentiment[direction_sentiment["trades"] >= 50]

    fear_data  = direction_sentiment[direction_sentiment["classification"] == "Extreme Fear"]
    greed_data = direction_sentiment[direction_sentiment["classification"] == "Extreme Greed"]

    fig, ax = plt.subplots(figsize=(14, 7))
    fig.patch.set_facecolor("#0d1117")
    ax.set_facecolor("#161b22")

    x, w = np.arange(len(fear_data)), 0.4
    ax.bar(x - w / 2, fear_data["avg_pnl"].values, w,
           color="#ff4d4f", alpha=0.85, label="Extreme Fear", edgecolor="#0d1117")
    ax.bar(x + w / 2,
           greed_data["avg_pnl"].reindex(fear_data.index).values, w,
           color="#36cfc9", alpha=0.85, label="Extreme Greed", edgecolor="#0d1117")

    ax.axhline(0, color="#8b949e", linewidth=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(fear_data["Direction"].values, rotation=25, ha="right", fontsize=10)
    ax.set_ylabel("Avg PnL per Trade ($)")
    ax.set_title(
        "Extreme Fear vs Extreme Greed — Avg PnL by Trade Direction\n"
        "(the 'buy the fear' narrative: does it actually hold?)",
        fontsize=13, fontweight="bold", color="#f0f6fc",
    )
    ax.yaxis.grid(True); ax.set_axisbelow(True)
    ax.legend(fontsize=11, facecolor="#21262d", edgecolor="#30363d")

    plt.tight_layout()
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"   saved → {out}")
    return out
