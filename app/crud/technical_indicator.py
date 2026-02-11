from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import date, datetime
import pandas as pd
from typing import List, Optional

from app.models.technical_indicator import TechnicalIndicator

def save_indicators(db: Session, df: pd.DataFrame) -> int:
    """
    Save technical indicators from DataFrame to database.
    
    Args:
        db: Database session
        df: DataFrame with calculated indicators
    
    Returns:
        Number of records saved
    """
    saved_count = 0
    
    for _, row in df.iterrows():
        # Skip rows where all indicators are NaN
        if pd.isna(row['sma_20']) and pd.isna(row['rsi_14']):
            continue
        
        # Convert date format if needed (from pandas timestamp to sql date)
        if isinstance(row['date'], pd.Timestamp):
            row_date = row['date'].date()
        else:
            row_date = row['date']
        
        # Check if record already exists
        existing = db.query(TechnicalIndicator).filter(
            and_(
                TechnicalIndicator.symbol == row['symbol'],
                TechnicalIndicator.date == row_date
            )
        ).first()
        
        if existing:
            # Update existing record
            for key in ['sma_20', 'sma_50', 'sma_200', 'ema_12', 'ema_26',
                        'rsi_14', 'macd', 'macd_signal', 'macd_histogram',
                        'bb_upper', 'bb_middle', 'bb_lower', 'bb_width']:
                value = row[key]
                # Convert NaN to None (NULL in database)
                setattr(existing, key, None if pd.isna(value) else float(value))
            saved_count += 1
        else:
            # Create new record
            indicator = TechnicalIndicator(
                symbol=row['symbol'],
                date=row_date,
                sma_20=None if pd.isna(row['sma_20']) else float(row['sma_20']),
                sma_50=None if pd.isna(row['sma_50']) else float(row['sma_50']),
                sma_200=None if pd.isna(row['sma_200']) else float(row['sma_200']),
                ema_12=None if pd.isna(row['ema_12']) else float(row['ema_12']),
                ema_26=None if pd.isna(row['ema_26']) else float(row['ema_26']),
                rsi_14=None if pd.isna(row['rsi_14']) else float(row['rsi_14']),
                macd=None if pd.isna(row['macd']) else float(row['macd']),
                macd_signal=None if pd.isna(row['macd_signal']) else float(row['macd_signal']),
                macd_histogram=None if pd.isna(row['macd_histogram']) else float(row['macd_histogram']),
                bb_upper=None if pd.isna(row['bb_upper']) else float(row['bb_upper']),
                bb_middle=None if pd.isna(row['bb_middle']) else float(row['bb_middle']),
                bb_lower=None if pd.isna(row['bb_lower']) else float(row['bb_lower']),
                bb_width=None if pd.isna(row['bb_width']) else float(row['bb_width'])
            )
            db.add(indicator)
            saved_count += 1
    
    db.commit()
    return saved_count

def get_latest_indicators(db: Session, symbol: str) -> Optional[TechnicalIndicator]:
    """
    Get the most recent technical indicators for a symbol.
    
    Args:
        db: Database session
        symbol: Stock symbol
    
    Returns:
        TechnicalIndicator object or None
    """
    return db.query(TechnicalIndicator).filter(TechnicalIndicator.symbol == symbol).order_by(TechnicalIndicator.date.desc()).first()

def get_indicators_by_date_range(
    db: Session, 
    symbol: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    limit: int = 100
) -> List[TechnicalIndicator]:
    """
    Get technical indicators for a symbol within a date range.
    
    Args:
        db: Database session
        symbol: Stock symbol
        start_date: Start date (optional)
        end_date: End date (optional)
        limit: Maximum number of records
    
    Returns:
        List of TechnicalIndicator objects
    """
    query = db.query(TechnicalIndicator).filter(TechnicalIndicator.symbol == symbol)
    
    if start_date:
        query = query.filter(TechnicalIndicator.date >= start_date)
    if end_date:
        query = query.filter(TechnicalIndicator.date <= end_date)
    
    return query.order_by(TechnicalIndicator.date.desc()).limit(limit).all()