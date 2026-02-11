from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class TechnicalIndicatorBase(BaseModel):
    """Base schema for technical indicators"""
    symbol: str = Field(..., max_length = 10)
    date:date
    
    # Moving averages
    sma_20: Optional[float] = None
    sma_50: Optional[float] = None
    sma_200: Optional[float] = None
    ema_12: Optional[float] = None
    ema_26: Optional[float] = None
    
    # Momentum indicators
    rsi_14: Optional[float] = None
    
    # MACD (Moving Average Convergence Divergence)
    macd: Optional[float] = None
    macd_signal: Optional[float] = None
    macd_histogram: Optional[float] = None
    
    # Volatility indicators
    bb_upper: Optional[float] = None
    bb_middle: Optional[float] = None
    bb_lower: Optional[float] = None
    bb_width: Optional[float] = None

class TechnicalIndicatorResponse(TechnicalIndicatorBase):
    """Response schema with id"""
    id: int
    
    class Config:
        from_attributes = True