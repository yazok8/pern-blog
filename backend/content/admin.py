from django.contrib import admin
from .models import Category, Tag, Post, Article, Comment, Like, ArticleLike

# Registering Models so they appear in the Django admin interface.
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(ArticleLike)
