from django.shortcuts import render

# Create your views here.

def landing_page(request):
    """Landing page view"""
    return render(request, 'app/landing.html')