import json
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import permissions

class HomeView(APIView):
    permission_classes = (permissions.AllowAny,)
    ordering = ['-updated']

    def get(self, *args, **kwargs):
        json_response = {
            'text': 'This is a text from back'
        }
        return HttpResponse(json.dumps(json_response), 'application/json', status=200)
