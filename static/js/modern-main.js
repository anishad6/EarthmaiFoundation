/* ============================================
   EARTHMAI FOUNDATION - MODERN INTERACTIONS
   Smooth Animations & Micro-interactions
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {
    
    // ============ Navbar Scroll Effect ============
    const navbar = document.querySelector('.navbar-modern');
    let lastScroll = 0;
    
    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;
        
        if (navbar) {
            if (currentScroll > 100) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
            
            // Hide/show navbar on scroll direction
            if (currentScroll > lastScroll && currentScroll > 200) {
                navbar.style.transform = 'translateY(-100%)';
            } else {
                navbar.style.transform = 'translateY(0)';
            }
            lastScroll = currentScroll;
        }
    });
    
    // ============ Scroll Progress Indicator ============
    const scrollProgress = document.createElement('div');
    scrollProgress.className = 'scroll-progress';
    document.body.prepend(scrollProgress);
    
    window.addEventListener('scroll', function() {
        const windowHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrolled = (window.scrollY / windowHeight) * 100;
        scrollProgress.style.width = scrolled + '%';
    });
    
    // ============ Back to Top Button ============
    const backToTop = document.querySelector('.back-to-top') || document.getElementById('backToTop');
    
    if (backToTop) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 500) {
                backToTop.classList.add('visible');
            } else {
                backToTop.classList.remove('visible');
            }
        });
        
        backToTop.addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // ============ Scroll Animations (Intersection Observer) ============
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                
                // Add stagger delay for children
                const children = entry.target.querySelectorAll('.animate-child');
                children.forEach((child, index) => {
                    child.style.transitionDelay = (index * 0.1) + 's';
                    child.classList.add('visible');
                });
            }
        });
    }, observerOptions);
    
    // Observe all elements with animation class
    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });
    
    // Auto-add animation class to common elements
    const animatableElements = [
        '.section-header',
        '.initiative-card',
        '.team-card',
        '.involved-card',
        '.gallery-item',
        '.mission-card',
        '.stat-item'
    ];
    
    animatableElements.forEach(selector => {
        document.querySelectorAll(selector).forEach((el, index) => {
            el.classList.add('animate-on-scroll');
            el.style.transitionDelay = (index * 0.1) + 's';
            observer.observe(el);
        });
    });
    
    // ============ Counter Animation ============
    const counters = document.querySelectorAll('.stat-number');
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = parseInt(counter.getAttribute('data-count'));
                const duration = 2000;
                const step = target / (duration / 16);
                let current = 0;
                
                const updateCounter = () => {
                    current += step;
                    if (current < target) {
                        counter.textContent = Math.floor(current).toLocaleString();
                        requestAnimationFrame(updateCounter);
                    } else {
                        counter.textContent = target.toLocaleString() + '+';
                    }
                };
                
                updateCounter();
                counterObserver.unobserve(counter);
            }
        });
    }, { threshold: 0.5 });
    
    counters.forEach(counter => counterObserver.observe(counter));
    
    // ============ Smooth Scroll for Anchor Links ============
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId !== '#') {
                e.preventDefault();
                const target = document.querySelector(targetId);
                if (target) {
                    const navHeight = navbar ? navbar.offsetHeight : 0;
                    const targetPosition = target.offsetTop - navHeight - 20;
                    
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
    
    // ============ Form Input Animations ============
    const formInputs = document.querySelectorAll('.form-modern .form-control');
    
    formInputs.forEach(input => {
        // Add wrapper for floating label effect
        const wrapper = input.closest('.form-group');
        if (wrapper) {
            input.addEventListener('focus', () => {
                wrapper.classList.add('focused');
            });
            
            input.addEventListener('blur', () => {
                if (!input.value) {
                    wrapper.classList.remove('focused');
                }
            });
            
            // Check initial state
            if (input.value) {
                wrapper.classList.add('focused');
            }
        }
    });
    
    // ============ Button Ripple Effect ============
    const buttons = document.querySelectorAll('.btn-modern, .btn-primary-modern, .btn-secondary-modern');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const ripple = document.createElement('span');
            ripple.className = 'ripple';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            
            this.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        });
    });
    
    // Add ripple CSS dynamically
    const rippleStyle = document.createElement('style');
    rippleStyle.textContent = `
        .btn-modern, .btn-primary-modern, .btn-secondary-modern {
            position: relative;
            overflow: hidden;
        }
        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.4);
            transform: scale(0);
            animation: ripple 0.6s ease-out;
            pointer-events: none;
        }
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(rippleStyle);
    
    // ============ Image Lazy Loading ============
    const lazyImages = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.add('loaded');
                imageObserver.unobserve(img);
            }
        });
    });
    
    lazyImages.forEach(img => imageObserver.observe(img));
    
    // ============ Gallery Modal / Lightbox ============
    const galleryItems = document.querySelectorAll('.gallery-item img, .responsive-gallery-img');
    
    galleryItems.forEach(img => {
        img.style.cursor = 'pointer';
        img.addEventListener('click', function() {
            createLightbox(this.src, this.alt);
        });
    });
    
    function createLightbox(src, alt) {
        const lightbox = document.createElement('div');
        lightbox.className = 'lightbox-overlay';
        lightbox.innerHTML = `
            <div class="lightbox-content">
                <button class="lightbox-close">&times;</button>
                <img src="${src}" alt="${alt}">
            </div>
        `;
        
        document.body.appendChild(lightbox);
        document.body.style.overflow = 'hidden';
        
        // Animate in
        setTimeout(() => lightbox.classList.add('active'), 10);
        
        // Close handlers
        lightbox.addEventListener('click', function(e) {
            if (e.target === lightbox || e.target.classList.contains('lightbox-close')) {
                closeLightbox(lightbox);
            }
        });
        
        document.addEventListener('keydown', function escHandler(e) {
            if (e.key === 'Escape') {
                closeLightbox(lightbox);
                document.removeEventListener('keydown', escHandler);
            }
        });
    }
    
    function closeLightbox(lightbox) {
        lightbox.classList.remove('active');
        setTimeout(() => {
            lightbox.remove();
            document.body.style.overflow = '';
        }, 300);
    }
    
    // Lightbox CSS
    const lightboxStyle = document.createElement('style');
    lightboxStyle.textContent = `
        .lightbox-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.9);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        .lightbox-overlay.active {
            opacity: 1;
        }
        .lightbox-content {
            position: relative;
            max-width: 90vw;
            max-height: 90vh;
        }
        .lightbox-content img {
            max-width: 100%;
            max-height: 90vh;
            border-radius: 8px;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
        }
        .lightbox-close {
            position: absolute;
            top: -40px;
            right: 0;
            width: 40px;
            height: 40px;
            background: transparent;
            border: none;
            color: white;
            font-size: 2rem;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .lightbox-close:hover {
            transform: scale(1.2);
        }
    `;
    document.head.appendChild(lightboxStyle);
    
    // ============ Toast Notifications ============
    window.showToast = function(message, type = 'success') {
        let container = document.querySelector('.toast-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'toast-container';
            document.body.appendChild(container);
        }
        
        const toast = document.createElement('div');
        toast.className = `toast-modern ${type}`;
        
        const icon = type === 'success' ? 'fa-check-circle' : 
                     type === 'error' ? 'fa-times-circle' : 
                     'fa-info-circle';
        
        toast.innerHTML = `
            <i class="fas ${icon}"></i>
            <span>${message}</span>
        `;
        
        container.appendChild(toast);
        
        setTimeout(() => {
            toast.style.animation = 'slideOutRight 0.3s ease forwards';
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    };
    
    // Toast CSS
    const toastStyle = document.createElement('style');
    toastStyle.textContent = `
        .toast-modern.success {
            border-left: 4px solid #10B981;
        }
        .toast-modern.success i {
            color: #10B981;
        }
        .toast-modern.error {
            border-left: 4px solid #EF4444;
        }
        .toast-modern.error i {
            color: #EF4444;
        }
        @keyframes slideOutRight {
            to {
                opacity: 0;
                transform: translateX(100%);
            }
        }
    `;
    document.head.appendChild(toastStyle);
    
    // ============ Mobile Menu Enhancements ============
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        navbarToggler.addEventListener('click', function() {
            this.classList.toggle('active');
        });
        
        // Close menu on link click
        navbarCollapse.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth < 992) {
                    navbarToggler.click();
                }
            });
        });
    }
    
    // ============ Parallax Effect for Hero ============
    const heroSection = document.querySelector('.hero-modern');
    
    if (heroSection) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const parallaxElements = heroSection.querySelectorAll('.carousel-item img');
            
            parallaxElements.forEach(el => {
                const speed = 0.3;
                el.style.transform = `translateY(${scrolled * speed}px)`;
            });
        });
    }
    
    // ============ Typing Effect for Hero Text ============
    const typingElements = document.querySelectorAll('.typing-effect');
    
    typingElements.forEach(el => {
        const text = el.textContent;
        el.textContent = '';
        let i = 0;
        
        function type() {
            if (i < text.length) {
                el.textContent += text.charAt(i);
                i++;
                setTimeout(type, 100);
            }
        }
        
        // Start typing when visible
        const typeObserver = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting) {
                type();
                typeObserver.disconnect();
            }
        });
        
        typeObserver.observe(el);
    });
    
    // ============ Tilt Effect for Cards ============
    const tiltCards = document.querySelectorAll('.tilt-effect');
    
    tiltCards.forEach(card => {
        card.addEventListener('mousemove', function(e) {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / 20;
            const rotateY = (centerX - x) / 20;
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
        });
        
        card.addEventListener('mouseleave', function() {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)';
        });
    });
    
    // ============ Cursor Custom Effect (Optional) ============
    /*
    const cursor = document.createElement('div');
    cursor.className = 'custom-cursor';
    document.body.appendChild(cursor);
    
    document.addEventListener('mousemove', (e) => {
        cursor.style.left = e.clientX + 'px';
        cursor.style.top = e.clientY + 'px';
    });
    
    document.querySelectorAll('a, button').forEach(el => {
        el.addEventListener('mouseenter', () => cursor.classList.add('hover'));
        el.addEventListener('mouseleave', () => cursor.classList.remove('hover'));
    });
    */
    
    console.log('🌍 Earthmai Foundation - Modern UI Loaded');
});

// ============ Preloader ============
window.addEventListener('load', function() {
    const preloader = document.querySelector('.preloader');
    if (preloader) {
        preloader.classList.add('fade-out');
        setTimeout(() => preloader.remove(), 500);
    }
});
