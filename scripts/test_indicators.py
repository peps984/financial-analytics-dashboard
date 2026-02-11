import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import Session
from app.services.technical_indicator import TechnicalIndicatorsService

# Create database session
db = Session()

try:
    # Create service
    service = TechnicalIndicatorsService(db)
    
    print("Calculating indicators for AAPL...\n")
    
    # Calculate indicators
    df = service.calculate_indicators("AAPL", days=200)
    
    print(f"Indicators calculated for {len(df)} days\n")
    
    # Show first and last 5 rows
    print("First and last 5 days:")
    
    print(df[['date', 'close', 'sma_20', 'rsi_14', 'macd']].head())
    print("...")
    print(df[['date', 'close', 'sma_20', 'rsi_14', 'macd']].tail())
    
finally:
    db.close()