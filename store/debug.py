import logging
import traceback
import json
import os
from datetime import datetime
from django.http import JsonResponse
from rest_framework import status
from django.conf import settings

# Define log directory
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configure logging
logger = logging.getLogger('store.debug')
logger.setLevel(logging.DEBUG)

# Create file handler
log_file = os.path.join(LOG_DIR, 'debug.log')
fh = logging.FileHandler(log_file)
fh.setLevel(logging.DEBUG)

# Create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(fh)
logger.addHandler(ch)

class APIDebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log request
        self.log_request(request)
        
        try:
            response = self.get_response(request)
            # Log response
            self.log_response(request, response)
            return response
        except Exception as e:
            # Log error
            self.log_error(request, e)
            return self.handle_error(e)

    def log_request(self, request):
        logger.debug(f"""
REQUEST: {request.method} {request.path}
Headers: {dict(request.headers)}
Query Params: {dict(request.GET)}
Body: {self.get_request_body(request)}
        """)

    def log_response(self, request, response):
        logger.debug(f"""
RESPONSE: {request.method} {request.path}
Status: {response.status_code}
Content: {self.get_response_content(response)}
        """)

    def log_error(self, request, exception):
        logger.error(f"""
ERROR: {request.method} {request.path}
Type: {type(exception).__name__}
Message: {str(exception)}
Traceback:
{traceback.format_exc()}
        """)

    def get_request_body(self, request):
        try:
            if request.content_type and 'application/json' in request.content_type:
                return json.loads(request.body)
            return request.POST
        except:
            return 'Could not parse request body'

    def get_response_content(self, response):
        try:
            return response.content.decode('utf-8')
        except:
            return 'Could not decode response content'

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

def log_debug(message, extra=None):
    """Utility function to log debug messages"""
    if extra:
        logger.debug(f"{message} - Extra: {json.dumps(extra, default=str)}")
    else:
        logger.debug(message)

def log_error(message, exception=None, extra=None):
    """Utility function to log error messages"""
    if exception:
        logger.error(f"{message}\nException: {str(exception)}\nTraceback:\n{traceback.format_exc()}")
    elif extra:
        logger.error(f"{message} - Extra: {json.dumps(extra, default=str)}")
    else:
        logger.error(message)

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
