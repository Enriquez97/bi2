import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go

def fields_columns(columns = []):
    list_ = []
    cols_ = ['Inventario Valorizado dolares','Inventario Valorizado soles','Precio Unitario','STOCK','Consumo Promedio Mensual','TI']
    for col in columns:
        if col in cols_:
            
            list_.append({
                "field": col,"cellStyle": {'font-size': 11},
                "type": "rightAligned", "cellDataType":"number",
                "valueFormatter": {"function": "params.value == null ? '' :  d3.format(',.2f')(params.value)"},
                        })
        elif col == 'Meses de Inventario':
            list_.append({
                "field": col,"cellStyle": {'font-size': 11},
                "type": "rightAligned", "cellDataType":"number",
                "valueFormatter": {"function": "params.value == null ? 'NO ROTA' :  d3.format(',.2f')(params.value)"},
            })
        else:
            list_.append({"field": col,"cellStyle": {'font-size': 11},"type": "rightAligned"})

    return list_

def validar_all_none(variables=()):
    contador = 0
    for i in variables:
        if i == None:
            contador = contador +1
    return True if len(variables) == contador else False

def dataframe_filtro(values=[],columns_df=[]):
   query = ""
   for value, col in zip(values,columns_df):
        if value != None:
            if type(value) == int:
                text=f"`{col}` == {value}"
            elif type(value) == str:
                text=f"`{col}` == '{value}'"
            elif type(value) == list:
                text=f"`{col}` in {value}"
            query += text + " and "
            
   return query[:-5]

def bar_ver(df = None, height = 400 , x = '',y = '',name_x = '',name_y = '',color = '#3aa99b', title = '',showticklabels_x = True, botton_size = 30 , template = 'plotly_white'):

    fig = go.Figure()
    #'Meses Inventario','Inventario Valorizado'
    fig.add_trace(go.Bar(
    x = df[x],
    y = df[y],
    name = '',
    cliponaxis=False,
    marker=dict(color = color,cornerradius=15),
    hovertemplate ='<br>'+name_x+': <b>%{x}</b><br>'+name_y+': <b>%{y:,.1f}</b>',hoverlabel=dict(font_size=13,bgcolor="white"),
    text=df[y],
    texttemplate='%{text:.2s}',
    textposition = "outside",
    ))
    
    fig.update_layout(
        #legend=dict(orientation="v"),
        #'<b>'+xaxis_title+'</b>'
        yaxis=dict(
            title=dict(text='<b>'+name_y+'</b>'),
            side="left",
            #range=[0, df['Meses Inventario'].max()]
        ),
        
        xaxis_title='<b>'+name_x+'</b>',
    )
    
    fig.update_layout(
        title = f"<b>{title}</b>",
        title_font_family="sans-serif", 
        title_font_size = 14,
        height = height,
        template = template
        #title_text="STOCK VALORIZADO Y NRO ITEMS POR MES Y AÑO",
    )
    fig.update_xaxes(tickfont=dict(size=14),showticklabels = showticklabels_x,title_font_family="sans-serif",title_font_size = 14,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
    fig.update_yaxes(tickfont=dict(size=14),showticklabels = True,title_font_family="sans-serif",title_font_size = 14,automargin=True)  
    fig.update_layout(yaxis_tickformat = ',',bargap=0.40,)#bargroupgap=0.1
    if botton_size == None:
        fig.update_layout(margin=dict(r = 20, t = 20,l=40))
    else:
        fig.update_layout(margin=dict(r = 20, t = 20,l=40, b= botton_size))
    return fig

def bar_hor(df = None, height = 350 , x = '',y = '',name_x = '',name_y = '',color = '#3aa99b', title = '', template = 'plotly_white'):

    fig = go.Figure()
    #'Meses Inventario','Inventario Valorizado'
    fig.add_trace(go.Bar(
    x = df[x],
    y = df[y],
    name = '',
    cliponaxis=False,
    marker=dict(color = color,cornerradius=15),
    hovertemplate ='<br>'+name_y+': <b>%{y}</b><br>'+name_x+': <b>%{x:,.1f}</b>',hoverlabel=dict(font_size=13,bgcolor="white"),
    orientation='h'
    ))
    
    fig.update_layout(
        #legend=dict(orientation="v"),
        #'<b>'+xaxis_title+'</b>'
        yaxis=dict(
            title=dict(text='<b>'+name_y+'</b>'),
            side="left",
            #range=[0, df['Meses Inventario'].max()]
        ),
        
        xaxis_title='<b>'+name_x+'</b>',
    )
    
    fig.update_layout(
        title = f"<b>{title}</b>",
        title_font_family="sans-serif", 
        title_font_size = 14,
        height = height,
        template = template
        #title_text="STOCK VALORIZADO Y NRO ITEMS POR MES Y AÑO",
    )
    fig.update_xaxes(tickfont=dict(size=11),showticklabels = True,title_font_family="sans-serif",title_font_size = 12,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
    fig.update_yaxes(tickfont=dict(size=11),showticklabels = True,title_font_family="sans-serif",title_font_size = 12,automargin=True)  
    #fig.update_layout(yaxis_tickformat = ',')
    fig.update_layout(margin=dict(r = 20, b = 30, t = 20,l =50))
    return fig

def pie_(df = pd.DataFrame(),label_col = '', 
             value_col = '',list_or_color = None, dict_color = None,
             title = '', textinfo = 'percent+label+value' , textposition = 'inside',
             height = 300, showlegend = True, color_list = [], textfont_size = 12, hole = 0,
             template = 'plotly_white'
             
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
                hovertemplate = "<b>%{label}</b> <br><b> %{percent}</b></br><b>%{value:,.0f}</b>",
                name='',
                rotation=10,
                )
        )    

        figure.update_layout(
            title={'text': f"<b>{title}</b>"},
            title_font_family="sans-serif", 
            title_font_size = 18,
            title_font_color = "rgba(0, 0, 0, 0.7)",
            template = template
        
        )
        figure.update_traces(textposition = textposition, textinfo = textinfo, hole = hole)
        figure.update_traces(hoverinfo='label+percent+value', textfont_size = textfont_size)
        figure.update_layout(height = height,margin = dict(t=20, b=60, l=60, r=60),showlegend = showlegend)
        figure.update_layout(legend=dict(
                                #orientation="h",
                                #yanchor="bottom",
                                #y=1.02,
                                #xanchor="right",
                                #x=1,
                                font=dict(size=10),
                            ))
        return figure

def pie_2(df = pd.DataFrame(),label_col = '', 
             value_col = '',list_or_color = None, dict_color = None,
             title = '', textinfo = 'percent+label+value' , textposition = 'inside',
             height = 300, showlegend = True, color_list = [], textfont_size = 12,hole=0, 
             ticked_hover = 'Importe',top = 60, template ="plotly_white"
             
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
                hovertemplate = '<b>%{label}</b><br>Porcentaje:<b> %{percent} </b></br>'+ticked_hover+': <b>%{value}</b>',
                name='',
                hole=hole
                )
        )    

        figure.update_layout(
            title={'text': f"<b>{title}</b>",'y':0.97,'x':0.5,'xanchor': 'center','yanchor': 'top'},
            title_font_family="sans-serif", 
            title_font_size = 18,
            title_font_color = "rgba(0, 0, 0, 0.7)",
            template = template
        
        )
        figure.update_traces(textposition = textposition, textinfo = textinfo)
        figure.update_traces(hoverinfo='label+percent+value', textfont_size = textfont_size,marker=dict(line=dict(color='#000000', width=1)))
        figure.update_layout(height = height,margin = dict(t=top, b=30, l=10, r=10),showlegend = showlegend)
        
        return figure
def figure_n_traces(df = None, height = 300 , trace = [],colors = [],ejex = [], hover_unified = True, template = "plotly_white"):
    fig = go.Figure()
    if len(ejex)==1:
        ejexx =df[ejex[0]]
    elif len(ejex)==2: 
        ejexx =[df[ejex[0]],df[ejex[1]]]#
    for value,color in zip(trace,colors):
        
        fig.add_trace(go.Scatter(
            x = ejexx,
            y = df[value],
            name = value,
            marker=dict(color=color),
            mode="markers+lines",
            cliponaxis=False,
            #hovertemplate ='<br><b>%{x}</b><br><b>%{y}</b>',
            hoverlabel=dict(font_size=16,bgcolor="white")
        ))
        if hover_unified == True:
            fig.update_layout(hovermode="x unified")
        else:
            fig.update_traces(hovertemplate ='<br><b>%{x}</b><br><b>%{y}</b>',hoverlabel=dict(font_size=15,bgcolor="white"))
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0
    ))
    fig.update_layout(
        #title = f"<b>{}</b>",
        title_font_family="sans-serif", 
        title_font_size = 18,
        height = height,
        template= template
        #title_text="STOCK VALORIZADO Y NRO ITEMS POR MES Y AÑO",
    )
    fig.update_xaxes(tickfont=dict(size=12),showticklabels = True,title_font_family="sans-serif",title_font_size = 12,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
    fig.update_yaxes(tickfont=dict(size=12),showticklabels = True,title_font_family="sans-serif",title_font_size = 12,automargin=True)  
    if len(ejex)==1:
        fig.update_layout(yaxis_tickformat = ',',margin = dict(t=20,b=60,r=20))
    elif len(ejex)==2: 
        fig.update_layout(yaxis_tickformat = ',',margin = dict(t=20,b=100,r=20))
    
    
    return fig

def create_stack_np(dataframe = pd.DataFrame(), lista = []):
    return np.stack(tuple(dataframe[elemento] for elemento in lista),axis = -1)



def bar_figure_d(dataframe = None, x = '', y = '', text = '', orientation = 'h', title = '', height = 450, showticklabels_x = True, showticklabels_y = True, template = "plotly_white"):
    fig = go.Figure()
    fig.add_trace(go.Bar(
      x = dataframe[x],
      y = dataframe[y],
      text = dataframe[text],
      name = "",
      textposition = 'outside',
      texttemplate="%{x}",
      orientation = orientation,
      cliponaxis = False,

      hovertemplate ='<br>'+y+': <b>%{y}</b><br>'+x+': <b>%{x}</b>',hoverlabel=dict(font_size=15,bgcolor="white")
    ))
    fig.update_layout(
        title = f"<b>{title}</b>",
        title_font_family="sans-serif", 
        title_font_size = 18,
        template= template,
        margin = dict( l = 20, r = 40, b = 40, t = 30, pad = 5, autoexpand = True),
        height = height
        #title_text="STOCK VALORIZADO Y NRO ITEMS POR MES Y AÑO",
    )
    fig.update_xaxes(tickfont=dict(size=12),showticklabels = showticklabels_x,title_font_family="sans-serif",title_font_size = 13,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
    fig.update_yaxes(tickfont=dict(size=12),showticklabels = showticklabels_y,title_font_family="sans-serif",title_font_size = 13,automargin=True)  
    fig.update_layout(xaxis_tickformat = ',')
    return fig

def figure_stock_var_y2(df = None, height = 450 , moneda = 'Soles', template ="plotly_white"):
    var_numerica = f'Stock Valorizado {moneda}'
    stock_var_df = df.groupby(['Año', 'Mes','Mes_'])[[var_numerica]].sum().sort_values(['Año','Mes_']).reset_index()
    stock_items_df = df.groupby(['Año', 'Mes','Mes_'])[[var_numerica]].count().sort_values(['Año','Mes_']).reset_index()
    stock_items_df = stock_items_df.rename(columns = {var_numerica:'Nro Items'})
    stock_var_items_df = stock_var_df.merge(stock_items_df,how = 'inner',on=["Año","Mes","Mes_"])
    fig = go.Figure()

    fig.add_trace(go.Bar(
    x = [stock_var_items_df['Año'],stock_var_items_df['Mes']],
    y = stock_var_items_df[var_numerica],
    name = "Stock Valorizado",
    cliponaxis=False,
    hovertemplate ='<br>'+'Periodo'+': <b>%{x}</b><br>'+var_numerica+': <b>%{y}</b>',hoverlabel=dict(font_size=15,bgcolor="white")
    ))
    fig.add_trace(
        go.Scatter(
            x=[stock_var_items_df['Año'],stock_var_items_df['Mes']],
            y=stock_var_items_df['Nro Items'],
            yaxis="y2",
            name="Nro Items",
            marker=dict(color="crimson"),
            cliponaxis=False,
            hovertemplate ='<br>'+'Periodo'+': <b>%{x}</b><br>'+'Nro Items'+': <b>%{y}</b>',hoverlabel=dict(font_size=15,bgcolor="white")
        )
    )
    fig.update_layout(
        #legend=dict(orientation="v"),
        yaxis=dict(
            title=dict(text="<b>Stock Valorizado</b>"),
            side="left",
            range=[0, stock_var_items_df[var_numerica].max()]
        ),
        yaxis2=dict(
            title=dict(text="<b>Nro Items</b>"),
            side="right",
            range=[0, stock_var_items_df['Nro Items'].max()],
            overlaying="y",
            tickmode="auto",
        ),
        template= template
    )
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0
    ))
    fig.update_layout(
        title = f"",
        title_font_family="sans-serif", 
        title_font_size = 18,
        height = height,
        margin = dict(t = 30, l = 90),
        #title_text="STOCK VALORIZADO Y NRO ITEMS POR MES Y AÑO",
    )
    fig.update_xaxes(tickfont=dict(size=14),showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
    fig.update_yaxes(tickfont=dict(size=14),showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True)  
    fig.update_layout(yaxis_tickformat = ',')
    return fig

def figure_bar_familia(df = None, height = 450, moneda = 'Soles', template = "plotly_white"):
    var_numerico = f'Stock Valorizado {moneda}'
    stock_familias_df = df.groupby(['Grupo Producto'])[[var_numerico]].sum().sort_values(var_numerico,ascending=True).reset_index()
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
    x = stock_familias_df[var_numerico],
    y = stock_familias_df['Grupo Producto'],
    text = stock_familias_df[var_numerico],
    name = "",
    textposition = 'outside',
    texttemplate="%{x}",
    orientation='h',
    cliponaxis=False,
    
    hovertemplate ='<br>'+'Grupo Producto'+': <b>%{y}</b><br>'+var_numerico+': <b>%{x}</b>',hoverlabel=dict(font_size=15,bgcolor="white")
    ))
    fig2.update_layout(
        title = f"",
        title_font_family="sans-serif", 
        title_font_size = 18,
        template= template,
        margin = dict( l = 20, r = 40, b = 20, t = 30, pad = 1, autoexpand = True),
        height = height
        #title_text="STOCK VALORIZADO Y NRO ITEMS POR MES Y AÑO",
    )
    fig2.update_xaxes(tickfont=dict(size=12),showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
    fig2.update_yaxes(tickfont=dict(size=12),showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True)  
    fig2.update_layout(xaxis_tickformat = ',')
    return fig2

def figure_bar_top_producto(df = None, height = 450, moneda = 'Soles',template = "plotly_white"):
    var_numerico = f'Stock Valorizado {moneda}'
    top_10_df= df.groupby(['Producto'])[[var_numerico]].sum().sort_values([var_numerico],ascending = True).tail(10).reset_index()
    return bar_figure_d(dataframe = top_10_df, x = var_numerico, y = 'Producto', text = var_numerico, orientation = 'h', title = '', height = height,showticklabels_y = False,template=template)

def figure_bar_relative(df = None, height = 300, eje_color = 'ABC Ventas', title = '',moneda = 'Soles',template = "plotly_white"):
    var_numerico = f'Stock Valorizado {moneda}'
    stock_abc_dff=df.groupby(['Año', 'Mes','Mes_',eje_color])[[var_numerico]].sum().sort_values(['Año','Mes_']).reset_index()
    lista_letras = sorted(stock_abc_dff[eje_color].unique())
    pivot_stick_adc_dff=stock_abc_dff.pivot_table(index=['Año', 'Mes','Mes_'],values=(var_numerico),columns=(eje_color)).sort_values(['Año','Mes_']).reset_index()
    for letra in lista_letras:
        pivot_stick_adc_dff[f'{letra} %'] = pivot_stick_adc_dff[letra]/(pivot_stick_adc_dff[lista_letras].sum(axis=1))
    #pivot_stick_adc_dff['B %'] = pivot_stick_adc_dff['B']/(pivot_stick_adc_dff[['A','B','C']].sum(axis=1))
    #pivot_stick_adc_dff['C %'] = pivot_stick_adc_dff['C']/(pivot_stick_adc_dff[['A','B','C']].sum(axis=1))
    x_stock_abc = [pivot_stick_adc_dff['Año'],pivot_stick_adc_dff['Mes']]
    fig_e = go.Figure()
    for letra in lista_letras:
        fig_e.add_bar(x = x_stock_abc,
                    y = pivot_stick_adc_dff[f'{letra} %'],
                    name = letra,
                    customdata=create_stack_np(pivot_stick_adc_dff,letra),
                    hovertemplate ='<br>'+'Periodo'+': <b>%{x}</b><br>'+''+' <b>%{y}</b>'+'<br>'+letra+': <b>%{customdata[0]:,.0f}</b><br>',
                                    
                    #hoverlabel=dict(font_size=15,bgcolor="white")
                    )

    fig_e.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0
    ))
    fig_e.update_layout(
        title = f"<b>{title}</b>",
        title_font_family="sans-serif", 
        title_font_size = 18,
        margin = dict( l = 50, r = 40, b = 70, t = 25, pad = 5, autoexpand = True),
        height = height,
        
        #title_text="STOCK VALORIZADO Y NRO ITEMS POR MES Y AÑO",
    )
    fig_e.update_layout(barmode="relative")
    fig_e.update_layout(yaxis_tickformat = '.0%', template=template)
    return fig_e

def figure_pie_rango_stock(df = None, height = 350, moneda = 'Soles',template = "plotly_white"):
    var_numerico = f'Stock Valorizado {moneda}'
    rango_stock_df = df.groupby(['Rango antigüedad del stock'])[[var_numerico]].sum().sort_values(['Rango antigüedad del stock']).reset_index()
    return pie_2(df = rango_stock_df, label_col = 'Rango antigüedad del stock', value_col = var_numerico,
             title = '', textinfo = 'percent+label' , textposition = 'inside',
             height = height, showlegend = False, textfont_size = 12,top=20,
             ticked_hover=var_numerico,template=template
    )
    
def figure_pie_rango_stock_count(df = None, height = 350, moneda = 'Soles', template = "plotly_white"):
    var_numerico = f'Stock Valorizado {moneda}'
    rango_stock_count_df = df.groupby(['Rango antigüedad del stock'])[['Producto']].count().sort_values(['Rango antigüedad del stock']).reset_index()
    return pie_2(df = rango_stock_count_df, label_col = 'Rango antigüedad del stock', value_col = 'Producto',
             title = '', textinfo = 'percent+label' , textposition = 'inside',
             height = height, showlegend = False, textfont_size = 12,top=20,
             hole = .6     ,ticked_hover = 'N° Items',template= template
    )
##############################ALM

def figure_stock_alm_y2(df = None, height = 450 , moneda = 'Importe Dolares', tipo = 'Grupo', template= 'plotly_white'):
    tipo_alm_dff = df.groupby([tipo])[['Stock', moneda]].sum().sort_values(moneda,ascending = False).reset_index()
    #tipo_alm_dff = tipo_alm_dff[tipo_alm_dff['Stock']>0]
    fig = go.Figure()

    fig.add_trace(go.Bar(
    x = tipo_alm_dff[tipo],
    y = tipo_alm_dff[moneda],
    name = moneda,
    cliponaxis=False,
    hovertemplate ='<br>'+tipo+': <b>%{x}</b><br>'+moneda+': <b>%{y}</b>',hoverlabel=dict(font_size=15,bgcolor="white")
    ))
    fig.add_trace(
        go.Scatter(
            x=tipo_alm_dff[tipo],
            y=tipo_alm_dff['Stock'],
            yaxis="y2",
            name='Stock',
            marker=dict(color="crimson"),
            cliponaxis=False,
            hovertemplate ='<br>'+tipo+': <b>%{x}</b><br>'+'Stock'+': <b>%{y}</b>',hoverlabel=dict(font_size=15,bgcolor="white")
        )
    )
    fig.update_layout(
        #legend=dict(orientation="v"),
        yaxis=dict(
            title=dict(text=moneda),
            side="left",
            range=[0, tipo_alm_dff[moneda].max()]
        ),
        yaxis2=dict(
            title=dict(text='Stock'),
            side="right",
            range=[0, tipo_alm_dff['Stock'].max()],
            overlaying="y",
            tickmode="auto",
        ),
        template= template
    )
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    fig.update_layout(
        title = f"<b>{tipo} por {moneda} y Stock </b>",
        title_font_family="sans-serif", 
        title_font_size = 18,
        height = height
        #title_text="STOCK VALORIZADO Y NRO ITEMS POR MES Y AÑO",
    )
    fig.update_xaxes(tickfont=dict(size=11),showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
    fig.update_yaxes(tickfont=dict(size=12),showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True)  
    fig.update_layout(yaxis_tickformat = ',')
    fig.update_layout(yaxis2_tickformat = ',')
    size_list = len(tipo_alm_dff[tipo].unique())
    if  size_list== 1:
            fig.update_layout(bargap=0.7)
    elif size_list== 2:
            fig.update_layout(bargap=0.4)
    elif size_list== 3:
            fig.update_layout(bargap=0.3)
    return fig
    

def figure_pie_estado_inv(df = None, height = 330, template= 'plotly_white'):
    print(df.columns)
    pie_estado_inv_dff = df.groupby(['Estado Inventario'])[['Tipo']].count().reset_index()
    pie_estado_inv_dff = pie_estado_inv_dff.rename(columns = {'Tipo':'Número de Registros'})
    
    return pie_2(df = pie_estado_inv_dff, label_col = 'Estado Inventario', value_col = 'Número de Registros',
             title = '', textinfo = 'percent+label' , textposition = 'outside',
             height = height, showlegend = False, color_list = px.colors.qualitative.Set3, textfont_size = 12,
             hole = .6,top=20 ,template= template
    )


def figure_bar_responsable(df = None, height = 450, template= 'plotly_white'):
    
    responsable_df = df.groupby(['Responsable Ingreso'])[['Tipo']].count().sort_values('Tipo',ascending=True).reset_index()
    responsable_df = responsable_df.rename(columns = {'Tipo':'Número de Registros'})
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
    x = responsable_df['Número de Registros'],
    y = responsable_df['Responsable Ingreso'],
    text = responsable_df['Número de Registros'],
    name = "",
    textposition = 'outside',
    texttemplate="%{x}",
    orientation='h',
    cliponaxis=False,
    
    hovertemplate ='<br>'+'Responsable Ingreso'+': <b>%{y}</b><br>Número de Registros: <b>%{x}</b>',hoverlabel=dict(font_size=15,bgcolor="white")
    ))
    fig2.update_layout(
        title = f"",
        title_font_family="sans-serif", 
        title_font_size = 18,
        template= template,
        margin = dict( l = 20, r = 40, b = 40, t = 30, pad = 5, autoexpand = True),
        height = height
        #title_text="STOCK VALORIZADO Y NRO ITEMS POR MES Y AÑO",
    )
    fig2.update_xaxes(tickfont=dict(size=12),showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
    fig2.update_yaxes(tickfont=dict(size=12),showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True)  
    fig2.update_layout(xaxis_tickformat = ',')
    return fig2

##########################################################################

def bar_logistica_y1(df = None, height = 450 , moneda = 'Soles', template ="plotly_white"):

    fig = go.Figure()
    #'Meses Inventario','Inventario Valorizado'
    fig.add_trace(go.Bar(
    x = df['DESCRIPCION'],
    y = df['Meses Inventario'],
    name = "Meses Inventario",
    cliponaxis=False,
    marker=dict(color="#3aa99b"),
    hovertemplate ='<br>'+'Producto'+': <b>%{x}</b><br>'+'Meses Inventario'+': <b>%{y}</b>',hoverlabel=dict(font_size=13,bgcolor="white")
    ))
    
    fig.update_layout(
        #legend=dict(orientation="v"),
        #'<b>'+xaxis_title+'</b>'
        yaxis=dict(
            title=dict(text='<b>'+'Meses Inventario'+'</b>'),
            side="left",
            range=[0, df['Meses Inventario'].max()]
        ),
        
        template= 'none',
        xaxis_title='<b>'+'Producto'+'</b>',
    )
    
    fig.update_layout(
        title = f"",
        title_font_family="sans-serif", 
        title_font_size = 18,
        height = height,
        template = template
        #title_text="STOCK VALORIZADO Y NRO ITEMS POR MES Y AÑO",
    )
    fig.update_xaxes(tickfont=dict(size=13),showticklabels = False,title_font_family="sans-serif",title_font_size = 13,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
    fig.update_yaxes(tickfont=dict(size=13),showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True)  
    fig.update_layout(yaxis_tickformat = ',')
    fig.update_layout(margin=dict(r = 40, b = 40 , t = 20))
    return fig

def bar_logistica_y2(df = None, height = 450 , moneda = 'Soles', y_col = ''):

    fig = go.Figure()
    #'Meses Inventario','Inventario Valorizado'
    fig.add_trace(go.Bar(
    x = df['DESCRIPCION'],
    y = df[y_col],
    name = 'Inventario Valorizado',
    cliponaxis=False,
    marker=dict(color="#5175c7"),
    hovertemplate ='<br>'+'Producto'+': <b>%{x}</b><br>'+'Inventario Valorizado'+': <b>%{y:,.2f}</b>',hoverlabel=dict(font_size=13,bgcolor="white")
    ))
    fig.add_trace(
        go.Scatter(
            x= df['DESCRIPCION'],
            y= df['Meses Inventario'],
            yaxis="y2",
            name="Meses de Inventario",
            marker=dict(color="#3aa99b"),
            cliponaxis=False,
            hovertemplate ='<br>'+'Producto'+': <b>%{x}</b><br>'+'Meses de Inventario'+': <b>%{y}</b>',hoverlabel=dict(font_size=13,bgcolor="white")
        )
    )
    fig.update_layout(
        #legend=dict(orientation="v"),
        #'<b>'+xaxis_title+'</b>'
        yaxis=dict(
            title=dict(text='<b>'+'Inventario Valorizado'+'</b>'),
            side="left",
            range=[0, df[y_col].max()]
        ),
        yaxis2=dict(
            title=dict(text='<b>'+'Meses Inventario'+'</b>'),
            side="right",
            range=[0, df['Meses Inventario'].max()],
            overlaying="y",
            tickmode="auto",
        ),
        template= 'none',
        xaxis_title='<b>'+'Producto'+'</b>',
    )
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    fig.update_layout(
        title = f"<b>Variación de Inventario Valorizado</b>",
        title_font_family="sans-serif", 
        title_font_size = 18,
        height = height,
        template = 'plotly_white'
        #title_text="STOCK VALORIZADO Y NRO ITEMS POR MES Y AÑO",
    )
    fig.update_xaxes(tickfont=dict(size=13),showticklabels = False,title_font_family="sans-serif",title_font_size = 13,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
    fig.update_yaxes(tickfont=dict(size=13),showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True)  
    fig.update_layout(yaxis_tickformat = ',')
    fig.update_layout(margin=dict(b = 40))
    
    return fig

def bar_horizontal(df = None, height = 350 , x = '',y = '',name_x = '',name_y = '',color = '#3aa99b', title = '', template ="plotly_white"):

    fig = go.Figure()
    #'Meses Inventario','Inventario Valorizado'
    fig.add_trace(go.Bar(
    x = df[x],
    y = df[y],
    name = '',
    cliponaxis=False,
    marker=dict(color = color,cornerradius=15),
    hovertemplate ='<br>'+name_y+': <b>%{y}</b><br>'+name_x+': <b>%{x:,.1f}</b>',hoverlabel=dict(font_size=13,bgcolor="white"),
    orientation='h'
    ))
    
    fig.update_layout(
        #legend=dict(orientation="v"),
        #'<b>'+xaxis_title+'</b>'
        yaxis=dict(
            title=dict(text='<b>'+name_y+'</b>'),
            side="left",
            #range=[0, df['Meses Inventario'].max()]
        ),
        
        xaxis_title='<b>'+name_x+'</b>',
    )
    
    fig.update_layout(
        title = f"<b>{title}</b>",
        title_font_family="sans-serif", 
        title_font_size = 14,
        height = height,
        template = template
        #title_text="STOCK VALORIZADO Y NRO ITEMS POR MES Y AÑO",
    )
    fig.update_xaxes(tickfont=dict(size=11),showticklabels = True,title_font_family="sans-serif",title_font_size = 12,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
    fig.update_yaxes(tickfont=dict(size=11),showticklabels = True,title_font_family="sans-serif",title_font_size = 12,automargin=True)  
    fig.update_layout(yaxis_tickformat = ',')
    fig.update_layout(margin=dict(r = 20, b = 40, t = 30))
    return fig

#######################################################
DICT_CULTIVOS_COLOR={'Arandano':'#7A325A',
               'Esparrago':'#87AA6C',
               'Uva':'#AF799F',
               'Palta':'#527E03',
               'Compost':'#5F524B',
               'Mandarina':'#F74628',
               'Frambuesa':'#DE194D',
               'Algodon':"#ccddb8",
               'Quinua':"#E3C08C",
                'Granada':"#D77477",
                'Ensayos':"#000000",
               'Naranja':"#ffbf75",
               'Palto':"#527E03",
               'Zarzamora':"#ff35c2",
               'Duraznos':"#e4c5c4",                
               'Maiz':"#f4ff91",
               'Ninguno':"#1d3d33",
               'Ciruelo':"#ff5f7c",
               'Manzano':"#9dc09d",
               'Kaki':"#e6a15c",
               'Arandanos':"#b93af8",
               'Tangelo':"#fd971c",
               'Lima':"#97db51",
               'Citrico':"#a0fb0e",
               'Granada':"#d35d1d",
               'Palto p roduccion':"#527E03",
               'Zapallo':"#cbe03d",
               'Limon':"#93EE59",
               'Pecana':"#b16d57",
               'Mango': "#bb2328"

              }

def create_hover_custom(lista = []):
    string_hover = ''
    for i,element in zip(range(len(lista)),lista):
         if element == 'AREA_CAMPAÑA' or element == 'AREA' or element == 'Area':
               string_hover = string_hover+'<br>'+element+': <b>%{customdata['+str(i)+']:,.2f}</b>'
         else:
               string_hover = string_hover+'<br>'+element+': <b>%{customdata['+str(i)+']}</b>'   
    return string_hover

def bar_comercial(df = pd.DataFrame(), x = '', y = '', text = '', orientation = 'v', height = 400 ,
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
        figure.update_xaxes(tickfont=dict(size=size_tickfont),showticklabels = showticklabel_x,title_font_family="sans-serif",title_font_size = 13,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
        figure.update_yaxes(tickfont=dict(size=size_tickfont),showticklabels = showticklabel_y,title_font_family="sans-serif",title_font_size = 13,automargin=True)  
        figure.update_layout(autosize=True,margin=dict(l = left, r = 40, b= 40, t = 20, ) )#
        if  size_list== 1:
            figure.update_layout(bargap=0.7)
        elif size_list== 2:
            figure.update_layout(bargap=0.4)
        elif size_list== 3:
            figure.update_layout(bargap=0.3)

        return figure

def funnel_comercial(df = pd.DataFrame(), x = '', y = '', text = '', height = 400 ,
        title = '', xaxis_title = '',yaxis_title = '', showticklabel_x = True, 
        showticklabel_y = True ,list_or_color = [],
        template = 'plotly_white',size_tickfont = 11,
        plot_bgcolor = 'white', paper_bgcolor = 'white',ticklabel_color = 'rgba(0, 0, 0, 0.7)'
    ):  
        
        figure = go.Figure(go.Funnel(
                    y = df[y],
                    x = df[x],
                    name='',
                    textposition = "outside",
                    textinfo = "value+percent total",
                    hovertemplate='<br>'+y+': <b>%{y}</b><br>'+x+':<b> %{x:,.2f}</b>',
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
                title_font_family="sans-serif", 
                title_font_size = 18,
                title_font_color = "rgba(0, 0, 0, 0.7)",
                height = height, 
        )
        figure.update_xaxes(tickfont=dict(size=size_tickfont),showticklabels = showticklabel_x,title_font_family="sans-serif",title_font_size = 13,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
        figure.update_yaxes(tickfont=dict(size=size_tickfont),showticklabels = showticklabel_y,title_font_family="sans-serif",title_font_size = 13,automargin=True)
        figure.update_layout(margin=dict(l = 50, r = 40, b= 20, t = 20, pad = 1))
        return figure

def pie_comercial(df = pd.DataFrame(),label_col = '', 
             value_col = '',list_or_color = None, dict_color = None,
             title = '', textinfo = 'percent+label+value' , textposition = 'inside',
             height = 300, showlegend = True, color_list = [], textfont_size = 12,
             plot_bgcolor = 'white', paper_bgcolor = 'white',top = 40, template = "plotly_white"
             
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
            template = template
        
        )
        figure.update_traces(textposition = textposition, textinfo = textinfo)
        figure.update_traces(hoverinfo='label+percent+value', textfont_size = textfont_size,marker=dict(line=dict(width=1)))
        figure.update_layout(height = height,margin = dict(t=top, b=30, l=30, r=30),showlegend = showlegend)
        return figure

def bar_chart(df = None,x = '',y = '', height = 450 , titulo = '' , name = '', color = '#3aa99b', orientacion = 'v',template = "plotly_white"):

    fig = go.Figure()
    #'Meses Inventario','Inventario Valorizado'
    fig.add_trace(go.Bar(
    x = df[x],
    y = df[y],
    name = name,
    cliponaxis=False,
    marker=dict(color = color),
    hovertemplate ='<br>'+x+': <b>%{x}</b><br>'+y+': <b>%{y}</b>',hoverlabel=dict(font_size=13,bgcolor="white"),
    orientation=orientacion,
    ))
    
    fig.update_layout(
        #legend=dict(orientation="v"),
        #'<b>'+xaxis_title+'</b>'
        yaxis=dict(
            title=dict(text='<b>'+y+'</b>'),
            side="left",
            
        ),
        
        template= template,
        xaxis_title='<b>'+x+'</b>',
    )
    
    fig.update_layout(
        title = f"<b>{titulo}</b>",
        title_font_family="sans-serif", 
        title_font_size = 18,
        height = height,
        #title_text="STOCK VALORIZADO Y NRO ITEMS POR MES Y AÑO",
    )
    fig.update_xaxes(tickfont=dict(size=12),showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
    fig.update_yaxes(tickfont=dict(size=12),showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True)  
    if orientacion == 'h':
        fig.update_layout(xaxis_tickformat = ',')
    elif orientacion == 'v':
        fig.update_layout(yaxis_tickformat = ',')
    fig.update_layout(margin=dict(r = 40, b = 40, t=20)),
    fig.update_traces(
                    #marker_line_color='black',
                    #marker_line_width=1, 
                    opacity=0.8
    )
    return fig