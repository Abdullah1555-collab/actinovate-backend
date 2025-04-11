import requests
from functools import lru_cache
from app.core.config import settings
from app.core.exceptions import CustomHTTPException
from app.utils.logger import logger

@lru_cache(maxsize=128)
async def get_stock_data(symbol: str, timeframe: str = "1D", indicators: str = None):
    base_url = "https://www.alphavantage.co/query"
    function = {
        "1D": "TIME_SERIES_DAILY",
        "1W": "TIME_SERIES_WEEKLY",
        "1M": "TIME_SERIES_MONTHLY"
    }.get(timeframe, "TIME_SERIES_DAILY")
    
    url = f"{base_url}?function={function}&symbol={symbol}&apikey={settings.ALPHA_VANTAGE_API_KEY}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "Error Message" in data:
            raise CustomHTTPException(400, data["Error Message"])
            
        time_series_key = next((k for k in data.keys() if "Time Series" in k), None)
        if not time_series_key:
            raise CustomHTTPException(404, "No time series data found")
            
        return {
            "meta": {
                "symbol": data.get("Meta Data", {}).get("2. Symbol", symbol),
                "lastRefreshed": data.get("Meta Data", {}).get("3. Last Refreshed", ""),
            },
            "values": [
                {
                    "datetime": date,
                    "open": float(values["1. open"]),
                    "high": float(values["2. high"]),
                    "low": float(values["3. low"]),
                    "close": float(values["4. close"]),
                    "volume": int(values["5. volume"])
                }
                for date, values in data[time_series_key].items()
            ]
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        raise CustomHTTPException(502, "Failed to fetch stock data")
