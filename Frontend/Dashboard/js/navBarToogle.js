// Navigation Bar Toggle Button
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
