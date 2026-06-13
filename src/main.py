# -*- coding: utf-8 -*-
"""
main.py — Entry point. Orchestrates loading, preprocessing, visualisations,
          and insights in the correct order.

Usage
-----
    python main.py

Both CSV files (fear_greed_index.csv, historical_data.csv) must be in the
same directory as main.py, or their paths must be updated in config.py.
"""

from config import apply_plot_theme
from data_loader import load_all
from visualizations import (
    fig1_overview_dashboard,
    fig2_buy_vs_sell,
    fig3_monthly_trend,
    fig4_top_traders,
    fig5_tier_sentiment_heatmap,
    fig6_pnl_distribution,
    fig7_top_coins,
    fig8_contrarian_insight,
)
from insights import run_insights


def main() -> None:
    # 1. Apply global plot theme before any figure is drawn
    apply_plot_theme()

    # 2. Load and merge data
    merged, closed = load_all()

    # 3. Pull the raw fear/greed frame for charts that need it directly
    from data_loader import load_raw
    fg, _ = load_raw()

    # 4. Generate all figures
    fig1_overview_dashboard(fg, closed)
    fig2_buy_vs_sell(closed)
    fig3_monthly_trend(merged, closed)
    fig4_top_traders(closed)
    fig5_tier_sentiment_heatmap(closed)
    fig6_pnl_distribution(closed)
    fig7_top_coins(closed)
    fig8_contrarian_insight(closed)

    # 5. Print summary and insights
    run_insights(closed)


if __name__ == "__main__":
    main()
