# 123

A benchmarking tool designed to measure, analyze and compare API latency for cryptocurrency exchanges using `pytest-benchmark`, supports multiple CEXs (OKX and Bitget by default, configurable in `scripts/config.py`).


## Usage
### Run benchmarks automatically
GitHub Actions is configured to automatically run latency tests periodically, generating reports and committing to the repository. This provides continuous monitoring of exchange API performance.

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
        'headers': {
            'Accept': 'application/json'
        }
    }
}
```


## Project Structure
TODO: update project structure

```
.
├── .github/
│   └── workflows/              # GitHub Actions workflow
│       └── api_latency_measurement.yml
├── assets/                     
├── data/                       
│   ├── okx_latency_data.json
│   └── bitget_latency_data.json
├── monitor/                    # Core monitoring functionality
│   ├── __init__.py
│   ├── config.py               # Configuration settings
│   ├── latency_core.py         # Core latency testing functionality
│   ├── okx_latency.py          # OKX-specific testing module
│   ├── bitget_latency.py       # Bitget-specific testing module
│   └── run_all_tests.py        # Combined test runner
├── reports/                    
│   ├── okx_latency_report.png
│   └── bitget_latency_report.png
├── generate_report.py          # Report generation script
├── main.py                     # Main entry point
├── pyproject.toml              
├── poetry.lock                 # Poetry lock file
└── README.md                   
```
