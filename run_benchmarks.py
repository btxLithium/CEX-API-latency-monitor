#!/usr/bin/env python3
"""
API Latency Benchmark Runner

This script runs benchmarks for all supported exchanges
and generates comprehensive reports of API latency performance.
"""
import os
import sys
import pytest
import argparse
from datetime import datetime

from monitor import (
    run_okx_benchmarks,
    run_bitget_benchmarks,
    EXCHANGES,
    BENCHMARK_SETTINGS
)

def setup_arg_parser():
    """Set up command line argument parser"""
    parser = argparse.ArgumentParser(
        description="Run API latency benchmarks for cryptocurrency exchanges"
    )
    parser.add_argument(
        "-e", "--exchange",
        choices=list(EXCHANGES.keys()) + ["all"],
        default="all",
        help="Exchange to benchmark (default: all)"
    )
    parser.add_argument(
        "-o", "--output-dir",
        default="benchmark_results",
        help="Directory to save benchmark results (default: benchmark_results)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    return parser

def create_output_dir(output_dir):
    """Create output directory if it doesn't exist"""
    os.makedirs(output_dir, exist_ok=True)
    print(f"Benchmark results will be saved to: {os.path.abspath(output_dir)}")

def run_benchmarks(exchange, output_dir, verbose=False):
    """
    Run benchmarks for specified exchange
    
    Args:
        exchange (str): Exchange name or 'all'
        output_dir (str): Directory to save benchmark results
        verbose (bool): Enable verbose output
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Set up pytest arguments
    pytest_args = [
        "-v" if verbose else "-q",
        "--benchmark-save={}".format(f"{exchange}_{timestamp}"),
        "--benchmark-storage={}/".format(output_dir),
        "--benchmark-columns=min,max,mean,stddev"
    ]
    
    if exchange == "all":
        print("\n=== Running benchmarks for all exchanges ===")
        for ex in EXCHANGES:
            print(f"\n--- Running {ex.upper()} benchmarks ---")
            if ex == "okx":
                run_okx_benchmarks()
            elif ex == "bitget":
                run_bitget_benchmarks()
    else:
        print(f"\n=== Running benchmarks for {exchange.upper()} ===")
        if exchange == "okx":
            run_okx_benchmarks()
        elif exchange == "bitget":
            run_bitget_benchmarks()

    print(f"\nBenchmark results saved to {output_dir}/")

def main():
    """Main function"""
    parser = setup_arg_parser()
    args = parser.parse_args()
    
    create_output_dir(args.output_dir)
    run_benchmarks(args.exchange, args.output_dir, args.verbose)
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 