import dash_mantine_components as dmc
from dash import Input, Output,dcc,html,no_update, State
import plotly.graph_objs as go
import pandas as pd
from django_plotly_dash import DjangoDash
from ...resource.constants import EXTERNAL_STYLESHEETS, EXTERNAL_SCRIPTS
from ...resource.layouts.base import layout_base
from ...resource.components.cards import card_graph
from ...handler_layout.models import KPI
from dash_iconify import DashIconify
from ..model.create import createDashboard

class DashCreate:
    #def __init__(self, ip: str, token :str):
    #    self.ip = ip
    #    self.token = token  
    def create_app(self, code: str, data_login = {}, model_sp = None):
        app = DjangoDash(
                name = code,
                external_stylesheets = EXTERNAL_STYLESHEETS, 
                external_scripts = EXTERNAL_SCRIPTS,
        )
        sp_dict = {fila.sp_name:fila.config.config for fila in model_sp} 
        sp_list = list(sp_dict.keys())
        kpi= KPI.objects.all()
        kpi_df = pd.DataFrame(data = [[fila.sp.sp_name, eval(fila.figure),fila.name] for fila in kpi], columns=["sp_name","figure","name"])
        layout_base(
            app,
            data_login = data_login, 
            children = [
                dmc.Accordion(
                    children=[
                        dmc.AccordionItem(
                            [
                                dmc.AccordionControl("Create"),
                                dmc.AccordionPanel(
                                   [
                                       dmc.Divider(label="Header Dashboard", labelPosition="center"),
                                       dmc.Grid(
                                            children=[
                                                dmc.Col([
                                                    dmc.Select(
                                                        label="SP Dashboard",
                                                        placeholder="Select one",
                                                        id="select-head",
                                                        value=None,
                                                        data= sp_list,
                                                        
                                                    ),
                                                ], span=2),
                                                dmc.Col([
                                                    dmc.TextInput(id ="title-dash" ,label="Título Dashboard", required = True, value= "Dash"),
                                                ], span=3),
                                                dmc.Col([
                                                    dmc.MultiSelect(
                                                        label="Filtros",
                                                        placeholder="Seleccione Campos",
                                                        id="filters",
                                                        #value=["ng", "vue"],
                                                        
                                                    ),
                                                ], span=5),
                                                dmc.Col([
                                                    dmc.Checkbox(
                                                        id="checkbox-state-title",
                                                        checked=False,
                                                        label=dmc.Text(
                                                            ["Título solo "]
                                                        ),
                                                        mt=30,
                                                    )
                                                ], span=2),
                                            ],
                                            gutter="xl",
                                        ),
                                        dmc.Divider(label="Body Dashboard", labelPosition="center"),
                                        dmc.Grid(
                                            children=[
                                                dmc.Col([
                                                   
                                                    dmc.MultiSelect(
                                                        label="Kpi Name",
                                                        placeholder="Seleccione Campos",
                                                        id="kpi-figure",
                                                        
                                                        #value=["ng", "vue"],
                                                        
                                                    ),
                                                ], span=6),
                                            ],
                                        gutter="xl",
                                        ),
                                   ]
                                ),
                            ],
                            value="only_title",
                        ),

                    ],
                ),
                html.Div(id="dashboard"),
                html.P(),   
                dmc.Grid(
                     children=[
                        dmc.Col(dmc.Button(
                            id = 'btn-save',
                            children="Guardar",
                            leftIcon=DashIconify(icon="fluent:save-20-filled"),
                            fullWidth=True,
                            disabled=True
                        ),span=6),
                        dmc.Col(dmc.Button(
                            id = "cancel",
                            children="Cancelar",
                            leftIcon=DashIconify(icon="fluent:backspace-20-filled"),
                            fullWidth=True,
                            color="red"
                        ),span=6)
                    ],
                    gutter="xs"
                ),
                html.Div(id="notifications-save"),
                
            ]
        )
        @app.callback(
            Output("filters","data"),
            Output("kpi-figure","data"),
            Input("select-head","value"),
        )
        def update_columns(select):
            if select != None:
                df = pd.DataFrame(eval(sp_dict[select]))
                dff = df[(df['Tipo Dato'] == "object")|(df['Tipo Dato'] == "string")]
                kpi_dff = kpi_df[kpi_df["sp_name"] == select]
                return dff['Columns'].values,list(kpi_dff["name"].values)
            else:
                return no_update
            
        @app.callback(
            Output("dashboard","children"),
            Output("btn-save","disabled"),
            #Output("body-dashboard","children"),
            #Input("select-head","value"),
            Input("filters","value"),
            Input("title-dash","value"),
            Input("checkbox-state-title","checked"),
            Input("kpi-figure","value"),
        )
        def update_create(columns, title,checkbox, name_kpi_list):
            def body_dashboard_layout(name_list_kpi = []):
                try :
                    dff = kpi_df[kpi_df["name"].isin(name_list_kpi)]
                    list_figure = dff["figure"].values
                    return [dmc.Col(card_graph(title =name[:-5],fig_ = fig), span=4)for fig,name  in zip(list_figure,name_list_kpi)]
                except:
                    return []
                #dmc.Grid(
                    #children=,      
                #    gutter="xl",
                #)
            def head_dashboard_layout(columns = [], only_title_col = False, name_list_kpi = []):
                    size_title = 12 if only_title_col == True else 4
                    return \
                    html.Div([
                        dmc.Grid(
                                children= 
                                [dmc.Col(dmc.Title(title_, align="center",order=2), span=size_title)]+
                                [dmc.Col([dmc.Select(label=filter,placeholder="Select one",id=f"select-{filter}")], span=2)for filter in columns],
                                
                                
                                
                            gutter="xl",
                        ),
                        dmc.Grid(
                            children=body_dashboard_layout(name_list_kpi = name_list_kpi),      
                            gutter="xl",
                        )
                    ])
            
            
            #try :
            title_ =  "Dashboard" if title == None or title == "" else title
            layout = head_dashboard_layout(columns = columns, only_title_col=checkbox,name_list_kpi = name_kpi_list)
            
            
            
            return layout,False

        @app.callback(
            Output("notifications-save", "children"),
            Input("btn-save","n_clicks"),
            State("dashboard","children"),
            State("title-dash","value"),
        )
        def update_save(n_clicks, children_dash,title):
            
            if n_clicks:
                print(type(children_dash))
                print(children_dash)
                createDashboard(name = title, dict_layout = str(children_dash), type = "Test")
                
                return dmc.Notification(
                                id="my-notification",
                                title="Save",
                                message="La Configuración se Guardo.",
                                #loading=True,
                                color="green",
                                action="show",
                                autoClose=False,
                                disallowClose=False,
                                icon=DashIconify(icon="akar-icons:circle-check"),
                                
                            )
        return app
    
