from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:post_id>/', views.post, name='post'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/comment/<int:parent_id>/', views.add_comment, name='add_comment_reply'),
    path('my_post/', views.my_post, name='my_post'),
    path('my_post/create_post/', views.create_post, name='create_post'),
    path('my_post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('my_post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('search/', views.search, name='search'),
    path('seccion/<slug:name>/', views.seccion, name='seccion'),
    path('category/<slug:categoryName>/', views.category, name='category'),
    path('ajax/load-subcategories/', views.load_subcategories, name='load_subcategories'),
]