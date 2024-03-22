from django.urls import path
from . import views

urlpatterns = [
    path('analyze/', views.analyze, name='analyze'),
    path('register/', views.register, name='register'),
    path('get_user_info/', views.get_user_info, name='get_user_info'),
    path('login/', views.login_view, name='login'),
    path('health/', views.health, name='health'),
]
