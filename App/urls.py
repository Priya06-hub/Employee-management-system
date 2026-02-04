from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.manage_profile, name='profile'),
    path('profile/<str:emp_id>/', views.manage_profile, name='admin_edit_profile'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    # path('reset_password/<int:emp_id>/', views.reset_password, name='reset_password'),
    path('change_password/', views.change_password, name='change_password'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('create-profile/', views.create_profile, name='create_profile'),
    path('emp-dashboard/', views.emp_dashboard, name='emp_dashboard'),
    path('manager-dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('hr-dashboard/', views.hr_dashboard, name='hr_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('mark_attendance/',views.mark_attendance,name='mark_attendance'),
    path('mn_attendance/', views.mn_attendance, name='mn_attendance'),
    path('apply_leave/', views.apply_leave, name='apply_leave'),
    path('leave_approval/<str:leave_id>/',views.leave_approval,name='leave_approval'),
    path('leave_list/',views.leave_list,name='leave_list'),
    path('mn_salary/',views.mn_salary,name='manager_salary'),
    path('mn_tasks/',views.mn_task,name='manager_task'),
    path('mn_performance/',views.mn_performance,name='manager_performance'),
    path('task_list/', views.task_list, name='task_list'),
    path('emp_task_list/', views.emp_task_list, name='emp_task_list'),
    # path('as_task/', views.assign_Task, name='assign_task'),

    # path('profile/<int:emp_id>/', views.view_profile, name='view_profile'),
    # path('salary_slip/<int:emp_id>/', views.salary_slip, name='salary_slip'),
    path('contact/',views.contact,name='contact'),
    path('features/',views.features,name='features'),
    path('modify_attendance/', views.modify_att, name='modify_attendance'),

    # path('modify_attendance/<str:atendance_id>/',views.modify_att,name='modify_attendance'),

    # path('modify_attendance/<str:attendance_id>/', views.modify_att, name='modify_attendance'),
    # path('attendance_list/',views.attendance_list,name='attendance_list'),
    # path('create/',views.create_profile,name='create_profile'),
    # path('edit/<int:emp_id>/',views.edit_profile,name='edit_profile'),   
    # urls.py
 
 
]

