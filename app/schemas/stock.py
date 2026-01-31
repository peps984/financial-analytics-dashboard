from pydantic import BaseModel, Field, PositiveFloat, PositiveInt
from datetime import date

class StockPriceBase(BaseModel):
    symbol: str = Field(..., max_length = 10)
    date:date
    open: PositiveFloat
    high: PositiveFloat
    low: PositiveFloat
    close: PositiveFloat
    volume: PositiveInt

class StockPriceCreate(StockPriceBase):
    pass

class StockPriceResponse(StockPriceBase):
    id: int
    
    class Config:
        from_attributes = True