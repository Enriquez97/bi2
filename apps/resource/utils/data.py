import base64 
import pandas as pd
from PIL import Image
from io import BytesIO

def mes_short(x):
    dict_mes = {1:'Ene',2:'Feb',3:'Mar',4:'Abr',5:'May',6:'Jun',7:'Jul',8:'Ago',9:'Set',10:'Oct',11:'Nov',12:'Dic'}
    return dict_mes[x] 

def values_default(list_cols = []):
    default_list = []
    for col in list_cols:
        if col in ["int", "float","int64","float64"]:
            default_list.append(0)
        else :
            default_list.append("No Especificado")
    return default_list

def num_type_data(lista= []):
    list_var_num = []
    list_var_cate = []
    list_var_fecha = []
    for type_column in lista:
        if type_column in ["int64","float64","float","int"]:
            list_var_num.append(type_column)
        elif type_column in ["object","string"]:
            list_var_cate.append(type_column)
        elif type_column in ["datetime64","timedelta[ns]"]:
            list_var_fecha.append(type_column)
    return len(list_var_num),len(list_var_cate),len(list_var_fecha)

def dict_rename(df = None ):
    rename_dict = {}
    for col, col_edit in zip(df['Fuente_Column'].values,df['Columns'].values):
        if col != col_edit:
            rename_dict[col]= col_edit
    return rename_dict

def clear_spaces(df = None):
    dff = df.copy()
    for column in dff.columns:
        try:
            dff[column] = dff[column].str.strip()
        except:
            pass
    return dff

def change_dtypes(df = None,df_config = None):
    dff = df.copy()
    list_f_dtype = df_config['Fuente_Dtype'].values
    list_dtype = df_config['Tipo Dato'].values
    for column,f_dtype,dtype in zip(dff.columns,list_f_dtype,list_dtype):
        if f_dtype != dtype:
            try:
                dff[column] = dff[column].astype(dtype)
            except:
                pass
    return dff  

def complete_values(df = None,df_config = None):
    dff = df.copy()
    list_default_value = df_config['Value default'].values
    for column, value_default in zip(dff.columns,list_default_value):
        try:
            dff[column] = dff[column].fillna(value_default)
            try:
                dff[column] = dff[column].replace([''],[value_default])
            except:
                pass
        except:
            pass
    return dff



def decoding_avatar(img_code = None,width = 200, height = 50): 
    code = base64.b64decode(img_code)
    return Image.open(BytesIO(code)).resize((width, height))


def transform_fecha_col(df = None, col_fecha = None):
    columns = list(df.columns)
    if columns[-1] == "Año":
        pass
    else:
        try:
            df[col_fecha] = pd.to_datetime(df[col_fecha].str[:-14], format="%Y-%m-%d")
        except:
            df[col_fecha] = pd.to_datetime(df[col_fecha], format="%Y-%m-%d")
            
        df['Dia'] = df[col_fecha].dt.day
        df['Mes_'] = df[col_fecha].dt.month
        df['Mes'] = df['Mes_']
        df['Mes'] = df.apply(lambda x: mes_short(x['Mes']),axis=1)
        df['Año'] =df[col_fecha].dt.year
        return df 
    #dataframe.apply(lambda x: semana_text(x['Año'], x['Semana_']),axis=1)