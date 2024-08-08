from .models import Category

def all_category(request):
    categories = Category.objects.all()
    return {'categories': categories }