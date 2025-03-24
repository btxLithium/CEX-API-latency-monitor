"""
Bitget Exchange API Latency Benchmark Module

This module provides pytest-benchmark functions for testing
the latency of various Bitget exchange API endpoints.
"""
import pytest
import requests
import json
from .benchmark_core import benchmark_api_request

@pytest.mark.benchmark(
    group="bitget",
    min_time=0.1,
    max_time=0.5,
    min_rounds=5,
    disable_gc=True,
    warmup=True
)
def test_bitget_market_data_benchmark(benchmark):
    """Benchmark Bitget market data API latency"""
    success, result = benchmark_api_request(benchmark, 'bitget', 'market_data')
    assert success, f"Bitget market data API benchmark failed: {result}"
    
    # Verify response data integrity
    response = result['response']
    data = response.json()
    assert "data" in data, f"API Error: {response.text}"
    # Further data validation can be added based on Bitget API response structure

@pytest.mark.benchmark(
    group="bitget",
    min_time=0.1,
    max_time=0.5,
    min_rounds=5,
    disable_gc=True,
    warmup=True
)
def test_bitget_book_benchmark(benchmark):
    """Benchmark Bitget orderbook API latency"""
    success, result = benchmark_api_request(benchmark, 'bitget', 'book')
    assert success, f"Bitget orderbook API benchmark failed: {result}"
    
    # Verify response data integrity
    response = result['response']
    data = response.json()
    assert "data" in data, f"API Error: {response.text}"
    # Further data validation can be added based on Bitget API response structure

@pytest.mark.benchmark(
    group="bitget",
    min_time=0.1,
    max_time=0.5,
    min_rounds=5,
    disable_gc=True,
    warmup=True
)
def test_bitget_trades_benchmark(benchmark):
    """Benchmark Bitget trades API latency"""
    success, result = benchmark_api_request(benchmark, 'bitget', 'trades')
    assert success, f"Bitget trades API benchmark failed: {result}"
    
    # Verify response data integrity
    response = result['response']
    data = response.json()
    assert "data" in data, f"API Error: {response.text}"
    # Further data validation can be added based on Bitget API response structure

# Helper function for manual testing
def run_all_benchmarks():
    """
    Run all Bitget benchmarks
    
    This function is exported and used by the main run_benchmarks.py script
    """
    print("\n=== Running Bitget API Benchmarks ===")
    pytest.main(["-xvs", __file__, "--benchmark-save=bitget"])
    
if __name__ == "__main__":
    run_all_benchmarks() 