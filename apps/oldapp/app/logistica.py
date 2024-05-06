from django_plotly_dash import DjangoDash
from backend.connector import APIConnector
from ...resource.constants import EXTERNAL_STYLESHEETS, EXTERNAL_SCRIPTS
import dash_mantine_components as dmc
from ...resource.helpers.make_grid import *
from ...resource.layouts.base import *
from ...resource.components.toggle import darkModeToggleDash
from ...resource.components.cards import card_id,card_segment,card_stack
from ...resource.components.notification import notification_update_show
from ...oldapp.utils import *
from ...resource.components.datepicker import datepicker_alm
from ...oldapp.callback import opened_modal,download_data
from ...oldapp.transform import * 
from ...resource.helpers.make_task_sync import read_apis_sync
from datetime import datetime,timedelta
from dash_iconify import DashIconify

class DashLogistica:
    def __init__(self, ip: str, token :str):#, data_login: dict
        self.ip = ip
        self.token = token
    def logistica_stocks(self, code: str):
        app = DjangoDash(
                name = code,
                external_stylesheets = EXTERNAL_STYLESHEETS, 
                external_scripts = EXTERNAL_SCRIPTS,
        )
        
        dataframe = APIConnector( ip = self.ip, token = self.token).send_get_dataframe(
                    endpoint="nsp_stocks",
                    params=None
        )
        stocks_df = transform_nsp_stocks(dataframe)
        height_layout = 330
        app.layout =  \
        Content([
            html.Div([dmc.Modal(title = '', id = f"modal_{i}", fullScreen=True, zIndex=10000, size= "85%" )for i in ['bar-stock-items','bar-stock-familia','bar-top-producto','pie-stock-antiguedad','pie-items-antiguedad','bar-stock-abc-ventas','bar-stock-abc-valorizado']]),
            Grid([
                Col([
                    dmc.Title("Stocks")
                ],size= 4),
                Col([
                    dmc.Select(
                        label="Año",
                        placeholder="Todos",
                        id="select-year",
                        clearable=True
                    )
                ],size= 2),
                Col([
                    dmc.Select(
                        label="Grupo",
                        placeholder="Todos",
                        id="select-grupo",
                        clearable=True
                    )
                ],size= 2),
                Col([
                    dmc.Select(
                        label="Rango Antigüedad",
                        placeholder="Todos",
                        id="select-rango",
                        clearable=True
                    )
                ],size= 2),
                Col([
                    dmc.Select(
                        label="Moneda",
                        #placeholder="Todos",
                        id="select-coin",
                        value = "USD",
                        data= ["USD","PEN"],
                        clearable=False
                    )
                ],size= 1),
                Col([
                    darkModeToggleDash()
                ],size= 1),

                Col([
                    card_id(id_ = "bar-stock-items",title="Stock Valorizado y N° Items por mes y año",height=height_layout)
                ],size= 7),
                Col([
                    card_id(id_ = "bar-stock-familia",title="Stock por Grupo de Producto",height=height_layout)
                ],size= 5),
                Col([
                    card_id(id_ = "bar-top-producto",title="Productos (Stock Valorizado Top 10)",height=height_layout)
                ],size= 4),
                Col([
                    card_id(id_ = "pie-stock-antiguedad",title="Stock Valorizado segun Antigüedad",height=height_layout)
                ],size= 4),
                Col([
                    card_id(id_ = "pie-items-antiguedad",title="Nro Items segun Antigüedad",height=height_layout)
                ],size= 4),
                Col([
                    card_id(id_ = "bar-stock-abc-ventas",title="Porcentaje Stock por ABC Ventas",height=height_layout)
                ],size= 6),
                Col([
                    card_id(id_ = "bar-stock-abc-valorizado",title="Porcentaje Stock por ABC Stock Valorizado",height=height_layout)
                ],size= 6),

            ]),
            html.Div(id='notifications-update-data'),
            dcc.Store(id='data-values'),
        ])
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
        Output('themeHolder','theme'),Input('themeSwitch','checked'))
        @app.callback(
            [Output(output_,'data')for output_ in ['select-year','select-grupo','select-rango']]+
            [Output("data-values","data"), Output("notifications-update-data","children")],
            [Input(input_,"value")for input_ in ['select-year','select-grupo','select-rango']]
        )
        def update_filter(*args):
            
            if validar_all_none(variables = args) == True:
                df=stocks_df.copy()
            else:
                df=stocks_df.query(dataframe_filtro(values=list(args),columns_df=["Año","Grupo Producto","Rango antigüedad del stock"]))
        
            return [
                [{'label': i, 'value': i} for i in sorted(df['Año'].unique())],
                [{'label': i, 'value': i} for i in sorted(df['Grupo Producto'].unique())],
                [{'label': i, 'value': i} for i in sorted(df['Rango antigüedad del stock'].unique())],
                df.to_dict('series'),
                notification_update_show(text=f'Se cargaron {len(df)} filas',title='Update')
            ]
        @app.callback(
            Output('bar-stock-items','figure'),
            Output('bar-stock-familia','figure'),
            Output('bar-top-producto','figure'),
            Output('bar-stock-abc-ventas','figure'),
            Output('bar-stock-abc-valorizado','figure'),
            Output('pie-stock-antiguedad','figure'),
            Output('pie-items-antiguedad','figure'),
            Input("data-values","data"),
            Input('select-coin','value'),
            Input('themeSwitch','checked')
        )
        def update_graph(data,moneda,theme):
            df = pd.DataFrame(data)
            col_moneda = 'Soles' if moneda == 'PEN' else 'Dolares'
            theme_ = "plotly_white" if theme == True else "plotly_dark"
            return [
            figure_stock_var_y2(df=df, height = height_layout, moneda = col_moneda,template =theme_),
            figure_bar_familia(df = df, height = height_layout, moneda = col_moneda,template =theme_),
            figure_bar_top_producto(df = df, height = height_layout, moneda = col_moneda,template =theme_),
            figure_bar_relative(df = df, height = height_layout, eje_color = 'ABC Ventas', title = '', moneda = col_moneda,template =theme_),
            figure_bar_relative(df = df, height = height_layout, eje_color = 'ABC Stock', title = '', moneda = col_moneda,template =theme_),
            figure_pie_rango_stock(df = df, height = height_layout, moneda = col_moneda,template =theme_),
            figure_pie_rango_stock_count(df = df, height = height_layout, moneda = col_moneda,template =theme_)
        ]
        opened_modal(app = app, id="bar-stock-items",height_modal=900)
        opened_modal(app = app, id="bar-stock-familia",height_modal=900)
        opened_modal(app = app, id="bar-top-producto",height_modal=900)
        opened_modal(app = app, id="pie-stock-antiguedad",height_modal=900)
        opened_modal(app = app, id="pie-items-antiguedad",height_modal=900)
        opened_modal(app = app, id="bar-stock-abc-ventas",height_modal=900)
        opened_modal(app = app, id="bar-stock-abc-valorizado",height_modal=900)
        return app
    def estado_inventario(self, code: str):
        app = DjangoDash(
                name = code,
                external_stylesheets = EXTERNAL_STYLESHEETS, 
                external_scripts = EXTERNAL_SCRIPTS,
        )
        dataframe = APIConnector( ip = self.ip, token = self.token).send_get_dataframe(
                    endpoint="STOCKALMVAL",
                    params={ 'EMPRESA':'001','SUCURSAL':'','ALMACEN': '','FECHA':str(datetime.now())[:10].replace('-', ""), 'IDGRUPO':'','SUBGRUPO':'','DESCRIPCION':'','IDPRODUCTO':''}
        )
        stocks_df = transform_stockalmval(dataframe)
        segment_list = [{'label': 'Sucursal', 'value': 'Sucursal'},{'label': 'Almacén', 'value': 'Almacén'},{'label': 'Tipo', 'value': 'Tipo'},{'label': 'Grupo', 'value': 'Grupo'}]
        height_layout = 360
        height_layout_row_1 = 300
        
        app.layout =  \
        Content([
            html.Div([dmc.Modal(title = '', id = f"modal_{i}", fullScreen=True, zIndex=10000, size= "85%" )for i in ['bar-importe-stock','table-status','pie-estadoinv','bar-respon']]),    
            Grid([
                Col([
                    dmc.Title("Estado de Inventario", align="center")
                ],size= 11), 
                Col([
                    darkModeToggleDash(pt = 10)
                ],size= 1),
                Col([
                    datepicker_alm(dataframe=stocks_df,text="Inicio",tipo="inicio")
                ],size= 2),
                Col([
                    datepicker_alm(dataframe=stocks_df,text="Fin",tipo="fin")
                ],size= 2),
                Col([
                    dmc.Select(
                        label="Almacén",
                        placeholder="Todos",
                        id="select-almacen",
                        value = None,
                        data= [],
                        clearable=True
                    )
                ],size= 2),
                Col([
                    dmc.Select(
                        label="Tipo",
                        placeholder="Todos",
                        id="select-tipo",
                        value = None,
                        data= [],
                        clearable=True
                    )
                ],size= 2),
                Col([
                    dmc.Select(
                        label="Grupo",
                        placeholder="Todos",
                        id="select-grupo",
                        value = None,
                        data= [],
                        clearable=True
                    )
                ],size= 2),
                Col([
                    dmc.Select(
                        label="Moneda",
                        #placeholder="Todos",
                        id="select-coin",
                        value = "USD",
                        data= ["USD","PEN"],
                        clearable=False
                    )
                ],size= 2),
                Col([
                    card_segment(id_='bar-importe-stock',id_segmented='segmented-col',value = 'Sucursal',data = segment_list,height=height_layout_row_1)
                ],size= 8),
                Col([
                    card_id(id_='pie-estadoinv',title="Estado de Inventario",height=height_layout_row_1)
                ],size= 4),
                Col([
                    card_id(id_='table-status',height=height_layout,title="Tabla de Estado", graph=False)
                ],size= 8),
                Col([
                    card_id(id_='bar-respon',height=height_layout,title="N° Registros por Responsable")
                ],size= 4),
            ]),
            html.Div(id='notifications-update-data'),
            dcc.Store(id='data-values'),
        ])
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
        Output('themeHolder','theme'),Input('themeSwitch','checked'))

        @app.callback(
            [Output(output_,'data')for output_ in ['select-almacen','select-tipo','select-grupo']]+
            [Output("data-values","data"), Output("notifications-update-data","children")],
            [Input(input_,"value")for input_ in ['select-almacen','select-tipo','select-grupo']]+
            [Input("datepicker-inicio","value"),Input("datepicker-fin","value")]
        )
        def update_filter(*args):

            datepicker_inicio = datetime.strptime(args[-2], '%Y-%m-%d').date()
            datepicker_fin = datetime.strptime(args[-1], '%Y-%m-%d').date()
            inputs = args[:-2]
            filter_datepicker_df = stocks_df[(stocks_df['Última Fecha Ingreso']>=datepicker_inicio)&(stocks_df['Última Fecha Ingreso']<=datepicker_fin)]
            
            if validar_all_none(variables = inputs) == True:
                df=filter_datepicker_df.copy()
                
            else:
                df=stocks_df.query(dataframe_filtro(values=list(inputs),columns_df=["Almacén","Tipo","Grupo"]))
                
            return [
                [{'label': i, 'value': i} for i in sorted(df['Almacén'].unique())],
                [{'label': i, 'value': i} for i in sorted(df['Tipo'].unique())],
                [{'label': i, 'value': i} for i in sorted(df['Grupo'].unique())],
                df.to_dict('series'),
                notification_update_show(text=f'Se cargaron {len(df)} filas',title='Update')
            ]
        @app.callback(
            [Output('bar-importe-stock','figure'),
            Output('table-status','rowData'),
            Output('table-status','columnDefs'),
            Output('table-status','className'),
            #Output('table-status','getRowStyle'),
            Output('pie-estadoinv','figure'),
            Output('bar-respon','figure')],
            [Input("data-values","data"),
            Input("segmented-col","value"),
            Input('select-coin','value'),
            Input('themeSwitch','checked')]
        )
        def update_graph(data, segmented,moneda,theme):
            df = pd.DataFrame(data)
            col_moneda = 'Importe Soles' if moneda == 'PEN' else 'Importe Dolares'
            theme_ = "plotly_white" if theme == True else "plotly_dark"
            #print(df['Última Fecha Salida'].unique())
            dff = df[df['Duracion_Inventario'].notna()]
            
            table_dff = dff[['Sucursal', 'Almacén', 'Tipo','Grupo','Sub Grupo','Producto','Responsable Ingreso','Última Fecha Ingreso', 'Última Fecha Salida','Duracion_Inventario','Stock',col_moneda]]
            return [
                figure_stock_alm_y2(df = df, height = height_layout_row_1 , moneda = col_moneda, tipo = segmented,template=theme_),
                table_dff.to_dict("records"),
                [{"field": i,"cellStyle": {'font-size': 11}} for i in table_dff.columns],
                "ag-theme-alpine" if theme == True else "ag-theme-alpine-dark",
                figure_pie_estado_inv(df = df, height = height_layout_row_1,template=theme_),
                figure_bar_responsable(df = df, height = height_layout,template=theme_)
            ]
        opened_modal(app = app, id="bar-importe-stock",height_modal=900)
        opened_modal(app = app, id="pie-estadoinv",height_modal=900)
        opened_modal(app = app, id="bar-respon",height_modal=900)
        opened_modal(app = app, id="table-status",height_modal=900)
        return app
    
    def gestion_stock(self, code: str):
        app = DjangoDash(
                name = code,
                external_stylesheets = EXTERNAL_STYLESHEETS, 
                external_scripts = EXTERNAL_SCRIPTS,
        )
        consumoalm_params = {'C_EMP':'001','C_SUC':'','C_ALM': '','C_FECINI':str(datetime.now()- timedelta(days = 6 * 30))[:8].replace('-', "")+str('01')  ,'C_FECFIN':str(datetime.now())[:10].replace('-', ""),'C_VALOR':'1','C_GRUPO':'','C_SUBGRUPO':'','C_TEXTO':'','C_IDPRODUCTO':'','LOTEP':'','C_CONSUMIDOR':''}
        saldosalm_params = {'EMPRESA':'001','SUCURSAL':'','ALMACEN': '','FECHA':str(datetime.now())[:10].replace('-', ""),'IDGRUPO':'','SUBGRUPO':'','DESCRIPCION':'','IDPRODUCTO':'','LOTEP':''}
        cn = APIConnector( ip = self.ip, token = self.token)
        consumos_api_alm_df, saldos_api_alm_df= read_apis_sync(
            api_conector_1 = cn.send_get_dataframe,endpoint_1="NSP_OBJREPORTES_CONSUMOSALM_DET_BI",params_1 = consumoalm_params,
            api_conector_2 = cn.send_get_dataframe,endpoint_2="NSP_OBJREPORTES_SALDOSALMACEN_BI",params_2 = saldosalm_params
        )
        saldos_api_alm_df = change_cols_saldosalm(saldos_api_alm_df)

        height_layout = 360
        height_layout_row_1 = 300
        app.layout =  \
        Content([
            html.Div([dmc.Modal(title = '', id = f"modal_{i}", fullScreen=True, zIndex=10000, size= "85%" )for i in ['bar-minv-prom','bar-inv_val-first','bar-inv_val-second','bar-inv_val-thrid']]),
            Grid([
                Col([
                    dmc.Title("Gestión de Stocks",order=2)
                ],size= 2),
                Col([
                    dmc.Select(
                        label="Grupo",
                        placeholder="Todos",
                        id="select-grupo",
                        value = None,
                        data= [],
                        clearable=True
                    )
                ],size= 2),
                Col([
                    dmc.Select(
                        label="Subgrupo",
                        placeholder="Todos",
                        id="select-subgrupo",
                        value = None,
                        data= [],
                        clearable=True
                    )
                ],size= 2),
                Col([
                   dmc.Select(
                        label="Marca",
                        placeholder="Todos",
                        id="select-marca",
                        value = None,
                        data= [],
                        clearable=True
                    ) 
                ],size= 2),
                Col([
                    dmc.NumberInput(
                        id = 'cpm-min',
                        label="Cpm Min",
                        placeholder='-',
                        min=-10000,
                        max=100000,
                        step=1,
                        size="sm",                 
                    ),
 
                ],size= 1),
                Col([
                    dmc.NumberInput(
                        id = 'cpm-max',
                        label="Cpm Max",
                        placeholder='-',
                        min=-10000,
                        max=100000,
                        step=1,
                        size="sm",                 
                    ),
                    
                ],size= 1),
                Col([
                    dmc.Select(
                        label="Moneda",
                        #placeholder="Todos",
                        id="select-moneda",
                        value = "USD",
                        data= ["USD","PEN"],
                        clearable=False
                    )
                ],size= 1),
                Col([
                    darkModeToggleDash()
                ],size= 1),
                Col([
                    dmc.Card([
                        dmc.Select(
                            label="Sucursal",
                            placeholder="Todos",
                            id="select-sucursal",
                            size = 'md',
                            clearable = True,
                            searchable = True,
                        ),

                        dmc.Select(
                            label="Almacen",
                            placeholder="Todos",
                            id="select-almacen",
                            size = 'md',
                            clearable = True,
                            searchable = True,
                        ),
                        dmc.Space(h=20),
                        dmc.TextInput(
                            label="Código o Descripción",
                            id="text-input-find",
                            size='md',
                            placeholder="Buscar...",
                            icon=DashIconify(icon="ic:search"),
                        ),  
                        dmc.Space(h=20),
                        dmc.Button("Filtrar", variant="filled",id='btn-filtrar',size='md',fullWidth=True), 
                    ],
                    withBorder=True,
                    shadow='xl',
                    radius='md',)
                ],size= 3),
                Col([
                    Grid([
                        Col([
                            card_stack()
                        ]),
                        Col([
                            card_id(id_='bar-minv-prom',title="Estado de Inventario",height=320)

                        ]),
                    ])
                ],size= 9),
                Col([
                    dmc.Accordion(
                        value='table-accordion',
                        children=[
                            dmc.AccordionItem(
                                        [
                                            dmc.AccordionControl("Tabla Detalle",icon=DashIconify(icon="tabler:table-filled",color=dmc.theme.DEFAULT_COLORS["blue"][6], width=20)),
                                            dmc.AccordionPanel(
                                               html.Div(children=[
                                                    dmc.ActionIcon(
                                                                DashIconify(icon=f"feather:{"download"}"), 
                                                                color="blue", 
                                                                variant="default",
                                                                id=f"btn-download",
                                                                n_clicks=0,
                                                                mb=10,
                                                                style={'position': 'absolute','z-index': '99'},#'top': '4px','right': '4px',
                                                    ),
                                                            #actionIcon(ids=id_download,icono='download'),
                                                    dag.AgGrid(
                                                            id="table",
                                                            defaultColDef = {
                                                                "resizable": True,
                                                                "initialWidth": 130,
                                                                "wrapHeaderText": True,
                                                                "autoHeaderHeight": True,
                                                                "minWidth":130,
                                                                "sortable": True, 
                                                                "filter": True
                                                            },
                                                            
                                                            columnSize="sizeToFit",
                                                            style={'font-size': '11px'},
                                                            dashGridOptions={"enableCellTextSelection": True, "ensureDomOrder": True},
                                                            

                                            )])
                                            ),
                                        ],
                                        value="table-accordion",
                                    ),
                        ],
                    ),
                ]),
                Col([
                    card_id(id_='bar-inv_val-first',title="Sucursal por Inventario Valorizado",height=320)

                ],size= 4),
                Col([
                    card_id(id_='bar-inv_val-second',title="Almacen por Inventario Valorizado",height=320)

                ],size= 4),
                Col([
                    card_id(id_='bar-inv_val-thrid',title="Grupo Producto por Inventario Valorizado",height=320)

                ],size= 4)
            ]),
            html.Div(id='notifications-update-data'),
            dcc.Store(id='data-stock'),
            dcc.Store(id='data-values'),
            dcc.Store(id='data-table'),
            dcc.Download(id="download")
        ])
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
        Output('themeHolder','theme'),Input('themeSwitch','checked'))
        @app.callback(
        [
        Output('select-sucursal','data'),   
        Output('select-almacen','data'),
        Output('select-grupo','data'),
        Output('select-subgrupo','data'),
        Output('select-marca','data'),

        Output("card-cpm","children"),
        Output("card-invval","children"),
        Output("card-stock","children"),
        Output("card-consumo","children"),
        Output("card-total-stock","children"),
        
        Output("bar-minv-prom","figure"),
        Output("bar-inv_val-first","figure"),
        Output("bar-inv_val-second","figure"),
        Output("bar-inv_val-thrid","figure"),
        
        Output("table","rowData"),
        Output("table","columnDefs"),
        Output("table","className"),
        Output("data-table","data"),
         #Output("data-values","data"),
        Output("notifications-update-data","children")
         
        ],
        [Input('btn-filtrar','n_clicks'),Input('themeSwitch','checked')],
        [
         State('select-sucursal','value'),   
         State('select-almacen','value'),
         State('select-grupo','value'),
         State('select-subgrupo','value'),
         State('select-marca','value'),
         #State('num-meses','value'),
         State('text-input-find','value'),
         
         State('cpm-min','value'),
         State('cpm-max','value'),
         State('select-moneda','value'),
        ],
        
        
        )
        def update_data_stock(*args):
            n_clicks = args[0]
            theme = args[1]
            sucursal =  args[2] 
            almacen =  args[3]
            grupo =  args[4]
            subgrupo =  args[5]
            marca = args[6]
            #meses_back = args[6]# if args[6] != None or args[6] == 0 else '1'
            find_text = args[7]
            cpm_min = args[8] if args[8] != '' else None
            cpm_max = args[9] if args[9] != '' else None
            moneda = args[10]
            #className="ag-theme-alpine headers1",
            
            col_pu = 'PU_S' if moneda == 'PEN' else 'PU_D'
            inv_val_moneda = 'INV_VALMOF' if moneda == 'soles' else 'INV_VALMEX'
            sig = 'S/.' if moneda == 'PEN' else '$'
            theme_ = "plotly_white" if theme == True else "plotly_dark"

            if n_clicks == None:
                consumos_alm_df = consumos_api_alm_df.copy()
                saldos_alm_df = saldos_api_alm_df.copy()
            else:
                if validar_all_none(variables = (sucursal,almacen,grupo,subgrupo,marca)) == True:
                    consumos_alm_df = consumos_api_alm_df.copy()
                    saldos_alm_df = saldos_api_alm_df.copy()
                else:
                    if sucursal == None and almacen == None and grupo == None and subgrupo == None and marca != None:
                        consumos_alm_df = consumos_api_alm_df.copy()
                    else :
                        consumos_alm_df = consumos_api_alm_df.query(dataframe_filtro(values=[sucursal,almacen,grupo,subgrupo],columns_df=['SUCURSAL','ALMACEN','DSC_GRUPO','DSC_SUBGRUPO']))
                    saldos_alm_df = saldos_api_alm_df.query(dataframe_filtro(values=[sucursal,almacen,grupo,subgrupo,marca],columns_df=['SUCURSAL','ALMACEN','DSC_GRUPO','DSC_SUBGRUPO','MARCA']))

            
            input_df = saldos_alm_df.groupby(['SUCURSAL','ALMACEN','DSC_GRUPO','DSC_SUBGRUPO','MARCA'])[['STOCK']].sum().reset_index()
            ###
            
            #PRECIO UNITARIO PROM
            precio_unit_prom = saldos_alm_df.groupby(['COD_PRODUCTO'])[[col_pu]].mean().reset_index()
            precio_unit_prom = precio_unit_prom.rename(columns = {col_pu:'Precio Unitario Promedio'})
            precio_unit_prom['Precio Unitario Promedio'] = precio_unit_prom['Precio Unitario Promedio'].fillna(0).round(2)
            #
            consumos_alm_df = consumos_alm_df.groupby(['IDPRODUCTO'])[['CANTIDAD']].sum().reset_index()
            saldos_alm_group_df = saldos_alm_df.groupby(['DSC_GRUPO', 'DSC_SUBGRUPO', 'COD_PRODUCTO', 'DESCRIPCION', 'UM','MARCA'])[['PU_S','PU_D', 'STOCK', 'INV_VALMOF', 'INV_VALMEX']].sum().reset_index()
            dff = saldos_alm_group_df.merge(consumos_alm_df, how='left', left_on=["COD_PRODUCTO"], right_on=["IDPRODUCTO"])
            dff = dff.merge(precio_unit_prom,how='left', left_on=["COD_PRODUCTO"], right_on=["COD_PRODUCTO"])
            dff.loc[dff.MARCA =='','MARCA']='NO ESPECIFICADO'
            if find_text != None:
                dff = dff[(dff['COD_PRODUCTO'].str.contains(find_text))|(dff['DESCRIPCION'].str.contains(find_text))]
            
            
                
            dff['CANTIDAD'] = dff['CANTIDAD'].fillna(0)
            dff['STOCK'] = dff['STOCK'].fillna(0)
            dff['Precio Unitario'] = dff[col_pu].fillna(0)
            dff['CANTIDAD'] = dff['CANTIDAD']/6
            dff['CANTIDAD'] = dff['CANTIDAD'].round(2)
            dff['Meses Inventario'] = dff.apply(lambda x: meses_inventario(x['CANTIDAD'],x['STOCK']),axis=1)
            dff['TI'] = 1/dff['CANTIDAD']
            dff['TI'] = dff['TI'].replace([np.inf],0)
            #CARDS
            
            if cpm_min != None and cpm_max != None:
                dff = dff[(dff['CANTIDAD']>=cpm_min)&(dff['CANTIDAD']<=cpm_max)]
                
            cpm = round(dff['CANTIDAD'].mean(),2)
            invval = f"{sig}{(int(round(dff[inv_val_moneda].sum(),0))):,}"
            meses_invet_prom = dff[dff['Meses Inventario']!='NO ROTA']
            stock = round(meses_invet_prom['Meses Inventario'].mean(),2)
            consumo = round(dff['TI'].mean(),2)
            total_stock = f"{(int(round(dff['STOCK'].sum(),0))):,}"
            
            #GRAPHS
            mi_dff = dff[(dff['Meses Inventario']!='NO ROTA')]
            mi_dff = mi_dff[mi_dff['Meses Inventario']>0]
            
            df_mi_ =mi_dff.groupby(['COD_PRODUCTO','DESCRIPCION'])[['Meses Inventario']].sum().sort_values('Meses Inventario').reset_index().tail(30)
            
            df_mi_iv =mi_dff.groupby(['COD_PRODUCTO','DESCRIPCION'])[['Meses Inventario',inv_val_moneda]].sum().sort_values(inv_val_moneda).reset_index().tail(30)
            ##table
            df_table = dff[['DSC_GRUPO', 'DSC_SUBGRUPO', 'COD_PRODUCTO', 'DESCRIPCION', 'UM','MARCA','Precio Unitario Promedio', 'STOCK', inv_val_moneda,'IDPRODUCTO', 'CANTIDAD', 'Meses Inventario','TI']]
            df_table = df_table.drop(['IDPRODUCTO'], axis=1)

            df_table = df_table.rename(columns = {
                    'DSC_GRUPO':'GRUPO', 
                    'DSC_SUBGRUPO':'SUBGRUPO', 
                    'COD_PRODUCTO':'CODIGO', 
                    'DESCRIPCION':'DESCRIPCION', 
                    'UM':'UMD',
                    'MARCA':'MARCA', 
                    'STOCK':'STOCK', 
                    inv_val_moneda:f'Inventario Valorizado {moneda}', 
                    
                    'CANTIDAD': f'Consumo Promedio Mensual', 
                    'Meses Inventario':'Meses de Inventario', 
                    #'Inventario Valorizado':'Inventario Valorizado', 
                    'TI':'TI'
                })
            sucursal_df = saldos_alm_df.groupby(['SUCURSAL'])[[inv_val_moneda]].sum().sort_values(inv_val_moneda).reset_index()
            almacen_df = saldos_alm_df.groupby(['ALMACEN'])[[inv_val_moneda]].sum().sort_values(inv_val_moneda).reset_index()
            grupo_df = saldos_alm_df.groupby(['DSC_GRUPO'])[[inv_val_moneda]].sum().sort_values(inv_val_moneda).reset_index()
            return [
                [{'label': i, 'value': i} for i in sorted(input_df['SUCURSAL'].unique())],
                [{'label': i, 'value': i} for i in sorted(input_df['ALMACEN'].unique())],
                [{'label': i, 'value': i} for i in sorted(input_df['DSC_GRUPO'].unique())],
                [{'label': i, 'value': i} for i in sorted(input_df['DSC_SUBGRUPO'].unique())],
                [{'label': i, 'value': i} for i in sorted(input_df['MARCA'].unique())],
                cpm,invval,stock,consumo,total_stock,
                bar_logistica_y1(df = df_mi_,height = 320, template=theme_),
                #bar_logistica_y2(df = df_mi_iv,height = 320,y_col=inv_val_moneda ),
                bar_horizontal(df = sucursal_df, height = 350, x= inv_val_moneda, y = 'SUCURSAL', name_x='Inventario Valorizado', name_y='Sucursal',title = 'Sucursal por Inventario Valorizado',color = 'rgb(95, 70, 144)', template=theme_),
                bar_horizontal(df = almacen_df, height = 350, x= inv_val_moneda, y = 'ALMACEN', name_x='Inventario Valorizado', name_y='Almacen',title = 'Almacen por Inventario Valorizado',color ='rgb(29, 105, 150)', template=theme_),
                bar_horizontal(df = grupo_df, height = 350, x= inv_val_moneda, y = 'DSC_GRUPO', name_x='Inventario Valorizado', name_y='Grupo Producto',title = 'Grupo Producto por Inventario Valorizado',color = 'rgb(56, 166, 165)', template=theme_),
                df_table.to_dict("records"),
                fields_columns(columns = df_table.columns),
                "ag-theme-alpine" if theme == True else "ag-theme-alpine-dark",
                df_table.to_dict("series"),
                notification_update_show(text=f'Se cargaron {len(dff)} filas',title='Update')
            ]
        download_data(app,input_id_data='data-table',name_file = 'stocks_producto.xlsx')
        opened_modal(app, id="bar-minv-prom",height_modal=900)
        #opened_modal(app, id="bar-inv-val",height_modal=900)
        opened_modal(app, id="bar-inv_val-first",height_modal=900)
        opened_modal(app, id="bar-inv_val-second",height_modal=900)
        opened_modal(app, id="bar-inv_val-thrid",height_modal=900)
        return app
        