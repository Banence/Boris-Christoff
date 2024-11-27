document.addEventListener('DOMContentLoaded', function() {
    const modalOverlay = document.querySelector('.modal-overlay');
    const closeModalBtn = document.querySelector('.close-modal');
    const seeMoreBtns = document.querySelectorAll('.see-more-btn');

    console.log('Found see more buttons:', seeMoreBtns.length);

    // Open modal
    seeMoreBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            console.log('Button clicked');
            const eventCard = this.closest('.event-card');
            const eventTitle = eventCard.querySelector('.event-title').textContent;
            const eventDescription = eventCard.querySelector('.event-full-description').textContent;
            const eventImage = eventCard.querySelector('.event-image-container img').src;
            const eventDate = eventCard.querySelector('.event-date').textContent;

            // Update modal content before opening
            document.getElementById('modal-event-name').textContent = eventTitle;
            document.getElementById('modal-event-description').textContent = eventDescription;
            document.getElementById('modal-event-image').src = eventImage;
            document.getElementById('modal-event-date').textContent = eventDate;

            // Ensure content is visible before animation
            const modalElements = document.querySelectorAll('.modal-content > *');
            modalElements.forEach(el => {
                el.style.opacity = '1';
                el.style.transform = 'none';
            });

            // Then open the modal
            openModal();
        });
    });

    // Close modal
    closeModalBtn.addEventListener('click', closeModal);
    modalOverlay.addEventListener('click', function(e) {
        if (e.target === modalOverlay) {
            closeModal();
        }
    });

    // Close modal with escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modalOverlay.classList.contains('active')) {
            closeModal();
        }
    });

    function openModal() {
        modalOverlay.classList.remove('closing');
        modalOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
        
        // Reset any previous styles
        const modalElements = [
            '.modal-image',
            '.modal-info h2',
            '.modal-meta',
            '.modal-description'
        ];
        
        modalElements.forEach(selector => {
            const element = document.querySelector(selector);
            if (element) {
                // Reset the element's styles first
                element.style.opacity = '0';
                element.style.transform = 'translateY(30px)';
                
                // Force a reflow
                element.offsetHeight;
                
                // Add the animation
                setTimeout(() => {
                    element.style.transition = 'all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)';
                    element.style.opacity = '1';
                    element.style.transform = 'translateY(0)';
                }, 100);
            }
        });

        // Enhanced image animation
        const modalImage = document.querySelector('.modal-image img');
        if (modalImage) {
            modalImage.style.transform = 'scale(1.1)';
            modalImage.style.transition = 'transform 1.2s cubic-bezier(0.34, 1.56, 0.64, 1)';
            setTimeout(() => {
                modalImage.style.transform = 'scale(1)';
            }, 100);
        }
    }

    function closeModal() {
        modalOverlay.classList.add('closing');
        document.body.style.overflow = '';
        
        // Don't reset the content immediately
        setTimeout(() => {
            modalOverlay.classList.remove('active', 'closing');
            
            // Only reset the animations after the modal is fully closed
            const modalElements = document.querySelectorAll('.modal-content > *');
            modalElements.forEach(el => {
                el.style.transition = 'none'; // Disable transitions temporarily
                el.style.opacity = '1'; // Keep content visible for next opening
                el.style.transform = 'none';
            });
        }, 400);
    }

    // Smooth reveal of title underline
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    });

    document.querySelectorAll('.title-underline').forEach(underline => {
        observer.observe(underline);
    });

    // Get hero section reference once
    const heroSection = document.querySelector('.hero-section');
    let ticking = false;

    // Add navbar scroll effect
    const navbar = document.querySelector('.navbar');
    
    function updateNavbar() {
        if (window.scrollY > heroSection.offsetHeight - navbar.offsetHeight) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }

    // Initial check
    updateNavbar();

    // Combined scroll event listener for all scroll-based effects
    window.addEventListener('scroll', () => {
        // Update navbar
        updateNavbar();
        
        // Parallax background effect
        if (!ticking) {
            window.requestAnimationFrame(function() {
                const scrolled = window.pageYOffset;
                // Apply both transform and background position effects
                heroSection.style.transform = `translateY(${scrolled * 0.5}px)`;
                heroSection.style.opacity = 1 - Math.max(0, scrolled / (window.innerHeight * 0.5));
                heroSection.style.backgroundPositionY = `${scrolled * 0.5}px`;
                ticking = false;
            });
            ticking = true;
        }
    });

    // Smooth scroll for navigation
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Smooth scroll for hero scroll indicator
    const scrollIndicator = document.querySelector('.hero-scroll-indicator');
    if (scrollIndicator) {
        scrollIndicator.addEventListener('click', () => {
            const eventsContainer = document.querySelector('.events-container');
            eventsContainer.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        });
    }
}); 