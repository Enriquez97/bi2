from django.urls import path
from .views.explorer import ExplorerData

urlpatterns = [
    path('explorer-data',ExplorerData.as_view(),name='explorer_data'),
]