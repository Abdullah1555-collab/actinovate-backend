import requests
from functools import lru_cache
from typing import Dict, Any, Optional
from app.core.config import settings
from app.core.exceptions import CustomHTTPException
from app.utils.logger import logger

@lru_cache(maxsize=128)
async def get_stock_data(
    symbol: str,
    timeframe: str = "1D",
    indicators: Optional[str] = None
) -> Dict[str, Any]:
    """
    Fetch stock data from Alpha Vantage with caching
    Supports multiple timeframes and indicators that match your frontend needs
    """
    base_url = settings.ALPHA_VANTAGE_BASE_URL
    
    # Map your frontend's timeframe to Alpha Vantage intervals
    timeframe_map = {
        "1D": "TIME_SERIES_DAILY",
        "1W": "TIME_SERIES_WEEKLY",
        "1M": "TIME_SERIES_MONTHLY"
    }
    
    function = timeframe_map.get(timeframe, "TIME_SERIES_DAILY")
    
    url = f"{base_url}?function={function}&symbol={symbol}&apikey={settings.ALPHA_VANTAGE_API_KEY}"
    
    try:
        logger.info(f"Fetching stock data for {symbol} ({timeframe})")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "Error Message" in data:
            raise CustomHTTPException(
                status_code=400,
                detail=data["Error Message"],
                error_code="API_ERROR"
            )
            
        # Transform data to match your frontend's expected format
        time_series_key = next((k for k in data.keys() if "Time Series" in k), None)
        if not time_series_key:
            raise CustomHTTPException(
                status_code=404,
                detail="No time series data found",
                error_code="NO_DATA"
            )
            
        transformed = {
            "meta": {
                "symbol": data.get("Meta Data", {}).get("2. Symbol", symbol),
                "lastRefreshed": data.get("Meta Data", {}).get("3. Last Refreshed", ""),
                "timeframe": timeframe
            },
            "values": [
                {
                    "datetime": key,
                    "open": float(values["1. open"]),
                    "high": float(values["2. high"]),
                    "low": float(values["3. low"]),
                    "close": float(values["4. close"]),
                    "volume": int(values["5. volume"])
                }
                for key, values in data[time_series_key].items()
            ]
        }
        
        # Add technical indicators if requested
        if indicators:
            transformed["indicators"] = await _add_technical_indicators(symbol, indicators)
            
        return transformed
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Stock data fetch error: {str(e)}")
        raise CustomHTTPException(
            status_code=502,
            detail="Failed to fetch stock data",
            error_code="NETWORK_ERROR"
        )

async def _add_technical_indicators(symbol: str, indicators: str) -> Dict[str, Any]:
    """Fetch and add technical indicators to stock data"""
    # Implementation for SMA, RSI, MACD etc.
    pass
