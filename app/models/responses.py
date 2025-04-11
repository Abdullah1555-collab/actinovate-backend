from pydantic import BaseModel
from typing import Optional, Dict, Any

class StockResponse(BaseModel):
    success: bool
    symbol: str
    data: Dict[str, Any]
    error: Optional[str] = None
    message: Optional[str] = None
