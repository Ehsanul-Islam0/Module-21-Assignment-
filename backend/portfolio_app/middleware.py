import logging
import time

logger = logging.getLogger(__name__)


class RequestTimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.perf_counter()
        response = self.get_response(request)
        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
        logger.info('%s %s -> %s (%sms)', request.method, request.path, response.status_code, duration_ms)
        response['X-Response-Time'] = f'{duration_ms}ms'
        return response
