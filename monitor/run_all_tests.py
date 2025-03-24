"""
Combined test runner for all exchange latency tests
"""
import sys
import os
from .config import API_ENDPOINTS

# Import latency test functions
from .okx_latency import test_okx_latency, test_okx_book_latency, test_okx_trades_latency
from .bitget_latency import test_bitget_latency, test_bitget_book_latency, test_bitget_trades_latency

def run_api_test(exchange, endpoint_type, test_function):
    """
    Run a specific API test and format the results
    
    Args:
        exchange (str): Exchange identifier (e.g., 'okx', 'bitget')
        endpoint_type (str): Type of endpoint being tested (e.g., 'market_data', 'book', 'trades')
        test_function (function): The test function to call
    
    Returns:
        dict: Test results
    """
    exchange_name = exchange.upper()
    print(f"Testing {exchange_name} {endpoint_type} API latency...")
    
    success, result = test_function()
    
    # Store results
    test_result = {
        'success': success,
        'result': result
    }
    
    # Format output
    if success:
        print(f"✓ {exchange_name} {endpoint_type} API latency: {result:.2f} ms")
    else:
        print(f"✗ {exchange_name} {endpoint_type} API test failed: {result}")
        
    return test_result

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
    if exchange == 'okx':
        results['market_data'] = run_api_test(exchange, 'market data', test_okx_latency)
        results['book'] = run_api_test(exchange, 'orderbook', test_okx_book_latency)
        results['trades'] = run_api_test(exchange, 'trades', test_okx_trades_latency)
    elif exchange == 'bitget':
        results['market_data'] = run_api_test(exchange, 'market data', test_bitget_latency)
        results['book'] = run_api_test(exchange, 'orderbook', test_bitget_book_latency)
        results['trades'] = run_api_test(exchange, 'trades', test_bitget_trades_latency)
    
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