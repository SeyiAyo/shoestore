import logging
import json
import traceback
from datetime import datetime
from django.http import JsonResponse
from rest_framework import status
from django.conf import settings

# Define log directory
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configure logging
logger = logging.getLogger('store')
logger.setLevel(logging.DEBUG)

# Create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(ch)

def log_debug(message, extra=None):
    """Log debug message with optional extra data"""
    if extra:
        message = f"{message} - Extra: {json.dumps(extra)}"
    logger.debug(message)

def log_error(message, exc=None, extra=None):
    """Log error message with optional exception and extra data"""
    if exc:
        tb = ''.join(traceback.format_tb(exc.__traceback__))
        message = f"{message}\nException: {str(exc)}\nTraceback:\n{tb}"
    if extra:
        message = f"{message}\nExtra: {json.dumps(extra)}"
    logger.error(message)

class APIDebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log request
        self._log_request(request)
        
        try:
            response = self.get_response(request)
            # Log response
            self._log_response(request, response)
            return response
        except Exception as e:
            # Log error
            log_error("An error occurred", e)
            return self.handle_error(e)

    def _log_request(self, request):
        """Log incoming request details"""
        headers = dict(request.headers)
        # Remove sensitive information
        if 'Authorization' in headers:
            headers['Authorization'] = '[FILTERED]'
        
        body = None
        if request.body:
            try:
                body = json.loads(request.body)
            except json.JSONDecodeError:
                body = "Could not parse request body"
        
        log_debug(
            f"\nREQUEST: {request.method} {request.path}",
            {
                "headers": headers,
                "query_params": dict(request.GET),
                "body": body
            }
        )

    def _log_response(self, request, response):
        """Log outgoing response details"""
        content = None
        if hasattr(response, 'content'):
            try:
                content = response.content.decode('utf-8')
            except:
                content = "[Binary content]"
        
        log_debug(
            f"\nRESPONSE: {request.method} {request.path}",
            {
                "status": response.status_code,
                "content": content
            }
        )

    def handle_error(self, exception):
        error_response = {
            'error': {
                'type': type(exception).__name__,
                'message': str(exception),
                'timestamp': datetime.now().isoformat()
            }
        }
        
        if settings.DEBUG:
            error_response['error']['traceback'] = traceback.format_exc()
        
        return JsonResponse(
            error_response,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

def api_error_response(message, status_code=status.HTTP_400_BAD_REQUEST, extra=None):
    """Utility function to return consistent error responses"""
    response = {
        'error': {
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
    }
    
    if extra:
        response['error'].update(extra)
    
    if settings.DEBUG:
        response['error']['debug_info'] = {
            'status_code': status_code,
            'extra': extra
        }
    
    return JsonResponse(response, status=status_code)
