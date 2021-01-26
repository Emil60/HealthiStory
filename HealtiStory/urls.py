from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
      path('i18n/', include('django_translation_flags.urls')),
      path('admin/', admin.site.urls),
      path('', include('home.urls')),
      path('products/', include('product.urls')),
      path('account/', include('account.urls')),


      path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(
          template_name='account/password_reset_done.html'),
           name='password_reset_done'),

      path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
          template_name='account/password_reset_confirm.html'),
           name='password_reset_confirm'),

      path('password_reset/', auth_views.PasswordResetView.as_view(
          email_template_name='account/password_reset_email.html',
          subject_template_name='account/password_reset_subject.txt',
          template_name='account/password_reset_form.html'),
           name='password_reset'),

      path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
          template_name='account/password_reset_complete.html'),
           name='password_reset_complete'),

      ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
