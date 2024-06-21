from django_plotly_dash import DjangoDash
from backend.connector import APIConnector
from ...resource.constants import EXTERNAL_STYLESHEETS, EXTERNAL_SCRIPTS
import dash_mantine_components as dmc
from ...resource.components.toggle import darkModeToggleDash
from ...resource.components.cards import card_id
from ...resource.layouts.base import *
from ...resource.helpers.make_grid import *
from ...oldapp.utils import *
from dash_iconify import DashIconify
from ...management.models import Company

class DashHomeOld:
    #def __init__(self, ip: str, token :str):#, data_login: dict
    #    self.ip = ip
    #    self.token = token
    def index(self, code: str, user_index = {}):
        app = DjangoDash(
                name = code,
                external_stylesheets = EXTERNAL_STYLESHEETS, 
                external_scripts = EXTERNAL_SCRIPTS,
        )
        def grid_left(validate_1 : bool, validate_2 : bool):
            if validate_1 == True and validate_2 == True:
                return dmc.Stack(
                            spacing="xs",
                            children=[
                                dmc.Title("Admin test")
                            ],
                        )
            else:
                return dmc.Stack(
                            spacing="xs",
                            children=[
                                dmc.Skeleton(height=50, circle=True),
                                dmc.Skeleton(height=8),
                                dmc.Skeleton(height=8),
                                dmc.Skeleton(height=8, width="70%"),
                            ],
                        )
            
        app.layout =  \
        Content([
            Grid([
                
                Col([
                    dmc.Title("",align="left")
                ],size=11),
                Col([
                    darkModeToggleDash()
                ],size=1),
                
                Col([
                    dmc.Card([
                       
                           Grid([
                           Col([ dmc.Center([dmc.Avatar(src=user_index["avatar_profile"],radius="xl",size=130)])]), 
                           Col([dmc.Center([dmc.Text(children=[user_index["name_user"]],size=18,weight=700,align="center")])]), 
                           Col([dmc.Center([dmc.Text(children=[user_index["empresa"]],size=18,weight=700)])]), 
                           Col([dmc.Center([dmc.Text(children=[user_index["rol"]],size=16)])]),
                           Col([dmc.Center([dmc.Text(children=[user_index["rubro"]],size=16)])]),  
                           Col([dmc.Center([dmc.Badge("Servicios On", variant="outline",color="blue")if user_index["status_service"] == True else dmc.Badge("Servicios Off", variant="outline",color="red")])]), 
                        ]) 
                        
                        
                        
                    ],
                        withBorder=True,
                        shadow="sm",
                        radius="md",
                        style={"height": 400}
                    )
                ],size=4),
                Col([
                    dmc.Card([
                        grid_left(user_index["is_superuser"],user_index["is_staff"])
                    ],
                        withBorder=True,
                        shadow="sm",
                        radius="md",
                        style={"height": 400}
                    )
                ],size=8),
                Col([
                    dmc.Card([
                        dmc.List(
                        icon=dmc.ThemeIcon(
                            DashIconify(icon="radix-icons:check-circled", width=16),
                            radius="xl",
                            color="teal",
                            size=24,
                        ),
                        size="sm",
                        spacing="sm",
                        children=[
                            dmc.ListItem("Rework Dashboards"),
                            dmc.ListItem(
                                dmc.Text(["Update components"])
                            ),
                            dmc.ListItem(
                                dmc.Text(["Add Darkmode"])
                            ),
                            dmc.ListItem(
                                "Versión 2.0",
                                icon=dmc.ThemeIcon(
                                    DashIconify(icon="radix-icons:pie-chart", width=16),
                                    radius="xl",
                                    color="blue",
                                    size=24,
                                ),
                            ),
                        ],
                    )
                    ],
                        withBorder=True,
                        shadow="sm",
                        radius="md",
                        style={"height": 200}
                    )
                ],size=12),
            ])
        ],fluid=False)
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