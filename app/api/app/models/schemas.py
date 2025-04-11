from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class StockDataPoint(BaseModel):
    datetime: str
    open: float
    high: float
    low: float
    close: float
    volume: int

class StockMeta(BaseModel):
    symbol: str
    lastRefreshed: str
    timeframe: str

class StockResponse(BaseModel):
    success: bool
    symbol: str
    timeframe: str
    data: Dict[str, Any]
    indicators: Optional[List[str]] = None

class PortfolioCreate(BaseModel):
    name: str
    description: Optional[str] = None
    stocks: Dict[str, float]  # {symbol: weight}

class PortfolioResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    stocks: Dict[str, float]
    performance: Dict[str, float]app/models/schemas.py
