from django.contrib import admin

from .models import Category, Post, Comment, Media, PostCategory, Reply

admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Media)
admin.site.register(Reply)