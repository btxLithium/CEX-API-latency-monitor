"""
API Latency Monitoring and Benchmarking

This package provides tools for monitoring and benchmarking 
API latency for various cryptocurrency exchanges.
"""

from .config import (
    EXCHANGES,
    ENDPOINTS,
    BENCHMARK_SETTINGS,
    API_SETTINGS,
    DATA_STORAGE,
    REPORTING
)

from .benchmark_core import (
    make_api_request,
    benchmark_api_request,
    save_benchmark_results
)

# Export exchange-specific modules
from .okx_latency import test_okx_market_data_benchmark, test_okx_book_benchmark, test_okx_trades_benchmark, run_all_benchmarks as run_okx_benchmarks
from .bitget_latency import test_bitget_market_data_benchmark, test_bitget_book_benchmark, test_bitget_trades_benchmark, run_all_benchmarks as run_bitget_benchmarks

__all__ = [
    'EXCHANGES',
    'ENDPOINTS',
    'BENCHMARK_SETTINGS',
    'API_SETTINGS',
    'DATA_STORAGE',
    'REPORTING',
    'make_api_request',
    'benchmark_api_request',
    'save_benchmark_results',
    'test_okx_market_data_benchmark',
    'test_okx_book_benchmark',
    'test_okx_trades_benchmark',
    'test_bitget_market_data_benchmark',
    'test_bitget_book_benchmark',
    'test_bitget_trades_benchmark',
    'run_okx_benchmarks',
    'run_bitget_benchmarks'
] 