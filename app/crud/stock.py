from typing import Optional
from sqlalchemy.orm import Session
from app.models.stock import StockPrice
from app.schemas.stock import StockPriceCreate

def create_stock_price(db: Session, stock_data: StockPriceCreate):
    db_stock = StockPrice(**stock_data.model_dump())
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock

def get_stock_prices(db: Session, symbol: Optional[str] = None, skip: int = 0, limit: int = 100):
    query = db.query(StockPrice)
    if symbol:
        query = query.filter(StockPrice.symbol == symbol)
    return query.offset(skip).limit(limit).all()

def get_stock_price_by_id(db: Session, stock_id: int):
    return db.query(StockPrice).filter(StockPrice.id == stock_id).first()