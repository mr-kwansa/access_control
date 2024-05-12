from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('micro_focus_admin/',views.micro_focus_admin,name='micro_focus_admin'),
    path('api/micro_focus_admin/', views.micro_focus_admin_api, name='micro_focus_admin_api'),
    path('toggle_access_key_status/<int:access_key_id>/',views.toggle_access_key_status, name='toggle_access_key_status'),
    path('school_integration_endpoint/', views.school_integration_endpoint, name='school_integration_endpoint'),

    
    
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('generate_access_key/', views.generate_access_key, name='generate_access_key'),
    
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name='login/reset_password.html'),
         name='reset_password'),
    
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='login/reset_password_sent.html'),
         name='password_reset_done'),
    
    path('reset_password/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='login/password_reset_form.html'), 
         name='password_reset_confirm'),
    
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='login/password_reset_done.html'),
         name='password_reset_complete'),
    
]
