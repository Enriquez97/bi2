from django_plotly_dash import DjangoDash
from ...resource.constants import EXTERNAL_STYLESHEETS, EXTERNAL_SCRIPTS
from ...resource.layouts.base import layout_base
import dash_mantine_components as dmc

class DashFinanzas:
    def __init__(self, ip: str, token :str, data_login: dict):
        self.ip = ip
        self.token = token
        self.user_login = data_login
    def finanzas_bg(self, code: str):
        app = DjangoDash(
                name = code,
                external_stylesheets = EXTERNAL_STYLESHEETS, 
                external_scripts = EXTERNAL_SCRIPTS,
        )
        layout_base(
            app,
            data_login = self.user_login, 
            children = [
                dmc.Text("BALANCE DE COMPROBACIÓN")
            ]
        )
        return app
    
    def finanzas_balance_ap(self, code: str):
        app = DjangoDash(
                name = code,
                external_stylesheets = EXTERNAL_STYLESHEETS, 
                external_scripts = EXTERNAL_SCRIPTS,
        )
        layout_base(
            app,
            data_login = self.user_login, 
            children = [
                dmc.Text("BALANCE ACTIVO & PASIVO")
            ]
        )
        return app
    
    def finanzas_analisis_activo(self, code: str):
        app = DjangoDash(
                name = code,
                external_stylesheets = EXTERNAL_STYLESHEETS, 
                external_scripts = EXTERNAL_SCRIPTS,
        )
        layout_base(
            app,
            data_login = self.user_login, 
            children = [
                dmc.Text("ANÁLISIS DE ACTIVOS")
            ]
        )
        return app
    
    def finanzas_analisis_pasivo(self, code: str):
        app = DjangoDash(
                name = code,
                external_stylesheets = EXTERNAL_STYLESHEETS, 
                external_scripts = EXTERNAL_SCRIPTS,
        )
        layout_base(
            app,
            data_login = self.user_login, 
            children = [
                dmc.Text("ANÁLISIS DE PASIVOS")
            ]
        )
        return app