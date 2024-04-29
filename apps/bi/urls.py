from django.urls import path
from . import views
from .views.build import CreateDash,BuildDash

urlpatterns = [
    #path('', views.home, name='test_view'),
    path('create-dashboard', CreateDash.as_view(), name='create_dashboard'),
    path('build-dashboard', BuildDash.as_view(), name='build_dashboard')
]