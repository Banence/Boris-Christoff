const burgerIconElement = document.getElementById("burger-icon");
const navbarMobileElement = document.querySelector(".nav-mobile-container");
const burgerSvgElement = document.getElementById("burger-svg");

burgerIconElement.addEventListener('click', function () {
    navbarMobileElement.classList.toggle("visible");
    burgerSvgElement.classList.toggle("open");
});


