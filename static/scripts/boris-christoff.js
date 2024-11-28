document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.querySelector('.navbar');
    
    // Set initial state
    if (window.scrollY === 0) {
        navbar.classList.add('transparent');
    }
    
    window.addEventListener('scroll', function() {
        if (window.scrollY === 0) {
            navbar.classList.add('transparent');
        } else {
            navbar.classList.remove('transparent');
        }
    });

    // Enhanced smooth number animation
    function animateNumber(element, start, end, duration) {
        const startTime = performance.now();
        const plus = element.getAttribute('data-plus') === 'true';

        // Use requestAnimationFrame for smoother animation
        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Easing function for smooth animation
            const easeOutQuart = 1 - Math.pow(1 - progress, 4);
            
            const current = Math.floor(start + (end - start) * easeOutQuart);
            
            // Format the number and add plus sign if needed
            element.textContent = current + (plus ? '+' : '');

            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }

        requestAnimationFrame(update);
    }

    // Intersection Observer for number animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const numberElement = entry.target;
                const targetNumber = parseInt(numberElement.getAttribute('data-target'));
                const hasPlus = numberElement.textContent.includes('+');
                
                // Store plus sign information
                numberElement.setAttribute('data-plus', hasPlus);
                
                // Start animation
                animateNumber(numberElement, 0, targetNumber, 2000);
                observer.unobserve(numberElement);
            }
        });
    }, { 
        threshold: 0.5,
        rootMargin: '0px'
    });

    // Observe all stat numbers
    document.querySelectorAll('.stat-number').forEach(number => {
        const targetNumber = parseInt(number.textContent);
        number.setAttribute('data-target', targetNumber);
        number.textContent = '0';
        observer.observe(number);
    });

    // Legacy cards animation
    const legacyCards = document.querySelectorAll('.legacy-card');
    const legacyTitle = document.querySelector('.artistic-legacy-section h2');

    const legacyObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                if (entry.target.tagName === 'H2') {
                    entry.target.style.animation = 'fadeInUp 0.8s var(--transition-smooth) forwards';
                } else {
                    setTimeout(() => {
                        entry.target.classList.add('animate');
                    }, index * 200); // Stagger the animations
                }
                legacyObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.2
    });

    if (legacyTitle) {
        legacyObserver.observe(legacyTitle);
    }
    
    legacyCards.forEach(card => {
        legacyObserver.observe(card);
    });

    // Spiritual legacy animations
    const spiritualLegacyObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
                spiritualLegacyObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.2
    });

    // Observe spiritual legacy elements
    document.querySelectorAll('.legacy-section .legacy-content, .legacy-section .legacy-image').forEach(element => {
        spiritualLegacyObserver.observe(element);
    });
}); 