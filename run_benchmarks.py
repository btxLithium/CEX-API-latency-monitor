#!/usr/bin/env python3
"""
API Latency Benchmark Runner

This script runs benchmarks for the two exchanges
and generates comprehensive reports of API latency performance.
"""
import os
import sys
from datetime import datetime

from scripts import (
    run_okx_benchmarks,
    run_bitget_benchmarks,
    generate_comprehensive_report
)

def create_output_dir(output_dir="benchmark_results"):
    """Create output directory if it doesn't exist"""
    os.makedirs(output_dir, exist_ok=True)
    print(f"Benchmark results will be saved to: {os.path.abspath(output_dir)}")
    return output_dir

def run_benchmarks(exchange="all", output_dir="benchmark_results"):
    """
    Run benchmarks for specified exchange
    
    Args:
        exchange (str): Exchange name or 'all'
        output_dir (str): Directory to save benchmark results
    """

    output_dir = create_output_dir(output_dir)
    
    if exchange == "all":
        print("\n=== Running benchmarks for all exchanges ===")
        run_okx_benchmarks()
        run_bitget_benchmarks()
    else:
        print(f"\n=== Running benchmarks for {exchange.upper()} ===")
        if exchange == "okx":
            run_okx_benchmarks()
        elif exchange == "bitget":
            run_bitget_benchmarks()

    # 生成综合报告
    generate_comprehensive_report(output_dir)
    
    print(f"\nBenchmark results saved to {output_dir}/")

def main():
    """Main function"""
    output_dir = "benchmark_results"
    EXCHANGES = ["okx", "bitget"]

    args = sys.argv[1:]
    exchange = args[0]
        
    if exchange not in (EXCHANGES + ["all"]):
        exchange = "all"
        
    run_benchmarks(exchange, output_dir)
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 