from flask import Flask, render_template, request, jsonify
from datetime import datetime

from Backend.MarketData.YahooAPI.market_data_source import get_market_data, get_current_price, \
    get_stock_info, get_asset_name  # Import your function here
from Backend.Database.DB_communication import (
    create_asset, read_assets, update_asset, delete_asset,
    create_category, read_categories, update_category, delete_category,
    create_transaction, read_transactions, update_transaction, delete_transaction,
    buy_stock, sell_stock
)


class CashAmount:
    USD = 0


app = Flask(
    __name__,
    template_folder='Frontend/Dashboard',  # Set template folder to Dashboard
    static_folder='Frontend/Dashboard'  # Set static folder to Dashboard
)
app.config.from_object(CashAmount)


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
    assets = read_assets()
    return render_template('index.html', assets=assets)


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
    assets = read_assets()
    print(assets)
    return render_template('index.html', assets=assets), 200
    # return jsonify(assets),200
    # assets = fetch_assets()
    # print(assets)
    # return render_template('index.html', assets=assets)
    # return jsonify(assets), 200


@app.route("/api/get_current_price/<string:stock>")
def get_current_price_api(stock):
    return get_current_price(stock)


@app.route("/api/get_stock_info/<string:stock>")
def get_stock_info_api(stock):
    return get_stock_info(stock)


@app.route("/api/get_net_value")
def get_net_value():
    assets = read_assets()
    total_value = 0
    for asset in assets:
        stock_value = get_current_price(asset["symbol"])
        stock_quantity = asset["quantity"]
        total_value += stock_value * stock_quantity
    return total_value


 
@app.route("/api/add_funds/<int:deposit_amount>")
def add_funds(deposit_amount):
    CashAmount.USD += deposit_amount
 


@app.route("/api/get_funds")
def get_funds():
    return CashAmount.USD


@app.route("/api/get_unrealized_profit")
def get_unrealized_profit():
    assets = read_assets()
    profit = 0
    for asset in assets:
        if asset["category_name"] == 'Stock':
            profit += get_asset_unrealized_profit(asset)
    return profit


def get_asset_unrealized_profit(asset):
    purchase_price_total = asset["total_purchase_price"]
    total_current_asset_value = asset["quantity"] * get_current_price(asset["symbol"])
    return total_current_asset_value - purchase_price_total

 
@app.route('/buy_stock', methods=['POST'])
def buy_stock_endpoint():
    data = request.get_json()

    input_symbol = data.get('symbol')
    long_name = get_asset_name(input_symbol)
    purchase_price = get_current_price_api(input_symbol)
    input_quantity = data.get('quantity')

    if not input_symbol or not long_name or not purchase_price or not input_quantity:
        return jsonify({'error': 'Missing required parameters'}), 400

    result, status_code = buy_stock(input_symbol, long_name, purchase_price, input_quantity)
    return jsonify(result), status_code

@app.route('/sell_stock', methods=['POST'])
def sell_stock_endpoint():
    data = request.get_json()

    input_symbol = data.get('symbol')
    selling_price = get_current_price_api(input_symbol)
    input_quantity = data.get('quantity')

    if not input_symbol or not selling_price or not input_quantity:
        return jsonify({'error': 'Missing required parameters'}), 400

    result, status_code = sell_stock(input_symbol, selling_price, input_quantity)
    return jsonify(result), status_code

@app.route('/api/get_transactions')
def get_transactions():
    return read_transactions()


@app.route('/api/get_assets_market_price')
def get_assets_market_price():
    assets = read_assets()
    ticker_names = set()
    for asset in assets:
        ticker_names.add(asset["symbol"])

    ticker_price_dict ={}
    for ticker in ticker_names:
        price = get_current_price(ticker)
        ticker_price_dict[ticker] = price
    return ticker_price_dict


if __name__ == '__main__':
    app.run(debug=True)
