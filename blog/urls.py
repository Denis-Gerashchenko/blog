from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from posts.views import index, single, blog, search



urlpatterns = [
    path('', index),
    path('single/<id>/', single, name='post-detail'),
    path('blog/', blog, name='post-list'),
    path('search/', search, name='search'),
    path('tinymce/', include('tinymce.urls')),

    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

