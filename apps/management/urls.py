from django.urls import path
from .views.users import *
from .views.index import Home

urlpatterns = [
    path('login',login_view, name='login'),
    path('logout',logout_view, name='logout'),
    path('',Home.as_view(), name='home'),
    
    path('create-user',FormNewuserDash.as_view(), name='create_user'),
    path('create-empresa',FormNewCompanyDash.as_view(), name='create_empresa'),
    
    path('usuarios',ShowUsuarios.as_view(), name='usuarios'),
    path('empresas',ShowEmpresa.as_view(), name='empresas'),
    
    path('update-user/<str:id>',FormModuserDash.as_view(), name='update_user'),
    
]