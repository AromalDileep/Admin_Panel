from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.log_in, name='login'),
    path('home/', views.home, name='home'),
    path('adminpanel/', views.adminpanel, name='adminpanel'),
    
    path('', views.log_out, name='log_out'),  # Corrected URL for logout
]
