import pandas as pd
import yfinance as yf
import os
import sys

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import TICKER, START_DATE, END_DATE, DATA_PATH

class DataLoader:
    def __init__(self, ticker=TICKER, start_date=START_DATE, end_date=END_DATE):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.data_path = f"data/historical_data_{self.ticker}.csv"
        self.data = None
        
    def download_data(self):
        """Download historical data from Yahoo Finance"""
        print(f"Downloading data for {self.ticker} from {self.start_date} to {self.end_date}...")
        data = yf.download(self.ticker, start=self.start_date, end=self.end_date)
        
        # Save to CSV
        os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
        data.to_csv(self.data_path)
        print(f"Data saved to {self.data_path}")
        
        return data
    
    def load_data(self):
        """Load historical data from CSV"""
        if not os.path.exists(self.data_path):
            print("Data file not found. Downloading data...")
            return self.download_data()
        
        print(f"Loading data from {self.data_path}...")
        data = pd.read_csv(self.data_path, index_col=0, parse_dates=True)
        
        # Ensure all columns are numeric
        for col in data.columns:
            data[col] = pd.to_numeric(data[col], errors='coerce')
            
        return data