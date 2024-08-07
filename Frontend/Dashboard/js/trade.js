document.addEventListener('DOMContentLoaded', function () {
    const tradeButtons = document.querySelectorAll('.tradeButton');
    tradeButtons.forEach(button => {
        button.addEventListener('click', function () {
            const assetName = button.getAttribute('data-asset-name');
            const stockSymbol = button.getAttribute('data-stock-symbol');
            showTradePopup(assetName, stockSymbol);
        });
    });
});

function showTradePopup(assetName, stockSymbol) {
    fetch(`/api/get_current_price/${stockSymbol}`)
        .then(response => {
            if (!response.ok) {
                return response.json().then(error => {
                    throw new Error(error.error || 'Failed to fetch current price');
                });
            }
            return response.json();
        })
        .then(data => {
            Swal.fire({
                title: 'Trade',
                html: `
                    <div class="form-container">
                        <form id="tradeForm">
                            <div class="form-group">
                                <label for="transactionType">Transaction Type:</label>
                                <select id="transactionType" name="transactionType" required>
                                    <option value="buy">Buy</option>
                                    <option value="sell">Sell</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="stockSymbol">Stock Symbol:</label>
                                <input type="text" id="stockSymbol" name="stockSymbol" value="${assetName}" required>
                            </div>
                            <div class="form-group">
                                <label for="quantity">Quantity:</label>
                                <input type="number" id="quantity" name="quantity" required>
                            </div>
                            <div class="form-group">
                                <label for="price">Price per Share:</label>
                                <input type="number" id="price" name="price" step="0.01" value="${data.price}" required>
                            </div>
                        </form>
                    </div>
                `,
                showCloseButton: true,
                showCancelButton: true,
                confirmButtonText: 'Submit',
                focusConfirm: false,
                preConfirm: () => {
                    const form = Swal.getPopup().querySelector('#tradeForm');
                    if (!form.checkValidity()) {
                        Swal.showValidationMessage('Please check the information entered in the fields');
                        return false;
                    }
                    // Manually trigger form submission
                    submitForm();
                }
            });
        })
        .catch(error => {
            console.error('Error fetching current price:', error);
            Swal.fire('Error', `There was a problem fetching the current price: ${error.message}`, 'error');
        });
}

function submitForm() {
    const form = document.getElementById('tradeForm');
    const transactionType = form.querySelector('#transactionType').value;
    const stockSymbol = form.querySelector('#stockSymbol').value;
    const quantity = form.querySelector('#quantity').value;
    const price = form.querySelector('#price').value;

    const data = {
        symbol: stockSymbol,
        quantity: quantity,
        price: price
    };

    const url = transactionType === 'buy' ? '/api/buy_stock' : '/api/sell_stock';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => { throw new Error(text); });
        }
        return response.json();
    })
    .then(result => {
        console.log('Success:', result);
        updateTradeHistory(result);
    })
    .catch(error => {
        console.error('Error:', error);
        Swal.fire('Error', `There was a problem with your request: ${error.message}`, 'error');
    });
}

function updateTradeHistory(result) {
    const tradeHistoryTable = document.getElementById('tradeHistory').getElementsByTagName('tbody')[0];
    const newRow = tradeHistoryTable.insertRow();
    newRow.insertCell(0).innerText = result.side; // 'buy' or 'sell'
    newRow.insertCell(1).innerText = result.size;
    newRow.insertCell(2).innerText = result.price;
    newRow.insertCell(3).innerText = new Date(result.timestamp).toLocaleString();
    newRow.insertCell(4).innerText = result.position;
    newRow.insertCell(5).innerText = result.balance; // or realized PnL
    newRow.insertCell(6).innerText = result.unrealizedPnL;
}

function hideTradePopup() {
    document.getElementById('tradeContainer').style.display = 'none';
}
