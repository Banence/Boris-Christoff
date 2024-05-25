document.addEventListener("DOMContentLoaded", () => {
    const elements = document.querySelectorAll('.fade-in, .slide-in-left, .slide-in-right, .fade');
  
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    });
  
    elements.forEach(element => {
      observer.observe(element);
    });
});
  