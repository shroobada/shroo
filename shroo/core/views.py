from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def health_check(request):
    """
    Health check endpoint for API status verification
    """
    return Response({
        'status': 'healthy',
        'message': 'Django API is running',
        'debug': request.query_params.get('debug', False)
    })