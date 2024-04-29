from django.contrib import admin
from django.urls import path
from django.urls import path, include
from drf_yasg import openapi #new foe swagger
from drf_yasg.views import get_schema_view as swagger_get_schema_view #new foe swagger


schema_view = swagger_get_schema_view(
    openapi.Info(
        title="Your Project APIs",
        default_version='1.0.0',
        description="API documentation of App",
    ),
    public=True,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/schema/', schema_view.with_ui('swagger', cache_timeout=0), name="swagger-schema"),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('dash/',include('apps.bi.urls')),
    path('hdata/',include('apps.handler_data.urls')),
    path('hlayout/',include('apps.handler_layout.urls')),
    path('',include('apps.management.urls')),
    
    path('app/',include('apps.oldapp.urls')),
]
