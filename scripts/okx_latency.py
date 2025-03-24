"""
OKX Exchange API Latency Benchmark Module

This module provides pytest-benchmark functions for testing
the latency of various OKX exchange API endpoints.
"""
import pytest
import requests
import json
from .benchmark_core import benchmark_api_request

@pytest.mark.benchmark(
    group="okx",
    min_time=0.1,
    max_time=0.5,
    min_rounds=5,
    disable_gc=True,
    warmup=True
)
def test_okx_market_data_benchmark(benchmark):
    """Benchmark OKX market data API latency"""
    success, result = benchmark_api_request(benchmark, 'okx', 'market_data')
    assert success, f"OKX market data API benchmark failed: {result}"
    
    # Verify response data integrity
    response = result['response']
    data = response.json()
    assert data.get("code") == "0", f"API Error: {response.text}"
    # Further data validation can be added based on OKX API response structure

@pytest.mark.benchmark(
    group="okx",
    min_time=0.1,
    max_time=0.5,
    min_rounds=5,
    disable_gc=True,
    warmup=True
)
def test_okx_book_benchmark(benchmark):
    """Benchmark OKX orderbook API latency"""
    success, result = benchmark_api_request(benchmark, 'okx', 'book')
    assert success, f"OKX orderbook API benchmark failed: {result}"
    
    # Verify response data integrity
    response = result['response']
    data = response.json()
    assert data.get("code") == "0", f"API Error: {response.text}"
    # Further data validation can be added based on OKX API response structure

@pytest.mark.benchmark(
    group="okx",
    min_time=0.1,
    max_time=0.5,
    min_rounds=5,
    disable_gc=True,
    warmup=True
)
def test_okx_trades_benchmark(benchmark):
    """Benchmark OKX trades API latency"""
    success, result = benchmark_api_request(benchmark, 'okx', 'trades')
    assert success, f"OKX trades API benchmark failed: {result}"
    
    # Verify response data integrity
    response = result['response']
    data = response.json()
    assert data.get("code") == "0", f"API Error: {response.text}"
    # Further data validation can be added based on OKX API response structure

# Helper function for manual testing
def run_all_benchmarks():
    """
    Run all OKX benchmarks
    
    This function is exported and used by the main run_benchmarks.py script
    """
    print("\n=== Running OKX API Benchmarks ===")
    pytest.main(["-xvs", __file__, "--benchmark-save=okx"])
    
if __name__ == "__main__":
    run_all_benchmarks() 