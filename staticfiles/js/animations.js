// Intersection Observer for animations
document.addEventListener('DOMContentLoaded', function() {
    const animatedElements = document.querySelectorAll('[data-animate]');
    
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const element = entry.target;
                const animationType = element.getAttribute('data-animate');
                const delay = element.getAttribute('data-delay') || 0;
                
                setTimeout(() => {
                    element.classList.add('animate-in');
                    
                    // Apply specific animation classes
                    switch(animationType) {
                        case 'fade-up':
                            element.style.opacity = '0';
                            element.style.transform = 'translateY(50px)';
                            requestAnimationFrame(() => {
                                element.style.transition = 'all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)';
                                element.style.opacity = '1';
                                element.style.transform = 'translateY(0)';
                            });
                            break;
                        case 'fade-down':
                            element.style.opacity = '0';
                            element.style.transform = 'translateY(-50px)';
                            requestAnimationFrame(() => {
                                element.style.transition = 'all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)';
                                element.style.opacity = '1';
                                element.style.transform = 'translateY(0)';
                            });
                            break;
                        case 'fade-in':
                            element.style.opacity = '0';
                            requestAnimationFrame(() => {
                                element.style.transition = 'opacity 0.5s ease-in-out';
                                element.style.opacity = '1';
                            });
                            break;
                        default:
                            element.style.opacity = '0';
                            element.style.transform = 'translateY(30px)';
                            requestAnimationFrame(() => {
                                element.style.transition = 'all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)';
                                element.style.opacity = '1';
                                element.style.transform = 'translateY(0)';
                            });
                    }
                }, delay);
                
                observer.unobserve(element);
            }
        });
    }, observerOptions);
    
    animatedElements.forEach(element => {
        observer.observe(element);
    });
});
