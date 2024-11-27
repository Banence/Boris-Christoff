const buttons = document.querySelectorAll("[data-carousel-button]")

buttons.forEach(button => {
  button.addEventListener("click", () => {
    const offset = button.dataset.carouselButton === "next" ? 1 : -1
    const slides = button
      .closest("[data-carousel]")
      .querySelector("[data-slides]")

    const activeSlide = slides.querySelector("[data-active]")
    let newIndex = [...slides.children].indexOf(activeSlide) + offset
    if (newIndex < 0) newIndex = slides.children.length - 1
    if (newIndex >= slides.children.length) newIndex = 0

    slides.children[newIndex].dataset.active = true
    delete activeSlide.dataset.active
  })
});

document.addEventListener('DOMContentLoaded', function() {
    // Intersection Observer for fade-in animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                // Unobserve after animation
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '50px'
    });

    // Observe all fade-in elements
    document.querySelectorAll('.fade-in, .featured-news-card, .hero-content > *').forEach((el) => {
        observer.observe(el);
    });

    // Add stagger delay to hero content children
    document.querySelectorAll('.hero-content > *').forEach((el, index) => {
        el.style.transitionDelay = `${index * 200}ms`;
    });

    function updateHeroHeight() {
        const navbar = document.querySelector('.navbar');
        if (navbar) {
            const navbarHeight = navbar.offsetHeight;
            document.documentElement.style.setProperty('--navbar-height', `${navbarHeight}px`);
        }
    }

    // Initial calculation
    updateHeroHeight();

    // Update on window resize
    window.addEventListener('resize', updateHeroHeight);

    // Update when navbar changes (e.g., mobile menu toggle)
    const navbarObserver = new ResizeObserver(updateHeroHeight);
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        navbarObserver.observe(navbar);
    }
});