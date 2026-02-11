from datetime import datetime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String, Float, Date, UniqueConstraint
from app.core.database import Base

class TechnicalIndicator(Base):
    """
    Technical indicators calculated from price data.
    One row per symbol per date.
    """
    
    __tablename__ = "technical_indicators"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    symbol: Mapped[str] = mapped_column(String(10))
    date: Mapped[datetime] = mapped_column(Date, index = True)
    
    # Moving averages
    sma_20: Mapped[float] = mapped_column(Float, nullable=True)   # Simple moving average 20 days
    sma_50: Mapped[float] = mapped_column(Float, nullable=True)   # Simple moving average 50 days
    sma_200: Mapped[float] = mapped_column(Float, nullable=True)  # Simple moving average 200 days
    ema_12: Mapped[float] = mapped_column(Float, nullable=True)   # Exponential moving average 12 days
    ema_26: Mapped[float] = mapped_column(Float, nullable=True)   # Exponential moving average 26 days
    
    # Momentum indicators
    rsi_14: Mapped[float] = mapped_column(Float, nullable=True)   # Relative Strength Index 14 days
    
    # MACD (Moving Average Convergence Divergence)
    macd: Mapped[float] = mapped_column(Float, nullable=True)          # MACD line
    macd_signal: Mapped[float] = mapped_column(Float, nullable=True)   # Signal line
    macd_histogram: Mapped[float] = mapped_column(Float, nullable=True) # MACD histogram
    
    # Volatility indicators
    bb_upper: Mapped[float] = mapped_column(Float, nullable=True)   # Bollinger band upper
    bb_middle: Mapped[float] = mapped_column(Float, nullable=True)  # Bollinger band middle (SMA 20)
    bb_lower: Mapped[float] = mapped_column(Float, nullable=True)   # Bollinger band lower
    bb_width: Mapped[float] = mapped_column(Float, nullable=True)   # Bollinger band width
    
    # Ensure one row per symbol per date
    __table_args__ = (
        UniqueConstraint('symbol', 'date', name='uix_symbol_date'),
    )