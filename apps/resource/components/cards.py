import dash_mantine_components as dmc
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output,State,dash_table,no_update,clientside_callback
from dash_iconify import DashIconify
from .figure import graph_empty,create_empty
import dash_ag_grid as dag

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



def card_id(height = 350,title ='',id_ = None, graph = True):
    if graph == True:
        block = dcc.Graph(id = id_,style={"height": height},figure=create_empty(text="Esperando Datos"))
    else:
        block = html.Div(children=[
                dag.AgGrid(
                        id= id_,
                        defaultColDef = {
                            "resizable": True,
                            "initialWidth": 160,
                            "wrapHeaderText": True,
                            "autoHeaderHeight": True,
                            "minWidth":160,
                            "sortable": True, 
                            "filter": True
                        },
                        #className="ag-theme-alpine headers1",
                        columnSize="sizeToFit",
                        style={'font-size': '13px','height':height-10},
            )]) 
    return \
    dmc.Card(
        children=[
            dmc.CardSection(
                children=[  

                    dmc.ActionIcon(
                                DashIconify(icon=f"feather:{"maximize"}"), 
                                color="blue", 
                                variant="default",
                                id=f"maxi_{id_}",
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
            dmc.CardSection(children = [
                dmc.LoadingOverlay([
                     block
                ]),
               
            ],p=0,style={'backgroundColor':'white','height':height,}),
        ],
        withBorder = True,
        radius = 'md',
        style={"position": "static"},#,'height':height
        p=0
    )

def card_segment(height = 350,id_ = None, id_segmented = '',value = '',data = []):
    return \
    dmc.Card(
        children=[
            dmc.SegmentedControl(
                id=id_segmented,
                value=value,
                data=data,
                fullWidth=True,
                #color='rgb(34, 184, 207)',
                size='xs'
            ),   
            dmc.ActionIcon(
                DashIconify(icon=f"feather:{"maximize"}"), 
                    color="blue", 
                    variant="default",
                    id=f"maxi_{id_}",
                    n_clicks=0,
                    mb=10,
                    style={'position': 'absolute','z-index': '99'},
            ),  
            dmc.LoadingOverlay(
            loaderProps={"variant": "bars", "color": "#01414b", "size": "xl"},
            loader=dmc.Image(src="https://i.imgur.com/KIj15up.gif", alt="", caption="", width=70,height=70),
            children=[
                dcc.Graph(id = id_,style={"height": height},figure=graph_empty(text=''))
            ]
        ),
            
        ],
        withBorder = True,
        radius = 'md',
        style={"position": "static"},#,'height':height
        p=0
    )

def card_stack(id_value = '',text = 'cpm'):
  
    return dmc.Card(
            id='card',
            children=[
            dmc.Group([
                #dmc.Divider(orientation="vertical"),
                dmc.Grid(
                    children=[
                        dmc.Col(dmc.Text('CPM',align='center',style={"fontSize": 12}), span=12,p=0),
                        dmc.Col(dmc.Text(id= 'card-cpm' , weight=700,children=[],align='center',style={"fontSize": 18}), span=12,p=0),
                        
                    ],
                    gutter="xs",id='grid-1',
                ),
                
                #dmc.Divider(orientation="vertical"),
                dmc.Grid(
                    children=[
                        dmc.Col(dmc.Text('INV VAL',align='center',style={"fontSize": 12}), span=12,p=0),
                        dmc.Col(dmc.Text(id= 'card-invval' , weight=700,children=[],align='center',style={"fontSize": 18}), span=12,p=0),
                        
                    ],
                    gutter="xs",id='grid-2',
                ),
                #
                dmc.Grid(
                    children=[
                        dmc.Col(dmc.Text('TOTAL STOCK', align='center',style={"fontSize": 12}), span=12,p=0),
                        dmc.Col(dmc.Text(id= 'card-total-stock' , weight=700,children=[],align='center',style={"fontSize": 18}), span=12,p=0),
                        
                    ],
                    gutter="xs",id='grid-2',
                ),
                #
                #dmc.Divider(orientation="vertical"),
                dmc.Grid(
                    children=[
                        dmc.Col(dmc.Text('TI STOCK', align='center',style={"fontSize": 12}), span=12,p=0),
                        dmc.Col(dmc.Text(id= 'card-stock' , weight=700,children=[],align='center',style={"fontSize": 18}), span=12,p=0),
                        
                    ],
                    gutter="xs",id='grid-3',
                ),

                #dmc.Divider(orientation="vertical"),
                dmc.Grid(
                    children=[
                        dmc.Col(dmc.Text('TI CON', align='center',style={"fontSize": 12}), span=12,p=0),
                        dmc.Col(dmc.Text(id= 'card-consumo' , weight=700,children=[],align='center',style={"fontSize": 18}), span=12,p=0),
                        
                    ],
                    gutter="xs",id='grid-4',
                ),
               
                
                #dmc.Text('18%', size='xs', color='rgb(9, 146, 104)'),
                #dmc.Text(html.I(className='fas fa-arrow-up fa-fw fa-xs'), color='rgb(9, 146, 104)')
            ], sx={'align-items': 'baseline'},grow=True,id='group-1'),#, spacing='0.5rem'
            
           
           

            ],
            withBorder=True,
            shadow='xl',
            radius='md',
        )
    
def cardGraph(id = ""):
    return html.Div([
        dmc.LoadingOverlay(
            loaderProps={"variant": "bars", "color": "#01414b", "size": "xl"},
            loader=dmc.Image(src="https://i.imgur.com/KIj15up.gif", alt="", caption="", width=70,height=70),
            children=[
                dmc.Card(
                    children=[
                        dmc.ActionIcon(
                            DashIconify(icon=f"feather:{"maximize"}"), 
                            color="blue", 
                            variant="default",
                            id=f"maxi_{id}",
                            n_clicks=0,
                            mb=10,
                            style={'position': 'absolute','top': '4px','right': '4px','z-index': '99'},
                        ),
                        dcc.Graph(id=id, figure=graph_empty(text=''))# figure=graph_empty
                    ],
                    withBorder=True,
                    shadow="sm",
                    radius="md",
                    p=0
                ),
            ]
        ),
        
    ])