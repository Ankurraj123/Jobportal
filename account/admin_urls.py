from django.urls import path
from account import admin_views

app_name = 'admin_panel'

urlpatterns = [
    path('', admin_views.admin_dashboard, name='dashboard'),
    path('employees/', admin_views.admin_employees, name='employees'),
    path('employers/', admin_views.admin_employers, name='employers'),
    path('jobs/', admin_views.admin_jobs, name='jobs'),
    path('user/<int:user_id>/', admin_views.admin_user_detail, name='user_detail'),
    path('user/<int:user_id>/edit/', admin_views.admin_user_edit, name='user_edit'),
    path('user/<int:user_id>/toggle/', admin_views.admin_toggle_user, name='toggle_user'),
    path('job/<int:job_id>/', admin_views.admin_job_detail, name='job_detail'),
    path('job/<int:job_id>/approve/', admin_views.admin_job_approve, name='job_approve'),
    path('job/<int:job_id>/delete/', admin_views.admin_job_delete, name='job_delete'),
]
