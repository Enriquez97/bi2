import dash_mantine_components as dmc
from django_plotly_dash import DjangoDash
from backend.connector import APIConnector
from ...resource.helpers.make_grid import *
from ...resource.layouts.base import *
from ...resource.constants import EXTERNAL_STYLESHEETS, EXTERNAL_SCRIPTS
from ...resource.components.cards import card_id,card_segment,card_stack,cardGraph
from ...resource.components.notification import notification_update_show
from ...oldapp.utils import *
from ...oldapp.callback import opened_modal,download_data
from plotly.subplots import make_subplots
from dash_iconify import DashIconify

DICT_TIPO_COSTO={
    'Insumos':'lightcyan',
    'Mano de obra':'#575d6d',
    'Depreciación':'royalblue',
    'Otros':'darkblue',
    'Maquinaria':'#123570',
    'Riego':'cyan'
}

def get_parameters_datepicker(df=pd.DataFrame(),col_inicio='',col_fin=''):
    minimo = str(df[col_inicio].min())
    maximo = str(df[col_fin].max())
    datepicker=[minimo,maximo]
    return [minimo, maximo, datepicker]

def hoversize_recurso_agricola(recurso = ''):
   if recurso=='Insumos':
        hover='<br><b>Cantidad</b>: %{y:.1f} Kg<br> <b>Unidad/Ha</b>: %{customdata[0]:.1f}<br>'
        size_text=9
   elif recurso=='Maquinaria':
        hover='<br><b>Cantidad</b>: %{y:.1f} h<br> <b>Hm/Ha</b>: %{customdata[0]:.1f} <br>'
        size_text=13
   elif recurso=='Mano de obra':
        hover='<br><b>Cantidad</b>: %{y:.1f} jr<br> <b>Jr/Ha</b>: %{customdata[0]:.1f}<br>'
        size_text=13
   elif recurso=='Riego':
        hover='<br><b>Cantidad</b>: %{y:.1f} m3<br> <b>m3/Ha</b>: %{customdata[0]:.1f}<br>'
        size_text=13
   else: 
        hover='<br><b>Cantidad</b>: %{y:.1f}<br>{text} <b>-/Ha</b>: %{customdata[0]:.1f}<br>'
        size_text=9
   return [hover,size_text]

DIC_RECURSOS_AGRICOLA = {
    
    'Metros cúbicos':"#00B6FF",
    'Horas máquina':"#000000",
    'Jornales':"#740000",
    'Potasio':"#1F77B4",
    'Calcio':"#FF7F0E",
    'Fosforo':"#2CA02C",
    'Magnesio':"#9467BD",
    'Nitrogeno':"#8C564B",
    'Zinc':"#BCBD22",

}
def create_dataframe_costos_tipo(
     df = pd.DataFrame(), category_col = [], numeric_col = [] ,radio_tipo_costo = ''
):
     if radio_tipo_costo == 'por ha':
          #LOS VALUES DE numeric_col deben ser saldo y luego area
          dff = df.groupby(category_col)[numeric_col].sum().reset_index()#.sort_values(numeric_col[0],ascending=True)
          dff[numeric_col[0]] = dff[numeric_col[0]]/dff[numeric_col[1]]
          return dff.sort_values(numeric_col[0],ascending=True) 
     else: 
          return df.groupby(category_col)[numeric_col].sum().reset_index().sort_values(numeric_col[0],ascending=True) 
      
      
def create_dict_of_list(df,col='Ingresos_Generales',dict_color=None,list_partidas=[],pivot=True,col_=''):
     total=df[col].sum()
     lista_diccionario=[]
     for element in list_partidas:
          if pivot==True:
               percent_value=round((df[element].sum()/total)*100)
          else:
               df_filtro=df[df[col_]==element]
               percent_value=round((df_filtro[col].sum()/total)*100)
          dicts={'value': percent_value, 'color': dict_color[element], 'label': f'{percent_value}%', "tooltip": element}
                #print(f"UNA ITERACION:{(df[element].sum()/total)*100}")
          lista_diccionario.append(dicts)
     return lista_diccionario
 
def line_(
        df = pd.DataFrame(), x = '', y = '', color = None, height = 360,x_title = '',
        y_title = '', title_legend = '', order = {}, title ='',
        template = 'plotly_white', discrete_color = {}, custom_data=[],
        hover_template = '', size_text = 11, legend_orizontal = True, markers = False,legend_font_size = 12,
        tickfont_x = 11, tickfont_y = 11, 
    ):
        ejex = 'Semana' if x == 'week' else 'Fecha'
        figure = px.line(
            df, x = x, y = y, color = color , template = template,
            color_discrete_map = discrete_color, 
             hover_name = color,
            custom_data = custom_data,
            markers = markers,
            category_orders=order,
            
            #color_discrete_sequence  = '#0d6efd'
        )
        figure.update_layout(
            title = f"<b>{title}</b>",
            title_font_family="sans-serif", 
            title_font_size = 18,
            title_font_color = "rgba(0, 0, 0, 0.7)",
            margin = dict( l = 20, r = 40, b = 20, t = 40, pad = 0, autoexpand = True),
            height = height,
            xaxis_title = '<b>'+x_title+'</b>',
            yaxis_title = '<b>'+y_title+'</b>',
            legend_title_text = title_legend,
            legend=dict(font=dict(size=legend_font_size,color="black"))
        )
        figure.update_traces(hovertemplate =hover_template,cliponaxis=False)
        figure.update_xaxes(tickfont=dict(size=tickfont_x),color='rgba(0, 0, 0, 0.8)',showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True) 
        figure.update_yaxes(tickfont=dict(size=tickfont_y),color='rgba(0, 0, 0, 0.8)',showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True)
        figure.update_layout(hovermode="x unified",hoverlabel=dict(font_size=size_text,font_family="sans-serif",bgcolor='rgba(255,255,255,0.75)'))
        if legend_orizontal == True:
            figure.update_layout(legend=dict(orientation="h",yanchor="bottom",xanchor="right",y=1.02,x=1))
        return figure
    
def tableDag(
            id = '',
            columnDefs = [],
            dataframe = pd.DataFrame(),
            defaultColDef = {"resizable": True, "sortable": True, "filter": True, "minWidth":100},
            theme = "ag-theme-balham",
            rules_col = [],
            dashGridOptions = {"domLayout": "autoHeight"},
            rowClassRules ={},
            column_size = "responsiveSizeToFit",
            style = {'font-size':15} 
):
    return dag.AgGrid(
                id=id,
                columnDefs=columnDefs,
                rowData=dataframe.to_dict("records"),
                columnSize = column_size,
                defaultColDef=defaultColDef,
                className = theme,
                rowClassRules=rowClassRules,
                style=style,
                #dashGridOptions=dashGridOptions,
                #columnDefs=columnDefs,
    ), 
def cardDivider(
    value = 1000,
    text = '',
    list_element = [
        {'value': 59, 'color': 'rgb(71, 214, 171)', 'label': '59%', "tooltip": "Docs - 14GB"},
        {'value': 35, 'color': 'rgb(3, 20, 26)', 'label': '35%'},
        {'value': 25, 'color': 'rgb(79, 205, 247)'},
    ]
):
    return dmc.Card(
                
                children=[
                dmc.Group([
                    dmc.Text( value ,style = {"fontSize": 18}, weight = 700),#25
                ], spacing='0.5rem', sx={'align-items': 'baseline'}),
                dmc.Text(text, size='md', color='blue',weight=500),
                dmc.Progress(
                    size='lg',
                    sections=list_element, 
                ),

                ],
                withBorder=True,
                shadow='xl',
                radius='md',
                #style = {'height':150}
            )

def table_agricola_recurso(dataframe = pd.DataFrame(), check = [], recursos = '', col ='CONSUMIDOR'):
     def colArea(df):
            df_area_agricola=pd.DataFrame()
            years=sorted(df['AÑO_CAMPAÑA'].unique())
            for year in years:
                df_year=df[df['AÑO_CAMPAÑA']==year]
                df_year=df_year.groupby(['CODCONSUMIDOR','CONSUMIDOR','CULTIVO','VARIEDAD','AREA_CAMPAÑA','AÑO_CAMPAÑA']).sum().reset_index()
                df_area_agricola=pd.concat([df_area_agricola,df_year])
            return df_area_agricola
     dff_area=colArea(dataframe)
     dff_pt=dff_area.groupby([col]).sum().reset_index()
     dff_pt=dff_pt.rename(columns={
                                        'Nitrógeno':'Nitrogeno',
                                        'Fósforo':'Fosforo',

                                       })
     print(check,type(check))
     dff_pt=dff_pt[[col,'AREA_CAMPAÑA']+check]
        ### CONSUMIDORES 
     if col == 'CONSUMIDOR':
          dff_lotes=dff_area.groupby([col]).sum().reset_index()
     else:
          dff_lotes=dff_area.groupby(['CONSUMIDOR',col]).sum().reset_index()
     dff_lotes=dff_lotes.rename(columns={
                                        'Nitrógeno':'Nitrogeno',
                                        'Fósforo':'Fosforo',

                                       })
     dff_lotes=dff_lotes[['CONSUMIDOR','AREA_CAMPAÑA']+check]
     if recursos == 'hectarea':
            columns=dff_pt.columns
            columns_lote=dff_lotes.columns
            dff_pt['AREA_CAMPAÑA']=dff_pt['AREA_CAMPAÑA'].astype('float64')
            dff_lotes['AREA_CAMPAÑA']=dff_lotes['AREA_CAMPAÑA'].astype('float64')
            for recurso in columns[2:]:
                dff_pt[recurso]=dff_pt[recurso]/dff_pt['AREA_CAMPAÑA']
            for recurso2 in columns_lote[2:]:
                dff_lotes[recurso2]=dff_lotes[recurso2]/dff_lotes['AREA_CAMPAÑA']
     dff_lotes=dff_lotes.round(1)
     dff_pt.loc['TOTAL',:]= dff_pt.sum(numeric_only=True, axis=0)      
     dff_pt=dff_pt.fillna('TOTAL')
     dff_pt=dff_pt.round(1)
     return dff_pt
def map_agricola_scatter(df = pd.DataFrame(),importe = 'SALDO_MEX', ubicacion = [-79.536047,-7.034728], zoom = 13, height = 300):
            fig = go.Figure()
            for lista_string,lote in zip(df['POLYGON'].unique(),df['CONSUMIDOR'].unique()):
                lote_df = df.query(f"CONSUMIDOR == '{lote}'")
                cultivo = lote_df['CULTIVO'].unique()[0]
                df['hover_cultivo'] = cultivo
                df['hover_lote'] = lote
                df['hover_variedad'] = lote_df['VARIEDAD'].unique()[0]
                df['hover_costo'] = lote_df[importe].sum()
                #df['hover_ha'] = lote_df['AREA_CAMPAÑA'].sum()
                lista_coord=eval(lista_string)
                fig.add_trace(go.Scattermapbox(
                    mode="lines",
                    lon=[coord[0] for coord in lista_coord],
                    lat=[coord[1] for coord in lista_coord],
                    fill='toself',
            
                    fillcolor=DICT_CULTIVOS_COLOR[cultivo],#
                    line=dict(color="black",width=2),##
                    #hovertext=lote,
                    name='',
                    customdata=np.stack((df['hover_cultivo'], df['hover_lote'],df['hover_variedad'],df['hover_costo']),axis = -1),#{y:$,.0f}
                    hovertemplate='<br><b>Lote: %{customdata[1]}</b><br><b>Cultivo: %{customdata[0]}</b><br><b>Variedad: %{customdata[2]}</b><br><b>Importe: %{customdata[3]:,.2f}</b>',
                    hoverlabel=dict(font_size=15,bgcolor=DICT_CULTIVOS_COLOR[cultivo])
                ))

                # Configurar el diseño del mapa
                fig.update_layout(
                    mapbox=dict(
                        center = dict(lon=ubicacion[0],lat=ubicacion[1]),#,-79.53234131
                        style = "open-street-map",
                        zoom = zoom
                    ),
                    showlegend = False
                )
                fig.update_layout(height = height, margin = dict(t=0, b=0, l=0, r=0))
            
                                
            return fig
def bar_(df = pd.DataFrame(), x = '', y = '', text = '', orientation = 'v', height = 400 ,
        title = '', space_ticked = 130, xaxis_title = '',yaxis_title = '', showticklabel_x = True, 
        showticklabel_y = True , color_dataframe= '#145f82',list_or_color = None, customdata = [],
        template = 'plotly_white', size_tickfont = 11, title_font_size = 20, clickmode = False,
        ticklabel_color = 'rgba(0, 0, 0, 0.7)',plot_bgcolor = 'white', paper_bgcolor = 'white',left = 40
    ):  
        #print(df)
        figure = go.Figure()
        if len(customdata)>0:
            custom = create_stack_np(dataframe = df, lista = customdata)
            hover_aditional_datacustom = create_hover_custom(lista = customdata)
        else:
            custom = []
            hover_aditional_datacustom = ""
            
        if orientation == 'h':
            value_left = space_ticked
            value_bottom = 40
            hover = '<br>'+y+': <b>%{y}</b><br>'+x+': <b>%{x:,.2f}</b>'+hover_aditional_datacustom
        elif orientation == 'v': 
            value_left = 60
            value_bottom = space_ticked
            hover = '<br>'+x+': <b>%{x}</b><br>'+y+': <b>%{y:,.2f}</b>'+hover_aditional_datacustom
            
        if  type(list_or_color) == list:
                value_colors =  list_or_color  
        elif type(list_or_color) == dict:
            #print(df.columns)
            #if 'CULTIVO' in df.columns:
            #    print('w')
            #    value_colors = [list_or_color[i] for i in df['CULTIVO']]
            #else :
                try :
                    value_colors = [list_or_color[i] for i in df[x]]
                except:
                    value_colors = [list_or_color[i] for i in df[y]]
        else :
            value_colors = color_dataframe
        figure.add_trace(
            go.Bar(y = df[y],
                   x = df[x],   
                   text = df[text],
                   
                   orientation = orientation,
                   textposition = 'outside',
                   texttemplate =' %{text:.2s}',
                   marker_color = [DICT_CULTIVOS_COLOR[i]for i in df[color_dataframe]] if color_dataframe == 'CULTIVO' else value_colors,    
                  # marker_color = value_colors,
                   opacity=0.9,
                   name = '',
                   customdata = custom,
                   hovertemplate=hover,
                   #hoverinfo='none',
                   hoverlabel=dict(font_size=13,bgcolor='rgba(255,255,255,0.75)',font_family="sans-serif",font_color = 'black'),
                   cliponaxis=False,
            )
        )
        
        figure.update_layout(
                template = template,
                title={'text': f"<b>{title}</b>",'y':0.97,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                #title_font_color="#145f82",
                xaxis_title='<b>'+xaxis_title+'</b>',
                yaxis_title='<b>'+yaxis_title+'</b>',
                legend_title="",
                #font=dict(size=15,color="black"),
                title_font_family="sans-serif", 
                title_font_size = title_font_size,
                title_font_color = "rgba(0, 0, 0, 0.7)",
                height = height, 
                
        )
        if clickmode == True:
            figure.update_layout(clickmode='event+select')
        size_list = len(df[x].unique()) if orientation == 'v' else len(df[y].unique())
        figure.update_xaxes(tickfont=dict(size=size_tickfont),color=ticklabel_color,showticklabels = showticklabel_x,title_font_family="sans-serif",title_font_size = 13,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
        figure.update_yaxes(tickfont=dict(size=size_tickfont),color=ticklabel_color,showticklabels = showticklabel_y,title_font_family="sans-serif",title_font_size = 13,automargin=True)  
        figure.update_layout(autosize=True,margin=dict(l = left, r = 40, b= 40, t = 50, ) )#
        figure.update_layout(plot_bgcolor = plot_bgcolor, paper_bgcolor = paper_bgcolor)
        if  size_list== 1:
            figure.update_layout(bargap=0.7)
        elif size_list== 2:
            figure.update_layout(bargap=0.4)
        elif size_list== 3:
            figure.update_layout(bargap=0.3)

        return figure

def pie_(df = pd.DataFrame(),label_col = '', 
             value_col = '',list_or_color = None, dict_color = None,
             title = '', textinfo = 'percent+label+value' , textposition = 'inside',
             height = 300, showlegend = True, color_list = [], textfont_size = 12,
             plot_bgcolor = 'white', paper_bgcolor = 'white',top = 40
             
    ):
        if dict_color != None:
            marker_colors = [dict_color[i]for i in df[label_col]] if type(dict_color) == dict else list_or_color
        elif color_list != None  and dict_color == None:
            marker_colors = color_list
        elif color_list == None  and dict_color == None:
              marker_colors = px.colors.qualitative.Plotly 
        figure = go.Figure()
        figure.add_trace(
            go.Pie(labels=df [label_col],values=df[value_col],
                marker_colors = marker_colors,
                #hovertemplate='<br><b>'+label_col+': %{labels}</b><br><b>'+value_col+': %{value:,.2f}</b>'
                hoverlabel=dict(font_size=15,bgcolor="white"),
                hovertemplate = "<b>%{label}</b> <br>Porcentaje:<b> %{percent} </b></br>Importe: <b>%{value}</b>",
                name='',
                )
        )    

        figure.update_layout(
            title={'text': f"<b>{title}</b>",'y':0.97,'x':0.5,'xanchor': 'center','yanchor': 'top'},
            title_font_family="sans-serif", 
            title_font_size = 18,
            title_font_color = "rgba(0, 0, 0, 0.7)",
        
        )
        figure.update_traces(textposition = textposition, textinfo = textinfo)
        figure.update_traces(hoverinfo='label+percent+value', textfont_size = textfont_size,marker=dict(line=dict(color='#000000', width=1)))
        figure.update_layout(height = height,margin = dict(t=top, b=30, l=30, r=30),showlegend = showlegend)
        figure.update_layout(plot_bgcolor = plot_bgcolor, paper_bgcolor = paper_bgcolor)
        return figure
                 
agricola_df = pd.read_parquet('agricola.parquet', engine='pyarrow')
#df = df.drop(["NCULTIVO","POLYGON","AREA_PLANIFICADA","CODSIEMBRA","CODCAMPAÑA","SEMANA"], axis=1)
#df = df[df['AÑO_CAMPAÑA']>2020]



class DashProduccion:
    #def __init__(self, ip: str, token :str):#, data_login: dict
        #self.ip = ip
        #self.token = token
    def ejecucion_campania(self, code: str):
        
        app = DjangoDash(
                name = code,
                external_stylesheets = EXTERNAL_STYLESHEETS, 
                external_scripts = EXTERNAL_SCRIPTS,
        )
        app.layout = \
        Content([
             Grid([
                 Col([dmc.Title("Ejecución de Campaña")],size=3),
                 Col([
                     dmc.MultiSelect(
                        #data=["React", "Angular", "Svelte", "Vue"],
                        id="campania",
                        label = "Campaña",
                        placeholder = "Todos",
                        searchable=True,
                        nothingFound="Opción no encontrada",
                        #value=sorted(df['AÑO_CULTIVO'].unique()),
                        data=[{'label': i, 'value': i} for i in sorted(df['AÑO_CULTIVO'].unique())],
                        size="sm", 
                    ),
                 ],size=3),
                 
                 Col([
                    dmc.Select(
                        label="Variedad",
                        placeholder="Todos",
                        id="variedad",
                        value = None,
                        data= [],
                        clearable=True
                    )
                ],size=3),
                 Col([
                     dmc.Select(
                        label="Lotes",
                        placeholder="Todos",
                        id="lote",
                        value = None,
                        data= [],
                        clearable=True
                    )
                 ],size=3),
                 
                 Col([
                    #html.Div(id = "graph-recursos")
                    cardGraph(id ="graph-recursos" )
                 ],size=9)
                 
             ]),
        html.Div(id='notifications-update-data'),
        dcc.Store(id='data-values'),    
        ])
        @app.callback(
            Output('variedad','data'),
            Output('lote','data'),
            Output("data-values","data"),
            Output("notifications-update-data","children"),
            Input('campania','value'),
            Input('variedad','value'),
            Input('lote','value'),
        )
        def update_data(*args):
            if validar_all_none(variables = args) == True:
                dff = df.copy()
            else:
                 dff = df.query(dataframe_filtro(values= args ,columns_df=['AÑO_CULTIVO',"VARIEDAD","CONSUMIDOR"]))
            return [
                [{'label': i, 'value': i} for i in sorted(dff['VARIEDAD'].unique())],
                [{'label': i, 'value': i} for i in sorted(dff['CONSUMIDOR'].unique())],
                dff.to_dict('series'), 
                notification_update_show(text=f'Se cargaron {len(dff)} filas',title='Update')
            ]
            
        @app.callback(
            Output("graph-recursos","figure"),
            Input("data-values","data"),
        )
        def update_graph(data):
            df = pd.DataFrame(data)
            
            tipo_list = df["TIPO"].unique()
            fig = go.Figure()#make_subplots(rows=len(tipo_list), cols=1, shared_yaxes=True)
            #div = Grid([
            #    Col([
            #        cardGraph(
            #            figure = px.line(df[df["TIPO"]==i].groupby(["week","AÑO_CULTIVO"])[["CANTIDAD"]].sum().reset_index(), x="week", y="CANTIDAD", color="AÑO_CULTIVO", title=i, template="plotly_white")
            #        ),
            #    ]) 
            #    for i in tipo_list
            #])
            for recurso,i in zip(tipo_list,range(len(tipo_list))):
                fig.add_trace(px.line(df[df["TIPO"]==recurso].groupby(["week","AÑO_CULTIVO"])[["CANTIDAD"]].sum().reset_index(), x="week", y="CANTIDAD", color="AÑO_CULTIVO", title=recurso, template="plotly_white"),i+1,1) 
            return fig
        return app
    
    def agricola_ejecucion(self, code: str):
        app = DjangoDash(
                name = code,
                external_stylesheets = EXTERNAL_STYLESHEETS, 
                external_scripts = EXTERNAL_SCRIPTS,
        )
        campaña_list=sorted(agricola_df['AÑO_CULTIVO'].unique())
        app.layout =  \
        Content([
            html.Div([dmc.Modal(title = '', id = f"modal_{i}", fullScreen=True, zIndex=10000, size= "85%" )for i in ['line-recurso-agricola']]),
            #DRAWER FILTER
            dmc.Drawer(
                title="Filtros",
                id="drawer-simple",
                padding="md",
                zIndex=10000,
                children=[
                    dmc.RadioGroup(
                        [dmc.Radio("Fecha", value="FECHA"),dmc.Radio("Semana", value="week")],
                        id="radio-serie-tiempo-ejex-recurso",
                        value="week",
                        label="Eje X - Serie de Tiempo",
                        size="sm",
                        mt=10,
                    ),
                    dmc.RadioGroup(
                        [dmc.Radio(label='Por Cantidad', value='cantidad'),dmc.Radio(label='Por Hectárea', value='hectarea')],
                        id="radio-serie-tiempo-ejey-recurso",
                        value="cantidad",
                        label="Medida",
                        size="sm",
                        mt=10,
                    ),
                ]
            ),
            Grid([
                #COL 1
                Col([
                dmc.ActionIcon(
                    DashIconify(icon="feather:filter"), 
                    color="blue", 
                    variant="default",
                    id="btn-filter",
                    n_clicks=0,
                    mb=10,
                    style = {}
                ),
                ],size= 1), 
                Col([
                dmc.Title("Informe de Ventas", align="center")
                ],size= 11), 
                # COL 2
                Col([
                    dmc.Select(
                        label="Campaña-Cultivo",
                        placeholder="Todos",
                        id="select-campania",
                        value = campaña_list[-1],
                        data= [{'label': i, 'value': i} for i in campaña_list],
                        clearable=False
                    )
                ],size= 2),
                Col([
                    dmc.Select(
                        label="Variedades",
                        placeholder="Todos",
                        id="select-variedad",
                    )
                ],size= 2),
                Col([
                    dmc.Select(
                        label="Lotes",
                        placeholder="Todos",
                        id="select-lote",
                    )
                ],size= 2),
                Col([
                    html.Div(id = 'label-range-inicio-campania',style={'padding-top':'35px'}),
                ],size= 3),
                Col([
                    html.Div(id = 'label-range-fin-campania',style={'padding-top':'35px'})
                ],size= 3),
                Col([
                    card_segment(id_='line-recurso-agricola',id_segmented='segmented-recurso',height=400)
                ]),
                Col([
                    dmc.Tabs(
                        [
                            dmc.TabsList(
                                [
                                    dmc.Tab("Variedad", value="Variedad"),
                                    dmc.Tab("Lote", value="Lote"),
                                    
                                ]
                            ),
                            dmc.TabsPanel(html.Div( id = 'table-variedad'), value="Variedad"),
                            dmc.TabsPanel(html.Div( id = 'table-lote'), value="Lote"),
                            
                        ],
                        value="Variedad",
                    )
                ])
            ]),
            html.Div(id='notifications-update-data'),
            dcc.Store(id='data-values'),
        ])

        app.clientside_callback(
            """
            function(n_clicks) {
                return true;
            }
            """,
            Output("drawer-simple", "opened"),
            Input("btn-filter", "n_clicks"),
            prevent_initial_call=True,
        )
        @app.callback(
                  #Output('select-campania','data'),
                  Output('select-variedad','data'),
                  Output('select-lote','data'),
                  Output('label-range-inicio-campania','children'), 
                  Output('label-range-fin-campania','children'), 
                  #Output('checklist-comercial-tipoventa','options'),
                  #Output('checklist-comercial-tipoventa','value'),  
                  Output("data-values","data"),
                  Output("segmented-recurso",'data'),
                  Output("segmented-recurso",'value'),
                  Output("notifications-update-data","children"),
                  Input('select-campania','value'),
                  Input('select-variedad','value'),
                  Input('select-lote','value'),
                 )
        def update_filter_agricola_recurso(*args):#select_campania,select_variedad,select_lote
            if validar_all_none(variables = args) == True:
                df=agricola_df.copy()
            else:
            #list_variables=create_list_var(select_campania,select_variedad,select_lote)
                df=agricola_df.query(dataframe_filtro(values=args,columns_df=['AÑO_CULTIVO','VARIEDAD','CONSUMIDOR']))
            """convirtiendo el dataframe a json"""
            
            #select_out_anio = [{'label': i, 'value': i} for i in sorted(df['AÑO_CULTIVO'].unique())]
            select_out_variedad = [{'label': i, 'value': i} for i in sorted(df['VARIEDAD'].unique())]
            select_out_lote = [{'label': i, 'value': i} for i in df['CONSUMIDOR'].unique()]
            
            segmented_recurso=df['TIPO'].unique()
            value_segmented_recurso=segmented_recurso[0]
            
            parametros_datepicker = get_parameters_datepicker(df=df,col_inicio='FECHAINICIO_CAMPAÑA',col_fin='FECHAFIN_CAMPAÑA')
            return [
                    #select_out_anio,
                    select_out_variedad, select_out_lote, 
                    dmc.Badge(f"Inicio Campaña: {parametros_datepicker[0]}",variant='dot',color='lime', size='lg',radius="lg",pt=0),
                    dmc.Badge(f"Fin Campaña: {parametros_datepicker[1]}",variant='dot',color='lime', size='lg',radius="lg"),
                    #DataDisplay.text(id='inicio',text=),
                    #DataDisplay.text(id='fin',text=),
                    df.to_dict('series'),
                    segmented_recurso,value_segmented_recurso,
                    notification_update_show(text=f'Se cargaron {len(df)} filas',title='Update'),
            ]
        @app.callback(
            Output('line-recurso-agricola','figure'),
            Output('table-variedad','children'),
            Output('table-lote','children'),
            Input("data-values","data"),
            Input("radio-serie-tiempo-ejex-recurso","value"),
            Input("radio-serie-tiempo-ejey-recurso","value"),
            #Input("checklist-recurso-agricola","value"),
            Input("segmented-recurso","value"),
            
            
        )
        def update_graph_recurso_agricola(data,radio_ejex,radio_ejey,segmented_recurso):#checklist_recursos
            df = pd.DataFrame(data)
            list_tipo = list(df["DSCVARIABLE"].unique())
            df_ha_sembrado=df.groupby(['CONSUMIDOR',radio_ejex,'SEMANA','CULTIVO','VARIEDAD','AÑO_FECHA','AÑO_CAMPAÑA','AREA_CAMPAÑA','AÑO_CULTIVO'])[['CANTIDAD']].sum().reset_index()
            df_ha_total=df_ha_sembrado.groupby(['CONSUMIDOR',radio_ejex,'SEMANA','VARIEDAD','AÑO_FECHA','AÑO_CAMPAÑA','AÑO_CULTIVO'])[['AREA_CAMPAÑA']].sum().reset_index()
            df_ha_st=df_ha_total.groupby([radio_ejex,'SEMANA','AÑO_FECHA','AÑO_CAMPAÑA','AÑO_CULTIVO'])[['AREA_CAMPAÑA']].sum().reset_index()
            df_ha_st=df_ha_st[[radio_ejex,'AREA_CAMPAÑA']]
            
            

            df_graph=df.groupby(['DSCVARIABLE','TIPO',radio_ejex,'AÑO_FECHA','SEMANA'])[['CANTIDAD']].sum().reset_index()
            df_graph=df_graph.merge(df_ha_st, how='inner', left_on=[radio_ejex], right_on=[radio_ejex])


            df_graph.loc[df_graph.DSCVARIABLE == 'Nitrógeno','DSCVARIABLE'] =  'Nitrogeno'  
            df_graph.loc[df_graph.DSCVARIABLE == 'Fósforo','DSCVARIABLE'] =  'Fosforo'  
            #df_graph=df_graph[df_graph['DSCVARIABLE'].isin(check)]
            df_graph['CANTXHA']=df_graph['CANTIDAD']/df_graph['AREA_CAMPAÑA']
            if radio_ejey == 'hectarea':
                df_graph['CANTIDAD']=df_graph['CANTIDAD']/df_graph['AREA_CAMPAÑA']
                
            df_segmented = df_graph[df_graph['TIPO'] == segmented_recurso]
            #df_segmented = df_segmented[df_segmented['DSCVARIABLE'].isin(checklist_recursos)]
            df_segmented = df_segmented.sort_values(by=[radio_ejex,'AÑO_FECHA','SEMANA'],ascending=True)
            
            hover_size = hoversize_recurso_agricola(recurso = segmented_recurso)
            ############################################
            df_pivot=df.pivot_table(index=('CULTIVO','VARIEDAD','CODCONSUMIDOR','CONSUMIDOR','CODSIEMBRA','CODCAMPAÑA','FECHA','AÑO_CAMPAÑA','AREA_CAMPAÑA','AREA_PLANIFICADA','week','AÑO_FECHA','SEMANA','AÑO_CULTIVO'),values=('CANTIDAD'),columns=('DSCVARIABLE'),aggfunc='sum').fillna(0).reset_index()
            #df_pivot['AÑO_CAMPAÑA']=df_pivot['AÑO_CAMPAÑA'].astype(object)
            variedad_table=table_agricola_recurso(dataframe= df_pivot,check = list_tipo,recursos  = radio_ejey,col = 'VARIEDAD')
            lote_table=table_agricola_recurso(dataframe= df_pivot,check = list_tipo,recursos = radio_ejey,col = 'CONSUMIDOR')
            def orderX(x,df):
                if x == 'week':
                    order={'week':sorted(df['week'].unique()),'DSCVARIABLE': sorted(df['DSCVARIABLE'].unique())}
                else: 
                    order={}
                return order
            if segmented_recurso == 'Maquinaria':
                ejey_ = 'Horas'
            elif segmented_recurso == 'Insumos':
                ejey_ = 'Unidades'
            elif segmented_recurso == 'Mano de obra':
                ejey_ = 'Jornales'
            else :
                ejey_ = 'Metros Cúbicos'
            #'Insumos' 'Mano de obra' 'Riego'
            print(df_segmented)
            return [
                line_(
                    df = df_segmented, x = radio_ejex, y = "CANTIDAD", color="DSCVARIABLE", height = 370,
                    y_title = ejey_,title_legend = '', order = orderX(x=radio_ejex,df=df_segmented ),#order_st_agricola_ejex(df = df_segmented, ejex = radio_ejex, var_col = "DSCVARIABLE")
                    title = segmented_recurso, discrete_color = DIC_RECURSOS_AGRICOLA, custom_data = ["CANTXHA"], hover_template = hover_size[0], size_text = 15,#hover_size[1]
                    legend_font_size  = 17,tickfont_x = 15, tickfont_y=15),
                tableDag(id='variedad', 
                 columnDefs=[{"field": i, "type": "rightAligned"} for i in variedad_table.columns],
                 dataframe= variedad_table,
                 rules_col=['TOTAL','VARIEDAD'],
                 theme='ag-theme-alpine',
                ),
                tableDag(id='lote', 
                 columnDefs=[{"field": i, "type": "rightAligned"} for i in lote_table.columns],
                 dataframe= lote_table,
                 rules_col=['TOTAL','CONSUMIDOR'],
                 theme='ag-theme-alpine',
                 
                ),
            ]
        
        opened_modal(app = app, id="line-recurso-agricola",height_modal=800)
        return app
    
    def agricola_costos(self, code: str):
        app = DjangoDash(
                name = code,
                external_stylesheets = EXTERNAL_STYLESHEETS, 
                external_scripts = EXTERNAL_SCRIPTS,
        )
        df_costos_agricola_default= pd.read_parquet('costos.parquet', engine='pyarrow')
        anio_campania = sorted(df_costos_agricola_default['AÑO_CAMPAÑA'].unique())
        app.layout =  \
        Content([
            html.Div([dmc.Modal(title = '', id = f"modal_{i}", fullScreen=True, zIndex=10000, size= "85%" )for i in ['bar-costos-cultivo','bar-costos-variedad','pie-costos-tipo','map-costos-lt','bar-costos-lote']]),
            dmc.Drawer(
                title="Filtros",
                id="drawer-simple",
                padding="md",
                zIndex=10000,
                children=[
                    dmc.RadioGroup(
                        [dmc.Radio(label='Costos', value='totales'),
                        dmc.Radio(label='Costos por Ha', value='por ha')],
                        id="radio-ha-costos-agricola",
                        value="totales",
                        label="Tipo de Costo",
                        size="sm",
                        mt=10,
                    ),
                    dmc.RadioGroup(
                        [dmc.Radio(label='PEN', value='SALDO_MOF'),dmc.Radio(label='USD', value='SALDO_MEX')],                       
                        id="radio-costos-moneda",
                        value="SALDO_MEX",
                        label="Tipo de Moneda",
                        size="sm",
                        mt=10,
                    ),
                ]
            ),
            Grid([
                #COL 1
                Col([
                    dmc.ActionIcon(
                        DashIconify(icon="feather:filter"), 
                        color="blue", 
                        variant="default",
                        id="btn-filter",
                        n_clicks=0,
                        mb=10,
                        style = {}
                    ),
                ],size= 1), 
                Col([
                    dmc.Title("Costos", align="center")
                ],size= 5),
                Col([
                    dmc.Select(
                        label="Año de Campaña",
                        placeholder="Todos",
                        id="select-anio",
                        clearable=True,
                        value=anio_campania[-1]
                    )
                ],size= 2),
                Col([
                    dmc.Select(
                        label="Cultivo",
                        placeholder="Todos",
                        id="select-cultivo",
                    )
                ],size= 2),
                Col([
                    dmc.Select(
                        label="Variedad",
                        placeholder="Todos",
                        id="select-variedad",
                    )
                ],size= 2),
                
                #graphs
                Col([
                    cardGraph(id ="bar-costos-cultivo" )
                ],size=4),
                Col([
                    cardGraph(id ="bar-costos-variedad" )
                ],size=4),
                
                Col([
                    Grid([
                        Col([
                            html.Div(id='card-costos-total')
                        ]),
                        Col([
                            html.Div(id='card-costos-ha')
                        ],size=6),
                        Col([
                            html.Div(id='card-costos-cultivo')
                        ],size=6),
                        Col([
                            cardGraph(id ="pie-costos-tipo" )
                        ],size=12),
                    ])
                ],size=4),
                #SEGUNDO ROW
                
                Col([
                    cardGraph(id ="map-costos-lt" )
                ],size=5),
                Col([
                    cardGraph(id ="bar-costos-lote" )
                ],size=7),
                
            ]),
            html.Div(id='notifications-update-data'),
            dcc.Store(id='data-values'),
        ])
        app.clientside_callback(
            """
            function(n_clicks) {
                return true;
            }
            """,
            Output("drawer-simple", "opened"),
            Input("btn-filter", "n_clicks"),
            prevent_initial_call=True,
        )
        @app.callback(
                  Output('select-anio','data'),
                  Output('select-cultivo','data'),
                  Output('select-variedad','data'),
                  #Output('checklist-tipo-costos','options'),
                  #Output('checklist-tipo-costos','value'),   
                  Output("data-values","data"),
                  Output("notifications-update-data","children"),
                  
                  Input('select-anio','value'),
                  Input('select-cultivo','value'),
                  Input('select-variedad','value'),
                  
                 )
        def update_filter_agricola_recurso(*args):#select_anio,select_cultivo,select_variedad
            if validar_all_none(variables = args) == True:
                df=df_costos_agricola_default.copy()
            else:
            #list_variables=create_list_var(select_anio,select_cultivo,select_variedad)
                df=df_costos_agricola_default.query(dataframe_filtro(values=args,columns_df=['AÑO_CAMPAÑA','CULTIVO','VARIEDAD']))
            #select_out_variedad
            select_out_anio=[{'label': i, 'value': i} for i in df['AÑO_CAMPAÑA'].unique()]
            select_out_cultivo=[{'label': i, 'value': i} for i in df['CULTIVO'].unique()]
            select_out_variedad=[{'label': i, 'value': i} for i in df['VARIEDAD'].unique()]
            return [
                select_out_anio,select_out_cultivo,select_out_variedad,
                #out_check,value_out_check,
                df.to_dict('series'),
                notification_update_show(text=f'Se cargaron {len(df)} filas',title='Update'),
            ]
        @app.callback(
        Output('card-costos-total','children'),
        Output('card-costos-ha','children'),
        Output('card-costos-cultivo','children'),
        Output('bar-costos-cultivo','figure'),
        Output('bar-costos-variedad','figure'),
        Output('pie-costos-tipo','figure'),
        Output('map-costos-lt','figure'),
        Output('bar-costos-lote','figure'),
        Input("data-values","data"),
        Input("radio-ha-costos-agricola","value"),
        Input("radio-costos-moneda","value"),
        #Input("checklist-tipo-costos","value"),
        
        )
        def update_graph_recurso_agricola(data, radio_ha_costos, radio_moneda):#, checklist_tipo_costos
            simbolo = "S/" if radio_moneda == 'SALDO_MOF' else "$"
            df = pd.DataFrame(data)
            #costos_df=df[df['TIPO'].isin(checklist_tipo_costos)]
            
            costos_distribuido_df = df.groupby(['IDCONSUMIDOR','CONSUMIDOR','CULTIVO','VARIEDAD','AREA_CAMPAÑA'])[[radio_moneda]].sum().reset_index()
            #costos_df_pivot = costos_df.pivot_table(index = ['CODCULTIVO','CULTIVO','VARIEDAD','AREA_CAMPAÑA','IDCONSUMIDOR','CONSUMIDOR','CODSIEMBRA','CODCAMPAÑA','AÑO_CAMPAÑA'], values = radio_moneda, columns = 'TIPO',aggfunc='sum').fillna(0).reset_index()

            #costos_cultivo_df = costos_df.groupby(['CULTIVO'])[[radio_moneda]].sum().reset_index()
            total_card_1 = "{:,.2f}".format(costos_distribuido_df[radio_moneda].sum())
            list_cultivo = costos_distribuido_df['CULTIVO'].unique()
            total_costos_dict = create_dict_of_list(costos_distribuido_df,col=radio_moneda,dict_color = DICT_CULTIVOS_COLOR,list_partidas=list_cultivo,pivot=False,col_='CULTIVO')
            ################
            #ha_cultivo_df = costos_df_pivot.groupby(['CULTIVO'])[['AREA_CAMPAÑA']].sum().reset_index()
            total_card_2 = "{:,.2f}".format(costos_distribuido_df['AREA_CAMPAÑA'].sum())
            list_cultivo_ha=costos_distribuido_df['CULTIVO'].unique()
            total_dict_ha = create_dict_of_list(costos_distribuido_df,col='AREA_CAMPAÑA',dict_color = DICT_CULTIVOS_COLOR,list_partidas=list_cultivo_ha,pivot=False,col_='CULTIVO')
            ###########
            cotos_por_ha = "{:,.2f}".format((costos_distribuido_df[radio_moneda].sum())/(costos_distribuido_df['AREA_CAMPAÑA'].sum()))
            
            
            cultivo_df = create_dataframe_costos_tipo(df = costos_distribuido_df, category_col = ['CULTIVO'], numeric_col = [radio_moneda,'AREA_CAMPAÑA'], radio_tipo_costo = radio_ha_costos)
            variedad_df = create_dataframe_costos_tipo(df = costos_distribuido_df, category_col = ['VARIEDAD','CULTIVO'], numeric_col = [radio_moneda,'AREA_CAMPAÑA'], radio_tipo_costo = radio_ha_costos)
            lote_df = create_dataframe_costos_tipo(df = costos_distribuido_df, category_col = ['CONSUMIDOR','CULTIVO'], numeric_col = [radio_moneda,'AREA_CAMPAÑA'], radio_tipo_costo = radio_ha_costos)
        
            pie_tipo_gasto = df.groupby('TIPO')[[radio_moneda]].sum().reset_index()
            if radio_ha_costos == 'por ha':
                pie_tipo_gasto[radio_moneda] = pie_tipo_gasto[radio_moneda]/costos_distribuido_df['AREA_CAMPAÑA'].sum()
                pie_tipo_gasto[radio_moneda] = pie_tipo_gasto[radio_moneda].round(2)
                
            try:
                df_map=df[df['POLYGON'].notnull()]
                df_map_polygon=df_map.groupby(['CONSUMIDOR','CULTIVO','VARIEDAD','POLYGON'])[['AREA_CAMPAÑA',radio_moneda]].sum().reset_index()
                map_graph = map_agricola_scatter(df = df_map_polygon, height = 300, importe = radio_moneda)
            except:
                map_graph = go.Figure(layout=dict(height=300,annotations=[dict(text=f"<b>Sin coordenadas de los Lotes </b>", showarrow=False)],xaxis=dict(showgrid=False, zeroline=False, visible=False),yaxis=dict(showgrid=False, zeroline=False, visible=False))) 
                
            return [
                cardDivider(value = f"{simbolo} {total_card_1}",text='Costos Totales',list_element=total_costos_dict),
                cardDivider(value = f"{total_card_2} ha",text='Hectáreas Sembradas',list_element=total_dict_ha),
                cardDivider(value = f"{simbolo} {cotos_por_ha}",text='Costo por Hectárea',list_element=[{'value': 100, 'color': "rgb(51, 102, 204)", 'label': '100%', "tooltip": "Costo por Hectárea"}]),
                bar_(df = cultivo_df, x = radio_moneda , y = 'CULTIVO', text= radio_moneda, orientation = 'h', height = 475, title = 'Costos por Cultivo', space_ticked = 100,xaxis_title = simbolo,yaxis_title = 'CULTIVO',list_or_color=DICT_CULTIVOS_COLOR,customdata=['AREA_CAMPAÑA']),#
                bar_(df = variedad_df, x = radio_moneda, y = 'VARIEDAD', text= radio_moneda, orientation = 'h', height = 475, title = 'Costos por Variedad', space_ticked = 100,xaxis_title = simbolo,yaxis_title = 'VARIEDAD',color_dataframe='CULTIVO',customdata=['AREA_CAMPAÑA','CULTIVO']),#
                pie_(df = pie_tipo_gasto, title = 'Tipo de Costo',label_col = 'TIPO', value_col = radio_moneda, height = 250, dict_color = DICT_TIPO_COSTO,top=20),
                map_graph,
                bar_(df = lote_df, x = 'CONSUMIDOR', y = radio_moneda, text= radio_moneda, orientation = 'v', height = 290, title = 'Costos por Lote', space_ticked = 30,xaxis_title = '',yaxis_title = simbolo, showticklabel_x=False,color_dataframe='CULTIVO',customdata=['AREA_CAMPAÑA','CULTIVO']),
            ]
        for i in ['bar-costos-cultivo','bar-costos-variedad','pie-costos-tipo','map-costos-lt','bar-costos-lote']:
            opened_modal(app = app, id=i,height_modal=800) 
        return app
    