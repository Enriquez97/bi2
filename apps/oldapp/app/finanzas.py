from django_plotly_dash import DjangoDash
from ...resource.constants import EXTERNAL_STYLESHEETS, EXTERNAL_SCRIPTS
from ...resource.layouts.base import layout_base
import dash_mantine_components as dmc
from ...resource.helpers.make_grid import *
from ...resource.layouts.base import *
from ...resource.components.toggle import darkModeToggleDash

class DashFinanzas:
    def __init__(self, ip: str, token :str):#, data_login: dict
        self.ip = ip
        self.token = token
        #self.user_login = data_login
    def finanzas_bg(self, code: str):
        app = DjangoDash(
                name = code,
                external_stylesheets = EXTERNAL_STYLESHEETS, 
                external_scripts = EXTERNAL_SCRIPTS,
        )
        app.layout =  \
        Content([
            Grid([
                Col([
                    dmc.Title("Balance General")
                ],size= 3),
                Col([
                    dmc.Select(
                        label="Formato",
                        placeholder="Todos",
                        id="select-format",
                        value = None,
                        data= [],
                        clearable=False
                    )
                ],size= 2),
                Col([
                    dmc.Select(
                        label="Año",
                        placeholder="Todos",
                        id="select-year",
                        value = None,
                        data= [],
                        clearable=True
                    )
                ],size= 2),
                
                Col([
                    dmc.Select(
                        label="Trimestre",
                        placeholder="Todos",
                        id="select-quarter",
                        value = None,
                        data= [],
                        clearable=False
                    )
                ],size= 2),
                Col([
                    dmc.Select(
                        label="Mes",
                        placeholder="Todos",
                        id="select-month",
                        value = None,
                        data= [],
                        clearable=False
                    )
                ],size= 1),
                Col([
                    dmc.Select(
                        label="Moneda",
                        #placeholder="Todos",
                        id="select-coin",
                        value = "USD",
                        data= ["USD","PEN"],
                        clearable=False
                    )
                ],size= 1),
                Col([
                    darkModeToggleDash()
                ],size= 1)
            ])
            
            
        ])
        app.clientside_callback(
        """
        function(checked) {
                if (checked) {
                    return {"colorScheme": "light"};
                } else {
                    return {"colorScheme": "dark"};
                }
        }
        """,
        Output('themeHolder','theme'),
        [Input('themeSwitch','checked'),]    
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