from django.urls import path
from .views.create import CreateLayout, ShowLayout

urlpatterns = [
    path('create-layout',CreateLayout.as_view(),name='create_layout'),
    path('show-layout',ShowLayout.as_view(),name='show_layout'),
]