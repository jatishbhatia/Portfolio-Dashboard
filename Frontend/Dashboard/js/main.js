document.addEventListener("DOMContentLoaded", function() {
        const ctx = document.getElementById('chart').getContext('2d');

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov'],
                datasets: [
                    {
                        label: 'BTC',
                        data: [29374, 33537, 49631, 59095, 57828, 36684, 33572, 39974, 48847, 48116, 61004],
                        borderColor: 'red',
                        borderWidth: 2,
                        fill: false
                    },
                    {
                        label: 'ETH',
                        data: [2174, 2737, 3631, 4095, 4828, 6684, 7572, 6974, 8847, 8116, 9004],
                        borderColor: 'blue',
                        borderWidth: 2,
                        fill: false
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Month'
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
        });
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