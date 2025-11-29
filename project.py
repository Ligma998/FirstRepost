# Portfolio Tracker
import json
import os
from typing import Dict, List, Any
import requests
import time

# Mock API
data_file = "portfolio_data.json"
API_Key = "T8CT1TMFL20Q0G9E"
# base url for Global Quote Endpoint
API_base_url = "https://www.alphavantage.co/query"

def fetch_current_price(ticker:str) -> float | None:
    params = {"function": "GLOBAL_QUOTE",
              "symbol": ticker.upper(),
              "apikey": API_Key}
    
    try:
        response = requests.get(API_base_url, params=params)
        response.raise_for_status()
        data = response.json()
        #Data errors
        if "Error Message" in data:
            print(f"API Error:\nFailed to fetch the price for {ticker}\n{data["Error Message"]}")
            return None
        if "Note" in data and "rate limit" in data["Note"]:
            print("Error:\nRate limit exceeded(5 calls per minute)\nTry again later.")
            return None
        
        #parse the global quote
        global_quote = data.get("Global Quote")
        if global_quote and "05. price" in global_quote:
            price_str = data['Global Quote']['05. price']
            return float(price_str)
        else:
            print(f"API Error:\nPrice data missing for {ticker}")
            return None
        
    except requests.exceptions.RequestException as e:
        print(f"Network Error:\nCould not connect to Alpha Vantage: {e}")
        return None
    except ValueError:
        print(f"Could not convert the {ticker} price string.")
        return None
    except Exception as e:
        print(f"Unexpected error:{e}")
        

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
                print("\nStarting with empty portfolio:")
                self.holdings = []

        else:
            print(f"No data files found: {data_file}")

    def save_holdings(self):
        try:
            with open(data_file, 'w') as f:
                json.dump(self.holdings, f, indent=4)
                print(f"Successfully saved {len(self.holdings)} to {data_file}")
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
        self.save_holdings()

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
            print("\nPortfolio is empty.\nAdd some holdings first.")
            return#to escape from this method
        
        total_current_value = 0.0
        total_investment = 0.0

        print("\n" + "=" * 60)
        print("PORTFOLIO ANALYSIS")
        print("+" * 60)

        # dictionary to aggregate results by ticker
        analysis_summary : Dict[str, Dict[str, Any]] = {}
        # aggregate data and calculate weighted average cost
        for holding in self.holdings:
            ticker = holding['ticker']
            shares = holding['shares']
            purchase_price = holding['purchase_price']
            # fetch with api requests
            current_price = fetch_current_price(ticker)
            if current_price is None:
                print(f"Warning:\nSkipping {ticker} in analysis due to error.")
                continue
            
            investment = shares * purchase_price
            current_value = shares * current_price

            total_investment += investment
            total_current_value += current_value

            if ticker not in analysis_summary:
                analysis_summary[ticker] = {'total_shares': 0.0,
                                            'total_investment':0.0,
                                            'current_price': current_price}
            analysis_summary[ticker]['total_shares'] += shares
            analysis_summary[ticker]['total_investment'] += investment
            
        # print detail summary and calculate P&L
        for ticker, summary in analysis_summary.items():
            #calculate weighted avg cost
            if summary['total_shares'] > 0:
                avg_cost = summary['total_investment'] / summary['total_shares']
            else:
                avg_cost = 0.0
            
            current_price = summary['current_price']
            total_shares = summary['total_shares']
            total_value = total_shares * current_price

            pnl = total_value - summary['total_investment']
            percentage_change = (pnl / summary['total_investment']) * 100 if summary['total_investment'] else 0

            status = "Gain" if pnl >= 0 else "Loss"
            print(f"\n{ticker}:")
            print(f"  Shares:       {total_shares:,.2f}")
            print(f"  Avg Cost:     ${avg_cost:,.2f}")
            print(f"  Current Price:${current_price:,.2f}")
            print(f"  Value:        ${total_value:,.2f}")
            print(f"  P&L ({status}:${pnl:,.2f} ({percentage_change:+.2f}%))")

        # print overall portfolio summary
        overall_pnl = total_current_value - total_investment
        overall_percent = (overall_pnl / total_investment) * 100 if total_investment else 0
        overall_status = "Gain" if overall_pnl >= 0 else "Loss"

        print("\n" + "=" * 60)
        print(f" OVERALL PORTFOLIO VALUE:   ${total_current_value:,.2f}")
        print(f" TOTAL INVESTMENT:          ${total_investment:,.2f}")
        print(f" TOTAL P&L ({overall_status}):  ${overall_pnl:,.2f} ({overall_percent:.2f}%)")
        print("=" * 60 + "\n")

def main_cli():
    # cli entry point for testing manager
    manager = PortfolioManager()

    while True:
        print("\n--- Portfolio Menu ---")
        print("1. Add Holding (e.g. AAPL)")
        print("2. Remove Holding (by ticker)")
        print("3. Analyze Portfolio (Fetch real-time prices)")
        print("4. Exist")
        



        