# Configuration file for API latency monitoring

# API endpoints for different exchanges
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
    'bitget': {
        'name': 'Bitget',
        'endpoints': {
            'market_data': 'https://api.bitget.com/api/spot/v1/market/ticker?symbol=BTCUSDT',
            'book': 'https://api.bitget.com/api/spot/v1/market/depth?symbol=BTCUSDT&limit=10',
            'trades': 'https://api.bitget.com/api/spot/v1/market/fills?symbol=BTCUSDT'
        },
        'description': 'Bitget Cryptocurrency Exchange'
    }
}

# Settings for latency testing
LATENCY_TEST_SETTINGS = {
    'timeout': 10,  # Request timeout in seconds
    'num_requests': 5,  # Number of requests to make for each test
    'retry_count': 3,  # Number of retries for failed requests
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}

# Data storage settings
DATA_STORAGE = {
    'max_entries': 1000,  # Maximum number of data points to keep per exchange
}

# Default endpoints to test when running a basic test
DEFAULT_TEST_ENDPOINT = 'market_data'

# Reporting settings
REPORTING = {
    'chart_width': 12,
    'chart_height': 7,
    'dpi': 300,
} 