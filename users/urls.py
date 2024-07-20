from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:user_id>/', views.profile, name='profile_user'),
    path('profile/update_profile/', views.update_profile, name='update_profile'), 
    path('profile/update_password/', views.update_password, name='update_password'),
]