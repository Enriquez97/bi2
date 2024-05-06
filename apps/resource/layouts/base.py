import dash_mantine_components as dmc
from ...resource.components.partials import navbar,sidebar,sidebar_low
from dash import Dash, dcc, html,dash_table, Output,State,Input

def layout_base2(data_login = {}, children = []):
    return \
        dmc.NotificationsProvider(
            dmc.MantineProvider(
                id="themeHolder",
                inherit=True,
                withGlobalStyles=True,
                withNormalizeCSS=True,
                children=[
                    dmc.Container([
                        
                        sidebar(avatar_company = data_login["avatar_company"]),
                        sidebar_low(),
                        
                        dmc.Container([
                        
                            navbar(avatar_user = data_login["avatar_profile"], name_user = data_login["name_user"]),
                            dmc.Container(children = children,fluid=True),
                        ],
                            id="page-container2",
                            p=0,
                            fluid=True,
                            style={ 'width':'100%', 'margin':'0'}#'background-color':'#f4f6f9',
                        ),
                        
                    ], size='100%', p=0,m=0, style={'display':'flex'})
                ]
            )
        )
        
def layout_base(app,data_login = {}, children = []):
    app.layout = \
        dmc.NotificationsProvider(
            dmc.MantineProvider(
                id="themeHolder",
                inherit=True,
                withGlobalStyles=True,
                withNormalizeCSS=True,
                children=[
                    dmc.Container([
                        
                        sidebar(avatar_company = data_login["avatar_company"]),
                        sidebar_low(),
                        
                        dmc.Container([
                        
                            navbar(avatar_user = data_login["avatar_profile"], name_user = data_login["name_user"]),
                            dmc.Container(children = children,fluid=True),
                        ],
                            id="page-container2",
                            p=0,
                            fluid=True,
                            style={ 'width':'100%', 'margin':'0'}#'background-color':'#f4f6f9',
                        ),
                        
                    ], size='100%', p=0,m=0, style={'display':'flex'})
                ]
            )
        )
    app.clientside_callback(
            """
            function(n_clicks) {
                if (n_clicks > 0) {
                    return true;
                } else {
                    return '';
                }
            }
            """
            ,
            Output("drawer-simple2", "opened"),
            [Input("drawer-demo-button2", "n_clicks")]
    )
    app.clientside_callback(
            """
            function(n_clicks, width) {
                const current_width = parseInt(width.base);
                if (n_clicks > 0 && current_width === 300) {
                    return {base: 70};
                } else {
                    return {base: 300};
                }
            }
            """,
            Output("sidebar2", "width"),
            [Input("sidebar-button2", "n_clicks"),],
            [State('sidebar2','width')]
        )
        
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
    Output('themeHolder','theme'),
    [Input('themeSwitch','checked'),]
            
    )
    return app

def Content(child = []):
    return \
    dmc.MantineProvider(
        id="themeHolder",
        inherit=True,
        withGlobalStyles=True,
        withNormalizeCSS=True,
        children=[
            dmc.NotificationsProvider(dmc.Container(child,fluid=True))
                    
        ]
    )
        