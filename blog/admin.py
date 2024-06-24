from django.contrib import admin
from .models import Category, SubCategory, Profile, Post, Comment

# Register your models here.
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)