from django.urls import path
from .views.old_apps import FinanzasBg,FinanzasBap,FinanzasActivo,FinanzasPasivo

urlpatterns = [
    path('balance-general',FinanzasBg.as_view(),name='balance-general'),
    path('balance-ap',FinanzasBap.as_view(),name='balance_ap'),
    path('analisis-activo',FinanzasActivo.as_view(),name='analisis_activo'),
    path('analisis-pasivo',FinanzasPasivo.as_view(),name='analisis_pasivo'),
]