from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.stock import StockPriceCreate, StockPriceResponse
from app.crud.stock import create_stock_price, get_stock_prices, get_stock_price_by_id

router = APIRouter(prefix="/stocks", tags=["stocks"])

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