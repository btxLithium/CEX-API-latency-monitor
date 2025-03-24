"""
Core benchmark utilities for API latency monitoring

This module provides core functionality for benchmarking API requests
and handling the results of those benchmarks.
"""
import time
import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os
from .config import EXCHANGES, ENDPOINTS, API_SETTINGS, BENCHMARK_SETTINGS, DATA_STORAGE

def make_api_request(exchange, endpoint_key):
    """
    Make API request to specified exchange endpoint
    
    Args:
        exchange (str): Exchange identifier
        endpoint_key (str): Endpoint key
        
    Returns:
        tuple: (success, result)
    """
    if exchange not in EXCHANGES:
        return False, f"Exchange '{exchange}' not found in config"
    
    if endpoint_key not in ENDPOINTS.get(exchange, {}):
        return False, f"Endpoint '{endpoint_key}' not found for exchange '{exchange}'"
    
    endpoint_data = ENDPOINTS[exchange][endpoint_key]
    url = endpoint_data['url']
    method = endpoint_data.get('method', 'GET')
    headers = endpoint_data.get('headers', {})
    params = endpoint_data.get('params', {})
    data = endpoint_data.get('data', None)
    
    # Add API key if configured
    if API_SETTINGS.get('use_api_key', False) and exchange in API_SETTINGS.get('api_keys', {}):
        api_key_header = API_SETTINGS.get('api_key_header', 'X-API-KEY')
        headers[api_key_header] = API_SETTINGS['api_keys'][exchange]
    
    try:
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers, params=params, timeout=API_SETTINGS.get('timeout', 10))
        elif method.upper() == 'POST':
            response = requests.post(url, headers=headers, params=params, json=data, timeout=API_SETTINGS.get('timeout', 10))
        else:
            return False, f"Unsupported HTTP method: {method}"
        
        return True, response
    except requests.exceptions.RequestException as e:
        return False, str(e)

def benchmark_api_request(benchmark, exchange, endpoint_key):
    """
    Benchmark API request latency using pytest-benchmark
    
    Args:
        benchmark: pytest-benchmark fixture
        exchange (str): Exchange identifier
        endpoint_key (str): Endpoint key
        
    Returns:
        tuple: (success, result_dict)
    """
    # Define the function to benchmark
    def api_call():
        success, response = make_api_request(exchange, endpoint_key)
        if not success:
            return False, response
        return True, response
    
    # Run the benchmark
    result = benchmark.pedantic(
        api_call,
        rounds=BENCHMARK_SETTINGS['min_rounds'],
        iterations=1
    )
    
    if not result[0]:
        return False, {"error": result[1]}
    
    return True, {"response": result[1], "stats": benchmark.stats}

def save_benchmark_results(results, exchange, output_dir=None):
    """
    Save benchmark results to CSV and generate plots
    
    Args:
        results (dict): Benchmark results
        exchange (str): Exchange identifier
        output_dir (str, optional): Output directory
        
    Returns:
        bool: Success status
    """
    if not output_dir:
        output_dir = DATA_STORAGE.get('output_dir', 'benchmark_results')
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create results DataFrame
    df = pd.DataFrame(results)
    
    # Save results to CSV
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = os.path.join(output_dir, f"{exchange}_benchmark_{timestamp}.csv")
    df.to_csv(csv_file, index=False)
    
    # Generate plots
    if len(df) > 0:
        plt.figure(figsize=(DATA_STORAGE['chart_width'], DATA_STORAGE['chart_height']))
        plt.bar(df['endpoint'], df['mean'], yerr=df['stddev'])
        plt.xlabel('Endpoint')
        plt.ylabel('Latency (ms)')
        plt.title(f'{exchange.upper()} API Endpoint Latency')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save plot
        plot_file = os.path.join(output_dir, f"{exchange}_benchmark_{timestamp}.png")
        plt.savefig(plot_file, dpi=DATA_STORAGE['dpi'])
        plt.close()
    
    return True 