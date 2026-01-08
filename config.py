 # Configuration settings for the backtesting project

# Data settings
TICKER = "MSFT"  # The stock to analyze
START_DATE = "2020-01-01"  # Start date for historical data
END_DATE = "2023-12-31"    # End date for historical data
DATA_PATH = f"data/historical_data_{TICKER}.csv"  # Path to store/load data

# Strategy parameters
SHORT_WINDOW = 50   # Short moving average window
LONG_WINDOW = 200   # Long moving average window

# Backtest parameters
INITIAL_CAPITAL = 10000.0  # Starting capital
COMMISSION = 0.001         # Trading commission (0.1%)