# CEX public API Benchmark

**Latest generated report of OKX and Bitget public API latency: [https://btxlithium.github.io/CEX-public-API-benchmark/benchmark_report_latest.html](https://btxlithium.github.io/CEX-public-API-benchmark/benchmark_report_latest.html)**

A benchmarking tool designed to measure, analyze and compare public API latency for crypto exchanges using `pytest` framework, supports multiple CEXs (OKX and Bitget by default, configurable in `scripts/config.py`).

一个基于`pytest`框架开发的性能测试工具，专门用于测试和对比加密货币交易所的public API的延迟。目前默认支持 OKX 和 Bitget（可以通过 `scripts/config.py` 文件进行配置和扩展）。

## Usage
### Run benchmarks automatically
GitHub Actions is configured to automatically run latency tests periodically(every 36 hours), generating reports and committing to the repository. This provides continuous monitoring of exchange API performance.

### Run benchmarks manually
This project uses [Poetry](https://python-poetry.org/) for dependency management.
```bash
# manually run benchmarks using the defined script entry point
poetry run run-benchmarks all
poetry run run-benchmarks okx
```


## Configuration

The tool is easily configurable through the `scripts/config.py` file. You can:

- Add new API endpoints 
- Adjust latency test settings (retries, timeouts, etc.)
- Configure data storage behavior
- Customize reporting parameters

Example configuration:

```python
'bitget': {
    'book': {
        'url': 'https://api.bitget.com/api/mix/v1/market/depth?symbol=BTCUSDT_UMCBL&limit=20',
        'method': 'GET',
    }
}
```


## Project Structure

```
.
├── .github/
│   └── workflows/              # GitHub Actions workflow
│       └── api_latency_measurement.yml
├── .benchmarks/                # Benchmark data saved by pytest-benchmark           
├── benchmark_results/          # Benchmark results output directory
│   ├── assets/               
│   └── comprehensive_report_*.html  # Generated HTML reports
├── scripts/                   
│   ├── __init__.py            
│   ├── config.py           
│   ├── benchmark_core.py       # Core benchmarking functionality
│   ├── okx_latency.py          # OKX exchange specific tests
│   └── bitget_latency.py       # Bitget exchange specific tests
├── run_benchmarks.py          
├── pyproject.toml              # Project configuration and dependencies
├── poetry.lock             
└── README.md                  
```

## Donations

If you'd like to support my work, consider buy me a coffee:

- USDT or USDC Aptos:  
0x675422152a1dcb2eba3011a5f2901d9756ca7be872db10caa3a4dd7f25482e8e  
- USDT or USDC BNB Smart Chain:  
0xbe9c806a872c826fb817f8086aafa26a6104afac  
