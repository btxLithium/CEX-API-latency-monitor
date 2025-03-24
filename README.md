# Crypto Exchange API Latency Monitoring System

A comprehensive system for measuring, logging, and visualizing the API latency of various cryptocurrency exchanges.

## Features

- Support for multiple exchanges (OKX, Bitget)
- Configurable API endpoints for each exchange (market data, orderbook, trades)
- Detailed latency testing with retry mechanisms and error handling
- Automated data collection and visualization
- Customizable reporting with statistical analysis
- GitHub Actions integration for continuous monitoring

## Automation

GitHub Actions is configured to automatically run latency tests periodically, generating reports and committing the updated data to the repository. This provides continuous monitoring of exchange API performance.

## Project Structure

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

## Installation

This project uses [Poetry](https://python-poetry.org/) for dependency management.

```bash

# manually run tests using the defined script entry point
poetry run run-tests all
```



## Configuration

The system is easily configurable through the `monitor/config.py` file. You can:

- Add new exchanges and API endpoints
- Adjust latency test settings (retries, timeouts, etc.)
- Configure data storage behavior
- Customize reporting parameters

Example configuration:

```python
API_ENDPOINTS = {
    'okx': {
        'name': 'OKX',
        'endpoints': {
            'market_data': 'https://www.okx.com/api/v5/market/ticker?instId=BTC-USDT',
            'book': 'https://www.okx.com/api/v5/market/books?instId=BTC-USDT&sz=10',
            'trades': 'https://www.okx.com/api/v5/market/trades?instId=BTC-USDT'
        },
        'description': 'OKX Cryptocurrency Exchange'
    },
    # Add more exchanges as needed
}
```


