from django.urls import path, include
from . import views

urlpatterns = [
    path('profile', views.user_account, name="profile"),
    path('profile/edit', views.user_account_edit, name="user_edit"),
    path('profile/changePassword', views.user_password_change, name="change_password"),
    path('profile/reports', views.user_reports, name="reports"),
    path('profile/askExpert', views.user_ask_expert, name="ask_expert"),
    path('register', views.user_register, name="register"),
    path('login', views.user_login, name="login"),
    path('logout', views.user_logout, name="logout"),
    path('ajax/load-cities', views.load_cities, name='ajax_load_cities'),
    path('ajax/load-districts/', views.load_districts, name='ajax_load_districts'),
    path('ajax/load-towns/', views.load_towns, name='ajax_load_towns'),

]
