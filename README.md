# 📈 Systematic Trading Strategy Backtesting Framework

## 📌 Project Overview

This project is a **modular Python-based backtesting framework** designed to evaluate **systematic trading strategies** on historical market data.

It provides:

* A **clean separation of concerns** (data, strategy, portfolio, execution, performance)
* A **strategy-agnostic architecture** for easy extensibility
* Realistic portfolio accounting with **transaction costs**
* Institutional-grade **performance metrics**
* Visualization tools for **equity curves, drawdowns, and signals**

The framework currently implements and evaluates a **Moving Average Crossover strategy**, but is fully extensible to additional strategies and asset classes.

---

## 🎯 Objectives

* Design a **production-style backtesting engine**
* Simulate realistic trade execution and portfolio evolution
* Evaluate strategies using **risk-adjusted performance metrics**
* Enable **parameter optimization**
* Provide reusable infrastructure for future quantitative strategies

---

## 🧠 Core Quant Concepts Covered

* Event-driven backtesting
* Signal generation & position management
* Portfolio accounting with commissions
* Risk-adjusted performance evaluation
* Drawdown and tail-risk analysis
* Strategy parameter optimization

---

## 🛠️ Technologies & Tools

* **Python**
* **Pandas & NumPy** – time-series & portfolio calculations
* **yFinance** – historical market data
* **Matplotlib & Seaborn** – visualization
* **SciPy** – statistical analysis
* **Object-Oriented Design (OOP)**

---

## 📂 Project Structure

```
Backtesting-Framework/
│
├── backtester/
│   ├── backtester.py          # Core backtesting engine
│   ├── portfolio.py           # Portfolio & trade execution logic
│   ├── performance.py         # Performance & risk metrics
│
├── data/
│   └── data_loader.py         # Market data download & loading
│
├── strategies/
│   ├── base_strategy.py       # Abstract strategy interface
│   └── moving_average_crossover.py
│
├── utils/
│   └── visualizations.py      # Equity curve, drawdown & signal plots
│
├── config.py                  # Global configuration parameters
├── backtestfile.py            # Standalone interactive backtest script
└── README.md
```

---

## ⚙️ Architecture Overview

### 1️⃣ Data Layer

* Downloads historical price data from **Yahoo Finance**
* Automatically caches data locally
* Ensures numeric consistency and clean indexing

### 2️⃣ Strategy Layer

* Abstract base class enforces a **standard signal interface**
* Strategies output:

  * Price
  * Indicators
  * Trading signals
  * Position changes

### 3️⃣ Execution & Portfolio Layer

* Simulates:

  * Buy / Sell execution
  * Cash management
  * Position tracking
  * Commission costs
* Maintains full trade history and portfolio value

### 4️⃣ Performance Layer

Calculates professional-grade metrics:

* Total & annualized returns
* Volatility
* Sharpe & Sortino ratios
* Maximum drawdown
* Win rate
* Profit factor
* Alpha, Beta & Information Ratio (if benchmark provided)

### 5️⃣ Visualization Layer

* Equity curve
* Drawdown profile
* Price + indicators + trade signals

---

## 📊 Implemented Strategy: Moving Average Crossover

**Logic**

* Buy when short-term MA crosses above long-term MA
* Sell when short-term MA crosses below long-term MA

**Default Parameters**

* Short window: 50 days
* Long window: 200 days

Fully configurable via `config.py` or parameter optimization.

---

## 🔍 Backtesting & Optimization

* Event-driven simulation over historical data
* Supports **grid search parameter optimization**
* Optimization criterion: **Sharpe Ratio**
* Easily extensible to walk-forward or rolling-window analysis

---

## ▶️ How to Run the Project

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/Backtesting-Framework.git
cd Backtesting-Framework
```

### 2️⃣ Install Dependencies

```bash
pip install pandas numpy matplotlib seaborn scipy yfinance
```

### 3️⃣ Run Modular Backtest

```bash
python backtester/backtester.py
```

### 4️⃣ Run Standalone Interactive Backtest

```bash
python simple_backtest.py
```

You’ll be prompted to enter a stock ticker (e.g., `AAPL`, `MSFT`, `GOOGL`).

---

## 📈 Outputs Generated

* Portfolio equity curve
* Drawdown chart
* Buy/Sell signal visualization
* Detailed performance report printed to console

---

## 📚 What I Learned

* Designing **scalable quantitative research infrastructure**
* Translating trading logic into **systematic rules**
* Portfolio-level risk measurement
* Importance of transaction costs in strategy performance
* Clean abstraction between strategy and execution layers

---

## 🔧 Possible Improvements

* Add multi-asset portfolio support
* Implement position sizing & leverage models
* Introduce stop-loss / take-profit logic
* Add walk-forward & Monte Carlo simulations
* Support intraday data & higher-frequency strategies
* Integrate factor-based and statistical arbitrage strategies

---
