from flask import Flask, render_template, request, jsonify
from datetime import datetime

from Backend.MarketData.YahooAPI.market_data_source import get_market_data, get_current_price, get_stock_info  # Import your function here
from Backend.Database.DB_communication import (
    create_asset, fetch_assets, update_asset, delete_asset,
    create_category, fetch_categories, update_category, delete_category,
    create_asset_category, fetch_asset_categories, delete_asset_category
)


app = Flask(
    __name__,
    template_folder='Frontend/Dashboard',  # Set template folder to Dashboard
    static_folder='Frontend/Dashboard'  # Set static folder to Dashboard
)


def parse_request(data):
    """
    Helper function to parse the request data and return the parameters for get_market_data.
    """
    name = data.get('name', 'AAPL')  # Default to 'AAPL' if not provided
    start = datetime.strptime(data.get('start', '2022-01-01'), '%Y-%m-%d')
    end = datetime.strptime(data.get('end', '2022-12-31'), '%Y-%m-%d')
    interval = data.get('interval', '1d')
    return name, start, end, interval


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/run_python_code', methods=['POST'])
def run_python_code():
    try:
        # Extract parameters from request
        data = request.json
        name, start, end, interval = parse_request(data)

        # Run the Python function
        result = get_market_data(name, start, end, interval)
        # Convert result to JSON serializable format
        result_json = result.to_json(orient='split')
        return jsonify(result=result_json)
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route("/api/get_market_data/<string:stock>/<string:start_date>/<string:end_date>/<string:interval>",
           methods=['GET'])
def get_market_data_api(stock, start_date, end_date, interval):
    start_date_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')
    df = get_market_data(stock, start_date_dt, end_date_dt, interval)
    return df.to_json(orient='records')

@app.route('/assets', methods=['GET'])
def get_assets():
    assets = fetch_assets()
    return jsonify(assets), 200

@app.route("/api/get_current_price/<string:stock>")
def get_current_price_api(stock):
    return get_current_price(stock)


@app.route("/api/get_stock_info/<string:stock>")
def get_stock_info_api(stock):
    return get_stock_info(stock)


if __name__ == '__main__':
    app.run(debug=True)
