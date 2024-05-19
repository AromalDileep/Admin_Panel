from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name = 'signup'),
    path('login/', views.log_in, name = 'login'),
    path('home/', views.home, name = 'home'),
    path('', views.log_out, name = 'log_out'),  # Corrected URL for logout
    path('adminlogin/', views.adminlogin, name = 'adminlogin'),
    path('adminpanel/', views.adminpanel, name = 'adminpanel'),
    path('adminlogout/', views.adminlogout, name = 'adminlogout'),  # Correct reference
    path('create/', views.create, name = 'create'),
    path('edit/<int:user_id>/', views.edituser, name='edit'),
    path('delete/<int:user_id>/', views.deleteuser, name='deleteuser'),
        
]
