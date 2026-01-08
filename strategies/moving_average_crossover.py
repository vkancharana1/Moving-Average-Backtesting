import pandas as pd
import numpy as np
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strategies.base_strategy import Strategy
from config import SHORT_WINDOW, LONG_WINDOW

class MovingAverageCrossover(Strategy):
    def __init__(self, data, short_window=SHORT_WINDOW, long_window=LONG_WINDOW):
        parameters = {
            'short_window': short_window,
            'long_window': long_window
        }
        super().__init__(data, parameters)
        
    def generate_signals(self):
        short_window = self.parameters['short_window']
        long_window = self.parameters['long_window']
    
    # Ensure we have the Close column
        if 'Close' not in self.data.columns:    
        # Try to find a similar column
            close_col = [col for col in self.data.columns if 'close' in col.lower()][0]
            close_data = self.data[close_col]
        else:
            close_data = self.data['Close']
    
         # Calculate moving averages
        signals = pd.DataFrame(index=self.data.index)
        signals['price'] = close_data
        signals['short_mavg'] = close_data.rolling(window=short_window, min_periods=1).mean()
        signals['long_mavg'] = close_data.rolling(window=long_window, min_periods=1).mean()
    
        # Generate signals
        signals['signal'] = 0.0
    
        # Only calculate signals where we have enough data
        if len(signals) > short_window:
            signals['signal'].iloc[short_window:] = np.where(
            signals['short_mavg'].iloc[short_window:] > signals['long_mavg'].iloc[short_window:], 
            1.0, 
            0.0
            )
    
         # Generate trading orders
        signals['positions'] = signals['signal'].diff()
    
        self.signals = signals
        return signals