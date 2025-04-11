from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter
from app.services.stock_service import get_stock_data
from app.models.schemas import StockResponse

router = APIRouter()

@router.get("/{symbol}", response_model=StockResponse)
async def get_stock(
    symbol: str,
    timeframe: str = "1D",
    indicators: str = None,
    _=Depends(RateLimiter(times=10, minutes=1))
):
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
