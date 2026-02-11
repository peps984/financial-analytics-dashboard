import pandas as pd
import talib
from sqlalchemy.orm import Session
from app.models.stock import StockPrice

class TechnicalIndicatorsService:
    """
    Service to calculate technical indicators from price data.
    Uses TA-Lib library for calculations.
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def calculate_indicators(self, symbol: str, days: int = 200) -> pd.DataFrame:
        """
        Calculate technical indicators for a given symbol
        
        Args:
            symbol: ticker symbol (e.g. "AAPL").
            days: number of days to fetch (default 200 for SMA 200)
        
        Returns:
            a pandas dataframe with prices and calculated indicators
        """
        prices = self.db.query(StockPrice).filter(StockPrice.symbol == symbol).order_by(StockPrice.date.asc()).limit(days).all()
        
        if not prices:
            raise ValueError(f"No price data found for symbol {symbol}")
        
        if len(prices) < 20:
            raise ValueError(f"Insufficient data for {symbol}. Need at least 20 days of data, got {len(prices)}")
        
        # Convert to pandas DataFrame
        df = pd.DataFrame([{
            'date': p.date,
            'open': float(p.open),
            'high': float(p.high),
            'low': float(p.low),
            'close': float(p.close),
            'volume': int(p.volume)
        } for p in prices])
        
        # Convert date to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Calculate indicators using TA-Lib
        
        # Moving averages
        df['sma_20'] = talib.SMA(df['close'], timeperiod=20)
        df['sma_50'] = talib.SMA(df['close'], timeperiod=50)
        df['sma_200'] = talib.SMA(df['close'], timeperiod=200)
        
        # Exponential moving averages
        df['ema_12'] = talib.EMA(df['close'], timeperiod=12)
        df['ema_26'] = talib.EMA(df['close'], timeperiod=26)
        
        # Momentum indicators
        df['rsi_14'] = talib.RSI(df['close'], timeperiod=14)
        
        # MACD (Moving Average Convergence Divergence)
        macd, macd_signal, macd_hist = talib.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
        df['macd'] = macd
        df['macd_signal'] = macd_signal
        df['macd_histogram'] = macd_hist
        
        # Volatility indicators
        bb_upper, bb_middle, bb_lower = talib.BBANDS(df['close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
        #nbdevup/nbdevdn: number of standard deviations (2 = 95% interval)
        #matype=0: average type = SMA
        
        df['bb_upper'] = bb_upper
        df['bb_middle'] = bb_middle
        df['bb_lower'] = bb_lower
        # Calculate band width (percentage) because TA-Lib can't
        df['bb_width'] = ((bb_upper - bb_lower) / bb_middle) * 100
        
        # Add symbol
        df['symbol'] = symbol
        
        return df