import requests
import json

def get_live_nepse_data():
    """
    Fetches live NEPSE data from the Nepselytics API.
    """
    url = "https://nepselytics-6d61dea19f30.herokuapp.com/api/nepselytics/live-nepse"
    
    try:
        print(f"Fetching data from {url}...")
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        data = response.json()
        
        if data.get("success"):
            return data.get("data", [])
        else:
            print("API returned success: False")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching data: {e}")
        return []

def display_stock_summary(stocks, limit=10):
    """
    Displays a summary of the first few stocks from the data.
    """
    if not stocks:
        print("No stock data to display.")
        return

    print("\n" + "="*80)
    print(f"{'Symbol':<10} | {'Name':<35} | {'LTP':>10} | {'Change':>10}")
    print("-" * 80)
    
    for stock in stocks[:limit]:
        symbol = stock.get("symbol", "N/A")
        name = stock.get("securityName", "N/A")
        ltp = stock.get("lastTradedPrice", 0.0)
        change = stock.get("percentageChange", 0.0)
        
        # Trim name if too long
        if len(name) > 33:
            name = name[:30] + "..."
            
        print(f"{symbol:<10} | {name:<35} | {ltp:>10.2f} | {change:>9.2f}%")
    
    print("="*80)
    print(f"Total stocks fetched: {len(stocks)}")

if __name__ == "__main__":
    live_data = get_live_nepse_data()
    
    if live_data:
        display_stock_summary(live_data)
        
        # Example: Save to a JSON file
        # with open('nepse_live_data.json', 'w') as f:
        #     json.dump(live_data, f, indent=4)
        # print("\nData saved to nepse_live_data.json")
