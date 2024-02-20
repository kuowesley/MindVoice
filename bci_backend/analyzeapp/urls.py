from django.urls import path
from . import views

urlpatterns = [
    path('analyze/', views.analyze, name='analyze'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
]
