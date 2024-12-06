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
        const isActive = force !== null ? force : !mobileNav.classList.contains('active');
        
        // Add/remove classes
        mobileNav.classList.toggle('active', isActive);
        mobileNavOverlay.classList.toggle('active', isActive);
        mobileMenuBtn.classList.toggle('active', isActive);
        document.body.classList.toggle('mobile-nav-active', isActive);
        
        // Update ARIA attributes
        mobileMenuBtn.setAttribute('aria-expanded', isActive);
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
        if (mobileNav.classList.contains('active') && 
            !mobileNav.contains(e.target) && 
            !mobileMenuBtn.contains(e.target)) {
            toggleMobileMenu(false);
        }
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            toggleMobileMenu(false);
            
            // Close all dropdowns
            document.querySelectorAll('.nav-dropdown').forEach(dropdown => {
                dropdown.classList.remove('active');
            });
        }
    });

    // Mobile dropdown functionality
    const mobileDropdowns = document.querySelectorAll('.mobile-dropdown');
    
    mobileDropdowns.forEach(dropdown => {
        const trigger = dropdown.querySelector('.mobile-dropdown-trigger');
        
        trigger.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Close other dropdowns
            mobileDropdowns.forEach(other => {
                if (other !== dropdown) {
                    other.classList.remove('active');
                }
            });
            
            // Toggle current dropdown
            dropdown.classList.toggle('active');
        });
    });

    // Close mobile dropdowns when clicking outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.mobile-dropdown')) {
            mobileDropdowns.forEach(dropdown => {
                dropdown.classList.remove('active');
            });
        }
    });

    // Close mobile dropdowns when mobile menu is closed
    const closeMobileDropdowns = () => {
        mobileDropdowns.forEach(dropdown => {
            dropdown.classList.remove('active');
        });
    };

    // Add dropdown closing to existing mobile menu toggle
    const originalToggleMobileMenu = toggleMobileMenu;
    toggleMobileMenu = (force = null) => {
        originalToggleMobileMenu(force);
        if (force === false) {
            closeMobileDropdowns();
        }
    };

    // Prevent body scroll when mobile menu is open
    document.body.addEventListener('touchmove', (e) => {
        if (document.body.classList.contains('mobile-nav-active')) {
            if (!mobileNav.contains(e.target)) {
                e.preventDefault();
            }
        }
    }, { passive: false });
});
