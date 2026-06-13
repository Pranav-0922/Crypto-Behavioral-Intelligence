# -*- coding: utf-8 -*-
"""
data_loader.py — Load raw CSVs and produce the merged / closed DataFrames.
"""

import pandas as pd
from config import FEAR_GREED_CSV, HISTORICAL_CSV


def load_raw() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load the fear/greed index and historical trade data from CSV.

    Returns
    -------
    fg : pd.DataFrame   — Fear & Greed index with a parsed 'date' column.
    hd : pd.DataFrame   — Historical trades with a parsed 'date' column.
    """
    fg = pd.read_csv(FEAR_GREED_CSV)
    hd = pd.read_csv(HISTORICAL_CSV)

    fg["date"] = pd.to_datetime(fg["date"])
    hd["date"] = pd.to_datetime(
        hd["Timestamp IST"], format="%d-%m-%Y %H:%M", errors="coerce"
    ).dt.normalize()

    return fg, hd


def build_merged(fg: pd.DataFrame, hd: pd.DataFrame) -> pd.DataFrame:
    """
    Left-join historical trades with the fear/greed index on date.

    Returns
    -------
    merged : pd.DataFrame   — All trades enriched with 'value' and
                               'classification' from the fear/greed index.
    """
    merged = hd.merge(
        fg[["date", "value", "classification"]],
        on="date",
        how="left",
    )
    return merged


def build_closed(merged: pd.DataFrame) -> pd.DataFrame:
    """
    Filter merged trades to closed positions (Closed PnL != 0) and add a
    boolean 'profitable' column.

    Returns
    -------
    closed : pd.DataFrame
    """
    closed = merged[merged["Closed PnL"] != 0].copy()
    closed["profitable"] = closed["Closed PnL"] > 0
    return closed


def load_all() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Convenience wrapper: load CSVs → merge → filter closed trades.

    Returns
    -------
    merged : pd.DataFrame
    closed : pd.DataFrame
    """
    print("📂  Loading datasets...")
    fg, hd = load_raw()
    merged = build_merged(fg, hd)
    closed = build_closed(merged)

    print(f"✅  Total trades      : {len(merged):,}")
    print(f"✅  Closed positions  : {len(closed):,}")
    print(f"✅  Unique traders    : {merged['Account'].nunique():,}")
    print(f"✅  Sentiment coverage: {merged['classification'].notna().mean()*100:.1f}%")
    print()

    return merged, closed
