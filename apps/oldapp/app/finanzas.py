from django_plotly_dash import DjangoDash
from backend.connector import APIConnector
from ...resource.constants import EXTERNAL_STYLESHEETS, EXTERNAL_SCRIPTS
import dash_mantine_components as dmc
from ...resource.helpers.make_grid import *
from ...resource.layouts.base import *
from ...resource.components.toggle import darkModeToggleDash
from ...resource.components.cards import card_id,cardGraph
from ...resource.components.notification import notification_update_show
from ...oldapp.utils import *
from ...oldapp.callback import opened_modal
from dash_bootstrap_templates import load_figure_template
from ...oldapp.transform import * 
from .my_themes import *

import plotly.io as pio


class DashFinanzas:
    def __init__(self, ip: str, token :str):#, data_login: dict
        self.ip = ip
        self.token = token

        #self.user_login = data_login
    def finanzas_bg(self, code: str):
        app = DjangoDash(
                name = code,
                external_stylesheets = EXTERNAL_STYLESHEETS, 
                external_scripts = EXTERNAL_SCRIPTS,
        )
        dataframe = APIConnector( ip = self.ip, token = self.token).send_get_dataframe(
                    endpoint="nsp_etl_situacion_financiera",
                    params=None
        )
        bg_df = transform_nsp_etl_situacion_financiera(df=dataframe)
        formato = bg_df['formato'].unique()
        height_layout = 380
        app.layout =  \
        Content([
            html.Div([dmc.Modal(title = '', id = f"modal_{i}", fullScreen=True, zIndex=10000, size= "85%" )for i in ['activo_graph','pasivo_graph','fondo_maniobra_graph']]),
            Grid([
                Col([
                    dmc.Title("Balance General")
                ],size= 3),
                Col([
                    dmc.Select(
                        label="Formato",
                        placeholder="Todos",
                        id="select-format",
                        value = formato[0],
                        data= formato,
                        clearable=False
                    )
                ],size= 2),
                Col([
                    dmc.Select(
                        label="Año",
                        placeholder="Todos",
                        id="select-year",
                        value = None,
                        data= [],
                        clearable=True
                    )
                ],size= 2),
                
                Col([
                    dmc.Select(
                        label="Trimestre",
                        placeholder="Todos",
                        id="select-quarter",
                        value = None,
                        data= [],
                        clearable=True
                    )
                ],size= 2),
                Col([
                    dmc.Select(
                        label="Mes",
                        placeholder="Todos",
                        id="select-month",
                        value = None,
                        data= [],
                        clearable=True
                    )
                ],size= 1),
                Col([
                    dmc.Select(
                        label="Moneda",
                        #placeholder="Todos",
                        id="select-coin",
                        value = "USD",
                        data= ["USD","PEN"],
                        clearable=True
                    )
                ],size= 1),
                Col([
                    darkModeToggleDash()
                ],size= 1),
                Col([
                    cardGraph(id="activo_graph")
                    #card_id(id_ = "activo_graph",title="ACTIVO",height=height_layout)
                ],size= 6),
                Col([
                    cardGraph(id="pasivo_graph")
                    #card_id(id_ = "pasivo_graph",title="PASIVO",height=height_layout)
                ],size= 6),
                Col([
                    cardGraph(id="fondo_maniobra_graph")
                    #card_id(id_ = "fondo_maniobra_graph",title="FONDO DE MANIOBRA",height=height_layout)
                ],size= 12),
                
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
            [   
                Output('select-year','data'),
                Output('select-quarter','data'),
                Output('select-month','data'),
                Output("data-values","data"),
                Output("notifications-update-data","children")
            ],
            [   
                Input('select-format','value'),
                Input('select-year','value'),
                Input('select-quarter','value'),
                Input('select-month','value'),
                #Input('select-moneda','value'),
            ],
        )
        def update_data_bg(format,year,quarter,month):
            dff = bg_df[bg_df['formato']==format]
            if validar_all_none(variables = (year,quarter,month)) == True:
                df = dff.copy()
            else:
                df = dff.query(dataframe_filtro(values=(year,month,quarter),columns_df=['Año',"Trimestre",'Mes_num']))
            
            return [
                [{'label': i, 'value': i} for i in sorted(df['Año'].unique())],
                [{'label': i, 'value': i} for i in sorted(df['Trimestre'].unique())],
                [{'label': i, 'value': i} for i in sorted(df['Mes_num'].unique())],
                
                df.to_dict('series'),  
                notification_update_show(text=f'Se cargaron {len(df)} filas',title='Update')
            ]
        @app.callback(
            [   
                Output("activo_graph","figure"),
                Output("pasivo_graph","figure"),
                Output("fondo_maniobra_graph","figure"),
            ],
            [   
                Input('select-coin','value'),
                Input("data-values","data"),
                Input('themeSwitch','checked')
            ],
        )
        def update_graph(moneda,data,theme):
            df = pd.DataFrame(data)
            col_moneda = 'saldomof' if moneda == 'PEN' else 'saldomex'
            theme_ = "plotly_white" if theme == True else "plotly_dark"
            
            #bg_df.groupby(['titulo1','titulo3'])[['saldomex']].sum().reset_index()
            activo_df = df[df['titulo1']=='ACTIVO']
            activo_p3_df = activo_df.groupby(['titulo1','titulo3'])[[col_moneda]].sum().sort_values(col_moneda).reset_index()
            pasivo_df = df[df['titulo1']=='PASIVO']
            pasivo_p3_df = pasivo_df.groupby(['titulo1','titulo3'])[[col_moneda]].sum().sort_values(col_moneda).reset_index()
            try :
                act_pas_corr_df = df[df['titulo2'].isin(['ACTIVO CORRIENTE','PASIVO CORRIENTE','ACTIVOS CORRIENTES','PASIVOS CORRIENTES'])]
                corr_pivot_df = pd.pivot_table(act_pas_corr_df,index=['periodo','Año', 'Mes', 'Mes_num', 'Mes_', 'Trimestre'],values= col_moneda,columns='titulo2',aggfunc='sum').reset_index()
                try:
                    corr_pivot_df['Fondo de Maniobra'] = corr_pivot_df['ACTIVO CORRIENTE'] - corr_pivot_df['PASIVO CORRIENTE']
                except:
                    corr_pivot_df['Fondo de Maniobra'] = corr_pivot_df['ACTIVO CORRIENTE'] - corr_pivot_df['PASIVOS CORRIENTES']
                fondo_mani_df = corr_pivot_df.groupby(['Mes_num','Mes_'])[['Fondo de Maniobra']].sum().sort_values('Mes_num',ascending = True).reset_index()
                fig_4 = px.bar(fondo_mani_df, x='Mes_', y='Fondo de Maniobra', #color='Tipo de operación' 
                    height=height_layout, 
                    template = "plotly_white",
                    orientation='v',
                    color_discrete_sequence=["rgb(93,105,177)"]
                    
                )
                fig_4.update_traces(hovertemplate='<br>'+"Fondo de Maniobra"+': <b>%{x}</b><br>'+moneda+': <b>%{y:,.1f}</b>',hoverlabel=dict(font_size=13,bgcolor="white"),cliponaxis=False,)
                fig_4.update_layout(legend=dict(orientation="v",yanchor="bottom",y=1.02,xanchor="right",x=1),legend_title_text='')
                fig_4.update_layout(xaxis_title='<b>'+"Mes"+'</b>',yaxis_title='<b>'+moneda+'</b>')
                fig_4.update_layout(yaxis_tickformat = ',',bargap=0.20,margin=dict(r = 20, t = 40,l=20,b = 20))
                fig_4.update_layout(title=dict(text="<b>Fondo de Maniobra</b>", font=dict(size=22,color="black"), automargin=True, yref='paper'))
            except:
                titulo2_df = df.groupby(['titulo2','Mes_num','Mes_'])[[col_moneda]].sum().reset_index()
                fig_4 = px.bar(titulo2_df, x='Mes_', y=col_moneda, color='titulo2',
                    height=height_layout, 
                    template = "plotly_white",
                    barmode='group',
                    color_discrete_sequence=px.colors.carto.Aggrnyl
                )
                fig_4.update_layout(xaxis_title='<b>'+"Mes"+'</b>',yaxis_title='<b>'+moneda+'</b>')
                fig_4.update_layout(
                    title = f"<b>Partidas Nivel 2</b>",
                    title_font_family="sans-serif", 
                    title_font_color="black", 
                    title_font_size = 18,
                    legend_title="",
                    #title_text="STOCK VALORIZADO Y NRO ITEMS POR MES Y AÑO",
                )
                fig_4.update_traces(hovertemplate='<br>'+"Mes"+': <b>%{x}</b><br>'+moneda+': <b>%{y:,.1f}</b>',hoverlabel=dict(font_size=13,bgcolor="white"),cliponaxis=False,)
            #table_df = df.groupby(['Año', 'Mes', 'Mes_num', 'Mes_','titulo1','titulo2', 'titulo3'])[[col_moneda]].sum().reset_index()
            #pivot_test_df = pd.pivot_table(table_df,index=['titulo1','titulo2', 'titulo3'],values=col_moneda,columns=['Año','Mes_num'],aggfunc='sum').fillna(0).reset_index()
            fig_2 = px.bar(activo_p3_df, x=col_moneda, y='titulo3', #color='Tipo de operación' 
                height=height_layout, 
                template = "plotly_white",
                #title = ,
                orientation='h',
                color_discrete_sequence=px.colors.sequential.RdBu,
                
            )
            fig_2.update_traces(hovertemplate='<br>'+"Activo"+': <b>%{y}</b><br>'+moneda+': <b>%{x:,.1f}</b>',hoverlabel=dict(font_size=13,bgcolor="white",bordercolor="darkblue"),cliponaxis=False,)
            fig_2.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),legend_title_text='')
            fig_2.update_layout(xaxis_title='<b>'+moneda+'</b>',yaxis_title='<b>'+"Partida"+'</b>')
            fig_2.update_layout(xaxis_tickformat = ',',bargap=0.20,margin=dict(r = 20, t = 40,l=20,b = 20))
            fig_2.update_layout(title=dict(text="<b>Activo</b>", font=dict(size=22,color="black"), automargin=True, yref='paper'))
            
            fig_3 = px.bar(pasivo_p3_df, x=col_moneda, y='titulo3', #color='Tipo de operación' 
                height=height_layout, 
                template = "plotly_white",
                #title = ,
                orientation='h',
                #color_discrete_sequence=px.colors.qualitative.G10,
                color_discrete_sequence=["rgb(204,102,119)"]
                
            )
            fig_3.update_traces(hovertemplate='<br>'+"Pasivo"+': <b>%{y}</b><br>'+moneda+': <b>%{x:,.1f}</b>',hoverlabel=dict(font_size=13,bgcolor="white"),cliponaxis=False,)
            fig_3.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),legend_title_text='')
            fig_3.update_layout(xaxis_title='<b>'+moneda+'</b>',yaxis_title='<b>'+"Partida"+'</b>')
            fig_3.update_layout(xaxis_tickformat = ',',bargap=0.20,margin=dict(r = 20, t = 40,l=20,b = 20))
            fig_3.update_layout(title=dict(text="<b>Pasivo</b>", font=dict(size=22,color="black"), automargin=True, yref='paper'))
            
            

            return [
                #bar_hor(df = activo_p3_df, height = height_layout, x= col_moneda, y = 'titulo3', name_x=moneda, name_y='Activo',title = '',color = '#4543E6',template=theme_),
                fig_2,
                #bar_hor(df = pasivo_p3_df, height = height_layout, x= col_moneda, y = 'titulo3', name_x=moneda, name_y='Pasivo',title = '',color = '#7EC2EB',template=theme_),
                fig_3,
                fig_4
                #bar_ver(df = fondo_mani_df, height = height_layout, x = 'Mes_',y='Fondo de Maniobra',name_x='Mes',name_y='Fondo de Maniobra',title = '',color = '#4374E6',template=theme_),

            ]
        opened_modal(app = app, id="activo_graph",height_modal=900)
        opened_modal(app = app, id="pasivo_graph",height_modal=900)
        opened_modal(app = app, id="fondo_maniobra_graph",height_modal=900)
        return app
    
    def finanzas_balance_ap(self, code: str):
        app = DjangoDash(
                name = code,
                external_stylesheets = EXTERNAL_STYLESHEETS, 
                external_scripts = EXTERNAL_SCRIPTS,
        )
        dataframe = APIConnector( ip = self.ip, token = self.token).send_get_dataframe(
                    endpoint="nsp_etl_situacion_financiera",
                    params=None 
        )
        bg_df = transform_nsp_etl_situacion_financiera(df=dataframe)
        formato = bg_df['formato'].unique()
        height_layout = 330
        app.layout =  \
        Content([
            html.Div([dmc.Modal(title = '', id = f"modal_{i}", fullScreen=True, zIndex=10000, size= "85%" )for i in ['ap-pie-graph','avsp-line-graph','comp-pasivo-graph','comp-activo-graph']]),
            Grid([
                Col([
                    dmc.Title("Activo & Pasivo")
                ],size= 3),
                Col([
                    dmc.Select(
                        label="Formato",
                        placeholder="Todos",
                        id="select-format",
                        value = formato[0],
                        data= formato,
                        clearable=False
                    )
                ],size= 2),
                Col([
                    dmc.Select(
                        label="Año",
                        placeholder="Todos",
                        id="select-year",
                        value = None,
                        data= [],
                        clearable=True
                    )
                ],size= 2),
                
                Col([
                    dmc.Select(
                        label="Trimestre",
                        placeholder="Todos",
                        id="select-quarter",
                        value = None,
                        data= [],
                        clearable=True
                    )
                ],size= 2),
                Col([
                    dmc.Select(
                        label="Mes",
                        placeholder="Todos",
                        id="select-month",
                        value = None,
                        data= [],
                        clearable=True
                    )
                ],size= 1),
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
                    cardGraph(id="ap-pie-graph")
                    #card_id(id_ = "ap-pie-graph",title="ACTIVO & PASIVO",height=height_layout)
                ],size= 4),
                Col([
                    cardGraph(id="avsp-line-graph")
                    #card_id(id_ = "avsp-line-graph",title="ACTIVO vs PASIVO",height=height_layout)
                ],size= 8),
                Col([
                    cardGraph(id="comp-pasivo-graph")
                    #card_id(id_ = "comp-pasivo-graph",title="COMPOSICIÓN DEL PASIVO",height=height_layout)
                ],size= 12),
                Col([
                    cardGraph(id="comp-activo-graph")
                    #card_id(id_ = "comp-activo-graph",title="COMPOSICIÓN DEL ACTIVO",height=height_layout)
                ],size= 12),
                
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
            [   
                Output('select-year','data'),
                Output('select-quarter','data'),
                Output('select-month','data'),
                Output("data-values","data"),
                Output("notifications-update-data","children")
            ],
            [   
                Input('select-format','value'),
                Input('select-year','value'),
                Input('select-quarter','value'),
                Input('select-month','value'),
                #Input('select-moneda','value'),
            ],
        )
        def update_data_bg(format,year,quarter,month):
            dff = bg_df[bg_df['formato']==format]
            if validar_all_none(variables = (year,quarter,month)) == True:
                df = dff.copy()
            else:
                df = dff.query(dataframe_filtro(values=(year,month,quarter),columns_df=['Año',"Trimestre",'Mes_num']))
            
            return [
                [{'label': i, 'value': i} for i in sorted(df['Año'].unique())],
                [{'label': i, 'value': i} for i in sorted(df['Trimestre'].unique())],
                [{'label': i, 'value': i} for i in sorted(df['Mes_num'].unique())],
                
                df.to_dict('series'),  
                notification_update_show(text=f'Se cargaron {len(df)} filas',title='Update')
            ]
        @app.callback(
            [   
                Output("ap-pie-graph","figure"),
                Output("avsp-line-graph","figure"),
                Output("comp-pasivo-graph","figure"),
                Output("comp-activo-graph","figure"),
            ],
            [   
                Input('select-coin','value'),
                Input("data-values","data"),
                Input('themeSwitch','checked')
            ],
        )
        def update_graph(moneda,data,theme):
            df = pd.DataFrame(data)
            col_moneda = 'saldomof' if moneda == 'PEN' else 'saldomex'
            theme_ = "plotly_white" if theme == True else "plotly_dark"
            
            colors_ = px.colors.qualitative.Bold+px.colors.qualitative.Set3
        
            ap_dff = df[df['titulo1'].isin(['ACTIVO','PASIVO'])]
            
            ap_df = ap_dff.groupby(['titulo1'])[[col_moneda]].sum().reset_index()
            ap_df[col_moneda] = ap_df[col_moneda].abs()
            
            line_df = ap_dff.groupby(['Año','Mes_num','Mes_','titulo1'])[[col_moneda]].sum().reset_index()
            line_df[col_moneda] = line_df[col_moneda].abs()
            line_pivot_dff = pd.pivot_table(line_df,index=['Año','Mes_num', 'Mes_'],values=col_moneda,columns='titulo1',aggfunc='sum').reset_index()
            line_pivot_dff['Year-Month'] = line_pivot_dff['Año'] +'-'+ line_pivot_dff['Mes_']
            
            activo_df = df[df['titulo1']=='ACTIVO']
            activo3_df = activo_df.groupby(['Año','Mes_num','Mes_','titulo3'])[[col_moneda]].sum().reset_index()
            activo3_df['Year-Month'] = activo3_df['Año'] +'-'+ activo3_df['Mes_']
            fig_activo = px.bar(activo3_df, y=activo3_df[col_moneda], x=activo3_df['Year-Month'],color = 'titulo3',template = theme_,color_discrete_sequence =colors_,custom_data=['titulo3'] )
            fig_activo.update_layout(uniformtext_minsize=8, uniformtext_mode='hide',height = height_layout)
            fig_activo.update_layout(barmode='relative',legend_title_text = 'Activo')
            fig_activo.update_traces(cliponaxis=False)
            fig_activo.update_xaxes(tickfont=dict(size=11),showticklabels = True,title_font_family="sans-serif",title_font_size = 11,automargin=True) 
            fig_activo.update_yaxes(tickfont=dict(size=11),showticklabels = True,title_font_family="sans-serif",title_font_size = 11,automargin=True)
            fig_activo.update_layout(
                margin = dict( l = 20, r = 40, b = 50, t = 40),
                xaxis_title = '<b>'+'Mes'+'</b>',
                yaxis_title = '<b>'+''+'</b>',
                legend=dict(font=dict(size=11))
            )                                                                           #'%{customdata}%'
            fig_activo.update_traces(hovertemplate='<br><b>%{x}</b><br><b>%{customdata[0]}</b><br><b>%{y:,.2f}</b>',hoverlabel=dict(font_size=13,bgcolor='rgba(255,255,255,0.75)',font_family="sans-serif",font_color = 'black'))
            fig_activo.update_layout(title=dict(text="<b>Composición del Activo</b>", font=dict(size=22,color="black"), automargin=True, yref='paper'))
            
            
            pasivo_df = df[df['titulo1']=='PASIVO']
            pasivo3_df = pasivo_df.groupby(['Año','Mes_num','Mes_','titulo3'])[[col_moneda]].sum().reset_index()
            pasivo3_df['Year-Month'] = pasivo3_df['Año'] +'-'+ pasivo3_df['Mes_']
            fig_pasivo = px.bar(pasivo3_df, y=pasivo3_df[col_moneda], x=pasivo3_df['Year-Month'],color = 'titulo3',template = theme_,color_discrete_sequence =colors_,custom_data=['titulo3'])
            fig_pasivo.update_layout(uniformtext_minsize=8, uniformtext_mode='hide',height = height_layout)
            fig_pasivo.update_layout(barmode='relative',legend_title_text = 'Pasivo')
            fig_pasivo.update_traces(cliponaxis=False)
            fig_pasivo.update_xaxes(tickfont=dict(size=11),showticklabels = True,title_font_family="sans-serif",title_font_size = 11,automargin=True) 
            fig_pasivo.update_yaxes(tickfont=dict(size=11),showticklabels = True,title_font_family="sans-serif",title_font_size = 11,automargin=True)
            fig_pasivo.update_layout(
                margin = dict( l = 20, r = 40, b = 50, t = 40,),
                xaxis_title = '<b>'+'Mes'+'</b>',
                yaxis_title = '<b>'+''+'</b>',
                legend=dict(font=dict(size=11))
            )
            fig_pasivo.update_traces(hovertemplate='<br><b>%{x}</b><br><b>%{customdata[0]}</b><br><b>%{y:,.2f}</b>', hoverlabel=dict(font_size=13,bgcolor='rgba(255,255,255,0.75)',font_family="sans-serif",font_color = 'black'))
            fig_pasivo.update_layout(title=dict(text="<b>Composición del Pasivo</b>", font=dict(size=22,color="black"), automargin=True, yref='paper'))
            return [pie_(
                        df = ap_df, 
                        label_col = 'titulo1', 
                        value_col = col_moneda, 
                        title = 'ACTIVO & PASIVO',
                        height=height_layout,
                        showlegend = True,
                        #color_list=['#ccaa14','#7a9c9f'],
                        dict_color={'ACTIVO':'#7a9c9f','PASIVO':'#ccaa14'},
                        hole = .6,
                        textinfo = 'percent+value',
                        textposition='outside',
                        template = theme_
                    ),
                    
                    figure_n_traces(df = line_pivot_dff, height = height_layout , trace = ['ACTIVO','PASIVO'],colors = ['#7a9c9f','#ccaa14'],ejex=['Year-Month'],hover_unified=True,template = theme_,title="Activo vs Pasivo"),
                    fig_activo,
                    fig_pasivo,
                    
            ]
        opened_modal(app, id="ap-pie-graph",height_modal=900)
        opened_modal(app, id="avsp-line-graph",height_modal=600)
        opened_modal(app, id="comp-activo-graph",height_modal=900)
        opened_modal(app, id="comp-pasivo-graph",height_modal=900)
        return app
    
    def finanzas_analisis_activo(self, code: str):
        app = DjangoDash(
                name = code,
                external_stylesheets = EXTERNAL_STYLESHEETS, 
                external_scripts = EXTERNAL_SCRIPTS,
        )
        dataframe = APIConnector( ip = self.ip, token = self.token).send_get_dataframe(
                    endpoint="nsp_etl_situacion_financiera",
                    params=None
        )
        bg_df = transform_nsp_etl_situacion_financiera(df=dataframe)
        formato = bg_df['formato'].unique()
        years=sorted(bg_df['Año'].unique())
        height_layout = 330
        app.layout =  \
        Content([
            html.Div([dmc.Modal(title = '', id = f"modal_{i}", fullScreen=True, zIndex=10000, size= "85%" )for i in ['activo-graph','actvant-graph','corr-ncorr-graph','cuentas-act-graph']]),
            Grid([
                Col([
                    dmc.Title("Análisis del Activo")
                ],size= 3),
                Col([
                    dmc.Select(
                        label="Formato",
                        placeholder="Todos",
                        id="select-format",
                        value = formato[0],
                        data= formato,
                        clearable=False
                    )
                ],size= 2),
                Col([
                    dmc.MultiSelect(
                        #data=["React", "Angular", "Svelte", "Vue"],
                        id="select-year",
                        label = "Año",
                        placeholder = "Todos",
                        searchable=True,
                        nothingFound="Opción no encontrada",
                        value=[years[-1],years[-2]],
                        data=years,
                        size="sm", 
                    ),
                ],size= 3),
                
                Col([
                    dmc.Select(
                        label="Trimestre",
                        placeholder="Todos",
                        id="select-quarter",
                        value = None,
                        data= [],
                        clearable=True
                    )
                ],size= 1),
                Col([
                    dmc.Select(
                        label="Mes",
                        placeholder="Todos",
                        id="select-month",
                        value = None,
                        data= [],
                        clearable=True
                    )
                ],size= 1),
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
                    cardGraph(id="activo-graph")
                    #card_id(id_ = "activo-graph",title="ACTIVO",height=height_layout)
                ],size= 4),
                Col([
                    cardGraph(id="actvant-graph")
                    #card_id(id_ = "actvant-graph",title="ACTIVO - AÑO COMPARATIVO",height=height_layout)
                ],size= 8),
                Col([
                    cardGraph(id="corr-ncorr-graph")
                    #card_id(id_ = "corr-ncorr-graph",title="ACTIVO CORRIENTE VS NO CORRIENTE",height=height_layout)
                ],size= 6),
                Col([
                    cardGraph(id="cuentas-act-graph")
                    #card_id(id_ = "cuentas-act-graph",title="CUENTAS DE ACTIVOS",height=height_layout)
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
            [   
                Output('select-quarter','data'),
                Output('select-month','data'),
                Output("data-values","data"),
                Output("notifications-update-data","children")
            ],
            [   
                Input('select-format','value'),
                Input('select-year','value'),
                Input('select-quarter','value'),
                Input('select-month','value'),
                #Input('select-moneda','value'),
            ],
        )
        def update_data_bg(format,year,quarter,month):
            dff = bg_df[bg_df['formato']==format]
            if validar_all_none(variables = (year,quarter,month)) == True:
                df = dff.copy()
            else:
                df = dff.query(dataframe_filtro(values=(year,month,quarter),columns_df=['Año',"Trimestre",'Mes_num']))
            
            return [
                [{'label': i, 'value': i} for i in sorted(df['Trimestre'].unique())],
                [{'label': i, 'value': i} for i in sorted(df['Mes_num'].unique())],
                
                df.to_dict('series'),  
                notification_update_show(text=f'Se cargaron {len(df)} filas',title='Update')
            ]
        @app.callback(
            [   
                Output("activo-graph","figure"),
                Output("actvant-graph","figure"),
                Output("corr-ncorr-graph","figure"),
                Output("cuentas-act-graph","figure"),
            ],
            [   
                Input('select-coin','value'),
                Input("data-values","data"),
                Input('themeSwitch','checked')
            ],
        )
        def update_graph(moneda,data,theme):
            df = pd.DataFrame(data)
            col_moneda = 'saldomof' if moneda == 'PEN' else 'saldomex'
            theme_ = "plotly_white" if theme == True else "plotly_dark"
            colors_ = px.colors.qualitative.Bold+px.colors.qualitative.Set3
            
            activo_dff = df[df['titulo1'].isin(['ACTIVO'])]
            ap_df = activo_dff.groupby(['titulo2'])[[col_moneda]].sum().reset_index()
            ap_df[col_moneda] = ap_df[col_moneda].abs()
            
            
            year_act_df = activo_dff.groupby(['Año','Mes_num','Mes_'])[[col_moneda]].sum().reset_index()
            year_df = pd.pivot_table(year_act_df,index=['Mes_num', 'Mes_'],values=col_moneda,columns='Año',aggfunc='sum').reset_index()
            #ap_df[col_moneda] = ap_df[col_moneda].abs()
            
            act2_df = activo_dff.groupby(['Año','Mes_num','Mes_','titulo2'])[[col_moneda]].sum().reset_index()
            act2_pv_df = pd.pivot_table(act2_df,index=['Año','Mes_num', 'Mes_'],values=col_moneda,columns='titulo2',aggfunc='sum').reset_index()
            act2_pv_df['Year-Month'] = act2_pv_df['Año'] +'-'+ act2_pv_df['Mes_']
            
            act4_df = activo_dff.groupby(['titulo4'])[[col_moneda]].sum().sort_values(col_moneda).reset_index()
            

            return [pie_(
                    df = ap_df, 
                    label_col = 'titulo2', 
                    value_col = col_moneda, 
                    title = 'Activo',
                    height=height_layout,
                    showlegend = True,
                    dict_color={'ACTIVO CORRIENTE':'#2B4CEA','ACTIVO NO CORRIENTE':'#974EE6','ACTIVOS NO CORRIENTES':'#974EE6'},
                    hole = .6,
                    textinfo = 'percent+value',
                    textposition='outside',
                    template=theme_
                ),
                figure_n_traces(df = year_df, height = height_layout , trace = sorted(year_act_df['Año'].unique()),colors = colors_,ejex=['Mes_'],template=theme_,title="Activo - Año Comparativo"),
                figure_n_traces(df = act2_pv_df, height = height_layout , trace = act2_df['titulo2'].unique(),colors = colors_,ejex=['Year-Month'],template=theme_,title="Activo - Corriente vs No Corriente"),
                bar_ver(df = act4_df, height = height_layout , x = 'titulo4',y = col_moneda,name_x = '',name_y = 'Saldos',color = '#3aa99b', title = 'Cuentas de Activos',showticklabels_x = False,botton_size = None,template=theme_)
                ]
        opened_modal(app, id="activo-graph",height_modal=900)
        opened_modal(app, id="actvant-graph",height_modal=900)
        opened_modal(app, id="corr-ncorr-graph",height_modal=900)
        opened_modal(app, id="cuentas-act-graph",height_modal=900)
        return app
    
    def finanzas_analisis_pasivo(self, code: str):
        app = DjangoDash(
                name = code,
                external_stylesheets = EXTERNAL_STYLESHEETS, 
                external_scripts = EXTERNAL_SCRIPTS,
        )
        dataframe = APIConnector( ip = self.ip, token = self.token).send_get_dataframe(
                    endpoint="nsp_etl_situacion_financiera",
                    params=None
        )
        bg_df = transform_nsp_etl_situacion_financiera(df=dataframe)
        formato = bg_df['formato'].unique()
        years=sorted(bg_df['Año'].unique())
        height_layout = 330
        app.layout =  \
        Content([
            html.Div([dmc.Modal(title = '', id = f"modal_{i}", fullScreen=True, zIndex=10000, size= "85%" )for i in ['pasivo-graph','pasvant-graph','corr-ncorr-graph','cuentas-pas-graph']]),
            Grid([
                Col([
                    dmc.Title("Análisis del Pasivo")
                ],size= 3),
                Col([
                    dmc.Select(
                        label="Formato",
                        placeholder="Todos",
                        id="select-format",
                        value = formato[0],
                        data= formato,
                        clearable=False
                    )
                ],size= 2),
                Col([
                    dmc.MultiSelect(
                        #data=["React", "Angular", "Svelte", "Vue"],
                        id="select-year",
                        label = "Año",
                        placeholder = "Todos",
                        searchable=True,
                        nothingFound="Opción no encontrada",
                        value=[years[-1],years[-2]],
                        data=years,
                        size="sm", 
                    ),
                ],size= 3),
                
                Col([
                    dmc.Select(
                        label="Trimestre",
                        placeholder="Todos",
                        id="select-quarter",
                        value = None,
                        data= [],
                        clearable=True
                    )
                ],size= 1),
                Col([
                    dmc.Select(
                        label="Mes",
                        placeholder="Todos",
                        id="select-month",
                        value = None,
                        data= [],
                        clearable=True
                    )
                ],size= 1),
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
                    cardGraph(id="pasivo-graph")
                    #card_id(id_ = "pasivo-graph",title="PASIVO",height=height_layout)
                ],size= 4),
                Col([
                    cardGraph(id="pasvant-graph")
                    #card_id(id_ = "pasvant-graph",title="PASIVO- AÑO COMPARATIVO",height=height_layout)
                ],size= 8),
                Col([
                    cardGraph(id="corr-ncorr-graph")
                    #card_id(id_ = "corr-ncorr-graph",title="PASIVO CORRIENTE VS NO CORRIENTE",height=height_layout)
                ],size= 6),
                Col([
                    cardGraph(id="cuentas-pas-graph")
                    #card_id(id_ = "cuentas-pas-graph",title="CUENTAS DE PASIVOS",height=height_layout)
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
            [   
                Output('select-quarter','data'),
                Output('select-month','data'),
                Output("data-values","data"),
                Output("notifications-update-data","children")
            ],
            [   
                Input('select-format','value'),
                Input('select-year','value'),
                Input('select-quarter','value'),
                Input('select-month','value'),
                #Input('select-moneda','value'),
            ],
        )
        def update_data_bg(format,year,quarter,month):
            dff = bg_df[bg_df['formato']==format]
            if validar_all_none(variables = (year,quarter,month)) == True:
                df = dff.copy()
            else:
                df = dff.query(dataframe_filtro(values=(year,month,quarter),columns_df=['Año',"Trimestre",'Mes_num']))
            
            return [
                [{'label': i, 'value': i} for i in sorted(df['Trimestre'].unique())],
                [{'label': i, 'value': i} for i in sorted(df['Mes_num'].unique())],
                
                df.to_dict('series'),  
                notification_update_show(text=f'Se cargaron {len(df)} filas',title='Update')
            ]
        @app.callback(
            [   
                Output("pasivo-graph","figure"),
                Output("pasvant-graph","figure"),
                Output("corr-ncorr-graph","figure"),
                Output("cuentas-pas-graph","figure"),
            ],
            [   
                Input('select-coin','value'),
                Input("data-values","data"),
                Input('themeSwitch','checked')
            ],
        )
        def update_graph(moneda,data,theme):
            df = pd.DataFrame(data)
            col_moneda = 'saldomof' if moneda == 'PEN' else 'saldomex'
            theme_ = "plotly_white" if theme == True else "plotly_dark"
            colors_ = px.colors.qualitative.Bold+px.colors.qualitative.Set3
            
            pasivo_dff = df[df['titulo1'].isin(['PASIVO'])]
            ap_df = pasivo_dff.groupby(['titulo2'])[[col_moneda]].sum().reset_index()
            ap_df[col_moneda] = ap_df[col_moneda].abs()
            
            year_act_df = pasivo_dff.groupby(['Año','Mes_num','Mes_'])[[col_moneda]].sum().reset_index()
            year_df = pd.pivot_table(year_act_df,index=['Mes_num', 'Mes_'],values=col_moneda,columns='Año',aggfunc='sum').reset_index()
            #ap_df[col_moneda] = ap_df[col_moneda].abs()
            
            pas2_df = pasivo_dff.groupby(['Año','Mes_num','Mes_','titulo2'])[[col_moneda]].sum().reset_index()
            pas2_pv_df = pd.pivot_table(pas2_df,index=['Año','Mes_num', 'Mes_'],values=col_moneda,columns='titulo2',aggfunc='sum').reset_index()
            pas2_pv_df['Year-Month'] = pas2_pv_df['Año'] +'-'+ pas2_pv_df['Mes_']
            
            
            pas4_df = pasivo_dff.groupby(['titulo4'])[[col_moneda]].sum().sort_values(col_moneda).reset_index()
            return [
                pie_(
                    df = ap_df, 
                    label_col = 'titulo2', 
                    value_col = col_moneda, 
                    title = 'Pasivo', 
                    height=height_layout,
                    showlegend = True,
                    dict_color={'PASIVO CORRIENTE':'#2B4CEA','PASIVO NO CORRIENTE':'#974EE6','PASIVOS CORRIENTES':'#2B4CEA','PASIVOS NO CORRIENTES':'#974EE6'},
                    hole = .6,
                    textinfo = 'percent+value',
                    textposition='outside',
                    template=theme_
                ),
                figure_n_traces(df = year_df, height = height_layout , trace = sorted(year_act_df['Año'].unique()),colors = colors_,ejex=['Mes_'],template=theme_,title="Pasivo - Año Comparativo"),
                figure_n_traces(df = pas2_pv_df, height = height_layout , trace = pas2_df['titulo2'].unique(),colors = colors_,ejex=['Year-Month'],template=theme_,title="Pasivo - Corriente vs No Corriente"),
                bar_ver(df = pas4_df, height = height_layout , x = 'titulo4',y = col_moneda,name_x = '',name_y = 'Saldos',color = '#3aa99b', title = 'Cuentas de Pasivos',showticklabels_x = False,botton_size = 50,template=theme_)
            ]
        opened_modal(app, id="pasivo-graph",height_modal=900)
        opened_modal(app, id="pasvant-graph",height_modal=900)
        opened_modal(app, id="corr-ncorr-graph",height_modal=900)
        opened_modal(app, id="cuentas-pas-graph",height_modal=900)
        return app