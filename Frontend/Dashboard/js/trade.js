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
                                <input type="text" id="stockSymbol" name="stockSymbol" value="${stockSymbol}" required>
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
                    const transactionType = form.querySelector('#transactionType').value;
                    const stockSymbol = form.querySelector('#stockSymbol').value;
                    const quantity = form.querySelector('#quantity').value;
                    const price = form.querySelector('#price').value;

                    if (!transactionType || !stockSymbol || !quantity || !price) {
                        Swal.showValidationMessage('Please fill out all fields');
                        return false;
                    }

                    console.log('Form Data:', { transactionType, stockSymbol, quantity, price });

                    return { transactionType, stockSymbol, quantity, price };
                }
            }).then((result) => {
                if (result.isConfirmed) {
                    const { transactionType, stockSymbol, quantity, price } = result.value;
                    submitForm(transactionType, stockSymbol, quantity, price);
                }
            });
        })
        .catch(error => {
            console.error('Error fetching current price:', error);
            Swal.fire('Error', `There was a problem fetching the current price: ${error.message}`, 'error');
        });
}

function submitForm(transactionType, stockSymbol, quantity, price) {
    const data = {
        symbol: stockSymbol,
        quantity: quantity,
        price: price
    };
    console.log('Form Data:', data);

    const url = transactionType === 'buy' ? '/buy_stock' : '/sell_stock';

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
        updateTradeHistory(result, { transactionType, stockSymbol, quantity, price });
        // Updating the assets table with the new data
        updateAssetsTable(result.asset);
    })
    .catch(error => {
        console.error('Error:', error);
        Swal.fire('Error', `There was a problem with your request: ${error.message}`, 'error');
    });
}


function updateTradeHistory(result, formData) {
    const tradeHistoryTable = document.getElementById('tradeHistory').getElementsByTagName('tbody')[0];
    const newRow = tradeHistoryTable.insertRow();

    // Ensure that the properties are defined or set default values
    const side = formData.transactionType || '';
    const size = formData.quantity || '';
    const price = formData.price !== undefined ? parseFloat(formData.price).toFixed(2) : '';
    const timestamp = new Date().toLocaleString(); // Current time
//    const position = result.asset.category || ''; // Category of the asset
    const position = '';
//    const balance = result.asset.purchasePrice !== undefined ? result.asset.purchasePrice.toFixed(2) : '';
//    const unrealizedPnL = result.unrealizedPnL !== undefined ? result.unrealizedPnL.toFixed(2) : '';
    const balance = '';
    const unrealizedPnL = '';
    console.log('Updating trade history with:', { side, size, price, timestamp, position, balance, unrealizedPnL });

    newRow.insertCell(0).innerText = side; // 'buy' or 'sell'
    newRow.insertCell(1).innerText = size;
    newRow.insertCell(2).innerText = price;
    newRow.insertCell(3).innerText = timestamp;
    newRow.insertCell(4).innerText = position;
    newRow.insertCell(5).innerText = balance;
    newRow.insertCell(6).innerText = unrealizedPnL;
}


function updateAssetsTable(asset) {
    const rows = document.querySelectorAll('#assetsTable tbody tr');
    rows.forEach(row => {
        const assetNameCell = row.querySelector('td:nth-child(1)');
        if (assetNameCell.innerText === asset.name) {
            row.querySelector('td:nth-child(3)').innerText = asset.purchasePrice !== undefined ? asset.purchasePrice.toFixed(2) : ''; // Ensure purchase price is displayed with 2 decimal places
            row.querySelector('td:nth-child(4)').innerText = asset.quantity;
        }
    });
}

function hideTradePopup() {
    document.getElementById('tradeContainer').style.display = 'none';
}
