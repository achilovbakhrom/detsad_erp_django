from rest_framework.response import Response
from rest_framework import status

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def error_response(msg, status = status.HTTP_500_INTERNAL_SERVER_ERROR):
    return Response(
        {"error": msg},
        status
    )
    
def success_response(data, status = status.HTTP_200_OK):
    return Response(data, status)
