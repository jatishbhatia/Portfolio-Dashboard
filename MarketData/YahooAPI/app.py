from flask import Flask, render_template, request, jsonify
from datetime import datetime
from market_data_source import get_market_data  # Import your function here

app = Flask(
    __name__,
    template_folder='Dashboard',  # Set template folder to Dashboard
    static_folder='Dashboard'  # Set static folder to Dashboard
)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_python_code', methods=['POST'])
def run_python_code():
    # Extract parameters from request
    data = request.json
    name = data.get('name', 'AAPL')  # Default to 'AAPL' if not provided
    start = datetime.strptime(data.get('start', '2022-01-01'), '%Y-%m-%d')
    end = datetime.strptime(data.get('end', '2022-12-31'), '%Y-%m-%d')
    interval = data.get('interval', '1d')

    result = get_market_data(name, start, end, interval)
    
    # Convert result to JSON serializable format
    result_json = result.to_json(orient='split')
    return jsonify(result=result_json)

if __name__ == '__main__':
    app.run(debug=True)
