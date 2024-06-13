from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:pk>', views.post, name='post'),
    path('my_post/', views.my_post, name='my_post'),
    path('create_post/', views.create_post, name='create_post'),
    # path('update_post/<id:pk>/update', views.update_post, name='update_post'),
    path('delete_post/', views.delete_post, name='delete_post'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('search/', views.search, name='search'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)