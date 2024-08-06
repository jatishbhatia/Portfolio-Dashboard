document.addEventListener('DOMContentLoaded', function () {
    const tradeButtons = document.querySelectorAll('.tradeButton');
    tradeButtons.forEach(button => {
        button.addEventListener('click', function () {
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
                                <input type="text" id="stockSymbol" name="stockSymbol" required>
                            </div>
                            <div class="form-group">
                                <label for="quantity">Quantity:</label>
                                <input type="number" id="quantity" name="quantity" required>
                            </div>
                            <div class="form-group">
                                <label for="price">Price per Share:</label>
                                <input type="number" id="price" name="price" step="0.1" required>
                            </div>
                        </form>
                    </div>
                `,
                showCloseButton: true,
                showCancelButton: true,
                confirmButtonText: 'Submit',
                focusConfirm: false,
                preConfirm: () => {
                    const form = document.getElementById('tradeForm');
                    if (!form.checkValidity()) {
                        Swal.showValidationMessage('Please Check the Information enter in fields');
                        return false;
                    }
                    // Manually trigger form submission
                    form.requestSubmit();
                }
            });
        });
    });
});

function submitForm(event) {
    event.preventDefault();
    const form = event.target;
    if (form.checkValidity()) {
        // Perform the actual submission logic here (e.g., send data to the server)
        console.log("Form submitted");
    } else {
        Swal.showValidationMessage('Please fill out all fields');
    }
}
