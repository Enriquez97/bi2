import dash_mantine_components as dmc
import pandas as pd
from dash import Input, Output,dcc,html,no_update, State
from django_plotly_dash import DjangoDash
from ...resource.constants import EXTERNAL_STYLESHEETS, EXTERNAL_SCRIPTS
from ...resource.layouts.base import layout_base


class DashBuild:
    #def __init__(self, ip: str, token :str):
    #    self.ip = ip
    #    self.token = token  
    def create_app(self, code: str, data_login = {}, dash_create = None ):
        app = DjangoDash(
                name = code,
                external_stylesheets = EXTERNAL_STYLESHEETS, 
                external_scripts = EXTERNAL_SCRIPTS,
        )
        
        layout_base(
            app,
            data_login = data_login, 
            children = [
            
            dash_create
            
            ]#
        )

        return app