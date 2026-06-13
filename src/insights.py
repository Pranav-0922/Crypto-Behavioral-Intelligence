# -*- coding: utf-8 -*-
"""
insights.py — Print the summary statistics table and key narrative insights.
"""

import pandas as pd
from config import SENTIMENT_ORDER


def print_summary_table(closed: pd.DataFrame) -> None:
    """
    Print a per-sentiment summary: days in market, trade count, total PnL,
    avg PnL per trade, and win rate.
    """
    summary = (
        closed.groupby("classification")
        .agg(
            Days_in_Market    =("date",       "nunique"),
            Total_Trades      =("Closed PnL", "count"),
            Total_PnL         =("Closed PnL", lambda x: f"${x.sum()/1e6:.2f}M"),
            Avg_PnL_per_Trade =("Closed PnL", lambda x: f"${x.mean():.1f}"),
            Win_Rate          =("profitable", lambda x: f"{x.mean()*100:.1f}%"),
        )
        .reindex(SENTIMENT_ORDER)
    )

    print()
    print("=" * 65)
    print("  SUMMARY — Sentiment vs Trader Performance")
    print("=" * 65)
    print(summary.to_string())
    print()


def print_key_insights() -> None:
    """Print the hard-coded narrative key insights."""
    print("=" * 65)
    print("  KEY INSIGHTS")
    print("=" * 65)
    print("""
1. 🟢  Extreme Greed → highest win rate (89.2%) — traders ride
       momentum well when sentiment is euphoric.

2. 🔴  Extreme Fear  → surprisingly decent win rate (76.2%) and
       the highest avg PnL per trade ($71) for BUY orders,
       supporting the classic 'buy the dip' contrarian thesis.

3. 📉  Fear          → best total PnL pool ($3.36M) because it
       covers the most trading days (781), not because each
       trade is more profitable.

4. 💡  Top traders don't just trade more — they have higher win
       rates AND larger avg trades. Quality over quantity.

5. 🪙  @107 and HYPE dominate volume; SOL/ETH lead on avg PnL
       per trade, suggesting fewer but higher-conviction trades.

6. 📅  Dec 2024 – Feb 2025 was a breakout period. PnL spiked
       massively, correlating with the Greed/Extreme Greed wave.
""")


def run_insights(closed: pd.DataFrame) -> None:
    """Run the full insights section: summary table + key takeaways."""
    print_summary_table(closed)
    print_key_insights()
    print("All charts saved as PNG files. Happy analysing! 🚀")
