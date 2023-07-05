from django.shortcuts import redirect
from django.urls import reverse

class RemoveNextParameterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 302 and response.url.startswith(reverse('login')):
            response = redirect(reverse('index'))

        return response