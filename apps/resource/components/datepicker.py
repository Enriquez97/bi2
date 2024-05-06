import dash_mantine_components as dmc
import pandas as pd
import numpy as np
from dash import html
from datetime import datetime, date, timedelta


def datepicker_alm(dataframe = pd.DataFrame(), value_col = 'Última Fecha Ingreso', text = '', tipo = 'inicio'):
    fecha_now = date(datetime.now().year,datetime.now().month,datetime.now().day)
    dataframe[value_col]=dataframe[value_col].apply(lambda a: pd.to_datetime(a).date())
    fecha_minima=str(dataframe[value_col].fillna(fecha_now).min())
    #fecha_minima = str('2023-07-07')
    #fecha_maxima = str('2023-11-09')
    fecha_maxima=str(dataframe[value_col].max())
    
    text_value = dataframe[value_col].min() if tipo == 'inicio' else dataframe[value_col].max()
    text_id = 'inicio' if tipo == 'inicio' else 'fin'
    return  html.Div([
        dmc.DatePicker(
            id=f'datepicker-{text_id}',
            label = text,
                        #description="You can also provide a description",
            minDate = date(int(fecha_minima[:4]),int(fecha_minima[-5:-3]),int(fecha_minima[-2:])),
            maxDate = date(int(fecha_maxima[:4]),int(fecha_maxima[-5:-3]),int(fecha_maxima[-2:])),
            value = text_value,
            locale = "es",
            clearable = False,     
            ),
    ])



