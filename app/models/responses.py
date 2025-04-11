from pydantic import BaseModel

class StandardResponse(BaseModel):
    success: bool
    data: dict | None = None
    error: str | None = None

class StockResponse(StandardResponse):
    symbol: str
    timeframe: str
