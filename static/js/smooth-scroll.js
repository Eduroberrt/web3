// Smooth scroll functionality
document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#!' && href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // Smooth scroll effect using requestAnimationFrame
    let currentScroll = window.pageYOffset;
    let targetScroll = window.pageYOffset;
    
    function smoothScroll() {
        currentScroll += (targetScroll - currentScroll) * 0.1;
        
        if (Math.abs(targetScroll - currentScroll) < 0.5) {
            currentScroll = targetScroll;
        }
        
        requestAnimationFrame(smoothScroll);
    }
    
    window.addEventListener('scroll', () => {
        targetScroll = window.pageYOffset;
    });
    
    smoothScroll();
});
