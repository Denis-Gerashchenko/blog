from django.contrib import admin

# Register your models here.

from .models import Author, Category, Post, Comment, PostViewCount

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostViewCount)
