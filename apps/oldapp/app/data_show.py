from django_plotly_dash import DjangoDash
from ...resource.constants import EXTERNAL_STYLESHEETS, EXTERNAL_SCRIPTS
import dash_mantine_components as dmc
from ...resource.components.toggle import darkModeToggleDash
from ...resource.components.cards import card_graph,cardGraph
from ...resource.layouts.base import *
from ...resource.helpers.make_grid import *
from ...oldapp.utils import *
from dash_iconify import DashIconify
from asgiref.sync import sync_to_async
from .my_themes import *
from ...resource.components.notification import notification_update_show
from ...oldapp.callback import opened_modal,download_data

import plotly.io as pio
df = pd.read_parquet('test_excel.parquet', engine='pyarrow')#, engine='pyarrow'
df["Año"] = df["Año"].astype("string")


def dashShowSP(code: str):
    app = DjangoDash(name = code,external_stylesheets = EXTERNAL_STYLESHEETS, external_scripts = EXTERNAL_SCRIPTS)
    
    
    app.layout =  \
    Content([
        html.Div([dmc.Modal(title = '', id = f"modal_{i}", fullScreen=True, zIndex=10000, size= "85%" )for i in ['ingresos-tcliente','ingresos-cliente','utilidad-year','pedido-year','rank-producto','ingresos-pareto']]),
        Grid([
            Col([
                dmc.Title("Comercial Test")
            ],size=3),
            Col([
                dmc.MultiSelect(
                        #data=["React", "Angular", "Svelte", "Vue"],
                        id="year",
                        label = "Año",
                        placeholder = "Todos",
                        searchable=True,
                        nothingFound="Opción no encontrada",
                        value=sorted(df['Año'].unique()),
                        data=[{'label': i, 'value': i} for i in sorted(df['Año'].unique())],
                        size="sm", 
                    ),
            ],size=3),
            Col([
                dmc.Select(
                        label="Clasificación Productos",
                        placeholder="Todos",
                        id="tipo-producto",
                        value = None,
                        data= [],
                        clearable=True
                    )
            ],size=2),
            Col([
                dmc.Select(
                        label="Tipo de Cliente",
                        placeholder="Todos",
                        id="tipo-cliente",
                        value = None,
                        data= [],
                        clearable=True
                    )
            ],size=2),
            Col([
                dmc.Select(
                        label="Tipo de Comprobante",
                        placeholder="Todos",
                        id="tipo-comprobante",
                        value = None,
                        data= [],
                        clearable=True
                    )
            ],size=2),
            Col([
                cardGraph(id="ingresos-tcliente")
                #card_graph(id="ingresos-tcliente"),
                
            ],size=6),
            Col([
                cardGraph(id="ingresos-cliente")
                
            ],size=6),
            Col([
                cardGraph(id="utilidad-year")
                
            ],size=6),
            Col([
                cardGraph(id="pedido-year")
                
            ],size=6),
            Col([
                cardGraph(id="rank-producto")
                
            ],size=4),
            Col([
                cardGraph(id="ingresos-pareto")
                
            ],size=8),
        ]),
        html.Div(id='notifications-update-data'),
        dcc.Store(id='data-values'),
    ])
    @app.callback(
        [   
        Output('tipo-producto','data'),
        Output('tipo-cliente','data'),
        Output('tipo-comprobante','data'),
        Output("data-values","data"),
        Output("notifications-update-data","children")
        ],
        [   
        Input('year','value'),
        Input('tipo-producto','value'),
        Input('tipo-cliente','value'),
        Input('tipo-comprobante','value'),
        #Input('select-moneda','value'),
        ],
    )
    def update_data(year,tipo_producto,tipo_cliente,tipo_comprobante):
        if validar_all_none(variables = (year,tipo_producto,tipo_cliente,tipo_comprobante)) == True:
            dff = df.copy()
        else:
            dff = df.query(dataframe_filtro(values=(year,tipo_producto,tipo_cliente,tipo_comprobante),columns_df=['Año',"Clasificación de productos","Tipo de cliente","Tipo de comprobante"]))
        return[
            [{'label': i, 'value': i} for i in sorted(dff['Clasificación de productos'].unique())],
            [{'label': i, 'value': i} for i in sorted(dff['Tipo de cliente'].unique())],
            [{'label': i, 'value': i} for i in sorted(dff['Tipo de comprobante'].unique())],
            dff.to_dict('series'), 
            notification_update_show(text=f'Se cargaron {len(dff)} filas',title='Update')
        ]
    @app.callback(
        [   
        Output("ingresos-tcliente","figure"),
        Output("ingresos-cliente","figure"),
        Output("utilidad-year","figure"),
        Output("pedido-year","figure"),
        Output("rank-producto","figure"),
        Output("ingresos-pareto","figure"),
        ],
        [   
        Input("data-values","data"),
        ],
    )
    def update_graph(data):
        df = pd.DataFrame(data)
        tc_to_df =  df.groupby(['Tipo de cliente','Tipo de operación'])[['Ingreso total']].sum().sort_values(["Ingreso total","Tipo de operación"]).reset_index()
        tc_to_pivot_df = pd.pivot_table(tc_to_df,index=['Tipo de cliente'], values = "Ingreso total", columns = "Tipo de operación", aggfunc = "sum").reset_index().fillna(0)
        tc_to_pivot_df['Total'] = tc_to_pivot_df.sum(numeric_only=True, axis=1)
        tc_to_pivot_df = tc_to_pivot_df.sort_values("Total",ascending=False) 
        #
        c_to_df =  df.groupby(['Cliente','Tipo de operación'])[['Ingreso total']].sum().sort_values(["Ingreso total"]).reset_index()
        c_to_pivot_df = pd.pivot_table(c_to_df,index=['Cliente'], values = "Ingreso total", columns = "Tipo de operación", aggfunc = "sum").reset_index().fillna(0)
        c_to_pivot_df['Total'] = c_to_pivot_df.sum(numeric_only=True, axis=1)
        c_to_pivot_df = c_to_pivot_df.sort_values("Total",ascending=True) 
        #
        year_total_df = df.groupby(['Mes',"Mes_","Año"])[["Utilidad"]].sum().reset_index()
        total_pivot_df = pd.pivot_table(year_total_df,index = ["Mes","Mes_"],values="Utilidad",columns = "Año",aggfunc = "sum").sort_values("Mes_").reset_index()
        #
        n_items_df = df.groupby(["Mes","Mes_","Año","Nro de Pedido"])["Ingreso total"].count().reset_index()
        num_items_df = n_items_df.groupby(["Mes","Mes_","Año"])[["Nro de Pedido"]].count().sort_values("Mes_").reset_index()
        nr_items_pivot_df = pd.pivot_table(num_items_df,index = ["Mes","Mes_"],values="Nro de Pedido",columns = "Año",aggfunc = "sum").sort_values("Mes_").reset_index()
        #
        productos_df = df.groupby(["Descripción"])[["Ingreso total"]].sum().sort_values("Ingreso total", ascending = True).reset_index().tail(15)
        #
        productos_pareto_df = df.groupby(["Descripción"])[["Ingreso total"]].sum().sort_values("Ingreso total", ascending = False).reset_index()
        productos_pareto_df["%"] = productos_pareto_df["Ingreso total"]/productos_pareto_df["Ingreso total"].sum()
        productos_pareto_df['% acum']=productos_pareto_df['%'].cumsum(axis = 0, skipna = True) 
        
        #
        fig_1 = px.bar(tc_to_pivot_df, x='Tipo de cliente', y=["Garantía","Venta"],
                height=400, 
                template = "plotly_white",
                title = "<b>Ingresos por Tipo de Cliente</b>",
                color_discrete_sequence=px.colors.qualitative.Set2,
                
                
        )
        fig_1.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),legend_title_text='',height = 380,bargroupgap=0.4)
        fig_1.update_xaxes(tickfont=dict(size=15),showticklabels = True,title_font_family="sans-serif",title_font_size = 15,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
        fig_1.update_yaxes(tickfont=dict(size=15),showticklabels = True,title_font_family="sans-serif",title_font_size = 15,automargin=True)  
        fig_1.update_layout(yaxis_tickformat = ',',xaxis_title="",yaxis_title="<b>Ingresos</b>",)
        
        fig_2 = px.bar(c_to_pivot_df, x=["Garantía","Venta"], y='Cliente', #color='Tipo de operación' 
                height=400, 
                template = "plotly_white",
                title = "<b>Ingresos por Cliente</b>",
                orientation='h',
                color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_2.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),legend_title_text='',height = 380,)
        fig_2.update_layout(xaxis_title="",yaxis_title="<b>Cliente</b>")
        
        fig_3 = px.line(total_pivot_df, x="Mes", y=list(total_pivot_df.columns[2:]), title='<b>Utilidad Mensual por Año</b>', template = "plotly_white", markers=True,color_discrete_sequence=px.colors.qualitative.Set2)
        fig_3.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),legend_title_text='',height = 320,hovermode="x unified")
        fig_3.update_layout(xaxis_title="<b>Mes</b>",yaxis_title="<b>Ingresos</b>")
        
        fig_4 = px.line(nr_items_pivot_df, x="Mes", y=list(nr_items_pivot_df.columns[2:]), title='<b>N° de Pedidos Mensual por Año</b>', template = "plotly_white", markers=True,color_discrete_sequence=px.colors.qualitative.Set2)
        fig_4.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),legend_title_text='',height = 320,hovermode="x unified")
        fig_4.update_layout(xaxis_title="Mes",yaxis_title="<b>Ingresos</b>")
        
        fig_5 = px.bar(productos_df, x="Ingreso total", y='Descripción', #color='Tipo de operación' 
                #height=400, 
                template = "plotly_white",
                title = "<b>Ranking de los 15 Productos más Vendidos</b>",
                orientation='h',
                color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_5.update_layout(xaxis_title="<b>Ingresos</b>",yaxis_title="<b>Producto</b>")
        
        fig_6= go.Figure()
        fig_6.add_trace(go.Bar(
            x = productos_pareto_df['Descripción'],
            y = productos_pareto_df["%"],
            name = "Producto",
            cliponaxis=False,
            ))
        fig_6.add_trace(
                go.Scatter(
                    x=productos_pareto_df['Descripción'],
                    y=productos_pareto_df['% acum'],
                    yaxis="y2",
                    name="% Acumulado",
                    #marker=dict(color="crimson"),
                    cliponaxis=False,
                    
                )
            )
        fig_6.update_layout(
                #legend=dict(orientation="v"),
                yaxis=dict(
                    title=dict(text="<b>%</b>"),
                    side="left",
                    
                    #range=[0, stock_var_items_df[var_numerica].max()]
                ),
                yaxis2=dict(
                    title=dict(text="<b>% Acumulado</b>"),
                    side="right",
                    #range=[0, stock_var_items_df['Nro Items'].max()],
                    overlaying="y",
                    tickmode="auto",
                    
                ),
                template= "plotly_white"
            )
        fig_6.update_layout(yaxis_tickformat = '.1%',yaxis2_tickformat = '.0%')
        fig_6.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
        fig_6.update_layout(title_text="<b>Diagrama de Pareto - Ingresos por Producto</b>")
        return [fig_1,fig_2,fig_3,fig_4,fig_5,fig_6]
    opened_modal(app = app, id="ingresos-tcliente",height_modal=900)
    opened_modal(app = app, id="ingresos-cliente",height_modal=900)
    opened_modal(app = app, id="utilidad-year",height_modal=900)
    opened_modal(app = app, id="pedido-year",height_modal=900)
    opened_modal(app = app, id="rank-producto",height_modal=900)
    opened_modal(app = app, id="ingresos-pareto",height_modal=900)
    return app
    

"""
df = pd.DataFrame(json)
    app.layout =  \
    Content([
        Grid([
            Col([
                 dmc.Title(sp_name,align="left")
            ],size=11),
            Col([
                darkModeToggleDash()
            ],size=1),
            
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
                                            columnDefs=[{"field": i,"type": "leftAligned","maxWidth": 200} for i in df.columns],
                                            rowData=df.to_dict("records"),
                                            columnSize="sizeToFit",
                                            style={'font-size': '11px'},
                                            dashGridOptions={"enableCellTextSelection": True, "ensureDomOrder": True},
                                        )
                                    ])
                                ),
                    ],
                        value="table-accordion",
                ),
                        ],
            ),
            ])
        ])
    ])

"""