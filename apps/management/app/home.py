import pandas as pd
import dash_mantine_components as dmc
from django_plotly_dash import DjangoDash
from dash_iconify import DashIconify
from dash import Dash, dcc, html, Input, Output,State,dash_table,no_update,clientside_callback
from ...resource.constants import EXTERNAL_STYLESHEETS, EXTERNAL_SCRIPTS
from ...resource.layouts.base import layout_base



class DashHome:
    #def __init__(self, ip: str, token :str):
    #    self.ip = ip
    #    self.token = token
    def create_app(self, code: str,data_login = {}):
        app = DjangoDash(
                name = code,
                external_stylesheets = EXTERNAL_STYLESHEETS, 
                external_scripts = EXTERNAL_SCRIPTS,
                #suppress_callback_exceptions=True
        )
        layout_base(app, data_login=data_login,
        children=[
            dmc.Grid([
                    dmc.Col([html.H4("Nisira")]),
                    
                    #dmc.Col([dcc.Loading(dcc.Graph(id="graph",style={"height":350,"position":"absolute"},), type="cube"),]),
                ]),
        ]
        
        )
        return app
        





        
