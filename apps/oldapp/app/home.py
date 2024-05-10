from django_plotly_dash import DjangoDash
from backend.connector import APIConnector
from ...resource.constants import EXTERNAL_STYLESHEETS, EXTERNAL_SCRIPTS
import dash_mantine_components as dmc
from ...resource.components.toggle import darkModeToggleDash
from ...resource.components.cards import card_id
from ...resource.layouts.base import *
from ...resource.helpers.make_grid import *
from ...oldapp.utils import *

class DashHomeOld:
    #def __init__(self, ip: str, token :str):#, data_login: dict
    #    self.ip = ip
    #    self.token = token
    def index(self, code: str):
        app = DjangoDash(
                name = code,
                external_stylesheets = EXTERNAL_STYLESHEETS, 
                external_scripts = EXTERNAL_SCRIPTS,
        )
        app.layout =  \
        Content([
            Grid([
                Col([
                    darkModeToggleDash()
                ]),
                Col([
                    dmc.Text("home",align="center")
                ])
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
        Output('themeHolder','theme'),Input('themeSwitch','checked'))
        return app