# Portfolio Tracker
import json
import os
from typing import Dict, List, Any

# Mock API
data_file = "portfolio_data.json"

def fetch_current_price(ticker:str) -> float:
    if ticker.upper() == "AAPL":
        return 190.50
    if ticker.upper() == "TSLA":
        return 240.50
    if ticker.upper() == "GOOG":
        return 140.50
    if ticker.upper() == "BTC":
        return 37000.00
    if ticker.upper() == "ETH":
        return 2025.00
    # fall back price
    return 100.00

class PortfolioManager:
    def __init__(self):
        self.holdings: List[Dict[str, Any]] = []
        self._load_holdings()

    def _load_holdings(self):
        print("we get to here")
        if os.path.exists(data_file):
            try:
                with open(data_file, 'r') as f:
                    self.holdings = json.load(f)
                    print(f"Successfully loaded {len(self.holdings)} from {data_file}")

            except (IOError, json.JSONDecodeError) as e:
                print(f"Could not load or parse data file:\nError: {e}")
                print("\nStarting with empty portfolio:")
                self.holdings = []

        else:
            print(f"No data files found: {data_file}")

    def save_holdings(self):
        try:
            with open(data_file, 'w') as f:
                json.dump(self.holdings, f, indent=4)
                print(f"Successfully added {len(self.holdings)} to {data_file}")
        except IOError as e:
            print(f"Could not save data file.\nError: {e}")

    def add_holdings(self, ticker: str, 
                     shares: float, 
                     purchase_price: float, 
                     purchase_date: str):
        new_holdings = {'ticker': ticker.upper(),
                        'shares': shares,
                        'purchase_price':purchase_price,
                        'purchase_date': purchase_date}
        self.holdings.append(new_holdings)

    def remove_holdings(self, ticker: str):
        # removes all if given ticker is the same as saved one
        initial_count = len(self.holdings)
        self.holdings = [h for h in self.holdings if h['ticker'] != ticker.upper()]
        removed_count = initial_count - len(self.holdings)

        if removed_count > 0:
            print(f"Removed {removed_count} entries for {ticker.upper()}")
            self.save_holdings()# save the empty holdings to data_file
        else:
            print(f"No holdings found for {ticker.upper()}.\nNothing's removed.")

    def analyze_portfolio(self):
        if not self.holdings:
            print("\nPortfolio is empty.\nAdd something first.")
            return#to escape from this method
        
        total_current_value = 0.0
        total_investment = 0.0

        print("\n" + "=" * 60)
        print("PORTFOLIO ANALYSIS")
        print("+" * 60)

        # dictionary to aggregate results by ticker
        analysis_summary : Dict[str, Dict[str, Any]] = {}
        for holding in self.holdings:
            ticker = holding['ticker']
            shares = holding['shares']
            purchase_price = holding['purchase_price']

        