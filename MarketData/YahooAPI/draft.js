/** // GET (getAll) API
        function callGetRecord() {
            const stock = document.getElementById('stock').value;
            const startDate = document.getElementById('start_date').value;
            const endDate = document.getElementById('end_date').value;
            const interval = document.getElementById('interval').value;

            fetch(`/api/get_market_data/${stock}/${startDate}/${endDate}/${interval}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (!response.ok) {
                    return response.text().then(text => { throw new Error(text) });
                }
                return response.json();
            })
            .then(data => {
                console.log(data.result);
                alert('Python code executed successfully!');
                displayData(data.result, stock, startDate, endDate, interval);
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
        **/



/** 
<body>
    <div>
        <label for="stock">Stock Symbol:</label>
        <input type="text" id="stock" name="stock" required>
    </div>
    <div>
        <label for="start_date">Start Date:</label>
        <input type="date" id="start_date" name="start_date" required>
    </div>
    <div>
        <label for="end_date">End Date:</label>
        <input type="date" id="end_date" name="end_date" required>
    </div>
    <div>
        <label for="interval">Interval:</label>
        <input type="text" id="interval" name="interval" required>
    </div>

    <button onclick="callPostRecord()"> TESTING THE POST BUTTON API </button>
    <div id="result"></div>

    <script>

        //// POST API
        function callPostRecord() {
            const stock = document.getElementById('stock').value;
            const startDate = document.getElementById('start_date').value;
            const endDate = document.getElementById('end_date').value;
            const interval = document.getElementById('interval').value;

            if (!stock || !startDate || !endDate || !interval) {
                alert('Please fill in all fields.');
                return;
            }

            fetch('/run_python_code', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    //name: 'AAPL',
                    //start: '2022-01-01',
                    //end: '2022-12-31',
                    //interval: '1d'
                    name: stock,
                    start: startDate,
                    end: endDate,
                    interval: interval
                })
            })
            .then(response => {
                if (!response.ok) {
                    return response.text().then(text => { throw new Error(text) });
                }
                return response.json();
            })
            .then(data => {
                console.log(data.result);
                alert('Python code executed successfully!');
                populateFields(stock, startDate, endDate, interval);
                displayData(data.result, stock, startDate, endDate, interval);
                // displayData(data.result, 'AAPL', '2022-01-01', '2022-12-31', '1d');
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }

        function populateFields(stock, startDate, endDate, interval) {
            document.getElementById('stock').value = stock;
            document.getElementById('start_date').value = startDate;
            document.getElementById('end_date').value = endDate;
            document.getElementById('interval').value = interval;
        }

        function displayData(data, stock, start_date, end_date, interval) {
            const resultDiv = document.getElementById('result');
            const table = document.createElement('table');
            const headerRow = document.createElement('tr');

            // Create header row
            const headers = ['Stock', 'Start Date', 'End Date', 'Interval'];
            headers.forEach(headerText => {
                const header = document.createElement('th');
                header.textContent = headerText;
                headerRow.appendChild(header);
            });
            table.appendChild(headerRow);

            // Create data row
            const dataRow = document.createElement('tr');

            // Symbol cell
            const symbolCell = document.createElement('td');
            symbolCell.textContent = stock;
            dataRow.appendChild(symbolCell);

            // Start Date cell
            const startDateCell = document.createElement('td');
            startDateCell.textContent = start_date;
            dataRow.appendChild(startDateCell);

            // End Date cell
            const endDateCell = document.createElement('td');
            endDateCell.textContent = end_date;
            dataRow.appendChild(endDateCell);

            // Interval cell
            const intervalCell = document.createElement('td');
            intervalCell.textContent = interval;
            dataRow.appendChild(intervalCell);

            table.appendChild(dataRow);

            // Clear previous results
            resultDiv.innerHTML = '';
            resultDiv.appendChild(table);
        }
    </script>
</body>

</html>
