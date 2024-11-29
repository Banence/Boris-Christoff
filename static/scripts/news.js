document.addEventListener('DOMContentLoaded', function() {
    // Add navbar scroll behavior
    const navbar = document.querySelector('.navbar');
    const heroSection = document.querySelector('.hero-section');
    
    function updateNavbar() {
        const scrollPosition = window.scrollY;
        const heroHeight = heroSection.offsetHeight;
        
        if (scrollPosition > heroHeight - 100) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }

    // Initial check
    updateNavbar();
    
    // Add scroll event listener
    window.addEventListener('scroll', updateNavbar);

    // Your existing modal code...
    const modal = document.querySelector('.modal-overlay');
    const closeBtn = document.querySelector('.close-modal');
    const readMoreBtns = document.querySelectorAll('.read-more-btn');

    // Rest of your existing news.js code...
}); 