# 📈 Crypto Behavioral Intelligence

### Leveraging Market Psychology to Understand Trading Behavior in Crypto Markets

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge\&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge\&logo=pandas)
![NumPy](https://img.shields.io/badge/NumPy-Scientific%20Computing-013243?style=for-the-badge\&logo=numpy)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-orange?style=for-the-badge)
![EDA](https://img.shields.io/badge/Exploratory%20Data%20Analysis-Advanced-success?style=for-the-badge)
![Web3](https://img.shields.io/badge/Domain-Web3%20Trading-purple?style=for-the-badge)

---

## Executive Summary

Financial markets are driven not only by fundamentals but also by collective investor psychology. In cryptocurrency markets, where volatility and sentiment often dominate decision-making, understanding behavioral patterns can provide a significant trading edge.

This project investigates the relationship between **Bitcoin Market Sentiment (Fear & Greed Index)** and **real-world trader performance data from Hyperliquid**. By combining market sentiment indicators with thousands of executed trades, the analysis uncovers how trader profitability, win rates, asset preferences, and risk-taking behavior change across different emotional market regimes.

The study aims to answer a fundamental question:

> **Do traders perform better when markets are fearful or greedy, and can sentiment be used as a predictive signal for smarter trading decisions?**

---

## Business Objective

The primary objective of this analysis is to identify actionable relationships between market sentiment and trading performance that can support:

* Quantitative trading strategy development
* Risk management optimization
* Market timing decisions
* Behavioral finance research
* Web3 trading intelligence systems

---

## Dataset

Due to GitHub file size limitations, the historical trading dataset is not stored in this repository.

### Download Links

- Historical Trader Data: [[Google Drive Link]](https://drive.google.com/file/d/1IAfLZwu6rJzyWKgBToqwSmmVYU6VbjVs/view?usp=sharing)
- Fear & Greed Index: [[Google Drive Link]](https://drive.google.com/file/d/1PgQC0tO8XN-wqkNyghWc_-mnrYv_nhSf/view?usp=sharing)

After downloading, place the files inside:

```text
data/
│
├── fear_greed_index.csv
└── dataset_links.md
```

---

## Dataset Overview

### 1. Bitcoin Fear & Greed Index

The Fear & Greed Index is a widely used market sentiment indicator that quantifies investor emotions on a scale from 0 to 100.

| Feature        | Description                                       |
| -------------- | ------------------------------------------------- |
| Date           | Observation date                                  |
| Value          | Fear & Greed score (0–100)                        |
| Classification | Extreme Fear, Fear, Neutral, Greed, Extreme Greed |

---

### 2. Hyperliquid Historical Trading Data

A comprehensive dataset containing real trading activity from Hyperliquid traders.

#### Key Attributes

| Feature         | Description               |
| --------------- | ------------------------- |
| Account         | Trader identifier         |
| Symbol/Coin     | Asset traded              |
| Execution Price | Trade execution price     |
| Size            | Position size             |
| Side            | Buy / Sell                |
| Leverage        | Leverage used             |
| Closed PnL      | Realized Profit & Loss    |
| Timestamp       | Trade execution time      |
| Start Position  | Position details          |
| Event Type      | Trading event information |

---

## Analytical Workflow

### Data Preparation

* Cleaned and standardized timestamps
* Processed sentiment classifications
* Filtered closed trades for profitability analysis
* Engineered profitability indicators
* Handled missing and inconsistent values

### Data Integration

Trading records were mapped to daily market sentiment values using timestamp alignment, enabling each trade to be analyzed within its corresponding emotional market context.

### Exploratory Analysis

The study examines:

* Profitability by sentiment regime
* Win-rate variations
* Buy vs Sell behavior
* Top trader characteristics
* Asset-level performance
* Market cycle impacts
* Contrarian trading opportunities

---

## Key Analytical Questions

### Market Sentiment

* How frequently does the market experience each sentiment state?
* Which sentiment regimes generate the highest profitability?

### Trader Performance

* Are traders more successful during Fear or Greed periods?
* Does sentiment affect trade win rates?

### Behavioral Analysis

* Do top-performing traders behave differently than losing traders?
* Are profitable traders more active during specific market conditions?

### Asset Performance

* Which cryptocurrencies generate the strongest returns?
* Does sentiment influence asset-level profitability?

---

## Visualization Suite

The project delivers eight analytical dashboards designed to communicate findings clearly and effectively.

| Figure   | Analysis                                           |
| -------- | -------------------------------------------------- |
| Figure 1 | Market Sentiment & Performance Overview Dashboard  |
| Figure 2 | Buy vs Sell Performance Across Sentiment Regimes   |
| Figure 3 | Monthly Profitability Trend with Sentiment Overlay |
| Figure 4 | Top Trader Performance Deep Dive                   |
| Figure 5 | Top vs Bottom Trader Sentiment Heatmap             |
| Figure 6 | Trade-Level PnL Distribution Analysis              |
| Figure 7 | Top Performing Cryptocurrency Assets               |
| Figure 8 | Contrarian Strategy Evaluation (Fear vs Greed)     |

---

## Major Insights

### 1. Market Euphoria Drives Consistent Wins

Periods classified as **Greed** and **Extreme Greed** exhibit the highest trader win rates, indicating that momentum-based strategies perform exceptionally well in bullish market environments.

---

### 2. Fear Creates High-Reward Opportunities

Although trading activity declines during fearful conditions, average profitability per trade often increases, supporting the effectiveness of selective contrarian strategies.

---

### 3. Sentiment Influences Trading Outcomes

Clear variations in profitability and trade success rates are observed across sentiment regimes, suggesting that market psychology has a measurable impact on trader performance.

---

### 4. Top Traders Demonstrate Superior Market Timing

High-performing traders consistently outperform their peers by:

* Maintaining stronger win rates
* Selecting higher-quality opportunities
* Avoiding excessive overtrading

---

### 5. Asset Selection Remains Critical

While sentiment affects overall market behavior, asset-specific performance differences remain significant, emphasizing the importance of combining sentiment analysis with asset selection.

---

### 6. Bull Market Phases Generate Disproportionate Returns

Periods of elevated optimism correspond with substantial increases in aggregate trader profitability, highlighting the importance of market regime awareness.

---

## Strategic Recommendations

### For Retail & Professional Traders

✔ Incorporate market sentiment into trade planning

✔ Increase conviction during high-probability sentiment regimes

✔ Identify oversold opportunities during Extreme Fear conditions

✔ Use sentiment as a complementary signal rather than a standalone indicator

---

### For Quantitative Research Teams

✔ Integrate Fear & Greed Index values into alpha-generation models

✔ Build sentiment-aware position sizing frameworks

✔ Enhance risk-adjusted return models with behavioral signals

✔ Develop regime-switching trading strategies

---

## Project Architecture

```text
bitcoin-sentiment-trader-analysis/
│
├── README.md
├── analysis.ipynb
│
├── data/
│   ├── fear_greed_index.csv
│   └── historical_data.csv
│
├── figures/
│   ├── fig1_overview_dashboard.png
│   ├── fig2_buy_vs_sell.png
│   ├── fig3_monthly_trend.png
│   ├── fig4_top_traders.png
│   ├── fig5_tier_sentiment_heatmap.png
│   ├── fig6_pnl_distribution.png
│   ├── fig7_top_coins.png
│   └── fig8_contrarian_insight.png
│
├── src/
│   └── analysis.py
│
└── requirements.txt
```

---

## Technology Stack

| Category                | Tools                                        |
| ----------------------- | -------------------------------------------- |
| Programming             | Python                                       |
| Data Processing         | Pandas, NumPy                                |
| Visualization           | Matplotlib                                   |
| Development Environment | Jupyter Notebook                             |
| Domain                  | Cryptocurrency Analytics, Behavioral Finance |

---

## Potential Future Enhancements

* Predictive Machine Learning Models for Trade Profitability
* Sentiment-Based Trading Signal Generation
* Strategy Backtesting Framework
* Risk-Adjusted Performance Evaluation
* Interactive Dashboard using Streamlit
* Real-Time Sentiment Monitoring Pipeline
* Portfolio Optimization using Market Sentiment

---

## Results & Impact

This analysis demonstrates that market sentiment is not merely a psychological indicator but a measurable factor associated with trading performance. By integrating behavioral signals with trading data, market participants can gain deeper insights into market regimes and make more informed trading decisions.

The findings provide a foundation for developing sentiment-aware quantitative trading systems and advanced market intelligence solutions.


                                                  --------------------------
