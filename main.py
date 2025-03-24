#!/usr/bin/env python3
"""
Main entry point for crypto exchange API latency tests
"""
import sys
import os
from monitor.config import API_ENDPOINTS
from monitor.run_all_tests import run_all_latency_tests, run_exchange_tests
import json
from datetime import datetime

def print_usage():
    """Print usage information"""
    exchanges = list(API_ENDPOINTS.keys())
    exchanges_str = ', '.join(exchanges)
    
    print(f"""
Crypto Exchange API Latency Testing Tool

Usage:
    python main.py [command]

Commands:
    all             Run latency tests for all exchanges
    list            List available exchanges
    {exchanges_str}    Run latency tests for a specific exchange
    help            Show this help message

Examples:
    python main.py all
    python main.py okx
    python main.py bitget
    """)

def list_exchanges():
    """List all available exchanges from config"""
    exchanges = list(API_ENDPOINTS.keys())
    
    if not exchanges:
        print("No exchanges configured.")
        return
    
    print("\nAvailable exchanges:")
    for ex in exchanges:
        config = API_ENDPOINTS[ex]
        print(f"  - {config['name']} ({ex}): {config['description']}")
        
        # List endpoints
        print("    Endpoints:")
        for endpoint, url in config['endpoints'].items():
            print(f"      - {endpoint}: {url}")
    
    print(f"\nTotal: {len(exchanges)} exchanges\n")

def main():
    """Main function to parse args and run tests"""
    # If no arguments, default to 'all'
    if len(sys.argv) < 2:
        run_all_latency_tests()
        return
    
    command = sys.argv[1].lower()
    
    if command == 'help' or command == '--help' or command == '-h':
        print_usage()
    elif command == 'list' or command == 'ls':
        list_exchanges()
    elif command == 'all':
        run_all_latency_tests()
    elif command in API_ENDPOINTS:
        run_exchange_tests(command)
    else:
        print(f"Unknown command or exchange: {command}")
        print_usage()
        sys.exit(1)

if __name__ == "__main__":
    main() 