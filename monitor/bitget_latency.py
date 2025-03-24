"""
Bitget API Latency Testing Module
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
LOG_FILE = os.path.join(DATA_DIR, 'bitget_latency_data.json')

def measure_api_latency(endpoint_key=None):
    """
    Measure API latency for Bitget exchange and endpoint
    
    Args:
        endpoint_key (str, optional): Specific endpoint to test. 
                                     Defaults to None, which uses the default endpoint.
    
    Returns:
        tuple: (success, latency_ms or error_message)
    """
    # Bitget specific API endpoints
    API_ENDPOINTS = {
        'market_data': "https://api.bitget.com/api/v2/spot/market/ticker?symbol=BTCUSDT",
        'book': "https://api.bitget.com/api/v2/spot/market/orderbook?symbol=BTCUSDT&limit=20",
        'trades': "https://api.bitget.com/api/v2/spot/market/fills?symbol=BTCUSDT&limit=20"
    }
    
    # If no endpoint specified, use the default market data endpoint
    if endpoint_key is None:
        endpoint_key = 'market_data'
    
    if endpoint_key not in API_ENDPOINTS:
        return False, f"Endpoint '{endpoint_key}' not found for Bitget"
    
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
    
    print(f"Saved latency data for Bitget: {latency:.2f} ms")
    return True

def test_bitget_latency():
    """
    Test Bitget API latency for market data
    
    Returns:
        tuple: (success, latency_ms or error_message)
    """
    print("Testing BITGET API latency...")
    success, result = measure_api_latency('market_data')
    
    if success:
        save_latency_data(result)
        print(f"✓ BITGET market data API latency: {result:.2f} ms")
        return True, result
    else:
        print(f"✗ BITGET market data API test failed: {result}")
        return False, result

def test_bitget_book_latency():
    """
    Test Bitget orderbook API latency
    
    Returns:
        tuple: (success, latency_ms or error_message)
    """
    print("Testing BITGET orderbook API latency...")
    success, result = measure_api_latency('book')
    
    if success:
        save_latency_data(result)
        print(f"✓ BITGET orderbook API latency: {result:.2f} ms")
        return True, result
    else:
        print(f"✗ BITGET orderbook API test failed: {result}")
        return False, result

def test_bitget_trades_latency():
    """
    Test Bitget trades API latency
    
    Returns:
        tuple: (success, latency_ms or error_message)
    """
    print("Testing BITGET trades API latency...")
    success, result = measure_api_latency('trades')
    
    if success:
        save_latency_data(result)
        print(f"✓ BITGET trades API latency: {result:.2f} ms")
        return True, result
    else:
        print(f"✗ BITGET trades API test failed: {result}")
        return False, result

if __name__ == "__main__":
    test_bitget_latency() 