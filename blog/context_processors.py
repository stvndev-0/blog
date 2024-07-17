from django.shortcuts import get_object_or_404
from .models import Category, Post

def all_category(request):
    categories = Category.objects.all()
    return {'categories': categories }