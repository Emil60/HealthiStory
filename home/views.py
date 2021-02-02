from django.shortcuts import render
import geoip2.database
from django.core.mail import send_mail
from django.conf import settings


def home_view(request):
    """Render homepage"""
    reader = geoip2.database.Reader('./GeoLite2-City_20210126/GeoLite2-City.mmdb')
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    response = reader.city(ip)
    email_from = settings.EMAIL_HOST_USER
    subject = "Country Check"
    message = f"""
                IP: {ip}
                Country ISO code: {response.country.iso_code}
                Country name: {response.country.name}
                City Name: {response.city.name}"""
    recipient_list = ['ojagverdiyev13@gmail.com']
    send_mail(subject, message, email_from, recipient_list)

    reader.close()
    return render(request, 'home/index.html')


def contact_us_view(request):
    """Render Contact us view"""
    return render(request, 'home/contact.html')


def location(request):
    """Render Contact us view"""
    return render(request, 'home/location.html')
