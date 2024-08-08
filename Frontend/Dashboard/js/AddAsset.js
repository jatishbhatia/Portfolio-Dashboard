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
                        <label for="stockSymbol">Stock Symbol:</label>
                        <input type="text" id="stockSymbol" name="stockSymbol" required>
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
                        <label for="price">Price per Share:</label>
//                        todo change the value of 100 to value="${data.price}"
                        <input type="number" id="price" name="price" step="0.01" required min="0.01" value="100" readonly>
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
            const stockSymbol = form.querySelector('#stockSymbol').value;
            const assetName = form.querySelector('#assetName').value;
            const categoryName = form.querySelector('#categoryName').value;
            const quantity = parseInt(form.querySelector('#quantity').value, 10);
            const price = parseFloat(form.querySelector('#price').value);

            if (!stockSymbol || !assetName || !categoryName || isNaN(quantity) || quantity <= 0 || isNaN(price) || price <= 0) {
                Swal.showValidationMessage('Please provide valid inputs.');
                return false;
            }

            return { stockSymbol, assetName, categoryName, quantity, price };
        }
    }).then((result) => {
        if (result.isConfirmed) {
            const { stockSymbol, assetName, categoryName, quantity, price } = result.value;
            submitForm(stockSymbol, assetName, categoryName, quantity, price);
        }
    });
}

function submitForm(stockSymbol, assetName, categoryName, quantity, price) {
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
