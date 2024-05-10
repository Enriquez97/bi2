from django_plotly_dash import DjangoDash
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
from backend.connector import APIConnector
class DashComercial:
    def __init__(self, dataframe):#, data_login: dict
        self.dataframe = dataframe
    def comercial_informe(self, code: str):
        app = DjangoDash(
                name = code,
                external_stylesheets = EXTERNAL_STYLESHEETS, 
                external_scripts = EXTERNAL_SCRIPTS,
        )
        
        
        df = transform_nsp_rpt_ventas_detallado(self.dataframe)
       
        #stocks_df = transform_nsp_stocks(dataframe)
        height_layout = 310
        inputs_ = ['select-year','select-cliente','select-tipo-venta','select-grupo-producto','select-grupo-cliente','select-producto']
        app.layout =  \
        Content([
            html.Div([dmc.Modal(title = '', id = f"modal_{i}", fullScreen=True, zIndex=10000, size= "85%" )for i in ['bar-comercial-productos','pie-comercial-pais','pie-comercial-vendedor','bar-comercial-mes','funnel-comercial-selector_second']]),
            Grid([
                Col([
                dmc.Title("Informe de Ventas", align="center")
                ],size= 11), 
                Col([
                    darkModeToggleDash(pt = 10)
                ],size= 1),
                Col([
                    dmc.Select(
                        label="Año",
                        placeholder="Todos",
                        id="select-year",
                        value = None,
                        data= [],
                        clearable=True
                    )
                ],size= 1),
                Col([
                    dmc.Select(
                        label="Cliente",
                        placeholder="Todos",
                        id="select-cliente",
                        value = None,
                        data= [],
                        clearable=True
                    )
                    
                ],size= 2),
                Col([
                    dmc.Select(
                        label="Tipo de Venta",
                        placeholder="Todos",
                        id="select-tipo-venta",
                        value = None,
                        data= [],
                        clearable=True
                    )
                ],size= 2),
                Col([
                    dmc.Select(
                        label="Grupo de Producto",
                        placeholder="Todos",
                        id="select-grupo-producto",
                        value = None,
                        data= [],
                        clearable=True
                    )
                ],size= 2),
                Col([
                    dmc.Select(
                        label="Grupo Cliente",
                        placeholder="Todos",
                        id="select-grupo-cliente",
                        value = None,
                        data= [],
                        clearable=True
                    )
                ],size= 2),
                Col([
                    dmc.Select(
                        label="Producto",
                        placeholder="Todos",
                        id="select-producto",
                        value = None,
                        data= [],
                        clearable=True
                    )
                ],size= 2),
                
                Col([
                    dmc.Select(
                        label="Moneda",
                        id="select-coin",
                        value = "USD",
                        data= ["USD","PEN"],
                        clearable=False
                    )
                ],size= 1),
                Col([
                    card_id(id_ = "bar-comercial-productos",title="Productos más Vendidos",height=height_layout)
                ],size= 6),
                Col([
                    card_id(id_ = "pie-comercial-pais",title="País",height=height_layout)
                ],size= 3),
                Col([
                    card_id(id_ = "pie-comercial-vendedor",title="Vendedor",height=height_layout)
                ],size= 3),
                Col([
                    card_id(id_ = "bar-comercial-mes",title="Ventas por Mes",height=height_layout)
                ],size= 6),
                Col([
                    card_id(id_ = "funnel-comercial-selector_second",title="Grupo Producto más vendido",height=height_layout)
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
        [Output(output_,'data')for output_ in inputs_]+
        [
        Output("data-values","data"),
        Output("notifications-update-data","children")],
        [Input(input_,"value")for input_ in inputs_]  
        )
        def update_filters(*args):
            if validar_all_none(variables = args) == True:
                dff=df.copy()
            else:
            #'select-grupo-producto','select-grupo-cliente','select-producto'    
                dff=df.query(dataframe_filtro(values=list(args),columns_df=['Año','Cliente','Tipo de Venta','Grupo Producto','Grupo Cliente','Producto']))
            
            return[
                [{'label': i, 'value': i} for i in sorted(df['Año'].unique())],
                [{'label': i, 'value': i} for i in sorted(df['Cliente'].unique())],
                [{'label': i, 'value': i} for i in sorted(df['Tipo de Venta'].unique())],
                [{'label': i, 'value': i} for i in sorted(df['Grupo Producto'].unique())],
                [{'label': i, 'value': i} for i in sorted(df['Grupo Cliente'].unique())],
                [{'label': i, 'value': i} for i in sorted(df['Producto'].unique())],
                dff.to_dict('series'),
                notification_update_show(text=f'Se cargaron {len(dff)} filas',title='Update')
            ]
        @app.callback(
            [
            Output('bar-comercial-productos','figure'),
            Output('bar-comercial-mes','figure'),
            Output('funnel-comercial-selector_second','figure'),
            Output('pie-comercial-pais','figure'),
            Output('pie-comercial-vendedor','figure')],
            [
            Input("data-values","data"),
            Input('select-coin',"value"),
            Input('themeSwitch','checked')
            ]
            
        )
        def update_graph(data,moneda,theme):
            df = pd.DataFrame(data)
            importe = 'Importe Soles' if moneda == 'PEN' else 'Importe Dolares'
            theme_ = "plotly_white" if theme == True else "plotly_dark"

            productos_df_20=df.groupby(['Producto','Grupo Producto','Subgrupo Producto'])[[importe]].sum().sort_values(importe,ascending=True).tail(20).reset_index()
            productos_df_20['Producto']=productos_df_20['Producto'].str.capitalize()
            
            grupo_producto_df = df.groupby(['Grupo Producto'])[[importe]].sum().reset_index().round(2)
            grupo_producto_df=grupo_producto_df[grupo_producto_df[importe]>0].sort_values(importe, ascending = False)
            
            meses_df_12 = df.groupby(['Mes','Mes Num'])[[importe]].sum().reset_index().sort_values('Mes Num',ascending=True).reset_index()
            meses_df_12['Porcentaje']=(meses_df_12[importe]/meses_df_12[importe].sum())*100
            meses_df_12['Porcentaje']=meses_df_12['Porcentaje'].map('{:,.1f}%'.format)
            #df[importe].map('{:,.1f}%'.format)
            pais_df = df.groupby(['Pais'])[[importe]].sum().sort_values(importe,ascending=True).reset_index()
            vendedor_df = df.groupby(['Vendedor'])[[importe]].sum().sort_values(importe,ascending=True).reset_index()
            return[
            bar_comercial(df=productos_df_20, x= importe, y= 'Producto',orientation= 'h', height = height_layout, 
              title= '', customdata=['Grupo Producto','Subgrupo Producto'],space_ticked= 180, text= importe,
                xaxis_title = importe, template= theme_,left=30
            ),
            bar_comercial(df=meses_df_12, x= 'Mes', y= importe,orientation= 'v', height = height_layout, 
                title= '', customdata=['Porcentaje'],space_ticked= 50, text= importe, yaxis_title= importe,xaxis_title= 'Mes',
                template=theme_,
            ),
            funnel_comercial(df = grupo_producto_df, x = importe, y = 'Grupo Producto', height = height_layout,xaxis_title = importe, yaxis_title = 'Grupo Producto', title = '',template=theme_),
            pie_comercial(df = pais_df, title = '',label_col = 'Pais', value_col = importe, height = height_layout, showlegend=False,textfont_size = 10,template=theme_),
            pie_comercial(df = vendedor_df, title = '',label_col = 'Vendedor', value_col = importe, height = height_layout, showlegend=False,textfont_size = 10,template=theme_)
            ]
        
        opened_modal(app = app, id="bar-comercial-productos",height_modal=900)
        opened_modal(app = app, id="pie-comercial-pais",height_modal=900)
        opened_modal(app = app, id="pie-comercial-vendedor",height_modal=900)
        opened_modal(app = app, id="bar-comercial-mes",height_modal=900)
        opened_modal(app = app, id="funnel-comercial-selector_second",height_modal=900)

    def resumen_ventas(self, code: str):
        app = DjangoDash(
                name = code,
                external_stylesheets = EXTERNAL_STYLESHEETS, 
                external_scripts = EXTERNAL_SCRIPTS,
        )
        
        df = transform_nsp_rpt_ventas_detallado(self.dataframe)
        list_year = sorted(df['Año'].astype('string').unique())
        list_tv = sorted(df['Tipo de Venta'].unique())
        #stocks_df = transform_nsp_stocks(dataframe)
        height_layout = 310
        inputs_ = ['select-grupo-producto','select-grupo-cliente','select-producto','select-cliente']
        app.layout =  \
        Content([
            html.Div([dmc.Modal(title = '', id = f"modal_{i}", fullScreen=True, zIndex=10000, size= "85%" )for i in ['pie_tipo_venta','bar_gp','bar_gc','bar_cliente_top','bar_producto_top','bar_mes']]),
            dmc.Drawer(
                title="Filtros",
                id="offcanvas-placement",
                padding="md",
                closeOnClickOutside=False,
                closeOnEscape=True,
                lockScroll=False,
                withOverlay=False,
                size="270px",
                style={'position': 'absolute','z-index': '99999'},
                children=[
                    dmc.Select(
                        id="select-grupo-producto",
                        label="Grupo de Producto",
                        size = 'md',
                        placeholder="Todos",
                        clearable = True,
                        searchable = True
                    ),
                    dmc.Select(
                        id="select-grupo-cliente",
                        label="Grupo de Cliente",
                        size = 'md',
                        placeholder="Todos",
                        clearable = True,
                        searchable = True
                    ),
                    dmc.Select(
                        id="select-producto",
                        label="Producto",
                        size = 'md',
                        placeholder="Todos",
                        clearable = True,
                        searchable = True
                    ),
                    dmc.Select(
                        id="select-cliente",
                        label="Cliente",
                        size = 'md',
                        placeholder="Todos",
                        clearable = True,
                        searchable = True
                    ),
                ],
                
            ),
            Grid([
                Col([
                    dmc.ActionIcon(
                        DashIconify(icon="feather:filter"), 
                        color = "blue", 
                        variant = "default",
                        id = "btn-filter",
                        n_clicks=0,
                        mb=10,
                        style = {'position': 'absolute','z-index': '99'}
                    ),
                ],size = 1),
                Col([
                    dmc.Title("Resumen de Ventas",order=2)
                ],size = 3),
                Col([
                    dmc.Select(
                        label="Año",
                        placeholder="Todos",
                        id="id_year",
                        value = list_year[-1],
                        data= list_year,
                        clearable=True
                    )
                ],size = 1),
                Col([
                    dmc.MultiSelect(
                        id="id_tipo_venta",
                        label="Tipo de Venta",
                        placeholder="Todos",
                        searchable=True,
                        nothingFound="Opción no encontrada",
                        style={'font-size': "80%"},
                        data=list_tv,
                        size="sm", 
                    )
                ],size = 5),
                Col([
                    dmc.Select(
                        label="Moneda",
                        #placeholder="Todos",
                        id="select-coin",
                        value = "USD",
                        data= ["USD","PEN"],
                        clearable=False
                    )
                ],size = 1),
                Col([
                    darkModeToggleDash()
                ],size = 1),
                Col([
                    card_id(id_ = "pie_tipo_venta",title="Ventas por Tipo",height=height_layout)
                ],size = 4),
                Col([
                    card_id(id_ = "bar_gp",title="Ventas por Grupo Producto",height=height_layout)
                ],size = 4),
                Col([
                    card_id(id_ = "bar_gc",title="Ventas por Grupo Cliente",height=height_layout)
                ],size = 4),
                Col([
                    card_id(id_ = "bar_cliente_top",title="Ventas por Cliente (Top 20)",height=height_layout)
                ],size = 4),
                Col([
                    card_id(id_ = "bar_producto_top",title="Ventas por Producto (Top 20)",height=height_layout)
                ],size = 4),
                Col([
                    card_id(id_ = "bar_mes",title="Ventas por Mes",height=height_layout)
                ],size = 4),
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
            Output("offcanvas-placement", "opened"),
            [Input("btn-filter", "n_clicks")]
    )
        @app.callback(
        [Output(output_,'data')for output_ in inputs_]+
        [Output('data-values','data'),Output('notifications-update-data','children')],
        [Input('id_year','value'),Input('id_tipo_venta','value')]+
        [Input(input_,"value")for input_ in inputs_]
        )
        def update_data(*args):
            if validar_all_none(variables = args) == True:#(anio,tipo_v)
                dff = df.copy()
            else:   
                if args[0] != None:
                    year_mod = int(args[0])
                    args = tuple(year_mod if i == 0 else elemento for i, elemento in enumerate(args))
                #df = dff.query(dataframe_filtro(values=(anio,tipo_v),columns_df=['Año','Tipo de Venta'])) 
                dff = df.query(dataframe_filtro(values=args,columns_df=['Año','Tipo de Venta','Grupo Producto','Grupo Cliente','Producto','Cliente']))   
            return [
            [{'label': i, 'value': i} for i in sorted(df['Grupo Producto'].unique())],
            [{'label': i, 'value': i} for i in sorted(df['Grupo Cliente'].unique())],
            [{'label': i, 'value': i} for i in sorted(df['Producto'].unique())],
            [{'label': i, 'value': i} for i in sorted(df['Cliente'].unique())],
            dff.to_dict('series'),  
            notification_update_show(text=f'Se cargaron {len(dff)} filas',title='Update')
            ]
        @app.callback(
        Output('pie_tipo_venta','figure'),
        Output('bar_gp','figure'),
        Output('bar_gc','figure'),
        Output('bar_cliente_top','figure'),
        Output('bar_producto_top','figure'),
        Output('bar_mes','figure'),
        Input('data-values','data'),
        Input('select-coin','value'),
        Input('themeSwitch','checked')
        )
        def update_build_dashboard(data, moneda_,theme):
        
            df = pd.DataFrame(data)
            moneda = 'Importe Soles' if moneda_ == 'PEN' else 'Importe Dolares'
            theme_ = "plotly_white" if theme == True else "plotly_dark"

            tv_df = df.groupby(['Tipo de Venta'])[[moneda]].sum().reset_index()
            tv_df = tv_df[tv_df['Tipo de Venta'].isin(list(tv_df['Tipo de Venta'].values))]
            
            gp_df = df.groupby(['Grupo Producto'])[[moneda]].sum().sort_values(moneda).reset_index()
            gc_df = df.groupby(['Grupo Cliente'])[[moneda]].sum().sort_values(moneda).reset_index()
            
            client_top_df = df.groupby(['Cliente'])[[moneda]].sum().sort_values(moneda).tail(20).reset_index()
            product_top_df = df.groupby(['Producto'])[[moneda]].sum().sort_values(moneda).tail(20).reset_index()
            
            meses_df = df.groupby(['Mes','Mes Num'])[[moneda]].sum().reset_index().sort_values('Mes Num',ascending=True).reset_index()
            meses_df['Porcentaje']=(meses_df[moneda]/meses_df[moneda].sum())*100
            meses_df['Porcentaje']=meses_df['Porcentaje'].map('{:,.1f}%'.format)
            return [ 
                pie_comercial(
                df = tv_df, 
                label_col = 'Tipo de Venta', 
                value_col = moneda, 
                title = '',
                height=height_layout,
                showlegend = False,
                template=theme_
                #color_list= dara_colores,
                #hole = .8
                ),
                bar_chart(df = gp_df, x = moneda, y = 'Grupo Producto', height=height_layout, titulo = '',color ='#306c9a', orientacion = 'h', template=theme_),
                bar_chart(df = gc_df, x = moneda, y = 'Grupo Cliente', height=height_layout, titulo = '',color ='#61abe3', orientacion = 'h',template=theme_),
                bar_chart(df = client_top_df, x = moneda, y = 'Cliente', height=height_layout, titulo = '',color ='#5ccbc2', orientacion = 'h',template=theme_),
                bar_chart(df = product_top_df, x = moneda, y = 'Producto', height=height_layout, titulo = '',color ='#e2c5c5', orientacion = 'h',template=theme_),
                bar_chart(df = meses_df, x = 'Mes', y = moneda, height=height_layout, titulo = '',color ='#5f6b6d', orientacion = 'v',template=theme_),
            ]
        opened_modal(app = app, id="pie_tipo_venta",height_modal=900)
        opened_modal(app = app, id="bar_gp",height_modal=900)
        opened_modal(app = app, id="bar_gc",height_modal=900)
        opened_modal(app = app, id="bar_cliente_top",height_modal=900)
        opened_modal(app = app, id="bar_producto_top",height_modal=900)
        opened_modal(app = app, id="bar_mes",height_modal=900)
"""
pie_tipo_venta
bar_gp
bar_gc
bar_cliente_top
bar_producto_top
bar_mes
"""