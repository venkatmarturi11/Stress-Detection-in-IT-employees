/**
 * Stress Detection - Advanced Animations & Interactions
 * Scroll reveal, animated counters, typewriter, theme toggle, back-to-top
 */

// ===== Scroll Reveal =====
function initScrollReveal() {
    const revealElements = document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-scale');
    if (revealElements.length === 0) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    revealElements.forEach(el => observer.observe(el));
}

// ===== Animated Counters =====
function initCounters() {
    const counters = document.querySelectorAll('[data-counter]');
    if (counters.length === 0) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(el => observer.observe(el));
}

function animateCounter(element) {
    const target = element.getAttribute('data-counter');
    const suffix = element.getAttribute('data-suffix') || '';
    const prefix = element.getAttribute('data-prefix') || '';
    const duration = parseInt(element.getAttribute('data-duration') || '2000');

    // Handle special values like "24/7"
    if (isNaN(parseInt(target))) {
        element.textContent = prefix + target + suffix;
        return;
    }

    const end = parseInt(target);
    const start = 0;
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);

        // Ease out cubic
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = Math.round(start + (end - start) * eased);

        element.textContent = prefix + current + suffix;

        if (progress < 1) {
            requestAnimationFrame(update);
        } else {
            element.textContent = prefix + target + suffix;
        }
    }

    requestAnimationFrame(update);
}

// ===== Typewriter Effect =====
function initTypewriter() {
    const elements = document.querySelectorAll('[data-typewriter]');
    elements.forEach(el => {
        const text = el.getAttribute('data-typewriter');
        const speed = parseInt(el.getAttribute('data-speed') || '80');
        el.textContent = '';
        el.classList.add('typewriter');

        let i = 0;
        function type() {
            if (i < text.length) {
                el.textContent += text.charAt(i);
                i++;
                setTimeout(type, speed);
            } else {
                // Remove cursor after typing completes
                setTimeout(() => {
                    el.style.borderRight = 'none';
                }, 1500);
            }
        }

        // Start typing when element is visible
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    setTimeout(type, 500);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        observer.observe(el);
    });
}

// ===== Theme Toggle =====
function initThemeToggle() {
    const toggle = document.getElementById('themeToggle');
    if (!toggle) return;

    // Check saved preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
        document.documentElement.setAttribute('data-theme', 'light');
        updateThemeIcon(toggle, 'light');
    } else {
        document.documentElement.setAttribute('data-theme', 'dark');
        updateThemeIcon(toggle, 'dark');
    }

    toggle.addEventListener('click', () => {
        const current = document.documentElement.getAttribute('data-theme');
        const newTheme = current === 'dark' ? 'light' : 'dark';

        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(toggle, newTheme);
    });
}

function updateThemeIcon(toggle, theme) {
    const icon = toggle.querySelector('i');
    if (!icon) return;
    icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
}

// ===== Back to Top Button =====
function initBackToTop() {
    const btn = document.getElementById('backToTop');
    if (!btn) return;

    window.addEventListener('scroll', () => {
        if (window.scrollY > 500) {
            btn.classList.add('visible');
        } else {
            btn.classList.remove('visible');
        }
    });

    btn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

// ===== Navbar Scroll Enhancement =====
function initNavbarScroll() {
    const navbar = document.getElementById('navbar');
    if (!navbar) return;

    let lastScrollTop = 0;

    window.addEventListener('scroll', () => {
        const scrollTop = window.scrollY;

        if (scrollTop > 100) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }

        lastScrollTop = scrollTop;
    });
}

// ===== Smooth Parallax for Hero =====
function initParallax() {
    const hero = document.querySelector('.hero');
    if (!hero) return;

    const floating = hero.querySelectorAll('.hero-float');

    window.addEventListener('scroll', () => {
        const scrolled = window.scrollY;
        if (scrolled > window.innerHeight) return;

        floating.forEach((el, i) => {
            const speed = 0.3 + (i * 0.1);
            el.style.transform = `translateY(${scrolled * speed}px)`;
        });
    });
}

// ===== Active Nav Highlight on Scroll =====
function initActiveNavOnScroll() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link[href^="#"]');

    if (sections.length === 0 || navLinks.length === 0) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.getAttribute('id');
                navLinks.forEach(link => {
                    link.classList.toggle('active', link.getAttribute('href') === `#${id}`);
                });
            }
        });
    }, { rootMargin: '-30% 0px -70% 0px' });

    sections.forEach(section => observer.observe(section));
}

// ===== Initialize All Animations =====
document.addEventListener('DOMContentLoaded', () => {
    initScrollReveal();
    initCounters();
    initTypewriter();
    initThemeToggle();
    initBackToTop();
    initNavbarScroll();
    initParallax();
    initActiveNavOnScroll();
});
