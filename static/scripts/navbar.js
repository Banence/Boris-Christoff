const burgerIconElement = document.getElementById("burger-icon");
const navbarMobileElement = document.querySelector(".nav-mobile-container");
const burgerSvgElement = document.getElementById("burger-svg");
const crossSvgElement = document.getElementById("cross-svg");

burgerIconElement.addEventListener('click', function () {
    navbarMobileElement.classList.toggle("visible");
    burgerSvgElement.classList.toggle("open");
    crossSvgElement.classList.toggle("open");
});

document.addEventListener("DOMContentLoaded", function() {
    const dropdownSVGs = document.querySelectorAll('.dropdown-svg');
    const dropdownItems = document.querySelectorAll('.dropdown-item-m a');

    dropdownSVGs.forEach((svg, index) => {
        svg.addEventListener('click', function(event) {
            event.stopPropagation();
            event.preventDefault(); 
            const dropdown = document.querySelectorAll('.dropdown-m')[index];
            dropdown.classList.toggle('show');
            svg.classList.toggle('rotated');
        });
    });

    dropdownItems.forEach(item => {
        item.addEventListener('click', function(event) {
            event.stopPropagation();
            event.preventDefault();
            const navbar = document.querySelector('.nav-mobile-container');
            navbar.classList.remove('visible');
            window.location.href = this.href; 
        });
    });

    document.addEventListener('click', function() {
        const dropdowns = document.querySelectorAll('.dropdown-m');
        dropdowns.forEach((dropdown) => {
            dropdown.classList.remove('show');
        });
        const svgs = document.querySelectorAll('.dropdown-svg');
        svgs.forEach((svg) => {
            svg.classList.remove('rotated');
        });
    });
});

let lastScrollTop = 0;
const navbar = document.querySelector('.nav-container');

window.addEventListener('scroll', () => {
    const scrollTop = window.scrollY || document.documentElement.scrollTop;

    if (scrollTop > lastScrollTop) {
        navbar.classList.add('hidden');
    } else {
        navbar.classList.remove('hidden');
    }

    lastScrollTop = Math.max(scrollTop, 0); 
});







