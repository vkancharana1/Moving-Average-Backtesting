import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from scipy import stats

# Get user input
ticker = input("Enter stock symbol (e.g., MSFT, GOOGL, TSLA): ").strip().upper()
if not ticker:
    ticker = "AAPL"  # Default to Apple

# Configuration - now based on user input
START_DATE = "2020-01-01"
END_DATE = "2023-12-31"
INITIAL_CAPITAL = 10000.0
COMMISSION = 0.001
SHORT_WINDOW = 50
LONG_WINDOW = 200

class SimpleBacktester:
    def __init__(self, ticker):
        self.ticker = ticker
        self.data = None
        self.signals = None
        self.portfolio_values = None
        
    def download_data(self):
        """Download historical data from Yahoo Finance with better error handling"""
        print(f"Downloading data for {self.ticker} from {START_DATE} to {END_DATE}...")
        try:
            # Try using Ticker method which is more reliable
            stock = yf.Ticker(self.ticker)
            data = stock.history(start=START_DATE, end=END_DATE)
            
            if data.empty:
                print(f"Warning: No data returned for {self.ticker}. Trying alternative method...")
                # Fallback to download method
                data = yf.download(self.ticker, start=START_DATE, end=END_DATE, progress=False)
            
            if data.empty:
                raise ValueError(f"No data available for {self.ticker}")
                
            print(f"Successfully downloaded {len(data)} days of data")
            return data
            
        except Exception as e:
            print(f"Error downloading data: {e}")
            return None
    
    def moving_average_strategy(self, data):
        """Generate trading signals using moving average crossover"""
        # Make sure we have data
        if data is None or data.empty:
            print("No data available for strategy")
            return pd.DataFrame()
            
        # Ensure we have the Close column
        if 'Close' not in data.columns:
            print("No 'Close' column in data")
            return pd.DataFrame()
            
        signals = pd.DataFrame(index=data.index)
        signals['price'] = data['Close']
        signals['short_ma'] = data['Close'].rolling(window=SHORT_WINDOW, min_periods=1).mean()
        signals['long_ma'] = data['Close'].rolling(window=LONG_WINDOW, min_periods=1).mean()
        
        # Generate signals
        signals['signal'] = 0
        # Only apply signals where we have enough data for both MAs
        valid_start = max(SHORT_WINDOW, LONG_WINDOW)
        if len(signals) > valid_start:
            signals['signal'].iloc[valid_start:] = np.where(
                signals['short_ma'].iloc[valid_start:] > signals['long_ma'].iloc[valid_start:], 1, 0
            )
        
        # Generate trading orders
        signals['positions'] = signals['signal'].diff()
        
        print(f"Generated {len(signals[signals['positions'] != 0])} trading signals")
        return signals
    
    def run_backtest(self, signals):
        """Run the backtest simulation with better error handling"""
        if signals is None or signals.empty:
            print("No signals to backtest")
            return pd.DataFrame()
            
        portfolio = pd.DataFrame(index=signals.index)
        portfolio['price'] = signals['price']
        portfolio['signal'] = signals['signal']
        portfolio['positions'] = signals['positions']
        
        # Initialize portfolio columns
        portfolio['holdings'] = 0.0
        portfolio['cash'] = INITIAL_CAPITAL
        portfolio['total'] = INITIAL_CAPITAL
        
        # Track shares owned
        shares_owned = 0
        
        # Simulate trades
        trade_count = 0
        for i in range(len(portfolio)):
            current_date = portfolio.index[i]
            price = portfolio['price'].iloc[i]
            signal = portfolio['positions'].iloc[i]
            
            # Skip if price is NaN
            if pd.isna(price):
                continue
                
            # Execute trade if signal indicates
            if signal == 1:  # Buy signal
                # Calculate how many shares we can buy
                shares_to_buy = INITIAL_CAPITAL // price
                if shares_to_buy > 0:
                    cost = shares_to_buy * price * (1 + COMMISSION)
                    
                    # Update portfolio
                    shares_owned += shares_to_buy
                    portfolio.loc[current_date, 'cash'] = portfolio['cash'].iloc[i-1] - cost if i > 0 else INITIAL_CAPITAL - cost
                    trade_count += 1
                
            elif signal == -1:  # Sell signal
                if shares_owned > 0:
                    # Sell all shares
                    revenue = shares_owned * price * (1 - COMMISSION)
                    
                    # Update portfolio
                    portfolio.loc[current_date, 'cash'] = portfolio['cash'].iloc[i-1] + revenue if i > 0 else INITIAL_CAPITAL + revenue
                    shares_owned = 0
                    trade_count += 1
            else:
                # No trade, carry forward cash
                portfolio.loc[current_date, 'cash'] = portfolio['cash'].iloc[i-1] if i > 0 else INITIAL_CAPITAL
            
            # Update holdings and total value
            portfolio.loc[current_date, 'holdings'] = shares_owned * price
            portfolio.loc[current_date, 'total'] = portfolio.loc[current_date, 'cash'] + portfolio.loc[current_date, 'holdings']
        
        print(f"Executed {trade_count} trades during backtest")
        return portfolio
    
    def calculate_performance(self, portfolio):
        """Calculate performance metrics with error handling"""
        if portfolio is None or portfolio.empty:
            return "No portfolio data available for performance calculation"
            
        # Check if we have any data points
        if len(portfolio) == 0:
            return "Portfolio is empty"
            
        # Check if we have the 'total' column and it's not empty
        if 'total' not in portfolio.columns or portfolio['total'].isna().all():
            return "No portfolio value data available"
            
        # Filter out NaN values
        portfolio_clean = portfolio.dropna(subset=['total'])
        if len(portfolio_clean) == 0:
            return "No valid portfolio data after cleaning"
            
        returns = portfolio_clean['total'].pct_change().fillna(0)
        
        # Check if we have valid returns
        if len(returns) == 0:
            return "No valid returns data"
        
        # Total return
        if portfolio_clean['total'].iloc[0] == 0:
            total_return = 0
        else:
            total_return = (portfolio_clean['total'].iloc[-1] / portfolio_clean['total'].iloc[0]) - 1
        
        # Annualized return
        if len(portfolio_clean) > 1:
            days = (portfolio_clean.index[-1] - portfolio_clean.index[0]).days
            if days > 0:
                annualized_return = (1 + total_return) ** (365 / days) - 1
            else:
                annualized_return = 0
        else:
            annualized_return = 0
        
        # Volatility (annualized)
        if len(returns) > 1:
            annualized_volatility = returns.std() * np.sqrt(252)
        else:
            annualized_volatility = 0
        
        # Sharpe ratio (assume 0% risk-free rate)
        if annualized_volatility > 0:
            sharpe_ratio = annualized_return / annualized_volatility
        else:
            sharpe_ratio = 0
        
        # Maximum drawdown
        if len(portfolio_clean) > 0:
            wealth_index = portfolio_clean['total']
            previous_peaks = wealth_index.expanding(min_periods=1).max()
            drawdowns = (wealth_index - previous_peaks) / previous_peaks
            max_drawdown = drawdowns.min() if len(drawdowns) > 0 else 0
        else:
            max_drawdown = 0
        
        # Create performance report
        report = f"""
        PERFORMANCE REPORT
        ==================
        
        Return Metrics:
        - Total Return: {total_return:.2%}
        - Annualized Return: {annualized_return:.2%}
        
        Risk Metrics:
        - Annualized Volatility: {annualized_volatility:.2%}
        - Maximum Drawdown: {max_drawdown:.2%}
        - Sharpe Ratio: {sharpe_ratio:.2f}
        """
        
        return report
    
    def plot_results(self, portfolio, signals):
        """Plot backtest results with error handling"""
        if portfolio is None or portfolio.empty or signals is None or signals.empty:
            print("No data available for plotting")
            return
            
        try:
            fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))
            
            # Plot 1: Price and moving averages
            ax1.plot(signals.index, signals['price'], label='Price', color='black')
            ax1.plot(signals.index, signals['short_ma'], label=f'{SHORT_WINDOW}-Day MA', alpha=0.75)
            ax1.plot(signals.index, signals['long_ma'], label=f'{LONG_WINDOW}-Day MA', alpha=0.75)
            
            # Plot buy and sell signals
            buy_signals = signals[signals['positions'] == 1]
            sell_signals = signals[signals['positions'] == -1]
            
            if not buy_signals.empty:
                ax1.scatter(buy_signals.index, buy_signals['price'], color='green', marker='^', label='Buy', alpha=1, s=100)
            if not sell_signals.empty:
                ax1.scatter(sell_signals.index, sell_signals['price'], color='red', marker='v', label='Sell', alpha=1, s=100)
            
            ax1.set_title(f'{self.ticker} - Price, Moving Averages, and Trading Signals')
            ax1.set_ylabel('Price ($)')
            ax1.legend()
            ax1.grid(True)
            
            # Plot 2: Portfolio value
            ax2.plot(portfolio.index, portfolio['total'], label='Portfolio Value', color='purple')
            ax2.set_title('Portfolio Value Over Time')
            ax2.set_ylabel('Value ($)')
            ax2.legend()
            ax2.grid(True)
            
            # Plot 3: Drawdown
            wealth_index = portfolio['total']
            previous_peaks = wealth_index.expanding(min_periods=1).max()
            drawdowns = (wealth_index - previous_peaks) / previous_peaks
            
            ax3.fill_between(drawdowns.index, drawdowns * 100, 0, alpha=0.3, color='red')
            ax3.plot(drawdowns.index, drawdowns * 100, color='red', alpha=0.8, linewidth=1)
            ax3.set_title('Portfolio Drawdown')
            ax3.set_ylabel('Drawdown (%)')
            ax3.grid(True)
            
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"Error generating plots: {e}")
    
    def run_complete_backtest(self):
        """Run the complete backtest with comprehensive error handling"""
        print(f"Starting Backtest for {self.ticker}...")
        
        # Download data
        data = self.download_data()
        if data is None or data.empty:
            print(f"Failed to download data for {self.ticker}. Please check the ticker symbol and try again.")
            return
        
        # Generate signals
        print("Generating trading signals...")
        signals = self.moving_average_strategy(data)
        if signals.empty:
            print("No trading signals generated. Backtest cannot continue.")
            return
        
        # Run backtest
        print("Running backtest simulation...")
        portfolio = self.run_backtest(signals)
        if portfolio.empty:
            print("Backtest simulation failed. No portfolio data generated.")
            return
        
        # Calculate performance
        print("Calculating performance metrics...")
        report = self.calculate_performance(portfolio)
        
        # Print report
        print(f"\nBACKTEST RESULTS FOR {self.ticker}")
        print("="*50)
        print(report)
        print("="*50)
        
        # Plot results
        print("Generating visualizations...")
        self.plot_results(portfolio, signals)
        
        print("Backtest completed successfully!")

# Run the backtest
if __name__ == "__main__":
    ticker = input("Enter stock symbol (e.g., MSFT, GOOGL, TSLA): ").strip().upper()
    if not ticker:
        ticker = "AAPL"  # Default to Apple
        
    backtester = SimpleBacktester(ticker)
    backtester.run_complete_backtest()