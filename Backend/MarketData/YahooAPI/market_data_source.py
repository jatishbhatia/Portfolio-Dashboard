from flask import Flask, jsonify
import yfinance as yf
from datetime import datetime


def get_market_data(name: str, start: datetime, end: datetime, interval: str):
    """
    start: inclusive
    end: exclusive
    """
    start_date = start.strftime('%Y-%m-%d')
    end_date = end.strftime('%Y-%m-%d')
    return yf.download(name, start=start_date, end=end_date, interval=interval)[['Open']]
