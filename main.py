import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class Visualizations:
    def __init__(self, backtest_results):
        self.results = backtest_results
        
    def plot_equity_curve(self):
        """Plot portfolio equity curve"""
        portfolio_values = self.results['portfolio'].holdings['total']
        
        plt.figure(figsize=(12, 6))
        plt.plot(portfolio_values.index, portfolio_values, label='Portfolio Value', color='blue')
        plt.title('Portfolio Equity Curve')
        plt.xlabel('Date')
        plt.ylabel('Portfolio Value ($)')
        plt.legend()
        plt.grid(True)
        plt.show()
    
    def plot_drawdown(self):
        """Plot portfolio drawdown"""
        portfolio_values = self.results['portfolio'].holdings['total']
        cumulative_returns = (portfolio_values / portfolio_values.iloc[0]) - 1
        peak = cumulative_returns.expanding(min_periods=1).max()
        drawdown = (cumulative_returns - peak) / peak
        
        plt.figure(figsize=(12, 6))
        plt.fill_between(drawdown.index, drawdown * 100, 0, alpha=0.3, color='red')
        plt.plot(drawdown.index, drawdown * 100, color='red', alpha=0.8, linewidth=1)
        plt.title('Portfolio Drawdown')
        plt.xlabel('Date')
        plt.ylabel('Drawdown (%)')
        plt.grid(True)
        plt.show()
    
    def plot_signals(self):
        """Plot trading signals with price data"""
        signals = self.results['signals']
        
        plt.figure(figsize=(12, 8))
        
        # Plot price and moving averages
        plt.subplot(2, 1, 1)
        plt.plot(signals.index, signals['price'], label='Price', color='black')
        if 'short_mavg' in signals.columns:
            plt.plot(signals.index, signals['short_mavg'], label=f"Short MA", alpha=0.75)
        if 'long_mavg' in signals.columns:
            plt.plot(signals.index, signals['long_mavg'], label=f"Long MA", alpha=0.75)
        
        # Plot buy and sell signals
        buy_signals = signals[signals['positions'] > 0]
        sell_signals = signals[signals['positions'] < 0]
        
        if not buy_signals.empty:
            plt.scatter(buy_signals.index, buy_signals['price'], color='green', marker='^', label='Buy', alpha=1, s=100)
        if not sell_signals.empty:
            plt.scatter(sell_signals.index, sell_signals['price'], color='red', marker='v', label='Sell', alpha=1, s=100)
            
        plt.title('Price, Moving Averages, and Trading Signals')
        plt.ylabel('Price ($)')
        plt.legend()
        plt.grid(True)
        
        # Plot signal values
        plt.subplot(2, 1, 2)
        plt.plot(signals.index, signals['signal'], label='Signal', drawstyle='steps-post', color='purple')
        plt.title('Trading Signal Over Time')
        plt.xlabel('Date')
        plt.ylabel('Signal (1=Buy, 0=Sell)')
        plt.legend()
        plt.grid(True)
        
        plt.tight_layout()
        plt.show()