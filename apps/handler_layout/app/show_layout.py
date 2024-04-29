import dash_mantine_components as dmc
import pandas as pd
from django_plotly_dash import DjangoDash
from ...resource.constants import EXTERNAL_STYLESHEETS, EXTERNAL_SCRIPTS
from dash import dash, dcc, html, Input, Output,State,dash_table,no_update,clientside_callback
from ...resource.components.head import head_global_dash
from ...resource.components.cards import *
from ...resource.components.accordion import * 
from ... resource.components.sidebar import *
from ...resource.layouts.base import layout_base
#####

####



class DashShowLayout:
    #def __init__(self, ip: str, token :str):
    #    self.ip = ip
    #    self.token = token
    def create_app(self, code: str, kpi_df = None):
        
        
        #kpi_layout = KPI.objects.all()
        #kpi_layout_list = [[fila.name,fila.figure] for fila in kpi_layout]
        #print(kpi_layout)
        app = DjangoDash(
                name = code,
                external_stylesheets = EXTERNAL_STYLESHEETS, 
                external_scripts = EXTERNAL_SCRIPTS,
                #suppress_callback_exceptions=True
        )
        data_login = {}
        data_login["avatar_company"] = ""
        data_login["avatar_profile"] = ""
        data_login["avatar_company"] = ""
        data_login["name_user"] = ""
        layout_base(
            app,
            data_login = data_login, 
            children = [
                dmc.Grid(children=[dmc.Col(card_show_layout(fig =eval(f),name_kpi= n), span=4)for f,n in zip(kpi_df['figure'].values,kpi_df['name_kpi'].values)],
                    gutter="xs"
                ),
            ]
        
        )

