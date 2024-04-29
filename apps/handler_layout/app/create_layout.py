from django_plotly_dash import DjangoDash
from dash import Dash, dcc, html, Input, Output,State,dash_table,no_update,clientside_callback
import dash_mantine_components as dmc
import pandas as pd
import plotly.graph_objects as go
from ...resource.constants import EXTERNAL_STYLESHEETS, EXTERNAL_SCRIPTS
import uuid
from dash_iconify import DashIconify
from backend.connector import APIConnector
from ...resource.helpers.makelayout import *
from ...resource.components.filtering import  *
from ...handler_data.models import DataConfig
from ...resource.helpers.make_data import config_data
from ...handler_layout.model.create import createKPI

from ...resource.layouts.base import layout_base
class DashCreateLayout:
    def __init__(self, ip: str, token :str):
        self.ip = ip
        self.token = token
        
    def create_app(self, code: str, sp = []):
        app = DjangoDash(
                name = code,
                external_stylesheets = EXTERNAL_STYLESHEETS, 
                external_scripts = EXTERNAL_SCRIPTS,
                #suppress_callback_exceptions=True
        )
        cn = APIConnector(ip = self.ip, token = self.token)
        data_login = {}
        data_login["avatar_company"] = ""
        data_login["avatar_profile"] = ""
        data_login["avatar_company"] = ""
        data_login["name_user"] = ""
        layout_base(
            app,
            data_login = data_login, 
            children = [
                html.Div(id="notifications-save"),
                            dmc.Grid(
                                
                                
                                children=[
                                    dmc.Col(
                                        dmc.Title(
                                            children=[
                                                "Crear Gráfico"
                                            ],
                                            align="center",
                                            order = 1
                                        )
                                    
                                    , span=6),
                                    dmc.Col(
                                        dmc.Select(
                                            label="SP",
                                            placeholder="Select",
                                            id="select-sp",
                                            value=sp[0],
                                            data= sp,
                                            
                                            clearable=False
                                        )
                                    , span=2),
                                    dmc.Col(
                                        dmc.Select(
                                            label="Tipo Graph",
                                            placeholder="Seleccione",
                                            id="select-type",
                                            data=[
                                                'Bar px',
                                                'Pie px',
                                                'Line px',
                                                #'Table dag'
                                            ],
                                            clearable=False,
                                            value = "Bar px"
                                        )
                                    , span=2),
                                    
                                    dmc.Col(
                                        dmc.Select(
                                            label="Tipo Operación",
                                            placeholder="Seleccione",
                                            id="select-operacion",
                                            value = "sum",
                                            data=[
                                                'sum',
                                                'mean',
                                                'count',
                                                'cols'
                                            ],
                                            clearable=False
                                        ),span=2
                                    ),
                                    dmc.Col(
                                        dmc.MultiSelect(
                                            id = "multi-cate",
                                            label="Variable Categorica",
                                            #data=["React", "Angular", "Svelte", "Vue"],
                                            #value=["TIPOVENTA"],
                                            clearable=True,
                                            searchable=True
                                            #style={"width": 400},
                                        ),span=6
                                    ),
                                    dmc.Col(
                                        dmc.MultiSelect(
                                            id = "multi-num",
                                            label="Variable Númerica o Fecha",
                                            #data=["React", "Angular", "Svelte", "Vue"],
                                            #value=["CANTIDAD"],
                                            clearable=True,
                                            searchable=True
                                            #style={"width": 400},
                                        ),span=6
                                    ),
                                    
                                ],
                                gutter="xs",
                            ),
                            html.P(),   
                            html.Div(id="others-filt"),
                            html.Div(id="layout"),
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
                            
                            
                            dcc.Store(id='data-values'),
                            dcc.Store(id='data-layout'),
                            dcc.Store(id='data-layout-last'),
            ]
        )
        
              
        @app.callback(
            Output("multi-cate","data"),
            Output("multi-num","data"),
            Output("data-values","data"),
            Input("select-sp","value")
            
        )
        def update_multi_inputs(sp_name):
            dataframe = cn.send_get_dataframe(endpoint=sp_name)
            data_config = DataConfig.objects.filter(config_sp_name = f"data-config-{sp_name}")
            config_sp = [fila.config for fila in data_config]
            config_ = eval(config_sp[0])
            dff = config_data(dataframe=dataframe,config=config_)
            columns = list(dff.columns)
            return [columns,columns,dff.to_dict('series')]
        
        @app.callback(
            [Output("layout","children",allow_duplicate=True),#
            Output("others-filt","children"),
            Output("data-layout","data"),
            ],
            [Input("data-values","data"),
            Input("multi-cate","value"),
            Input("multi-num","value"),
            Input("select-type","value"),
            Input("select-operacion","value")],
            prevent_initial_call=True
                   
        )
        def update_layout(data,list_cate,list_num, type_layout,type_operation):
            print(list_num)
            print(list_cate)
            df = pd.DataFrame(data)

            if (list_cate != None and list_num != None) and (len(list_cate)!=0 and len(list_num)!=0):
                if type_layout != None and type_operation!= None:
                    dff = dataframe_group(
                        type_operation = type_operation,
                        dataframe=df,
                        var_cate=list_cate,
                        var_num=list_num
                    )
                    layout_1,layout2 =layout_create(
                        type_l = type_layout,
                        dataframe=dff,
                        cate = list_cate,
                        num = list_num
                    )
                    
                    
                    #print(go.Figure(layout2).to_dict())
                    return [layout_1,accordion_ftr(type = type_layout),layout2]#layout_['props']['figure']
                else:
                    return [no_update, None,None]
            else:
                return [no_update, None,None]
        
        @app.callback(
            Output("layout","children"),
            Output("data-layout-last","data"),#
            Output("btn-save", "disabled"),
            #Output("others-filt","children"),
            Input("data-layout","data"),
            Input("select-template","value"),
            #Input("input-name","value"),
            prevent_initial_call=True              
        )
        def update_w(fig, tem):
            
            figure=go.Figure(fig)
            figure.update_layout(template = tem)
            figure.update_xaxes(tickfont=dict(size=13),color='rgba(0, 0, 0, 0.8)',showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True) 
            figure.update_yaxes(tickfont=dict(size=13),color='rgba(0, 0, 0, 0.8)',showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True)
            return [
                dmc.Card([dcc.Graph(figure =figure,style={"height": 400})],withBorder=True,shadow = 'xl',radius = 'xs',style={"position": "static"},p=0),
                
                figure.to_dict(),
                False
            ]
        
        
        @app.callback(
            Output("notifications-save", "children"),
            #Output("btn-save", "disabled",allow_duplicate=True),
            Input("btn-save", "n_clicks"),
            State("data-layout-last","data"),
            State("input-name","value"),
            State("multi-cate","value"),
            State("multi-num","value"),
            State("select-type","value"),
            State("select-operacion","value"),
            State("select-sp","value"),
            prevent_initial_call=True              
        )
        def update_save(*args):
            
            dict_data = {}
            if args[0]:
                #try:
                    figure_dict = args[1]
                    name = args[2]
                    var_cate = args[3]
                    var_num = args[4]
                    type_ = args[5]
                    operation = args[6]
                    sp_name = args[7]
                    
                    dict_data["sp_name"] = sp_name
                    dict_data["kpi_name"] = str(name)+str(uuid.uuid4())[:5].upper()
                    dict_data["type_graph"] = type_
                    dict_data["operation"] = operation
                    dict_data["var_cate"] = var_cate
                    dict_data["var_num"] = var_num
                    dict_data["figure"] = figure_dict
                    createKPI(dict_kpi = dict_data)
                    return dmc.Notification(
                            id="my-notification",
                            title="Save",
                            message="La Configuración se Guardo.",
                            #loading=True,
                            color="green",
                            action="show",
                            autoClose=False,
                            disallowClose=False,
                            icon=DashIconify(icon="akar-icons:circle-check")
                        )
            """    
                except:
                    return dmc.Notification(
                            id="my-notification",
                            title="Error",
                            message="Hubo un problema.",

                            color="red",
                            action="show",
                            autoClose=False,
                            disallowClose=False,
                            icon=DashIconify(icon="akar-icons:circle-check"),
                        ),False
                """
                
            
        
        return app  
        
        