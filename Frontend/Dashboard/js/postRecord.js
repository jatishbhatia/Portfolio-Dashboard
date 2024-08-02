//// POST API
function callPostRecord() {
        fetch('/run_python_code', {
                method: 'POST',
                headers: {
                        'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                        name: 'AAPL',
                        start: '2022-01-01',
                        end: '2022-12-31',
                        interval: '1d'
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
                        displayData(data.result, 'AAPL', '2022-01-01', '2022-12-31', '1d');
                })
                .catch(error => {
                        console.error('Error:', error);
                });
}

function displayData(data, stock, start_date, end_date, interval) {
    const resultDiv = document.getElementById('result');
    const table = document.createElement('table');
    table.classList.add('apiDataTable'); // Add a class to the table

    const headerRow = document.createElement('tr');
    headerRow.classList.add('apiHeaderRow'); // Add a class to the header row

    // Create header row
    const headers = ['Stock', 'Start Date', 'End Date', 'Interval'];
    headers.forEach(headerText => {
        const header = document.createElement('th');
        header.classList.add('apiHeaderCell'); // Add a class to header cells
        header.textContent = headerText;
        headerRow.appendChild(header);
    });
    table.appendChild(headerRow);

    // Create data row
    const dataRow = document.createElement('tr');
    dataRow.classList.add('apiDataRow'); // Add a class to the data row

    // Symbol cell
    const symbolCell = document.createElement('td');
    symbolCell.classList.add('apiDataCell'); // Add a class to data cells
    symbolCell.textContent = stock;
    dataRow.appendChild(symbolCell);

    // Start Date cell
    const startDateCell = document.createElement('td');
    startDateCell.classList.add('apiDataCell'); // Add a class to data cells
    startDateCell.textContent = start_date;
    dataRow.appendChild(startDateCell);

    // End Date cell
    const endDateCell = document.createElement('td');
    endDateCell.classList.add('apiDataCell'); // Add a class to data cells
    endDateCell.textContent = end_date;
    dataRow.appendChild(endDateCell);

    // Interval cell
    const intervalCell = document.createElement('td');
    intervalCell.classList.add('apiDataCell'); // Add a class to data cells
    intervalCell.textContent = interval;
    dataRow.appendChild(intervalCell);

    table.appendChild(dataRow);

    // Clear previous results
    resultDiv.innerHTML = '';
    resultDiv.appendChild(table);
}
