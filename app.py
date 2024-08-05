from flask import Flask, render_template, request, jsonify
from datetime import datetime

from Backend.MarketData.YahooAPI.market_data_source import get_market_data, get_current_price, get_stock_info  # Import your function here
from Backend.Database.DB_communication import (
    create_asset, read_assets, update_asset, delete_asset,
    create_category, read_categories, update_category, delete_category,
    create_transaction, read_transactions, update_transaction, delete_transaction
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
    return render_template('index.html', assets=assets),200
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


if __name__ == '__main__':
    app.run(debug=True)

'''
@app.route('/categories', methods=['POST'])
def add_category():
    data = request.json
    response, status_code = create_category(data['name'], data['description'])
    return jsonify(response), status_code

@app.route('/categories', methods=['GET'])
def get_categories():
    response, status_code = read_categories()
    return jsonify(response), status_code

@app.route('/categories/<string:name>', methods=['PUT'])
def edit_category(name):
    data = request.json
    response, status_code = update_category(name, data['description'])
    return jsonify(response), status_code

@app.route('/categories/<string:name>', methods=['DELETE'])
def remove_category(name):
    response, status_code = delete_category(name)
    return jsonify(response), status_code

# CRUD operations for Asset
@app.route('/assets', methods=['POST'])
def add_asset():
    data = request.json
    response, status_code = create_asset(
        data['symbol'], data['name'], data['category_name'], data['total_purchase_price']
    )
    return jsonify(response), status_code

@app.route('/assets', methods=['GET'])
def get_assets():
    response, status_code = read_assets()
    return jsonify(response), status_code

@app.route('/assets/<int:id>', methods=['PUT'])
def edit_asset(id):
    data = request.json
    response, status_code = update_asset(
        id, data['symbol'], data['name'], data['category_name'], data['total_purchase_price']
    )
    return jsonify(response), status_code

@app.route('/assets/<int:id>', methods=['DELETE'])
def remove_asset(id):
    response, status_code = delete_asset(id)
    return jsonify(response), status_code

# CRUD operations for Transaction
@app.route('/transactions', methods=['POST'])
def add_transaction():
    data = request.json
    response, status_code = create_transaction(
        data['asset_id'], data['transaction_type'], data['quantity'], data['price'], data['transaction_date']
    )
    return jsonify(response), status_code

@app.route('/transactions', methods=['GET'])
def get_transactions():
    response, status_code = read_transactions()
    return jsonify(response), status_code

@app.route('/transactions/<int:id>', methods=['PUT'])
def edit_transaction(id):
    data = request.json
    response, status_code = update_transaction(
        id, data['asset_id'], data['transaction_type'], data['quantity'], data['price'], data['transaction_date']
    )
    return jsonify(response), status_code

@app.route('/transactions/<int:id>', methods=['DELETE'])
def remove_transaction(id):
    response, status_code = delete_transaction(id)
    return jsonify(response), status_code
'''