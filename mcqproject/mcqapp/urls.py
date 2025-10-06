# mcqapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Custom Admin URLs
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    path('admin/send-invitations/<int:quiz_id>/', views.send_invitations, name='send_invitations'),
    
    # User URLs
    
    path('quiz-result/<int:quiz_id>/', views.quiz_result, name='quiz_result'),
]