/**
 * Stress Detection in IT Professionals
 * Authentication JavaScript
 */

// ===== Registration Form Handler =====
const registerForm = document.getElementById('registerForm');

if (registerForm) {
    registerForm.addEventListener('submit', (e) => {
        e.preventDefault();

        // Get form values
        const fullName = document.getElementById('fullName').value.trim();
        const email = document.getElementById('email').value.trim().toLowerCase();
        const mobile = document.getElementById('mobile').value.trim();
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        const termsCheckbox = document.getElementById('termsCheckbox').checked;

        // Clear previous errors
        clearErrors();

        // Validate fields
        let isValid = true;

        if (fullName.length < 2) {
            showError('nameError', 'Please enter a valid name');
            isValid = false;
        }

        if (!validateEmail(email)) {
            showError('emailError', 'Please enter a valid email address');
            isValid = false;
        }

        if (!validatePhone(mobile)) {
            showError('mobileError', 'Please enter a valid 10-digit mobile number');
            isValid = false;
        }

        if (password.length < 6) {
            showError('passwordError', 'Password must be at least 6 characters');
            isValid = false;
        }

        if (password !== confirmPassword) {
            showError('confirmPasswordError', 'Passwords do not match');
            isValid = false;
        }

        if (!termsCheckbox) {
            showAlert('Please accept the Terms of Service', 'warning');
            isValid = false;
        }

        if (!isValid) return;

        // Check if email already exists
        const users = JSON.parse(localStorage.getItem('users') || '[]');
        if (users.some(u => u.email === email)) {
            showError('emailError', 'This email is already registered');
            showAlert('This email is already registered. Please use a different email or login.', 'warning');
            return;
        }

        // Create new user
        const newUser = {
            id: Date.now(),
            name: fullName,
            email: email,
            mobile: mobile,
            password: password, // In production, this should be hashed
            status: 'pending', // Needs admin activation
            registeredAt: new Date().toISOString()
        };

        // Save user
        users.push(newUser);
        localStorage.setItem('users', JSON.stringify(users));

        // Show success message
        showAlert('Registration successful! Please wait for admin activation before logging in.', 'success');

        // Reset form
        registerForm.reset();

        // Redirect after delay
        setTimeout(() => {
            window.location.href = 'login.html';
        }, 2000);
    });
}

// ===== Login Form Handler =====
const loginForm = document.getElementById('loginForm');

if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();

        // Get form values
        const email = document.getElementById('email').value.trim().toLowerCase();
        const password = document.getElementById('password').value;

        // Clear previous errors
        clearErrors();

        // Validate fields
        let isValid = true;

        if (!validateEmail(email)) {
            showError('emailError', 'Please enter a valid email address');
            isValid = false;
        }

        if (!password) {
            showError('passwordError', 'Please enter your password');
            isValid = false;
        }

        if (!isValid) return;

        // Find user
        const users = JSON.parse(localStorage.getItem('users') || '[]');
        const user = users.find(u => u.email === email && u.password === password);

        if (!user) {
            showAlert('Invalid email or password. Please try again.', 'danger');
            return;
        }

        // Check if user is activated
        if (user.status !== 'active') {
            showAlert('Your account is pending activation. Please contact the admin.', 'warning');
            return;
        }

        // Save current user session
        localStorage.setItem('currentUser', JSON.stringify({
            id: user.id,
            name: user.name,
            email: user.email,
            mobile: user.mobile
        }));

        // Show success
        showAlert('Login successful! Redirecting...', 'success');

        // Redirect to dashboard
        setTimeout(() => {
            window.location.href = 'user-dashboard.html';
        }, 1000);
    });
}

// ===== Validation Functions =====
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePhone(phone) {
    const cleaned = phone.replace(/\D/g, '');
    return cleaned.length >= 10;
}

// ===== Error Display Functions =====
function showError(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = message;
        element.classList.remove('d-none');

        // Add error class to input
        const inputGroup = element.previousElementSibling;
        if (inputGroup) {
            const input = inputGroup.querySelector('.form-input') || inputGroup;
            input.classList.add('error');
        }
    }
}

function clearErrors() {
    document.querySelectorAll('.form-error').forEach(el => {
        el.classList.add('d-none');
        el.textContent = '';
    });

    document.querySelectorAll('.form-input').forEach(el => {
        el.classList.remove('error');
        el.classList.remove('success');
    });
}

// ===== Alert Display =====
function showAlert(message, type = 'info') {
    const alertElement = document.getElementById('alertMessage');
    const alertText = document.getElementById('alertText');

    if (alertElement && alertText) {
        alertText.textContent = message;
        alertElement.className = `alert alert-${type}`;
        alertElement.classList.remove('d-none');

        // Update icon
        const icon = alertElement.querySelector('i');
        if (icon) {
            const icons = {
                success: 'check-circle',
                warning: 'exclamation-triangle',
                danger: 'exclamation-circle',
                info: 'info-circle'
            };
            icon.className = `fas fa-${icons[type] || 'info-circle'}`;
        }

        // Auto hide after 5 seconds for non-error alerts
        if (type !== 'danger') {
            setTimeout(() => {
                alertElement.classList.add('d-none');
            }, 5000);
        }
    }
}

// ===== Check Authentication =====
function checkAuth() {
    const currentUser = localStorage.getItem('currentUser');
    if (!currentUser) {
        window.location.href = 'login.html';
        return null;
    }
    return JSON.parse(currentUser);
}

// ===== Logout =====
function logout() {
    localStorage.removeItem('currentUser');
    window.location.href = 'index.html';
}

// Export for global use
window.checkAuth = checkAuth;
window.logout = logout;
