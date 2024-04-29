import dash_mantine_components as dmc
from dash_iconify import DashIconify

def stats_data():
    return dmc.Card(
            
            children=[
            dmc.Group([
                #dmc.Divider(orientation="vertical"),
                dmc.Grid(
                    children=[
                        dmc.Col(dmc.Text('N° Columnas',align='center',style={"fontSize": 12}), span=12,p=0),
                        dmc.Col(dmc.Text(id= 'stat-cols' , weight=700,children=[],align='center',style={"fontSize": 18}), span=12,p=0),
                        
                    ],
                    gutter="xs",id='grid-1',
                ),
                
                #dmc.Divider(orientation="vertical"),
                dmc.Grid(
                    children=[
                        dmc.Col(dmc.Text('N° Filas',align='center',style={"fontSize": 12}), span=12,p=0),
                        dmc.Col(dmc.Text(id= 'stat-rows' , weight=700,children=[],align='center',style={"fontSize": 18}), span=12,p=0),
                        
                    ],
                    gutter="xs",id='grid-2',
                ),
                #
                dmc.Grid(
                    children=[
                        dmc.Col(dmc.Text('N° Var. Categ',align='center',style={"fontSize": 12}), span=12,p=0),
                        dmc.Col(dmc.Text(id= 'stat-cate' , weight=700,children=[],align='center',style={"fontSize": 18}), span=12,p=0),
                        
                    ],
                    gutter="xs",id='grid-2',
                ),
                #
                #dmc.Divider(orientation="vertical"),
                dmc.Grid(
                    children=[
                        dmc.Col(dmc.Text('N° Var. Num',align='center',style={"fontSize": 12}), span=12,p=0),
                        dmc.Col(dmc.Text(id= 'stat-num' , weight=700,children=[],align='center',style={"fontSize": 18}), span=12,p=0),
                        
                    ],
                    gutter="xs",id='grid-3',
                ),

                #dmc.Divider(orientation="vertical"),
                dmc.Grid(
                    children=[
                        dmc.Col(dmc.Text('N° Var. Fecha',align='center',style={"fontSize": 12}), span=12,p=0),
                        dmc.Col(dmc.Text(id= 'stat-fecha' , weight=700,children=[],align='center',style={"fontSize": 18}), span=12,p=0),
                        
                    ],
                    gutter="xs",id='grid-4',
                ),

            ], sx={'align-items': 'baseline'},grow=True,id='group-1'),#, spacing='0.5rem'
            dmc.ActionIcon(
                DashIconify(icon=f"feather:{"download"}"), 
                id='btn-download',
                n_clicks=0,
                mb=10,
                style = {'position': 'absolute','top': '4px','right': '4px','z-index': '99'},
                p=0
            ),
           
           

            ],
            withBorder=True,
            #shadow='xl',
            #radius='md',
            m=10
        )
    
