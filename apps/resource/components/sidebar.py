import dash_mantine_components as dmc
from dash import html, Input, Output, dcc, State
from dash_iconify import DashIconify
from ...resource.helpers.make_icon import get_icon
from ...resource.components.menu import menu_avatar
from ...resource.components.toggle import darkModeToggle

def navsidebar( avatar_user = "", avatar_company = "",name_user = ""):
    return \
    dmc.Container([
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
                                ),
                                dmc.NavLink(
                                        label="Test",
                                        opened = True ,
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
                        )],style={'overflow':'hidden', 'transition': 'width 0.3s ease-in-out', }#'background-color':'#343a40'
                    ),      
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
                dmc.Container([
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
                    html.P(),
                    
                    ],
                    id="page-container2",
                    p=0,
                    fluid=True,
                    style={ 'width':'100%', 'margin':'0'}#'background-color':'#f4f6f9',
            ),
            
        ], size='100%', p=0,m=0, style={'display':'flex'})#
        
    
"""
dmc.NavLink(
                                        opened=False,
                                        label="With right section",
                                        icon=get_icon(icon="tabler:gauge"),
                                        rightSection=get_icon(icon="tabler-chevron-right"),
                                    ),
                                    dmc.NavLink(
                                        label="Disabled",
                                        icon=get_icon(icon="tabler:circle-off"),
                                        disabled=True,
                                    ),
                                    dmc.NavLink(
                                        label="With description",
                                        description="Additional information",
                                        icon=dmc.Badge(
                                            "3", size="xs", variant="filled", color="red", w=16, h=16, p=0
                                        ),
                                        style={
                                            'body':{'overflow':'hidden'}
                                        }
                                    ),
                                    dmc.NavLink(
                                        label="Active subtle",
                                        icon=get_icon(icon="tabler:activity"),
                                        rightSection=get_icon(icon="tabler-chevron-right"),
                                        variant="subtle",
                                        active=True,
                                    ),
"""