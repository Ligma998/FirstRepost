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
        if os.path.exists(data_file):
            try:
                with open(data_file, 'r') as f:
                    self.holdings = json.load(f)
                    print(f"Successfully loaded {len(self.holdings)} from {data_file}")

            except (IOError, json.JSONDecodeError) as e:
                print(f"Could not load or parse data file:\nError: {e}")

manager = PortfolioManager()._load_holdings()
