"""
CORS Middleware for Django
Allows cross-origin requests from the frontend
"""

class CorsMiddleware:
    """
    Middleware to add CORS headers to responses
    Allows the frontend running on a different port to access the API
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Handle preflight requests
        if request.method == 'OPTIONS':
            from django.http import HttpResponse
            response = HttpResponse()
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
            response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
            response['Access-Control-Max-Age'] = '86400'  # 24 hours
            return response
        
        # Get the response
        response = self.get_response(request)
        
        # Add CORS headers to all responses
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        
        return response
