// API Configuration
const API_BASE_URL = 'http://localhost:8000'; // Update this if your backend runs elsewhere

// ===== Registration Form Handler =====
const registerForm = document.getElementById('registerForm');

if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
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

        try {
            // Show loading state
            const submitBtn = registerForm.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Registering...';

            const response = await fetch(`${API_BASE_URL}/api/register/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: fullName,
                    email: email,
                    mobile: mobile,
                    password: password
                })
            });

            const result = await response.json();

            if (result.success) {
                showAlert('Registration successful! Redirecting to login...', 'success');
                registerForm.reset();
                setTimeout(() => {
                    window.location.href = 'login.html';
                }, 2000);
            } else {
                showError('emailError', result.error || 'Registration failed');
                showAlert(result.error || 'Registration failed. Please try again.', 'danger');
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnText;
            }
        } catch (error) {
            console.error('Registration error:', error);
            showAlert('Backend server error. Please ensure the Django server is running.', 'danger');
            const submitBtn = registerForm.querySelector('button[type="submit"]');
            submitBtn.disabled = false;
            submitBtn.innerHTML = 'Create Account';
        }
    });
}

// ===== Login Form Handler =====
const loginForm = document.getElementById('loginForm');

if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
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

        try {
            // Show loading state
            const submitBtn = loginForm.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Logging in...';

            const response = await fetch(`${API_BASE_URL}/api/login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            });

            const result = await response.json();

            if (result.success) {
                // Save current user session in localStorage for frontend access
                localStorage.setItem('currentUser', JSON.stringify(result.user));
                
                showAlert('Login successful! Redirecting...', 'success');
                setTimeout(() => {
                    window.location.href = 'user-dashboard.html';
                }, 1000);
            } else {
                showAlert(result.error || 'Invalid email or password.', 'danger');
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnText;
            }
        } catch (error) {
            console.error('Login error:', error);
            showAlert('Backend server error. Please ensure the Django server is running.', 'danger');
            const submitBtn = loginForm.querySelector('button[type="submit"]');
            submitBtn.disabled = false;
            submitBtn.innerHTML = 'Login';
        }
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
