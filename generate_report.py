import os
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.font_manager as fm
from datetime import datetime, timezone, timedelta
import numpy as np
import platform
import time
import glob

# Define data and report paths
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
REPORTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reports')
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

# Set custom font from assets folder
def set_custom_font():
    """Set custom font from assets folder"""
    font_path = os.path.join(ASSETS_DIR, 'IBMPlexMono-Medium.ttf')
    if os.path.exists(font_path):
        # Register the font
        font_prop = fm.FontProperties(fname=font_path)
        # Use a simple approach: use the default font
        # Just register the font so it can be used in specific text elements
        return font_prop
    else:
        print(f"Error: Font file not found at {font_path}")
        return None

def load_latency_data(exchange):
    """
    Load latency data for a specific exchange
    
    Args:
        exchange (str): Exchange name
    
    Returns:
        list: Latency data records
    """
    data_file = os.path.join(DATA_DIR, f'{exchange}_latency_data.json')
    if not os.path.exists(data_file):
        print(f"Error: Latency data file not found at {data_file}")
        return []
    
    with open(data_file, 'r') as file:
        try:
            data = json.load(file)
            return data
        except json.JSONDecodeError:
            print(f"Error: Failed to parse {data_file}")
            return []

def generate_latency_report(exchange, data):
    """
    Generate latency report chart for a specific exchange
    
    Args:
        exchange (str): Exchange name
        data (list): Latency data records
    
    Returns:
        bool: True if successful, False otherwise
    """
    if not data:
        print(f"Error: No latency data available for {exchange}")
        return False
    
    # Set custom font
    font_prop = set_custom_font()
    
    # Extract time and latency data
    timestamps = [entry['timestamp'] for entry in data]
    dates = [datetime.fromtimestamp(int(ts)) for ts in timestamps]  # Ensure timestamps are integers
    latencies = [entry['latency'] for entry in data]  # already in milliseconds
    
    # Calculate statistics (removed max and min latency)
    avg_latency = np.mean(latencies)
    p95_latency = np.percentile(latencies, 95)
    
    # Create chart
    plt.figure(figsize=(12, 7))
    
    # Main chart - latency time series
    plt.subplot(111)
    plt.plot(dates, latencies, 'b-', linewidth=1, alpha=0.7)
    plt.plot(dates, latencies, 'bo', markersize=3)
    
    # Set x-axis date format
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    plt.gcf().autofmt_xdate()  # Auto-rotate date labels
    
    # Add title and labels
    beijing_tz = timezone(timedelta(hours=8))
    current_time = datetime.now(beijing_tz).isoformat(timespec='seconds')
    exchange_name = exchange.upper()
    title = f'{exchange_name} API Latency Report (Generated at {current_time})'
    xlabel = 'Time'
    ylabel = 'Latency (ms)'
    
    if font_prop:
        plt.title(title, fontproperties=font_prop)
        plt.xlabel(xlabel, fontproperties=font_prop)
        plt.ylabel(ylabel, fontproperties=font_prop)
    else:
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Add statistics (removed max and min latency)
    stats_text = (
        f"Statistics:\n"
        f"Samples: {len(latencies)}\n"
        f"Avg Latency: {avg_latency:.2f} ms\n"
        f"95th Percentile: {p95_latency:.2f} ms"
    )
    
    plt.annotate(stats_text, xy=(0.02, 0.97), xycoords='axes fraction',
                bbox=dict(boxstyle="round,pad=0.5", fc="white", alpha=0.8),
                va='top', ha='left', fontsize=9, 
                fontproperties=font_prop if font_prop else None)
    
    # Draw average and 95% lines
    avg_label = f'Avg: {avg_latency:.2f} ms'
    p95_label = f'P95: {p95_latency:.2f} ms'
        
    plt.axhline(y=avg_latency, color='r', linestyle='-', alpha=0.5, label=avg_label)
    plt.axhline(y=p95_latency, color='g', linestyle='--', alpha=0.5, label=p95_label)
    
    plt.legend(loc='upper right', prop=font_prop if font_prop else None)
    
    # Save chart with a fixed filename to overwrite old reports
    report_file = os.path.join(REPORTS_DIR, f'{exchange}_latency_report.png')
    plt.savefig(report_file, dpi=300, bbox_inches='tight')
    print(f"Report generated: {report_file}")
    
    # Close chart
    plt.close()
    
    return True

def generate_all_reports():
    """Generate reports for both Bitget and OKX exchanges"""
    exchanges = ["bitget", "okx"]
    
    print(f"Generating reports for exchanges: {', '.join(exchanges)}")
    
    for exchange in exchanges:
        print(f"\nGenerating report for {exchange.upper()}...")
        data = load_latency_data(exchange)
        
        if data:
            print(f"Loaded {len(data)} latency data records")
            if generate_latency_report(exchange, data):
                print(f"Report generation successful for {exchange}")
            else:
                print(f"Report generation failed for {exchange}")
        else:
            print(f"Error: No latency data available for {exchange}")

def main():
    """Main function"""
    print("Generating Exchange API latency reports...")
    generate_all_reports()

if __name__ == "__main__":
    main() 