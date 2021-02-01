from django.urls import path, re_path, include
from . import views
urlpatterns = [
    re_path(r'^$', views.home_view, name='home'),
    path('contact-us', views.contact_us_view, name='contact-us'),
    path('locations', views.location, name='location')
]
