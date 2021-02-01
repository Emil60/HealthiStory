from django.shortcuts import render


def home_view(request):
    """Render homepage"""
    return render(request, 'home/index.html')


def contact_us_view(request):
    """Render Contact us view"""
    return render(request, 'home/contact.html')


def location(request):
    """Render Contact us view"""
    return render(request, 'home/location.html')
