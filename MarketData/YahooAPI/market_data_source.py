import time
from datetime import datetime
import pandas as pd
import yfinance as yf


def get_market_data(name: str, start: datetime, end: datetime, interval: str):
    """
    start: inclusive
    end: exclusive
    """
    start_date = start.strftime('%Y-%m-%d')
    end_date = end.strftime('%Y-%m-%d')
    return yf.download(name, start=start_date, end=end_date, interval=interval)[['Open']]


