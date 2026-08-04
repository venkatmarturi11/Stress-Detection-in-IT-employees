/**
 * Global Configuration
 * Determines the API base URL based on the current hostname
 */

const CONFIG = {
    // Dynamically determine the backend URL based on the current hostname
    // Some browsers (Chrome/Edge) are strict with 'localhost' vs '127.0.0.1' origins
    get API_BASE_URL() {
        const port = '8000';
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            return `http://${window.location.hostname}:${port}`;
        }
        // On Render, the API is served from the same origin
        return window.location.origin;
    }
};

console.log('Environment:', (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') ? 'Local' : 'Production');
console.log('API Base URL:', CONFIG.API_BASE_URL);

