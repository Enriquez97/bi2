import dash_mantine_components as dmc
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output,State,dash_table,no_update,clientside_callback
from dash_iconify import DashIconify
from .figure import create_empty

def card_show_layout(fig = None, name_kpi = None):
    return \
    dmc.Card(
        children=[
            dmc.CardSection(
                dcc.Graph(figure=go.Figure(fig),style={"height":350})
            ),
            dmc.Group(
                [
                    dmc.Text(name_kpi[:-5], weight=500),
                    #dmc.Badge("On Sale", color="red", variant="light"),
                ],
                position="apart",
                mt="md",
                mb="xs",
            ),
        
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
    )

def card_graph(height = 350,title ='',fig_ = None):
    return \
    dmc.Card(
        children=[
            dmc.CardSection(
                children=[  
                    
                    dmc.ActionIcon(
                                DashIconify(icon=f"feather:{"maximize"}"), 
                                color="blue", 
                                variant="default",
                                #id=id,
                                n_clicks=0,
                                mb=10,
                                style={'position': 'absolute','z-index': '99'},#'top': '4px','right': '4px',
                    ),    
                    dmc.Text(children =[dmc.Center(children=[DashIconify(icon="icon", width=20,className="me-1"),title])] , weight=500),
                ],
                withBorder=True,
                inheritPadding=True,
                p = 2,
            ),
            #html.Div([
            #    dmc.LoadingOverlay(
            #        children = [
                        dmc.CardSection(children = [
                            
                            dcc.Graph(figure= fig_,style={"height": height})
                            
                        ],p=0,style={'backgroundColor':'white','height':height,}),
        #            ],
        #            loaderProps={"variant": type, "color": "#01414b", "size": "xl"},
        #            loader=dmc.Image(
        #                src="https://i.imgur.com/KIj15up.gif", alt="", caption="", width=70,height=70#
        #            )  
        #        )     
            
        #    ]),
        ],
        withBorder = True,
        
        radius = 'xs',
        style={"position": "static"},#,'height':height
        p=0
    )



def card_id(height = 350,title ='',id_ = None):
    return \
    dmc.Card(
        children=[
            dmc.CardSection(
                children=[  
                    
                    dmc.ActionIcon(
                                DashIconify(icon=f"feather:{"maximize"}"), 
                                color="blue", 
                                variant="default",
                                id=f"{id}-max",
                                n_clicks=0,
                                mb=10,
                                style={'position': 'absolute','z-index': '99'},#'top': '4px','right': '4px',
                    ),    
                    dmc.Text(children =[dmc.Center(children=[DashIconify(icon="icon", width=20,className="me-1"),title])] , weight=500),
                ],
                withBorder=True,
                inheritPadding=True,
                p = 2,
            ),
            #html.Div([
            #    dmc.LoadingOverlay(
            #        children = [
                        dmc.CardSection(children = [
                            
                            dcc.Graph(id = id_,style={"height": height},figure=create_empty(text="Esperando Datos"))
                            
                        ],p=0,style={'backgroundColor':'white','height':height,}),
        #            ],
        #            loaderProps={"variant": type, "color": "#01414b", "size": "xl"},
        #            loader=dmc.Image(
        #                src="https://i.imgur.com/KIj15up.gif", alt="", caption="", width=70,height=70#
        #            )  
        #        )     
            
        #    ]),
        ],
        withBorder = True,
        
        radius = 'md',
        style={"position": "static"},#,'height':height
        p=0
    )
