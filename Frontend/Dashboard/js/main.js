document.addEventListener("DOMContentLoaded", function() {
        const ctx = document.getElementById('chart').getContext('2d');

        fetch('/api/get_time_series').then(result => result.json())
            .then(series=>{
                const dataToGraph = []
                for ( const [label, vals] of Object.entries(series)) {
                    dataToGraph.push({
                        label: label,
                        data: vals.Close,
                        borderColor: getRandomColor(),
                        borderWidth: 2,
                        fill: false
                    })
                }
                new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: series[Object.keys(series)[0]].Date,
                        datasets: dataToGraph
                    },
                    options: {
                        responsive: true,
                        scales: {
                            x: {
                                display: true,
                                title: {
                                    display: true,
                                    text: 'Date'
                                }
                            },
                            y: {
                                display: true,
                                title: {
                                    display: true,
                                    text: 'Value'
                                }
                            }
                        }
                    }
                })

            })
    });

function getRandomColor() {
    const colors = ['Red', 'Green', 'Blue', 'Orange', 'Purple', 'Pink'];
    return colors[Math.floor(Math.random()*5)];
}


document.addEventListener("DOMContentLoaded", function() {
        function getProfit() {
            fetch('/api/get_unrealized_profit')
                .then(profit => profit.json())
                .then(profit => {
                    const profitElement = document.getElementById('profit');
                    let arrow = '';
                    let color = '';

                    if (profit >= 0) {
                        arrow = '▲';
                        color = 'green';
                    } else {
                        arrow = '▼';
                        color = 'red';
                    }

                    profitElement.innerHTML = `<span style="color: ${color};">${arrow} ${profit} USD</span>`;
                })
                .catch(err => {
                    console.error('Error displaying profit:', err);
                });
        }
        getProfit();
    });
// sho wor hide the sidebar
const menuBtn = document.querySelector('#menu-btn')
const closeBtn = document.querySelector('#close-btn')
const sidebar = document.querySelector('aside')

menuBtn.addEventListener('click', () => {
        sidebar.style.display = 'block';
})

closeBtn.addEventListener('click', () => {
        sidebar.style.display = 'none';
})

//change theme
const themeBtn = document.querySelector('.theme-btn');

themeBtn.addEventListener('click', () => {
        document.body.classList.toggle('dark-theme');

        themeBtn.querySelector('span:first-child').classList.toggle('active');
        themeBtn.querySelector('span:last-child').classList.toggle('active');
})


document.addEventListener("DOMContentLoaded", function () {
    const links = document.querySelectorAll('.sidebar-link');
    const sections = document.querySelectorAll('.content-section');

    links.forEach(link => {
        link.addEventListener('click', function (event) {
            event.preventDefault();
            const targetId = this.getAttribute('data-target');

            sections.forEach(section => {
                section.style.display = 'none';
            });

            document.getElementById(targetId).style.display = 'block';

            links.forEach(link => {
                link.classList.remove('active');
            });

            this.classList.add('active');
        });
    });
});