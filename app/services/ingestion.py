from sqlalchemy.orm import Session
from app.crud.stock import create_stock_price
from app.services.alpha_vantage import AlphaVantageClient
from app.schemas.stock import StockPriceCreate

client = AlphaVantageClient()

def ingest_stock_data(db: Session, symbol: str) -> dict:
    """Fetch daily stock prices from Alpha Vantage and persist them to the database.

    Retrieves raw daily price data for the given ticker symbol, parses it,
    and saves each record via the CRUD layer. Duplicates or invalid entries
    are silently skipped.

    Args:
        db: active SQLAlchemy database session.
        symbol: ticker symbol to ingest (e.g. "AAPL").

    Returns:
        a dict with keys 'symbol', 'saved', 'skipped', and 'total'.
    """
    print(f"\nWorking...")

    raw_data = client.get_daily_prices(symbol)
    parsed_data = client.parse_daily_prices(raw_data)

    saved = 0
    skipped = 0

    for day in parsed_data:
        try:
            stock_data = StockPriceCreate(**day)
            create_stock_price(db, stock_data)
            saved += 1
        except Exception as e:
            skipped += 1
            print(e)
            continue

    result = {
        "symbol": symbol,
        "saved": saved,
        "skipped": skipped,
        "total": len(parsed_data)
    }

    print(f"{symbol}: {saved} saved, {skipped} skipped")
    return result