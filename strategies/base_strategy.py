from abc import ABC, abstractmethod
import pandas as pd

class Strategy(ABC):
    def __init__(self, data, parameters=None):
        self.data = data
        self.parameters = parameters or {}
        self.signals = None
        
    @abstractmethod
    def generate_signals(self):
        """Generate trading signals based on strategy logic"""
        pass
    
    def get_signals(self):
        """Return generated signals"""
        if self.signals is None:
            self.generate_signals()
        return self.signals