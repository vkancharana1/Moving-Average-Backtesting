import pandas as pd
import numpy as np
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import INITIAL_CAPITAL, COMMISSION

class Portfolio:
    def __init__(self, initial_capital=INITIAL_CAPITAL):
        self.initial_capital = initial_capital
        self.positions = pd.DataFrame(columns=['shares'])
        self.cash = initial_capital
        self.holdings = pd.DataFrame()
        self.trades = pd.DataFrame(columns=['date', 'type', 'price', 'shares', 'value', 'cash_after'])
        
    def initialize_portfolio(self, index):
        """Initialize portfolio with cash only"""
        self.holdings = pd.DataFrame(index=index)
        self.holdings['cash'] = self.initial_capital
        self.holdings['holdings'] = 0.0
        self.holdings['total'] = self.initial_capital
        
    def update_portfolio(self, date, price, signal, position_size=1.0):
        """Update portfolio based on trading signals"""
        # Calculate position value
        position_value = position_size * price
        
        # Execute trade if signal indicates
        if signal != 0:
            # Calculate commission cost
            commission_cost = position_value * COMMISSION
            
            # Update cash (including commission)
            self.cash -= (position_value * signal) + commission_cost
            
            # Update positions
            if date not in self.positions.index:
                self.positions.loc[date] = {'shares': signal * position_size}
            else:
                self.positions.loc[date, 'shares'] += signal * position_size
        
        # Update holdings
        current_shares = self.positions['shares'].sum() if not self.positions.empty else 0
        self.holdings.loc[date, 'holdings'] = current_shares * price
        self.holdings.loc[date, 'cash'] = self.cash
        self.holdings.loc[date, 'total'] = self.holdings.loc[date, 'holdings'] + self.cash
        
        # Record trade
        if signal != 0:
            trade_record = {
                'date': date,
                'type': 'BUY' if signal > 0 else 'SELL',
                'price': price,
                'shares': position_size,
                'value': position_value,
                'cash_after': self.cash
            }
            self.trades = pd.concat([self.trades, pd.DataFrame([trade_record])], ignore_index=True)

# Test the portfolio
if __name__ == "__main__":
    # Create a simple test
    portfolio = Portfolio(initial_capital=10000)
    
    # Test dates and prices
    test_dates = pd.date_range('2023-01-01', periods=3)
    test_prices = [100, 105, 110]
    
    # Initialize portfolio
    portfolio.initialize_portfolio(test_dates)
    
    # Simulate some trades
    portfolio.update_portfolio(test_dates[0], test_prices[0], 1)  # Buy 1 share
    portfolio.update_portfolio(test_dates[1], test_prices[1], 0)  # Hold
    portfolio.update_portfolio(test_dates[2], test_prices[2], -1)  # Sell 1 share
    
    print("Portfolio Holdings:")
    print(portfolio.holdings)
    print("\nTrade History:")
    print(portfolio.trades)