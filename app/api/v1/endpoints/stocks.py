from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter
from typing import Dict, Any
from app.services.stock_service import get_stock_data
from app.models.schemas import StockResponse
from app.core.config import settings

router = APIRouter()

@router.get(
    "/stocks/{symbol}",
    response_model=StockResponse,
    dependencies=[Depends(RateLimiter(times=10, minutes=1))]
)
async def get_stock(
    symbol: str,
    timeframe: str = "1D",
    indicators: str = None
) -> Dict[str, Any]:
    """
    Get stock data with optional technical indicators
    Compatible with your frontend's StockChart component requirements
    """
    try:
        data = await get_stock_data(symbol, timeframe, indicators)
        return {
            "success": True,
            "symbol": symbol,
            "timeframe": timeframe,
            "data": data,
            "indicators": indicators.split(",") if indicators else []
        }
    except Exception as e:
        raise HTTPException(
            status_code=getattr(e, "status_code", 500),
            detail=getattr(e, "detail", str(e))
        )
