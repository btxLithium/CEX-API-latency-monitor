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

def generate_comprehensive_report(output_dir=None):
    """
    Generate a comprehensive report of all benchmark results
    
    Args:
        output_dir (str, optional): Output directory
        
    Returns:
        bool: Success status
    """
    if not output_dir:
        output_dir = DATA_STORAGE.get('output_dir', 'benchmark_results')
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all JSON benchmark files
    benchmark_dir = os.path.join(os.getcwd(), '.benchmarks')
    
    if not os.path.exists(benchmark_dir):
        print(f"No benchmark data found in {benchmark_dir}")
        return False
    
    # Find the most recent benchmark results for each exchange
    exchange_results = {}
    
    # Walk through the benchmark directory
    for root, dirs, files in os.walk(benchmark_dir):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        
                    # Extract benchmark data
                    if 'benchmarks' in data:
                        for benchmark in data['benchmarks']:
                            group = benchmark.get('group', 'unknown')
                            name = benchmark.get('name', '')
                            mean = benchmark.get('stats', {}).get('mean', 0) * 1000  # to ms
                            min_val = benchmark.get('stats', {}).get('min', 0) * 1000  # to ms
                            max_val = benchmark.get('stats', {}).get('max', 0) * 1000  # to ms
                            
                            # Parse endpoint from benchmark name
                            endpoint = name.replace('test_', '').replace('_benchmark', '')
                            
                            if group not in exchange_results:
                                exchange_results[group] = []
                                
                            exchange_results[group].append({
                                'endpoint': endpoint,
                                'mean': mean,
                                'min': min_val,
                                'max': max_val,
                                'file': file
                            })
                except Exception as e:
                    print(f"Error processing {file}: {str(e)}")
    
    # Create a comprehensive report
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(output_dir, f"comprehensive_report_{timestamp}.html")
    
    # Copy CSS file to output directory for relative path reference
    css_src = os.path.join(os.getcwd(), 'assets', 'css', 'report.css')
    css_dest_dir = os.path.join(output_dir, 'assets', 'css')
    os.makedirs(css_dest_dir, exist_ok=True)
    css_dest = os.path.join(css_dest_dir, 'report.css')
    
    # Copy font file to output directory
    font_src = os.path.join(os.getcwd(), 'assets', 'IBMPlexMono-Medium.ttf')
    font_dest_dir = os.path.join(output_dir, 'assets')
    os.makedirs(font_dest_dir, exist_ok=True)
    font_dest = os.path.join(font_dest_dir, 'IBMPlexMono-Medium.ttf')
    
    try:
        import shutil
        shutil.copy(css_src, css_dest)
        shutil.copy(font_src, font_dest)
    except Exception as e:
        print(f"Warning: Could not copy style files: {str(e)}")
    
    # Generate HTML report
    with open(report_file, 'w') as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
    <title>API Latency Benchmark Report</title>
    <link rel="stylesheet" href="assets/css/report.css">
    <meta charset="UTF-8">
</head>
<body>
    <h1>API Latency Benchmark Report</h1>
    <p class="timestamp">Generated on: """ + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
""")
        
        # Add summary for each exchange
        for exchange, results in exchange_results.items():
            f.write(f"""
    <h2>{exchange.upper()} Exchange</h2>
    <table>
        <tr>
            <th>Endpoint</th>
            <th>Mean (ms)</th>
            <th>Min (ms)</th>
            <th>Max (ms)</th>
        </tr>
""")
            
            for result in results:
                f.write(f"""
        <tr>
            <td>{result['endpoint']}</td>
            <td>{result['mean']:.2f}</td>
            <td>{result['min']:.2f}</td>
            <td>{result['max']:.2f}</td>
        </tr>
""")
            
            f.write("    </table>\n")
        
        # Add summary of all exchanges
        f.write("""
    <div class="summary">
        <h2>Comparison Summary</h2>
        <table>
            <tr>
                <th>Exchange</th>
                <th>Average Latency (ms)</th>
                <th>Best Endpoint</th>
                <th>Worst Endpoint</th>
            </tr>
""")
        
        for exchange, results in exchange_results.items():
            if results:
                avg_latency = sum(r['mean'] for r in results) / len(results)
                best = min(results, key=lambda x: x['mean'])
                worst = max(results, key=lambda x: x['mean'])
                
                f.write(f"""
            <tr>
                <td>{exchange.upper()}</td>
                <td>{avg_latency:.2f}</td>
                <td><span class="best-value">{best['endpoint']} ({best['mean']:.2f} ms)</span></td>
                <td><span class="worst-value">{worst['endpoint']} ({worst['mean']:.2f} ms)</span></td>
            </tr>
""")
        
        f.write("""
        </table>
    </div>
</body>
</html>
""")
    
    print(f"Comprehensive report generated: {report_file}")
    return True 