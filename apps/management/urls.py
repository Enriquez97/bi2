from django.urls import path
from .views.users import *
from .views.index import Home

urlpatterns = [
    path('login',login_view, name='login'),
    path('logout',logout_view, name='logout'),
    path('',Home.as_view(), name='home'),
]