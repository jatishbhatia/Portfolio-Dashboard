document.addEventListener('DOMContentLoaded', function () {
    const tradeButtons = document.querySelectorAll('.AddAssetButton');
    tradeButtons.forEach(button => {
        button.addEventListener('click', function () {
            AddAsset();
        });
    });
});

function AddAsset() {
    Swal.fire({
        title: 'Add Asset',
        html: `
            <div class="form-container">
                <form id="tradeForm">
                    <div class="form-group">
                        <label for="stockSymbolAddAsset">Stock Symbol:</label>
                        <input type="text" id="stockSymbolAddAsset" name="stockSymbol" required>
                    </div>
                    <div class="form-group">
                        <label for="assetName">Asset Name:</label>
                        <input type="text" id="assetName" name="assetName" required>
                    </div>
                    <div class="form-group">
                        <label for="categoryName">Category Name:</label>
                        <input type="text" id="categoryName" name="categoryName" required>
                    </div>
                    <div class="form-group">
                        <label for="quantity">Quantity:</label>
                        <input type="number" id="quantity" name="quantity" required min="1">
                    </div>
                    <div class="form-group">
                        <label for="priceInForm">Price per Share:</label>
                        <input type="number" id="priceInForm" name="priceInForm" step="0.01" required min="0.01" readonly>
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
            const stockSymbol = form.querySelector('#stockSymbolAddAsset').value;
            const assetName = form.querySelector('#assetName').value;
            const categoryName = form.querySelector('#categoryName').value;
            const quantity = parseInt(form.querySelector('#quantity').value, 10);
            const price = parseFloat(form.querySelector('#priceInForm').value);

            if (!stockSymbol || !assetName || !categoryName || isNaN(quantity) || quantity <= 0 || isNaN(price) || price <= 0) {
                Swal.showValidationMessage('Please provide valid inputs.');
                return false;
            }

            return { stockSymbol, assetName, categoryName, quantity, price };
        }
    }).then((result) => {
        if (result.isConfirmed) {
            const { stockSymbol, assetName, categoryName, quantity, price } = result.value;
            submitFormAsset(stockSymbol, assetName, categoryName, quantity, price);
        }
    });

    document.getElementById('stockSymbolAddAsset').addEventListener('blur', function() {
        const stockName = this.value;
        if (stockName) {
            fetchDataAndAddPrice(stockName);
        }
    });


    function fetchDataAndAddPrice(stockName) {
            fetch(`/api/get_current_price/${encodeURIComponent(stockName)}`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('priceInForm').value = data.price.toFixed(2);
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                });
    }
}



function submitFormAsset(stockSymbol, assetName, categoryName, quantity, price) {
    try {
        
        if (quantity <= 0 || price <= 0) {
            throw new Error('Invalid price or quantity provided');
        }

        const totalPurchasePrice = quantity * price;

        fetch('/create_asset', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                symbol: stockSymbol,
                name: assetName,
                category_name: categoryName,
                total_purchase_price: totalPurchasePrice,
                quantity: quantity
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            } else {
                Swal.fire({
                    icon: 'success',
                    title: 'Success',
                    text: data.message.message,
                });
            }
        })
        .catch(error => {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: error.message,
            });
        });
    } catch (error) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: error.message,
        });
    }
}
