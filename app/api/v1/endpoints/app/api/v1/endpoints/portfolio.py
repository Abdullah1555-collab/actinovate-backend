from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import List
from app.models.schemas import PortfolioCreate, PortfolioResponse
from app.services.portfolio_service import (
    create_portfolio,
    get_portfolios,
    get_portfolio,
    update_portfolio,
    delete_portfolio
)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/portfolios", response_model=PortfolioResponse)
async def create_user_portfolio(
    portfolio: PortfolioCreate,
    token: str = Depends(oauth2_scheme)
):
    """Create a new portfolio matching your frontend's structure"""
    try:
        return await create_portfolio(portfolio, token)
    except Exception as e:
        raise HTTPException(
            status_code=getattr(e, "status_code", 400),
            detail=getattr(e, "detail", str(e))
        )

@router.get("/portfolios", response_model=List[PortfolioResponse])
async def read_user_portfolios(token: str = Depends(oauth2_scheme)):
    """Get all portfolios for the current user"""
    try:
        return await get_portfolios(token)
    except Exception as e:
        raise HTTPException(
            status_code=getattr(e, "status_code", 404),
            detail=getattr(e, "detail", str(e))
        )
