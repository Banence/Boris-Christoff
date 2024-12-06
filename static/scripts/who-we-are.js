const teamData = {
    'boiko': {
        name: 'Boiko Tsvetanov',
        position: 'Founder',
        image: '/static/images/boykopfp.png',
        bio: 'Boyko Tsvetanov is one of the greatest and most successful Bulgarian tenors of all time. He is the first, most famous and beloved student of Boris Christoff. Maestro Christoff, who had no children, wanted to make him his successor. Tearful, Boyko Tsvetanov refused, saying that his successor was the entire Bulgarian people...'
    },
    'stoyan': {
        name: 'Stoyan Bonchev',
        position: 'Chairman',
        image: '/static/images/stoyanpfp.jpeg',
        bio: 'Stoyan Bonchev was born in Sofia. He received his basic education at the 133rd school - the Russian Language High School "A.S. Pushkin" After that, he continued his education at the First English Language High School "William Shakespeare" - Sofia, graduating with honors in 1995...'
    },
    'alex': {
        name: 'Alex Zografov',
        position: 'Artistic Director',
        image: '/static/images/alexpfp.jpg',
        bio: 'Maestro Alex Zografov is one of the great pianists, composers and arrangers of our time. Maestro Zografov holds a PhD in composition from the University of Los Angeles and has worked for decades at the highest level with mega stars such as George Benson, Janet Jackson, Andrew Lloyd Webber, Joe Cocker...'
    },
    // Artists
    'boiko-artist': {
        name: 'Boiko Tsvetanov',
        position: 'Tenor',
        image: '/static/images/boykopfp.png',
        bio: 'Boyko Tsvetanov is one of the greatest and most successful Bulgarian tenors of all time. He is the first, most famous and beloved student of BORIS HRISTOV.'
    },
    'stoyan-artist': {
        name: 'Stoyan Bonchev',
        position: 'Opera Bass',
        image: '/static/images/stoyanpfp.jpeg',
        bio: 'Stoyan Bonchev is an opera bass and chairman of the Boris Hristov Foundation. His repertoire is extremely rich and includes both operatic arias and classical works, as well as melodic evergreens, folk songs and author\'s music...'
    },
    'alex-artist': {
        name: 'Alex Zografov',
        position: 'Pianist & Composer',
        image: '/static/images/alexpfp.jpg',
        bio: 'Maestro Alex Zografov is one of the great pianists, composers and arrangers of our time. Maestro Zografov holds a PhD in composition from the University of Los Angeles and has worked for decades at the highest level with mega stars...'
    },
    'krum': {
        name: 'Krum Galabov',
        position: 'Baritone',
        image: '/static/images/krumpfp.jpeg',
        bio: 'Krum Galabov is a baritone with over 20 years of successful career on international opera stages. He graduated in music in Vienna and has in his repertoire over 30 central opera parts, as well as hundreds of songs, romances and canzonets...'
    },
    'boris': {
        name: 'Boris Lukov',
        position: 'Tenor',
        image: '/static/images/Borispfp.jpeg',
        bio: 'Boris Lukov is a Bulgarian tenor - a long-time soloist of the Ruse State Opera, as well as a guest soloist at almost all opera houses in Bulgaria. His repertoire is extremely rich and includes both operatic arias and parts, as well as world-famous evangelical, Russian songs and Italian canzonets.'
    },
    'albena': {
        name: 'Albena Veskova',
        position: 'Folk Singer',
        image: '/static/images/albenapfp.jpeg',
        bio: 'Albena Veskova is among the greatest Bulgarian folk singers of the last 20 years. Graduate of "Shiroka Laka", soloist of the Mysteries of Bulgarian Voices, soloist of the ensemble Bulgare, long-time TV presenter, soloist of "Painer" - one of the most beautiful and recognizable voices in our folk music.'
    },
    'anastasia-teodora': {
        name: 'Anastasia and Teodora',
        position: 'Vocal Duo',
        image: '/static/images/a&tpfp.jpeg',
        bio: 'Anastasia Balabanova and Teodora Zaneva are a young duo who are yet to develop their full potential. Former graduates of radio choirs, they are extremely musical and have wonderful vocal abilities. They have a wide repertoire of pop, rock, pop and stylized folk songs.'
    }
};

function openModal(memberId) {
    const modal = document.getElementById('bioModal');
    const data = teamData[memberId];
    
    document.getElementById('modalTitle').textContent = data.name;
    document.getElementById('modalPosition').textContent = data.position;
    document.getElementById('modalImage').src = data.image;
    document.getElementById('modalBio').innerHTML = data.bio.replace(/\n/g, '<br>');
    
    modal.classList.add('modal-open');
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    const modal = document.getElementById('bioModal');
    modal.classList.add('modal-closing');
    
    setTimeout(() => {
        modal.classList.remove('modal-open', 'modal-closing');
        document.body.style.overflow = '';
    }, 300);
}

// Close modal on backdrop click
document.querySelector('.modal-backdrop').addEventListener('click', closeModal);

// Prevent modal close when clicking modal content
document.querySelector('.modal-container').addEventListener('click', (e) => {
    e.stopPropagation();
});

// Add scroll animations
document.addEventListener('DOMContentLoaded', () => {
    // Scroll animation observer for all elements
    const scrollAnimationObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
                // Only animate once
                scrollAnimationObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.15,
        rootMargin: '50px'
    });

    // Select all elements to animate
    const animatedElements = document.querySelectorAll(
        '.mission-card, .vision-card, .story-main-card, .story-card, ' +
        '.team-card, .artist-card, .musical-line-container, ' +
        '.section-title-wrapper, .hero-content > *, .scroll-indicator, ' +
        '.mission-vision-grid, .story-grid, .team-grid, .artists-grid'
    );

    // Add animation classes and observe each element
    animatedElements.forEach((element, index) => {
        // Add staggered delay for grid items
        if (element.classList.contains('team-card') || element.classList.contains('artist-card')) {
            element.style.transitionDelay = `${index * 0.1}s`;
        }
        scrollAnimationObserver.observe(element);
    });

    const cards = document.querySelectorAll('.team-card, .artist-card');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });

    cards.forEach(card => observer.observe(card));

    const sectionTitles = document.querySelectorAll('.section-title-wrapper');
    
    const titleObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.querySelector('.section-title').classList.add('fade-in');
                titleObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.5,
        rootMargin: '0px'
    });

    sectionTitles.forEach(title => titleObserver.observe(title));

    // Update the storyObserver to handle both sections
    const storyObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                storyObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.2,
        rootMargin: '50px'
    });

    // Observe all story and mission-vision elements
    document.querySelectorAll('.story-fade-up').forEach(element => {
        storyObserver.observe(element);
    });
});

