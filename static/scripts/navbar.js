const burgerIconElement = document.getElementById("burger-icon");
const navbarMobileElement = document.querySelector(".nav-mobile-container");
const burgerSvgElement = document.getElementById("burger-svg");
const crossSvgElement = document.getElementById("cross-svg");

burgerIconElement.addEventListener('click', function () {
    navbarMobileElement.classList.toggle("visible");
    burgerSvgElement.classList.toggle("open");
    crossSvgElement.classList.toggle("open");
});


