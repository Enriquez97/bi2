from django.urls import path
from .views.sp import ShowAPI,NewTheme
from .views.old_apps import (
    HomeOld,
    FinanzasBg,FinanzasBap,FinanzasActivo,FinanzasPasivo,
    LogisticaStocks,EstadoInventario,GestionStocks,
    InformeVentas,ResumenVentas,
    AsyncHomeView,
    AgricolaCampania,AgricolaCostos
)


urls_home = [
    path('',HomeOld.as_view(),name='home_old'),
]

urls_finanzas = [
    path('balance-general',FinanzasBg.as_view(),name='balance-general'),
    path('balance-ap',FinanzasBap.as_view(),name='balance_ap'),
    path('analisis-activo',FinanzasActivo.as_view(),name='analisis_activo'),
    path('analisis-pasivo',FinanzasPasivo.as_view(),name='analisis_pasivo'),
]

urls_logistica = [
    path('stocks',LogisticaStocks.as_view(),name='logistica_stocks'),
    path('estado-inventario',EstadoInventario.as_view(),name='estado_inventario'),
    path('gestion-stocks',GestionStocks.as_view(),name='gestion_stocks'),
]

urls_comercial = [
    path('informe-ventas',InformeVentas.as_view(),name='informe_ventas'),
    path('resumen-ventas',ResumenVentas.as_view(),name='resumen_ventas'),

]

url_produccion = [
    path('agricola-ejecucion',AgricolaCampania.as_view(),name='ejecucion_agricola'),
    path('agricola-costos',AgricolaCostos.as_view(),name='agricola_costos'),
]

urls_test= [
    path('test',AsyncHomeView.as_view(),name='test'),
    path('endpoint/<str:sp>',ShowAPI.as_view(),name='sp_show_data'),
    path('comercial',NewTheme.as_view(),name='comercial'),
]

urlpatterns = urls_home + urls_finanzas + urls_logistica + urls_comercial + url_produccion + urls_test