from fastapi import APIRouter, HTTPException
from fastapi_limiter.depends import RateLimiter
import requests
from functools import lru_cache

router = APIRouter()

@lru_cache(maxsize=100)
def fetch_stock_data(symbol: str, api_key: str):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    return response.json()

@router.get("/{symbol}")
async def get_stock(symbol: str):
    try:
        api_key = "YOUR_ALPHA_VANTAGE_API_KEY"  # Replace with your actual key
        data = fetch_stock_data(symbol, api_key)
        
        if "Error Message" in data:
            raise HTTPException(status_code=400, detail="Invalid stock symbol")
            
        time_series = data.get("Time Series (Daily)", {})
        
        formatted_data = {
            "symbol": symbol,
            "data": [
                {
                    "date": date,
                    "open": values["1. open"],
                    "high": values["2. high"],
                    "low": values["3. low"],
                    "close": values["4. close"],
                    "volume": values["5. volume"]
                }
                for date, values in time_series.items()
            ]
        }
        
        return {
            "success": True,
            "data": formatted_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
