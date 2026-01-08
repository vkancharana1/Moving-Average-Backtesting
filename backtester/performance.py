import pandas as pd
import numpy as np
from scipy import stats
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class PerformanceMetrics:
    def __init__(self, portfolio_returns, benchmark_returns=None, risk_free_rate=0.0):
        self.portfolio_returns = portfolio_returns
        self.benchmark_returns = benchmark_returns
        self.risk_free_rate = risk_free_rate
        
    def calculate_metrics(self):
        """Calculate comprehensive performance metrics"""
        metrics = {}
        
        # Total return
        metrics['total_return'] = (self.portfolio_returns + 1).prod() - 1
        
        # Annualized return
        days = len(self.portfolio_returns)
        metrics['annualized_return'] = (1 + metrics['total_return']) ** (252 / days) - 1
        
        # Volatility
        metrics['volatility'] = self.portfolio_returns.std() * np.sqrt(252)
        
        # Sharpe ratio
        excess_returns = self.portfolio_returns - self.risk_free_rate / 252
        metrics['sharpe_ratio'] = excess_returns.mean() / excess_returns.std() * np.sqrt(252)
        
        # Maximum drawdown
        cumulative_returns = (1 + self.portfolio_returns).cumprod()
        peak = cumulative_returns.expanding(min_periods=1).max()
        drawdown = (cumulative_returns - peak) / peak
        metrics['max_drawdown'] = drawdown.min()
        
        # Sortino ratio
        negative_returns = self.portfolio_returns[self.portfolio_returns < 0]
        downside_std = negative_returns.std() * np.sqrt(252)
        metrics['sortino_ratio'] = (metrics['annualized_return'] - self.risk_free_rate) / downside_std
        
        # Alpha and beta if benchmark provided
        if self.benchmark_returns is not None:
            covariance = np.cov(self.portfolio_returns, self.benchmark_returns)[0, 1]
            benchmark_variance = np.var(self.benchmark_returns)
            metrics['beta'] = covariance / benchmark_variance
            metrics['alpha'] = metrics['annualized_return'] - (
                metrics['beta'] * (self.benchmark_returns.mean() * 252)
            )
            
            # Information ratio
            active_returns = self.portfolio_returns - self.benchmark_returns
            metrics['information_ratio'] = (
                active_returns.mean() * np.sqrt(252) / active_returns.std()
            )
        
        # Win rate
        winning_trades = len(self.portfolio_returns[self.portfolio_returns > 0])
        total_trades = len(self.portfolio_returns[self.portfolio_returns != 0])
        metrics['win_rate'] = winning_trades / total_trades if total_trades > 0 else 0
        
        # Profit factor
        gross_profit = self.portfolio_returns[self.portfolio_returns > 0].sum()
        gross_loss = abs(self.portfolio_returns[self.portfolio_returns < 0].sum())
        metrics['profit_factor'] = gross_profit / gross_loss if gross_loss != 0 else float('inf')
        
        return metrics
    
    def generate_report(self):
        """Generate a comprehensive performance report"""
        metrics = self.calculate_metrics()
        
        report = f"""
        PERFORMANCE REPORT
        ==================
        
        Return Metrics:
        - Total Return: {metrics['total_return']:.2%}
        - Annualized Return: {metrics['annualized_return']:.2%}
        
        Risk Metrics:
        - Annualized Volatility: {metrics['volatility']:.2%}
        - Maximum Drawdown: {metrics['max_drawdown']:.2%}
        - Sharpe Ratio: {metrics['sharpe_ratio']:.2f}
        - Sortino Ratio: {metrics['sortino_ratio']:.2f}
        
        """
        
        if self.benchmark_returns is not None:
            report += f"""
        Benchmark Comparison:
        - Alpha: {metrics.get('alpha', 0):.2%}
        - Beta: {metrics.get('beta', 0):.2f}
        - Information Ratio: {metrics.get('information_ratio', 0):.2f}
        
        """
        
        report += f"""
        Trade Metrics:
        - Win Rate: {metrics['win_rate']:.2%}
        - Profit Factor: {metrics['profit_factor']:.2f}
        """
        
        return report

# Test the performance metrics
if __name__ == "__main__":
    # Create sample returns for testing
    np.random.seed(42)
    sample_returns = pd.Series(np.random.normal(0.001, 0.02, 252))
    
    # Create performance metrics
    perf = PerformanceMetrics(sample_returns)
    
    # Calculate metrics
    metrics = perf.calculate_metrics()
    
    # Print metrics
    print("Sample Performance Metrics:")
    for key, value in metrics.items():
        print(f"{key}: {value}")
    
    # Generate report
    print(perf.generate_report())