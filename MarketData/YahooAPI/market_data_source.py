from flask import Flask, jsonify
import pandas as pd
import yfinance as yf
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

@app.route("/api/get_market_data/<string:stock>/<string:start_date>/<string:end_date>/<string:interval>", methods=['GET'])
def get_market_data_solution(stock, start_date, end_date, interval):
    start_date_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')
    df = get_market_data(stock, start_date_dt, end_date_dt, interval)
    return df.to_json(orient='records')

def get_market_data(name: str, start: datetime, end: datetime, interval: str):
    """
    start: inclusive
    end: exclusive
    """
    start_date = start.strftime('%Y-%m-%d')
    end_date = end.strftime('%Y-%m-%d')
    return yf.download(name, start=start_date, end=end_date, interval=interval)[['Open']]

if __name__ == "__main__":
    app.run(debug=True)
