
from fastapi import FastAPI, HTTPException
import requests
import pandas as pd
from functools import lru_cache
from config import (
    ALPHA_VANTAGE_API_KEY, GOOGLE_FINANCE_API_KEY, 
    ALPHA_VANTAGE_BASE_URL, GOOGLE_FINANCE_BASE_URL
)

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your frontend's URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@lru_cache(maxsize=10)
def get_stock_data_alpha(symbol: str):
    """
    Get intraday stock data (5-minute interval) from Alpha Vantage.
    This endpoint works on the FREE tier.
    """
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url)
    data = response.json()

    # Optional: Clean the data for frontend
    if "Time Series (5min)" in data:
        latest_time = sorted(data["Time Series (5min)"].keys())[-1]
        return {
            "symbol": symbol,
            "latest": data["Time Series (5min)"][latest_time],
            "timestamp": latest_time
        }
    else:
        return {"error": "No data found or request limit exceeded", "raw": data}

@lru_cache(maxsize=10)
def get_stock_data_google(query: str):
    """Fetch stock data from Google Finance (via SerpAPI)."""
    url = f"{GOOGLE_FINANCE_BASE_URL}?engine=google_finance&q={query}&api_key={GOOGLE_FINANCE_API_KEY}"
    return fetch_stock_data(url)

def fetch_stock_data(url: str):
    """Generic function to fetch stock data from an API URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data:
            raise HTTPException(status_code=400, detail="Invalid stock symbol or API limit exceeded.")

        return data
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"API request failed: {str(e)}")

@app.get("/stock/{symbol}/alpha")
def stock_analysis_alpha(symbol: str):
    return get_stock_data_alpha(symbol)

@app.get("/stock/{query}/google")
def stock_analysis_google(query: str):
    return get_stock_data_google(query)

@app.get("/")
def root():
    return {"message": "Actinovate Backend is Live ✅"}
@app.get("/")
def root():
    return {"message": "Actinovate Backend is Live ✅"}
