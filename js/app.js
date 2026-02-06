/**
 * Stress Detection in IT Professionals
 * Main Application JavaScript
 */

// ===== Navbar Scroll Effect =====
const navbar = document.getElementById('navbar');

if (navbar) {
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  });
}

// ===== Mobile Menu Toggle =====
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const navMenu = document.querySelector('.nav-menu');

if (mobileMenuBtn && navMenu) {
  mobileMenuBtn.addEventListener('click', () => {
    navMenu.classList.toggle('active');
    mobileMenuBtn.classList.toggle('active');
  });
}

// ===== Sidebar Toggle (for mobile) =====
const sidebar = document.getElementById('sidebar');
const sidebarToggle = document.getElementById('sidebarToggle');

if (sidebarToggle && sidebar) {
  sidebarToggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
  });
}

// ===== Smooth Scroll for Anchor Links =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  });
});

// ===== Toast Notification System =====
function showToast(message, type = 'info') {
  const container = document.getElementById('toastContainer');
  if (!container) return;
  
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  
  const icons = {
    success: 'check-circle',
    error: 'exclamation-circle',
    warning: 'exclamation-triangle',
    info: 'info-circle'
  };
  
  toast.innerHTML = `
    <i class="fas fa-${icons[type] || 'info-circle'}"></i>
    <span>${message}</span>
  `;
  
  container.appendChild(toast);
  
  // Auto remove after 3 seconds
  setTimeout(() => {
    toast.style.animation = 'slideIn 0.3s ease-out reverse forwards';
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

// ===== Form Validation Helpers =====
function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}

function validatePhone(phone) {
  const re = /^[0-9]{10}$/;
  return re.test(phone.replace(/\D/g, ''));
}

function validatePassword(password) {
  return password.length >= 6;
}

// ===== Local Storage Helpers =====
function saveToStorage(key, data) {
  try {
    localStorage.setItem(key, JSON.stringify(data));
    return true;
  } catch (e) {
    console.error('Error saving to localStorage:', e);
    return false;
  }
}

function getFromStorage(key) {
  try {
    const data = localStorage.getItem(key);
    return data ? JSON.parse(data) : null;
  } catch (e) {
    console.error('Error reading from localStorage:', e);
    return null;
  }
}

// ===== Date Formatting =====
function formatDate(date) {
  const options = { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  };
  return new Date(date).toLocaleDateString('en-US', options);
}

function formatDateShort(date) {
  const options = { 
    month: 'short', 
    day: 'numeric'
  };
  return new Date(date).toLocaleDateString('en-US', options);
}

// ===== Animation on Scroll =====
function animateOnScroll() {
  const elements = document.querySelectorAll('.animate-on-scroll');
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-slideUp');
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.1
  });
  
  elements.forEach(el => observer.observe(el));
}

// ===== Initialize on DOM Load =====
document.addEventListener('DOMContentLoaded', () => {
  // Initialize animations
  animateOnScroll();
  
  // Add active class to current nav link
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link, .sidebar-link').forEach(link => {
    if (link.getAttribute('href') === currentPage) {
      link.classList.add('active');
    }
  });
});

// ===== Export functions for global use =====
window.showToast = showToast;
window.validateEmail = validateEmail;
window.validatePhone = validatePhone;
window.validatePassword = validatePassword;
window.saveToStorage = saveToStorage;
window.getFromStorage = getFromStorage;
window.formatDate = formatDate;
