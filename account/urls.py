from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('profile', views.user_account, name="profile"),
    path('profile/edit', views.user_account_edit, name="user_edit"),
    path('profile/changePassword', views.user_password_change, name="change_password"),
    path('profile/reports', views.user_reports, name="reports"),
    path('profile/askExpert', views.user_ask_expert, name="ask_expert"),
    path('register', views.user_register, name="register"),
    path('login', views.user_login, name="login"),
    path('logout', views.user_logout, name="logout"),


    path('doctor/profile', views.doctor_account, name="doctor_profile"),
    path('doctor/login', views.doctor_login, name="doctor_login"),
    path('doctor/questions', views.doctor_questions, name="doctor_questions"),





    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='account/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('password_reset/', views.password_reset_request, name="password_reset"),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password_reset_complete.html'),
         name='password_reset_complete'),

    path('ajax/load-cities', views.load_cities, name='ajax_load_cities'),
    path('ajax/load-districts/', views.load_districts, name='ajax_load_districts'),
    path('ajax/load-towns/', views.load_towns, name='ajax_load_towns'),

]
