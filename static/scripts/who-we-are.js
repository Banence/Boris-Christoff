document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('modal');
    const modalText = document.getElementById('modal-text');
    const closeBtn = document.querySelector('.close');
    const readMoreLinks = document.querySelectorAll('.read-more');

    readMoreLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            let content = this.getAttribute('data-modal-content');
            content = content.replace(/\n/g, '<br>'); // Replace newline placeholders with <br> tags
            modalText.innerHTML = content;
            modal.style.display = 'block';
        });
    });

    closeBtn.addEventListener('click', () => {
        modal.style.animation = 'fadeOut 0.5s forwards'; // Apply fade-out animation
        setTimeout(() => {
            modal.style.display = 'none';
            modal.style.animation = ''; // Reset animation
        }, 500); // Match this to the duration of the fade-out animation
    });

    window.addEventListener('click', (event) => {
        if (event.target == modal) {
            modal.style.animation = 'fadeOut 0.5s forwards'; // Apply fade-out animation
            setTimeout(() => {
                modal.style.display = 'none';
                modal.style.animation = ''; // Reset animation
            }, 500); // Match this to the duration of the fade-out animation
        }
    });
});

