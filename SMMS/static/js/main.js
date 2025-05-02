// Main JavaScript file for Arthavidya Trading Community

document.addEventListener('DOMContentLoaded', function() {
    // Initialize mobile menu
    initMobileMenu();
    
    // Initialize animations
    initAnimations();
    
    // Initialize login modal
    initLoginModal();
    
    // Initialize scroll effects
    initScrollEffects();
    
    // Set animation indices for staggered an imations
    setAnimationIndices();
});

// Mobile Menu Toggle
function initMobileMenu() {
    const menuToggle = document.querySelector('.mobile-menu-toggle');
    const mainNav = document.querySelector('.main-nav');
    
    if (menuToggle && mainNav) {
        menuToggle.addEventListener('click', function() {
            mainNav.classList.toggle('active');
            document.body.classList.toggle('menu-open');
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!event.target.closest('.main-nav') && !event.target.closest('.mobile-menu-toggle') && mainNav.classList.contains('active')) {
                mainNav.classList.remove('active');
                document.body.classList.remove('menu-open');
            }
        });
    }
}

// Initialize animations
function initAnimations() {
    // Add animation classes to elements that should animate on page load
    document.querySelectorAll('.feature-item, .reason-item, .stat-item, .trainer-card, .partner-logo').forEach(function(element, index) {
        element.style.setProperty('--i', index + 1);
        element.classList.add('animate-on-load');
    });
}

// Initialize scroll effects
function initScrollEffects() {
    // Add scroll event listener
    window.addEventListener('scroll', function() {
        // Parallax effect on hero banner
        const heroSection = document.querySelector('.hero-banner');
        if (heroSection) {
            const scrollPosition = window.scrollY;
            heroSection.style.backgroundPosition = `center ${scrollPosition * 0.5}px`;
        }
        
        // Reveal animations on scroll
        revealOnScroll();
    });
}

// Reveal elements on scroll
function revealOnScroll() {
    const elements = document.querySelectorAll('.section-heading, .different-content, .reason-item, .founder-content, .trainer-card, .partner-logo');
    
    elements.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const windowHeight = window.innerHeight;
        
        if (elementTop < windowHeight - 100) {
            element.classList.add('visible');
        }
    });
}

// Set animation indices for staggered animations
function setAnimationIndices() {
    const staggeredElements = document.querySelectorAll('.feature-item, .reason-item, .stat-item, .trainer-card');
    
    staggeredElements.forEach((element, index) => {
        element.style.setProperty('--i', index + 1);
    });
}

// Show notification
function showNotification(message, type = 'success') {
    // Create notification element if it doesn't exist
    if (!document.querySelector('.notification')) {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Show notification
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);
        
        // Hide and remove notification after 3 seconds
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }
}

// Add the following CSS to your style.css for notifications
/*
.notification {
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 15px 20px;
    border-radius: var(--border-radius);
    color: white;
    font-weight: 500;
    box-shadow: var(--box-shadow-md);
    z-index: 2000;
    transform: translateX(100%);
    opacity: 0;
    transition: transform 0.3s ease, opacity 0.3s ease;
}

.notification.show {
    transform: translateX(0);
    opacity: 1;
}

.notification.success {
    background-color: #28a745;
}

.notification.error {
    background-color: #dc3545;
}

.notification.warning {
    background-color: #ffc107;
    color: #333;
}
*/