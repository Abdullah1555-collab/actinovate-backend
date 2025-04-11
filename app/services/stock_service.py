from fastapi import APIRouter, HTTPException, Depends
from fastapi_limiter.depends import RateLimiter
from app.core.config import settings
from app.models.responses import StockResponse
from app.core.exceptions import InvalidSymbolException
import requests
from functools import lru_cache

router = APIRouter()

@lru_cache(maxsize=100)
def get_cached_stock_data(symbol: str):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={settings.ALPHA_VANTAGE_API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        raise InvalidSymbolException(symbol)

@router.get("/{symbol}", 
           response_model=StockResponse,
           dependencies=[Depends(RateLimiter(times=5, minutes=1))])
async def get_stock_data(symbol: str):
    try:
        data = get_cached_stock_data(symbol)
        
        if "Error Message" in data:
            raise InvalidSymbolException(symbol)
            
        time_series = data.get("Time Series (Daily)", {})
        
        formatted_data = {
            "meta": {
                "symbol": symbol,
                "last_refreshed": data.get("Meta Data", {}).get("3. Last Refreshed", "")
            },
            "values": [
                {
                    "date": date,
                    "open": float(values["1. open"]),
                    "high": float(values["2. high"]),
                    "low": float(values["3. low"]),
                    "close": float(values["4. close"]),
                    "volume": int(values["5. volume"])
                }
                for date, values in time_series.items()
            ]
        }
        
        return StockResponse(
            success=True,
            symbol=symbol,
            data=formatted_data
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
