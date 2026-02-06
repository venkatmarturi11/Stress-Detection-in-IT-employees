/**
 * Global Configuration
 * Determines the API base URL based on the current hostname
 */

const CONFIG = {
    // If running on localhost/127.0.0.1, use local backend
    // Otherwise, use the production backend URL (User needs to update this after deployment)
    API_BASE_URL: (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
        ? 'http://localhost:8000'
        : 'https://stress-detection-backend.onrender.com' // Placeholder: Update this after deploying backend
};

console.log('Environment:', (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') ? 'Local' : 'Production');
console.log('API Base URL:', CONFIG.API_BASE_URL);
