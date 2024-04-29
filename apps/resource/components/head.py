from dash import Dash, dcc, html, Input, Output,State,dash_table,no_update
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from ...resource.components.toggle import darkModeToggle
from ...resource.components.menu import menu_avatar

def head_dashboard():
    return \
    html.Div([
        
    ])
    
def head_global_dash(name_user = "", imagen = ""):
        
    return  dmc.Grid(
            [
                
                dmc.Col(
                    [
                        dmc.Group(
                            [
                                dmc.ActionIcon(
                                    [
                                        DashIconify(icon='bx:data', color='#C8C8C8', width=25,)
                                    ],
                                    variant='transparent',
                                    id='about-data-source'
                                ),
                                dmc.Badge(
                                    name_user,
                                    leftSection=dmc.Avatar(
                                        src=imagen,
                                        size=24,
                                        radius="xl",
                                        mr=5,
                                    ),
                                    sx={"paddingLeft": 0},
                                    size="lg",
                                    radius="xl",
                                    color="teal",
                                )
                                
                            ],
                            spacing='xl',
                            position='right'
                        )
                    ],
                    offsetMd=1,
                    md=10,
                    span=11
                ),
                dmc.Col(children=[
                    darkModeToggle()
                ],span=1),
            ],
            mt='md',
            mb=10
        )
    
def head_global_dash_2(name_user = "Edwardo Enriquez", imagen = ""):
    


        
    return  dmc.Grid(
            [   
                
                dmc.Col(
                    [
                      dmc.Menu(
                        [
                            dmc.MenuTarget([
                                dmc.Avatar(
                                        src = imagen,
                                        size=34,
                                        radius="xl",
                                        mr=5,
                                        
                                    ),
                                
                                ]
                            ),
                            dmc.MenuDropdown(
                                [
                                    dmc.MenuLabel("Application"),
                                    dmc.MenuItem("Settings", icon=DashIconify(icon="tabler:settings")),
                                    dmc.MenuItem("Messages", icon=DashIconify(icon="tabler:message")),
                                    dmc.MenuItem("Gallery", icon=DashIconify(icon="tabler:photo")),
                                    dmc.MenuItem("Search", icon=DashIconify(icon="tabler:search")),
                                    dmc.MenuDivider(),
                                    dmc.MenuLabel("Danger Zone"),
                                    dmc.MenuItem(
                                        "Transfer my data",
                                        icon=DashIconify(icon="tabler:arrows-left-right"),
                                    ),
                                    dmc.MenuItem(
                                        "Delete my account",
                                        icon=DashIconify(icon="tabler:trash"),
                                        color="red",
                                    ),
                                ]
                            ),
                        ],
                        trigger="hover",
                    )  
                    ],
                    
                    md=10,
                    span=1
                ),
                dmc.Col(children=[
                    dmc.Text("Edwardo Enriquez", weight=600),
                    
                ],span=2),
                dmc.Col(children=[
                    darkModeToggle()
                ],span=1),
                
            ],
            #mt='md',
            m=0
        )




def head_dashboard_select(value_select = ""):
    if value_select == "only_title":
        return dmc.Grid(
            children=[
                dmc.Col(html.Div("span=auto", ), span="auto"),
                dmc.Col(dmc.Title("garbage test", align="center",order=2), span=6),
                dmc.Col(html.Div("span=auto",), span="auto"),
            ],
            gutter="xl",
        )

    #elif value_select == "":
    else:
        return dmc.Grid(
            children=[
                dmc.Col(dmc.Title("garbage test", align="center",order=2), span=3),
                dmc.Col(
                    html.Div([  
                        dmc.Select(
                        label="Select framework",
                        placeholder="Select one",
                        id="",
                        value="ng",
                        data=[
                            {"value": "react", "label": "React"},
                            {"value": "ng", "label": "Angular"},
                            {"value": "svelte", "label": "Svelte"},
                            {"value": "vue", "label": "Vue"},
                        ],
                        
                        )
                    ]) 
                , span=3),
                dmc.Col(
                html.Div([     
                    dmc.Select(
                    label="Select framework",
                    placeholder="Select one",
                    id="select1",
                    value="ng",
                    data=[
                        {"value": "react", "label": "React"},
                        {"value": "ng", "label": "Angular"},
                        {"value": "svelte", "label": "Svelte"},
                        {"value": "vue", "label": "Vue"},
                    ],
                    
                    )
                ]) 
                , span=3),
                
            ],
            gutter="xl",
        )

