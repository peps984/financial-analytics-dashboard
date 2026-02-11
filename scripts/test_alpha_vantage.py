import sys
from pathlib import Path

# Adjustment needed to import modules from parent subdirectories
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.alpha_vantage import AlphaVantageClient

client = AlphaVantageClient()

print("Calling API Alpha Vantage...\n")
print(f"Rate limit: {client.min_interval:.0f} seconds between calls\n")

try:
    raw_data = client.get_daily_prices("AAPL")
    
    print("Raw data acquired!\n")
    
    parsed_data = client.parse_daily_prices(raw_data)
    
    print("First 3 days available:")
    for day in parsed_data[:3]:
        print(f"{day}")

except Exception as e:
    print(f"Error: {e}")