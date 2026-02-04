import httpx
import time
from app.core.config import settings

class AlphaVantageClient:
    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self):
        self.api_key = settings.ALPHA_VANTAGE_API_KEY
        self.last_call_time = 0 
        self.min_interval = 60 / settings.ALPHA_VANTAGE_RATE_LIMIT # minimum time between calls (seconds)

    def _wait_for_rate_limit(self):
        """
        Ensure a minimum interval between calls to avoid exceeding the rate limit.
        """
        elapsed = time.time() - self.last_call_time
        if elapsed < self.min_interval:
            wait_time = self.min_interval - elapsed
            print(f"⏳ Rate limit: waiting {wait_time:.1f} seconds...")
            time.sleep(wait_time)
        self.last_call_time = time.time()

    def get_daily_prices(self, symbol: str) -> dict:
        """
        Fetch the daily price time series for a stock symbol.

        Args:
            symbol: stock symbol (e.g., "AAPL")

        Returns:
            Raw Alpha Vantage response as a dict
        """
        self._wait_for_rate_limit()

        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "apikey": self.api_key,
            "outputsize": "compact"
        }

        response = httpx.get(self.BASE_URL, params=params)
        data = response.json()

        if "Error Message" in data:
            raise ValueError(f"Alpha Vantage error: {data['Error Message']}")

        if "Information" in data:
            raise ValueError(f"API limit reached: {data['Information']}")

        return data
    
    def parse_daily_prices(self, raw_data: dict) -> list[dict]:
        """
        Parse Alpha Vantage response into the database schema format.

        Args:
            raw_data: raw response from Alpha Vantage.

        Returns:
            List of records ready to insert into the database.
        """
        metadata = raw_data.get("Meta Data", {})
        symbol = metadata.get("2. Symbol")
        
        time_series = raw_data.get("Time Series (Daily)", {})
        parsed = []

        for date_str, values in time_series.items():
            parsed.append({
                "symbol": symbol,
                "date": date_str,
                "open": float(values["1. open"]),
                "high": float(values["2. high"]),
                "low": float(values["3. low"]),
                "close": float(values["4. close"]),
                "volume": int(values["5. volume"])
            })

        return parsed
