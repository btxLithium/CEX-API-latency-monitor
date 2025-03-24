"""
OKX API Latency Testing Module
"""
import requests
import time
import json
import os
import pytest
from datetime import datetime, timezone, timedelta

# Define data directory
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
os.makedirs(DATA_DIR, exist_ok=True)
LOG_FILE = os.path.join(DATA_DIR, 'okx_latency_data.json')

def measure_api_latency(endpoint_key=None):
    """
    Measure API latency for OKX exchange and endpoint
    
    Args:
        endpoint_key (str, optional): Specific endpoint to test. 
                                     Defaults to None, which uses the default endpoint.
    
    Returns:
        tuple: (success, latency_ms or error_message)
    """
    # OKX specific API endpoints
    API_ENDPOINTS = {
        'market_data': "https://www.okx.com/api/v5/market/ticker?instId=BTC-USDT",
        'book': "https://www.okx.com/api/v5/market/books?instId=BTC-USDT",
        'trades': "https://www.okx.com/api/v5/market/trades?instId=BTC-USDT"
    }
    
    # If no endpoint specified, use the default market data endpoint
    if endpoint_key is None:
        endpoint_key = 'market_data'
    
    if endpoint_key not in API_ENDPOINTS:
        return False, f"Endpoint '{endpoint_key}' not found for OKX"
    
    url = API_ENDPOINTS[endpoint_key]
    
    # Get settings
    timeout = 5  # Example timeout
    retries = 3  # Example retry count
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    num_requests = 5  # Example number of requests
    
    headers = {
        'User-Agent': user_agent,
    }
    
    # Make multiple requests and average the latency
    latencies = []
    errors = 0
    
    for i in range(num_requests):
        attempt = 0
        success = False
        
        while attempt < retries and not success:
            try:
                start_time = time.time()
                response = requests.get(url, headers=headers, timeout=timeout)
                end_time = time.time()
                
                if response.status_code == 200:
                    latency = (end_time - start_time) * 1000  # Convert to milliseconds
                    latencies.append(latency)
                    success = True
                else:
                    errors += 1
                    attempt += 1
            except requests.RequestException as e:
                errors += 1
                attempt += 1
                if attempt >= retries:
                    return False, f"Request failed after {retries} attempts: {str(e)}"
    
    # If we have at least one successful request, calculate average latency
    if latencies:
        avg_latency = sum(latencies) / len(latencies)
        return True, avg_latency
    else:
        return False, f"All {num_requests} requests failed"

def save_latency_data(latency):
    """
    Save latency data to a JSON file
    
    Args:
        latency (float): Latency in milliseconds
    """
    # Load existing data if any
    data = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            # If file is corrupted, start with empty data
            data = []
    
    # Add new data point
    timestamp = int(time.time())
    data.append({
        'timestamp': timestamp,
        'latency': latency,
        'date': datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    })
    
    # Limit the number of entries to keep the file size manageable (use the last 100 entries)
    max_entries = 100
    if len(data) > max_entries:
        data = data[-max_entries:]
    
    # Save back to file
    with open(LOG_FILE, 'w') as file:
        json.dump(data, file, indent=2)
    
    print(f"Saved latency data for OKX: {latency:.2f} ms")
    return True

def get_btc_usdt_price():
    """
    Get BTC-USDT price from OKX exchange and calculate latency
    
    Returns:
        tuple: (data, latency_seconds)
    """
    url = "https://www.okx.com/api/v5/market/ticker?instId=BTC-USDT"
    start_time = time.time()
    response = requests.get(url)
    latency = time.time() - start_time
    data = response.json()
    return data, latency

def test_okx_latency():
    """
    Test OKX API latency for market data
    
    Returns:
        tuple: (success, latency_ms or error_message)
    """
    print("Testing OKX API latency...")
    success, result = measure_api_latency('market_data')
    
    if success:
        save_latency_data(result)
        print(f"✓ OKX market data API latency: {result:.2f} ms")
        return True, result
    else:
        print(f"✗ OKX market data API test failed: {result}")
        return False, result

def test_okx_book_latency():
    """
    Test OKX orderbook API latency
    
    Returns:
        tuple: (success, latency_ms or error_message)
    """
    print("Testing OKX orderbook API latency...")
    success, result = measure_api_latency('book')
    
    if success:
        save_latency_data(result)
        print(f"✓ OKX orderbook API latency: {result:.2f} ms")
        return True, result
    else:
        print(f"✗ OKX orderbook API test failed: {result}")
        return False, result

def test_okx_trades_latency():
    """
    Test OKX trades API latency
    
    Returns:
        tuple: (success, latency_ms or error_message)
    """
    print("Testing OKX trades API latency...")
    success, result = measure_api_latency('trades')
    
    if success:
        save_latency_data(result)
        print(f"✓ OKX trades API latency: {result:.2f} ms")
        return True, result
    else:
        print(f"✗ OKX trades API test failed: {result}")
        return False, result

def test_btc_usdt_price():
    """
    Test OKX BTC-USDT price API latency using original method
    """
    data, latency = get_btc_usdt_price()
    
    # Validate return data format
    assert data.get("code") == "0", f"API Error: {data}"
    assert "data" in data and len(data["data"]) > 0, "Empty or invalid response data"
    
    ticker_info = data["data"][0]
    last_price = ticker_info.get("last")
    
    # Output BTC-USDT latest price and API latency (milliseconds)
    print(f"BTC-USDT Latest Price: {last_price}")
    print(f"API Access Latency: {latency * 1000:.2f} ms")
    
    # Log latency
    save_latency_data(latency * 1000)
    
    # Optional: Assert latency is within reasonable range (e.g., under 1 second)
    assert latency < 1, f"API Access Latency Too High: {latency * 1000:.2f} ms"

if __name__ == "__main__":
    test_okx_latency() 