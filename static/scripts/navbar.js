document.addEventListener('DOMContentLoaded', function () {
    const navbar = document.querySelector('.navbar');
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const mobileNav = document.querySelector('.mobile-nav');
    const mobileNavOverlay = document.querySelector('.mobile-nav-overlay');

    if (!navbar || !mobileMenuBtn || !mobileNav || !mobileNavOverlay) {
        console.error('Required navbar elements are missing.');
        return;
    }

    const toggleMobileMenu = (force = null) => {
        const isActive = force !== null ? force : mobileNav.classList.toggle('active');
        mobileNav.classList.toggle('active', isActive);
        mobileNavOverlay.classList.toggle('active', isActive);
        mobileMenuBtn.classList.toggle('active', isActive);
        mobileMenuBtn.setAttribute('aria-expanded', isActive);
        document.body.style.overflow = isActive ? 'hidden' : '';
    };

    // Handle window resize
    const handleResize = () => {
        if (window.innerWidth > 1290 && mobileNav.classList.contains('active')) {
            toggleMobileMenu(false);
        }
    };

    window.addEventListener('resize', handleResize);

    // Update transparent navbar handling
    if (document.body.classList.contains('is-index') || document.body.classList.contains('who-we-are')) {
        const handleScroll = () => {
            navbar.classList.toggle('scrolled', window.scrollY > 50);
        };
        window.addEventListener('scroll', handleScroll);
        handleScroll();
    }

    // Event Listeners
    mobileMenuBtn.addEventListener('click', () => toggleMobileMenu());
    mobileNavOverlay.addEventListener('click', () => toggleMobileMenu(false));

    document.addEventListener('click', (e) => {
        if (!mobileNav.contains(e.target) && !mobileMenuBtn.contains(e.target) && mobileNav.classList.contains('active')) {
            toggleMobileMenu(false);
        }
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && mobileNav.classList.contains('active')) {
            toggleMobileMenu(false);
        }
    });
});
