from django.urls import path
from . import views

urlpatterns = [
    path('analyze/', views.analyze, name='analyze'),
    path('register/', views.register, name='register'),
    path('get_user_info/', views.get_user_info, name='get_user_info'),
    path('login/', views.login_view, name='login'),
    path('get-user-emails/', views.get_user_emails, name='get-user-emails'),
    path('health/', views.health, name='health'),
    path('send-email-notifications/', views.send_email_notifications, name='send-email-notifications'),
    path('delete_user/', views.delete_user, name='delete_user'),
]
