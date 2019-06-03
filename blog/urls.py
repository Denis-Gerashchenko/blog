from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from posts.views import index, single, blog



urlpatterns = [
    path('', index),
    path('single/', single),
    path('blog/', blog),

    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

