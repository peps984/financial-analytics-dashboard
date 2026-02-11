import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import Session
from app.services.technical_indicator import TechnicalIndicatorsService
from app.crud.technical_indicator import save_indicators, get_latest_indicators

db = Session()

try:
    # Create service
    service = TechnicalIndicatorsService(db)
    
    print("Calculating indicators for AAPL...\n")
    
    # Calculate indicators
    df = service.calculate_indicators("AAPL", days=200)
    
    print(f"Indicators calculated for {len(df)} days\n")
    
    print("Writing the database...")
    saved = save_indicators(db, df)
    print(f"{saved} records saved\n")
    
    print("Reading latest indicators from database...")
    latest = get_latest_indicators(db, "AAPL")
    
    if latest:
        print(f"Date: {latest.date}")
        print(f"SMA 20: {latest.sma_20:.2f}" if latest.sma_20 else "SMA 20: N/A")
        print(f"RSI 14: {latest.rsi_14:.2f}" if latest.rsi_14 else "RSI 14: N/A")
        print(f"MACD: {latest.macd:.4f}" if latest.macd else "MACD: N/A")
    else:
        print("No technical indicators found")
        
finally:
    db.close()