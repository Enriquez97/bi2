from ..utils.data import *
import pandas as pd 
def config_data(dataframe = pd.DataFrame,config = None):
    df_config = pd.DataFrame(config)

    df = dataframe.rename(columns = dict_rename(df_config))

    df = clear_spaces(df)

    dataframe = change_dtypes(df,df_config)

    dataframe = complete_values(dataframe,df_config)
    delete_columns = list(df_config[df_config['Estado']=="Inactive"]['Columns'].values)
    if len(delete_columns) != 0:
        
        dataframe = dataframe.drop(delete_columns,axis=1)
    return dataframe