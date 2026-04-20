# Carnegie Terminal — Carnegie Terminal

A Bloomberg-inspired stock screening and portfolio backtesting tool built with Python and `cmu_graphics`. Screen equities, construct custom portfolios, and run animated backtests with real performance analytics.

Built as a 15-112 term project at Carnegie Mellon University.

---

## Features

**Stock Screener**
- 10 equities across Tech, Semiconductor, Finance, Healthcare, Energy, and Auto
- Sort by any column (Ticker, Name, Sector, P/E, Revenue Growth, Price, Return)
- Filter by sector with one click
- Color-coded returns (green / crimson)

**Portfolio Builder**
- Select up to 10 stocks and manually allocate weights in 10% increments
- Weight validation — Backtest only unlocks at exactly 100% allocation
- Sharpe-maximizing optimizer using backtracking search (up to 5 stocks)

**Backtest Engine**
- Animated equity curve drawn week-by-week from 50 weeks of price data
- Hover crosshair shows exact portfolio value at any week
- Draggable metrics panel with four analytics:
  - Total Return
  - Annualized Volatility
  - Sharpe Ratio (5% risk-free rate)
  - Maximum Drawdown

---

## Project Structure

```
Carnegie Terminal/
├── main.py              # Entry point + all event handlers (onAppStart, mouse events)
├── utils.py             # Shared helpers: distance(), getVolatility()
├── data/
│   └── stocks.py        # Stock class + loadStockData() — no graphics dependency
├── screens/
│   ├── welcome.py       # drawWelcome()
│   ├── screener.py      # drawScreener(), getSortKey()
│   ├── portfolio.py     # drawPortfolio()
│   └── backtest.py      # drawBacktest()
└── logic/
    ├── backtest.py      # runBacktest() — computes equity curve + all metrics
    └── optimizer.py     # optimizeWeights(), optimizeHelper() — backtracking
```

The `data/` and `logic/` layers have no `cmu_graphics` dependency and can be imported and tested independently.

---

## How to Run

1. Install `cmu_graphics`:
```bash
pip install cmu-graphics
```

2. Clone the repo and run from the project root:
```bash
python main.py
```

> **Note:** `cmu_graphics` requires the working directory to be the project root so relative imports resolve correctly.

---

## Implementation Notes

**Backtracking Optimizer** (`logic/optimizer.py`)

`optimizeHelper` performs exhaustive search over all weight allocations in 10% increments that sum to 100%, evaluating each by Sharpe ratio. Complexity is O(C(n+9, 9)) where n is the number of selected stocks — manageable for up to 5 stocks, which is why the Optimize button is gated at that threshold.

**Sharpe Ratio Calculation**

Uses a risk-free rate of 5% annually (≈ 0.096% weekly), annualized by multiplying by √52. Computed over the full 50-week backtest window.

**Equity Curve Animation**

`onStep` increments `backtestStep` by 2 per frame. `drawBacktest` draws only the first `backtestStep` segments, creating the left-to-right animation effect without storing intermediate states.

---

## Stocks Included

| Ticker | Name | Sector |
|--------|------|--------|
| AAPL | Apple | Tech |
| AMZN | Amazon | Tech |
| ASE | ASE Technology | Semiconductor |
| JNJ | Johnson & Johnson | Healthcare |
| JPM | JPMorgan | Finance |
| META | Meta | Tech |
| MSFT | Microsoft | Tech |
| NVDA | Nvidia | Semiconductor |
| TSLA | Tesla | Auto |
| XOM | ExxonMobil | Energy |

Price data covers 50 weeks of weekly closing prices.

---

## Author

Jacob — Carnegie Mellon University, Class of 2028  
Mathematical Sciences (Operations Research & Statistics) | Machine Learning Minor
