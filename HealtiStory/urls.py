from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
      path('i18n/', include('django_translation_flags.urls')),
      path('admin/', admin.site.urls),
      path('', include('home.urls')),
      path('products/', include('product.urls')),
      path('account/', include('account.urls')),
      ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
