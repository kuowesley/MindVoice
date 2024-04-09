from django.urls import path
from . import controllers

urlpatterns = [
    path('analyze/', controllers.analyze, name='analyze'),
    path('register/', controllers.register, name='register'),
    path('get_user_info/', controllers.get_user_info, name='get_user_info'),
    path('login/', controllers.login_view, name='login'),
    path('get-user-emails/', controllers.get_user_emails, name='get-user-emails'),
    path('health/', controllers.health, name='health'),
    path('send-email-notifications/', controllers.send_email_notifications, name='send-email-notifications'),
    path('log-usage/', controllers.log_usage, name='log-usage'),
    path('create-user-feedback/', controllers.create_user_feedback, name='create-user-feedback'),
]
