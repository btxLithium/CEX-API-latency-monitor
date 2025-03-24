"""
Combined test runner for all exchange latency tests
"""
import sys
import os
from .config import API_ENDPOINTS

# Import latency test functions
from .okx_latency import test_okx_latency, test_okx_book_latency, test_okx_trades_latency
from .bitget_latency import test_bitget_latency, test_bitget_book_latency, test_bitget_trades_latency

def run_exchange_tests(exchange):
    """
    Run all latency tests for a specific exchange
    
    Args:
        exchange (str): Exchange identifier (e.g., 'okx', 'bitget')
    
    Returns:
        dict: Test results
    """
    results = {}
    exchange_name = exchange.upper()
    
    print(f"\n=== Running {exchange_name} latency tests ===")
    
    # Market data test
    print(f"Testing {exchange_name} market data API latency...")
    if exchange == 'okx':
        success, result = test_okx_latency()
    elif exchange == 'bitget':
        success, result = test_bitget_latency()
    else:
        success, result = False, f"Exchange {exchange} not supported"
    
    results['market_data'] = {
        'success': success,
        'result': result
    }
    
    if success:
        print(f"✓ {exchange_name} market data API latency: {result:.2f} ms")
    else:
        print(f"✗ {exchange_name} market data API test failed: {result}")
    
    # Orderbook test
    print(f"Testing {exchange_name} orderbook API latency...")
    if exchange == 'okx':
        success, result = test_okx_book_latency()
    elif exchange == 'bitget':
        success, result = test_bitget_book_latency()
    else:
        success, result = False, f"Exchange {exchange} not supported"
    
    results['book'] = {
        'success': success,
        'result': result
    }
    
    if success:
        print(f"✓ {exchange_name} orderbook API latency: {result:.2f} ms")
    else:
        print(f"✗ {exchange_name} orderbook API test failed: {result}")
    
    # Trades test
    print(f"Testing {exchange_name} trades API latency...")
    if exchange == 'okx':
        success, result = test_okx_trades_latency()
    elif exchange == 'bitget':
        success, result = test_bitget_trades_latency()
    else:
        success, result = False, f"Exchange {exchange} not supported"
    
    results['trades'] = {
        'success': success,
        'result': result
    }
    
    if success:
        print(f"✓ {exchange_name} trades API latency: {result:.2f} ms")
    else:
        print(f"✗ {exchange_name} trades API test failed: {result}")
    
    return results

def run_all_latency_tests():
    """
    Run latency tests for all configured exchanges
    
    Returns:
        dict: Test results for all exchanges
    """
    all_results = {}
    
    print("Starting API latency tests for all exchanges...")
    
    # Get list of exchanges from config
    exchanges = list(API_ENDPOINTS.keys())
    
    for exchange in exchanges:
        all_results[exchange] = run_exchange_tests(exchange)
    
    # Print summary
    print("\n=== Test Summary ===")
    for exchange in exchanges:
        exchange_name = exchange.upper()
        results = all_results[exchange]
        
        print(f"\n{exchange_name} Results:")
        
        for endpoint, data in results.items():
            if data['success']:
                print(f"  ✓ {endpoint}: {data['result']:.2f} ms")
            else:
                print(f"  ✗ {endpoint}: Failed - {data['result']}")
    
    print("\nAPI latency tests completed.")
    return all_results

if __name__ == "__main__":
    run_all_latency_tests() 