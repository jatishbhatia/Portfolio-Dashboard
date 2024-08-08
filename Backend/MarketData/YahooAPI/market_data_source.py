import yfinance as yf
from datetime import datetime, time


def get_market_data(name: str, start: datetime, end: datetime, interval: str):
    """
    start: inclusive
    end: exclusive
    """
    start_date = start.strftime('%Y-%m-%d')
    end_date = end.strftime('%Y-%m-%d')
    return yf.download(name, start=start_date, end=end_date, interval=interval)[['Open', 'High', 'Low', 'Close']]


def get_current_price(stock_name: str):
    ticker = yf.Ticker(stock_name)
    data = ticker.history(period='1d', interval='1m')
    if data.empty:
        raise ValueError(f"Stock symbol {stock_name} not found.")
    return data['Close'].iloc[-1]


def get_stock_info(stock_name):
    ticker = yf.Ticker(stock_name)
    return ticker.info


def get_asset_name(ticker_name: str) -> str:
    stock_info = get_stock_info(ticker_name)
    if "longName" in stock_info:
        return stock_info["longName"]
    else:
        raise KeyError("longName not found in stock info")

        