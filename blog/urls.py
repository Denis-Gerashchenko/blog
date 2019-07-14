from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from posts.views import (
                           IndexView, single, BlogView,
                           search, TestView, update,
                           delete, create, profile,
                           UpdateProfileView, another_user_view,
                           delete_comment,
                        )



urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('single/<id>/', single, name='post-detail'),
    path('blog/', BlogView.as_view(), name='post-list'),
    path('search/', search, name='search'),
    path('tinymce/', include('tinymce.urls')),
    path('test/', TestView.as_view(), name='test-zone'),
    path('single/<id>/update', update, name='post-update'),
    path('single/<id>/delete', delete, name='post-delete'),
    path('comment/<id>/delete', delete_comment, name='comment-delete'),
    path('create/', create, name='post-create'),
    path('update/', update, name='post-update'),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/profile/update/', UpdateProfileView.as_view(), name='profile-update'),
    path('accounts/profile/<username>', another_user_view, name='another-user'),

    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
