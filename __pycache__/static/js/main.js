// =============================================
// Puff n' Fleur - Main JavaScript
// =============================================

document.addEventListener('DOMContentLoaded', function() {
    initMobileMenu();
    initBackToTopButton();
    initFormValidation();
    hideFlashMessages();
});

/**
 * Initialize mobile navigation menu toggle
 */
function initMobileMenu() {
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');

    if (navToggle) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            
            // Animate hamburger icon
            const spans = this.querySelectorAll('span');
            if (navMenu.classList.contains('active')) {
                spans[0].style.transform = 'rotate(45deg) translate(10px, 10px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(7px, -7px)';
            } else {
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });

        // Close menu when a link is clicked
        const navLinks = navMenu.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                navMenu.classList.remove('active');
                const spans = navToggle.querySelectorAll('span');
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            });
        });
    }
}

/**
 * Initialize back-to-top button functionality
 */
function initBackToTopButton() {
    const backToTopBtn = document.getElementById('backToTopBtn');

    if (!backToTopBtn) return;

    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopBtn.classList.add('show');
        } else {
            backToTopBtn.classList.remove('show');
        }
    });

    backToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

/**
 * Basic form validation for booking form
 */
function initFormValidation() {
    const bookingForm = document.getElementById('bookingForm');

    if (bookingForm) {
        bookingForm.addEventListener('submit', function(e) {
            // Get form fields
            const fullName = document.getElementById('full_name').value.trim();
            const email = document.getElementById('email').value.trim();
            const phone = document.getElementById('phone').value.trim();
            const eventType = document.getElementById('event_type').value;
            const eventDate = document.getElementById('event_date').value;
            const eventLocation = document.getElementById('event_location').value.trim();

            // Validate required fields
            if (!fullName || !email || !phone || !eventType || !eventDate || !eventLocation) {
                e.preventDefault();
                showAlert('Please fill in all required fields.', 'error');
                return false;
            }

            // Validate email format
            if (!isValidEmail(email)) {
                e.preventDefault();
                showAlert('Please enter a valid email address.', 'error');
                return false;
            }

            // Validate phone format (basic)
            if (!isValidPhone(phone)) {
                e.preventDefault();
                showAlert('Please enter a valid phone number.', 'error');
                return false;
            }

            // Validate event date is in the future
            const selectedDate = new Date(eventDate);
            const today = new Date();
            today.setHours(0, 0, 0, 0);

            if (selectedDate < today) {
                e.preventDefault();
                showAlert('Event date must be in the future.', 'error');
                return false;
            }

            return true;
        });
    }
}

/**
 * Validate email format
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Validate phone format (basic check for digits)
 */
function isValidPhone(phone) {
    const phoneRegex = /^[\d\s\-\(\)]{10,}$/;
    return phoneRegex.test(phone.replace(/\s/g, ''));
}

/**
 * Show temporary alert message
 */
function showAlert(message, type) {
    // Create alert element
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.innerHTML = `
        ${message}
        <button class="alert-close" onclick="this.parentElement.style.display='none';">&times;</button>
    `;

    // Insert at top of page
    const mainContent = document.querySelector('main');
    if (mainContent) {
        mainContent.insertBefore(alert, mainContent.firstChild);
    }

    // Auto-remove after 5 seconds
    setTimeout(function() {
        if (alert.parentElement) {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.3s ease';
            setTimeout(function() {
                if (alert.parentElement) {
                    alert.remove();
                }
            }, 300);
        }
    }, 5000);
}

/**
 * Hide flash messages after 5 seconds
 */
function hideFlashMessages() {
    const flashMessage = document.getElementById('flashMessage');
    if (flashMessage) {
        setTimeout(function() {
            flashMessage.style.opacity = '0';
            flashMessage.style.transition = 'opacity 0.3s ease';
            setTimeout(function() {
                if (flashMessage.parentElement) {
                    flashMessage.remove();
                }
            }, 300);
        }, 5000);
    }
}

/**
 * Smooth scroll behavior for anchor links
 */
document.addEventListener('click', function(e) {
    if (e.target.tagName === 'A' && e.target.getAttribute('href').startsWith('#')) {
        const targetId = e.target.getAttribute('href').substring(1);
        const targetElement = document.getElementById(targetId);
        
        if (targetElement) {
            e.preventDefault();
            targetElement.scrollIntoView({ behavior: 'smooth' });
        }
    }
});

/**
 * Format phone number input in real-time
 */
document.addEventListener('DOMContentLoaded', function() {
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    
    phoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            
            if (value.length > 10) {
                value = value.slice(0, 10);
            }
            
            // Format: (XXX) XXX-XXXX
            if (value.length <= 3) {
                e.target.value = value;
            } else if (value.length <= 6) {
                e.target.value = `(${value.slice(0, 3)}) ${value.slice(3)}`;
            } else {
                e.target.value = `(${value.slice(0, 3)}) ${value.slice(3, 6)}-${value.slice(6)}`;
            }
        });
    });
});

/**
 * Add ripple effect to buttons on click
 */
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('btn')) {
        const button = e.target;
        const ripple = document.createElement('span');
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;

        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.style.position = 'absolute';
        ripple.style.background = 'rgba(255, 255, 255, 0.5)';
        ripple.style.borderRadius = '50%';
        ripple.style.animation = 'ripple-animation 0.6s ease-out';
        ripple.style.pointerEvents = 'none';

        // Add animation CSS if not already present
        if (!document.querySelector('style[data-ripple]')) {
            const style = document.createElement('style');
            style.setAttribute('data-ripple', 'true');
            style.textContent = `
                @keyframes ripple-animation {
                    from {
                        transform: scale(1);
                        opacity: 1;
                    }
                    to {
                        transform: scale(4);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
        }

        button.style.position = 'relative';
        button.style.overflow = 'hidden';
        button.appendChild(ripple);

        setTimeout(() => ripple.remove(), 600);
    }
});

/**
 * Lazy load images with placeholder
 */
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img');
    
    images.forEach(img => {
        if (img.complete) return; // Already loaded
        
        img.addEventListener('load', function() {
            this.style.animation = 'fadeIn 0.5s ease';
        });
        
        img.addEventListener('error', function() {
            this.style.opacity = '0.5';
        });
    });
});

console.log('%cWelcome to Puff n\' Fleur 🎈', 'font-size: 16px; color: #C47A8A; font-weight: bold;');
