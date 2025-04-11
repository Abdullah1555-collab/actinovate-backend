from fastapi import HTTPException

class InvalidSymbolException(HTTPException):
    def __init__(self, symbol: str):
        super().__init__(
            status_code=400,
            detail=f"Invalid stock symbol: {symbol}"
        )

class RateLimitException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=429,
            detail="Too many requests"
        )
