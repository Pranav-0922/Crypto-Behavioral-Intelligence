# -*- coding: utf-8 -*-
"""
preprocessing.py — Feature engineering: monthly aggregations, trader tiers,
                   and other derived columns consumed by visualisations.
"""

import numpy as np
import pandas as pd
from config import SENTIMENT_ORDER


# ── Generic helper ───────────────────────────────────────────────────────────

def sentiment_grouped(df: pd.DataFrame, col: str, agg) -> pd.Series:
    """
    Group *df* by 'classification', aggregate *col* with *agg*, and reindex
    to SENTIMENT_ORDER so every chart has the same x-axis order.
    """
    return (
        df.groupby("classification")[col]
        .agg(agg)
        .reindex(SENTIMENT_ORDER)
    )


# ── Monthly features ─────────────────────────────────────────────────────────

def add_month_column(df: pd.DataFrame) -> pd.DataFrame:
    """Add a 'month' Period column derived from 'Timestamp IST'."""
    df = df.copy()
    df["month"] = pd.to_datetime(
        df["Timestamp IST"], format="%d-%m-%Y %H:%M", errors="coerce"
    ).dt.to_period("M")
    return df


def monthly_pnl(closed: pd.DataFrame) -> pd.Series:
    """
    Return a Series of total Closed PnL per calendar month, indexed by
    Timestamp (first day of each month).
    """
    closed = add_month_column(closed)
    series = closed.groupby("month")["Closed PnL"].sum()
    series.index = series.index.to_timestamp()
    return series


def monthly_fear_greed(merged: pd.DataFrame) -> pd.Series:
    """
    Return a Series of average Fear/Greed index value per calendar month,
    indexed by Timestamp (first day of each month).
    """
    merged = merged.copy()
    merged["month_ts"] = pd.to_datetime(
        merged["Timestamp IST"], format="%d-%m-%Y %H:%M", errors="coerce"
    ).dt.to_period("M").dt.to_timestamp()
    return merged.groupby("month_ts")["value"].mean()


# ── Trader tiers ─────────────────────────────────────────────────────────────

def assign_trader_tiers(closed: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    """
    Label each trade row with the tier of its trader:
        • 'Top N Traders'    — accounts in the top-N by total PnL
        • 'Bottom N Traders' — accounts in the bottom-N by total PnL
        • 'Rest'             — everyone else

    Parameters
    ----------
    closed  : closed-trades DataFrame (must have 'Account' and 'Closed PnL').
    top_n   : how many accounts to include in each extreme tier (default 20).
    """
    trader_pnl = closed.groupby("Account")["Closed PnL"].sum()
    top_accounts    = trader_pnl.nlargest(top_n).index
    bottom_accounts = trader_pnl.nsmallest(top_n).index

    closed = closed.copy()
    closed["Tier"] = np.where(
        closed["Account"].isin(top_accounts),
        f"Top {top_n} Traders",
        np.where(
            closed["Account"].isin(bottom_accounts),
            f"Bottom {top_n} Traders",
            "Rest",
        ),
    )
    return closed


# ── Trader-level stats ───────────────────────────────────────────────────────

def compute_trader_stats(closed: pd.DataFrame) -> pd.DataFrame:
    """
    Compute per-account summary statistics (total PnL, avg PnL, trade count,
    win rate) sorted descending by total PnL.
    """
    return (
        closed.groupby("Account")
        .agg(
            total_pnl   =("Closed PnL", "sum"),
            avg_pnl     =("Closed PnL", "mean"),
            trade_count =("Closed PnL", "count"),
            win_rate    =("profitable",  "mean"),
        )
        .sort_values("total_pnl", ascending=False)
    )


# ── Coin-level stats ─────────────────────────────────────────────────────────

def compute_coin_stats(closed: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Return the top-N coins by total PnL, with win rate and trade count.
    """
    return (
        closed.groupby("Coin")
        .agg(
            total_pnl=("Closed PnL", "sum"),
            win_rate =("profitable",  "mean"),
            count    =("Closed PnL", "count"),
        )
        .sort_values("total_pnl", ascending=False)
        .head(top_n)
    )
