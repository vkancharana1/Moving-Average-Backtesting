import pandas as pd
import numpy as np
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from the same directory
from portfolio import Portfolio
from performance import PerformanceMetrics

class Backtester:
    def __init__(self, data, strategy, initial_capital=10000.0, commission=0.001):
        self.data = data
        self.strategy = strategy
        self.initial_capital = initial_capital
        self.commission = commission
        self.portfolio = Portfolio(initial_capital)
        self.performance = None
        
    def run_backtest(self):
        """Run the backtest simulation"""
        # Generate trading signals
        signals = self.strategy.generate_signals()
        
        # Initialize portfolio
        self.portfolio.initialize_portfolio(signals.index)
        
        # Execute trades based on signals
        for date, row in signals.iterrows():
            price = row['price']
            signal = row['positions']
            
            # Update portfolio
            self.portfolio.update_portfolio(date, price, signal)
        
        # Calculate returns
        portfolio_values = self.portfolio.holdings['total']
        returns = portfolio_values.pct_change().fillna(0)
        
        # Calculate performance metrics
        self.performance = PerformanceMetrics(returns)
        
        return {
            'signals': signals,
            'portfolio': self.portfolio,
            'performance': self.performance
        }
    
    def get_performance_report(self):
        """Get performance report"""
        if self.performance is None:
            self.run_backtest()
        
        return self.performance.generate_report()
    
    def optimize_parameters(self, parameter_grid):
        """Optimize strategy parameters using grid search"""
        best_params = None
        best_performance = -float('inf')
        results = []
        
        # Generate all parameter combinations
        from itertools import product
        param_names = list(parameter_grid.keys())
        param_values = list(parameter_grid.values())
        
        for combination in product(*param_values):
            params = dict(zip(param_names, combination))
            
            # Update strategy with new parameters
            self.strategy.parameters.update(params)
            
            # Run backtest
            self.run_backtest()
            performance = self.performance.calculate_metrics()
            
            # Use Sharpe ratio as optimization criterion
            performance_score = performance['sharpe_ratio']
            
            results.append({
                'params': params,
                'performance': performance,
                'score': performance_score
            })
            
            if performance_score > best_performance:
                best_performance = performance_score
                best_params = params
        
        return {
            'best_params': best_params,
            'best_performance': best_performance,
            'all_results': results
        }

# Test the backtester
if __name__ == "__main__":
    # Import necessary modules
    from data.data_loader import DataLoader
    from strategies.moving_average_crossover import MovingAverageCrossover
    
    # Load data
    loader = DataLoader()
    data = loader.load_data()
    
    # Create strategy
    strategy = MovingAverageCrossover(data)
    
    # Create backtester
    backtester = Backtester(data, strategy)
    
    # Run backtest
    results = backtester.run_backtest()
    
    # Print performance report
    print(backtester.get_performance_report())