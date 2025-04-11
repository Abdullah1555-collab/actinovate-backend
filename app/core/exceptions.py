from fastapi import HTTPException

class StockDataException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=503,
            detail="Stock data service unavailable"
        )

class InvalidSymbolException(HTTPException):
    def __init__(self, symbol: str):
        super().__init__(
            status_code=400,
            detail=f"Invalid stock symbol: {symbol}"
        )
