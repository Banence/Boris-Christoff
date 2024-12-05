document.addEventListener('DOMContentLoaded', () => {
    const slides = document.querySelectorAll('.project-slide');
    const indicators = document.querySelectorAll('.indicator');
    const prevButton = document.querySelector('.prev-button');
    const nextButton = document.querySelector('.next-button');
    let currentIndex = 0;
    let interval;
    let isAnimating = false;

    function showSlide(index, direction = 1) {
        if (isAnimating) return;
        isAnimating = true;

        const currentSlide = slides[currentIndex];
        const nextSlide = slides[index];
        
        // Reset transforms
        slides.forEach(slide => {
            slide.style.transition = 'none';
            slide.style.transform = 'translateX(0) rotateY(0)';
            slide.style.opacity = '0';
            slide.classList.remove('active');
        });

        // Set initial positions
        currentSlide.style.transform = 'translateX(0) rotateY(0)';
        currentSlide.style.opacity = '1';
        nextSlide.style.transform = `translateX(${direction * 100}%) rotateY(${direction * 10}deg)`;
        
        // Force reflow
        void currentSlide.offsetWidth;
        
        // Add transitions back
        currentSlide.style.transition = 'all 0.8s cubic-bezier(0.4, 0, 0.2, 1)';
        nextSlide.style.transition = 'all 0.8s cubic-bezier(0.4, 0, 0.2, 1)';
        
        // Animate slides
        currentSlide.style.transform = `translateX(${direction * -100}%) rotateY(${direction * -10}deg)`;
        currentSlide.style.opacity = '0';
        nextSlide.style.transform = 'translateX(0) rotateY(0)';
        nextSlide.style.opacity = '1';
        nextSlide.classList.add('active');

        // Update indicators
        indicators.forEach(indicator => indicator.classList.remove('active'));
        indicators[index].classList.add('active');

        currentIndex = index;

        // Reset animation flag
        setTimeout(() => {
            isAnimating = false;
        }, 800);
    }

    function nextSlide() {
        const nextIndex = (currentIndex + 1) % slides.length;
        showSlide(nextIndex);
    }

    function prevSlide() {
        const prevIndex = (currentIndex - 1 + slides.length) % slides.length;
        showSlide(prevIndex);
    }

    function startAutoplay() {
        interval = setInterval(nextSlide, 7000);
    }

    function stopAutoplay() {
        clearInterval(interval);
    }

    // Event Listeners
    prevButton.addEventListener('click', () => {
        prevSlide();
        stopAutoplay();
        startAutoplay();
    });

    nextButton.addEventListener('click', () => {
        nextSlide();
        stopAutoplay();
        startAutoplay();
    });

    indicators.forEach((indicator, index) => {
        indicator.addEventListener('click', () => {
            showSlide(index);
            stopAutoplay();
            startAutoplay();
        });
    });

    // Start autoplay
    startAutoplay();

    // Pause autoplay on hover
    const projectContainer = document.querySelector('.project-container');
    projectContainer.addEventListener('mouseenter', stopAutoplay);
    projectContainer.addEventListener('mouseleave', startAutoplay);
}); 