from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

# import for stock prices api
from app.core.database import get_db
from app.schemas.stock import StockPriceCreate, StockPriceResponse
from app.crud.stock import create_stock_price, get_stock_prices, get_stock_price_by_id
from app.services.ingestion import ingest_stock_data

# import for technical indicators api
from app.services.technical_indicator import TechnicalIndicatorsService
from app.crud.technical_indicator import save_indicators, get_latest_indicators, get_indicators_by_date_range
from app.schemas.technical_indicator import TechnicalIndicatorResponse
from datetime import date as date_type

router = APIRouter(prefix="/stocks", tags=["stocks"])

# stock prices api
@router.post("/", response_model=StockPriceResponse)
def add_stock_price(stock_data: StockPriceCreate, db: Session = Depends(get_db)):
    return create_stock_price(db, stock_data)

@router.get("/", response_model=List[StockPriceResponse])
def list_stock_prices(symbol: Optional[str] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_stock_prices(db, symbol, skip, limit)

@router.get("/{stock_id}", response_model=StockPriceResponse)
def get_stock_price(stock_id: int, db: Session = Depends(get_db)):
    stock = get_stock_price_by_id(db, stock_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock price not found")
    return stock

@router.post("/ingest/{symbol}")
def ingest_stock(symbol: str, db: Session = Depends(get_db)):
    result = ingest_stock_data(db, symbol)
    return result

# technical indicators api
@router.post("/{symbol}/indicators", response_model=dict)
def calculate_and_save_indicators(symbol: str, db: Session = Depends(get_db)):
    """
    Calculate technical indicators for a symbol and save to database.
    
    Returns summary of calculation results.
    """
    service = TechnicalIndicatorsService(db)
    
    try:
        # Calculate indicators
        df = service.calculate_indicators(symbol, days=200)
        
        # Save to database
        saved_count = save_indicators(db, df)
        
        # Get latest for response
        latest = get_latest_indicators(db, symbol)
        
        return {
            "symbol": symbol,
            "calculated": len(df),
            "saved": saved_count,
            "latest_date": str(latest.date) if latest else None,
            "status": "success"
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating indicators: {str(e)}")

@router.get("/{symbol}/indicators/latest", response_model=TechnicalIndicatorResponse)
def get_latest_indicator(symbol: str, db: Session = Depends(get_db)):
    """
    Get the most recent technical indicators for a symbol.
    """
    indicator = get_latest_indicators(db, symbol)
    
    if not indicator:
        raise HTTPException(
            status_code=404, 
            detail=f"No indicators found for symbol {symbol}"
        )
    
    return indicator

@router.get("/{symbol}/indicators", response_model=List[TechnicalIndicatorResponse])
def list_indicators(
    symbol: str,
    start_date: Optional[date_type] = None,
    end_date: Optional[date_type] = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get technical indicators for a symbol, optionally filtered by date range.
    """
    indicators = get_indicators_by_date_range(db, symbol, start_date, end_date, limit)
    
    if not indicators:
        raise HTTPException(
            status_code=404,
            detail=f"No indicators found for symbol {symbol}"
        )
    
    return indicators

@router.post("/{symbol}/full-ingest")
def full_ingest_with_indicators(symbol: str, db: Session = Depends(get_db)):
    """
    Complete ingestion: download prices + calculate indicators.
    
    This is a convenience endpoint that combines:
    1. POST /stocks/ingest/{symbol}
    2. POST /stocks/{symbol}/indicators
    """
    # Step 1: Ingest prices
    try:
        price_result = ingest_stock_data(db, symbol)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Price ingestion failed: {str(e)}")
    
    # Step 2: Calculate indicators
    try:
        service = TechnicalIndicatorsService(db)
        df = service.calculate_indicators(symbol, days=200)
        saved_count = save_indicators(db, df)
        latest = get_latest_indicators(db, symbol)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Indicator calculation failed: {str(e)}")
    
    return {
        "symbol": symbol,
        "prices": {
            "saved": price_result["saved"],
            "skipped": price_result["skipped"]
        },
        "indicators": {
            "calculated": len(df),
            "saved": saved_count,
            "latest_date": str(latest.date) if latest else None
        },
        "status": "success"
    }