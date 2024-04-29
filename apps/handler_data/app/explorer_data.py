from django_plotly_dash import DjangoDash
from dash import Dash, dcc, html, Input, Output,State,dash_table,no_update,clientside_callback
import dash_mantine_components as dmc
import pandas as pd
from ...resource.constants import EXTERNAL_STYLESHEETS, EXTERNAL_SCRIPTS
import dash_ag_grid as dag
from datetime import datetime,timedelta
from dash_iconify import DashIconify
from backend.connector import APIConnector
from ...resource.components.head import head_global_dash
from ...resource.components.blocks import stats_data
from ...resource.utils.data import values_default, num_type_data,transform_fecha_col
from ...resource.layouts.base import layout_base
from ..model.create import createDataConfig
#import uuid

import plotly.express as px


class DashExplorerData:
    def __init__(self, ip: str, token :str):
        self.ip = ip
        self.token = token
    
    def create_app(self, code: str, model = None):
        
        sp_table = [[fila.sp_name,fila.parameters] for fila in model]
        sp_df = pd.DataFrame(sp_table,columns = ["SP","PARAMETERS"])
        sp_list = sp_df['SP'].unique()
        cn = APIConnector(ip = self.ip, token = self.token)
        app = DjangoDash(
            name = code,
            external_stylesheets = EXTERNAL_STYLESHEETS, 
            external_scripts = EXTERNAL_SCRIPTS,
            
        )
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
                                                "Transformación - Datos"
                                            ],
                                            align="center",
                                            order = 1
                                        )
                                    
                                    , span=6),
                                    dmc.Col(
                                        dmc.Select(
                                            label="Select Store Procedure",
                                            placeholder="Select",
                                            id="select-sp",
                                            value= sp_list[0],
                                            data = sp_list,
                                            
                                            clearable=False
                                        )
                                    
                                    , span=3),
                                    dmc.Col(
                                        dmc.Button(
                                            "Load from SP",
                                            id="loading-button",
                                            leftIcon=DashIconify(icon="fluent:database-plug-connected-20-filled"),
                                            mt = 21
                                        )
                                    , span=3),
                                    #dmc.Col(dmc.Text(id="clicked-output", mt=10), span=5),
                                ],
                                gutter="xl",
                            ),
                            
                            stats_data(),
                            
                            dmc.Accordion(
                                
                                children=[
                                    dmc.AccordionItem(
                                        [
                                            dmc.AccordionControl("Clean"),
                                            dmc.AccordionPanel(
                                                dmc.Grid([
                                                    dmc.Col([
                                                        dmc.Select(
                                                            label="Campo Fecha",
                                                            placeholder="Select",
                                                            id="select-col-fecha",
                                                            clearable=False,
                                                            searchable=True
                                                        ),
                                                    ],span=2),
                                                    dmc.Col([
                                                        dmc.Button(
                                                            "Crear Columnas",
                                                            id="btn-create-time-columns",
                                                            #leftIcon=DashIconify(icon="fluent:database-plug-connected-20-filled"),
                                                            mt = 21,
                                                            color="gray"
                                                        )
                                                    ],span=2)
                                                ],gutter="xs"),
                                                
                                            ),
                                        ],
                                        value="table",
                                        m =10,
                                    ),
                                    
                                ],
                            ),
                        #dcc.Store(id='data-values'),
                        dcc.Store(id='data-cols'),
                        #html.Div(id = "table-data-config"),
                        dmc.LoadingOverlay(
                            children=[
                                dag.AgGrid(
                                    id = "grid-cell-data-types",
                                    dashGridOptions={"animateRows": False},
                                    #className="ag-theme-alpine-dark",
                                    columnSize="sizeToFit",
                                    defaultColDef={"flex": 1},
                                    className="ag-theme-alpine dbc-ag-grid"
                                    
                                ), 
                            ],
                            loaderProps={"variant": "dots", "color": "orange", "size": "xl"},
                        ),
                        
                        html.Pre(id="output-cell-data-types"),
                        dcc.Download(id="download"),
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
                                        id = "btn-cancel",
                                        children="Cancelar",
                                        leftIcon=DashIconify(icon="fluent:backspace-20-filled"),
                                        fullWidth=True,
                                        color="red"
                                    ),span=6)
                                ],
                                gutter="xs"
                            ),
                        
            ]
        
        )
        
        app.clientside_callback(
            """
            function updateLoadingState(n_clicks) {
                return true
            }
            """,
            Output("loading-button", "loading", allow_duplicate=True),
            Input("loading-button", "n_clicks"),
            prevent_initial_call=True,
        )
        
        @app.callback(
            [
            #Output("table-data","columnDefs"),
            #Output("table-data","rowData"),
             Output("stat-cols","children"),
             Output("stat-rows","children"),
             Output("stat-cate","children"),
             Output("stat-num","children"),
             Output("stat-fecha","children"),
             Output("loading-button", "loading"),
             Output("grid-cell-data-types","columnDefs"),
             Output("grid-cell-data-types","rowData"),
             #Output("download", "data"),
             #Output("output-cell-data-types", "children"),
             Output("data-cols","data"),
             Output("btn-save", "disabled"),
             Output("select-col-fecha","data")
             #Output("data-values","data"),
            ],
            [Input("loading-button","n_clicks")],
            Input("btn-create-time-columns","n_clicks"),
            State("select-col-fecha","value"),
            [State("select-sp","value"),
             
             
             
             #State("btn-download", "n_clicks"),
             #State("grid-cell-data-types", "cellValueChanged"),
             #State("grid-cell-data-types", "virtualRowData"),
            ],
            prevent_initial_call=True,
        )
        def update_table(n_clicks,n_clicks_create_columns,fecha_transform,sp_name,):
            if n_clicks:
                filt_par = sp_df[sp_df['SP']==sp_name]['PARAMETERS'].values[0]
                parameters = None if filt_par == '' else eval(filt_par)
                dataframe = cn.send_get_dataframe(endpoint=sp_name, params= parameters)
                """
                ADD DATA COLUMNS TIME
                """
                if n_clicks_create_columns:
                    dataframe = transform_fecha_col(df = dataframe, col_fecha= fecha_transform)
                """"""
                
                
                columns = list(dataframe.columns)
                n_rows = dataframe.shape[0]
                """"""
                dtypes_list = []
                for i in dataframe.dtypes:
                    dtypes_list.append(str(i))
                """"""
                list_types = [str(i) for i in dataframe.dtypes]
                var_num_len, var_cate_len, var_fecha_len =num_type_data(list_types)
                #export_data = dataframe.to_dict("series")
                df_config = pd.DataFrame()
                df_config['Columns'] = list(dataframe.columns)
                df_config['Tipo Dato'] = dtypes_list
                df_config['Value default'] = values_default(dtypes_list)
                df_config['Estado'] = "Active"
                
                data_dict = {"Column_Fuente":columns, "Dtype_Fuente":list_types}
                return [
                    #[{"field": i, "type": "rightAligned"} for i in dataframe.columns],
                    #dataframe.to_dict("records"),
                    len(columns),
                    n_rows,
                    var_num_len,
                    var_cate_len,
                    var_fecha_len,
                    False,
                    [
                        {"field":"Columns", "editable":True},
                        {"field":"Tipo Dato","editable":True, "cellEditor": "agSelectCellEditor","cellEditorParams": {"values": ["object", "int", "float","int64","float64","string","datetime64"]}},
                        {"field":"Value default","editable":True},
                        {"field":"Estado","editable":True, "cellEditor": "agSelectCellEditor","cellEditorParams": {"values": ["Active", "Inactive"]}},#"editable": True,"cellEditor": "agCheckboxCellEditor",#"cellEditor": "agCheckboxCellEditor"
                    ],
                    df_config.to_dict('records'),

                    pd.DataFrame(data_dict,columns = ["Column_Fuente","Dtype_Fuente"]).to_dict("records"),
                    False,
                    columns  
                ]
                
        
        app.clientside_callback(
            """
            function updateLoadingState(n_clicks) {
                return true
            }
            """
            ,
            Output("btn-save", "loading", allow_duplicate=True),
            Input("btn-save", "n_clicks"),
            prevent_initial_call=True,
        )  
        
        
        @app.callback(
            Output("notifications-save", "children"),
            Output("btn-save", "disabled",allow_duplicate=True),
            Input("btn-save", "n_clicks"),
            State("grid-cell-data-types", "cellValueChanged"),
            State("grid-cell-data-types", "virtualRowData"),
            State("data-cols","data"),
            State("select-sp","value"),
            
            #State("save-modal", "opened"),
            prevent_initial_call=True,
            #btn-save
        )
        def update(n_clicks,changed,data, columns_fuente,sp_name):#changed,
            if n_clicks:
                dff = pd.DataFrame(data)
                dff['Fuente_Column'] =[columns_fuente[i]['Column_Fuente'] for i in range(len(columns_fuente))]
                dff['Fuente_Dtype'] =[columns_fuente[i]['Dtype_Fuente'] for i in range(len(columns_fuente))]
                try:
                    createDataConfig(config_data = dff.to_dict('records'),sp_name = sp_name)
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
                    ),True
                except:
                    return dmc.Notification(
                        id="my-notification",
                        title="Error",
                        message="Hubo un problema.",

                        color="red",
                        action="show",
                        autoClose=False,
                        disallowClose=True,
                        icon=DashIconify(icon="akar-icons:circle-check"),
                    ),False
                    
                    
                    
            else:
                return no_update
            
        
        
        return app
        

        """
          app.clientside_callback(
            
            function updateLoadingState(n_clicks) {
                return true
            }
            ,
            Output("btn-save", "loading", allow_duplicate=True),
            Input("btn-save", "n_clicks"),
            prevent_initial_call=True,
        )          
        """