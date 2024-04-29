from dash import Dash, dcc, html, Input, Output,State,dash_table,no_update
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from ...resource.components.toggle import darkModeToggle
from ...resource.components.menu import menu_avatar
from ...resource.helpers.make_icon import get_icon

def navbar( avatar_user = "", avatar_company = "",name_user = ""):
    return \
    html.Div([
        
            dmc.Header(
                height=60,
                children=[
                    dmc.Group(children=[
                    dmc.MediaQuery([
                        dmc.Button(
                            DashIconify(icon="ci:hamburger-lg", width=24, height=24,color="#c2c7d0"),
                                variant="subtle", 
                                p=1,
                                id='sidebar-button2'
                        ),
                    ], smallerThan="md", styles={'display': 'none'}),
                    dmc.MediaQuery([
                        dmc.Button(
                            DashIconify(icon="ci:hamburger-lg", width=24, height=24,color="#c2c7d0"),
                            variant="subtle", 
                            p=1,
                            id='drawer-demo-button2'
                        ),
                    ], largerThan="md", styles={'display': 'none'}),
                    darkModeToggle(),
                    menu_avatar(avatar_user = avatar_user, name_user = name_user),
                    ],position="apart"),
                                
            ],p='10px'),#, style={"backgroundColor": "#fff"}
                        
           
            
    ])

def sidebar( avatar_company = ""):
    return \
    html.Div([
        dmc.Navbar(
                        p="md",
                        fixed=False,
                        width={"base": 300},
                        hidden=True,
                        hiddenBreakpoint='md',
                        position='right',
                        height='100vh',
                        id='sidebar2',
                        children=[
                            html.Div(
                                [   
                                    dmc.Center(
                                        dmc.Image(
                                            src = avatar_company,
                                            width=115,
                                            height=40,
                                            withPlaceholder=True,
                                            placeholder=[dmc.Loader(color="gray", size="sm")],
                                            
                                        ),
                                    ),
                                    html.P(),
                                    dmc.NavLink(
                                        label="Inicio",
                                        icon=get_icon(icon="bi:house-door-fill"),
                                        href="/",
                                        refresh=True
                                    ),
                                    dmc.NavLink(
                                            label="Dashboard",
                                            opened = False ,
                                            icon=get_icon(icon="tabler:dashboard"),
                                            childrenOffset=28,
                                            children=[
                                                dmc.NavLink(label="Create",href="/dash/create-dashboard",refresh=True),
                                                dmc.NavLink(label="Show",href="/dash/build-dashboard",refresh=True),
                                            
                                            ],
                                    ),
                                    dmc.NavLink(
                                            label="Layouts",
                                            opened = False ,
                                            icon=get_icon(icon="tabler:layout-dashboard"),
                                            childrenOffset=28,
                                            children=[
                                                dmc.NavLink(label="Create",href="/hlayout/create-layout",refresh=True),
                                                dmc.NavLink(label="Show",href="/hlayout/show-layout",refresh=True),
                                            
                                            ],
                                    ),
                                    dmc.NavLink(
                                            label="Data",
                                            opened = False ,
                                            icon=get_icon(icon="tabler:database"),
                                            
                                            childrenOffset=28,
                                            children=[
                                                dmc.NavLink(label="Configuración",href="/hdata/explorer-data",refresh=True),
                                                
                                            
                                            ],
                                    ),
                                    dmc.NavLink(
                                            label="Old Apps",
                                            opened = False ,
                                            icon=get_icon(icon="tabler:apps"),
                                            
                                            childrenOffset=28,
                                            children=[
                                                dmc.NavLink(label="Balance General",href="/app/balance-general",refresh=True),
                                                dmc.NavLink(label="Activos & Pasivos",href="/app/balance-ap",refresh=True),
                                                dmc.NavLink(label="Análisis Activos",href="/app/analisis-activo",refresh=True),
                                                dmc.NavLink(label="Análisis Pasivos",href="/app/analisis-pasivo",refresh=True),
                                            ],
                                    ),
                                ],
                                style={'white-space': 'nowrap'},
                            )],style={'overflow':'hidden', 'transition': 'width 0.3s ease-in-out', }#'background-color':'#343a40'
        ), 
    ])
    
    
def sidebar_low():
    return \
    html.Div([
        dmc.Drawer(
            title="",
            id="drawer-simple2",
            padding="md",
            zIndex=10000,
            size=300,       
            overlayOpacity=0.1,
            children=[
                                html.Div(
                                    [
                                        dmc.NavLink(
                                            label="Inicio",
                                            icon=get_icon(icon="bi:house-door-fill"),
                                        ),
                                        dmc.NavLink(
                                            label="Test",
                                            icon=get_icon(icon="tabler:gauge"),
                                            childrenOffset=28,
                                            children=[
                                                dmc.NavLink(label="First child link"),
                                                dmc.NavLink(label="Second child link"),
                                                dmc.NavLink(
                                                    label="Nested parent link",
                                                    childrenOffset=28,
                                                    children=[
                                                        dmc.NavLink(label="First child link"),
                                                        dmc.NavLink(label="Second child link"),
                                                        dmc.NavLink(label="Third child link"),
                                                    ],
                                                ),
                                            ],
                                        ),
                                        
                                    ],
                                    style={'white-space': 'nowrap'},
                                )
            ], style={'background-color':''}, styles={'drawer':{'background-color':'#343a40'}}),
    ])